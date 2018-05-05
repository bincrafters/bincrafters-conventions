#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan_clang_update.conan_clang_update import Command

def test_update_clang_remote():
    """ Clone dummy project and update it.
    """
    args = ['--remote', 'uilianries/conan-base64', '--skip-push']
    command = Command()
    command.run(args)
