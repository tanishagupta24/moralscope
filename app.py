import streamlit as st
from ethics_engine import get_moral_judgment
from memory import MoralMemory

st.set_page_config(page_title="MoralScope", page_icon="🧠")
st.title("🧠 MoralScope: Autonomous Moral Philosophy Explorer")

# Initialize moral memory
memory = MoralMemory()

# Input form
with st.form("dilemma_form"):
    dilemma = st.text_area("Enter a moral dilemma:")
    framework = st.selectbox("Choose ethical framework:", ["Utilitarianism", "Deontology", "Virtue Ethics"])
    submitted = st.form_submit_button("Analyze")

# Handle form submission
if submitted and dilemma:
    judgment, justification = get_moral_judgment(dilemma, framework)
    memory.store_judgment(dilemma, framework, judgment, justification)

    st.subheader("🧾 Judgment:")
    st.write(judgment)

    st.subheader("📚 Justification:")
    st.write(justification)

    st.subheader("🧠 Memory (Past dilemmas):")
    for item in memory.past_judgments:
        st.markdown(f"- **{item['framework']}** on *{item['dilemma'][:60]}...*: {item['judgment']}")
