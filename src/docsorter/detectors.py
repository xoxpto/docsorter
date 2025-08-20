"""
Date detection utilities.

We try multiple strategies in order:
1) Parse patterns from the filename (e.g., 2024-12-31 or 31_12_2024).
2) Read EXIF timestamps for images (DateTimeOriginal).
3) Fall back to file's modification time if nothing else is found.
"""

import re
import datetime as dt
from pathlib import Path
import exifread  # Library to extract EXIF data from image files.

# Regular expressions for common date patterns in filenames.
PATTERNS = [
    # yyyy-mm-dd, yyyy_mm_dd, yyyy.mm.dd
    r"(?P<y>20\d{2})[-_/\.](?P<m>0?[1-9]|1[0-2])[-_/\.](?P<d>0?[1-9]|[12]\d|3[01])",
    # dd-mm-yyyy, dd_mm_yyyy, dd.mm.yyyy
    r"(?P<d>0?[1-9]|[12]\d|3[01])[-_/\.](?P<m>0?[1-9]|1[0-2])[-_/\.](?P<y>20\d{2})",
]

def from_filename(path: Path):
    """
    Try to extract a date from the filename using regex patterns.

    Args:
        path: File path whose stem will be inspected.

    Returns:
        datetime.date or None
    """
    name = path.stem
    for pat in PATTERNS:
        m = re.search(pat, name)
        if m:
            y, mth, d = int(m["y"]), int(m["m"]), int(m["d"])
            return dt.date(y, mth, d)
    return None

def from_exif(path: Path):
    """
    Try to extract a date from image EXIF metadata.

    Returns:
        datetime.date or None
    """
    if path.suffix.lower() not in {".jpg", ".jpeg", ".tiff", ".png"}:
        return None
    try:
        with open(path, "rb") as f:
            tags = exifread.process_file(f, details=False)
        raw = tags.get("EXIF DateTimeOriginal") or tags.get("Image DateTime")
        if raw:
            s = str(raw)            # Typical format: "YYYY:MM:DD HH:MM:SS"
            y, m, d = int(s[0:4]), int(s[5:7]), int(s[8:10])
            return dt.date(y, m, d)
    except Exception:
        # Ignore EXIF issues and return None so the caller can try other methods.
        pass
    return None

def detect_date(path: Path):
    """
    Determine the best date for organizing this file.

    Order of precedence:
    filename pattern > EXIF metadata > file modification time.
    """
    return from_filename(path) or from_exif(path) or dt.date.fromtimestamp(path.stat().st_mtime)
