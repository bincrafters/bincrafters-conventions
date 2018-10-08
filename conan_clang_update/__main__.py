#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major == 3:
    from conan_clang_update import conan_clang_update
else:
    import conan_clang_update


def run():
    conan_clang_update.main(sys.argv[1:])


if __name__ == '__main__':
    run()
