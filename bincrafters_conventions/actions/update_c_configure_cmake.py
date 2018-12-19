def update_c_configure_cmake(main, file):
    """ Replace configure cmake helper
    """
    if (main.replace_in_file(file, "def configure_cmake", "def _configure_cmake") and
            main.replace_in_file(file, "self.configure_cmake", "self._configure_cmake")):
        main.output_result_update(title="Rename configure_cmake to _configure_cmake")
        return True
    return False
