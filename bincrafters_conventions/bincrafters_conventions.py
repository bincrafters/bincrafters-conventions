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
from .actions.update_a_use_package_tools_auto import update_a_use_package_tools_auto
from .actions.update_a_jobs import update_a_jobs
from .actions.update_gha import update_gha
from .actions.update_c_attributes import update_c_delete_author, update_c_topics, update_c_delete_licensemd_export
from .actions.update_c_deprecated_attributes import update_c_deprecated_attributes
from .actions.update_c_openssl_version_patch import update_c_openssl_version_patch
from .actions.update_c_default_options_to_dict import update_c_default_options_to_dict
from .actions.update_c_delete_meta_lines import update_c_delete_meta_lines
from .actions.update_c_tools_version import update_c_tools_version
from .actions.update_c_recipe_references import update_c_recipe_references
from .actions.update_c_remove_compiler_cppstd import update_c_remove_compiler_cppstd
from .actions.update_readme_travis_url import update_readme_travis_url
from .actions.update_migrate_travis_to_import_and_gha import update_migrate_travis_to_import_and_gha

__version__ = '0.24.6'
__author__ = 'Bincrafters <bincrafters@gmail.com>'
__license__ = 'MIT'

LOGGING_FORMAT = '[%(levelname)s]\t%(asctime)s %(message)s'
LOGGING_LEVEL = os.getenv("BINCRAFTERS_LOGGING_LEVEL", logging.INFO)
logging.basicConfig(level=int(LOGGING_LEVEL), format=LOGGING_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

# Current Python version for AppVeyor
python_version_current_appveyor = "37"

# What MSVC versions are available on which AppVeyor image?
appveyor_win_msvc_images_compiler_mapping = {'12': '2015', '14': '2015', '15': '2017', '16': '2019'}

# This compiler versions are getting added if they are newer than the existing jobs
# and if they don't already exist
compiler_versions = {'visual': ('15', '16')}
# This compiler versions are getting actively removed from existing jobs
compiler_versions_deletion = {'visual': ('12',)}


# What are the latest AVAILABLE patches for OpenSSL, which versions are End-Of-Life?
openssl_version_matrix = {'1.0.1': {'latest_patch': 'h', 'eol': True},
                          '1.0.2': {'latest_patch': 'u', 'eol': True},
                          '1.1.0': {'latest_patch': 'l', 'eol': True},
                          '1.1.1': {'latest_patch': 'g', 'eol': False},
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
    def __init__(self):
        self._logger = logging.getLogger(__file__)
        self._logger.setLevel(logging.INFO)

    def _parse_arguments(self, *args):
        """ Add program arguments

        :param args: User arguments
        """
        parser = argparse.ArgumentParser(description="Bincrafters Conventions")
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--remote', type=str, help='Github repo to be updated e.g. bincrafters/conan-foobar')
        group.add_argument('--remote-add-gha-secrets', type=str,
                           help='Add secrets to all Conan GitHub repositories of an organisation.'
                                'Set env vars CONAN_LOGIN_USERNAME and CONAN_PASSSWORD and argument --remote-token')
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
            elif arguments.remote_add_gha_secrets:
                self._add_gha_secrets_to_github_repos(user=arguments.remote_add_gha_secrets, token=arguments.remote_token)
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
            update_migrate_travis_to_import_and_gha(self, file)
        ])

        return result

    def _update_appveyor_file(self, file):
        if not os.path.isfile(file):
            return [False, ]

        result = [
            update_a_python_environment_variable(self, file),
            update_a_python_version(self, file, python_version_current_appveyor),
            update_a_path_manipulation(self, file),
            update_a_use_package_tools_auto(self, file),
        ]

        # Add new compiler versions to CI jobs
        result.extend([
            update_a_jobs(self, file, compiler_versions, appveyor_win_msvc_images_compiler_mapping, compiler_versions_deletion)
        ])

        return result

    def _update_azp_file(self, file):
        if not os.path.isfile(file):
            return [False, ]

        result = [ ]

        return result

    def _update_gha_file(self, gha_file):
        if not os.path.isfile(gha_file):
            return [False, ]

        result = []

        result.extend([
            update_gha(self, gha_file)
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
                update_c_remove_compiler_cppstd(self, conanfile),
                update_c_delete_licensemd_export(self, conanfile)
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

    # Method is from https://developer.github.com/v3/actions/secrets/#example-encrypting-a-secret-using-python
    def _encrypt_for_github_actions(self, public_key: str, secret_value: str) -> str:
        from base64 import b64encode
        from nacl import encoding, public
        """Encrypt a Unicode string using the public key."""
        public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return b64encode(encrypted).decode("utf-8")

    def _add_gha_secrets_to_github_repos(self, user, token):
        self.output_remote_update("")
        self.output_remote_update("Adding/Updating GitHub Actions secret to all Conan repositories for {}".format(user))
        self.output_remote_update("")

        conan_login_username = os.getenv("CONAN_LOGIN_USERNAME", "bincrafters-user")
        conan_password = os.getenv("CONAN_PASSWORD", None)

        projects = self._list_user_projects(user, token)
        credentials = token.split(":", 1)
        auth = (credentials[0], credentials[1])

        for project in projects:
            key_request = requests.get("https://api.github.com/repos/{}/actions/secrets/public-key".format(project),
                                      auth=auth)
            public_key = key_request.json()

            login_user = self._encrypt_for_github_actions(public_key["key"], conan_login_username)
            login_password = self._encrypt_for_github_actions(public_key["key"], conan_password)

            url_user = "https://api.github.com/repos/{}/actions/secrets/{}".format(project, "CONAN_LOGIN_USERNAME")
            url_password = "https://api.github.com/repos/{}/actions/secrets/{}".format(project, "CONAN_PASSWORD")

            data_user = {"key_id": public_key["key_id"], "encrypted_value": login_user}
            data_pw = {"key_id": public_key["key_id"], "encrypted_value": login_password}

            ru = requests.put(url_user, auth=auth, json=data_user)
            rp = requests.put(url_password, auth=auth, json=data_pw)

            if ru.status_code == 201 and rp.status_code == 201:
                self.output_result_check(passed=True,
                                         title="Adding GitHub Actions Secret for {}".format(project),
                                         reason="Success")
            elif ru.status_code == 204 and rp.status_code == 204:
                self.output_result_check(passed=True,
                                         title="Updating GitHub Actions Secret for {}".format(project),
                                         reason="Success")
            else:
                self.output_result_check(passed=False,
                                         title="Adding/Updating GitHub Actions Secret for {}".format(project),
                                         reason="Failed with {}/{}".format(ru.status_code, rp.status_code))

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
        self.output_remote_update("")
        self.output_remote_update("Updating conventions")
        self.output_remote_update("")

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
