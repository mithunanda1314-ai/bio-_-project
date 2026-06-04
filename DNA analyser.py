

import streamlit as st
import matplotlib.pyplot as plt


st.title("DNA Sequence Analyzer")

uploaded_file = st.file_uploader(
    "Upload DNA File",
    type=["txt", "fasta"]
)

if uploaded_file:

    sequence = uploaded_file.read().decode("utf-8")

    if sequence.startswith(">"):
        lines = sequence.split("\n")
        sequence = "".join(lines[1:])

    sequence = sequence.upper()
    sequence = sequence.replace("\n", "")
    sequence = sequence.replace(" ", "")

    st.success("DNA File Loaded Successfully")

    A = sequence.count("A")
    T = sequence.count("T")
    G = sequence.count("G")
    C = sequence.count("C")

    st.subheader("DNA Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("A", A)
    col2.metric("T", T)
    col3.metric("G", G)
    col4.metric("C", C)

    length = len(sequence)

    gc_content = ((G + C) / length) * 100

    st.metric(
        "GC Content %",
        f"{gc_content:.2f}"
    )

    st.subheader("DNA Base Distribution")

    bases = ["A", "T", "G", "C"]
    counts = [A, T, G, C]

    fig, ax = plt.subplots(figsize=(8,5))

    bars = ax.bar(
        bases,
        counts
    )

    ax.set_title("Nucleotide Distribution")
    ax.set_xlabel("DNA Base")
    ax.set_ylabel("Count")

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height,
            str(int(height)),
            ha='center'
        )

    st.pyplot(fig)

    st.subheader("DNA Composition")

    fig2, ax2 = plt.subplots(figsize=(6,6))

    ax2.pie(
        counts,
        labels=bases,
        autopct='%1.1f%%'
    )

    ax2.set_title("Percentage Composition")

    st.pyplot(fig2)

    # mutation highlighter
    # Mutation Detection

    st.subheader("Mutation Detection")

    seq1 = st.text_area("Reference DNA")
    seq2 = st.text_area("Comparison DNA")

    if seq1 and seq2:

        seq1 = seq1.upper().replace(" ", "").replace("\n", "")
        seq2 = seq2.upper().replace(" ", "").replace("\n", "")

        mutations = []

        min_len = min(len(seq1), len(seq2))

        for i in range(min_len):

            if seq1[i] != seq2[i]:
                mutations.append(
                    f"Position {i + 1}: {seq1[i]} → {seq2[i]}"
                )

        st.write(
            f"Total Mutations Found: {len(mutations)}"
        )

        for m in mutations[:20]:
            st.write(m)

        # Similarity %

        matches = 0

        for i in range(min_len):

            if seq1[i] == seq2[i]:
                matches += 1

        similarity = (matches / min_len) * 100

        st.metric(
            "Similarity %",
            f"{similarity:.2f}%"
        )

    report = f"""
    DNA ANALYSIS REPORT

    Length: {len(sequence)}

    A: {A}
    T: {T}
    G: {G}
    C: {C}

    GC Content:
    {gc_content:.2f} %

    """

    st.download_button(
        label="Download Report",
        data=report,
        file_name="dna_report.txt",
        mime="text/plain"
    )

    #bilogical interpretation

    st.subheader("Interpretation")

    if gc_content > 60:

        st.success(
            "High GC content. DNA is generally more stable."
        )

    elif gc_content > 40:

        st.info(
            "Moderate GC content. Typical for many organisms."
        )

    else:

        st.warning(
            "Low GC content. DNA may be less thermally stable."
        )