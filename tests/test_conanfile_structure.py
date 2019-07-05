# -*- coding: utf-8 -*-

from .test_check_for_deprecation import _create_recipe, MockOutputResultCheck
from bincrafters_conventions.actions.check_for_download_hash import check_for_download_hash

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
