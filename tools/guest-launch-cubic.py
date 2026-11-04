"""Buka Cubic sebagai builder pada sesi desktop VM build."""
import os
from pathlib import Path
import subprocess
import sys

if os.getuid() == 0 or not Path('/var/lib/labkita-build-vm-ready').exists():
    raise SystemExit('Jalankan sebagai builder di VM build proyek.')
if not os.path.ismount('/mnt/labkita-input'):
    subprocess.run(['sudo', '-n', 'mkdir', '-p', '/mnt/labkita-input'], check=True)
    subprocess.run(['sudo', '-n', 'vmhgfs-fuse', '.host:/LabKitaInput', '/mnt/labkita-input', '-o', 'ro,allow_other'], check=True)
home = Path('/home/builder')
(home / 'cubic').mkdir(exist_ok=True)
pid = subprocess.check_output(['pgrep', '-u', str(os.getuid()), '-x', 'gnome-shell'], text=True).splitlines()[0]
environment = dict(os.environ)
for entry in Path(f'/proc/{pid}/environ').read_bytes().split(b'\0'):
    if b'=' in entry:
        key, value = entry.split(b'=', 1)
        environment[key.decode()] = value.decode(errors='surrogateescape')
environment['XDG_RUNTIME_DIR'] = f'/run/user/{os.getuid()}'
environment['DBUS_SESSION_BUS_ADDRESS'] = f'unix:path=/run/user/{os.getuid()}/bus'
session_environment = subprocess.check_output(['systemctl', '--user', 'show-environment'], env=environment, text=True)
for line in session_environment.splitlines():
    if '=' in line:
        key, value = line.split('=', 1)
        environment[key] = value
environment['GDK_BACKEND'] = 'x11'
if not environment.get('DISPLAY'):
    raise SystemExit('DISPLAY sesi desktop belum tersedia; tunggu login desktop selesai.')
log = (home / 'cubic-launch.log').open('a')
if len(sys.argv) > 1 and sys.argv[1] == 'run-cubic':
    subprocess.Popen(['cubic'] + sys.argv[2:], env=environment, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
elif len(sys.argv) > 1:
    raise SystemExit(subprocess.run(sys.argv[1:], env=environment, stdout=log, stderr=subprocess.STDOUT).returncode)
else:
    subprocess.Popen(['cubic'], env=environment, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


