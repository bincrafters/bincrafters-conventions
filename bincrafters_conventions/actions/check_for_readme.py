import os


def check_for_readme(main):
    if (os.path.isfile("readme") or os.path.isfile("README") or
        os.path.isfile("README.md") or os.path.isfile("readme.md")):
        main.output_result_check(passed=True, title="Readme")
        return True
    main.output_result_check(passed=False, title="Readme",
                             reason="could not be found. Please check out https://github.com/bincrafters/conan-readme-generator")
    return False
