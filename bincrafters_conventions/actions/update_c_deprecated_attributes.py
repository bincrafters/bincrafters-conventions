def update_c_deprecated_attributes(main, file):
    conanfile = open(file, 'r')
    recipe = conanfile.read()
    conanfile.close()

    deprecations = {  # Official Conan attributes
                    "self.cpp_info.cppflags": "self.cpp_info.cxxflags",
                      # Custom attributes
                    }

    for deprecated, replacement in deprecations.items():
        if deprecated in recipe:
            if main.replace_in_file(file, deprecated, replacement):
                main.output_result_update(title="Replace deprecated attribute {} with {}".format(deprecated, recipe))
            return True
    return True
