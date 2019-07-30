# Module for find signtool.exe and generate sign command
# Dmitriy Vetutnev, Odant, 2018


import platform
import os
if platform.system() == "Windows":
    import winreg


# Find signtool.exe

def get_sdk8x_bin_paths(reg_keys=None, reg_path="Software\\Microsoft\\Windows Kits\\Installed Roots"):
    if reg_keys is None:
        reg_keys = ["KitsRoot", "KitsRoot81"]
    ret = []
    hk = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
    for key in reg_keys:
        try:
            p = winreg.QueryValueEx(hk, key)[0]
            p = os.path.join(p, "bin")
            ret.append(p)
        except WindowsError:
            continue
    return ret


def get_sdk10x_bin_paths(reg_key="KitsRoot10", reg_path="Software\\Microsoft\\Windows Kits\\Installed Roots"):
    ret = []
    try:
        hk = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        p10 = winreg.QueryValueEx(hk, reg_key)[0]
        i = 0
        while True:
            try:
                ver = winreg.EnumKey(hk, i)
                p = os.path.join(p10, "bin", ver)
                ret.append(p)
                i += 1
            except:
                break
    except:
        pass
    return ret


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
    paths += get_sdk8x_bin_paths()
    paths += get_sdk10x_bin_paths()
    paths.reverse()
    for p in paths:
        signtool_path = os.path.join(p, ms_arch, "signtool.exe")
        res = signtool_path.replace("\\", "/")
        if os.path.exists(res):
            if res.count(" ") > 0:
                res = "\"" + res + "\""
            return res
    return None


# Generate command line

def _sha1(timestamp_server):
    res = ["/fd", "sha1"]
    if not timestamp_server is None:
        res += ["/tr", timestamp_server]
        res += ["/td", "sha1"]
    return res


def _sha256(timestamp_server):
    res = [
        "/as",
        "/fd", "sha256"
    ]
    if not timestamp_server is None:
        res += ["/tr", timestamp_server]
        res += ["/td", "sha256"]
    return res


def get_sign_command(
        file,
        digest_algorithm="sha1",
        timestamp=True,
        timestamp_server_sha1="http://sha1timestamp.ws.symantec.com/sha1/timestamp",
        timestamp_server_sha256="http://sha256timestamp.ws.symantec.com/sha256/timestamp",
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
        "/a"
    ]
    #
    if digest_algorithm == "sha1":
        ts = timestamp_server_sha1 if timestamp else None
        cmd += _sha1(ts)
    elif digest_algorithm == "sha256":
        ts = timestamp_server_sha256 if timestamp else None
        cmd += _sha256(ts)
    else:
        raise Exception("Invalid digest algorithm!")
    #
    cmd += [
        "/v",
        "/debug",
        file
    ]
    return " ".join(cmd)
