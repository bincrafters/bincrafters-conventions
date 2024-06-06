def check_for_required_attributes(main, file):
    """  Check if the conan file has all attributes we do require from recipes
    If you want to validate the individual attributes please create own checks for it
    See check_for_spdx_license as a reference
    """
    not_found = []
    for field in ["name", "description", "topics", "url", "homepage", "license"]:
        value = main._compat_api.local.compat_inspect_attribute(conanfile=file, attribute=field)
        if value is None or not value:
            not_found.append(field)

    if len(not_found) >= 1:
        missing_attributes = ', '.join(map(str, not_found))
        main.output_result_check(passed=False, title="Required recipe attributes",
                                 reason=f"missing attribute(s): {missing_attributes}")
        return False
    else:
        main.output_result_check(passed=True, title="Required recipe attributes")
        return True
