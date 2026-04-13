# DNA Codec v3.0 — Self-Descriptive Container Protocol for DNA Data Storage

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--6093--8267-green.svg)](https://orcid.org/0009-0008-6093-8267)

**Author:** Francisco Molina-Burgos  
**ORCID:** 0009-0008-6093-8267  
**Contact:** pako.molina@gmail.com  

---

## Overview

DNA Codec v3.0 implements a self-descriptive container protocol for encoding arbitrary binary data into synthetic DNA sequences with robust error correction, cryptographic security, and zero parsing ambiguity.

### Key Technical Contributions

- **Container Protocol v3.0** — Self-descriptive DNA containers with unique 12-nucleotide boundary markers (collision probability: 1 in 16.7 million), explicit length fields, and per-container checksums
- **Reed-Solomon Error Correction** — Mathematical recovery from up to 25% sequence corruption; validated across 100 independent replicates
- **Biological Cryptography** — AES-256-GCM encryption with PBKDF2-HMAC-SHA256 key derivation (100,000 iterations) from physical DNA sequences
- **Multi-Platform Biological Simulation** — Realistic sequencing error models for Illumina, Oxford Nanopore, PacBio, and synthesis platforms

### Container Structure

```
[START_MARKER][TYPE][LENGTH][DATA][CHECKSUM][END_MARKER]
 GATTACACAGTA  4nt   4nt    Nnt    4nt      TCATGTACAATC
```

| Container Type | Code | Purpose |
|---|---|---|
| METADATA | AAAA | Global file metadata |
| DATA | AAAT | Raw data segments |
| CHECKSUM | AATA | Global integrity |
| REDUNDANT | AATG | Reed-Solomon parity |
| INDEX | AATC | Segment indexing |
| COMPRESSED | AACG | Compressed payload |
| ENCRYPTED | AACT | Encrypted payload |
| REED_SOLOMON | AACC | RS-protected data |

## Installation

```bash
pip install -r requirements.txt
```

For full research extensions (figures, notebooks):

```bash
pip install -r requirements.txt matplotlib seaborn jupyter
```

## Quick Start

```bash
# Encode a file to DNA
python cli_interface.py encode document.pdf --output dna_sequence.fasta

# Decode DNA back to original
python cli_interface.py decode dna_sequence.fasta --output recovered_document.pdf

# Validate sequence for physical synthesis
python cli_interface.py validate dna_sequence.fasta --detailed

# Analyze GC content, homopolymers, synthesis constraints
python cli_interface.py analyze dna_sequence.fasta
```

## Python API

```python
from dna_codec_advanced import DNACodecAdvanced

codec = DNACodecAdvanced()

# Encode
with open("data.bin", "rb") as f:
    dna = codec.encode(f.read())

# Optional: biological key encryption
codec.set_biological_key("ATCGATCGATCG")
dna_encrypted = codec.encode(data)

# Decode
recovered = codec.decode(dna)
```

## Statistical Validation

The implementation has been validated against 100 independent replicates with real genomic data:

```bash
python statistical_validation.py
```

Results are reported in the companion article (see `article/`).

## Article

The full scientific article describing the Container Protocol v3.0 design, validation methodology, and comparative analysis is available in `article/`:

- `DNA_Codec_Article_FINAL.pdf` — Publication-ready manuscript
- `DNA_Codec_Article_FINAL.tex` — LaTeX source
- `references.bib` — Bibliography
- `figures/` — Publication-quality figures (600 DPI)

**Target journals:** Nature Biotechnology, Nature Communications, Bioinformatics

## Repository Structure

```
dna_codec_advanced/    — Core Python package
cli_interface.py       — Command-line interface
dna_codec_v3.py        — Main codec implementation (2,500+ lines)
statistical_validation.py  — Validation experiments
tests/                 — Test suite (220+ unit tests)
genome_data/           — Test genomic data (GRCh38 chr22)
article/               — Scientific publication package
Figure_Generator_COMPLETE.ipynb  — Publication figure generator
```

## Running Tests

```bash
pytest tests/ -v
```

## License

This software is released under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

AGPL-3.0 means:
- Academic and research use: **free and open**
- Network deployment (SaaS, APIs): must release source code of modified versions
- Commercial proprietary use: requires a separate commercial license

For commercial licensing: pako.molina@gmail.com

## Citation

If you use DNA Codec v3.0 in your research, please cite:

```bibtex
@software{molina2024dnacodec,
  title={DNA Codec v3.0: Self-Descriptive Container Protocol for Robust DNA Data Storage},
  author={Molina-Burgos, Francisco},
  year={2024},
  url={https://github.com/Yatrogenesis/DNA-Codec-Advanced},
  orcid={0009-0008-6093-8267}
}
```
