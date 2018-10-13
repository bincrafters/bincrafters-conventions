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
import collections
import jinja2
import shutil


__version__ = '0.1.0'
__author__ = 'Bincrafters <bincrafters@gmail.com>'
__license__ = 'MIT'


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


Compiler = collections.namedtuple('Compiler', 'name, var, version, os, osx_version')


LINUX_TEMPLATE = """linux: &linux
   os: linux
   sudo: required
   language: python
   python: "3.6"
   services:
     - docker"""

OSX_TEMPLATE = """
osx: &osx
   os: osx
   language: generic"""

TRAVIS_TEMPLATE = """{{ linux_template }}{{ osx_template }}
matrix:
   include:{% for compiler in compilers %}
      - <<: *{{ compiler.os }}{% if compiler.os == "osx" %}
        osx_image: xcode{{ compiler.osx_version }}{% endif %}
        {% if compiler.os == "linux" %}env: {{ compiler.var }}={{ compiler.version}} CONAN_DOCKER_IMAGE=conanio/{{ compiler.name }}{{ compiler.version.replace(".", "") }}{% else %}env: {{ compiler.var }}={{ compiler.version }}{% endif %}{% endfor %}

install:
  - chmod +x .ci/install.sh
  - ./.ci/install.sh

script:
  - chmod +x .ci/run.sh
  - ./.ci/run.sh

"""


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
        group.add_argument('--file', type=str, help='Travis file to be updated e.g. .travis.yml')
        parser.add_argument('--dry-run', '-d', action='store_true', default=False, help='Do not push after update from remote')
        parser.add_argument('--project-pattern', '-pp', type=str, help='Project pattern to filter over user projects e.g bincrafters/conan-*')
        parser.add_argument('--branch-pattern', '-bp', type=str, help='Branch pattern to filter over user projects e.g stable/*')
        parser.add_argument('--conanfile', '-c', type=str, default='conanfile.py', help='Conan recipe path')
        parser.add_argument('--version', '-v', action='version', version='%(prog)s {}'.format(__version__))
        args = parser.parse_args(*args)
        return args

    def run(self, *args):
        """ Process file update

        :param args: User arguments
        """
        arguments = self._parse_arguments(*args)
        if arguments.remote:
            self._update_remote(arguments.remote, arguments.conanfile, arguments.dry_run, arguments.project_pattern,
                                arguments.branch_pattern)
        else:
            self._update_compiler_jobs(arguments.file)

    def _update_compiler_jobs(self, file):
        """ Read Travis file and Update OSX job

        :param file: Travis file path
        """
        compilers = self._read_compiler_versions(file)
        self._logger.debug("Found compilers: {}".format(compilers))
        sorted_compilers = self._add_recommended_compiler_versions(compilers)
        self._logger.debug("Updated compilers: {}".format(sorted_compilers))
        has_linux, has_osx, compiler_objs = self._transform_compiler_list(sorted_compilers)

        self._logger.debug("compilers: {}".format(compiler_objs))

        template = jinja2.Template(TRAVIS_TEMPLATE)
        linux_template = LINUX_TEMPLATE if has_linux else ""
        osx_template = OSX_TEMPLATE if has_osx else ""

        travis_content = template.render(linux_template=linux_template, osx_template=osx_template, compilers=compiler_objs)
        with open(file, 'w') as fd:
            fd.write(travis_content)

        return sorted(compilers) != sorted_compilers

    def _transform_compiler_list(self, compilers):
        """ Transform compiler version list in Compiler object list

        :param compilers: Target compiler versions
        :return: Compiler metadata in a list
        """
        has_linux = False
        has_osx = False
        compiler_list = []
        osx_versions = {'7.3': '7.3', '8.1': '8.3', '9.0': '9', '9.1': '9.4', '10.0': '10'}

        for compiler_name in ['gcc', 'clang']:
            if compiler_name in compilers:
                for version in compilers[compiler_name]:
                    compiler = Compiler(compiler_name, 'CONAN_%s_VERSIONS' % compiler_name.upper(), version, 'linux', None)
                    compiler_list.append(compiler)
                has_linux = True

        compiler_name = 'apple_clang'
        if compiler_name in compilers:
            for version in compilers[compiler_name]:
                compiler = Compiler(compiler_name, 'CONAN_%s_VERSIONS' % compiler_name.upper(), version, 'osx', osx_versions[version])
                compiler_list.append(compiler)
                has_osx = True

        return has_linux, has_osx, compiler_list

    def _add_recommended_compiler_versions(self, compilers):
        """ Add recommended compiler versions to configured versions

        :param compilers: compiler list read from travis file
        :return:
        """

        if compilers.get('gcc'):
            compilers['gcc'] = sorted(compilers['gcc'].union(['6', '7', '8']), key=float)
        if compilers.get('clang'):
            compilers['clang'] = sorted(compilers['clang'].union(['5.0', '6.0', '7']), key=float)
        if compilers.get('apple_clang'):
            compilers['apple_clang'] = sorted(compilers['apple_clang'].union(['9.1', '10.0']), key=float)
        return compilers

    def _update_travis_path(self):
        """ Replace Travis directory by CI dir
        """
        travis_dir = ".travis"
        ci_dir = ".ci"
        self._logger.info("Update Travis directory path")
        if os.path.isdir(travis_dir):
            shutil.move(os.path.abspath(travis_dir), os.path.abspath(ci_dir))
            return True
        return False

    def _update_configure_cmake(self, file):
        """ Replace configure cmake helper
        """
        self._logger.info("Update Configure CMake")
        return (self._replace_in_file(file, "def configure_cmake", "def _configure_cmake"),
                self._replace_in_file(file, "self.configure_cmake", "self._configure_cmake"))

    def _update_source_subfolder(self, file):
        """ Replace source subfolder from Conan recipe
        """
        self._logger.info("Update Source subfolder")
        return (self._replace_in_file(file, " source_subfolder =", " _source_subfolder ="),
                self._replace_in_file(file, "self.source_subfolder", "self._source_subfolder"))

    def _update_build_subfolder(self, file):
        """ Replace build subfolder from Conan recipe
        """
        self._logger.info("Update Build subfolder")
        return (self._replace_in_file(file, " build_subfolder =", " _build_subfolder ="),
                self._replace_in_file(file, "self.build_subfolder", "self._build_subfolder"))

    def _update_ci_path_in_travis(self, file):
        """ Update travis folder path in travis file

        :param file: travis file path
        :return:
        """
        return self._replace_in_file(file, ".travis", ".ci")

    def _replace_in_file(self, file, old, new):
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
                    self._logger.info("File {} was updated".format(file))
        else:
            self._logger.warning("Could not update {}: File does not exist".format(file))
        return result

    def _is_hearder_only(self, conanfile):
        """ Check if Conan recipe is header-only

        :param conanfile: Conan recipe path
        :return: True if recipe is header-only. Otherwise, False.
        """
        if os.path.isfile(conanfile):
            with open(conanfile) as ifd:
                content = ifd.read()
                return "self.info.header_only()" in content
        else:
            self._logger.warning("Could not check header-only recipe")
        return False

    def _read_compiler_versions(self, file):
        """ Read travis file and list all version used by compiler

        :param file: Travis file path
        :return: dictionary with present compiler and their versions
        """
        versions = {'gcc': set(), 'clang': set(), 'apple_clang': set()}
        for compiler_name in versions.keys():
            regex = re.compile(r'CONAN_{}_VERSIONS=([^\s]+)'.format(compiler_name.upper()))
            if os.path.isfile(file):
                with open(file) as ifd:
                    for line in ifd:
                        match = regex.search(line)
                        if match:
                            versions[compiler_name].add(match.group(1))
        return versions

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
            header_only = self._is_hearder_only(conanfile)
            travis_updater = self._update_compiler_jobs
            if header_only:
                travis_updater = self._update_ci_path_in_travis
                self._logger.info("Conan recipe for header-only project")
            else:
                self._logger.info("Conan recipe is not for header-only project")

            versions = self._read_compiler_versions(file)
            self._logger.info(versions)

            result = (self._update_travis_path(),
                      self._update_configure_cmake(conanfile),
                      self._update_source_subfolder(conanfile),
                      self._update_build_subfolder(conanfile),
                      travis_updater(file))
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
