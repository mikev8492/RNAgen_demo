#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, sys
from pathlib import Path
from src.simulator import Simulator

def create_parser(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Creates and configures argument parser.
    Args: 
        argv - optional list of CLI arguments. If None, 
    Returns:
        argparse.Namespace
            Parsed arguments with attributes
    """
    parser = argparse.ArgumentParser(
        description="Generate synthetic RNA sequences in FASTA format."
    )
    parser.add_argument("-n", "--num-sequences", type=int, default=10, help="Number of sequences to generate.")

    parser.add_argument("-o", "--output", type=str, default="sequences.fasta", help="Output FASTA file name.")

    parser.add_argument("--min-length", type=int, default=100, help="Minimum ORF length.")

    parser.add_argument("--max-length", type=int, default=1000, help="Maximum ORF length.")

    parser.add_argument("--flanking-prob", type=float, default=0.5, help="Flanking probability 0-1.")

    parser.add_argument("--flanking-length", type=int, default=50, help="Flanking sequence length.")

    parser.add_argument("--completeness", type=float, default=0.7, help="Ratio of complete ORFs 0-1.")
    
    return parser.parse_args(argv)
    

def validate_arguments(args: argparse.Namespace) -> None:
    """
    Check Ensures:
    - All number parameters are valid.
    - All string parameters are non-empty.
    - min values are smaller than max values

    If validation fails, writes an error message to stderr and exits
    the program with a non-zero status code.

    """
    num_fields = ["num_sequences", "min_length", "max_length", "flanking_prob", "flanking_length", "completeness"]
    
    # Check for valid numbers
    for field in num_fields:
        value = getattr(args, field)
        # Validate integers
        if isinstance(value, int):
            if value < 1:
                sys.stderr.write(f"Error: {field} must be an integer >= 1.\n")
                sys.exit(1)
        # validate float
        elif isinstance(value, float):
            if value <= 0:
                sys.stderr.write(f"Error: {field} must be between 0 and 1.\n")
                sys.exit(1)

    # Check for valid string
    str_value = getattr(args, "output")
    if not isinstance(str_value, str) or str_value == "":
        sys.stderr.write(f"Error: output filename must be a non-empty string.\n")
        sys.exit(1)

    # Check min/max values are logical
    min = getattr(args, "min_length")
    max = getattr(args, "max_length")
    if min >= max:
        sys.stderr.write(f"Error: Minimum ORF length cannot be greater than Maximum")
    return

def create_output() -> None:
    """
    Creates output folder for user
    """
    folder_path = Path("output")
    folder_path.mkdir(parents=True, exist_ok=True)

def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    try:
        create_output()
        # 1. Parse args
        args = create_parser(argv)
        # 2. Validate args
        validate_arguments(args)
        # 3. Create Simulator
        rna = Simulator(args)
        # 4. Save FASTA
        rna.save_fasta(args.output)
        # 5. Return 0 on success, 1 on error
        sys.stdout.write(f"\n\u2713 Successfully generated {args.num_sequences} RNA sequences\n")
        sys.stdout.write(f"\u2713 Sequences saved to output/{args.output}\n")
        sys.stdout.write(rna.generate_report())
        return 0

    except Exception as err:
        sys.stderr.write(f"Error: {str(err)}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())