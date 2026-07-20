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

# 3. Text Summarization function with Tone
def summarize_text(text, length, language, tone):
    max_chars = 100000
    if len(text) > max_chars:
        text = text[:max_chars]
        
    prompt = f"""Summarize the following document in {length} form.
The tone of the summary should be strictly {tone}.
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

# 4. Streamlit UI Elements & Configuration
st.set_page_config(page_title="Ultimate AI PDF Assistant", page_icon="🤖", layout="wide")

# Injecting Custom Professional Custom CSS Styling 🎨
st.markdown("""
    <style>
        /* Main Page Background and Text Color */
        .stApp {
            background-color: #F8F9FA;
            color: #212529;
        }
        
        /* Main Headers Styling */
        h1 {
            color: #1E3A8A !important; /* Deep Professional Blue */
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-weight: 700;
        }
        
        h3 {
            color: #0F172A !important; /* Slate Blue */
            font-weight: 600;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0F172A !important; /* Dark Elegant Slate */
        }
        [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
            color: #E2E8F0 !important; /* Crisp Light Text for Sidebar Labels */
        }
        
        /* Custom Styling for Information Cards */
        .stAlert {
            background-color: #FFFFFF !important;
            border-left: 5px solid #2563EB !important; /* Indigo Blue Border Accent */
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        
        /* Primary Buttons Customization */
        div.stButton > button:first-child {
            background-color: #2563EB !important;
            color: white !important;
            border-radius: 6px;
            border: none;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #1D4ED8 !important; /* Hover effect: Darker Blue */
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Ultimate AI PDF Assistant")
st.write("Upload your PDF, generate smart summaries, and chat with your document!")

# Sidebar Settings
st.sidebar.header("⚙️ App Settings")
summary_lang = st.sidebar.selectbox("Summary Language:", ["English", "Hindi"])
summary_len = st.sidebar.radio("Summary Length:", ["Short", "Medium", "Detailed"])
summary_tone = st.sidebar.selectbox("Summary Tone:", ["Professional", "Simple/Easy", "Detailed/Academic"])

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Session state to store text and summary so they don't disappear during chat
    if "pdf_text" not in st.session_state:
        with st.spinner("Extracting text from PDF..."):
            st.session_state.pdf_text = extract_text_from_pdf(uploaded_file)
            
    pdf_text = st.session_state.pdf_text

    if pdf_text.strip():
        # Quick Stats Panel
        words = len(pdf_text.split())
        reading_time = max(1, round(words / 200))
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📊 *Word Count:* {words} words")
        with col2:
            st.info(f"⏱️ *Reading Time:* ~{reading_time} min")

        # Action Buttons
        if st.button("Generate Summary ✨"):
            with st.spinner("AI is generating your summary..."):
                st.session_state.summary = summarize_text(pdf_text, length=summary_len, language=summary_lang, tone=summary_tone)

        # Display Summary if generated
        if "summary" in st.session_state:
            st.subheader("📋 Your Summary:")
            st.write(st.session_state.summary)
            
            st.download_button(
                label="📥 Download Summary",
                data=st.session_state.summary,
                file_name="pdf_summary.txt",
                mime="text/plain"
            )
            
            st.markdown("---")
            
            # CHAT WITH PDF FEATURE 💬
            st.subheader("💬 Ask Anything about this PDF:")
            user_question = st.text_input("Type your question here:")
            
            if user_question:
                with st.spinner("AI is searching for the answer..."):
                    chat_prompt = f"You are an AI assistant. Answer the user's question based strictly on this document text.\n\nDocument:\n{pdf_text}\n\nQuestion: {user_question}"
                    chat_response = co.chat(
                        model="command-r-plus-08-2024",
                        message=chat_prompt,
                        temperature=0.4
                    )
                    st.write("🤖 *AI Answer:*")
                    st.success(chat_response.text)
    else:
        st.error("Could not extract text from this PDF. Please try another file.")
