import spdx_lookup
from conans.client import conan_api
from conans.errors import ConanException


def check_for_spdx_license(main, file):
    conan_instance, _, _ = conan_api.Conan.factory()
    try:
        recipe_license = conan_instance.inspect(path=file, attributes=['license'])['license']
        if spdx_lookup.by_id(recipe_license):
            main.output_result_check(passed=True, title="SPDX License identifier")
            return True
        else:
            main.output_result_check(passed=False, title="SPDX License identifier",
                                reason="identifier doesn't seem to be a valid SPDX one. Have a look at https://spdx.org/licenses/")
            return False
    except ConanException:
        main.output_result_check(passed=False, title="SPDX License identifier",
                            reason="could not get the license attribute from the Conanfile")
        return False
