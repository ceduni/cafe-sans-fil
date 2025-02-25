"""
Module for handling cafe-related helper functions.
"""

import re
import unicodedata
from datetime import datetime


def slugify(text):
    """Generate a slug from the given text."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    slug = re.sub(r"\W+", "-", text)
    slug = slug.strip("-")
    return slug


def time_blocks_overlap(block1, block2):
    """Check if two time blocks overlap."""
    start1, end1 = datetime.strptime(block1.start, "%H:%M"), datetime.strptime(
        block1.end, "%H:%M"
    )
    start2, end2 = datetime.strptime(block2.start, "%H:%M"), datetime.strptime(
        block2.end, "%H:%M"
    )
    return start1 < end2 and start2 < end1
