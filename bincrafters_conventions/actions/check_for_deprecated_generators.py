def check_for_deprecated_generators(main, file):
    """  Check if the Conan file if using some deprecated generator
    :param main: Output stream
    :param file: Conanfile path
    """
    generators = main._compat_api.local.compat_inspect_attribute(conanfile=file, attribute="generators")
    generators = list(generators)
    for generator in generators:
        if generator in ["gcc", "boost-build", "cmake", "cmake_paths", "cmake_find_package", "cmake_find_package_multi", "visual_studio_legacy"]:
            main.output_result_check(passed=False, title="Deprecated generator",
                                     reason=f"generator: {generator}")
            return False
    return True
