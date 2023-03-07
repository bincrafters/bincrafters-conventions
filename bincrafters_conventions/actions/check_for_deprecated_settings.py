def check_for_deprecated_settings(main, file):
    """ Check if the file has all valid settings
    """
    settings = main._compat_api.graph.compat_inspect_attribute(conanfile=file, attribute="settings")

    if settings and "cppstd" in settings:
        main.output_result_check(passed=False, title="Deprecated settings",
                                 reason="deprecated attribute(s): {}".format(settings))
        return False
    else:
        main.output_result_check(passed=True, title="Deprecated settings")
        return True
