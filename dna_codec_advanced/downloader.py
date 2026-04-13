"""
Human Genome Downloader Module
==============================

Automated genome data acquisition from public databases.
"""

# Extract downloader classes from codec.py
from .codec import HumanGenomeDownloader

__all__ = ["HumanGenomeDownloader"]