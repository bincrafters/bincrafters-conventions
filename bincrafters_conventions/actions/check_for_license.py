import os


def check_for_license(main):
    if (os.path.isfile("license") or os.path.isfile("LICENSE") or
            os.path.isfile("license.md") or os.path.isfile("LICENSE.md")) or \
            (os.path.isdir(os.path.join("..", "..", "..", "recipes")) and (
                    os.path.isfile(os.path.join("..", "..", "..", "license")) or
                    os.path.isfile(os.path.join("..", "..", "..", "LICENSE")) or
                    os.path.isfile(os.path.join("..", "..", "..", "license.md")) or
                    os.path.isfile(os.path.join("..", "..", "..", "LICENSE.md"))
            )):
        main.output_result_check(passed=True, title="Recipe license file")
        return True
    main.output_result_check(passed=False, title="Recipe license file",
                             reason="could not be found. Please add a LICENSE.md for the recipe")
    return False
