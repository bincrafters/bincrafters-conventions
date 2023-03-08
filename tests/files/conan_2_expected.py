from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conans import CMake, tools
import os


class GrpcConan(ConanFile):
    name = "grpc"
    version = "1.23.0"
    description = "Google's RPC library and framework."
    topics = ("conan", "grpc", "rpc")
    url = "https://github.com/bincrafters/conan-grpc"
    homepage = "https://github.com/grpc/grpc"
    license = "Apache-2.0"
    exports = ["something.cmake"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    short_paths = True  # Otherwise some folders go out of the 260 chars path length scope rapidly (on windows)

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "fPIC": [True, False],
        "build_codegen": [True, False],
        "build_csharp_ext": [True, False]
    }
    default_options = {
        "fPIC": True,
        "build_codegen": True,
        "build_csharp_ext": False
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "zlib/1.2.13",
        "openssl/1.0.2u",
        "protobuf/3.9.1",
        "c-ares/1.15.0"
    )

    def requirements(self):
        self.options["openssl"].shared = False

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            del self.options.fPIC
            compiler_version = int(str(self.settings.compiler.version))
            if compiler_version < 14:
                raise ConanInvalidConfiguration("gRPC can only be built with Visual Studio 2015 or higher.")

    def source(self):
        sha256 = "86d7552cb79ab9ba7243d86b768952df1907bacb828f5f53b8a740f716f3937b"
        tools.get("{}/archive/v{}.zip".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

        cmake_path = os.path.join(self._source_subfolder, "CMakeLists.txt")

        tools.replace_in_file(cmake_path, "_gRPC_PROTOBUF_LIBRARIES", "CONAN_LIBS_PROTOBUF")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        dummy = self.deps_cpp_info["openssl"].include_paths[0]
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        self.copy(pattern="LICENSE", dst="licenses")
        self.copy('*', dst='include', src='{}/include'.format(self._source_subfolder))
        self.copy('*.cmake', dst='lib', src='{}/lib'.format(self._build_subfolder), keep_path=True)
        self.copy("*.lib", dst="lib", src="", keep_path=False)
        self.copy("*.a", dst="lib", src="", keep_path=False)
        self.copy("*", dst="bin", src="bin")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.cpp_info.libs = [
            "grpc++",
            "grpc",
            "grpc++_unsecure",
            "grpc_unsecure",
            "gpr",
            "address_sorting"
        ]
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs += ["wsock32", "ws2_32"]
