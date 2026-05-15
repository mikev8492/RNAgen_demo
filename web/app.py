import streamlit as st
import argparse
import io
import sys
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RNAgen",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Import simulator from src/ ────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.simulator import Simulator
from src.sequence_lib import write_fasta

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Tighten up the header */
    .block-container { padding-top: 2rem; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #1a1a2e;
        border: 1px solid #2d2d4e;
        border-radius: 8px;
        padding: 0.75rem 1rem;
    }

    /* Sequence preview box */
    .seq-box {
        font-family: 'Courier New', monospace;
        font-size: 0.75rem;
        background: #0f0f1a;
        color: #7eb8a4;
        border: 1px solid #2d2d4e;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        overflow-x: auto;
        white-space: pre-wrap;
        word-break: break-all;
        line-height: 1.6;
        max-height: 120px;
        overflow-y: auto;
    }

    .seq-header {
        font-family: 'Courier New', monospace;
        font-size: 0.7rem;
        color: #7a9ec0;
        margin-bottom: 0.25rem;
    }

    .tag {
        display: inline-block;
        font-size: 0.65rem;
        padding: 0.15rem 0.5rem;
        border-radius: 3px;
        margin-right: 0.3rem;
        margin-bottom: 0.3rem;
        font-family: monospace;
    }

    .tag-complete  { background: #1a3a2a; color: #7eb8a4; border: 1px solid #2a5a3a; }
    .tag-partial   { background: #3a2a1a; color: #c8a87a; border: 1px solid #5a3a1a; }
    .tag-flanked   { background: #1a2a3a; color: #7a9ec0; border: 1px solid #1a3a5a; }
    .tag-unflanked { background: #2a2a2a; color: #888;    border: 1px solid #3a3a3a; }
</style>
""", unsafe_allow_html=True)


# ── Helper: build args namespace from UI values ───────────────────────────────
def build_args(n, min_len, max_len, completeness, flanking_prob, flanking_length):
    args = argparse.Namespace(
        num_sequences=n,
        min_length=min_len,
        max_length=max_len,
        completeness=completeness,
        flanking_prob=flanking_prob,
        flanking_length=flanking_length,
        output="sequences.fasta",
    )
    return args


def sequences_to_fasta(sequences) -> str:
    """Convert generate_sequences() output to FASTA string."""
    lines = []
    for seq_id, description, seq in sequences:
        desc_str = " | ".join(description)
        lines.append(f">{seq_id} {desc_str}")
        # Wrap sequence at 60 chars (standard FASTA)
        for i in range(0, len(seq), 60):
            lines.append(seq[i:i+60])
    return "\n".join(lines)


def tag(label, kind):
    return f'<span class="tag tag-{kind}">{label}</span>'


# ── Sidebar: parameters ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 RNAgen")
    st.markdown("Synthetic RNA sequence generator")
    st.divider()

    st.markdown("#### Sequences")
    n = st.slider("Number of sequences", min_value=1, max_value=200, value=10, step=1)

    st.markdown("#### ORF Length")
    col1, col2 = st.columns(2)
    with col1:
        min_len = st.number_input("Min", min_value=30, max_value=4900, value=100, step=10)
    with col2:
        max_len = st.number_input("Max", min_value=100, max_value=5000, value=1000, step=10)

    if min_len >= max_len:
        st.error("Min length must be less than Max length.")

    st.markdown("#### ORF Completeness")
    completeness = st.slider(
        "Fraction with start/stop codons",
        min_value=0.0, max_value=1.0, value=0.7, step=0.05,
        help="1.0 = all complete ORFs, 0.0 = all partial"
    )

    st.markdown("#### Flanking Regions")
    flanking_prob = st.slider(
        "Probability of flanking",
        min_value=0.0, max_value=1.0, value=0.5, step=0.05,
    )
    flanking_length = st.slider(
        "Flanking length (nt)",
        min_value=10, max_value=300, value=50, step=10,
    )

    st.divider()
    generate = st.button("⚡ Generate", use_container_width=True, type="primary")


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("# RNAgen")
st.markdown("Configure parameters in the sidebar, then click **Generate**.")
st.divider()

if generate and min_len < max_len:
    with st.spinner("Generating sequences..."):
        args = build_args(n, min_len, max_len, completeness, flanking_prob, flanking_length)
        sim = Simulator(args)
        sequences = sim.generate_sequences()
        fasta_str = sequences_to_fasta(sequences)

    # ── Summary metrics ───────────────────────────────────────────────────────
    complete_count  = sum(1 for _, desc, _ in sequences if any("Complete" in d for d in desc))
    partial_count   = n - complete_count
    flanked_count   = sum(1 for _, desc, _ in sequences if any("Flanked" == d.split(" = ")[-1] for d in desc))
    avg_len         = sum(len(seq) for _, _, seq in sequences) // n

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sequences",     n)
    c2.metric("Complete ORFs", complete_count)
    c3.metric("Flanked",       flanked_count)
    c4.metric("Avg Length",    f"{avg_len} nt")

    st.divider()

    # ── Download button ───────────────────────────────────────────────────────
    st.download_button(
        label="⬇ Download FASTA",
        data=fasta_str,
        file_name="sequences.fasta",
        mime="text/plain",
        use_container_width=False,
    )

    st.divider()

    # ── Sequence preview table ────────────────────────────────────────────────
    st.markdown(f"### Preview — {n} sequences")

    for seq_id, description, seq in sequences:
        desc_dict = {}
        for d in description:
            k, v = d.split(" = ")
            desc_dict[k.strip()] = v.strip()

        orf_type    = desc_dict.get("ORF Type", "")
        flank_stat  = desc_dict.get("Status", "")
        gc          = desc_dict.get("GC", "")
        amb         = desc_dict.get("Ambiguity", "")
        length      = desc_dict.get("Length", "")

        orf_kind    = "complete"  if "Complete" in orf_type  else "partial"
        flank_kind  = "flanked"   if flank_stat == "Flanked" else "unflanked"

        with st.expander(f"{seq_id}  ·  {length}  ·  GC {gc}"):
            # Tags row
            tags_html = (
                tag(orf_type,   orf_kind)  +
                tag(flank_stat, flank_kind) +
                tag(f"GC {gc}", "flanked")  +
                tag(f"Amb {amb}", "unflanked")
            )
            st.markdown(tags_html, unsafe_allow_html=True)

            # Sequence
            st.markdown(
                f'<div class="seq-box">{seq}</div>',
                unsafe_allow_html=True
            )

elif generate and min_len >= max_len:
    st.error("Fix the length parameters in the sidebar before generating.")

else:
    # Placeholder state
    st.info("👈 Set your parameters in the sidebar and click **Generate** to create sequences.")

    with st.expander("What does RNAgen generate?"):
        st.markdown("""
        **RNAgen** produces synthetic RNA sequences in FASTA format with the following features:

        - **Complete ORFs** — sequences with AUG start codon and a stop codon (UAA, UAG, UGA)
        - **Partial ORFs** — randomly generated sequences without start/stop codons
        - **Flanking regions** — optional 5′ and 3′ untranslated regions of configurable length

        Each sequence in the output includes metadata: length, GC content, ambiguity content, ORF type, and flanking status.
        """)
