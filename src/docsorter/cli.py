"""
Command-line interface (CLI) for docsorter.

This module defines a Typer application that exposes a `run` command to organize files
from a source directory into a destination directory structured by YEAR/MONTH.
"""

from pathlib import Path  # Pathlib gives convenient, cross-platform path handling.
import typer               # Typer helps build modern CLIs with automatic help.
from rich.console import Console  # Rich provides pretty terminal output.

from .config import load_config   # Load YAML configuration if provided by the user.
from .core import organize        # Core logic that performs the organization.

# Create a Typer application instance; this is the root CLI object.
app = typer.Typer(add_completion=False)

# Instantiate a Rich console for styled output.
console = Console()

# Define the `run` command of our CLI.
@app.command()
def run(
    # `source` must exist and be a directory (no single file). Typer validates these.
    source: Path = typer.Argument(..., exists=True, readable=True, dir_okay=True, file_okay=False),
    # `dest` is where organized files will be placed; it can be created if missing.
    dest: Path = typer.Argument(...),
    # Optional config file (.yaml) with rules such as allowed extensions.
    config: Path = typer.Option(None, "--config", "-c", exists=True, readable=True),
    # If True, copy files instead of moving them (safer but duplicates data).
    copy: bool = typer.Option(False, "--copy", help="Copy instead of move"),
    # If True, print what would happen but do not change anything on disk.
    dry_run: bool = typer.Option(False, "--dry-run", help="Plan actions without changing files"),
    # Toggle verbose mode to show each action taken per file.
    verbose: bool = typer.Option(True, "--verbose/--no-verbose", help="Show progress messages"),
):
    """
    Organize files from SOURCE into DEST/YYYY/MM/.
    Date detection priority: filename patterns -> EXIF (images) -> file modification time.
    """
    # Load config from YAML if provided; otherwise use defaults inside core logic.
    cfg = load_config(config) if config else {}

    # Perform the organization and collect summary statistics as a dict.
    stats = organize(source, dest, cfg, copy=copy, dry_run=dry_run, verbose=verbose)

    # Print a concise summary using Rich formatting.
    console.print(
        f"[bold]Done[/]: {stats['moved']} moved, "
        f"{stats['copied']} copied, {stats['skipped']} skipped, "
        f"{stats['errors']} errors."
    )

# Allow running `python -m docsorter.cli` directly during development.
if __name__ == "__main__":
    app()
