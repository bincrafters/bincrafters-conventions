#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters_conventions.bincrafters_conventions import Command


def test_update_clang_remote_project():
    """ Clone dummy project and update it.
    """
    args = ['--remote', 'uilianries/conan-base64', '--dry-run']
    command = Command()
    command.run(args)


def test_update_clang_filter_branch():
    """ Clone dummy project, filter by branch and update it.
    """
    args = ['--remote', 'uilianries/conan-base64', '--dry-run', '--branch-pattern', 'testing/*']
    command = Command()
    command.run(args)

