import os


def update_c_deprecated_attributes(main, file):
    """ This updates deprecated attributes in the conanfile
        Only add attributes here which do have a 1:1 replacement
        If there is no direct replacement then extend/write a check script for it
        and let the developer decide manually
        Automatic replacements should be a safe bet

    :param file: Conan file path
    """

    test_v1_package = file.replace("conanfile.py", os.path.join("test_v1_package", "conanfile.py"))
    test_package = file.replace("conanfile.py", os.path.join("test_package", "conanfile.py"))

    updated = False

    # We need to go regularly though the changelog to catch new deprecations
    # Last checked for Conan versions up to 1.16.1
    deprecations_conan_v1 = {  # Official Conan attributes
        # Conan 1.13.0
        "self.cpp_info.cppflags": "self.cpp_info.cxxflags",

        # Custom attributes
        " install_subfolder =": " _install_subfolder =",
        "self.install_subfolder": "self._install_subfolder",

        " build_subfolder =": " _build_subfolder =",
        "self.build_subfolder": "self._build_subfolder",

        " source_subfolder =": " _source_subfolder =",
        "self.source_subfolder": "self._source_subfolder",

        "def configure_cmake": "def _configure_cmake",
        "self.configure_cmake": "self._configure_cmake",

        # Unknown
        "self.requires.add": "self.requires",
        "self.build_requires.add": "self.build_requires",

        "tools.cross_building(self.settings)": "tools.cross_building(self)",
    }

    deprecations_conan_v2 = {
    }

    deprecations_v1_and_v2 = deprecations_conan_v1.copy()
    deprecations_v1_and_v2.update(deprecations_conan_v2)

    for cfile in [file, test_v1_package, test_package]:
        if cfile == test_v1_package or cfile == test_package:
            if not os.path.exists(cfile):
                continue

        conanfile = open(cfile, 'r')
        recipe = conanfile.read()
        conanfile.close()

        deprecations = deprecations_conan_v1
        if cfile == test_v1_package:
            deprecations = deprecations_v1_and_v2

        for deprecated, replacement in deprecations.items():
            if deprecated in recipe:
                if main.replace_in_file(cfile, deprecated, replacement):
                    main.output_result_update(title=f"Replace deprecated {deprecated} with {replacement}")
                updated = True

    if updated:
        return True

    return False
