"""Guest operations VMware untuk VM LabKita yang dibuat proyek ini saja."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
vm = root / "build/vm/labkita-build.vmx"
vmrun = Path(r"C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe")
arguments = sys.argv[1:]
if not arguments:
    raise SystemExit("Pemakaian: vmctl.py status | ip | screen <png> | copy-in <host> <guest> | copy-out <guest> <host> | run <guest-program> [args...]")
action, *extra = arguments
if action == "status":
    command = [str(vmrun), "checkToolsState", str(vm)]
elif action == "ip":
    command = [str(vmrun), "getGuestIPAddress", str(vm)]
else:
    auth = json.loads((root / "build/builder.credentials.json").read_text(encoding="utf-8"))
    if os.environ.get("LABKITA_PASSWORD_CR") == "1":
        auth["password"] += "\r"
    command = [str(vmrun), "-gu", auth["username"], "-gp", auth["password"]]
    if action == "screen" and len(extra) == 1:
        command += ["captureScreen", str(vm), str(Path(extra[0]).resolve())]
    elif action == "copy-in" and len(extra) == 2:
        command += ["copyFileFromHostToGuest", str(vm), str(Path(extra[0]).resolve()), extra[1]]
    elif action == "copy-out" and len(extra) == 2:
        command += ["copyFileFromGuestToHost", str(vm), extra[0], str(Path(extra[1]).resolve())]
    elif action in ("run", "run-wait") and extra:
        command += ["runProgramInGuest", str(vm)]
        if action == "run":
            command += ["-noWait"]
        command += extra
    else:
        raise SystemExit("Argumen tidak sesuai.")
result = subprocess.run(command, capture_output=True, text=True)
print(result.stdout, end="")
if result.stderr:
    print(result.stderr, end="", file=sys.stderr)
sys.exit(result.returncode)
