#!/usr/bin/env python
# -*- coding: utf-8 -*-


def check_for_deprecated_methods(main, file):
    conanfile = open(file, 'r')
    recipe = conanfile.read()
    conanfile.close()

    for deprecated in ['self.conanfile_directory', 'ConfigureEnvironment', 'werror',
                       'build_sln_command', 'msvc_build_command', 'cmake.build_type']:
        if deprecated in recipe:
            main.output_result_check(passed=False, title="Deprecated method",
                                     reason="detected '{}' in recipe".format(deprecated))
            return False
    return True
