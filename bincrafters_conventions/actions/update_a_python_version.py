import os


def update_a_python_version(main, path, current_python_version, check_for_old_versions):
    """ Replace python version

    :param path: Appveyor yaml file
    """
    result = False
    if os.path.isfile(path):
        for old_version in check_for_old_versions:
            old_version_string = old_version.replace(".", "")
            old_install_string = "Python{}".format(old_version_string)

            if main.file_contains(path, old_install_string):
                with open(path) as ifd:
                    content = ifd.readlines()
                with open(path, 'w') as ofd:
                    for line in content:
                        if 'PYTHON_HOME:' in line:
                            line = '    PYTHON_HOME: "C:\\\\Python{}"\n'.format(current_python_version)
                            result = True
                        elif 'PYTHON_VERSION:' in line or 'PYTHON_ARCH:' in line:
                            continue
                        ofd.write(line)
    else:
        main._logger.warning("Could not update {}: File does not exist".format(path))

    if result:
        main.output_result_update(title="Update Python version which is used by AppVeyor")

    return result
