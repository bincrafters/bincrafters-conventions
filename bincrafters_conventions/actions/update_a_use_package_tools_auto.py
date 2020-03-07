def update_a_use_package_tools_auto(main, file):
    """ Migrates AppVeyor to use bincrafters-package-tools auto detection instead of custom build.py
    """
    if main.replace_in_file(file, "python build.py", "bincrafters-package-tools --auto"):
        main.output_result_update(title="AppVeyor: Migrate to use bincrafters-package-tools --auto")
        return True
    return False
