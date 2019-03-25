def update_a_python_environment_variable(main, file):
    """ Replace %PYTHON% with %PYTHON_HOME% to avoid conflicts with autotools
    """
    if main.replace_in_file(file, "%PYTHON%", "%PYTHON_HOME%") and \
       main.replace_in_file(file, "PYTHON:", "PYTHON_HOME:"):
        main.output_result_update(title="AppVeyor: Update PYTHON environment variable")
        return True
    return False
