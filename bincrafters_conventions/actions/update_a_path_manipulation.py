def update_a_path_manipulation(main, file):
    """ Replace PATH manipulating with a PATH setting which actually
        respects our Python version wish
    """
    if main.replace_in_file(file, "set PATH=%PATH%;%PYTHON_HOME%/Scripts/", "set PATH=%PYTHON_HOME%;%PYTHON_HOME%/Scripts/;%PATH%"):
        main.output_result_update(title="AppVeyor: Update PATH manipulation to actually use our specified Python")
        return True
    return False
