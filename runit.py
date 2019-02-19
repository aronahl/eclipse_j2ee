#!/usr/bin/python3
import subprocess
import sys
import os.path
import os
import time

if __name__ == "__main__":
    if os.path.exists('/tmp/.X10-lock'):
        os.unlink('/tmp/.X10-lock')
    if os.path.exists("/tmp/:10.log"):
        os.unlink("/tmp/:10.log")
    http = int(os.getenv("HTTP", "0"))
    xpraArgs = [
        "xpra",
        "--bind-tcp=0.0.0.0:9999",
        "--dpi=%s" % os.getenv("DPI", "92"),
        "start",
        ":10"]
    if http:
        xpraArgs.insert(1, "--html=on")
    subprocess.check_call(args=xpraArgs)
    logFound = False
    for _ in range(30):
        if os.path.exists("/tmp/:10.log"):
            logFound = True
            break
        time.sleep(1)
    if not logFound:
        print("Startup failed without a log file")
        sys.exit(1)
    tailProc = subprocess.Popen(args=("tail", "-f", "/tmp/:10.log"))
    eclipseArgs=["/opt/eclipse/eclipse", "-data", "/opt/workspace" ] + sys.argv[1:]
    while not os.path.exists('/tmp/:10.log'):
        print('Waiting on log file.')
        time.sleep(1)
    #waiting for the connection before starting eclipse prevents odd DPI issues.
    offset = 0
    while True:
        with open('/tmp/:10.log', 'r') as f:
            print('Waiting on TCP Connection.')
            buff = f.read()
            if "New tcp connection" in buff:
                break
            print(buff[offset:])
            offset=len(buff)
            time.sleep(1)
    eclipseEnv = dict(os.environ)
    eclipseEnv["DISPLAY"] = ":10"
    eclipseProc = subprocess.Popen(args=eclipseArgs, env=eclipseEnv)
    eclipseProc.wait()
    tailProc.kill()
