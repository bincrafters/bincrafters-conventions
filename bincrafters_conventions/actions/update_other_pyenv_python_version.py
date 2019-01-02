def update_other_pyenv_python_version(main, file):
    """ Replaces which Python version is getting installed in .ci/install.sh for macOS via pyenv
    """

    current_python_version = "3.7.1"
    check_for_old_versions = ["2.7.10", "3.7.0"]

    current_install_string = "pyenv install {}".format(current_python_version)
    current_virtualenv_string = "pyenv virtualenv {} conan".format(current_python_version)

    for old_version in check_for_old_versions:
        old_install_string = "pyenv install {}".format(old_version)
        old_virtualenv_string = "pyenv virtualenv {} conan".format(old_version)

        if main.file_contains(file, old_install_string):
            if (main.replace_in_file(file, old_install_string, current_install_string) and
                    main.replace_in_file(file, old_virtualenv_string, current_virtualenv_string)):
                main.output_result_update(title="Update Python version which is installed via pyenv for macOS")
                return True
    return False
