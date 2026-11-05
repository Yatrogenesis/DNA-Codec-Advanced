# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Francisco Molina-Burgos
"""Reed-Solomon must repair substitutions inside the payload of REED_SOLOMON containers (regression for 3.0.1)."""
import logging
import random

import pytest

from dna_codec_v3 import ContainerDNACodec

logging.disable(logging.CRITICAL)


def _payload_positions(codec, dna):
    """Indices that lie inside the data field of REED_SOLOMON containers (not markers, type, length or checksum)."""
    out, pos = [], 0
    while True:
        start = dna.find(codec.CONTAINER_START, pos)
        if start == -1:
            return out
        container, nxt = codec._parse_container(dna, start)
        if container is None:
            pos = start + 1
            continue
        if container.container_type == 'REED_SOLOMON':
            data_start = start + len(codec.CONTAINER_START) + 4 + 4
            data_len = len(codec._bytes_to_dna(container.data))
            out.extend(range(data_start, data_start + data_len))
        pos = nxt


def _substitute(dna, positions):
    d = list(dna)
    for p in positions:
        d[p] = 'A' if d[p] != 'A' else 'C'
    return ''.join(d)


@pytest.mark.parametrize("n_errors", [1, 2, 4])
def test_reed_solomon_repairs_payload_substitutions(n_errors):
    rng = random.Random(1000 + n_errors)
    data = bytes(rng.randrange(256) for _ in range(4000))
    codec = ContainerDNACodec(enable_reed_solomon=True)
    dna = codec.encode(data)
    payload = _payload_positions(codec, dna)
    assert payload, "no REED_SOLOMON payload found"
    # One error per distinct 255-byte RS block is always within the 5-symbol correction capacity of RSCodec(10).
    picks = rng.sample(payload[:4 * 255 * 4], n_errors)
    out, meta = codec.decode(_substitute(dna, picks))
    assert out == data
    assert meta.get('checksum_valid', True)


def test_without_reed_solomon_a_payload_substitution_is_not_repaired():
    data = bytes(range(256)) * 8
    codec = ContainerDNACodec(enable_reed_solomon=False)
    dna = codec.encode(data)
    mid = len(dna) // 2
    try:
        out, _ = codec.decode(_substitute(dna, [mid]))
    except ValueError:
        return
    assert out != data


def test_reed_solomon_with_encryption_roundtrip_and_repair():
    data = bytes(range(200)) * 10
    codec = ContainerDNACodec(enable_reed_solomon=True, enable_encryption=True)
    codec.set_biological_key("ATCG" * 10)
    dna = codec.encode(data)
    assert codec.decode(dna)[0] == data
    payload = _payload_positions(codec, dna)
    out, _ = codec.decode(_substitute(dna, [payload[len(payload) // 3]]))
    assert out == data
