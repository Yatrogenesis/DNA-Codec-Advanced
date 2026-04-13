#!/usr/bin/env python3
"""
Test Suite for Advanced DNA Codec v3.0
=====================================

Comprehensive test suite for the DNA encoding/decoding system with
container protocol, encryption, and error correction.

Run with: python test_dna_codec.py
"""

import unittest
import os
import sys
import hashlib
from typing import Dict, List, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dna_codec_v3 import (
    ContainerDNACodec, 
    BiologicalSequencingSimulator,
    HumanGenomeDownloader,
    demo_container_protocol,
    demo_advanced_extensions
)


class TestBasicCodec(unittest.TestCase):
    """Test basic encoding/decoding functionality"""
    
    def setUp(self):
        self.codec = ContainerDNACodec()
        self.test_data = b"Hello, DNA storage world! This is a test message."
        self.test_string = "Testing string encoding and decoding."
    
    def test_basic_string_encoding(self):
        """Test basic string encoding and decoding"""
        encoded = self.codec.encode(self.test_string)
        self.assertIsInstance(encoded, str)
        self.assertTrue(all(c in 'ATGC' for c in encoded))
        
        decoded_data, metadata = self.codec.decode(encoded)
        decoded_string = decoded_data.decode('utf-8')
        
        self.assertEqual(decoded_string, self.test_string)
        self.assertTrue(metadata['checksum_valid'])
        self.assertGreaterEqual(metadata['containers_found'], 2)
    
    def test_basic_bytes_encoding(self):
        """Test basic bytes encoding and decoding"""
        encoded = self.codec.encode(self.test_data)
        self.assertIsInstance(encoded, str)
        
        decoded_data, metadata = self.codec.decode(encoded)
        
        self.assertEqual(decoded_data, self.test_data)
        self.assertTrue(metadata['checksum_valid'])
        self.assertEqual(len(metadata['decoding_errors']), 0)
    
    def test_empty_data(self):
        """Test handling of empty data"""
        encoded = self.codec.encode("")
        decoded_data, metadata = self.codec.decode(encoded)
        decoded_string = decoded_data.decode('utf-8')
        
        self.assertEqual(decoded_string, "")
        self.assertTrue(metadata['checksum_valid'])
    
    def test_large_data(self):
        """Test handling of large data requiring multiple containers"""
        # Use codec with small container size to force multiple containers
        small_codec = ContainerDNACodec(max_container_size=100)
        large_data = "A" * 1000  # 1KB of data
        encoded = small_codec.encode(large_data)
        
        decoded_data, metadata = small_codec.decode(encoded)
        decoded_string = decoded_data.decode('utf-8')
        
        self.assertEqual(decoded_string, large_data)
        self.assertTrue(metadata['checksum_valid'])
        self.assertGreater(metadata['data_containers'], 1)
    
    def test_binary_data_with_embedded_markers(self):
        """Test binary data containing potential marker sequences"""
        # Create binary data with embedded marker-like sequences
        marker_start = self.codec._dna_to_bytes(self.codec.CONTAINER_START)
        marker_end = self.codec._dna_to_bytes(self.codec.CONTAINER_END)
        
        problematic_data = bytearray(b"Binary data: ")
        problematic_data.extend(marker_start)
        problematic_data.extend(b" middle content ")
        problematic_data.extend(marker_end)
        problematic_data.extend(b" end content")
        
        encoded = self.codec.encode(bytes(problematic_data))
        decoded_data, metadata = self.codec.decode(encoded)
        
        self.assertEqual(decoded_data, bytes(problematic_data))
        self.assertTrue(metadata['checksum_valid'])


