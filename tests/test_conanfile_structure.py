# -*- coding: utf-8 -*-

from conans import tools

from .test_check_for_deprecation import _create_recipe, MockOutputResultCheck
from bincrafters_conventions.actions.check_for_download_hash import check_for_download_hash
from bincrafters_conventions.actions.check_for_required_attributes import check_for_required_attributes
from bincrafters_conventions.actions.update_c_attributes import update_c_topics, update_c_author

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
    res = check_for_download_hash(mock_output, recipe)
    assert res == True
    assert mock_output.passed == True
    assert mock_output.skipped == True
    assert 'tools.get() isn\'t used' in mock_output.reason


def test_sha256_checksum_tools_get_missing_checksum():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("some_url")'))
    res = check_for_download_hash(mock_output, recipe)
    assert res == False
    assert mock_output.passed == False
    assert 'checksum not found' in mock_output.reason


def test_sha256_checksum_tools_get_checksum():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("some_url", sha256="256")'))
    res = check_for_download_hash(mock_output, recipe)
    assert res == True
    assert mock_output.passed == True
    assert mock_output.skipped == False
    assert 'SHA256 hash in tools.get()' in mock_output.title


def test_sha256_checksum_tools_get_checksum_variable():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("www.{}.com".format(domain), sha256=sha256)'))
    res = check_for_download_hash(mock_output, recipe)
    assert res == True
    assert mock_output.passed == True
    assert mock_output.skipped == False
    assert 'SHA256 hash in tools.get()' in mock_output.title


def test_sha256_checksum_tools_get_checksum_multiline():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("some_url",\n        sha256="256")'))
    res = check_for_download_hash(mock_output, recipe)
    assert res == True
    assert mock_output.passed == True
    assert mock_output.skipped == False
    assert 'SHA256 hash in tools.get()' in mock_output.title


def test_sha256_checksum_tools_get_false_positive():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("some\\") _url")\n        method(sha256="abcdef")'))
    res = check_for_download_hash(mock_output, recipe)
    assert res == False
    assert mock_output.passed == False
    assert 'checksum not found' in mock_output.reason


def test_sha256_checksum_tools_get_multiple_fail():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("some", sha256="abcdef")\n        tools.get("abc")'))
    res = check_for_download_hash(mock_output, recipe)
    assert res == False
    assert mock_output.passed == False
    assert 'checksum not found' in mock_output.reason


def test_sha256_checksum_tools_get_multiple_success():
    mock_output = MockOutputResultCheck()

    recipe = _create_recipe(CONANFILE_SRC_TOOLS_GET.format(source_body='tools.get("some", sha256="abcdef")\n        tools.get("abc", sha256="abcdef")'))
    res = check_for_download_hash(mock_output, recipe)
    assert res == True
    assert mock_output.passed == True
    assert mock_output.skipped == False


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


def test_missing_license():
    mock_output = MockOutputResultCheck()

    conanfile_original = CONANFILE_SRC_ATTRIBUTE.format(attribute='')
    recipe = _create_recipe(conanfile_original)
    check_for_required_attributes(mock_output, recipe)

    assert mock_output.passed == False
    assert mock_output.title == 'Required recipe attributes'
    assert 'license' in mock_output.reason


def test_update_author_bincrafters_no_uppercase():
    mock_output = MockOutputResultCheck()

    conanfile_original = CONANFILE_SRC_ATTRIBUTE.format(attribute="""author = 'bincrafters <bincrafters@gmail.com>'""")
    recipe = _create_recipe(conanfile_original)
    check_for_required_attributes(mock_output, recipe)

    mock_main = MockCommand()
    res = update_c_author(mock_main, recipe)
    assert res is True

    conanfile_new = open(recipe).read()
    assert conanfile_original != conanfile_new
    assert """author = 'Bincrafters <bincrafters@gmail.com>""" in conanfile_new
