#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major == 3:
    from bincrafters_conventions import bincrafters_conventions
else:
    import bincrafters_conventions


def run():
    bincrafters_conventions.main(sys.argv[1:])


if __name__ == '__main__':
    run()
