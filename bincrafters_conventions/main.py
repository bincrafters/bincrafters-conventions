#!/usr/bin/env python

import sys
from bincrafters_conventions import bincrafters_conventions


def run():
    bincrafters_conventions.main(sys.argv[1:])


if __name__ == '__main__':
    run()
