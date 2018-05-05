#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import re
import logging

#from __init__ import __version__ as package_version

LOGGING_FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT)

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
        parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1.0')
        args = parser.parse_args(*args)
        return args

    def run(self, *args):
        """ Process file update

        :param args: User arguments
        """
        arguments = self._parse_arguments(*args)
        if arguments.remote:
            self._update_remote(arguments.remote)
        else:
            self._update_file(arguments.file)
        self._logger.info("ARGS: %s" % arguments)

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
            return

        if self._is_updated(file):
            self._logger.info("File {} is up to date".format(file))
            return

        lines = self._read_and_update(file)
        self._dump_file(file, lines)

    def _update_remote(self, remote):
        pass

def main(args):
    try:
        command = Command()
        command.run(args)
    except Exception as error:
        logging.error("ERROR: {}".format(error))
        sys.exit(1)
