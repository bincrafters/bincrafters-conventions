import os


def update_c_recipe_references(main, file):
    """ This update script updates Conan references, mostly

    :param file: Conan file path
    """

    if not os.path.isfile(file):
        return False

    references_updated = False

    # noinspection SpellCheckingInspection
    references = {
        # Let's eliminate master/latest versions...
        "depot_tools_installer/master@bincrafters/stable": "depot_tools_installer/20190909@bincrafters/stable",

        # CCI adoptions...
        "zlib/1.2.8@conan/stable": "zlib/1.2.11",
        "zlib/1.2.9@conan/stable": "zlib/1.2.11",
        "zlib/1.2.11@conan/stable": "zlib/1.2.11",

        "zstd/1.3.8@bincrafters/stable": "zstd/1.3.8",
        "zstd/1.4.0@bincrafters/stable": "zstd/1.4.3",

        "strawberryperl/5.28.1.1@conan/stable": "strawberryperl/5.28.1.1",
        "strawberryperl/5.30.0.1@conan/stable": "strawberryperl/5.30.0.1",

        "sqlite3/3.29.0@bincrafters/stable": "sqlite3/3.29.0",

        "Poco/1.8.1@pocoproject/stable": "poco/1.8.1",
        "Poco/1.9.3@pocoproject/stable": "poco/1.9.4",
        "Poco/1.9.4@pocoproject/stable": "poco/1.9.4",

        # For newer OpenSSL versions the dedicated update OpenSSL version update script is enough
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

        "gtest/1.8.1@bincrafters/stable": "gtest/1.8.1",

        "libjpeg-turbo/2.0.2@bincrafters/stable": "libjpeg-turbo/2.0.2",

        "libpng/1.6.32@bincrafters/stable": "libpng/1.6.37",
        "libpng/1.6.34@bincrafters/stable": "libpng/1.6.37",
        "libpng/1.6.36@bincrafters/stable": "libpng/1.6.37",
        "libpng/1.6.37@bincrafters/stable": "libpng/1.6.37",

        "libiconv/1.15@bincrafters/stable": "libiconv/1.15",

        "glm/0.9.8.5@bincrafters/stable": "glm/0.9.9.5",
        "glm/0.9.8.5@g-truc/stable": "glm/0.9.9.5",
        "glm/0.9.9.0@g-truc/stable": "glm/0.9.9.5",
        "glm/0.9.9.1@g-truc/stable": "glm/0.9.9.5",
        "glm/0.9.9.4@g-truc/stable": "glm/0.9.9.5",
        "glm/0.9.9.5@g-truc/stable": "glm/0.9.9.5",

        "gsl_microsoft/2.0.0@bincrafters/stable": "ms-gsl/2.0.0",

        "optional-lite/3.2.0@bincrafters/stable": "optional-lite/3.2.0",

        "Catch2/2.9.0@catchorg/stable": "catch2/2.9.2",
        "Catch2/2.9.1@catchorg/stable": "catch2/2.9.2",
        "Catch2/2.9.2@catchorg/stable": "catch2/2.9.2",

        "libwebp/1.0.0@bincrafters/stable": "libwebp/1.0.3",
        "libwebp/1.0.3@bincrafters/stable": "libwebp/1.0.3",

        "protobuf/3.9.1@bincrafters/stable": "protobuf/3.9.1",

        "flatbuffers/1.11.0@google/stable": "flatbuffers/1.11.0",

        "boost_build/4.0.0@bincrafters/testing": "b2/4.0.0",
        "boost_build/4.0.0@bincrafters/stable": "b2/4.0.0",

        "lz4/1.8.0@bincrafters/stable": "lz4/1.9.2",
        "lz4/1.8.2@bincrafters/stable": "lz4/1.9.2",
        "lz4/1.8.3@bincrafters/stable": "lz4/1.9.2",

        "lzma/5.2.3@bincrafters/stable": "xz_utils/5.2.4",
        "lzma/5.2.4@bincrafters/stable": "xz_utils/5.2.4",

        "pcre/8.41@bincrafters/stable": "pcre/8.41",

        "pcre2/10.31@bincrafters/stable": "pcre2/10.33",
        "pcre2/10.32@bincrafters/stable": "pcre2/10.33",
        
        "double-conversion/3.1.1@bincrafters/stable": "double-conversion/3.1.5",
        "double-conversion/3.1.4@bincrafters/stable": "double-conversion/3.1.5",
        "double-conversion/3.1.5@bincrafters/stable": "double-conversion/3.1.5",
        
        "libpq/11.5@bincrafters/stable": "libpq/11.5",
        
        "odbc/2.3.7@bincrafters/stable": "odbc/2.3.7",

        "libffi/3.2.1@bincrafters/stable": "libffi/3.2.1",

        "gflags/2.2.1@bincrafters/stable": "gflags/2.2.2",
        "gflags/2.2.2@bincrafters/stable": "gflags/2.2.2",

        "yas/7.0.2@bincrafters/stable": "yas/7.0.4",
        "yas/7.0.3@bincrafters/stable": "yas/7.0.4",

        "freetype/2.10.0@bincrafters/stable": "freetype/2.10.0",

        "libtiff/4.0.8@bincrafters/stable": "libtiff/4.0.9",
        "libtiff/4.0.9@bincrafters/stable": "libtiff/4.0.9",
    }

    reference_names = {
        "OpenSSL": "openssl",
        "Expat": "expat",
        "Poco": "poco",
        "Catch2": "catch2",
        "boost_build": "b2",
        "gsl_microsoft": "ms-gsl",
        "nasm_installer": "nasm",
        "msys2_installer": "msys2",
        "lzma": "xz_utils",
    }

    for old_name, new_name in reference_names.items():
        update_cases = {
            "self.deps_cpp_info['{}']".format(old_name): "self.deps_cpp_info['{}']".format(new_name),
            'self.deps_cpp_info["{}"]'.format(old_name): 'self.deps_cpp_info["{}"]'.format(new_name),
            "self.options['{}']".format(old_name): "self.options['{}']".format(new_name),
            'self.options["{}"]'.format(old_name): 'self.options["{}"]'.format(new_name),
        }
        for old_ref, new_ref in update_cases.items():
            if main.replace_in_file(file, old_ref, new_ref):
                msg = "Update reference from {} to {}".format(old_ref, new_ref)
                main.output_result_update(title=msg)
                references_updated = True

    for old_ref, new_ref in references.items():
        if main.replace_in_file(file, old_ref, new_ref):
            msg = "Update Conan recipe reference from {} to {}".format(old_ref, new_ref)
            main.output_result_update(title=msg)
            references_updated = True

    if references_updated:
        return True

    return False

