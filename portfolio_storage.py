"""Local portfolio storage without replacing existing work."""

from pathlib import Path
import re


def save_upload(directory: Path, filename: str, data: bytes) -> Path:
    """Save a supported asset under a portable, collision-free filename."""
    name = filename.replace("\\", "/").rsplit("/", 1)[-1]
    suffix = Path(name).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".webm"}:
        raise ValueError("Unsupported file extension.")
    if not data:
        raise ValueError("The file is empty.")
    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", Path(name).stem).strip(" .")[:120]
    stem = stem or "asset"
    if stem.split(".")[0].upper() in {"CON", "PRN", "AUX", "NUL", *[f"{p}{i}" for p in ("COM", "LPT") for i in range(1, 10)]}:
        stem = "asset_" + stem
    directory.mkdir(parents=True, exist_ok=True)
    number = 0
    while True:
        tail = f"_{number}" if number else ""
        target = directory / f"{stem}{tail}{suffix}"
        try:
            handle = target.open("xb")
        except FileExistsError:
            number += 1
            continue
        try:
            with handle:
                handle.write(data)
        except OSError:
            target.unlink(missing_ok=True)
            raise
        return target
