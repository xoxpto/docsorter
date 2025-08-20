"""
File moving/copying utilities.
"""

from pathlib import Path
import shutil  # High-level file operations (copy2 preserves metadata like timestamps).
from .report import Stats

def place(fp: Path, target_dir: Path, copy: bool, dry_run: bool, verbose: bool, stats: Stats):
    """
    Move or copy a single file to the target directory.

    Args:
        fp: Source file path.
        target_dir: Destination directory where the file should end up.
        copy: If True, copy instead of move.
        dry_run: If True, only print actions (no changes on disk).
        verbose: If True, print each action.
        stats: Stats object to update counters.
    """
    # Make sure destination directory exists.
    target_dir.mkdir(parents=True, exist_ok=True)

    # Compose the final target path (same basename as the source).
    target = target_dir / fp.name

    # A small label for printing purposes.
    action = "copy" if copy else "move"

    if dry_run:
        # In dry-run mode we only report what would happen.
        if verbose:
            print(f"[dry-run] {action} {fp} -> {target}")
        return

    # Perform the actual file operation.
    if copy:
        shutil.copy2(fp, target)
        stats.copied += 1
    else:
        shutil.move(str(fp), str(target))
        stats.moved += 1

    if verbose:
        print(f"{action} {fp} -> {target}")
