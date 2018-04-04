# Module for find signtool.exe and generate sign command
# Dmitriy Vetutnev, Odant, 2018


import platform
import os


# Find signtool.exe

def _sdk8x_bin_path():
    pass


def _sdk10x_bin_path():
    pass


def get_signtool_path(arch=None):
    if arch is None:
        arch = platform.architecture()[0]
    ms_arch = {
            "x86": "x86",
            "32bit": "x86",
            "x86_64": "x64",
            "64bit": "x64"
        }.get(str(arch))
    #
    paths = []
    paths += _sdk8x_bin_path()
    paths += _sdk10x_bin_path()
    paths.reverse()
    for p in paths:
        signtool_path = os.path.join(p, ms_arch, "signtool.exe")
        res = signtool_path.replace("\\", "/")
        if os.path.exists(res):
            return res
    return None


# Generate command line

def _sha1(timestamp_server):
    res = ["/fd", "sha1"]
    if not timestamp_server is None:
        res += ["/t", '"' + timestamp_server + '"']
    return res


def _sha256(timestamp_server):
    res = ["/fd", "sha256"]
    if not timestamp_server is None:
        res += ["/tr", '"' + timestamp_server + '"']
    res += ["/td", "sha256"]
    return res
    
    
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
        "/as"
    ]
    #
    if digest_algorithm == "sha1":
        cmd += _sha1(timestamp_server)
    elif digest_algorithm == "sha256":
        cmd += _sha256(timestamp_server)
    else:
        raise Exception("Invalid digest algorithm!")
    #
    cmd += [
        "/v",
        file
    ]
    return " ".join(cmd)
