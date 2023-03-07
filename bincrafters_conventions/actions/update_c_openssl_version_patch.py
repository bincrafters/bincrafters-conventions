import os
import re


def update_c_openssl_version_patch(main, file, openssl_version_matrix: dict):
    """ This update script updates OpenSSL versions to the latest patch version in the current version branch

    :param file: Conan file path
    :param openssl_version_matrix: Matrix of OpenSSL versions, latest patches, EOL versions
    """

    if not os.path.isfile(file):
        return False

    openssl_updated = False

    ccontent = []
    with open(file) as ifd:
        ccontent = ifd.readlines()

    for line in ccontent:
        for key, version_matrix in openssl_version_matrix.items():
            regex_patches = [
                re.compile(f'OpenSSL/{key}' + r'([^\s]+)@conan/stable'),
                re.compile(f'openssl/{key}' + r'([^\s]+)(\'|\")')
            ]

            for regex_patch in regex_patches:
                if regex_patch.search(line):
                    latest_patch = version_matrix["latest_patch"]
                    patch_found = regex_patch.search(line).group(1)

                    if patch_found < latest_patch:
                        old_version = f"{key}{patch_found}"
                        new_version = f"{key}{latest_patch}"

                        old_string_deprecated = f"OpenSSL/{old_version}@conan/stable"
                        old_string = f"openssl/{old_version}"
                        new_string = f"openssl/{new_version}"

                        if main.replace_in_file(file, old_string, new_string) \
                                or main.replace_in_file(file, old_string_deprecated, new_string):
                            msg = f"Update OpenSSL version patch from {old_version} to {new_version}"
                            main.output_result_update(title=msg)
                            openssl_updated = True

                    if version_matrix["eol"]:
                        main.output_result_check(passed=False,
                                                 title="OpenSSL is End-Of-Life",
                                                 reason=f"{key} isn't supported anymore. Please upgrade!",
                                                 skipped=False
                                                 )

    if openssl_updated:
        return True

    return False
