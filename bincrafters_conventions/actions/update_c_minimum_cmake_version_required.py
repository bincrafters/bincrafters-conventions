import os


def update_c_H048_minimum_cmake_version_required(main, file):
    """ Increases the minimum CMake version in test_packages to at least 3.1
    """
    cmake_file = os.path.join(os.path.dirname(file), "test_package", "CMakeLists.txt")
    old_versions = (
        "cmake_minimum_required(VERSION 2.8)",
        "cmake_minimum_required(VERSION 2.8.0)",
        "cmake_minimum_required(VERSION 2.8.1)",
        "cmake_minimum_required(VERSION 2.8.11)",
        "cmake_minimum_required(VERSION 2.8.12)",
    )
    new_version = "cmake_minimum_required(VERSION 3.1)"

    if main.file_contains(cmake_file, "WINDOWS_EXPORT_ALL_SYMBOLS"):

        old_versions.add("cmake_minimum_required(VERSION 3.1.0)")
        old_versions.add("cmake_minimum_required(VERSION 3.1)")
        new_version = "cmake_minimum_required(VERSION 3.4)"

    for version in old_versions:
        if main.replace_in_file(cmake_file, version, new_version):
            main.output_result_update(title="H048: Update CMake required version in test_package to 3.1")
            return True

    return False


def update_c_H049_minimum_cmake_version_required(main, file):
    """ Increases the minimum CMake version in the main CMake file
    """

    cmake_file = os.path.join(os.path.dirname(file), "CMakeLists.txt")

    if not main.file_contains(cmake_file, "WINDOWS_EXPORT_ALL_SYMBOLS"):
        return False

    old_versions = (
        "cmake_minimum_required(VERSION 2.8)",
        "cmake_minimum_required(VERSION 2.8.0)",
        "cmake_minimum_required(VERSION 2.8.1)",
        "cmake_minimum_required(VERSION 2.8.11)",
        "cmake_minimum_required(VERSION 2.8.12)",
        "cmake_minimum_required(VERSION 3.0)",
        "cmake_minimum_required(VERSION 3.0.0)",
        "cmake_minimum_required(VERSION 3.1)",
        "cmake_minimum_required(VERSION 3.1.0)",
    )
    new_version = "cmake_minimum_required(VERSION 3.4)"

    for version in old_versions:
        if main.replace_in_file(cmake_file, version, new_version):
            main.output_result_update(title="H049: Update CMake required version in main CMake file to 3.4")
            return True

    return False
