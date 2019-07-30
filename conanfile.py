from conans import ConanFile


class Conan_windows_signtool(ConanFile):
    name = "windows_signtool"
    version = "1.1"
    license = "MIT"
    url = "https://github.com/odant/conan-windows_signtool"
    description = "Python module for find MS signtool.exe and generate sign command"
    settings = {
        "os_build": ["Windows"],
        "arch_build": ["x86", "x86_64"]
    }
    exports = "__init__.py", "windows_signtool.py"
    build_policy = "missing"
    
    def package(self):
        self.copy("*")
        
    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)
