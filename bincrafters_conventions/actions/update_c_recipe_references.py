import os


def update_c_recipe_references(main, file):
    """ This update script updates Conan references, mostly

    :param file: Conan file path
    """

    if not os.path.isfile(file):
        return False

    references_updated = False

    references = {
        "zlib/1.2.8@conan/stable": "zlib/1.2.11",
        "zlib/1.2.9@conan/stable": "zlib/1.2.11",
        "zlib/1.2.11@conan/stable": "zlib/1.2.11",

        "zstd/1.3.8@bincrafters/stable": "zstd/1.3.8",
        "zstd/1.4.0@bincrafters/stable": "zstd/1.4.3",

        "strawberryperl/5.28.1.1@conan/stable": "strawberryperl/5.28.1.1",
        "strawberryperl/5.30.0.1@conan/stable": "strawberryperl/5.30.0.1",

        "sqlite3/3.29.0@bincrafters/stable": "sqlite3/3.29.0",

        "self.deps_cpp_info['Poco']": "self.deps_cpp_info['poco']",
        'self.deps_cpp_info["Poco"]': 'self.deps_cpp_info["poco"]',
        "Poco/1.8.1@pocoproject/stable": "poco/1.8.1",
        "Poco/1.9.3@pocoproject/stable": "poco/1.9.3",

        "self.deps_cpp_info['OpenSSL']": "self.deps_cpp_info['openssl']",
        'self.deps_cpp_info["OpenSSL"]': 'self.deps_cpp_info["openssl"]',
        "OpenSSL/1.0.2s@conan/stable": "openssl/1.0.2t",
        "OpenSSL/1.0.2t@conan/stable": "openssl/1.0.2t",
        "OpenSSL/1.1.0k@conan/stable": "openssl/1.1.0l",
        "OpenSSL/1.1.0l@conan/stable": "openssl/1.1.0l",
        "OpenSSL/1.1.1c@conan/stable": "openssl/1.1.1d",
        "OpenSSL/1.1.1d@conan/stable": "openssl/1.1.1d",

        "nasm/2.13.01@conan/stable": "nasm/2.13.02",
        "nasm_installer/2.13.02@bincrafters/stable": "nasm/2.13.02",

        "msys2_installer/20161025@bincrafters/stable": "msys2/20161025",

        "libjpeg/9b@bincrafters/stable": "libjpeg/9c",
        "libjpeg/9c@bincrafters/stable": "libjpeg/9c",

        "fmt/5.3.0@bincrafters/stable": "fmt/5.3.0",

        "self.deps_cpp_info['Expat']": "self.deps_cpp_info['expat']",
        'self.deps_cpp_info["Expat"]': 'self.deps_cpp_info["expat"]',
        "Expat/2.2.1@pix4d/stable": "expat/2.2.7",
        "Expat/2.2.2@pix4d/stable": "expat/2.2.7",
        "Expat/2.2.3@pix4d/stable": "expat/2.2.7",
        "Expat/2.2.4@pix4d/stable": "expat/2.2.7",
        "Expat/2.2.5@pix4d/stable": "expat/2.2.7",
        "Expat/2.2.6@pix4d/stable": "expat/2.2.7",
        "Expat/2.2.7@pix4d/stable": "expat/2.2.7",

        "bzip2/1.0.6@conan/stable": "bzip2/1.0.6",
        "bzip2/1.0.8@conan/stable": "bzip2/1.0.8",

        "boost/1.70.0@conan/stable": "boost/1.70.0",
        "boost/1.71.0@conan/stable": "boost/1.71.0",
    }

    for old_ref, new_ref in references.items():
        if main.replace_in_file(file, old_ref, new_ref):
            msg = "Update Conan recipe reference from {} to {}".format(old_ref, new_ref)
            main.output_result_update(title=msg)
            references_updated = True

    if references_updated:
        return True

    return False

