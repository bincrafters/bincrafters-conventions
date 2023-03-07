def check_for_deprecated_generators(main, file):
    """  Check if the Conan file if using some deprecated generator
    :param main: Output stream
    :param file: Conanfile path
    """
    main._compat_api.graph.compat_inspect_attribute(conanfile=file, attribute="generators")
    generators = list(generators)
    for generator in generators:
        if generator in ["gcc", "boost-build"]:
            main.output_result_check(passed=False, title="Deprecated generator",
                                     reason="generator: {}".format(generator))
            return False
    return True
