# -*- coding: utf-8 -*-

from conans import tools

from .test_check_for_deprecation import _create_recipe, MockOutputResultCheck
from bincrafters_conventions.actions.check_for_download_hash import check_for_download_hash
from bincrafters_conventions.actions.check_for_required_attributes import check_for_required_attributes
from bincrafters_conventions.actions.update_c_attributes import update_c_topics

CONANFILE_SRC_TOOLS_GET = '''
from conans import ConanFile, tools

class FooConan(ConanFile):
    name = "foo"
    version = "0.1"

    def source(self):
        {source_body}
'''


def test_sha256_checksum_no_tools_get():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='pass'))
    check_for_download_hash(mock_output, recipe)
    assert mock_output.passed == True
    assert mock_output.skipped == True
    assert 'tools.get() isn\'t used' in mock_output.reason


def test_sha256_checksum_tools_get_missing_checksum():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("some_url")'))
    check_for_download_hash(mock_output, recipe)
    assert mock_output.passed == False
    assert 'checksum not found' in mock_output.reason


def test_sha256_checksum_tools_get_checksum():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("some_url", sha256="256")'))
    check_for_download_hash(mock_output, recipe)
    assert mock_output.passed == True
    assert mock_output.skipped == False
    assert 'SHA256 hash in tools.get()' in mock_output.title


def test_sha256_checksum_tools_get_checksum_multiline():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("some_url",\n            sha256="256")'))
    check_for_download_hash(mock_output, recipe)
    assert mock_output.passed == True
    assert mock_output.skipped == False
    assert 'SHA256 hash in tools.get()' in mock_output.title


CONANFILE_SRC_ATTRIBUTE = '''
from conans import ConanFile, tools

class FooConan(ConanFile):
    name = "foo"
    version = "0.1"
    {attribute}
'''


class MockCommand(object):
    def __init__(self):
        self.titles = []

    def output_result_update(self, title):
        self.titles.append(title)

    def replace_in_file(self, file, original, change):
        tools.replace_in_file(file, original, change)


def test_missing_topics():
    mock_output = MockOutputResultCheck()

    conanfile_original = CONANFILE_SRC_ATTRIBUTE.format(attribute='')
    recipe = _create_recipe(conanfile_original)
    check_for_required_attributes(mock_output, recipe)

    assert mock_output.passed == False
    assert mock_output.title == 'Required recipe attributes'
    assert 'topics' in mock_output.reason

    mock_main = MockCommand()
    res = update_c_topics(mock_main, recipe)
    assert res is False

    conanfile_new = open(recipe).read()
    assert conanfile_original == conanfile_new


def test_update_topics_no_parentheses():
    mock_output = MockOutputResultCheck()

    conanfile_original = CONANFILE_SRC_ATTRIBUTE.format(attribute='''topics = 'conan', 'hallo', ''')
    recipe = _create_recipe(conanfile_original)
    check_for_required_attributes(mock_output, recipe)

    assert mock_output.passed == False
    assert mock_output.title == 'Required recipe attributes'
    assert 'topics' not in mock_output.reason

    mock_main = MockCommand()
    res = update_c_topics(mock_main, recipe)
    assert res is True

    conanfile_new = open(recipe).read()
    assert conanfile_original != conanfile_new
    assert """topics = ('conan', 'hallo')""" in conanfile_new


def test_update_topics_parentheses():
    mock_output = MockOutputResultCheck()
    conanfile_original = CONANFILE_SRC_ATTRIBUTE.format(attribute='''topics = ('conan', 'hallo', )''')
    recipe = _create_recipe(conanfile_original)
    check_for_required_attributes(mock_output, recipe)

    assert mock_output.passed == False
    assert mock_output.title == 'Required recipe attributes'
    assert 'topics' not in mock_output.reason

    mock_main = MockCommand()
    res = update_c_topics(mock_main, recipe)
    assert res is False

    conanfile_new = open(recipe).read()
    assert conanfile_original == conanfile_new
    