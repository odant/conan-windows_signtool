# Module for find signtool.exe and generate sign command
# Dmitriy Vetutnev, Odant, 2018


def get_signtool_path(arch=None):
    pass


def get_sign_command(
        file,
        digest_algorithm="sha1",
        timestamp_server="http://timestamp.verisign.com/scripts/timestamp.dll",
        signtool_path=None,
        arch=None):
    #
    get_signtool_path(arch)
