def update_c_deprecated_attributes(main, file):
    """ This updates deprecated attributes in the conanfile
        Only add attributes here which do have a 1:1 replacement
        If there is no direct replacement then extend/write a check script for it
        and let the developer decide manually
        Automatic replacements should be a safe bet

    :param file: Conan file path
    """

    test_package = file.replace("conanfile.py", "test_package/conanfile.py")

    updated = False

    for file in [file, test_package]:
        conanfile = open(file, 'r')
        recipe = conanfile.read()
        conanfile.close()

        # We need to go regularly though the changelog to catch new deprecations
        # Last checked for Conan versions up to 1.14.1
        deprecations = {  # Official Conan attributes
            # Conan 1.13.0
            "self.cpp_info.cppflags": "self.cpp_info.cxxflags",  # 1.13.0

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

            # Conan 1.47
            "from conans.errors import": "from conan.errors import",
        }

        for deprecated, replacement in deprecations.items():
            if deprecated in recipe:
                if main.replace_in_file(file, deprecated, replacement):
                    main.output_result_update(title="Replace deprecated {} with {}".format(deprecated, replacement))
                updated = True

    if updated:
        return True

    return False
