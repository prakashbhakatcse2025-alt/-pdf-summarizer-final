## 🤖 Smart PDF Assistant :

An AI-powered Streamlit web app that summarizes PDF documents and lets you *chat with them directly* — powered by [Cohere API](https://cohere.com/).

Upload any PDF, choose your preferred *summary length, tone, and language*, and get a clean, structured summary in seconds. Then ask follow-up questions and get answers grounded strictly in the document's content.

## ✨ Features

* 📄 PDF Text Extraction — reads and extracts text from any PDF using pypdf
* 📝 Smart Summarization — generate summaries in Short / Medium / Detailed length
* 🎭 Tone Control — choose Professional / Simple / Academic tone
* 🌐 Multi-language Output — get summaries in English or Hindi
* 💬 Ask Anything (Q&A) — chat with your PDF and get answers based only on its content
* 📊 Word Count & Reading Time — instantly see document stats after upload
* 📥 One-Click Download — save your generated summary as a .txt file
* 🎨 Custom UI Styling — clean, professional light blue/gray themed interface


## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io/) | Frontend/UI framework |
| [Cohere API](https://cohere.com/) (command-r-plus-08-2024) | Summarization & Q&A |
| [pypdf](https://pypi.org/project/pypdf/) | PDF text extraction |
| Streamlit Secrets | Secure API key management |
| Streamlit Community Cloud | Deployment |

## 📂 Project Structure

smart-pdf-assistant/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # Local API key (never pushed to GitHub)
└── .gitignore


## 🚀 Getting Started (Local Setup)
 # 1. Clone the repository
bash

git clone https://github.com/<your-username>/smart-pdf-assistant.git
cd smart-pdf-assistant

# 2. Create a virtual environment
bash

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux


# 3. Install dependencies
bash

pip install -r requirements.txt


# 4. Add your Cohere API key
Get a free API key from [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys), then create .streamlit/secrets.toml:
toml

COHERE_API_KEY = "your_api_key_here"


# 5. Run the app
bash

streamlit run app.py

The app will open at http://localhost:8501.


## ☁️ Deployment (Streamlit Community Cloud)

1. Push your code to GitHub (make sure secrets.toml is in .gitignore)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click *New app* → select your repo → set main file as app.py
4. In *App Settings → Secrets*, add:
   toml
   
   COHERE_API_KEY = "your_api_key_here"
   
6. Click *Deploy* — your app will be live at a public .streamlit.app URL

## 📋 Requirements
code-
streamlit
cohere
pypdf

## ⚠️ Known Limitations

* Free-tier Streamlit apps may "sleep" after inactivity — first load can take a few seconds
* Very large PDFs are truncated to the first ~100,000 characters before summarization
* Scanned/image-based PDFs are not yet supported (no OCR)

## 🔮 Future Improvements

* OCR support for scanned PDFs
* Persistent chat history across sessions
* Multi-PDF search and summarization
* Specialized modes (resume screening, medical report analysis)


## 📄 License

This project is open-source and available for personal and educational use.
