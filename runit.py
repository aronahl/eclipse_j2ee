#!/usr/bin/python3
import subprocess
import sys
import os.path
import os
import time

if __name__ == "__main__":
    if os.path.exists('/tmp/.X10-lock'):
        os.unlink('/tmp/.X10-lock')
    xpraArgs = (
        "xpra",
        "--bind-tcp=0.0.0.0:9999",
        "--dpi=%s" % os.getenv("DPI", "92"),
        "start",
        ":10")
    subprocess.check_call(args=xpraArgs)
    logFound = False
    for _ in range(30):
        if os.path.exists("/home/user/.xpra/:10.log"):
            logFound = True
            break
        time.sleep(1)
    if not logFound:
        print("Startup failed without a log file")
        sys.exit(1)
    tailProc = subprocess.Popen(args=("tail", "-f", "/home/user/.xpra/:10.log"))
    eclipseArgs=["/opt/eclipse/eclipse", "-data", "/opt/workspace" ] + sys.argv[1:]
    eclipseEnv = dict(os.environ)
    eclipseEnv["DISPLAY"] = ":10"
    eclipseProc = subprocess.Popen(args=eclipseArgs, env=eclipseEnv)
    eclipseProc.wait()
    tailProc.kill()
