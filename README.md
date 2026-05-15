# RNAgen | RNA Sequence Simulator

>Live demo: [RNAgen]()
## Description:
This project is a Python-based RNA sequence simulator that generates synthetic RNA sequences in FASTA format. The simulator produces Open Reading Frames (ORFs) with configurable properties, including complete and partial ORFs, optional flanking regions, and sequence-level metadata such as GC content and ambiguity content. It is designed for bioinformatics workflows, testing pipelines, and educational purposes.

## Features:
- Generates synthetic RNA sequences with randomized content
- Support for **complete ORFs** (start + stop codons)
- Support for **partial/random sequences**
- Configurable **sequence length ranges**
- Optional **flanking regions** to simulate genomic context
- Metadata calculation:
  - GC content (%)
  - Ambiguity content (%)
- Output in **FASTA format**
- Fully configurable via **command-line interface (argparse)**
- Modular, reusable code structure


## Requirements:
- Python 3.11 or later
- Conda (Anaconda or Miniconda)

## Project Structure:
```
└── 📁RNAgen_demo
    └── 📁.github
        └── 📁workflows
            ├── keep_alive.yml
    └── 📁src
        └── 📁__pycache__
            ├── sequence_lib.cpython-311.pyc
            ├── simulator.cpython-311.pyc
        ├── __init__.py
        ├── sequence_lib.py
        ├── simulator.py
    └── 📁web
        ├── app.py
        ├── UI-README.md
    ├── .gitignore
    ├── environment.yml
    ├── LICENSE
    ├── main.py
    ├── README.md
    └── requirements.txt
```

- `main.py`: CLI entry point

- `src/simulator.py`: Core simulation logic

- `src/sequence_lib.py`: Utility functions

## Installation:

### 1. Clone the repository
```bash
git clone https://github.com/mikev8492/RNAgen.git

cd RNAgen
```
### 2. Create conda environment
```bash
conda env create -f environment.yml

conda activate RNAgen
```
### 3. Verify installation
```bash
python main.py --help
```

## Usage:
 ### Default:
 ```bash
python main.py
 ```
 ### Example with custom parameters:
 ```bash
python main.py -n 50 -o my_sequences.fasta --min-length 200 --max-length 2000
 ```

 ### Example with Flanking control:
 ```bash
python main.py -n 20 --flanking-prob 0.8 --flanking-length 100
 ```


## Command-Line Arguments:
| Argument                | Description                                  | Default         |
| ----------------------- | -------------------------------------------- | --------------- |
| `-n`, `--num-sequences` | Number of sequences to generate              | 10              |
| `-o`, `--output`        | Output FASTA file                            | sequences.fasta |
| `--min-length`          | Minimum ORF length                           | 100             |
| `--max-length`          | Maximum ORF length                           | 1000            |
| `--flanking-prob`       | Probability of adding flanking regions (0–1) | 0.5             |
| `--flanking-length`     | Length of flanking sequences                 | 50              |
| `--completeness`        | Fraction of complete ORFs (0–1)              | 0.7             |



## Output Format:
Sequences are written in FASTA format to `output` folder:
```
>seq_001 length=523 gc_content=45.5 ambiguity=0.0 type=complete flanked=yes
ACGUACGUACGUACGUAUGCCCUACGUACGUACGUACGUACGUACGUACGUAA
```
### Header fields:

- `length`: total sequence length

- `gc_content`: % of G and C nucleotides

- `ambiguity`: % of IUPAC ambiguous bases

- `type`: complete or partial ORF

- `flanked`: yes or no

## Algorithm Descriptions:

1. Determine ORF type
    - Sample from Bernoulli distribution using completeness_ratio
    - Decide between complete ORF or partial sequence
2. Generate ORF
    - Complete: AUG + codons + STOP
    - Partial: random RNA sequence
3. Add flanking regions (optional)
    - Based on flanking_probability
    - Add random sequences to both ends
4. Compute metadata
    - GC content
    - Ambiguity content
5. Write output
    - Format sequences in FASTA


## Metadata:
### GC Content:
GC% = (G count + C count)/ sequence length * 100

### Ambiguity Content:
Ambiguity % = (IUPAC ambiguous base count / sequence length) * 100

>Ambiguous bases follow IUPAC codes (e.g., N, R, Y).
## References:
1. FASTA format: https://en.wikipedia.org/wiki/FASTA_format
2. Open Reading Frames: https://en.wikipedia.org/wiki/Open_reading_frame
3. IUPAC nucleotide codes: https://www.bioinformatics.org/sms/iupac.html
4. Biopython documentation: https://biopython.org/
5. Python argparse: https://docs.python.org/3/library/argparse.html
6. Python type hints: https://docs.python.org/3/library/typing.html
7. PEP 8 style guide: https://peps.python.org/pep-0008/

## License:
GNU GENERAL PUBLIC LICENSE

## Author:
Michael Villarreal - mvillar6@charlotte.edu | mikev8492@gmail.com
