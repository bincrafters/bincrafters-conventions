#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters_conventions.bincrafters_conventions import Command

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
        env: CONAN_CLANG_VERSIONS=3.9 CONAN_DOCKER_IMAGE=lasote/conanclang39
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=4.0 CONAN_DOCKER_IMAGE=lasote/conanclang40
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

TRAVIS_FILE_WITH_GLOBAL = """env:
   global:
     - CONAN_DOCKER_32_IMAGES: 1
     - CONAN_TOTAL_PAGES: 2
linux: &linux
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
        env: CONAN_GCC_VERSIONS=4.9 CONAN_DOCKER_IMAGE=lasote/conangcc49 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_GCC_VERSIONS=4.9 CONAN_DOCKER_IMAGE=lasote/conangcc49 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_GCC_VERSIONS=5 CONAN_DOCKER_IMAGE=lasote/conangcc5 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_GCC_VERSIONS=5 CONAN_DOCKER_IMAGE=lasote/conangcc5 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=3.9 CONAN_DOCKER_IMAGE=lasote/conanclang39 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=3.9 CONAN_DOCKER_IMAGE=lasote/conanclang39 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=4.0 CONAN_DOCKER_IMAGE=lasote/conanclang40 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=4.0 CONAN_DOCKER_IMAGE=lasote/conanclang40 CONAN_CURRENT_PAGE=2
      - <<: *osx
        osx_image: xcode7.3
        env: CONAN_APPLE_CLANG_VERSIONS=7.3 CONAN_CURRENT_PAGE=1
      - <<: *osx
        osx_image: xcode7.3
        env: CONAN_APPLE_CLANG_VERSIONS=7.3 CONAN_CURRENT_PAGE=2
      - <<: *osx
        osx_image: xcode8.3
        env: CONAN_APPLE_CLANG_VERSIONS=8.1 CONAN_CURRENT_PAGE=1
      - <<: *osx
        osx_image: xcode8.3
        env: CONAN_APPLE_CLANG_VERSIONS=8.1 CONAN_CURRENT_PAGE=2
      - <<: *osx
        osx_image: xcode9
        env: CONAN_APPLE_CLANG_VERSIONS=9.0 CONAN_CURRENT_PAGE=1
      - <<: *osx
        osx_image: xcode9
        env: CONAN_APPLE_CLANG_VERSIONS=9.0 CONAN_CURRENT_PAGE=2

install:
  - chmod +x .travis/install.sh
  - ./.travis/install.sh

script:
  - chmod +x .travis/run.sh
  - ./.travis/run.sh
"""

