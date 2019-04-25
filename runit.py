#!/usr/bin/python3
import subprocess
import sys
import os.path
import os
import stat
import time
import textwrap

if __name__ == "__main__":
    if os.path.exists('/tmp/.X10-lock'):
        os.unlink('/tmp/.X10-lock')
    if os.path.exists("/run/user/1000/xpra/:10.log"):
        os.unlink("/run/user/1000/xpra/:10.log")
    http = int(os.getenv("HTTP", "0"))
    xpraArgs = [
        "xpra",
        "--bind-tcp=0.0.0.0:9999",
        "--dpi=%s" % os.getenv("DPI", "92"),
        "start",
        "--start",
        "/tmp/launch.sh",
        ":10"]
    oldmask = os.umask(0o077)
    with open("/tmp/launch.sh", 'w') as f:
        f.write(textwrap.dedent("""\
                #!/bin/bash
                exec /opt/eclipse/eclipse -data /opt/workspace
        """))
    os.chmod('/tmp/launch.sh', os.stat('/tmp/launch.sh').st_mode | stat.S_IEXEC)
    os.umask(oldmask)
    if http:
        xpraArgs.insert(1, "--html=on")
    subprocess.check_call(args=("whoami"))
    subprocess.check_call(args=("grep", "user", "/etc/passwd"))
    print(xpraArgs)
    subprocess.check_call(args=xpraArgs)
    logFound = False
    for _ in range(30):
        if os.path.exists("/run/user/1000/xpra/:10.log"):
            logFound = True
            break
        time.sleep(1)
    if not logFound:
        print("Startup failed without a log file")
        sys.exit(1)
    subprocess.check_call(args=("tail", "-f", "/run/user/1000/xpra/:10.log"))
