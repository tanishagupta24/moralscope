import streamlit as st
from ethics_engine import get_moral_judgment
from memory import MoralMemory
from philosophy_loader import extract_text_from_pdf
from vector_store import chunk_text, build_faiss_index

st.set_page_config(page_title="MoralScope", page_icon="📖")
st.title("📖 MoralScope: Autonomous Moral Philosophy Explorer")

# Initialize moral memory
memory = MoralMemory()

# Input form
with st.form("dilemma_form"):
    dilemma = st.text_area("Enter a moral dilemma:")
    frameworks = st.multiselect(
        "Choose one or more ethical frameworks to compare:",
        [
            "Utilitarianism",
            "Deontology",
            "Virtue Ethics",
            "Care Ethics",
            "Moral Relativism",
            "Contractualism",
            "Divine Command Theory"
        ],
        default=["Utilitarianism", "Deontology"]
    )
    submitted = st.form_submit_button("Analyze")

if submitted and dilemma and frameworks:
    tabs = st.tabs([f"{fw}" for fw in frameworks])

    for i, fw in enumerate(frameworks):
        with tabs[i]:
            judgment, justification = get_moral_judgment(dilemma, fw)
            memory.store_judgment(dilemma, fw, judgment, justification)

            st.subheader("Judgment")
            st.write(judgment)

            st.subheader("Justification")
            st.write(justification)

st.sidebar.subheader("Upload Philosophy PDFs")
uploaded_files = st.sidebar.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)

philosophy_corpus = ""

if uploaded_files:
    for uploaded_file in uploaded_files:
        text = extract_text_from_pdf(uploaded_file)
        philosophy_corpus += f"\n\n--- FROM: {uploaded_file.name} ---\n\n{text}"

if philosophy_corpus:
    chunks = chunk_text(philosophy_corpus)
    index, chunk_sources = build_faiss_index(chunks)
else:
    index, chunk_sources = None, []
