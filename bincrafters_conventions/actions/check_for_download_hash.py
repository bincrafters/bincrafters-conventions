import re


def check_for_download_hash(main, file):
    conanfile = open(file, 'r')
    recipe = conanfile.read()
    conanfile.close()

    result_passed = None

    for m in re.finditer(r"tools\.get\((?P<args>.*?[^\\])\)", recipe, re.DOTALL):
        if re.search(r"sha256\s*=\s*(['\"]).*?\1", m["args"], re.DOTALL):
            main.output_result_check(passed=True, title="SHA256 hash in tools.get()")
            result_passed = True if result_passed is None else result_passed
        else:
            main.output_result_check(passed=False, title="SHA256 hash in tools.get()", reason="checksum not found")
            result_passed = False
    if result_passed is None:
        main.output_result_check(passed=True, skipped=True, title="SHA256 hash in tools.get()", reason="tools.get() isn't used")
        result_passed = True
    return result_passed
