from conans import python_requires, ConanFile
import os


cpython_version = "3.7.1"
cpython_base = python_requires("cpython_base/{}@maarten/testing".format(cpython_version))

assert cpython_version == cpython_base.CPythonBaseConan.version


class CPythonInstallerConan(cpython_base.CPythonBaseConan):
    name = "cpython_installer"
    version = cpython_version
    description = "The Python programming language"
    topics = ("conan", "python", "programming", "language", "scripting")
    url = "https://github.com/bincrafters/conan-cpython_installer"
    homepage = "https://www.python.org"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "PSF"
    settings = "os_build", "arch_build"
    options = cpython_base.CPythonBaseConan.base_options
    default_options = cpython_base.CPythonBaseConan.base_default_options
    cpython_base_fail_on_error = True

    def config_options(self):
        for option in self.options.fields:
            setattr(self.options, option, False)
        self.options.optimizations = False  # True  # FIXME: Enable when finished?
        self.options.ctypes = True
        self.options.decimal = True

    def build_requirements(self):
        for base_requirement in self.base_requirements:
            self.build_requires(base_requirement)
        self.base_options_requirements(self.build_requires)

    def source(self):
        self.base_source()

    def build(self):
        if self.settings.os_build in ("Linux", "Macos"):
            self.build_autotools()
            self.package_autotools()
        else:
            self.build_msvc()

    def package(self):
        if self.settings.os_build in ("Linux", "Macos"):
            pass
        else:
            self.package_msvc()
        self.copy("LICENSE", src=os.path.join(self.source_folder, self._source_subfolder), dst="licenses")

    def package_info(self):
        self.cpp_info.libs = []
        self.cpp_info.bindirs = []
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
