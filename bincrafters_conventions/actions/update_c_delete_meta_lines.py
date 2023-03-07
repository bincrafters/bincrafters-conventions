def update_c_delete_meta_lines(main, file):
    """ This update script deletes several meta lines

    :param file: Conan file path
    """

    updated_global = False

    # noinspection SpellCheckingInspection
    line_deleting = [
        "#!/usr/bin/env python",
        "#!/usr/local/bin/python",
        "# -*- coding: utf-8 -*-",
        "# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4",
    ]

    test_package = file.replace("conanfile.py", "test_package/conanfile.py")

    for file in [file, test_package]:
        updated = False
        first_lines_deleted = False
        content = ""

        with open(file) as ifd:
            for line in ifd:
                delete_line = False
                if not first_lines_deleted:
                    for line_pattern in line_deleting:
                        if line.strip() == line_pattern.strip():
                            deleted_line_output = line.strip()
                            main.output_result_update(f"Delete meta line: {deleted_line_output}")
                            delete_line = True
                            updated = True

                if delete_line:
                    continue
                elif first_lines_deleted is False and line.strip() == "":
                    first_lines_deleted = True
                    continue
                else:
                    content += line

        if updated:
            with open(file, 'w') as fd:
                fd.write(content)
            updated_global = True

    return updated_global
