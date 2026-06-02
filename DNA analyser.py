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