class TestContainerProtocol(unittest.TestCase):
    """Test container protocol specifics"""
    
    def setUp(self):
        self.codec = ContainerDNACodec(max_container_size=100)
    
    def test_container_parsing(self):
        """Test container parsing and structure"""
        test_data = "Test container parsing"
        encoded = self.codec.encode(test_data)
        
        # Analyze the sequence structure
        analysis = self.codec.analyze_sequence(encoded)
        
        self.assertGreaterEqual(analysis['containers_detected'], 2)
        self.assertIn('METADATA', analysis['container_types'])
        self.assertIn('CHECKSUM', analysis['container_types'])
        self.assertGreater(analysis['coverage_ratio'], 0.8)
        self.assertEqual(analysis['parsing_errors'], 0)
    
    def test_corrupted_sequence_handling(self):
        """Test handling of corrupted DNA sequences"""
        test_data = "Test corruption handling"
        encoded = self.codec.encode(test_data)
        
        # Corrupt the sequence by changing random nucleotides
        corrupted = list(encoded)
        corruption_positions = [100, 200, 300, 400, 500]
        for pos in corruption_positions:
            if pos < len(corrupted):
                corrupted[pos] = 'N'  # Invalid nucleotide
        
        corrupted_sequence = ''.join(corrupted)
        
        # Should handle corruption gracefully
        try:
            decoded_data, metadata = self.codec.decode(corrupted_sequence)
            # If decoding succeeds, check for error reporting
            self.assertGreater(len(metadata['decoding_errors']), 0)
        except ValueError:
            # Corruption too severe - expected behavior
            pass
    
    def test_nucleotide_composition(self):
        """Test that output has reasonable nucleotide composition"""
        test_data = "ATGC" * 100
        encoded = self.codec.encode(test_data)
        
        analysis = self.codec.analyze_sequence(encoded)
        composition = analysis['nucleotide_composition']
        
        # Check that all nucleotides are present
        for nt in ['A', 'T', 'G', 'C']:
            self.assertGreater(composition[nt], 0)
        
        # Check for invalid nucleotides
        self.assertEqual(composition['other'], 0)


class TestAdvancedFeatures(unittest.TestCase):
    """Test advanced features like encryption and compression"""
    
    def test_compression_large_data(self):
        """Test compression with repetitive data"""
        # Create highly repetitive data that should compress well
        repetitive_data = "ATGCATGCATGC" * 100
        
        codec = ContainerDNACodec(compression_threshold=50)
        encoded = codec.encode(repetitive_data)
        
        decoded_data, metadata = codec.decode(encoded)
        decoded_string = decoded_data.decode('utf-8')
        
        self.assertEqual(decoded_string, repetitive_data)
        # Should have applied compression
        self.assertTrue(metadata['file_metadata'].get('compressed', False))
    
    def test_encryption_basic(self):
        """Test basic encryption functionality (if available)"""
        try:
            crypto_codec = ContainerDNACodec(enable_encryption=True)
            
            # Set a biological key
            test_key = "ATGCGATCGTAGCTAGCGATCGTAGCTAGC"
            crypto_codec.set_biological_key(test_key, "Test key")
            
            secret_data = "This is secret information"
            
            # Encode with encryption
            encrypted_dna = crypto_codec.encode(secret_data)
            
            # Decode with same key
            decrypted_data, metadata = crypto_codec.decode(encrypted_dna)
            decrypted_text = decrypted_data.decode('utf-8')
            
            self.assertEqual(decrypted_text, secret_data)
            self.assertTrue(metadata['file_metadata'].get('encrypted', False))
            
        except ImportError:
            self.skipTest("Cryptography not available")
    
    def test_reed_solomon_basic(self):
        """Test basic Reed-Solomon functionality (if available)"""
        try:
            rs_codec = ContainerDNACodec(enable_reed_solomon=True)
            
            test_data = "Data with error protection"
            encoded = rs_codec.encode(test_data)
            
            decoded_data, metadata = rs_codec.decode(encoded)
            decoded_string = decoded_data.decode('utf-8')
            
            self.assertEqual(decoded_string, test_data)
            self.assertTrue(metadata['file_metadata'].get('reed_solomon', False))
            
        except ImportError:
            self.skipTest("Reed-Solomon not available")


