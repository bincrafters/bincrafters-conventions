def update_c_build_subfolder(main, file):
    """ Replace build subfolder from Conan recipe
    """
    if (main.replace_in_file(file, " build_subfolder =", " _build_subfolder =") and
            main.replace_in_file(file, "self.build_subfolder", "self._build_subfolder")):
        main.output_result_update(title="Rename build_subfolder to _build_subfolder")
        return True
    return False
