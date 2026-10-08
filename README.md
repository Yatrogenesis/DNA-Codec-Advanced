# DNA Codec v3.0 — Self-Descriptive Container Protocol for DNA Data Storage

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--6093--8267-green.svg)](https://orcid.org/0009-0008-6093-8267)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20444764.svg)](https://doi.org/10.5281/zenodo.20444764)

**Author:** Francisco Molina-Burgos  
**ORCID:** 0009-0008-6093-8267  
**Contact:** pako.molina@gmail.com  

---

## Overview

DNA Codec v3.0 implements a self-descriptive container protocol for encoding arbitrary binary data into synthetic DNA sequences with robust error correction, cryptographic security, and zero parsing ambiguity.

### Key Technical Contributions

- **Container Protocol v3.0** — Self-descriptive DNA containers with unique 12-nucleotide boundary markers (collision probability: 1 in 16.7 million), explicit length fields, and per-container checksums
- **Reed-Solomon parity (byte level)** — uses the `reedsolo` library with 10 parity symbols per block, which can correct a small, bounded number of corrupted bytes per block. It does not by itself correct DNA insertions or deletions, and no corruption-recovery rate has been measured and archived in this repository.
- **Optional encryption** — AES-256-GCM with a key derived by PBKDF2-HMAC-SHA256 (100,000 iterations) from a user-supplied DNA string. This is password-style key derivation, not a physical or biological authentication factor, and the KDF salt is a fixed constant in this release (see Known limitations).
- **Sequencing error simulation** — simple error models for Illumina, Oxford Nanopore, PacBio and synthesis platforms (`simulator.py`); they are not calibrated against published instrument error profiles.

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

There is **no working command-line interface in this release**: the `cli_interface.py` module referenced by earlier
versions of this README and by `dna_codec_advanced/cli.py` / `setup.py` is not part of the repository. Use the Python API below.

## Python API

Encryption and Reed-Solomon protection are **disabled by default**; enable them explicitly.

```python
from dna_codec_advanced import ContainerDNACodec

codec = ContainerDNACodec()                      # plain containers
dna = codec.encode(open("data.bin", "rb").read())  # bytes (or str) -> DNA string
data, metadata = codec.decode(dna)               # -> (bytes, dict)

# Optional features (both off unless requested)
codec = ContainerDNACodec(enable_encryption=True, enable_reed_solomon=True)
codec.set_biological_key("ATCGATCGATCGATCGATCGATCGATCGATCG")  # DNA string of at least 30 bases
dna_encrypted = codec.encode(b"secret")
data, metadata = codec.decode(dna_encrypted)
```

## Validation status

This repository does **not** contain archived statistical validation results. The notebook `benchmark_colab_T4.ipynb`
is a benchmark script whose outputs are not stored here, and any figures produced from simulated error models are
synthetic, not experimental sequencing data. Claims about recovery rates, throughput or comparisons with other
systems should be treated as unverified until raw results, environment and seeds are published.

## Repository Structure

```
dna_codec_advanced/    — Python package (codec.py, simulator.py, downloader.py; cli.py is not functional, see above)
dna_codec_v3.py        — Single-file codec implementation
tests/                 — Unit tests (tests/test_dna_codec.py, 16 test functions)
benchmark_colab_T4.ipynb — Benchmark notebook (outputs not archived)
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

## Known limitations

- The key-derivation salt used by `set_biological_key` is a fixed constant, so equal inputs give equal keys across installations.
- Reed-Solomon protection is byte-level; DNA insertions/deletions are not corrected by it.
- The command-line entry points declared in earlier packaging do not exist in this release.
- The unit tests import the single-file `dna_codec_v3.py`, not the `dna_codec_advanced` package, so the package itself has no automated test coverage (the coverage report shows 0 % for it); no coverage figure should be quoted.

## Data sources and attribution

`HumanGenomeDownloader` fetches reference sequences from Ensembl (`ftp.ensembl.org`). Ensembl data may be used and
redistributed, including commercially, with attribution: Cunningham F. et al., *Ensembl 2022*, Nucleic Acids Research
(doi:10.1093/nar/gkab1049).

## License note

The code is licensed under **AGPL-3.0** (see `LICENSE`). The archived Zenodo record for v3.0.0 may display a different
license (CC-BY-4.0) because its metadata was set when it was deposited; the repository license governs the code.

## Citation

If you use DNA Codec v3.0 in your research, please cite:

```bibtex
@software{molina2025dnacodec,
  title={DNA Codec v3.0: Self-Descriptive Container Protocol for Robust DNA Data Storage},
  author={Molina-Burgos, Francisco},
  year={2025},
  doi={10.5281/zenodo.20444764},
  url={https://doi.org/10.5281/zenodo.20444764},
  orcid={0009-0008-6093-8267}
}
```
