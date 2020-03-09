import os


def update_a_python_version(main, path, current_python_version):
    """ Update Python version

    :param path: AppVeyor yaml file
    :param current_python_version: Current Python version in AppVeyor-like style
    """

    result = False
    current_version_string = "Python{}".format(current_python_version)

    if not main.file_contains(path, current_version_string):
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

    if result:
        main.output_result_update(title="Update Python version which is used by AppVeyor")

    return result
