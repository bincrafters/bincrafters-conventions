from conans.client import conan_api
from conans.errors import ConanException


def check_for_deprecated_settings(main, file):
    """ Check if the file has all valid settings
    """
    conan_instance, _, _ = conan_api.Conan.factory()
    settings = None
    field = "settings"

    try:
        settings = conan_instance.inspect(path=file, attributes=[field])[field]
    except ConanException:
        pass

    if settings and "cppstd" in settings:
        main.output_result_check(passed=False, title="Deprecated settings",
                                 reason="deprecated attribute(s): {}".format(settings))
        return False
    else:
        main.output_result_check(passed=True, title="Deprecated settings")
        return True
