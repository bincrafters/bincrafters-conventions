import os


def check_for_license(main):
    if (os.path.isfile("license") or os.path.isfile("LICENSE") or
        os.path.isfile("license.md") or os.path.isfile("LICENSE.md")):
        main.output_result_check(passed=True, title="Recipe license")
        return True
    main.output_result_check(passed=False, title="Recipe license",
                             reason="could not be found. Please add a LICENSE.md for the recipe")
    return False
