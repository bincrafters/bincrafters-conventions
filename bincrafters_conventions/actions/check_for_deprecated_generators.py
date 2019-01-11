#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans.client import conan_api
from conans.errors import ConanException


def check_for_deprecated_generators(main, file):
    """  Check if the conan file if using some deprecated generator
    :param main: Output stream
    :param file: Conanfile path
    """
    conan_instance, _, _ = conan_api.Conan.factory()
    dict_generators = conan_instance.inspect(path=file, attributes=["generators"])
    generators = dict_generators.get('generators')
    generators = [generators] if isinstance(generators, str) else generators
    for generator in generators:
        if generator in ["gcc", "boost-build"]:
            main.output_result_check(passed=False, title="Deprecated generator",
                                     reason="generator: {}".format(generator))
            return False
    return True