EXPECTED_TRAVIS_FILE_WITH_GLOBAL = """env:
   global:
     - CONAN_DOCKER_32_IMAGES: 1
     - CONAN_TOTAL_PAGES: 2
linux: &linux
   os: linux
   dist: xenial
   language: python
   python: "3.7"
   services:
     - docker
osx: &osx
   os: osx
   language: generic
matrix:
   include:
      - <<: *linux
        env: CONAN_GCC_VERSIONS=4.9 CONAN_DOCKER_IMAGE=conanio/gcc49 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_GCC_VERSIONS=4.9 CONAN_DOCKER_IMAGE=conanio/gcc49 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_GCC_VERSIONS=5 CONAN_DOCKER_IMAGE=conanio/gcc5 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_GCC_VERSIONS=5 CONAN_DOCKER_IMAGE=conanio/gcc5 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_GCC_VERSIONS=6 CONAN_DOCKER_IMAGE=conanio/gcc6 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_GCC_VERSIONS=6 CONAN_DOCKER_IMAGE=conanio/gcc6 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_GCC_VERSIONS=7 CONAN_DOCKER_IMAGE=conanio/gcc7 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_GCC_VERSIONS=7 CONAN_DOCKER_IMAGE=conanio/gcc7 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_GCC_VERSIONS=8 CONAN_DOCKER_IMAGE=conanio/gcc8 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_GCC_VERSIONS=8 CONAN_DOCKER_IMAGE=conanio/gcc8 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=3.9 CONAN_DOCKER_IMAGE=conanio/clang39 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=3.9 CONAN_DOCKER_IMAGE=conanio/clang39 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=4.0 CONAN_DOCKER_IMAGE=conanio/clang40 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=4.0 CONAN_DOCKER_IMAGE=conanio/clang40 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=5.0 CONAN_DOCKER_IMAGE=conanio/clang50 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=5.0 CONAN_DOCKER_IMAGE=conanio/clang50 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=6.0 CONAN_DOCKER_IMAGE=conanio/clang60 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=6.0 CONAN_DOCKER_IMAGE=conanio/clang60 CONAN_CURRENT_PAGE=2
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=7 CONAN_DOCKER_IMAGE=conanio/clang7 CONAN_CURRENT_PAGE=1
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=7 CONAN_DOCKER_IMAGE=conanio/clang7 CONAN_CURRENT_PAGE=2
      - <<: *osx
        osx_image: xcode7.3
        env: CONAN_APPLE_CLANG_VERSIONS=7.3 CONAN_CURRENT_PAGE=1
      - <<: *osx
        osx_image: xcode7.3
        env: CONAN_APPLE_CLANG_VERSIONS=7.3 CONAN_CURRENT_PAGE=2
      - <<: *osx
        osx_image: xcode8.3
        env: CONAN_APPLE_CLANG_VERSIONS=8.1 CONAN_CURRENT_PAGE=1
      - <<: *osx
        osx_image: xcode8.3
        env: CONAN_APPLE_CLANG_VERSIONS=8.1 CONAN_CURRENT_PAGE=2
      - <<: *osx
        osx_image: xcode9
        env: CONAN_APPLE_CLANG_VERSIONS=9.0 CONAN_CURRENT_PAGE=1
      - <<: *osx
        osx_image: xcode9
        env: CONAN_APPLE_CLANG_VERSIONS=9.0 CONAN_CURRENT_PAGE=2
      - <<: *osx
        osx_image: xcode9.4
        env: CONAN_APPLE_CLANG_VERSIONS=9.1 CONAN_CURRENT_PAGE=1
      - <<: *osx
        osx_image: xcode9.4
        env: CONAN_APPLE_CLANG_VERSIONS=9.1 CONAN_CURRENT_PAGE=2
      - <<: *osx
        osx_image: xcode10.1
        env: CONAN_APPLE_CLANG_VERSIONS=10.0 CONAN_CURRENT_PAGE=1
      - <<: *osx
        osx_image: xcode10.1
        env: CONAN_APPLE_CLANG_VERSIONS=10.0 CONAN_CURRENT_PAGE=2

install:
  - chmod +x .ci/install.sh
  - ./.ci/install.sh

script:
  - chmod +x .ci/run.sh
  - ./.ci/run.sh
"""

EXPECTED_TRAVIS_FILE = """linux: &linux
   os: linux
   dist: xenial
   language: python
   python: "3.7"
   services:
     - docker
osx: &osx
   os: osx
   language: generic
matrix:
   include:
      - <<: *linux
        env: CONAN_GCC_VERSIONS=4.9 CONAN_DOCKER_IMAGE=conanio/gcc49
      - <<: *linux
        env: CONAN_GCC_VERSIONS=5 CONAN_DOCKER_IMAGE=conanio/gcc5
      - <<: *linux
        env: CONAN_GCC_VERSIONS=6 CONAN_DOCKER_IMAGE=conanio/gcc6
      - <<: *linux
        env: CONAN_GCC_VERSIONS=7 CONAN_DOCKER_IMAGE=conanio/gcc7
      - <<: *linux
        env: CONAN_GCC_VERSIONS=8 CONAN_DOCKER_IMAGE=conanio/gcc8
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=3.9 CONAN_DOCKER_IMAGE=conanio/clang39
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=4.0 CONAN_DOCKER_IMAGE=conanio/clang40
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=5.0 CONAN_DOCKER_IMAGE=conanio/clang50
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=6.0 CONAN_DOCKER_IMAGE=conanio/clang60
      - <<: *linux
        env: CONAN_CLANG_VERSIONS=7 CONAN_DOCKER_IMAGE=conanio/clang7
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
        osx_image: xcode9.4
        env: CONAN_APPLE_CLANG_VERSIONS=9.1
      - <<: *osx
        osx_image: xcode10.1
        env: CONAN_APPLE_CLANG_VERSIONS=10.0

install:
  - chmod +x .ci/install.sh
  - ./.ci/install.sh

script:
  - chmod +x .ci/run.sh
  - ./.ci/run.sh
"""

