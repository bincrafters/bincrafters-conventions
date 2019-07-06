# -*- coding: utf-8 -*-


def update_c_check_header(main, file):
    result = False
    firstline = open(file, "r").readline()
    if firstline.startswith("#!"):
        main.output_result_update(title="Remove shebang from conanfile")
        main.replace_in_file(file, firstline, "")
        result = True

    coding_part = "# -*- coding:"
    coding_text = "# -*- coding: utf-8 -*-"
    firstline = open(file, "r").readline()
    wholetext = open(file, "r").read()
    if coding_part in wholetext:
        if coding_part not in firstline:
            main.output_result_check(passed=False, title="encoding",
                                     reason="encoding header not on first line ({})".format(coding_text))
    else:
        open(file, "w").write(coding_text + "\n" + wholetext)
        result = True

    return result