class TestSequencingSimulator(unittest.TestCase):
    """Test biological sequencing error simulation"""
    
    def test_illumina_simulation(self):
        """Test Illumina platform simulation"""
        simulator = BiologicalSequencingSimulator('Illumina')
        test_sequence = "ATGCGATCGTAGCTAGC" * 20
        
        noisy_sequence, stats = simulator.simulate_errors(test_sequence, seed=42)
        
        self.assertEqual(stats['platform'], 'Illumina')
        self.assertEqual(stats['original_length'], len(test_sequence))
        self.assertGreaterEqual(stats['total_errors'], 0)
        self.assertIn('substitutions', stats['error_breakdown'])
        self.assertIn('insertions', stats['error_breakdown'])
        self.assertIn('deletions', stats['error_breakdown'])
    
    def test_nanopore_simulation(self):
        """Test Nanopore platform simulation"""
        simulator = BiologicalSequencingSimulator('Nanopore')
        test_sequence = "ATGCGATCG" * 50
        
        noisy_sequence, stats = simulator.simulate_errors(test_sequence, seed=42)
        
        self.assertEqual(stats['platform'], 'Nanopore')
        # Nanopore should have higher error rates
        self.assertGreater(stats['error_rate'], 0.01)  # >1% error rate expected
    
    def test_homopolymer_sensitivity(self):
        """Test homopolymer error sensitivity"""
        simulator = BiologicalSequencingSimulator('Nanopore')
        
        # Sequence with long homopolymers
        homopolymer_sequence = "ATGC" + "A" * 20 + "TGCA" + "T" * 15 + "GCAT"
        
        noisy_sequence, stats = simulator.simulate_errors(homopolymer_sequence, seed=42)
        
        # Should have some errors due to homopolymer runs
        self.assertGreater(stats['total_errors'], 0)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple features"""
    
    def test_full_pipeline_with_errors(self):
        """Test complete pipeline with simulated sequencing errors"""
        # Create codec
        codec = ContainerDNACodec()
        
        # Original data
        original_data = "Integration test: This data will go through the full pipeline"
        
        # Encode
        encoded_dna = codec.encode(original_data)
        
        # Simulate sequencing errors
        simulator = BiologicalSequencingSimulator('Illumina')
        noisy_dna, error_stats = simulator.simulate_errors(encoded_dna, seed=42)
        
        # Try to decode noisy sequence
        try:
            decoded_data, decode_metadata = codec.decode(noisy_dna)
            decoded_string = decoded_data.decode('utf-8')
            
            # Should either succeed perfectly or fail gracefully
            if decode_metadata['checksum_valid']:
                self.assertEqual(decoded_string, original_data)
            else:
                # Checksum should catch the errors
                self.assertFalse(decode_metadata['checksum_valid'])
                
        except ValueError:
            # Severe corruption - expected behavior
            pass
    
    def test_metadata_preservation(self):
        """Test that metadata is properly preserved"""
        codec = ContainerDNACodec()
        
        original_metadata = {
            'experiment': 'test_run',
            'version': '1.0',
            'author': 'test_user'
        }
        
        test_data = "Data with custom metadata"
        encoded = codec.encode(test_data, metadata=original_metadata)
        
        decoded_data, metadata = codec.decode(encoded)
        decoded_string = decoded_data.decode('utf-8')
        
        self.assertEqual(decoded_string, test_data)
        
        # Check metadata preservation
        file_metadata = metadata['file_metadata']
        self.assertEqual(file_metadata['experiment'], 'test_run')
        self.assertEqual(file_metadata['version'], '1.0')
        self.assertEqual(file_metadata['author'], 'test_user')


def run_performance_benchmark():
    """Run performance benchmarks"""
    print("\n=== PERFORMANCE BENCHMARKS ===")
    
    codec = ContainerDNACodec()
    
    # Test different data sizes
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        test_data = "A" * size
        
        import time
        
        # Encoding benchmark
        start_time = time.time()
        encoded = codec.encode(test_data)
        encode_time = time.time() - start_time
        
        # Decoding benchmark
        start_time = time.time()
        decoded_data, metadata = codec.decode(encoded)
        decode_time = time.time() - start_time
        
        # Calculate metrics
        encoding_ratio = len(encoded) / (size * 8 / 2)  # nucleotides vs theoretical minimum
        
        print(f"\nData size: {size} bytes")
        print(f"Encoded length: {len(encoded)} nucleotides")
        print(f"Encoding ratio: {encoding_ratio:.2f}x theoretical minimum")
        print(f"Encoding time: {encode_time:.3f}s ({size/encode_time:.0f} bytes/s)")
        print(f"Decoding time: {decode_time:.3f}s ({size/decode_time:.0f} bytes/s)")
        print(f"Checksum valid: {metadata['checksum_valid']}")
        print(f"Containers: {metadata['containers_found']}")


def main():
    """Main test runner"""
    print("Advanced DNA Codec v3.0 - Test Suite")
    print("=" * 50)
    
    # Run unit tests
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestBasicCodec,
        TestContainerProtocol,
        TestAdvancedFeatures,
        TestSequencingSimulator,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Run performance benchmarks
    if result.wasSuccessful():
        run_performance_benchmark()
        
        print("\n=== DEMO EXECUTIONS ===")
        
        # Run demo functions
        try:
            print("\n--- Container Protocol Demo ---")
            demo_container_protocol()
            
            print("\n--- Advanced Extensions Demo ---")
            demo_advanced_extensions()
            
        except Exception as e:
            print(f"Demo execution error: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {'PASS' if result.wasSuccessful() else 'FAIL'}")
    
    if not result.wasSuccessful():
        print("\nFAILURES:")
        for test, error in result.failures:
            print(f"  {test}: {error.split(chr(10))[0]}")
        
        print("\nERRORS:")
        for test, error in result.errors:
            print(f"  {test}: {error.split(chr(10))[0]}")
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())