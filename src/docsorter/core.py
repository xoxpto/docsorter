"""
Core orchestration logic.

Walks the source directory, filters files by extension, detects a date for each file,
and then places the file under DEST/YYYY/MM using the move/copy utilities.
"""

from pathlib import Path
from .detectors import detect_date
from .mover import place
from .report import Stats

def organize(source: Path, dest: Path, cfg: dict, copy: bool, dry_run: bool, verbose: bool):
    """
    Organize files from `source` into `dest/YYYY/MM`.

    Args:
        source: Root folder to scan recursively.
        dest: Destination root folder for organized files.
        cfg: Optional configuration dictionary (e.g., allowed extensions).
        copy: Copy instead of move if True.
        dry_run: Only print what would be done if True.
        verbose: Print per-file actions if True.

    Returns:
        dict: Summary statistics of the operation.
    """
    stats = Stats()

    # Ensure destination root exists to avoid errors when placing files.
    dest.mkdir(parents=True, exist_ok=True)

    # Allowed extensions come from config or defaults if not provided.
    patterns = cfg.get("extensions", ["pdf", "jpg", "jpeg", "png", "docx", "xlsx", "txt"])
    exts = {f".{e.lower().lstrip('.')}" for e in patterns}

    # Recursively iterate through all files under `source`.
    for fp in source.rglob("*"):
        # Skip non-files and files whose extension is not in our whitelist.
        if not fp.is_file() or fp.suffix.lower() not in exts:
            continue
        try:
            # Determine a date to categorize this file.
            dt = detect_date(fp)
            year = f"{dt.year:04d}"
            month = f"{dt.month:02d}"

            # Build the destination directory based on the detected date.
            target_dir = dest / year / month

            # Move/copy the file and update statistics.
            place(fp, target_dir, copy=copy, dry_run=dry_run, verbose=verbose, stats=stats)
        except Exception:
            # On any unexpected error, increment error counter and continue with others.
            stats.errors += 1

    # Return a plain dict for convenience (easy to print or serialize).
    return stats.as_dict()
