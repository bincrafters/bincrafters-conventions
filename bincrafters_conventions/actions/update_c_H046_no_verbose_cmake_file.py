import os


def update_c_H046_no_verbose_cmake_file(main, file):
    """ The CMake file in test_packages should not use CMAKE_VERBOSE_MAKEFILE TRUE
    """

    files = {
        "CMakeLists.txt": os.path.join(os.path.dirname(file), "CMakeLists.txt"),
        "test_package/CMakeLists.txt": os.path.join(os.path.dirname(file), "test_package", "CMakeLists.txt"),
    }

    for display_name, cmake_file in files.items():
        if main.replace_in_file(cmake_file, "set(CMAKE_VERBOSE_MAKEFILE TRUE)\n", ""):
            main.output_result_update(title="H046: Removed set(CMAKE_VERBOSE_MAKEFILE TRUE) from {}".format(display_name))
            return True

    return False
