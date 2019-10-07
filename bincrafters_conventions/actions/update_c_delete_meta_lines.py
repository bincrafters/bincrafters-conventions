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
        first_lines_deleted = True
        content = ""

        with open(file) as ifd:
            for line in ifd:
                delete_line = False
                for line_pattern in line_deleting:
                    if line.strip() == line_pattern.strip():
                        main.output_result_update("Delete meta line: {}".format(line.strip()))
                        delete_line = True
                        updated = True

                if first_lines_deleted is True and line.strip() == "":
                    continue
                elif delete_line is False:
                    content += line
                    first_lines_deleted = False

        if updated:
            with open(file, 'w') as fd:
                fd.write(content)
            updated_global = True

    return updated_global
