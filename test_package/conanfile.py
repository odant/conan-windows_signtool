from conans import ConanFile


class TestPackage(ConanFile):

    def test(self):
        import windows_signtool
        #
        signtool = windows_signtool.get_signtool_path()
        self.run("%s /?" % signtool)
        #
        cmd = windows_signtool.get_sign_command("C:/project/main.exe", digest_algorithm="sha1")
        self.output.info("SHA1 cmd: %s" % cmd)
        #
        cmd = windows_signtool.get_sign_command("C:/project/main.exe", digest_algorithm="sha256")
        self.output.info("SHA256 cmd: %s" % cmd)