EXPECTED_CONAN_FILE = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os


class DoubleConversionConan(ConanFile):
    name = "double-conversion"
    version = "3.0.0"
    url = "https://github.com/bincrafters/conan-double-conversion"
    homepage = "https://github.com/google/double-conversion"
    author = "Bincrafters <bincraters@gmail.com>"
    description = "Efficient binary-decimal and decimal-binary conversion routines for IEEE doubles."
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"


    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           float(self.settings.compiler.version.value) < 14:
           raise ConanInvalidConfiguration("Double Convertion could not be built by MSVC <14")

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
"""

CONAN_FILE_OLD = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class DoubleConversionConan(ConanFile):
    name = "double-conversion"
    version = "3.0.0"
    url = "https://github.com/bincrafters/conan-double-conversion"
    homepage = "https://github.com/google/double-conversion"
    author = "Bincrafters <bincraters@gmail.com>"
    description = "Efficient binary-decimal and decimal-binary conversion routines for IEEE doubles."
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"


    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           float(self.settings.compiler.version.value) < 14:
           raise Exception("Double Convertion could not be built by MSVC <14")

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
"""

CONAN_FILE_OLD_MULTILINE = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class DoubleConversionConan(ConanFile):
    name = "double-conversion"
    version = "3.0.0"
    url = "https://github.com/bincrafters/conan-double-conversion"
    homepage = "https://github.com/google/double-conversion"
    author = "Bincrafters <bincraters@gmail.com>"
    description = "Efficient binary-decimal and decimal-binary conversion routines for IEEE doubles."
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = ("shared=False",
     "fPIC=True")
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"


    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           float(self.settings.compiler.version.value) < 14:
           raise Exception("Double Convertion could not be built by MSVC <14")

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
"""

APPVEYOR_FILE = """build: false

environment:
    PYTHON: "C:\\\\Python27"
    PYTHON_VERSION: "2.7.8"
    PYTHON_ARCH: "32"

    matrix:
        - APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio 2015
          CONAN_VISUAL_VERSIONS: 14
          CONAN_BUILD_TYPES: Release
        - APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio 2015
          CONAN_VISUAL_VERSIONS: 14
          CONAN_BUILD_TYPES: Debug
        - APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio 2017
          CONAN_VISUAL_VERSIONS: 15
          CONAN_BUILD_TYPES: Release
        - APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio 2017
          CONAN_VISUAL_VERSIONS: 15
          CONAN_BUILD_TYPES: Debug

install:
  - set PATH=%PATH%;%PYTHON%/Scripts/
  - pip.exe install conan --upgrade
  - pip.exe install conan_package_tools bincrafters_package_tools
  - conan user # It creates the conan data directory

test_script:
  - python build.py
"""

EXPECTED_APPVEYOR_FILE = """build: false

environment:
    PYTHON: "C:\\\\Python37"

    matrix:
        - APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio 2015
          CONAN_VISUAL_VERSIONS: 14
          CONAN_BUILD_TYPES: Release
        - APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio 2015
          CONAN_VISUAL_VERSIONS: 14
          CONAN_BUILD_TYPES: Debug
        - APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio 2017
          CONAN_VISUAL_VERSIONS: 15
          CONAN_BUILD_TYPES: Release
        - APPVEYOR_BUILD_WORKER_IMAGE: Visual Studio 2017
          CONAN_VISUAL_VERSIONS: 15
          CONAN_BUILD_TYPES: Debug

