import streamlit as st
from utils.file_parser import parse_file
from analyzers.summarizer import generate_summary
from analyzers.ner import extract_entities
from utils.highlighter import highlight_entities
from utils.report_generator import generate_report_docx
import io

st.set_page_config(page_title="Doc Insight Analyzer", layout="wide")
st.title("📄 Doc Insight Analyzer")
st.write("Upload a `.docx` or `.pdf` file to extract and summarize key information.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

if uploaded_file:
    model_choice = st.selectbox(
        "Choose summarization model:",
        options=["facebook/bart-large-cnn", "google/pegasus-xsum"],
        format_func=lambda x: "BART (Detailed)" if "bart" in x else "PEGASUS (Concise)"
    )

    with st.spinner("Reading document..."):
        text = parse_file(uploaded_file)

        MAX_WORDS = 1000
        if len(text.split()) > MAX_WORDS:
            st.warning(f"⚠️ Document too long. Please upload a file with under {MAX_WORDS} words.")
            st.stop()

        entities = extract_entities(text)
        highlighted_text = highlight_entities(text, entities)

        st.subheader("📄 Extracted Text (Entities Highlighted)")
        st.markdown(highlighted_text, unsafe_allow_html=True)

        with st.expander("🧠 Named Entities", expanded=False):
            for label, items in entities.items():
                st.markdown(f"**{label}**: {', '.join(items)}")

        if "summary" not in st.session_state:
            st.session_state.summary = None

        if st.button("🔍 Generate Summary"):
            with st.spinner("Summarizing..."):
                st.session_state.summary = generate_summary(text, model_choice)

        if st.session_state.summary:
            st.subheader("🧠 Summary")
            st.write(st.session_state.summary)

            st.subheader("📁 Downloadable Report")
            doc = generate_report_docx(st.session_state.summary, entities, text)
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            st.download_button("📥 Download Full Report (.docx)", data=buffer, file_name="doc_insight_report.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

            with st.expander("📊 Compare with Human Summary"):
                reference = st.text_area("Enter human-written summary here", key="ref_input")
                if st.button("Evaluate Summary Quality"):
                    from utils.evaluator import evaluate_summary
                    with st.spinner("Evaluating..."):
                        results = evaluate_summary(reference, st.session_state.summary)
                        for metric, score in results.items():
                            st.write(f"**{metric}**: {score:.4f}")
