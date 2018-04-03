import unittest
import mock as mock


import windows_signtool


class Test_get_sign_command__arch(unittest.TestCase):

    @mock.patch("windows_signtool.get_signtool_path")
    def test_arch_None(self, mock_get_signtool_path):
        mock_get_signtool_path.return_value = "C:/blablabla/bin/x64/signtool.exe"
        #
        windows_signtool.get_sign_command("D:/build/binary.exe")
        #
        mock_get_signtool_path.assert_called_once_with(None)

    @mock.patch("windows_signtool.get_signtool_path")
    def test_arch_x86(self, mock_get_signtool_path):
        mock_get_signtool_path.return_value = "C:/blablabla/bin/x86/signtool.exe"
        #
        windows_signtool.get_sign_command("D:/build/binary.exe", arch="x86")
        #
        mock_get_signtool_path.assert_called_once_with("x86")

    @mock.patch("windows_signtool.get_signtool_path")
    def test_arch_x86_64(self, mock_get_signtool_path):
        mock_get_signtool_path.return_value = "C:/blablabla/bin/x64/signtool.exe"
        #
        windows_signtool.get_sign_command("D:/build/binary.exe", arch="x86_64")
        #
        mock_get_signtool_path.assert_called_once_with("x86_64")


class Test_get_sign_command__path_to_signtool(unittest.TestCase):

    @mock.patch("windows_signtool.get_signtool_path")
    def test_find_signtool_path(self, mock_get_signtool_path):
        mock_get_signtool_path.return_value = "C:/blablabla/bin/x64/signtool.exe"
        #
        result = windows_signtool.get_sign_command("D:/build/binary.exe")
        #
        self.assertTrue(result.startswith("C:/blablabla/bin/x64/signtool.exe"))

    @mock.patch("windows_signtool.get_signtool_path")
    def test_custom_signtool_path(self, mock_get_signtool_path):
        mock_get_signtool_path.return_value = "C:/blablabla/bin/x64/signtool.exe"
        #
        result = windows_signtool.get_sign_command("D:/build/binary.exe", signtool_path="C:/lablabla/bin/x64/signtool.exe")
        #
        self.assertTrue(result.startswith("C:/lablabla/bin/x64/signtool.exe"))

    
if __name__ == "__main__":
    unittest.main()
