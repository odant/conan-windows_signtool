from conan import ConanFile

import platform
if platform.system() == "Windows":
    import os, winreg, glob

    class WindowsSigntool:

        def get_sdk8x_bin_paths(self, reg_keys=None, reg_path="Software\\Microsoft\\Windows Kits\\Installed Roots"):
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

        def get_sdk10x_bin_paths(self, reg_key="KitsRoot10", reg_path="Software\\Microsoft\\Windows Kits\\Installed Roots"):
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

        def get_signtool_path(self, arch=None):
            if arch is None:
                arch = platform.architecture()[0]
            ms_arch = {
                    "x86": "x86",
                    "32bit": "x86",
                    "Win32": "x86",
                    "x86_64": "x64",
                    "Win64": "x64",
                    "64bit": "x64"
                }.get(str(arch))
            #
            paths = []
            paths += self.get_sdk8x_bin_paths()
            paths += self.get_sdk10x_bin_paths()
            paths.reverse()
            for p in paths:
                signtool_path = os.path.join(p, ms_arch, "signtool.exe")
                res = signtool_path.replace("\\", "/")
                if os.path.exists(res):
                    if res.count(" ") > 0:
                        res = "\"" + res + "\""
                    return res
            return None

        def _sha1(self, timestamp_server):
            res = ["/fd", "sha1"]
            if not timestamp_server is None:
                res += ["/tr", timestamp_server]
                res += ["/td", "sha1"]
            return res

        def _sha256(self, timestamp_server):
            res = [
                "/as",
                "/fd", "sha256"
            ]
            if not timestamp_server is None:
                res += ["/tr", timestamp_server]
                res += ["/td", "sha256"]
            return res

        def get_sign_command(
                self,
                file,
                digest_algorithm="sha1",
                timestamp=True,
                timestamp_server_sha1="http://timestamp.digicert.com",
                timestamp_server_sha256="http://timestamp.digicert.com",
                signtool_path=None,
                arch=None):
            #
            signtool = self.get_signtool_path(arch) if signtool_path is None else signtool_path
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
                cmd += self._sha1(ts)
            elif digest_algorithm == "sha256":
                ts = timestamp_server_sha256 if timestamp else None
                cmd += self._sha256(ts)
            else:
                raise Exception("Invalid digest algorithm!")
            #
            additional = os.environ.get("ODA_WIN_SIGNTOOL_ADDITIONAL", None)
            if additional is not None:
                cmd += [additional]
            #
            cmd += [
                "/v",
                "/debug",
                file
            ]
            return " ".join(cmd)
            
    def sign(conanfile, patterns):
        for pattern in patterns:
            signtool = WindowsSigntool()
            for fpath in glob.glob(pattern):
                fpath = fpath.replace("\\", "/")
                for alg in ["sha256"]:
                    is_timestamp = True if conanfile.settings.build_type == "Release" else False
                    cmd = signtool.get_sign_command(fpath, digest_algorithm=alg, timestamp=is_timestamp)
                    conanfile.output.info("Sign %s" % fpath)
                    conanfile.run(cmd, quiet=True, env="", scope="run")
            


class Conan_windows_signtool(ConanFile):
    name = "windows_signtool"
    version = "1.3"
    license = "MIT"
    url = "https://github.com/odant/conan-windows_signtool"
    description = "Python class for find MS signtool.exe and generate sign command"
    package_type = "python-require"
