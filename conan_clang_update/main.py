#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan_clang_update.conan_clang_update import main
import sys


def run():
    main(sys.argv[1:])


if __name__ == '__main__':
    run()
