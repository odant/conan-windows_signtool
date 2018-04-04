# Module for find signtool.exe and generate sign command
# Dmitriy Vetutnev, Odant, 2018


import unittest
import sys
if sys.version.startswith("2"):
    import mock as mock
else:
    import unittest.mock as mock


import os
import platform
import windows_signtool


class Test_get_signtool_path__arch(unittest.TestCase):

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool._sdk10x_bin_path")
    @mock.patch("windows_signtool._sdk8x_bin_path")
    def test_x86(self, mock_sdk8x_bin_path, mock_sdk10x_bin_path, mock_exists):
        mock_sdk8x_bin_path.return_value = []
        mock_sdk10x_bin_path.return_value = [r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"]
        mock_exists.return_value = True
        #
        result = windows_signtool.get_signtool_path("x86")
        #
        normal_result = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x86/signtool.exe"
        self.assertEqual(result, normal_result)
        mock_exists.assert_called_with(normal_result)

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool._sdk10x_bin_path")
    @mock.patch("windows_signtool._sdk8x_bin_path")
    def test_x86_64(self, mock_sdk8x_bin_path, mock_sdk10x_bin_path, mock_exists):
        mock_sdk8x_bin_path.return_value = []
        mock_sdk10x_bin_path.return_value = [r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"]
        mock_exists.return_value = True
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        normal_result = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x64/signtool.exe"
        self.assertEqual(result, normal_result)
        mock_exists.assert_called_with(normal_result)

    @mock.patch("platform.architecture")
    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool._sdk10x_bin_path")
    @mock.patch("windows_signtool._sdk8x_bin_path")
    def test_None_32bit(self, mock_sdk8x_bin_path, mock_sdk10x_bin_path, mock_exists, mock_architecture):
        mock_sdk8x_bin_path.return_value = []
        mock_sdk10x_bin_path.return_value = [r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"]
        mock_exists.return_value = True
        mock_architecture.return_value = ("32bit", "WindowsPE")
        #
        result = windows_signtool.get_signtool_path()
        #
        normal_result = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x86/signtool.exe"
        self.assertEqual(result, normal_result)
        mock_exists.assert_called_with(normal_result)

    @mock.patch("platform.architecture")
    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool._sdk10x_bin_path")
    @mock.patch("windows_signtool._sdk8x_bin_path")
    def test_None_64bit(self, mock_sdk8x_bin_path, mock_sdk10x_bin_path, mock_exists, mock_architecture):
        mock_sdk8x_bin_path.return_value = []
        mock_sdk10x_bin_path.return_value = [r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"]
        mock_exists.return_value = True
        mock_architecture.return_value = ("64bit", "WindowsPE")
        #
        result = windows_signtool.get_signtool_path()
        #
        normal_result = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x64/signtool.exe"
        self.assertEqual(result, normal_result)
        mock_exists.assert_called_with(normal_result)

class Test_get_signtool_path__order(unittest.TestCase):

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool._sdk10x_bin_path")
    @mock.patch("windows_signtool._sdk8x_bin_path")
    def test_last_sdk10x(self, mock_sdk8x_bin_path, mock_sdk10x_bin_path, mock_exists):
        mock_sdk8x_bin_path.return_value = [
            r"C:\Program Files (x86)\Windows Kits\8.0\bin",
            r"C:\Program Files (x86)\Windows Kits\8.1\bin"
        ]
        mock_sdk10x_bin_path.return_value = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.15063.0",
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"
        ]
        mock_exists.return_value = True
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        normal_result = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x64/signtool.exe"
        self.assertEqual(result, normal_result)

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool._sdk10x_bin_path")
    @mock.patch("windows_signtool._sdk8x_bin_path")
    def test_prelast_sdk10x(self, mock_sdk8x_bin_path, mock_sdk10x_bin_path, mock_exists):
        mock_sdk8x_bin_path.return_value = [
            r"C:\Program Files (x86)\Windows Kits\8.0\bin",
            r"C:\Program Files (x86)\Windows Kits\8.1\bin"
        ]
        mock_sdk10x_bin_path.return_value = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.15063.0",
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"
        ]
        mock_exists.side_effect = [False, True]
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        normal_result = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.15063.0/x64/signtool.exe"
        self.assertEqual(result, normal_result)
        

if __name__ == "__main__":
    unittest.main()
