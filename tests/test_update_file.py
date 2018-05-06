#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan_clang_update.conan_clang_update import Command

import tempfile
import filecmp

TRAVIS_FILE = """linux: &linux
   os: linux
   sudo: required
   language: python
   python: "3.6"
   services:
     - docker
osx: &osx
   os: osx
   language: generic
matrix:
   include:
      - <<: *linux
        env: CONAN_GCC_VERSIONS=4.9 CONAN_DOCKER_IMAGE=lasote/conangcc49
      - <<: *linux
        env: CONAN_GCC_VERSIONS=5 CONAN_DOCKER_IMAGE=lasote/conangcc5
      - <<: *linux
        env: CONAN_GCC_VERSIONS=6 CONAN_DOCKER_IMAGE=lasote/conangcc6
      - <<: *linux
        env: CONAN_GCC_VERSIONS=7 CONAN_DOCKER_IMAGE=lasote/conangcc7
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=3.9 CONAN_DOCKER_IMAGE=lasote/conanclang39
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=4.0 CONAN_DOCKER_IMAGE=lasote/conanclang40
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=5.0 CONAN_DOCKER_IMAGE=lasote/conanclang50
      - <<: *osx
        osx_image: xcode7.3
        env: CONAN_APPLE_CLANG_VERSIONS=7.3
      - <<: *osx
        osx_image: xcode8.3
        env: CONAN_APPLE_CLANG_VERSIONS=8.1
      - <<: *osx
        osx_image: xcode9
        env: CONAN_APPLE_CLANG_VERSIONS=9.0

install:
  - chmod +x .travis/install.sh
  - ./.travis/install.sh

script:
  - chmod +x .travis/run.sh
  - ./.travis/run.sh
"""

UPDATED_TRAVIS = """linux: &linux
   os: linux
   sudo: required
   language: python
   python: "3.6"
   services:
     - docker
osx: &osx
   os: osx
   language: generic
matrix:
   include:
      - <<: *linux
        env: CONAN_GCC_VERSIONS=4.9 CONAN_DOCKER_IMAGE=lasote/conangcc49
      - <<: *linux
        env: CONAN_GCC_VERSIONS=5 CONAN_DOCKER_IMAGE=lasote/conangcc5
      - <<: *linux
        env: CONAN_GCC_VERSIONS=6 CONAN_DOCKER_IMAGE=lasote/conangcc6
      - <<: *linux
        env: CONAN_GCC_VERSIONS=7 CONAN_DOCKER_IMAGE=lasote/conangcc7
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=3.9 CONAN_DOCKER_IMAGE=lasote/conanclang39
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=4.0 CONAN_DOCKER_IMAGE=lasote/conanclang40
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=5.0 CONAN_DOCKER_IMAGE=lasote/conanclang50
      - <<: *osx
        osx_image: xcode7.3
        env: CONAN_APPLE_CLANG_VERSIONS=7.3
      - <<: *osx
        osx_image: xcode8.3
        env: CONAN_APPLE_CLANG_VERSIONS=8.1
      - <<: *osx
        osx_image: xcode9
        env: CONAN_APPLE_CLANG_VERSIONS=9.0
      - <<: *osx
        osx_image: xcode9.3
        env: CONAN_APPLE_CLANG_VERSIONS=9.1

install:
  - chmod +x .travis/install.sh
  - ./.travis/install.sh

script:
  - chmod +x .travis/run.sh
  - ./.travis/run.sh
"""


def test_update_clang_file():
    """ Create a standard travis file and update it.
    """
    _, travis_path = tempfile.mkstemp(prefix='travis', suffix='.yml')
    with open(travis_path, 'w') as file:
        file.write(TRAVIS_FILE)

    _, expected_path = tempfile.mkstemp(prefix='travis', suffix='.yml')
    with open(expected_path, 'w') as file:
        file.write(UPDATED_TRAVIS)

    args = ['--file', travis_path]
    command = Command()
    command.run(args)

    assert filecmp.cmp(travis_path, expected_path)
