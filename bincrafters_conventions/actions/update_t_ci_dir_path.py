def update_t_ci_dir_path(main, file):
    """ Update travis folder path in travis file

    :param file: travis file path
    :return:
    """
    if main.replace_in_file(file, ".travis", ".ci"):
        main.output_result_update("Updated .travis -> .ci in travis file")
        return True
    return False
