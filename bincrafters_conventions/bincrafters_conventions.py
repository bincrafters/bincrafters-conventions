#!/usr/bin/env python

import argparse
import os
import sys
import logging
import git
import tempfile
import requests
import contextlib
import re
from conans.client import conan_api
from conans.errors import ConanException
from .actions.check_for_spdx_license import check_for_spdx_license
from .actions.check_for_download_hash import check_for_download_hash
from .actions.check_for_license import check_for_license
from .actions.check_for_deprecated_generators import check_for_deprecated_generators
from .actions.check_for_deprecated_methods import check_for_deprecated_methods
from .actions.check_for_deprecated_settings import check_for_deprecated_settings
from .actions.check_for_required_attributes import check_for_required_attributes
from .actions.update_a_python_version import update_a_python_version
from .actions.update_a_path_manipulation import update_a_path_manipulation
from .actions.update_a_python_environment_variable import update_a_python_environment_variable
from .actions.update_a_jobs import update_a_jobs
from .actions.update_azp_jobs import update_azp_jobs
from .actions.update_gha import update_gha
from .actions.update_c_attributes import update_c_delete_author, update_c_topics
from .actions.update_c_deprecated_attributes import update_c_deprecated_attributes
from .actions.update_c_openssl_version_patch import update_c_openssl_version_patch
from .actions.update_c_default_options_to_dict import update_c_default_options_to_dict
from .actions.update_c_delete_meta_lines import update_c_delete_meta_lines
from .actions.update_c_tools_version import update_c_tools_version
from .actions.update_c_recipe_references import update_c_recipe_references
from .actions.update_c_remove_compiler_cppstd import update_c_remove_compiler_cppstd
from .actions.update_t_ci_dir_path import update_t_ci_dir_path
from .actions.update_t_macos_images import update_t_macos_images
from .actions.update_t_new_docker_image_names import update_t_new_docker_image_names
from .actions.update_t_jobs import update_t_jobs
from .actions.update_t_linux_image import update_t_linux_image
from .actions.update_t_linux_python_version import update_t_linux_python_version
from .actions.update_other_travis_to_ci_dir_name import update_other_travis_to_ci_dir_name
from .actions.update_other_pyenv_python_version import update_other_pyenv_python_version
from .actions.update_readme_travis_url import update_readme_travis_url


__version__ = '0.18.5'
__author__ = 'Bincrafters <bincrafters@gmail.com>'
__license__ = 'MIT'

