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
    signtool = get_signtool_path(arch) if signtool_path is None else signtool_path
    if signtool is None:
        raise Exception("signtool.exe not found!")
    #
    cmd = [
        signtool,
        "sign",
        "/a",
        "/fd", digest_algorithm,
    ]
    if not timestamp_server is None:
        cmd += ["/t", '"' + timestamp_server + '"']
    cmd += [
        "/v",
        file
    ]
    return " ".join(cmd)
