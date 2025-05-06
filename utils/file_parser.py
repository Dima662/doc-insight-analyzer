import fitz  # PyMuPDF
import docx
import tempfile

def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

def extract_text_from_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    doc = fitz.open(tmp_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_file(uploaded_file):
    if uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    else:
        return "Unsupported file type. Please upload a .docx or .pdf."
