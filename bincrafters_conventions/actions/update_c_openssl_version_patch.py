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
    openssl_eol = False

    ccontent = []
    with open(file) as ifd:
        ccontent = ifd.readlines()

    for line in ccontent:
        for key, version_matrix in openssl_version_matrix.items():
            # TODO: After OpenSSL 3 release we need to handle the rename of the recipe to lower-case
            #  + change of version schema
            regex_patch = re.compile('OpenSSL/{}'.format(key) + r'([^\s]+)@conan/stable')

            if regex_patch.search(line):
                latest_patch = version_matrix["latest_patch"]
                patch_found = regex_patch.search(line).group(1)

                if version_matrix["eol"]:
                    main.output_result_check(passed=False,
                                             title="OpenSSL is End-Of-Life",
                                             reason="{} isn't supported anymore. Please upgrade!".format(key),
                                             skipped=False
                                             )
                    openssl_eol = True
                elif patch_found < latest_patch:
                    old_version = "{}{}".format(key, patch_found)
                    new_version = "{}{}".format(key, latest_patch)

                    old_string = "OpenSSL/{}@conan/stable".format(old_version)
                    new_string = "OpenSSL/{}@conan/stable".format(new_version)

                    if main.replace_in_file(file, old_string, new_string):
                        msg = "Update OpenSSL version patch from {} to {}".format(old_version, new_version)
                        main.output_result_update(title=msg)
                        openssl_updated = True

    if openssl_updated or openssl_eol:
        return True

    return False