LOGGING_FORMAT = '[%(levelname)s]\t%(asctime)s %(message)s'
LOGGING_LEVEL = os.getenv("BINCRAFTERS_LOGGING_LEVEL", logging.INFO)
logging.basicConfig(level=int(LOGGING_LEVEL), format=LOGGING_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

# Python version for updating files
python_version_current_pyenv = "3.7.1"
python_version_current_appveyor = "37"
python_version_current_travis_linux = "3.7"
# for AppVeyor dot zero releases need to be added without dot zero, for pyenv a second time with a dot zero
python_check_for_old_versions = ["2.7.8", "2.7.10", "2.7.14", "2.7", "3.6", "3.7.0"]  # TODO: Remove this


# Current GitHub Actions Bincrafters workflow versions
gha_workflow_version = "1"

# Sometimes Travis is publishing new CI images with new XCode versions
# but they still have the same Clang version
# in this case we do NOT need to add new compiler versions and therefore jobs
# but we need to update the existing jobs
travis_macos_images_updates = [["9.3", "9.4"], ["10", "10.3"], ["10.1", "10.3"], ["10.2", "10.3"], ["11", "11.3"],
                               ["11.2", "11.3"]]

# What apple_clang version is available on which Travis image? What MSVC versions are available on which AppVeyor image?
travis_macos_images_compiler_mapping = {'7.3': '7.3', '8.1': '8.3', '9.0': '9', '9.1': '9.4', '10.0': '10.3', '11.0': '11.3'}
appveyor_win_msvc_images_compiler_mapping = {'12': '2015', '14': '2015', '15': '2017', '16': '2019'}

# This compiler versions are getting added if they are newer than the existing jobs
# and if they don't already exist
compiler_versions = {'gcc': ('6', '7', '8', '9'),
                     'clang': ('5.0', '6.0', '7.0', '8', '9'),
                     'apple_clang': ('9.1', '10.0', '11.0'),
                     'visual': ('15', '16')}
# This compiler versions are getting actively removed from existing jobs
compiler_versions_deletion = {'gcc': (), 'clang': (), 'apple_clang': ('7.3', '8.1', '9.0'), 'visual': ('12',)}


# What are the latest AVAILABLE patches for OpenSSL, which versions are End-Of-Life?
openssl_version_matrix = {'1.0.1': {'latest_patch': 'h', 'eol': True},
                          '1.0.2': {'latest_patch': 'u', 'eol': True},
                          '1.1.0': {'latest_patch': 'l', 'eol': True},
                          '1.1.1': {'latest_patch': 'd', 'eol': False},
                          }

@contextlib.contextmanager
def chdir(newdir):
    """ Change directory using locked scope

    :param newdir: Temporary folder to move
    """
    old_path = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(old_path)


class Command(object):
    """ Execute Travis file update
    """

    def __init__(self):
        """ Fill regex compiler
        """
        self._logger = logging.getLogger(__file__)
        self._logger.setLevel(logging.INFO)

    def _parse_arguments(self, *args):
        """ Add program arguments

        :param args: User arguments
        """
        parser = argparse.ArgumentParser(description="Bincrafters Conventions")
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--remote', type=str, help='Github repo to be updated e.g. bincrafters/conan-foobar')
        group.add_argument('--local', action='store_true', help='Update current local repository')
        group.add_argument('-t', '--travisfile', type=str, nargs='?', const='.travis.yml',
                           help='Travis file to be updated e.g. .travis.yml')
        group.add_argument('-a', '--appveyorfile', type=str, nargs='?', const='appveyor.yml',
                           help='Appveyor file to be updated e.g. appveyor.yml')
        group.add_argument('-azp', '--azpfile', type=str, nargs='?', const='azure-pipelines.yml',
                           help='Azure Pipelines file to be updated e.g. azure-pipelines.yml')
        group.add_argument('-gha', '--ghafile', type=str, nargs='?', const=os.path.join(".github", "workflows", "conan.yml"),
                           help='GitHub Actions file to be updated e.g. .github/workflows/conan.yml')
        group.add_argument('--conanfile', '-c', type=str, nargs='?', const='conanfile.py',
                           help='Conan recipe path e.g conanfile.py')
        group.add_argument('--check', action='store_true', help='Checks for additional conventions')
        parser.add_argument('--all-branches', action='store_true', default=False,
                            help='Remote only, update all branches')
        parser.add_argument('--dry-run', '-d', action='store_true', default=False,
                            help='Do not push after update from remote')
        parser.add_argument('--project-pattern', '-pp', type=str,
                            help='Project pattern to filter over user projects e.g bincrafters/conan-*')
        parser.add_argument('--branch-pattern', '-bp', type=str,
                            help='Branch pattern to filter over user projects e.g stable/*')
        parser.add_argument('--remote-token', type=str,
                            help='Remote only, user:token pair for auth')
        parser.add_argument('--remote-max-repos', '-rmr', type=int, default=3,
                            help='Remote only, max amount of repositories which should get updated. Default: 3')
        group.add_argument('--version', '-v', action='version', version='%(prog)s {}'.format(__version__))
        args = parser.parse_args(*args)
        return args

    def run(self, *args):
        """ Process file update

        :param args: User arguments
        """
        arguments = self._parse_arguments(*args)
        if not len(sys.argv) > 1 or arguments.local:
            self._update_compiler_jobs(".travis.yml")
            self._update_appveyor_file("appveyor.yml")
            self._update_azp_file("azure-pipelines.yml")
            self._update_gha_file(os.path.join(".github", "workflows", "conan.yml"))
            self._update_conanfile("conanfile.py")
            self._update_readme("README.md")
            self._run_conventions_checks()
        else:
            if arguments.remote:
                self._update_remote(arguments.remote, arguments.conanfile, arguments.dry_run, arguments.project_pattern,
                                    arguments.branch_pattern, arguments.all_branches, arguments.remote_token,
                                    arguments.remote_max_repos)
            else:
                if arguments.check:
                    self._run_conventions_checks()
                else:
                    if arguments.conanfile:
                        self._update_conanfile(arguments.conanfile)
                    if arguments.travisfile:
                        self._update_compiler_jobs(arguments.travisfile)
                    if arguments.appveyorfile:
                        self._update_appveyor_file(arguments.appveyorfile)
                    if arguments.azpfile:
                        self._update_azp_file(arguments.azpfile)
                    if arguments.ghafile:
                        self._update_gha_file(arguments.ghafile)

    def _update_compiler_jobs(self, file):
        """ Read Travis file and compiler jobs

        :param file: Travis file path
        """

        if not os.path.isfile(file):
            return [False, ]

        result = []

        result.extend([
            # Rename .travis -> .ci
            update_other_travis_to_ci_dir_name(self),
            update_t_ci_dir_path(self, file),
            # Update which Python version macOS is using via pyenv
            update_other_pyenv_python_version(self, '.ci/install.sh', python_version_current_pyenv,
                                              python_check_for_old_versions),
            # Update Travis Linux Python version
            update_t_linux_python_version(self, file, python_version_current_travis_linux, python_check_for_old_versions),
            # Update which macOS image existing jobs are using
            update_t_macos_images(self, file, travis_macos_images_updates),
            # Update docker image names lasote -> conanio
            update_t_new_docker_image_names(self, file),
            # Update Travis Linux CI base image
            update_t_linux_image(self, file),
        ])

        if self._is_getting_new_compiler_versions("conanfile.py"):
            result.extend([update_t_jobs(self, file, compiler_versions, travis_macos_images_compiler_mapping,
                          compiler_versions_deletion)])

        return result

    def _update_appveyor_file(self, file):
        if not os.path.isfile(file):
            return [False, ]

        result = [
            update_a_python_environment_variable(self, file),
            update_a_python_version(self, file, python_version_current_appveyor, python_check_for_old_versions),
            update_a_path_manipulation(self, file),
        ]

        if self._is_getting_new_compiler_versions("conanfile.py"):
            # Add new compiler versions to CI jobs
            result.extend([
                update_a_jobs(self, file, compiler_versions, appveyor_win_msvc_images_compiler_mapping, compiler_versions_deletion)
            ])

        return result

    def _update_azp_file(self, file):
        if not os.path.isfile(file):
            return [False, ]

        result = []

        if self._is_getting_new_compiler_versions("conanfile.py"):
            # Add new compiler versions to CI jobs
            result.extend([
                update_azp_jobs(self, file, compiler_versions, appveyor_win_msvc_images_compiler_mapping, compiler_versions_deletion)
            ])

        return result

    def _update_gha_file(self, gha_file):
        if not os.path.isfile(gha_file):
            return [False, ]

        result = []

        result.extend([
            update_gha(self, gha_file, gha_workflow_version)
        ])

        return result

    def replace_in_file(self, file, old, new):
        """ Read file and replace ALL occurrences of old by new

        :param file: target file
        :param old: pattern to match
        :param new: new string to be used
        :return: True if was replaced. Otherwise, False.
        """
        result = False
        if os.path.isfile(file):
            with open(file) as ifd:
                content = ifd.read()
            result = old in content
            if result:
                with open(file, 'w', newline="\n") as ofd:
                    ofd.write(content.replace(old, new))
        else:
            self._logger.warning("Could not update {}: File does not exist".format(file))
        return result

    def file_contains(self, file, word):
        """ Read file and search for word

        :param file: File path to be read
        :param word: word to be found
        :return: True if found. Otherwise, False
        """
        if os.path.isfile(file):
            with open(file) as ifd:
                content = ifd.read()
                if word in content:
                    return True
        return False

    def _is_header_only(self, conanfile):
        """ Check if Conan recipe is header-only

        :param conanfile: Conan recipe path
        :return: True if recipe is header-only. Otherwise, False.
        """
        if conanfile and os.path.isfile(conanfile) and \
           self.file_contains(conanfile, "self.info.header_only()"):
            return True
        return False

    def _is_installer_recipe(self, conanfile):
        if conanfile and os.path.isfile(conanfile):
            conan_instance, _, _ = conan_api.Conan.factory()
            settings = None
            try:
                settings = conan_instance.inspect(path=conanfile, attributes=["name"])["name"]
            except ConanException:
                pass

            if settings.endswith("_installer"):
                return True

        return False

    def _is_getting_new_compiler_versions(self, conanfile):
        if self._is_header_only(conanfile)\
                or self._is_installer_recipe(conanfile):
            return False

        return True

    def _get_branch_names(self, git_repo):
        """ Retrieve branch names from current git repo

        :param git_repo: Git repository
        """
        branches = []
        for branch in git_repo.references:
            if "HEAD" in str(branch):
                continue
            branches.append(str(branch).replace("origin/", ""))

        # filter non-tags
        filtered_branches = [branch for branch in branches if branch not in git_repo.tags]
        # remove duplicates
        filtered_branches = list(set(filtered_branches))
        return filtered_branches

    def _update_branch(self, git_repo, branch, conanfile, skip_push):
        """ Update local branch and push to origin

        :param git_repo: Git repository
        :param branch: Branch name to be updated
        :param conanfile: Conan recipe path
        :param skip_push: Do not push
        """
        git_repo.git.checkout(branch)

        self.output_remote_update("On branch {}".format(git_repo.active_branch))

        try:
            conanfile = "conanfile.py" if conanfile is None else conanfile
            result_conanfile = self._update_conanfile(conanfile)
            result_readme = self._update_readme("README.md")
            result_travis = self._update_compiler_jobs(".travis.yml")
            result_appveyor = self._update_appveyor_file("appveyor.yml")
            result_azp = self._update_azp_file("azure-pipelines.yml")
            result_gha = self._update_gha_file(os.path.join(".github", "workflows", "conan.yml"))

            result = []
            result.extend(result_conanfile)
            result.extend(result_readme)
            result.extend(result_travis)
            result.extend(result_appveyor)
            result.extend(result_azp)
            result.extend(result_gha)

            if True in result:
                changedFiles = [item.a_path for item in git_repo.index.diff(None)]
                git_repo.git.add('--all')

                self.output_remote_update("On branch {} committing files: {}".format(git_repo.active_branch,
                                                                        " ".join(map(str, changedFiles))))

                commitMsg = "Update Conan conventions\n\n"
                commitMsg += "Automatically created by bincrafters-conventions {}\n\n".format(__version__)
                if True not in result_travis and True not in result_conanfile and True not in result_appveyor:
                    commitMsg += "[skip ci]"
                else:
                    if True not in result_travis and True not in result_conanfile:
                        commitMsg += "[skip travis]"
                    if True not in result_appveyor and True not in result_conanfile:
                        commitMsg += "[skip appveyor]"
                    if True not in result_azp and True not in result_conanfile:
                        commitMsg += "[skip azp]"
                    if True not in result_gha and True not in result_conanfile:
                        commitMsg += "[skip gha]"

                self.output_remote_update("Commit message: {}".format(commitMsg))

                git_repo.index.commit(commitMsg)
                if not skip_push:
                    self.output_remote_update("Pushing branch {} to origin".format(git_repo.active_branch))
                    git_repo.git.push('origin', branch)

                return True

        except Exception as error:
            self._logger.warning(error)

        return False

    def _update_conanfile(self, conanfile):
        """ Update Conan recipe with Conan conventions

        :param conanfile: Conan recipe path
        :return:
        """

        if not os.path.isfile(conanfile):
            return [False, ]

        return [update_c_delete_meta_lines(self, conanfile),
                update_c_deprecated_attributes(self, conanfile),
                update_c_default_options_to_dict(self, conanfile),
                update_c_openssl_version_patch(self, conanfile, openssl_version_matrix),
                update_c_tools_version(self, conanfile),
                update_c_delete_author(self, conanfile),
                update_c_topics(self, conanfile),
                update_c_recipe_references(self, conanfile),
                update_c_remove_compiler_cppstd(self, conanfile)
                ]

    def _update_readme(self, readme):
        """ Update README.md file with new URL

        :param readme: Readme file path
        :return: True if updated. Otherwise, False.
        """
        if not os.path.isfile(readme):
            return [False, ]

        return [
            update_readme_travis_url(self, readme)
        ]

    def _run_conventions_checks(self, conanfile="conanfile.py"):
        """ Checks for conventions which we can't automatically update
        when they should fail
        """

        if not os.path.isfile(conanfile):
            return [False, ]

        return (check_for_license(self),
                check_for_required_attributes(self, conanfile),
                check_for_spdx_license(self, conanfile),
                check_for_download_hash(self, conanfile),
                check_for_deprecated_generators(self, conanfile),
                check_for_deprecated_methods(self, conanfile),
                check_for_deprecated_settings(self, conanfile))

    def output_remote_update(self, title):
        self._logger.info("[\033[1;35mREMOTE\033[0m]  {}".format(title))

    def output_result_update(self, title):
        self._logger.info("[\033[1;32mUPDATED\033[0m]  {}".format(title))

    def output_result_check(self, passed: bool, title, reason="", skipped=False):
        if not reason == "":
            reason = ": {}".format(reason)

        if skipped:
            self._logger.info("[SKIPPED]  {}{}".format(title, reason))
        elif passed:
            self._logger.info("[\033[1;32mPASSED\033[0m]   {}{}".format(title, reason))
        else:
            self._logger.error("[\033[1;31mFAILED\033[0m]   {}{}".format(title, reason))

    def _clone_project(self, github_url):
        """ Clone Github project to temporary directory

        :param github_url: Project url
        """
        temp_dir = tempfile.mkdtemp(prefix='github')
        project = github_url[(github_url.rfind('/') + 1):]
        project_path = os.path.join(temp_dir, project)
        repo = git.Repo.clone_from(github_url, project_path)
        self.output_remote_update("Clone project {} to {}".format(github_url, project_path))
        return repo, project_path

    def _list_user_projects(self, user, token):
        """ List all projects from GitHub public account

        :param user: User name
        """
        projects = []

        # If user provided a GitHub token lets use it for the API request to avoid strict request limits
        auth = None
        if token:
            credentials = token.split(":", 1)
            auth = (credentials[0], credentials[1])

        pages = (1, 2, 3, 4, 5, 6)
        for page in pages:
            repos_url = 'https://api.github.com/users/{}/repos?sort=updated&direction=asc&per_page=100&page={}'\
                .format(user, page)

            response = requests.get(repos_url, auth=auth)
            if page == 1 and not response.ok:
                raise Exception("Could not retrieve {}".format(repos_url))
            for project in response.json():
                if project["name"].startswith("conan-") \
                        and not project["name"].startswith("conan-boost") \
                        and not project["archived"] \
                        and not project["fork"] \
                        and not project["disabled"]:
                    projects.append(project["full_name"])
        self.output_remote_update("Repository list: " + " ".join(map(str, projects)))
        return projects

    def _filter_list(self, names, pattern):
        """ Filter list by user pattern

        :param names: User list names
        :param pattern: Project user filter name
        """
        regex = re.compile(pattern)
        filtered_list = [name for name in names if regex.match(name)]
        self._logger.debug("Filtered list: {}".format(filtered_list))
        return filtered_list

    def _update_remote_project(self, remote, conanfile, skip_push, branch_pattern, all_branches, token=False):
        """ Clone remote project, update Travis and maybe upload

        :param remote: Project full name
        :param conanfile: Conan recipe path
        :param skip_push: Do not push to origin after to update
        :param branch_pattern: Filter to be applied over project branch names
        """
        result = []
        github_url = "git@github.com:{}.git".format(remote)

        if skip_push:
            github_url = "https://github.com/{}.git".format(remote)
        elif token:
            github_url = "https://{}@github.com/{}".format(token, remote)

        git_repo, project_path = self._clone_project(github_url)
        with chdir(project_path):
            branches = []
            if all_branches:
                self.output_remote_update("Update ALL branches of remote")
                branches.extend(self._get_branch_names(git_repo))
            else:
                self.output_remote_update("Update default branch only")
                default_branch = str(git_repo.head.ref)
                branches.extend([default_branch])
            if branch_pattern:
                branches = self._filter_list(branches, branch_pattern)
            for branch in branches:
                self._logger.debug("Current branch to be updated: {}".format(branch))
                result.append(self._update_branch(git_repo, branch, conanfile, skip_push))

        return True if True in result else False

    def _update_remote_user(self, user, conanfile, skip_push, project_pattern,
                            branch_pattern, all_branches, token, max_repos):
        """ Clone remote user projects, update Travis and maybe upload

        :param user: Github username
        :param conanfile: Conan recipe path
        :param skip_push: Do not push to origin after to update
        :param project_pattern: Filter to be applied over user project names
        :param branch_pattern: Filter to be applied over project branch names
        :param all_branches: Bool if all branches or only the default one should get updated
        :param token: GitHub username:token for login
        :param max_repos: Int, how many repositories should get updated max in one run
        """

        repos_updated = 0
        projects = self._list_user_projects(user, token)
        if project_pattern:
            projects = self._filter_list(projects, project_pattern)
        for project in projects:
            if repos_updated < max_repos:
                print("\n")
                if self._update_remote_project(project, conanfile, skip_push, branch_pattern, all_branches, token):
                    repos_updated += 1
            else:
                print("\n")
                self.output_remote_update("Reached max updated remote repositories amount of {}".format(max_repos))
                return True

    def _update_remote(self, remote, conanfile, skip_push, project_pattern, branch_pattern,
                       all_branches, token, max_repos):
        """ Validate which strategy should executed to update the project

        :param remote: Github remote address
        :param conanfile: Conan recipe path
        :param skip_push: Do not push to origin after to update
        :param project_pattern: Filter to be applied over user project names
        :param branch_pattern: Filter to be applied over project branch names
        """
        if "/" not in remote:
            self._update_remote_user(remote, conanfile, skip_push, project_pattern, branch_pattern,
                                     all_branches, token, max_repos)
        else:
            self._update_remote_project(remote, conanfile, skip_push, branch_pattern, all_branches, token)


def main(args):
    """ Execute command update

    :param args: User arguments
    """
    try:
        command = Command()
        command.run(args)
    except Exception as error:
        logging.error("ERROR: {}".format(error))
        sys.exit(1)
