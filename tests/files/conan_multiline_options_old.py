#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class DoubleConversionConan(ConanFile):
    name = "double-conversion"
    version = "3.0.0"
    url = "https://github.com/bincrafters/conan-double-conversion"
    homepage = "https://github.com/google/double-conversion"
    author = "Bincrafters <bincraters@gmail.com>"
    description = "Efficient binary-decimal and decimal-binary conversion routines for IEEE doubles."
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = ("shared=False",
     "fPIC=True")
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"


    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           float(self.settings.compiler.version.value) < 14:
           raise Exception("Double Convertion could not be built by MSVC <14")

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.cppflags = ["-pthread"]
