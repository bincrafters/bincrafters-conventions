def update_t_linux_python_version(main, file, current_python_version, check_for_old_versions):
    """ Replaces which Python version is getting installed for Travis Linux CI
    """

    current_install_string = 'python: "{}"\n'.format(current_python_version)

    for old_version in check_for_old_versions:
        old_install_string = 'python: "{}"\n'.format(old_version)

        if current_install_string == old_install_string:
            continue

        if main.file_contains(file, old_install_string):
            if main.replace_in_file(file, old_install_string, current_install_string):
                main.output_result_update(title="Update Python version which is installed in Linux Travis CI {}".format(current_install_string))
                return True
    return False
