import spdx_lookup
from conans.client import conan_api
from conans.errors import ConanException


def check_license(main, recipe_license):
    if spdx_lookup.by_id(recipe_license):
        main.output_result_check(passed=True, title="SPDX License identifier")
        return True
    else:
        main.output_result_check(passed=False, title="SPDX License identifier",
                                 reason="identifier doesn't seem to be a valid SPDX one. "
                                        "Have a look at https://spdx.org/licenses/")
        return False

def check_for_spdx_license(main, file):
    conan_instance, _, _ = conan_api.Conan.factory()
    try:
        recipe_license = conan_instance.inspect(path=file, attributes=['license'])['license']
        if isinstance(recipe_license, str):
            recipe_licenses = [recipe_license]
        elif isinstance(recipe_license, tuple):
            recipe_licenses = recipe_license
        else:
            main.output_result_check(passed=False, title="SPDX License identifier",
                                     reason="license attribute is neither tuple nor string")
            return False

        return all([check_license(main, recipe_license) for recipe_license in recipe_licenses])
    except ConanException:
        main.output_result_check(passed=False, title="SPDX License identifier",
                            reason="could not get the license attribute from the Conanfile")
        return False
