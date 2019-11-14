import os


def check_for_download_hash(main, file):

    if not os.path.exists("conandata.yml") and not main.file_contains(file, "tools.get"):
        main.output_result_check(passed=True, skipped=True, title="Conandata.yml + tools.get()", reason="tools.get() isn't used")
        return True

    if os.path.exists("conandata.yml")\
            and main.file_contains(file, 'tools.get(**self.conan_data["sources"][self.version])'):
        main.output_result_check(passed=True, title="Conandata.yml + tools.get()")
        return True

    main.output_result_check(passed=False, title="Conandata.yml + tools.get()",
                             reason="Either Conandata.yml doesn't exist or not used in tools.get()")
    return False
