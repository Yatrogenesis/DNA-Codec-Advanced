#!/usr/bin/env python3
"""
Setup script for DNA-Codec-Advanced - Professional PyPI Distribution
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Version handling
version = "3.0.1"

setup(
    name="dna-codec-advanced",
    version=version,
    author="Francisco Molina",
    author_email="pako.molina@gmail.com",
    description="Advanced DNA Encoder/Decoder System v3.0 - Container Protocol for Robust Data Storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yatrogenesis/DNA-Codec-Advanced",
    project_urls={
        "Bug Reports": "https://github.com/Yatrogenesis/DNA-Codec-Advanced/issues",
        "Source": "https://github.com/Yatrogenesis/DNA-Codec-Advanced",
        "Documentation": "https://github.com/Yatrogenesis/DNA-Codec-Advanced#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archival",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "full": [
            "matplotlib>=3.0",
            "seaborn>=0.11",
            "jupyter>=1.0",
            "notebook>=6.0",
        ],
    },
    keywords=[
        "bioinformatics",
        "dna-storage",
        "data-archival",
        "synthetic-biology",
        "encryption",
        "reed-solomon",
        "error-correction",
        "genomics",
        "biotechnology",
    ],
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.fasta", "*.ipynb"],
    },
    zip_safe=False,
)