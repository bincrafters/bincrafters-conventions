#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from .actions.check_for_readme import check_for_readme
from .actions.check_for_license import check_for_license
from .actions.check_for_deprecated_generators import check_for_deprecated_generators
from .actions.check_for_deprecated_methods import check_for_deprecated_methods
from .actions.check_for_required_attributes import check_for_required_attributes
from .actions.update_a_python_version import update_a_python_version
from .actions.update_a_path_manipulation import update_a_path_manipulation
from .actions.update_a_python_environment_variable import update_a_python_environment_variable
from .actions.update_c_generic_exception_to_invalid_conf import update_c_generic_exception_to_invalid_conf
from .actions.update_c_install_subfolder import update_c_install_subfolder
from .actions.update_c_build_subfolder import update_c_build_subfolder
from .actions.update_c_default_options_to_dict import update_c_default_options_to_dict
from .actions.update_c_configure_cmake import update_c_configure_cmake
from .actions.update_c_source_subfolder import update_c_source_subfolder
from .actions.update_t_ci_dir_path import update_t_ci_dir_path
from .actions.update_t_macos_images import update_t_macos_images
from .actions.update_t_new_docker_image_names import update_t_new_docker_image_names
from .actions.update_t_add_new_compiler_versions import update_t_add_new_compiler_versions
from .actions.update_t_linux_image import update_t_linux_image
from .actions.update_t_linux_python_version import update_t_linux_python_version
from .actions.update_other_travis_to_ci_dir_name import update_other_travis_to_ci_dir_name
from .actions.update_other_pyenv_python_version import update_other_pyenv_python_version


__version__ = '0.5.0'
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
python_check_for_old_versions = ["2.7.8", "2.7", "2.7.10", "3.6", "3.7.0"]

# Sometimes Travis is publishing new CI images with new XCode versions
# but they still have the same Clang version
# in this case we do NOT need to add new compiler versions and therefore jobs
# but we need to update the existing jobs
# travis_macos_images_updates = [["10.1", "10.2"]] 10.2 isn't ready yet due to zlib problems
travis_macos_images_updates = [["9.3", "9.4"]]

# What apple_clang version is available on which Travis image?
travis_macos_images_compiler_mapping = {'7.3': '7.3', '8.1': '8.3', '9.0': '9', '9.1': '9.4', '10.0': '10.1'}

