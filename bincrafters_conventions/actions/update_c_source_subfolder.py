def update_c_source_subfolder(main, file):
    """ Replace source subfolder from Conan recipe
    """
    if (main.replace_in_file(file, " source_subfolder =", " _source_subfolder =") and
            main.replace_in_file(file, "self.source_subfolder", "self._source_subfolder")):
        main.output_result_update(title="Rename source_subfolder to _source_subfolder")
        return True
    return False
