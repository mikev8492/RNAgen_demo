# RNAgen - Streamlit Web UI

## Description:

Streamlit graphical web interface for RNAgen. 

### UI Features

- **Parameter controls** - configure all sequence generation settings from the sidebar using sliders and number inputs
- **Instant download** - generated sequences are available as a `.fasta` file with one click, no output path required
- **Sequence preview** - each sequence is displayed in an expandable panel showing GC content, ambiguity content, ORF type, and flanking status
- **Summary metrics** - after generation, a dashboard displays total sequences, complete ORF count, flanked count, and average length

### Live Demo

The hosted version is available at [rna-gen.streamlit.app](https://rna-gen.streamlit.app/).

## Run the UI Locally

```bash
cd RNAgen

streamlit run web/app.py
```


## Layout

The UI is split into two areas: a **sidebar** for configuration and a **main panel** for output.

## Sidebar - Parameters

All generation settings are controlled from the sidebar:

- **Number of sequences** - slider from 1 to 200 (default: 10)
- **Min / Max ORF length** - number inputs for the ORF length range in nucleotides (default: 100–1000). An error is shown if min ≥ max.
- **ORF completeness** - slider from 0.0 to 1.0 controlling the fraction of sequences that will have start (AUG) and stop codons (default: 0.7)
- **Flanking probability** - slider from 0.0 to 1.0 controlling how likely each sequence is to have UTR flanking regions (default: 0.5)
- **Flanking length** - slider from 10 to 300 nt controlling the length of those flanking regions (default: 50)

Clicking **⚡ Generate** runs the simulator with the current settings.

## Main Panel - Output

After generation, the main panel displays three sections:

**Summary metrics** - four cards showing total sequences generated, number of complete ORFs, number of flanked sequences, and average sequence length.

**Download button** - a one-click **⬇ Download FASTA** button that saves all generated sequences as `sequences.fasta`. No output path is required.

**Sequence preview** - each sequence is shown in a collapsible panel labelled with its ID, length, and GC content. Expanding a panel reveals:
- Tag badges for ORF type (Complete / Partial), flanking status (Flanked / Unflanked), GC content, and ambiguity content
- The full nucleotide sequence rendered in a monospace scrollable box

## Idle State

Before any sequences are generated, the main panel shows a short info message and an expandable **"What does RNAgen generate?"** explainer describing ORF types and flanking regions.

## Author:
Michael Villarreal - mvillar6@charlotte.edu | mikev8492@gmail.com
