# Module for find signtool.exe and generate sign command
# Dmitriy Vetutnev, Odant, 2018


import unittest
import platform


import windows_signtool


class Test_get_sdk8x_bin_paths(unittest.TestCase):

    @unittest.skipIf(platform.system() != "Windows", "only Windows support")
    def test_sdk_80(self):
        print("\nSDK 8.0 path:\n%s" % windows_signtool.get_sdk8x_bin_paths(reg_keys=["KitsRoot"])[0])

    @unittest.skipIf(platform.system() != "Windows", "only Windows support")
    def test_sdk_81(self):
        print("\nSDK 8.1 path:\n%s" % windows_signtool.get_sdk8x_bin_paths(reg_keys=["KitsRoot81"])[0])

    @unittest.skipIf(platform.system() != "Windows", "only Windows support")
    def test_sdk_all(self):
        print("\nAll SDK paths:")
        for p in windows_signtool.get_sdk8x_bin_paths():
            print(p)

    @unittest.skipIf(platform.system() != "Windows", "only Windows support")
    def test_skip_bad_key(self):
        print("\nSDK paths (skip bad key):")
        for p in windows_signtool.get_sdk8x_bin_paths(reg_keys=["KitsRoot", "bad_key", "KitsRoot81"]):
            print(p)


if __name__ == "__main__":
    unittest.main()