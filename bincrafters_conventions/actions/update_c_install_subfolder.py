def update_c_install_subfolder(main, file):
    """ Replace install subfolder from Conan recipe
    """

    if (main.replace_in_file(file, " install_subfolder =", " _install_subfolder =") and
            main.replace_in_file(file, "self.install_subfolder", "self._install_subfolder")):
        main.output_result_update(title="Rename install_subfolder to _install_subfolder")
        return True
    return False
