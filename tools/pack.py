"""Buat arsip kit dengan path relatif, LF, dan mode berkas Linux."""
from pathlib import Path
import io
import tarfile

root = Path(__file__).resolve().parents[1]
output = root / "dist" / "labkita-kit.tar.gz"
output.parent.mkdir(exist_ok=True)
with tarfile.open(output, "w:gz") as archive:
    for folder in ("config", "scripts", "payload"):
        for source in sorted((root / folder).rglob("*")):
            if not source.is_file() or "__pycache__" in source.parts:
                continue
            content = source.read_bytes().replace(b"\r\n", b"\n")
            item = tarfile.TarInfo("labkita-linux/" + source.relative_to(root).as_posix())
            item.size = len(content)
            item.mode = 0o755 if source.suffix == ".sh" or source.parent.name in ("bin", "sbin") else 0o644
            item.uid = item.gid = 0
            item.mtime = 0
            archive.addfile(item, io.BytesIO(content))
print(output)
