import streamlit as st
import cohere
from pypdf import PdfReader



# 1. Text extraction function
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# 2. Cohere Client Initialization
co = cohere.Client(st.secrets["COHERE_API_KEY"])

# 3. Text Summarization function
def summarize_text(text, length="medium"):
    max_chars = 100000
    if len(text) > max_chars:
        text = text[:max_chars]
        
    prompt = f"""Summarize the following document in {length} form.
Give the summary in clear bullet points followed by a short conclusion.

Document:
{text}"""

    response = co.chat(
        model="command-r-plus-08-2024",
        message=prompt,
        temperature=0.3
    )
    return response.text

# 4. Streamlit UI Elements
st.title("PDF Summarizer App")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")


if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    
    if pdf_text.strip():
        st.success("Text extracted successfully!")
        
        with st.spinner("Generating summary..."):
            summary = summarize_text(pdf_text, length="medium")
        
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.error("Could not extract text from this PDF. Please check the file.")





