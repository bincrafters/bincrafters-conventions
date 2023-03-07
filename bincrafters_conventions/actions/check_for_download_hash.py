import os

# FIXME: This is too unflexible for the recent varities of source() mutations
def check_for_download_hash(main, file):

    if not os.path.exists("conandata.yml") and not main.file_contains(file, "tools.get") and not main.file_contains(file, "get(self"):
        main.output_result_check(passed=True, skipped=True, title="Conandata.yml + tools.get()", reason="get() isn't used")
        return True

    if os.path.exists("conandata.yml")\
        and main.file_contains("conandata.yml", "sha256")\
            and (main.file_contains(file, 'tools.get(**self.conan_data["sources"][self.version]')\
                or main.file_contains(file, 'get(self, **self.conan_data["sources"][self.version]')):
        main.output_result_check(passed=True, title="Conandata.yml + get() is used")
        return True

    main.output_result_check(passed=False, title="Conandata.yml + tools.get()",
                             reason="Either Conandata.yml doesn't exist or not used in get()")
    return False