# This compiler versions are getting added if they are newer than the existing jobs
# and if they don't already exist
travis_compiler_versions = {'gcc': ('6', '7', '8'), 'clang': ('5.0', '6.0', '7.0'), 'apple_clang': ('9.1', '10.0')}


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
        group.add_argument('--conanfile', '-c', type=str, nargs='?', const='conanfile.py',
                           help='Conan recipe path e.g conanfile.py')
        group.add_argument('--check', action='store_true', help='Checks for additional conventions')
        parser.add_argument('--dry-run', '-d', action='store_true', default=False,
                            help='Do not push after update from remote')
        parser.add_argument('--project-pattern', '-pp', type=str,
                            help='Project pattern to filter over user projects e.g bincrafters/conan-*')
        parser.add_argument('--branch-pattern', '-bp', type=str,
                            help='Branch pattern to filter over user projects e.g stable/*')
        group.add_argument('--version', '-v', action='version', version='%(prog)s {}'.format(__version__))
        args = parser.parse_args(*args)
        return args

    def run(self, *args):
        """ Process file update

        :param args: User arguments
        """
        arguments = self._parse_arguments(*args)
        if not len(sys.argv) > 1 or arguments.local:
            if os.path.isfile(".travis.yml"):
                self._update_compiler_jobs(".travis.yml")
            if os.path.isfile("appveyor.yml"):
                self._update_appveyor_file("appveyor.yml")
            self._update_conanfile("conanfile.py")
            self._run_conventions_checks()
        else:
            if arguments.remote:
                self._update_remote(arguments.remote, arguments.conanfile, arguments.dry_run, arguments.project_pattern,
                                    arguments.branch_pattern)
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

    def _update_compiler_jobs(self, file):
        """ Read Travis file and compiler jobs

        :param file: Travis file path
        """

        # Rename .travis -> .ci
        update_other_travis_to_ci_dir_name(self)
        update_t_ci_dir_path(self, file)
        # Update which Python version macOS is using via pyenv
        update_other_pyenv_python_version(self, '.ci/install.sh', python_version_current_pyenv, python_check_for_old_versions)
        # Update Travis Linux Python version
        update_t_linux_python_version(self, file, python_version_current_travis_linux, python_check_for_old_versions)
        # Update which macOS image existing jobs are using
        update_t_macos_images(self, file, travis_macos_images_updates)
        # Update docker image names lasote -> conanio
        update_t_new_docker_image_names(self, file)
        # Update Travis Linux CI base image
        update_t_linux_image(self, file)

        if not self._is_header_only("conanfile.py"):
            # Add new compiler versions to CI jobs
            update_t_add_new_compiler_versions(self, file, travis_compiler_versions, travis_macos_images_compiler_mapping)

    def _update_appveyor_file(self, file):
        update_a_python_environment_variable(self, file)
        update_a_python_version(self, file, python_version_current_appveyor, python_check_for_old_versions)
        update_a_path_manipulation(self, file)


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
                with open(file, 'w') as ofd:
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
        if self.file_contains(conanfile, "self.info.header_only()"):
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

    def _update_branch(self, git_repo, branch, file, conanfile, skip_push):
        """ Update local branch and push to origin

        :param git_repo: Git repository
        :param branch: Branch name to be updated
        :param file: File name to be updated
        :param conanfile: Conan recipe path
        :param skip_push: Do not push
        """
        git_repo.git.checkout(branch)
        self._logger.info("On branch {}".format(git_repo.active_branch))

        try:
            header_only = self._is_header_only(conanfile)
            travis_updater = self._update_compiler_jobs
            if header_only:
                travis_updater = update_t_ci_dir_path(self, conanfile)
                self._logger.info("Conan recipe for header-only project")
            else:
                self._logger.info("Conan recipe is not for header-only project")

            result = (update_other_travis_to_ci_dir_name(self),
                      update_other_pyenv_python_version(self, '.ci/install.sh', python_version_current_pyenv, python_check_for_old_versions),
                      self._update_conanfile(conanfile),
                      travis_updater(file),
                      self._update_appveyor_file('appveyor.yml'))
            self._logger.info("RESULT: {}".format(result))
            if True in result:
                self._logger.debug("Add file {} on branch {}".format(file, git_repo.active_branch))
                git_repo.git.add('--all')
                self._logger.debug("Commit file {} on branch {}".format(file, git_repo.active_branch))
                git_repo.index.commit("#482 Update Conan conventions [build=outdated]")
                if not skip_push:
                    self._logger.debug("Push branch {} to origin".format(git_repo.active_branch))
                    git_repo.git.push('origin', branch)
        except Exception as error:
            self._logger.warning(error)
            pass

    def _update_conanfile(self, conanfile):
        """ Update Conan recipe with Conan conventions

        :param conanfile: Conan recipe path
        :return:
        """
        return (update_c_default_options_to_dict(self, conanfile),
                update_c_generic_exception_to_invalid_conf(self, conanfile),
                update_c_configure_cmake(self, conanfile),
                update_c_source_subfolder(self, conanfile),
                update_c_build_subfolder(self, conanfile),
                update_c_install_subfolder(self, conanfile))

    def _run_conventions_checks(self, conanfile="conanfile.py"):
        """ Checks for conventions which we can't automatically update
        when they should fail
        """
        return (check_for_readme(self),
                check_for_license(self),
                check_for_required_attributes(self, conanfile),
                check_for_spdx_license(self, conanfile),
                check_for_download_hash(self, conanfile),
                check_for_deprecated_generators(self, conanfile),
                check_for_deprecated_methods(self, conanfile))

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
        self._logger.info("Clone project {} to {}".format(github_url, project_path))
        return repo, project_path

    def _list_user_projects(self, user):
        """ List all projects from Github public account

        :param user: User name
        """
        projects = []
        repos_url = 'https://api.github.com/users/{}/repos'.format(user)
        response = requests.get(repos_url)
        if not response.ok:
            raise Exception("Could not retrieve {}".format(repos_url))
        for project in response.json():
            projects.append(project["full_name"])
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

    def _update_remote_project(self, remote, conanfile, skip_push, branch_pattern):
        """ Clone remote project, update Travis and maybe upload

        :param remote: Project full name
        :param conanfile: Conan recipe path
        :param skip_push: Do not push to origin after to update
        :param branch_pattern: Filter to be applied over project branch names
        """
        travis_file = '.travis.yml'
        github_url = "git@github.com:{}.git".format(remote)

        if skip_push:
            github_url = "https://github.com/{}.git".format(remote)

        git_repo, project_path = self._clone_project(github_url)
        with chdir(project_path):
            branches = self._get_branch_names(git_repo)
            if branch_pattern:
                branches = self._filter_list(branches, branch_pattern)
            for branch in branches:
                self._logger.debug("Current branch to be updated: {}".format(branch))
                self._update_branch(git_repo, branch, travis_file, conanfile, skip_push)

    def _update_remote_user(self, user, conanfile, skip_push, project_pattern, branch_pattern):
        """ Clone remote user projects, update Travis and maybe upload

        :param user: Github username
        :param conanfile: Conan recipe path
        :param skip_push: Do not push to origin after to update
        :param project_pattern: Filter to be applied over user project names
        :param branch_pattern: Filter to be applied over project branch names
        """
        projects = self._list_user_projects(user)
        if project_pattern:
            projects = self._filter_list(projects, project_pattern)
        for project in projects:
            self._update_remote_project(project, conanfile, skip_push, branch_pattern)

    def _update_remote(self, remote, conanfile, skip_push, project_pattern, branch_pattern):
        """ Validate which strategy should executed to update the project

        :param remote: Github remote address
        :param conanfile: Conan recipe path
        :param skip_push: Do not push to origin after to update
        :param project_pattern: Filter to be applied over user project names
        :param branch_pattern: Filter to be applied over project branch names
        """
        if "/" not in remote:
            self._update_remote_user(remote, conanfile, skip_push, project_pattern, branch_pattern)
        else:
            self._update_remote_project(remote, conanfile, skip_push, branch_pattern)


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
