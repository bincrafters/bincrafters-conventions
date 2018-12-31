from conans.client import conan_api
from conans.errors import ConanException


def check_for_required_attributes(main, file):
    """  Check if the conan file has all attributes we do require from recipes
    If you want to validate the individual attributes please create own checks for it
    See check_for_spdx_license as a reference
    """
    conan_instance, _, _ = conan_api.Conan.factory()
    not_found = []
    for field in ["name", "description", "topics", "url", "homepage", "author", "license"]:
        try:
            if conan_instance.inspect(path=file, attributes=[field])[field] is None:
                not_found.append(field)
        except ConanException:
            not_found.append(field)

    if len(not_found) >= 1:
        main.output_result_check(passed=False, title="Required recipe attributes",
                                 reason="missing attribute(s): {}".format(', '.join(map(str, not_found))))
        return False
    else:
        main.output_result_check(passed=True, title="Required recipe attributes")
        return True
