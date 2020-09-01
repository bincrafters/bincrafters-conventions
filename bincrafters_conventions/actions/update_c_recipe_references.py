import os


# noinspection SpellCheckingInspection
REFERENCES = {
    "depot_tools_installer/master@bincrafters/stable": "depot_tools_installer/20190909@bincrafters/stable",
    "depot_tools_installer/20190909@bincrafters/stable": "depot_tools/20200407",
    "depot_tools_installer/20200207@bincrafters/stable": "depot_tools/20200407",
    # TODO: Enable this, when we have a newer version in CCI, so we don't downgrade
    # "depot_tools_installer/20200515@bincrafters/stable": "depot_tools/20200407",

    "zlib/1.2.8@conan/stable": "zlib/1.2.11",
    "zlib/1.2.9@conan/stable": "zlib/1.2.11",
    "zlib/1.2.11@conan/stable": "zlib/1.2.11",

    "zstd/1.3.5@bincrafters/stable": "zstd/1.3.5",
    "zstd/1.3.8@bincrafters/stable": "zstd/1.3.8",
    "zstd/1.4.0@bincrafters/stable": "zstd/1.4.3",

    "strawberryperl/5.28.1.1@conan/stable": "strawberryperl/5.28.1.1",
    "strawberryperl/5.30.0.1@conan/stable": "strawberryperl/5.30.0.1",

    "sqlite3/3.29.0@bincrafters/stable": "sqlite3/3.29.0",

    "Poco/1.8.1@pocoproject/stable": "poco/1.8.1",
    "Poco/1.9.3@pocoproject/stable": "poco/1.9.4",
    "Poco/1.9.4@pocoproject/stable": "poco/1.9.4",
    "Poco/1.10.0@pocoproject/stable": "poco/1.10.1",

    # For newer OpenSSL versions the dedicated update OpenSSL version update script is enough
    "OpenSSL/1.0.2s@conan/stable": "openssl/1.0.2t",
    "OpenSSL/1.0.2t@conan/stable": "openssl/1.0.2t",
    "OpenSSL/latest_1.0.2x@conan/stable": "openssl/1.0.2t",
    "OpenSSL/1.1.0k@conan/stable": "openssl/1.1.0l",
    "OpenSSL/1.1.0l@conan/stable": "openssl/1.1.0l",
    "OpenSSL/latest_1.1.0x@conan/stable": "openssl/1.1.0l",
    "OpenSSL/1.1.1c@conan/stable": "openssl/1.1.1d",
    "OpenSSL/1.1.1d@conan/stable": "openssl/1.1.1d",
    "OpenSSL/latest_1.1.1x@conan/stable": "openssl/1.1.1d",

    "nasm/2.13.01@conan/stable": "nasm/2.13.02",
    "nasm_installer/2.13.02@bincrafters/stable": "nasm/2.13.02",
    "nasm/2.13.02": "nasm/2.14",

    "msys2_installer/latest@bincrafters/stable": "msys2/20190524",
    "msys2_installer/20161025@bincrafters/stable": "msys2/20190524",
    "msys2/20161025": "msys2/20190524",
    # TODO: Good idea?
    # "msys2/20190524": "msys2/20200517",

    "libjpeg/9b@bincrafters/stable": "libjpeg/9d",
    "libjpeg/9c@bincrafters/stable": "libjpeg/9d",
    "libjpeg/9c": "libjpeg/9d",

    "fmt/5.3.0@bincrafters/stable": "fmt/5.3.0",
    "fmt/6.0.0@bincrafters/stable": "fmt/6.0.0",

    "Expat/2.2.1@pix4d/stable": "expat/2.2.9",
    "Expat/2.2.2@pix4d/stable": "expat/2.2.9",
    "Expat/2.2.3@pix4d/stable": "expat/2.2.9",
    "Expat/2.2.4@pix4d/stable": "expat/2.2.9",
    "Expat/2.2.5@pix4d/stable": "expat/2.2.9",
    "Expat/2.2.6@pix4d/stable": "expat/2.2.9",
    "Expat/2.2.7@pix4d/stable": "expat/2.2.9",

    "bzip2/1.0.6@conan/stable": "bzip2/1.0.6",
    "bzip2/1.0.8@conan/stable": "bzip2/1.0.8",

    "boost/1.69.0@conan/stable": "boost/1.69.0",
    "boost/1.70.0@conan/stable": "boost/1.70.0",
    "boost/1.71.0@conan/stable": "boost/1.71.0",

    "gtest/1.8.1@bincrafters/stable": "gtest/1.8.1",

    "libjpeg-turbo/2.0.2@bincrafters/stable": "libjpeg-turbo/2.0.2",
    "libjpeg-turbo/2.0.2": "libjpeg-turbo/2.0.4",
    "libjpeg-turbo/2.0.4": "libjpeg-turbo/2.0.5",

    "libpng/1.6.32@bincrafters/stable": "libpng/1.6.37",
    "libpng/1.6.34@bincrafters/stable": "libpng/1.6.37",
    "libpng/1.6.36@bincrafters/stable": "libpng/1.6.37",
    "libpng/1.6.37@bincrafters/stable": "libpng/1.6.37",

    "libiconv/1.15@bincrafters/stable": "libiconv/1.16",
    "libiconv/1.15": "libiconv/1.16",

    "glm/0.9.8.5@bincrafters/stable": "glm/0.9.9.6",
    "glm/0.9.8.5@g-truc/stable": "glm/0.9.9.6",
    "glm/0.9.9.0@g-truc/stable": "glm/0.9.9.6",
    "glm/0.9.9.1@g-truc/stable": "glm/0.9.9.6",
    "glm/0.9.9.4@g-truc/stable": "glm/0.9.9.6",
    "glm/0.9.9.5@g-truc/stable": "glm/0.9.9.6",
    "glm/0.9.9.6": "glm/0.9.9.8",
    "glm/0.9.9.7": "glm/0.9.9.8",

    "gsl_microsoft/2.0.0@bincrafters/stable": "ms-gsl/2.0.0",

    "optional-lite/3.2.0@bincrafters/stable": "optional-lite/3.2.0",

    "Catch2/2.9.0@catchorg/stable": "catch2/2.11.0",
    "Catch2/2.9.1@catchorg/stable": "catch2/2.11.0",
    "Catch2/2.9.2@catchorg/stable": "catch2/2.11.0",
    "Catch2/2.10.0@catchorg/stable": "catch2/2.11.0",
    "Catch2/2.10.1@catchorg/stable": "catch2/2.11.0",
    "Catch2/2.10.2@catchorg/stable": "catch2/2.11.0",
    "Catch2/2.11.0@catchorg/stable": "catch2/2.11.0",
    "Catch2/2.11.1@catchorg/stable": "catch2/2.11.1",
    "catch2/2.0.1@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.1.0@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.1.1@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.1.2@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.2.0@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.2.1@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.2.2@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.3.0@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.4.0@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.4.1@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.4.2@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.5.0@bincrafters/stable": "catch2/2.11.0",
    "catch2/2.9.2": "catch2/2.11.0",
    "catch2/2.11.0": "catch2/2.11.1",
    "catch2/2.11.1": "catch2/2.11.3",

    "libwebp/1.0.0@bincrafters/stable": "libwebp/1.0.3",
    "libwebp/1.0.3@bincrafters/stable": "libwebp/1.0.3",

    # Note that this might produce that protobuf is added two times (which should be harmless)
    "protobuf/3.9.1@bincrafters/stable": "protobuf/3.9.1",
    "protoc_installer/3.9.1@bincrafters/stable": "protobuf/3.9.1",

    "flatbuffers/1.11.0@google/stable": "flatbuffers/1.11.0",

    "boost_build/4.0.0@bincrafters/testing": "b2/4.1.0",
    "boost_build/4.0.0@bincrafters/stable": "b2/4.1.0",
    "b2/4.0.0": "b2/4.1.0",
    "b2/4.1.0": "b2/4.2.0",

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

    "freetype/2.8.1@bincrafters/stable": "freetype/2.10.1",
    "freetype/2.9.0@bincrafters/stable": "freetype/2.10.1",
    "freetype/2.9.1@bincrafters/stable": "freetype/2.10.1",
    "freetype/2.10.0@bincrafters/stable": "freetype/2.10.1",
    "freetype/2.10.0": "freetype/2.10.1",
    "freetype/2.10.1": "freetype/2.10.2",

    "libtiff/4.0.8@bincrafters/stable": "libtiff/4.0.9",
    "libtiff/4.0.9@bincrafters/stable": "libtiff/4.0.9",

    "libev/4.25@bincrafters/stable": "libev/4.25",
    "libev/4.27@bincrafters/stable": "libev/4.27",

    "libuuid/1.0.3@bincrafters/stable": "libuuid/1.0.3",

    "yaml-cpp/0.6.2@bincrafters/stable": "yaml-cpp/0.6.3",

    "c-ares/1.14.0@conan/stable": "c-ares/1.15.0",
    "c-ares/1.15.0@conan/stable": "c-ares/1.15.0",

    "libssh2/1.8.0@bincrafters/stable": "libssh2/1.9.0",
    "libssh2/1.8.2@bincrafters/stable": "libssh2/1.9.0",

    "jansson/2.10@bincrafters/stable": "jansson/2.12",
    "jansson/2.11@bincrafters/stable": "jansson/2.12",
    "jansson/2.12@bincrafters/stable": "jansson/2.12",

    "giflib/5.1.3@bincrafters/stable": "giflib/5.1.4",
    "giflib/5.1.4@bincrafters/stable": "giflib/5.1.4",

    "yasm_installer/1.3.0@bincrafters/stable": "yasm/1.3.0",

    "ninja_installer/1.8.2@bincrafters/stable": "ninja/1.9.0",
    "ninja_installer/1.9.0@bincrafters/stable": "ninja/1.9.0",
    "ninja/1.9.0": "ninja/1.10.0",

    "libelf/0.8.13@bincrafters/stable": "libelf/0.8.13",

    "mysql-connector-c/6.1.11@bincrafters/stable": "mysql-connector-c/6.1.11",

    "libevent/2.1.8@bincrafters/stable": "libevent/2.1.11",
    "libevent/2.1.10@bincrafters/stable": "libevent/2.1.11",
    "libevent/2.1.11@bincrafters/stable": "libevent/2.1.11",
    "libevent/2.1.11": "libevent/2.1.12",

    "rapidjson/1.1.0@bincrafters/stable": "rapidjson/1.1.0",
    "RapidJSON/1.0.2@inexorgame/stable": "rapidjson/1.1.0",
    "RapidJSON/1.1.0@inexorgame/stable": "rapidjson/1.1.0",

    "glog/20181109@bincrafters/stable": "glog/0.4.0",
    "glog/0.3.5@bincrafters/stable": "glog/0.4.0",
    "glog/0.4.0@bincrafters/stable": "glog/0.4.0",

    "meson_installer/0.49.0@bincrafters/stable": "meson/0.54.0",
    "meson_installer/0.49.2@bincrafters/stable": "meson/0.54.0",
    "meson_installer/0.50.0@bincrafters/stable": "meson/0.54.0",
    "meson_installer/0.51.0@bincrafters/stable": "meson/0.54.0",
    "meson/0.50.0": "meson/0.54.0",
    "meson/0.52.1": "meson/0.54.0",
    "meson/0.53.0": "meson/0.54.0",
    "meson/0.53.1": "meson/0.54.0",
    "meson/0.53.2": "meson/0.54.0",
    "meson/0.54.0": "meson/0.54.1",
    "meson/0.54.1": "meson/0.54.2",
    "meson/0.54.3": "meson/0.54.3",
    "meson/0.54.3": "meson/0.55.0",

    "lcms/2.9@bincrafters/stable": "lcms/2.9",

    "libmount/2.33.1@bincrafters/stable": "libmount/2.33.1",

    "libxml2/2.9.3@bincrafters/stable": "libxml2/2.9.9",
    "libxml2/2.9.8@bincrafters/stable": "libxml2/2.9.9",
    "libxml2/2.9.9@bincrafters/stable": "libxml2/2.9.9",
    "libxml2/2.9.9": "libxml2/2.9.10",

    "nghttp2/1.38.0@bincrafters/stable": "libnghttp2/1.39.2",

    "spdlog/1.4.1@bincrafters/stable": "spdlog/1.4.2",
    "spdlog/1.4.2@bincrafters/stable": "spdlog/1.4.2",

    "jasper/2.0.14@conan/stable": "jasper/2.0.14",

    "libalsa/1.1.5@conan/stable": "libalsa/1.1.9",
    "libalsa/1.1.9@conan/stable": "libalsa/1.1.9",

    "jsonformoderncpp/3.0.0@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.0.1@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.1.0@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.1.1@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.1.2@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.2.0@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.3.0@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.4.0@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.5.0@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.6.0@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.6.1@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.7.0@vthiery/stable": "nlohmann_json/3.7.3",
    "jsonformoderncpp/3.7.0": "nlohmann_json/3.7.3",

    "xerces-c/3.2.2@bincrafters/stable": "xerces-c/3.2.2",
    "xerces-c/3.2.2": "xerces-c/3.2.3",

    "cccl_installer/1.0@bincrafters/stable": "cccl/1.1",

    "asio/1.10.8@bincrafters/stable": "asio/1.13.0",
    "asio/1.11.0@bincrafters/stable": "asio/1.13.0",
    "asio/1.12.0@bincrafters/stable": "asio/1.13.0",
    "asio/1.12.2@bincrafters/stable": "asio/1.13.0",
    "asio/1.13.0@bincrafters/stable": "asio/1.13.0",

    "ENet/1.3.13@inexorgame/stable": "enet/1.3.14",
    "enet/1.3.13@bincrafters/stable": "enet/1.3.14",
    "enet/1.3.14@bincrafters/stable": "enet/1.3.14",

    "http-parser/2.8.1@bincrafters/stable": "http_parser/2.9.2",

    "ogg/1.3.3@bincrafters/stable": "ogg/1.3.4",

    "openjpeg/2.3.0@bincrafters/stable": "openjpeg/2.3.1",
    "openjpeg/2.3.1@bincrafters/stable": "openjpeg/2.3.1",

    "jsoncpp/1.0.0@theirix/stable": "jsoncpp/1.9.2",
    "jsoncpp/1.8.4@theirix/stable": "jsoncpp/1.9.2",
    "jsoncpp/1.9.0@theirix/stable": "jsoncpp/1.9.2",

    "gmp/6.1.2@bincrafters/stable": "gmp/6.1.2",

    "mbedtls/2.6.1@bincrafters/stable": "mbedtls-apache/2.16.3",
    "mbedtls/2.11.0@bincrafters/stable": "mbedtls-apache/2.16.3",
    "mbedtls/2.13.0@bincrafters/stable": "mbedtls-apache/2.16.3",

    "json-c/0.13.1@bincrafters/stable": "json-c/0.13.1",
    "json-c/0.13.1": "json-c/0.13.1",

    "fftw/3.3.8@bincrafters/stable": "fftw/3.3.8",

    "leptonica/1.75.1@bincrafters/stable": "leptonica/1.78.0",
    "leptonica/1.76.0@bincrafters/stable": "leptonica/1.78.0",

    "log4cplus/2.0.0-rc2@bincrafters/stable": "log4cplus/2.0.4",
    "log4cplus/2.0.1@bincrafters/stable": "log4cplus/2.0.4",
    "log4cplus/2.0.2@bincrafters/stable": "log4cplus/2.0.4",
    "log4cplus/2.0.4@bincrafters/stable": "log4cplus/2.0.4",

    "openexr/2.3.0@conan/stable": "openexr/2.3.0",

    "openal/1.18.2@bincrafters/stable": "openal/1.19.1",
    "openal/1.19.0@bincrafters/stable": "openal/1.19.1",
    "openal/1.19.1@bincrafters/stable": "openal/1.19.1",

    "mozjpeg/3.3.1@bincrafters/stable": "mozjpeg/3.3.1",

    "date/2.4@bincrafters/stable": "date/2.4.1",
    "date/2.4.1@bincrafters/stable": "date/2.4.1",

    "snappy/1.1.7@bincrafters/stable": "snappy/1.1.7",

    "docopt/0.6.2@conan/stable": "docopt.cpp/0.6.2",
    "docopt.cpp/0.6.2": "docopt.cpp/0.6.3",

    "libsodium/1.0.15@bincrafters/stable": "libsodium/1.0.18",
    "libsodium/1.0.16@bincrafters/stable": "libsodium/1.0.18",
    "libsodium/1.0.18@bincrafters/stable": "libsodium/1.0.18",

    "libcurl/7.50.3@bincrafters/stable": "libcurl/7.67.0",
    "libcurl/7.52.1@bincrafters/stable": "libcurl/7.67.0",
    "libcurl/7.56.1@bincrafters/stable": "libcurl/7.67.0",
    "libcurl/7.60.0@bincrafters/stable": "libcurl/7.67.0",
    "libcurl/7.61.1@bincrafters/stable": "libcurl/7.67.0",
    "libcurl/7.64.1@bincrafters/stable": "libcurl/7.67.0",
    "libcurl/7.66.0@bincrafters/stable": "libcurl/7.67.0",

    "doctest/2.0.0@bincrafters/stable": "doctest/2.3.5",
    "doctest/2.0.1@bincrafters/stable": "doctest/2.3.5",
    "doctest/2.2.0@bincrafters/stable": "doctest/2.3.5",
    "doctest/2.3.1@bincrafters/stable": "doctest/2.3.5",
    "doctest/2.3.4@bincrafters/stable": "doctest/2.3.5",

    "7z_installer/1.0@conan/stable": "7zip/19.00",

    "IrrXML/1.2@conan/stable": "irrxml/1.2",

    "TBB/4.4.4@conan/stable": "tbb/2019_u9",
    "TBB/2018_U5@conan/stable": "tbb/2019_u9",
    "TBB/2018_U6@conan/stable": "tbb/2019_u9",
    "TBB/2019_U1@conan/stable": "tbb/2019_u9",
    "TBB/2019_U2@conan/stable": "tbb/2019_u9",
    "TBB/2019_U3@conan/stable": "tbb/2019_u9",
    "TBB/2019_U4@conan/stable": "tbb/2019_u9",

    "eastl/3.07.00@bincrafters/stable": "eastl/3.15.00",

    "sqlpp11/0.57@bincrafters/stable": "sqlpp11/0.58",

    "libdwarf/20190505@bincrafters/stable": "libdwarf/20191104",

    "eigen/3.3.4@conan/stable": "eigen/3.3.7",
    "eigen/3.3.5@conan/stable": "eigen/3.3.7",
    "eigen/3.3.7@conan/stable": "eigen/3.3.7",

    "range-v3/0.2.6@ericniebler/stable": "range-v3/0.9.1",
    "range-v3/0.3.0@ericniebler/stable": "range-v3/0.9.1",
    "range-v3/0.3.5@ericniebler/stable": "range-v3/0.9.1",
    "range-v3/0.3.6@ericniebler/stable": "range-v3/0.9.1",
    "range-v3/0.3.7@ericniebler/stable": "range-v3/0.9.1",
    "range-v3/0.4.0@ericniebler/stable": "range-v3/0.9.1",
    "range-v3/0.5.0@ericniebler/stable": "range-v3/0.9.1",
    "range-v3/0.9.0@ericniebler/stable": "range-v3/0.9.1",
    "range-v3/0.9.1@ericniebler/stable": "range-v3/0.9.1",

    "libusb/1.0.21@bincrafters/stable": "libusb/1.0.23",
    "libusb/1.0.22@bincrafters/stable": "libusb/1.0.23",
    "libusb/1.0.23@bincrafters/stable": "libusb/1.0.23",

    "botan/2.1.0@bincrafters/stable": "botan/2.12.1",
    "botan/2.3.0@bincrafters/stable": "botan/2.12.1",
    "botan/2.7.0@bincrafters/stable": "botan/2.12.1",
    "botan/2.8.0@bincrafters/stable": "botan/2.12.1",
    "botan/2.9.0@bincrafters/stable": "botan/2.12.1",
    "botan/2.10.0@bincrafters/stable": "botan/2.12.1",
    "botan/2.11.0@bincrafters/stable": "botan/2.12.1",
    "botan/2.12.1@bincrafters/stable": "botan/2.12.1",

    "libx264/20171211@bincrafters/stable": "libx264/20190605",
    "libx264/20190605@bincrafters/stable": "libx264/20190605",

    "dirent-win32/1.23.2@bincrafters/stable": "dirent/1.23.2",

    "clara/1.1.0@bincrafters/stable": "clara/1.1.5",
    "clara/1.1.1@bincrafters/stable": "clara/1.1.5",
    "clara/1.1.4@bincrafters/stable": "clara/1.1.5",
    "clara/1.1.5@bincrafters/stable": "clara/1.1.5",

    "cctz/2.2@bincrafters/stable": "cctz/2.3",
    "cctz/2.3@bincrafters/stable": "cctz/2.3",

    "jom_installer/1.1.2@bincrafters/stable": "jom/1.1.3",

    "mpfr/4.0.2@bincrafters/stable": "mpft/4.0.2",

    "entt/3.x.y-WIP@skypjack/stable": "entt/3.2.2",
    "entt/3.0.0@skypjack/stable": "entt/3.2.2",
    "entt/3.1.0@skypjack/stable": "entt/3.2.2",
    "entt/3.1.1@skypjack/stable": "entt/3.2.2",
    "entt/3.2.0-RC@skypjack/stable": "entt/3.2.2",
    "entt/v3.2.0-RC@skypjack/stable": "entt/3.2.2",
    "entt/3.2.0-RC1@skypjack/stable": "entt/3.2.2",
    "entt/3.2.0@skypjack/stable": "entt/3.2.2",
    "entt/3.2.1@skypjack/stable": "entt/3.2.2",
    "entt/3.2.2@skypjack/stable": "entt/3.2.2",

    "sqlitecpp/2.2.0@bincrafters/stable": "sqlitecpp/2.5.0",
    "sqlitecpp/2.3.0@bincrafters/stable": "sqlitecpp/2.5.0",
    "sqlitecpp/2.4.0@bincrafters/stable": "sqlitecpp/2.5.0",

    "libfdk_aac/2.0.0@bincrafters/stable": "libfdk_aac/2.0.0",

    "libiberty/9.1.0@bincrafters/stable": "libiberty/9.1.0",

    "libunwind/1.3.1@bincrafters/stable": "libunwind/1.3.1",

    "premake_installer/5.0.0-alpha12@bincrafters/stable": "premake/5.0.0-alpha14",
    "premake_installer/5.0.0-alpha13@bincrafters/stable": "premake/5.0.0-alpha14",
    "premake_installer/5.0.0-alpha14@bincrafters/stable": "premake/5.0.0-alpha14",

    "cmake_installer/3.0.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.0.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.0.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.1.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.1.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.1.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.1.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.2.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.2.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.2.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.2.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.3.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.3.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.3.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.4.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.4.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.4.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.4.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.5.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.5.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.5.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.6.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.6.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.6.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.6.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.7.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.7.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.7.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.8.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.8.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.8.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.9.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.9.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.9.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.9.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.9.4@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.9.5@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.9.6@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.10.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.10.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.10.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.10.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.11.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.11.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.11.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.11.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.11.4@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.12.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.12.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.12.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.12.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.12.4@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.13.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.13.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.13.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.13.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.13.4@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.14.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.14.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.14.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.14.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.14.4@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.14.5@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.14.6@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.14.7@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.15.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.15.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.15.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.15.3@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.15.4@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.15.5@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.16.0@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.16.1@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.16.2@conan/stable": "cmake/3.16.3",
    "cmake_installer/3.16.3@conan/stable": "cmake/3.16.3",
    "cmake/3.16.2": "cmake/3.16.3",
    "cmake/3.16.3": "cmake/3.16.4",
    "cmake/3.16.4": "cmake/3.16.5",

    "opus/1.2.1@bincrafters/stable": "opus/1.3.1",
    "opus/1.3.1@bincrafters/stable": "opus/1.3.1",

    "opusfile/0.10@bincrafters/stable": "opusfile/0.11",

    "libmp3lame/3.100@bincrafters/stable": "libmp3lame/3.100",

    "tcl/8.6.8@bincrafters/stable": "tcl/8.6.10",
    "tcl/8.6.9@bincrafters/stable": "tcl/8.6.10",

    "termcap/1.3.1@bincrafters/stable": "termcap/1.3.1",

    "pixman/0.34.0@bincrafters/stable": "pixman/0.38.4",
    "pixman/0.38.0@bincrafters/stable": "pixman/0.38.4",
    "pixman/0.38.4": "pixman/0.40.0",

    "vorbis/1.3.5@bincrafters/stable": "vorbis/1.3.6",
    "vorbis/1.3.6@bincrafters/stable": "vorbis/1.3.6",
    "vorbis/1.3.6": "vorbis/1.3.7",

    "nettle/3.4@bincrafters/stable": "nettle/3.5",
    "nettle/3.4.1@bincrafters/stable": "nettle/3.5",

    "imgui/1.53@bincrafters/stable": "imgui/1.74",
    "imgui/1.61@bincrafters/stable": "imgui/1.74",
    "imgui/1.62@bincrafters/stable": "imgui/1.74",
    "imgui/1.63@bincrafters/stable": "imgui/1.74",
    "imgui/1.64@bincrafters/stable": "imgui/1.74",
    "imgui/1.65@bincrafters/stable": "imgui/1.74",
    "imgui/1.66@bincrafters/stable": "imgui/1.74",
    "imgui/1.69@bincrafters/stable": "imgui/1.74",
    "imgui/1.73@bincrafters/stable": "imgui/1.74",

    "openh264/1.7.0@bincrafters/stable": "openh264/1.7.0",

    "tweetnacl/20140427@conan/stable": "tweetnacl/20140427",

    "zmq/4.2.2@bincrafters/stable": "zeromq/4.3.2",
    "zmq/4.2.5@bincrafters/stable": "zeromq/4.3.2",
    "zmq/4.3.1@bincrafters/stable": "zeromq/4.3.2",
    "zmq/4.3.2@bincrafters/stable": "zeromq/4.3.2",

    "czmq/4.1.0@bincrafters/stable": "czmq/4.2.0",

    "cppzmq/4.2.2@bincrafters/stable": "cppzmq/4.6.0",
    "cppzmq/4.3.0@bincrafters/stable": "cppzmq/4.6.0",
    "cppzmq/4.4.1@bincrafters/stable": "cppzmq/4.6.0",
    "cppzmq/4.6.0@bincrafters/stable": "cppzmq/4.6.0",
    "cppzmq/4.5.0": "cppzmq/4.6.0",

    "pthread-win32/2.9.1@bincrafters/stable": "pthreads4w/3.0.0",
    "pthreads4w/2.9.1@bincrafters/stable": "pthreads4w/3.0.0",

    "bullet3/2.87@bincrafters/stable": "bullet3/2.89",
    "bullet3/2.88@bincrafters/stable": "bullet3/2.89",

    "sqlpp11-connector-sqlite3/0.29@bincrafters/stable": "sqlpp11-connector-sqlite3/0.29",

    "cpp-sort/1.0.0@morwenn/stable": "cpp-sort/1.6.0",
    "cpp-sort/1.1.0@morwenn/stable": "cpp-sort/1.6.0",
    "cpp-sort/1.1.1@morwenn/stable": "cpp-sort/1.6.0",
    "cpp-sort/1.2.0@morwenn/stable": "cpp-sort/1.6.0",
    "cpp-sort/1.3.0@morwenn/stable": "cpp-sort/1.6.0",
    "cpp-sort/1.4.0@morwenn/stable": "cpp-sort/1.6.0",
    "cpp-sort/1.5.0@morwenn/stable": "cpp-sort/1.6.0",
    "cpp-sort/1.5.1@morwenn/stable": "cpp-sort/1.6.0",
    "cpp-sort/1.6.0@morwenn/stable": "cpp-sort/1.6.0",

    "glad/0.1.24@bincrafters/stable": "glad/0.1.33",
    "glad/0.1.29@bincrafters/stable": "glad/0.1.33",

    "openblas/0.2.20@conan/stable": "openblas/0.3.7",
    "openblas/0.3.5@conan/stable": "openblas/0.3.7",
    "openblas/0.3.7": "openblas/0.3.9",
    "openblas/0.3.9": "openblas/0.3.10",

    "libmad/0.15.1b@bincrafters/stable": "libmad/0.15.1b",

    "libx265/3.0@bincrafters/stable": "libx265/3.2.1",

    # TODO: icu: no installer for now https://github.com/conan-io/conan-center-index/pull/151
    "icu/59.1@bincrafters/stable": "icu/64.2",
    "icu/60.2@bincrafters/stable": "icu/64.2",
    "icu/62.1@bincrafters/stable": "icu/64.2",
    "icu/63.1@bincrafters/stable": "icu/64.2",
    "icu/64.2@bincrafters/stable": "icu/64.2",

    "cereal/1.2.2@conan/stable": "cereal/1.3.0",

    "rapidxml/1.13@bincrafter/stable": "rapidxml/1.13",

    "wtl/10.0.7336@bincrafters/stable": "wtl/10.0.9163",
    "wtl/10.0.9163@bincrafters/stable": "wtl/10.0.9163",

    "paho-c/1.2.0@conan/stable": "paho-mqtt-c/1.3.1",
    "paho-c/1.3.0@conan/stable": "paho-mqtt-c/1.3.1",
    "paho-c/1.3.1@conan/stable": "paho-mqtt-c/1.3.1",
    "paho-mqtt-c/1.3.0": "paho-mqtt-c/1.3.1",

    "paho-cpp/1.0.0@conan/stable": "paho-mqtt-cpp/1.0.1",
    "paho-cpp/1.0.1@conan/stable": "paho-mqtt-cpp/1.0.1",

    "tinyxml2/7.0.0@nicolastagliani/stable": "tinyxml2/7.1.0",
    "tinyxml2/7.0.1@nicolastagliani/stable": "tinyxml2/7.1.0",
    "tinyxml2/7.1.0@nicolastagliani/stable": "tinyxml2/7.1.0",

    "tuple/1.0.0@taocpp/stable": "taocpp-tuple/1.0.0",

    "pegtl/2.5.1@bincrafters/stable": "taocpp-pegtl/2.8.1",
    "pegtl/2.5.2@taocpp/stable": "taocpp-pegtl/2.8.1",
    "pegtl/2.6.0@taocpp/stable": "taocpp-pegtl/2.8.1",
    "pegtl/2.6.1@taocpp/stable": "taocpp-pegtl/2.8.1",
    "pegtl/2.7.0@taocpp/stable": "taocpp-pegtl/2.8.1",
    "pegtl/2.7.1@taocpp/stable": "taocpp-pegtl/2.8.1",
    "pegtl/2.8.0@taocpp/stable": "taocpp-pegtl/2.8.1",
    "pegtl/2.8.1@taocpp/stable": "taocpp-pegtl/2.8.1",

    "operators/1.0.2@taocpp/stable": "taocpp-operators/1.2.2",
    "operators/1.1.1@taocpp/stable": "taocpp-operators/1.2.2",
    "operators/1.2.0@taocpp/stable": "taocpp-operators/1.2.2",
    "operators/1.2.2@taocpp/stable": "taocpp-operators/1.2.2",

    "sequences/2.0.1@taocpp/stable": "taocpp-sequences/2.0.1",

    "stb/20180214@conan/stable": "stb/20200203",
    "stb/20190512@conan/stable": "stb/20200203",

    "abseil/20181200@bincrafters/stable": "abseil/20200225.2",
    "abseil/20200205": "abseil/20200225.2",

    "c-blosc/v1.12.4b8@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.13.5@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.13.6@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.13.7@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.14.0@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.14.1@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.14.2@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.14.3@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.14.4@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.15.0@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/1.15.1@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.16.0@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.16.1@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.16.2@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.16.3@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.17.0@francescalted/stable": "c-blosc/1.17.1",
    "c-blosc/v1.17.1@francescalted/stable": "c-blosc/1.17.1",

    "libqrencode/4.0.0@bincrafters/stable": "libqrencode/4.0.0",

    "geographiclib/1.49.0@bincrafters/stable": "geographiclib/1.50.1",

    "gettext/0.20.1@bincrafters/stable": "libgettext/0.20.1",
    "gettext_installer/0.20.1@bincrafters/stable": "gettext/0.20.1",

    "msgpack/3.0.1@bincrafters/stable": "msgpack/3.2.1",
    "msgpack/3.1.1@bincrafters/stable": "msgpack/3.2.1",
    "msgpack/3.2.0@bincrafters/stable": "msgpack/3.2.1",
    "msgpack/3.2.1@bincrafters/stable": "msgpack/3.2.1",

    "getopt/1.0@bincrafters/stable": "getopt-for-visual-studio/20200201",
    "getopt/2.0@bincrafters/stable": "getopt-for-visual-studio/20200201",

    "blaze/3.3@conan/release": "blaze/3.7",

    "libmodplug/0.8.9.0@bincrafters/stable": "libmodplug/0.8.9.0",

    "flac/1.3.2@bincrafters/stable": "flac/1.3.3",

    "gperf_installer/3.1@conan/stable": "gperf/3.1",

    "libuv/1.15.0@bincrafters/stable": "libuv/1.34.2",
    "libuv/1.23.2@bincrafters/stable": "libuv/1.34.2",
    "libuv/1.24.0@bincrafters/stable": "libuv/1.34.2",
    "libuv/1.25.0@bincrafters/stable": "libuv/1.34.2",
    "libuv/1.27.0@bincrafters/stable": "libuv/1.34.2",
    "libuv/1.31.0@bincrafters/stable": "libuv/1.34.2",

    "libpqxx/7.0.0@bincrafters/stable": "libpqxx/7.0.5",
    "libpqxx/7.0.1@bincrafters/stable": "libpqxx/7.0.5",
    "libpqxx/7.0.1": "libpqxx/7.0.5",
    "libpqxx/7.0.2": "libpqxx/7.0.5",
    "libpqxx/7.0.3": "libpqxx/7.0.5",
    "libpqxx/7.0.4": "libpqxx/7.0.5",
    "libpqxx/7.0.5": "libpqxx/7.0.6",
    "libpqxx/7.0.6": "libpqxx/7.0.7",

    "m4_installer/1.4.18@bincrafters/stable": "m4/1.4.18",

    "websocketpp/0.7.0@bincrafters/stable": "websocketpp/0.8.1",
    "websocketpp/0.8.0@bincrafters/stable": "websocketpp/0.8.1",
    "websocketpp/0.8.1@bincrafters/stable": "websocketpp/0.8.1",
    "websocketpp/0.8.1": "websocketpp/0.8.2",

    "folly/2018.11.12.00@bincrafters/stable": "folly/2019.10.21.00",

    "rxcpp/4.0.0@bincrafters/stable": "rxcpp/4.1.0",
    "rxcpp/4.1.0@bincrafters/stable": "rxcpp/4.1.0",

    "spirv-headers/1.3.7@bincrafters/stable": "spirv-headers/1.5.1",
    "spirv-headers/1.4.1@bincrafters/stable": "spirv-headers/1.5.1",

    "tesseract/4.0.0@bincrafters/stable": "tesseract/4.1.1",

    "cpprestsdk/2.9.1@bincrafters/stable": "cpprestsdk/2.10.15",
    "cpprestsdk/2.10.1@bincrafters/stable": "cpprestsdk/2.10.15",
    "cpprestsdk/2.10.2@bincrafters/stable": "cpprestsdk/2.10.15",
    "cpprestsdk/2.10.10@bincrafters/stable": "cpprestsdk/2.10.15",
    "cpprestsdk/2.10.12@bincrafters/stable": "cpprestsdk/2.10.15",
    "cpprestsdk/2.10.13@bincrafters/stable": "cpprestsdk/2.10.15",
    "cpprestsdk/2.10.14@bincrafters/stable": "cpprestsdk/2.10.15",
    "cpprestsdk/2.10.15@bincrafters/stable": "cpprestsdk/2.10.15",
    "cpprestsdk/2.10.15": "cpprestsdk/2.10.16",

    # Note that this might produce that bison is added two times (which should be harmless)
    "bison/3.0.4@bincrafters/stable": "bison/3.5.3",
    "bison/3.0.5@bincrafters/stable": "bison/3.5.3",
    "bison/3.3.2@bincrafters/stable": "bison/3.5.3",
    "bison_installer/3.2.4@bincrafters/stable": "bison/3.5.3",
    "bison_installer/3.3.2@bincrafters/stable": "bison/3.5.3",

    "frozen/20181020@bincrafters/stable": "frozen/1.0.0",

    "libsndfile/1.0.28@bincrafters/stable": "libsndfile/1.0.28",

    "rang/3.0.0@rang/stable": "rang/3.1.0",
    "rang/3.1.0@rang/stable": "rang/3.1.0",

    "CTRE/2.0@ctre/stable": "ctre/2.8.2",
    "CTRE/2.1@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.2@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.3@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.4@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.5@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.5.1@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.6@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.6.1@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.6.2@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.6.3@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.6.4@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.7@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.8@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.8.1@ctre/stable": "ctre/2.8.2",
    "CTRE/v2.8.2@ctre/stable": "ctre/2.8.2",

    "mpc/1.1.0@bincrafters/stable": "mpc/1.1.0",

    "apache-apr/1.5.2@jgsogo/stable": "apr/1.7.0",
    "apache-apr/1.6.3@jgsogo/stable": "apr/1.7.0",

    "variant/1.3.0@bincrafters/stable": "mpark-variant/1.4.0",

    "libxslt/1.1.33@bincrafters/stable": "libxslt/1.3.34",

    "automake/1.16.1": "automake/1.16.2",

    "wt/4.0.3@bincrafters/stable": "wt/4.3.1",
    "wt/4.0.4@bincrafters/stable": "wt/4.3.1",

    "mpdecimal/2.4.2@bincrafters/stable": "mpdecimal/2.4.2",

    "winflexbison/2.5.15@bincrafters/stable": "winflexbison/2.5.22",
    "winflexbison/2.5.16@bincrafters/stable": "winflexbison/2.5.22",
    "winflexbison/2.5.17@bincrafters/stable": "winflexbison/2.5.22",
    "winflexbison/2.5.18@bincrafters/stable": "winflexbison/2.5.22",
    "winflexbison/2.5.20@bincrafters/stable": "winflexbison/2.5.22",
    "winflexbison/2.5.21@bincrafters/stable": "winflexbison/2.5.22",

    "restinio/0.6.0.1@inexorgame/testing": "restinio/0.6.8",
    "restinio/0.4.8@bincrafters/stable": "restinio/0.6.8",
    "restinio/0.4.8.5@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.4.8.6@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.4.9@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.4.9.1@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.5.0@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.5.1@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.5.1.1@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.0@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.0.1@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.1@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.1.1@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.2@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.3@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.3.1@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.4@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.5@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.6@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.7@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.7.1@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.8@stiffstream/stable": "restinio/0.6.8",
    "restinio/0.6.8.1@stiffstream/stable": "restinio/0.6.8.1",
    "restinio/0.6.9@stiffstream/stable": "restinio/0.6.9",
    "restinio/0.6.10@stiffstream/stable": "restinio/0.6.10",
    "restinio/0.6.8": "restinio/0.6.8.1",
    "restinio/0.6.8.1": "restinio/0.6.9",
    "restinio/0.6.9": "restinio/0.6.10",

    "ncurses/6.1@conan/stable": "ncurses/6.2",

    # Note that this might produce that flex is added two times (which should be harmless)
    "flex/2.6.4@bincrafters/stable": "flex/2.6.4",
    "flex_installer/2.6.4@bincrafters/stable": "flex/2.6.4",

    "kainjow-mustache/3.2.1@bincrafters/stable": "kainjow-mustache/4.1",

    "gdbm/1.18.1@bincrafters/stable": "gdbm/1.18.1",

    "libselinux/2.8@bincrafters/stable": "libselinux/2.9",
    "libselinux/2.9@bincrafters/stable": "libselinux/2.9",

    "fontconfig/2.13.91@bincrafters/stable": "fontconfig/2.13.91",
    "fontconfig/2.13.1@bincrafters/stable": "fontconfig/2.13.91",

    "gsoap/2.8.91@bincrafters/stable": "gsoap/2.8.103",
    "gsoap/2.8.94@bincrafters/stable": "gsoap/2.8.103",
    "gsoap/2.8.100@bincrafters/stable": "gsoap/2.8.103",
    "gsoap/2.8.101@bincrafters/stable": "gsoap/2.8.103",

    # Note that this might produce that thrift is added two times (which should be harmless)
    "thrift/0.12.0@bincrafters/stable": "thrift/0.13.0",
    "thrift/0.13.0@bincrafters/stable": "thrift/0.13.0",
    "thrift_installer/0.12.0@bincrafters/stable": "thrift/0.13.0",
    "thrift_installer/0.13.0@bincrafters/stable": "thrift/0.13.0",

    "doxygen_installer/1.8.13@bincrafters/stable": "doxygen/1.8.17",
    "doxygen_installer/1.8.15@bincrafters/stable": "doxygen/1.8.17",
    "doxygen_installer/1.8.16@bincrafters/stable": "doxygen/1.8.17",
    "doxygen_installer/1.8.17@bincrafters/stable": "doxygen/1.8.17",
    "doxygen/1.8.13@inexorgame/stable": "doxygen/1.8.17",
    "doxygen/1.8.14@inexorgame/stable": "doxygen/1.8.17",
    "doxygen/1.8.17": "doxygen/1.8.18",

    "pugixml/1.8.1@bincrafters/stable": "pugixml/1.10",
    "pugixml/1.9@bincrafters/stable": "pugixml/1.10",
    "pugixml/1.10@bincrafters/stable": "pugixml/1.10",

    "opengl/virtual@bincrafters/stable": "opengl/system",

    "box2d/2.3.1@conan/stable": "box2d/2.3.1",

    "khronos-opencl-headers/20190412@bincrafters/stable": "opencl-headers/2020.03.13",
    "khronos-opencl-headers/20190502@bincrafters/stable": "opencl-headers/2020.03.13",
    "khronos-opencl-headers/20190806@bincrafters/stable": "opencl-headers/2020.03.13",

    "swig_installer/4.0.0@bincrafters/stable": "swig/4.0.1",
    "swig_installer/4.0.1@bincrafters/stable": "swig/4.0.1",

    "tsl-robin-map/0.6.1@tessil/stable": "tsl-robin-map/0.6.3",
    "tsl-robin-map/0.6.2@tessil/stable": "tsl-robin-map/0.6.3",
    "tsl-robin-map/0.6.3@tessil/stable": "tsl-robin-map/0.6.3",

    "boost-di/1.1.0@inexorgame/stable": "di/1.1.0",

    "magic_enum/0.6.3@neargye/stable": "magic_enum/0.6.6",
    "magic_enum/0.6.5": "magic_enum/0.6.6",

    "ragel_installer/6.10@bincrafters/stable": "ragel/6.10",

    "glfw/3.2.1@bincrafters/stable": "glfw/3.3.2",
    "glfw/3.2.1.20180327@bincrafters/stable": "glfw/3.3.2",
    "glfw/3.3@bincrafters/stable": "glfw/3.3.2",
    "glfw/3.3.1@bincrafters/stable": "glfw/3.3.2",
    "glfw/3.3.2@bincrafters/stable": "glfw/3.3.2",

    "glib/2.56.1@bincrafters/stable": "glib/2.64.0@bincrafters/stable",
    "glib/2.57.1@bincrafters/stable": "glib/2.64.0@bincrafters/stable",
    "glib/2.58.3@bincrafters/stable": "glib/2.64.0@bincrafters/stable",
    "glib/2.63.3@bincrafters/stable": "glib/2.64.0@bincrafters/stable",
    "glib/2.63.6@bincrafters/stable": "glib/2.64.0@bincrafters/stable",
    "glib/2.56.1@bincrafters/stable": "glib/2.65.0",
    "glib/2.57.1@bincrafters/stable": "glib/2.65.0",
    "glib/2.58.3@bincrafters/stable": "glib/2.65.0",
    "glib/2.63.3@bincrafters/stable": "glib/2.65.0",
    "glib/2.63.6@bincrafters/stable": "glib/2.65.0",
    "glib/2.64.0@bincrafters/stable": "glib/2.65.0",
    "glib/2.65.0": "glib/2.65.1",

    "cpp-taskflow/2.2.0": "taskflow/2.2.0",
    "cpp-taskflow/2.4.0": "taskflow/2.4.0",

    "parallelstl/20181004@conan/stable": "onedpl/20200330",

    "greatest/1.3.1@bincrafters/stable": "greatest/1.4.2",
    "greatest/1.4.0@bincrafters/stable": "greatest/1.4.2",

    "fribidi/1.0.5@bincrafters/stable": "fribidi/1.0.9",

    "harfbuzz/2.3.0@bincrafters/stable": "harfbuzz/2.6.8",
    "harfbuzz/2.4.0@bincrafters/stable": "harfbuzz/2.6.8",
    "harfbuzz/2.6.1@bincrafters/stable": "harfbuzz/2.6.8",
    "harfbuzz/2.6.2@bincrafters/stable": "harfbuzz/2.6.8",
    "harfbuzz/2.6.4@bincrafters/stable": "harfbuzz/2.6.8",
    "harfbuzz/2.6.7@bincrafters/stable": "harfbuzz/2.6.8",

    "libepoxy/1.5.4@bincrafters/stable": "libepoxy/1.5.4",

    "cxxopts/v2.1.2@inexorgame/stable": "cxxopts/2.2.0",

    # TODO: https://github.com/conan-io/conan-center-index/pull/2498#pullrequestreview-468672977
    # "cunit/2.1-3@bincrafters/stable": "cunit/2.1.3",

    "xkbcommon/0.8.2@bincrafters/stable": "xkbcommon/0.10.0",
    "xkbcommon/0.8.3@bincrafters/stable": "xkbcommon/0.10.0",
    "xkbcommon/0.8.4@bincrafters/stable": "xkbcommon/0.10.0",
    "xkbcommon/0.9.1@bincrafters/stable": "xkbcommon/0.10.0",
    "xkbcommon/0.10.0@bincrafters/stable": "xkbcommon/0.10.0",

    "libyaml/0.2.2@bincrafters/stable": "libyaml/0.2.5",

    "cli11/1.3.0@bincrafters/stable": "cli11/1.9.1",
    "cli11/1.4.0@bincrafters/stable": "cli11/1.9.1",
    "cli11/1.5.3@bincrafters/stable": "cli11/1.9.1",
    "cli11/1.6.0@bincrafters/stable": "cli11/1.9.1",
    "cli11/1.6.1@bincrafters/stable": "cli11/1.9.1",
    "CLI11/1.4.0@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.5.0@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.5.1@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.5.2@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.5.3@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.5.4@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.6.0@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.6.1@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.6.2@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.7.0@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.7.1@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.8.0@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.9.0@cliutils/stable": "cli11/1.9.1",
    "CLI11/1.9.1@cliutils/stable": "cli11/1.9.1",

    "glew/2.1.0@bincrafters/stable": "glew/2.1.0",

    "libuvc/0.0.6@bincrafters/stable": "libuvc/0.0.6",

    "benchmark/1.5.0": "benchmark/1.5.1",
}


