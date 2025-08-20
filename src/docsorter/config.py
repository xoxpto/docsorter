"""
Configuration loader for docsorter.

Reads optional YAML files to customize behavior (e.g., file extensions to include).
"""

import yaml  # PyYAML parses YAML into Python dictionaries.

def load_config(path):
    """
    Load YAML configuration from `path` and perform basic validation.

    Args:
        path: Path to a YAML file.

    Returns:
        dict: Parsed configuration (or empty dict if file is blank).
    """
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    # Basic validation: `extensions`, if present, must be a list of strings.
    if "extensions" in data and not isinstance(data["extensions"], list):
        raise ValueError("`extensions` must be a list of strings, e.g. ['pdf', 'jpg'].")

    return data
