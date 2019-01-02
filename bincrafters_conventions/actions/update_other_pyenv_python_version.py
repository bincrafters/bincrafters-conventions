def update_other_pyenv_python_version(main, file, current_python_version, check_for_old_versions):
    """ Replaces which Python version is getting installed in .ci/install.sh for macOS via pyenv
    """

    current_install_string = "pyenv install {}\n".format(current_python_version)
    current_virtualenv_string = "pyenv virtualenv {} conan\n".format(current_python_version)

    for old_version in check_for_old_versions:
        old_install_string = "pyenv install {}\n".format(old_version)
        old_virtualenv_string = "pyenv virtualenv {} conan\n".format(old_version)

        if main.file_contains(file, old_install_string):
            if (main.replace_in_file(file, old_install_string, current_install_string) and
                    main.replace_in_file(file, old_virtualenv_string, current_virtualenv_string)):
                main.output_result_update(title="Update Python version which is installed via pyenv for macOS")
                return True
    return False
