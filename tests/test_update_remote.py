#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan_clang_update.conan_clang_update import Command
import platform


def is_macos():
    return 'Darwin' in platform.system()


def test_update_clang_remote_project():
    """ Clone dummy project and update it.
    """
    args = ['--remote', 'uilianries/conan-base64', '--skip-push']
    command = Command()
    command.run(args)


def test_update_clang_remote_user():
    """ Clone all projects and update it.
    """
    # XXX (uilianries): There is some error to request Github API on Mac jobs
    if is_macos():
        return

    args = ['--remote', 'uilianries', '--skip-push']
    command = Command()
    command.run(args)


def test_update_clang_remote_user_project_pattern():
    """ Clone only filtered projects and update it.
    """
    # XXX (uilianries): There is some error to request Github API on Mac jobs
    if is_macos():
        return

    args = ['--remote', 'uilianries', '--skip-push', '--projects-pattern', 'uilianries/conan-*']
    command = Command()
    command.run(args)
