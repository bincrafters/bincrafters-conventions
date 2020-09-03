import os


def update_c_H048_minimum_cmake_version_required(main, file):
    """ Increases the minimum CMake version in test_packages to at least 3.1
    """
    cmake_file = os.path.join(os.path.dirname(file), "test_package", "CMakeLists.txt")
    old_versions = (
        "cmake_minimum_required(VERSION 2.8)",
        "cmake_minimum_required(VERSION 2.8.11)",
        "cmake_minimum_required(VERSION 2.8.12)",
    )
    new_version = "cmake_minimum_required(VERSION 3.1)"

    for version in old_versions:
        if main.replace_in_file(cmake_file, version, new_version):
            main.output_result_update(title="H048: Update CMake required version in test_package to 3.1")
            return True

    return False
