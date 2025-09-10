# Un-Law ⚖️ - AI Legal Document Analyzer ([text](https://un-law-1.onrender.com/))

Un-Law is a web application designed to demystify complex legal documents. Powered by Google's Gemini API, this tool provides clear, concise, and actionable insights from dense legal texts, empowering individuals to understand contracts, agreements, and terms of service before they sign.

---

## ✨ Key Features

- 📄 **PDF Document Upload**: Easily upload any legal document in PDF format for analysis.
- 🧠 **Instant AI Analysis**: Get an immediate breakdown of your document, including:
  - A plain-English summary.
  - A risk and benefit analysis from your perspective.
  - An explanation of the most critical clauses.
- 📊 **Interactive Dashboard**: A sleek, modern interface with a resizable, two-column layout to view the original document and its analysis side-by-side.
- 📥 **One-Click PDF Reports**: Download a professionally formatted, 1-2 page PDF of the complete analysis for your records.

---

## 🚀 How It Works

1. **Upload**: The user uploads a legal document in PDF format via a clean, simple interface.
2. **Analyze**: The frontend sends the document to a Python Flask backend. The backend extracts the text and sends it to the Gemini API with a specialized prompt to analyze it.
3. **Display**: The structured analysis (summary, risks, clauses) is returned to the frontend and displayed in an interactive dashboard. The user can view the original PDF and the AI's insights simultaneously.
4. **Interact & Download**: The user can ask follow-up questions or download the complete analysis as a high-quality PDF report.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Backend**: Python 3, Flask
- **AI Model**: Google Gemini API
- **PDF Handling**: PyPDF2 (Backend), pdf.js & jsPDF (Frontend)

---

## ⚙️ Local Setup & Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- A Google Gemini API Key

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/un-law.git
   cd un-law
   ```

2. **Backend Setup**
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Set your Gemini API Key as an environment variable.
     - macOS / Linux:
       ```bash
       export GEMINI_API_KEY="YOUR_API_KEY"
       ```
     - Windows (Command Prompt):
       ```bash
       set GEMINI_API_KEY="YOUR_API_KEY"
       ```
   - Run the Flask backend server:
     ```bash
     python main.py
     ```
     > This will run on http://127.0.0.1:5000

3. **Frontend Setup**
   - Open a new terminal window.
   - Navigate to the project directory where `index.html` is located.
   - Start a simple local web server:
     ```bash
     python -m http.server 8000
     ```
     > This will run on http://localhost:8000

4. **Access the Application**
   Open your browser and navigate to:  
   👉 http://localhost:8000

---

## 📂 Project Structure

```
.
├── 📄 main.py          # Flask Backend Server
├── 📄 index.html       # Frontend Application
├── 📄 requirements.txt # Python Dependencies
└── 📄 README.md        # You are here!
```

---

## 🔮 Future Improvements

- Support for more document types (e.g., .docx, .txt)
- Multi-language analysis and translation
- User accounts to save and manage document history
- Integration with cloud storage providers (Google Drive, Dropbox)

---


