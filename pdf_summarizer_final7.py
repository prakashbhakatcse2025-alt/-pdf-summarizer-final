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

# 3. Text Summarization function (Ab isme language aur length dono user ke hisab se badlenge)
def summarize_text(text, length, language):
    max_chars = 100000
    if len(text) > max_chars:
        text = text[:max_chars]
        
    prompt = f"""Summarize the following document in {length} form.
Give the final summary strictly in {language} language.
Use clear bullet points followed by a short conclusion.

Document:
{text}"""

    response = co.chat(
        model="command-r-plus-08-2024",
        message=prompt,
        temperature=0.3
    )
    return response.text

# 4. Streamlit UI Elements
st.set_page_config(page_title="AI PDF Summarizer", page_icon="📄")
st.title("📄 Smart AI PDF Summarizer")
st.write("Upload your PDF and get a summary in your preferred language!")

# Sidebar me settings daal dete hain taaki screen saaf dikhe
st.sidebar.header("⚙️ Settings")
summary_lang = st.sidebar.selectbox("Select the summary language:", ["English", "Hindi"])
summary_len = st.sidebar.radio("Summary ki Length chune:", ["Short", "Medium", "Detailed"])

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Agar user file upload karega, tabhi ye chalega
if uploaded_file is not None:
    with st.spinner("PDF se text nikala ja raha hai..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    
    if pdf_text.strip():
        st.success("PDF successfully read ho gayi!")
        
        # Summary generate karne ka button
        if st.button("Generate Summary ✨"):
            with st.spinner(f"Cohere AI aapki {summary_len} summary {summary_lang} me bana raha hai..."):
                summary = summarize_text(pdf_text, length=summary_len, language=summary_lang)
            
            st.subheader("📋 Aapki Summary:")
            st.write(summary)
            
            # Download Button feature
            st.download_button(
                label="📥 Summary Download Karein",
                data=summary,
                file_name="pdf_summary.txt",
                mime="text/plain"
            )
    else:
        st.error("Is PDF se text nahi nikal paya. Kripya doosri file try karein.")
