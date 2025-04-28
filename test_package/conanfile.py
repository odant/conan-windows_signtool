from conan import ConanFile
from conan.tools.env import VirtualRunEnv, Environment
from conan import tools
import os

class TestPackage(ConanFile):
    python_requires = "tested_reference_str"

    def test(self):
        signtool = self.python_requires["windows_signtool"].module.WindowsSigntool()
        signtool_path = signtool.get_signtool_path()
        self.output.info(f"signtool_path: {signtool_path}")
        self.run("%s /?" % signtool_path)
        #
        cmd = signtool.get_sign_command("C:/project/main.exe", digest_algorithm="sha1")
        self.output.info("SHA1 cmd: %s" % cmd)
        #
        cmd = signtool.get_sign_command("C:/project/main.exe", digest_algorithm="sha256")
        self.output.info("SHA256 cmd: %s" % cmd)
