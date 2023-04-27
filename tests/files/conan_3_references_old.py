from conans import ConanFile, CMake, tools

required_conan_version = ">=1.33.0"


class LibnameConan(ConanFile):
    name = "libname"
    description = "Keep it short"
    topics = ("libname", "logging", "debugging")
    url = "https://github.com/bincrafters/community"
    homepage = "https://github.com/original_author/original_lib"
    license = "MIT"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def requirements(self):
        # Obviously, in real conanfiles it makes no sense to have dependencies multiple times
        self.requires("zlib/1.2.8@conan/stable")
        self.requires("opengl/virtual@bincrafters/stable")
        self.requires("testtest-test/2.33.1@bincrafters/stable")
        self.requires("testtest-test/2.36")
        self.requires("testtest-test/2.36.2")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["BUILD_TESTS"] = False  # example
            self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
