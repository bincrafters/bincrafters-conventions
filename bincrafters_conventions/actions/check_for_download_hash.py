import re


def check_for_download_hash(main, file):
    conanfile = open(file, 'r')
    recipe = conanfile.read()
    conanfile.close()

    if re.search(r'tools\.get\(.+\)', recipe):
        if re.search(r'tools\.get\(.+,\s?sha256=.+\)', recipe):
            main.output_result_check(passed=True, title="SHA256 hash in tools.get()")
            return True
        else:
            main.output_result_check(passed=False, title="SHA256 hash in tools.get()", reason="checksum not found")
            return False
    main.output_result_check(passed=True, skipped=True, title="SHA256 hash in tools.get()", reason="tools.get() isn't used")
    return True
