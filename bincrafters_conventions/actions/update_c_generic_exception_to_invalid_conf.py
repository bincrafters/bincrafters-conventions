def update_c_generic_exception_to_invalid_conf(main, file):
    """ Replace default exception by Invalid config

    :param file: Conan recipe path
    """
    if main.file_contains(file, "raise Exception"):
        if (main.replace_in_file(file, "raise Exception", "raise ConanInvalidConfiguration") and
                main.replace_in_file(file, "import os",
                                      "from conans.errors import ConanInvalidConfiguration\nimport os")):
            main.output_result_update(title="Generic exception to ConanInvalidConfiguration exception")
            return True
    return False
