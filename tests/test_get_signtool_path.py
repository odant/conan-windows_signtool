# Module for find signtool.exe and generate sign command
# Dmitriy Vetutnev, Odant, 2018


import unittest
import mock as mock


import windows_signtool


class Test_get_signtool_path(unittest.TestCase):

    @mock.patch("windows_signtool._sdk10x_bin_path")
    @mock.patch("windows_signtool._sdk8x_bin_path")
    def test_arch_None(self, mock_skd8x_bin_path, mock_sdk10x_bin_path):
        mock_skd8x_bin_path.return_value = []
        #
        windows_signtool.get_signtool_path()
        #
        mock_skd8x_bin_path.assert_called()
        

if __name__ == "__main__":
    unittest.main()
