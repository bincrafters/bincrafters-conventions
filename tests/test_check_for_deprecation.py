#!/usr/bin/env python

import os

from conans import tools
from conans.util.files import mkdir_tmp

from bincrafters_conventions.actions.check_for_deprecated_generators import check_for_deprecated_generators
from bincrafters_conventions.actions.check_for_deprecated_methods import check_for_deprecated_methods
from bincrafters_conventions.actions.check_for_deprecated_settings import check_for_deprecated_settings
from bincrafters_conventions.bincrafters_conventions import Command

CONANFILE_GENERATOR = """
from conans import ConanFile

class FooConan(ConanFile):
    name = "foo"
    version = "0.1"
    generators = "cmake"{generator}
    url = "https://github.com/bincrafters/foo"
    homepage = "https://github.com/foo/foo"
    author = "Bincrafters"
    description = "Foo Bar"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "arch", "compiler", "build_type"{settings}
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
"""

CONANFILE_BODY = """
def build(self):
    self.output("{method}")
    cmake = CMake(self)
    cmake.configure()
    cmake.build()
"""


class MockOutputResultCheck(object):
    def output_result_check(self, passed: bool, title, reason="", skipped=False):
        self.passed = passed
        self.title = title
        self.reason = reason
        self.skipped = skipped

    def file_contains(self, file, word):
        command = Command()
        return command.file_contains(file, word)


def _create_recipe(content):
    conanfile = os.path.join(mkdir_tmp(), 'conanfile.py')
    tools.save(conanfile, content)
    return conanfile


def test_check_for_deprecated_generators():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_GENERATOR.replace("{generator}", "").replace("{settings}", ""))
    assert check_for_deprecated_generators(mock_output, recipe)

    recipe = _create_recipe(CONANFILE_GENERATOR.replace("{generator}", ',"gcc"').replace("{settings}", ""))
    assert not check_for_deprecated_generators(mock_output, recipe)


def test_check_for_deprecated_methods():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_GENERATOR.replace("{generator}", "") + CONANFILE_BODY.replace("{method}", "Wubba lubba dub dub!"))
    assert check_for_deprecated_methods(mock_output, recipe)

    recipe = _create_recipe(CONANFILE_GENERATOR.replace("{generator}", "") + CONANFILE_BODY.replace("{method}", "self.conanfile_directory"))
    assert not check_for_deprecated_methods(mock_output, recipe)


def test_check_for_deprecated_settings():
    mock_output = MockOutputResultCheck()
    body = CONANFILE_BODY.replace("{method}", "Wubba lubba dub dub!")

    recipe = _create_recipe(CONANFILE_GENERATOR.replace("{generator}", "").replace("{settings}", "") + body)
    assert check_for_deprecated_settings(mock_output, recipe)

    recipe = _create_recipe(CONANFILE_GENERATOR.replace("{generator}", "").replace("{settings}", ', "cppstd"') + body)
    assert not check_for_deprecated_settings(mock_output, recipe)
