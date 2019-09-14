import os, stat
from conans import ConanFile
from conans.client import tools
from conans.errors import ConanInvalidConfiguration

class AppImageToolConan(ConanFile):
    name = "appimagetool"
    # Conan: Valid names must contain at least 2 characters.
    version = "v12"
    license = "MIT"
    url = "https://github.com/altairwei/conan-appimagetool.git"
    homepage = "https://github.com/AppImage/AppImageKit"
    settings = "os_build", "arch_build"
    build_policy = "missing"
    description = '''Package desktop applications as AppImages that run on
 common Linux-based operating systems, such as RHEL, CentOS, openSUSE,
 SLED, Ubuntu, Fedora, debian and derivatives.'''

    def configure(self):
        if self.settings.os_build != "Linux":
            raise ConanInvalidConfiguration("Only Linux supported for appimagetool")
        if self.settings.arch_build not in ["x86_64", "x86"]:
            raise ConanInvalidConfiguration("Only x86_64 supported for appimagetool")

    def build(self):
        if self.settings.arch_build == "x86":
            arch = "i686"
        elif self.settings.arch_build == "x86_64":
            arch = "x86_64"
        appimage_name = "appimagetool-%s.AppImage" % arch
        url = "https://github.com/AppImage/AppImageKit/releases/download/%s/%s" % (self.version[1:], appimage_name)
        self.output.warn("Downloading %s: %s" % (appimage_name, url))
        tools.download(url, "appimagetool")
        # Add execute permission
        st = os.stat('appimagetool')
        os.chmod("appimagetool", st.st_mode | stat.S_IEXEC)

    def package(self):
        self.copy("appimagetool", dst="bin", keep_path=False)

    def package_info(self):
        self.output.info("Using appimagetool" % self.version[1])
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))