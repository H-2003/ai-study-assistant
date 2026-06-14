import pypdf

def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = pypdf.PdfReader(uploaded_file)
    for page in reader.pages:
        text += page.extract_text()
    return text.strip()