def update_c_recipe_references(main, conanfile):
    """ This update script updates Conan references, mostly

    :param file: Conan file path
    """

    if not os.path.isfile(conanfile):
        return False

    files = [conanfile,]

    test_package = os.path.join(os.path.dirname(conanfile), "test_package", "conanfile.py")
    if os.path.isfile(test_package):
        files.append(test_package)

    buildpy = os.path.join(os.path.dirname(conanfile), "build.py")
    if os.path.isfile(buildpy):
        files.append(buildpy)

    references_updated = False

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
        "meson_installer": "meson",
        "nghttp2": "libnghttp2",
        "cccl_installer": "cccl",
        "ENet": "enet",
        "http-parser": "http_parser",
        "mbedtls": "mbedtls-apache",
        "docopt": "docopt.cpp",
        "jsonformoderncpp": "nlohmann_json",
        "7z_installer": "7zip",
        "IrrXML": "irrxml",
        "TBB": "tbb",
        "dirent-win32": "dirent",
        "jom_installer": "jom",
        "premake_installer": "premake",
        "cmake_installer": "cmake",
        "zmq": "zeromq",
        "paho-c": "paho-mqtt-c",
        "paho-cpp": "paho-mqtt-cpp",
        "tuple": "taocpp-tuple",
        "pegtl": "taocpp-pegtl",
        "operators": "taocpp-operators",
        "sequences": "taocpp-sequences",
        "gettext": "libgettext",
        "gettext_installer": "gettext",
        "getopt": "getopt-for-visual-studio",
        "gperf_installer": "gperf",
        "pthread-win32": "pthreads4w",
        "m4_installer": "m4",
        "bison_installer": "bison",
        "CTRE": "ctre",
        "apache-apr": "apr",
        "variant": "mpark-variant",
        "RapidJSON": "rapidjson",
        "thrift_installer": "thrift",
        "khronos-opencl-headers": "opencl-headers",
        "swig_installer": "swig",
        "boost-di": "di",
        "ragel_installer": "ragel",
        "protoc_installer": "protobuf",
        "cpp-taskflow": "taskflow",
        "parallelstl": "onedpl",
        "depot_tools_installer": "depot_tools",
        "CLI11": "cli11",
    }

    for old_name, new_name in reference_names.items():
        update_cases = {
            "self.deps_cpp_info['{}']".format(old_name): "self.deps_cpp_info['{}']".format(new_name),
            'self.deps_cpp_info["{}"]'.format(old_name): 'self.deps_cpp_info["{}"]'.format(new_name),
            "self.options['{}']".format(old_name): "self.options['{}']".format(new_name),
            'self.options["{}"]'.format(old_name): 'self.options["{}"]'.format(new_name),
        }
        for old_ref, new_ref in update_cases.items():
            for file in files:
                if main.replace_in_file(file, old_ref, new_ref):
                    msg = "Update reference from {} to {}".format(old_ref, new_ref)
                    main.output_result_update(title=msg)
                    references_updated = True

    for old_ref, new_ref in REFERENCES.items():
        for file in files:
            if main.replace_in_file(file, old_ref, new_ref):
                msg = "Update Conan recipe reference from {} to {}".format(old_ref, new_ref)
                main.output_result_update(title=msg)
                references_updated = True

    if references_updated:
        return True

    return False

