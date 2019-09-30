def update_c_remove_compiler_cppstd(main, file):
    # Remove self.settings.compiler.cppstd as well, when self.settings.compiler.libcxx is getting removed
    search_string = "del self.settings.compiler.libcxx"
    new_string = "del self.settings.compiler.cppstd"
    if not main.file_contains(file, new_string):
        with open(file) as ifd:
            for line in ifd:
                if line.strip() == search_string:
                    new_string = line.replace(search_string, new_string)
                    new_line = line + new_string

                    if main.replace_in_file(file, line, new_line):
                        main.output_result_update(title="Add del self.settings.compiler.cppstd")
                        return True
    return False
