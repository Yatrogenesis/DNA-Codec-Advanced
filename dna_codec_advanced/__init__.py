"""
DNA-Codec-Advanced: Professional Data Storage in DNA Sequences
==============================================================

A production-ready system for encoding binary data into DNA sequences using 
an advanced container protocol with maximum robustness and zero ambiguity.

Key Features:
- Container Protocol v3.0 with unique 12-nucleotide markers
- AES-256-GCM biological key encryption
- Reed-Solomon error correction codes
- Intelligent DNA-specific compression
- Biological sequencing error simulation
- Scientific validation framework

Usage:
    >>> from dna_codec_advanced import ContainerDNACodec
    >>> codec = ContainerDNACodec()
    >>> encoded = codec.encode("Hello, DNA storage!")
    >>> decoded, metadata = codec.decode(encoded)

Author: Francisco Molina (ORCID: 0009-0008-6093-8267)
License: MIT
"""

from .codec import ContainerDNACodec, DNAContainer
from .simulator import BiologicalSequencingSimulator
from .downloader import HumanGenomeDownloader

__version__ = "3.0.0"
__author__ = "Francisco Molina"
__email__ = "pako.molina@gmail.com"
__license__ = "MIT"

__all__ = [
    "ContainerDNACodec",
    "DNAContainer", 
    "BiologicalSequencingSimulator",
    "HumanGenomeDownloader",
    "__version__",
]

# Version info tuple for programmatic access
VERSION_INFO = (3, 0, 0)

# Package metadata
PACKAGE_INFO = {
    "name": "dna-codec-advanced",
    "version": __version__,
    "description": "Advanced DNA Encoder/Decoder System v3.0",
    "author": __author__,
    "author_email": __email__,
    "license": __license__,
    "url": "https://github.com/Yatrogenesis/DNA-Codec-Advanced",
}

def get_version():
    """Return the package version string."""
    return __version__

def get_package_info():
    """Return package metadata dictionary."""
    return PACKAGE_INFO.copy()