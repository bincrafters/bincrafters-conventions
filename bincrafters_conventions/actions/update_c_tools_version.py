def update_c_tools_version(main, file):
    """ Update Version import
    """
    if main.replace_in_file(file, "from conans.model.version import Version", "from conans.tools import Version"):
        main.output_result_update(title="Update 'Version' import")
        return True
    return False
