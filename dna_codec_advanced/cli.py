"""
Command Line Interface Module
=============================

Professional CLI for DNA-Codec-Advanced package.
"""

import sys
import os

# Import CLI functionality
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from cli_interface import *

def main():
    """Main entry point for the dna-codec command."""
    if len(sys.argv) == 1:
        parser = create_cli_interface()
        parser.print_help()
        sys.exit(1)
    
    parser = create_cli_interface()
    args = parser.parse_args()
    
    if args.command:
        success = execute_cli_command(args)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)

def cli_encode_wrapper():
    """Wrapper for direct encode command."""
    sys.argv = ['dna-encode'] + sys.argv[1:]
    main()

def cli_decode_wrapper():
    """Wrapper for direct decode command.""" 
    sys.argv = ['dna-decode'] + sys.argv[1:]
    main()

if __name__ == "__main__":
    main()