install:
  - set PATH=%PATH%;%PYTHON%/Scripts/
  - pip.exe install conan --upgrade
  - pip.exe install conan_package_tools bincrafters_package_tools
  - conan user # It creates the conan data directory

test_script:
  - python build.py
"""


def test_update_travis_file():
    """ Create a standard travis file and update it.
    """
    _, travis_path = tempfile.mkstemp(prefix='travis', suffix='.yml')
    with open(travis_path, 'w') as file:
        file.write(TRAVIS_FILE)

    _, expected_path = tempfile.mkstemp(prefix='travis', suffix='.yml')
    with open(expected_path, 'w') as file:
        file.write(EXPECTED_TRAVIS_FILE)

    args = ['--travisfile', travis_path]
    command = Command()
    command.run(args)

    assert filecmp.cmp(travis_path, expected_path)


def test_updated_conanfile():
    """ Try to update an up-to-date file
    """
    _, conan_path = tempfile.mkstemp(prefix='conanfile', suffix='.py')
    with open(conan_path, 'w') as file:
        file.write(EXPECTED_CONAN_FILE)

    _, expected_path = tempfile.mkstemp(prefix='conanfile', suffix='.py')
    with open(expected_path, 'w') as file:
        file.write(EXPECTED_CONAN_FILE)

    args = ['--conanfile', conan_path]
    command = Command()
    command.run(args)

    assert filecmp.cmp(conan_path, expected_path)


def test_conanfile_default_options():
    """ Try to update an up-to-date file
    """
    _, conan_path = tempfile.mkstemp(prefix='conanfile', suffix='.py')
    with open(conan_path, 'w') as file:
        file.write(CONAN_FILE_OLD)

    _, expected_path = tempfile.mkstemp(prefix='conanfile', suffix='.py')
    with open(expected_path, 'w') as file:
        file.write(EXPECTED_CONAN_FILE)

    args = ['--conanfile', conan_path]
    command = Command()
    command.run(args)

    assert filecmp.cmp(conan_path, expected_path)


def test_conanfile_default_options_mutiline():
    """ Try to update an up-to-date file
    """
    _, conan_path = tempfile.mkstemp(prefix='conanfile', suffix='.py')
    with open(conan_path, 'w') as file:
        file.write(CONAN_FILE_OLD_MULTILINE)

    _, expected_path = tempfile.mkstemp(prefix='conanfile', suffix='.py')
    with open(expected_path, 'w') as file:
        file.write(EXPECTED_CONAN_FILE)

    args = ['--conanfile', conan_path]
    command = Command()
    command.run(args)

    assert filecmp.cmp(conan_path, expected_path)


def test_appveyor_update():
    """ Try to update an up-to-date file
    """
    _, appveyor_path = tempfile.mkstemp(prefix='appveyor', suffix='.yml')
    with open(appveyor_path, 'w') as file:
        file.write(APPVEYOR_FILE)

    _, expected_path = tempfile.mkstemp(prefix='appveyor', suffix='.yml')
    with open(expected_path, 'w') as file:
        file.write(EXPECTED_APPVEYOR_FILE)

    args = ['--appveyorfile', appveyor_path]
    command = Command()
    command.run(args)

    assert filecmp.cmp(appveyor_path, expected_path)


def test_update_travis_file_with_global():
    """ Create a standard travis file and update it.
    """
    _, travis_path = tempfile.mkstemp(prefix='travis', suffix='.yml')
    with open(travis_path, 'w') as file:
        file.write(TRAVIS_FILE_WITH_GLOBAL)

    _, expected_path = tempfile.mkstemp(prefix='travis', suffix='.yml')
    with open(expected_path, 'w') as file:
        file.write(EXPECTED_TRAVIS_FILE_WITH_GLOBAL)

    args = ['--travisfile', travis_path]
    command = Command()
    command.run(args)

    assert filecmp.cmp(travis_path, expected_path)
