#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import re
import logging
import git
import tempfile
import requests
import contextlib

LOGGING_FORMAT = '[%(levelname)s]\t%(asctime)s %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')


@contextlib.contextmanager
def chdir(newdir):
    """ Change directory using locked scope

    :param newdir: Tempory folder to move
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
        self._logger.setLevel(logging.DEBUG)
        self._pattern = r"(\s*)env: CONAN_APPLE_CLANG_VERSIONS=\d\.\d"
        self._regex = re.compile(self._pattern)

    def _parse_arguments(self, *args):
        """ Add program arguments

        :param args: User arguments
        """
        parser = argparse.ArgumentParser(description="Conan Clang Update")
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--file', '-f', type=str, help='Travis file to be updated')
        group.add_argument('--remote', '-r', type=str, help='Github repo to be updated')
        parser.add_argument(
            '--skip-push',
            '-sp',
            action='store_true',
            default=False,
            help='Do not push after update from remote')
        parser.add_argument(
            '--project-pattern',
            '-pp',
            type=str,
            help='Project pattern to filter over user projects e.g bincrafters/conan-*')
        parser.add_argument(
            '--branch-pattern',
            '-bp',
            type=str,
            help='Branch pattern to filter over user projects e.g stable/*')
        # TODO (uilian): Consume version from __init__
        parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.2.0')
        args = parser.parse_args(*args)
        return args

    def run(self, *args):
        """ Process file update

        :param args: User arguments
        """
        arguments = self._parse_arguments(*args)
        if arguments.remote:
            self._update_remote(arguments.remote, arguments.skip_push, arguments.project_pattern,
                                arguments.branch_pattern)
        else:
            self._update_file(arguments.file)

    def _has_osx(self, file):
        """ Check for OSX support on Travis file

        :param file: Travis file path
        :rtype file: str
        """
        return 'CONAN_APPLE_CLANG_VERSIONS' in open(file).read()

    def _is_updated(self, file):
        """ Validate if Travis file is already updated

        :param file: Travis file path
        :rtype file: str
        """
        return 'CONAN_APPLE_CLANG_VERSIONS=9.1' in open(file).read()

    def _dump_file(self, file, lines):
        """ Dump content on file

        :param file: File path
        :param lines: string list to be dumped
        """
        with open(file, 'w') as fd:
            for line in lines:
                fd.write(line + "\n")

    def _read_and_update(self, file):
        """ Read Travis file and Update OSX job

        :param file: Travis file path
        """
        lines = []
        with open(file, 'r') as fd:
            updated = False
            # search for latest occurrence
            for line in reversed(fd.readlines()):
                if not updated:
                    match = self._regex.match(line)
                    if match:
                        lines = self._inject_clang(lines, match.group(1))
                        updated = True
                lines.append(line.rstrip())
        return reversed(lines)

    def _inject_clang(self, lines, spaces):
        """ Update lines with Clang 9.1

        :param lines: Travis file lines
        :param spaces: Indentation
        """
        lines.append("{}{}".format(spaces, 'env: CONAN_APPLE_CLANG_VERSIONS=9.1'))
        lines.append("{}{}".format(spaces, 'osx_image: xcode9.3'))
        lines.append("{}{}".format(spaces[2:], '- <<: *osx'))
        return lines

    def _update_file(self, file):
        """ Open Travis and inject clang 9.1 if OSX is supported

        :param file: Travis file path
        :rtype file: str
        """
        if not os.path.isfile(file):
            raise ValueError("Invalid file path")

        if not self._has_osx(file):
            self._logger.info("File {} has no support for OSX".format(file))
            return False

        if self._is_updated(file):
            self._logger.info("File {} is up to date".format(file))
            return False

        lines = self._read_and_update(file)
        self._dump_file(file, lines)
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

    def _update_branch(self, git_repo, branch, file, skip_push):
        """ Update local branch and push to origin

        :param git_repo: Git repository
        :param branch: Branch name to be updated
        :param file: File name to be updated
        :param skip_push: Do not push
        """
        git_repo.git.checkout(branch)
        self._logger.info("Update file {} on branch {}".format(file, git_repo.active_branch))
        try:
            if self._update_file(file):
                self._logger.debug("Add file {} on branch {}".format(file, git_repo.active_branch))
                git_repo.index.add([file])
                self._logger.debug("Commit file {} on branch {}".format(
                    file, git_repo.active_branch))
                git_repo.index.commit("Add apple clang 9.1 job on travis file")
                if not skip_push:
                    self._logger.debug("Push branch {} to origin".format(git_repo.active_branch))
                    git_repo.git.push('origin', branch)
        except Exception as error:
            self._logger.warning(error)
            pass

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
        if response.status_code != 200:
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

    def _update_remote_project(self, remote, skip_push, branch_pattern):
        """ Clone remote project, update Travis and maybe upload

        :param remote: Project full name
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
                self._update_branch(git_repo, branch, travis_file, skip_push)

    def _update_remote_user(self, user, skip_push, project_pattern, branch_pattern):
        """ Clone remote user projects, update Travis and maybe upload

        :param user: Github username
        :param skip_push: Do not push to origin after to update
        :param project_pattern: Filter to be applied over user project names
        :param branch_pattern: Filter to be applied over project branch names
        """
        projects = self._list_user_projects(user)
        if project_pattern:
            projects = self._filter_list(projects, project_pattern)
        for project in projects:
            self._update_remote_project(project, skip_push, branch_pattern)

    def _update_remote(self, remote, skip_push, project_pattern, branch_pattern):
        """ Validate which strategy should executed to update the project

        :param remote: Github remote address
        :param skip_push: Do not push to origin after to update
        :param project_pattern: Filter to be applied over user project names
        :param branch_pattern: Filter to be applied over project branch names
        """
        if "/" not in remote:
            self._update_remote_user(remote, skip_push, project_pattern, branch_pattern)
        else:
            self._update_remote_project(remote, skip_push, branch_pattern)


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
