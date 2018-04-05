# Module for find signtool.exe and generate sign command
# Dmitriy Vetutnev, Odant, 2018


import unittest
import sys
# Support Python 2.x and 3.x
if sys.version.startswith("2"):
    import mock as mock
else:
    import unittest.mock as mock


import os
import platform
import windows_signtool


class Test_get_signtool_path__arch(unittest.TestCase):

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_x86(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists):
        mock_get_sdk8x_bin_paths.return_value = []
        mock_get_sdk10x_bin_paths.return_value = [r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"]
        mock_exists.return_value = True
        #
        result = windows_signtool.get_signtool_path("x86")
        #
        normal_path = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x86/signtool.exe"
        self.assertEqual(result, "\"" + normal_path + "\"")
        mock_exists.assert_called_with(normal_path)

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_x86_64(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists):
        mock_get_sdk8x_bin_paths.return_value = []
        mock_get_sdk10x_bin_paths.return_value = [r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"]
        mock_exists.return_value = True
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        normal_path = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x64/signtool.exe"
        self.assertEqual(result, "\"" + normal_path + "\"")
        mock_exists.assert_called_with(normal_path)

    @mock.patch("platform.architecture")
    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_None_32bit(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists, mock_architecture):
        mock_get_sdk8x_bin_paths.return_value = []
        mock_get_sdk10x_bin_paths.return_value = [r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"]
        mock_exists.return_value = True
        mock_architecture.return_value = ("32bit", "WindowsPE")
        #
        result = windows_signtool.get_signtool_path()
        #
        normal_path = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x86/signtool.exe"
        self.assertEqual(result, "\"" + normal_path + "\"")
        mock_exists.assert_called_with(normal_path)

    @mock.patch("platform.architecture")
    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_None_64bit(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists, mock_architecture):
        mock_get_sdk8x_bin_paths.return_value = []
        mock_get_sdk10x_bin_paths.return_value = [r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"]
        mock_exists.return_value = True
        mock_architecture.return_value = ("64bit", "WindowsPE")
        #
        result = windows_signtool.get_signtool_path()
        #
        normal_path = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x64/signtool.exe"
        self.assertEqual(result, "\"" + normal_path + "\"")
        mock_exists.assert_called_with(normal_path)

class Test_get_signtool_path__order(unittest.TestCase):

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_last_sdk10x(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists):
        mock_get_sdk8x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\8.0\bin",
            r"C:\Program Files (x86)\Windows Kits\8.1\bin"
        ]
        mock_get_sdk10x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.15063.0",
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"
        ]
        mock_exists.return_value = True
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        normal_path = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/x64/signtool.exe"
        self.assertEqual(result, "\"" + normal_path + "\"")

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_prelast_sdk10x(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists):
        mock_get_sdk8x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\8.0\bin",
            r"C:\Program Files (x86)\Windows Kits\8.1\bin"
        ]
        mock_get_sdk10x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.15063.0",
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"
        ]
        mock_exists.side_effect = [False, True]
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        normal_path = "C:/Program Files (x86)/Windows Kits/10/bin/10.0.15063.0/x64/signtool.exe"
        self.assertEqual(result, "\"" + normal_path + "\"")

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_last_sdk8x(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists):
        mock_get_sdk8x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\8.0\bin",
            r"C:\Program Files (x86)\Windows Kits\8.1\bin"
        ]
        mock_get_sdk10x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.15063.0",
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"
        ]
        mock_exists.side_effect = [False, False, True]
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        normal_path = "C:/Program Files (x86)/Windows Kits/8.1/bin/x64/signtool.exe"
        self.assertEqual(result, "\"" + normal_path + "\"")

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_prelast_sdk8x(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists):
        mock_get_sdk8x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\8.0\bin",
            r"C:\Program Files (x86)\Windows Kits\8.1\bin"
        ]
        mock_get_sdk10x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.15063.0",
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"
        ]
        mock_exists.side_effect = [False, False, False, True]
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        normal_path = "C:/Program Files (x86)/Windows Kits/8.0/bin/x64/signtool.exe"
        self.assertEqual(result, "\"" + normal_path + "\"")

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_not_found_signtool(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists):
        mock_get_sdk8x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\8.0\bin",
            r"C:\Program Files (x86)\Windows Kits\8.1\bin"
        ]
        mock_get_sdk10x_bin_paths.return_value = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.15063.0",
            r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0"
        ]
        mock_exists.return_value = False
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        self.assertIsNone(result)

    @mock.patch("os.path.exists")
    @mock.patch("windows_signtool.get_sdk10x_bin_paths")
    @mock.patch("windows_signtool.get_sdk8x_bin_paths")
    def test_miss_sdk(self, mock_get_sdk8x_bin_paths, mock_get_sdk10x_bin_paths, mock_exists):
        mock_get_sdk8x_bin_paths.return_value = []
        mock_get_sdk10x_bin_paths.return_value = []
        mock_exists.return_value = False
        #
        result = windows_signtool.get_signtool_path("x86_64")
        #
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
