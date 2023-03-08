import os
import yaml

with open(os.path.join(os.path.dirname(__file__), "update_c_recipe_references_manual.yml")) as fd:
    REFERENCES = yaml.load(fd, Loader=yaml.Loader)


def update_c_recipe_references(main, conanfile):
    """ This update script updates Conan references, mostly

    :param file: Conan file path
    """

    if not os.path.isfile(conanfile):
        return False

    files = [conanfile,]

    test_package = os.path.join(os.path.dirname(conanfile), "test_package", "conanfile.py")
    if os.path.isfile(test_package):
        files.append(test_package)

    buildpy = os.path.join(os.path.dirname(conanfile), "build.py")
    if os.path.isfile(buildpy):
        files.append(buildpy)

    references_updated = False

    with open(os.path.join(os.path.dirname(__file__), "update_c_recipe_references_manual_names.yml")) as fd:
        reference_names = yaml.load(fd, Loader=yaml.Loader)

    for old_name, new_name in reference_names.items():
        update_cases = {
            f"self.deps_cpp_info['{old_name}']": f"self.deps_cpp_info['{new_name}']",
            f'self.deps_cpp_info["{old_name}"]': f'self.deps_cpp_info["{new_name}"]',
            f"self.options['{old_name}']": f"self.options['{new_name}']",
            f'self.options["{old_name}"]': f'self.options["{new_name}"]',
        }
        for old_ref, new_ref in update_cases.items():
            for file in files:
                if main.replace_in_file(file, old_ref, new_ref):
                    msg = f"Update reference from {old_ref} to {new_ref}"
                    main.output_result_update(title=msg)
                    references_updated = True

    for old_ref, new_ref in REFERENCES.items():
        for file in files:
            if main.replace_in_file(file, old_ref, new_ref):
                msg = f"Update Conan recipe reference from {old_ref} to {new_ref}"
                main.output_result_update(title=msg)
                references_updated = True

    if references_updated:
        return True

    return False
