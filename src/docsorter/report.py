"""
Statistics data structure for reporting results to the user.
"""

from dataclasses import dataclass  # Dataclasses reduce boilerplate for simple containers.

@dataclass
class Stats:
    """
    Holds counters for actions performed during organization.
    """
    moved: int = 0
    copied: int = 0
    skipped: int = 0
    errors: int = 0

    def as_dict(self):
        """
        Return a plain dict for easy printing and potential JSON output in the future.
        """
        return vars(self)
