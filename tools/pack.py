"""Buat arsip kit dengan path relatif, LF untuk berkas teks, dan mode berkas Linux."""
from pathlib import Path
import io
import tarfile

TEXT_EXTENSIONS = {
    ".sh", ".py", ".txt", ".service", ".desktop", ".html", ".css",
    ".svg", ".json", ".yaml", ".yml", ".md", ".tsv", ".conf", ".theme",
    ".policy", ".rules", ".xml"
}
TEXT_FILENAMES = {
    "20-labkita", "labkita-check", "labkita-postinstall", "labkita-guide",
    "packages.txt", "LICENSE", "CREDITS.md"
}

root = Path(__file__).resolve().parents[1]
output = root / "dist" / "labkita-kit.tar.gz"
output.parent.mkdir(exist_ok=True)

with tarfile.open(output, "w:gz") as archive:
    for folder in ("config", "scripts", "payload"):
        folder_path = root / folder
        if not folder_path.is_dir():
            continue
        for source in sorted(folder_path.rglob("*")):
            if not source.is_file() or "__pycache__" in source.parts:
                continue
            raw_bytes = source.read_bytes()
            if source.suffix.lower() in TEXT_EXTENSIONS or source.name in TEXT_FILENAMES:
                content = raw_bytes.replace(b"\r\n", b"\n")
            else:
                content = raw_bytes

            item = tarfile.TarInfo("labkita-linux/" + source.relative_to(root).as_posix())
            item.size = len(content)
            is_exec = source.suffix == ".sh" or source.parent.name in ("bin", "sbin") or source.name in ("labkita-check", "labkita-postinstall", "labkita-guide")
            item.mode = 0o755 if is_exec else 0o644
            item.uid = item.gid = 0
            item.mtime = 0
            archive.addfile(item, io.BytesIO(content))

print(f"Kit built: {output} ({output.stat().st_size} bytes)")
