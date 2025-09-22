import os
import fitz  # PyMuPDF
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import dotenv

# Load environment variables from a .env file
dotenv.load_dotenv()

app = Flask(__name__)
# Enable CORS for specific routes and origins
CORS(app, resources={r"/analyze": {"origins": "*"}, r"/chat": {"origins": "*"}})

# --- Gemini AI Model Configuration ---
try:
    # Configure the Gemini API with the key from environment variables
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=gemini_api_key)
    # Initialize the Generative Model
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error configuring Gemini API. Please set your GEMINI_API_KEY. Details: {e}")
    model = None

def extract_text_from_pdf(pdf_file_stream):
    """Extracts text content from a PDF file stream."""
    text_content = ""
    try:
        # Open the PDF from a byte stream
        with fitz.open(stream=pdf_file_stream.read(), filetype="pdf") as doc:
            for page in doc:
                text_content += page.get_text()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None
    return text_content

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """
    Receives a PDF file, extracts text, sends it to Gemini for analysis,
    and returns a structured JSON response with a 200 status code.
    """
    if not model:
        return jsonify({"error": "Gemini API is not configured"}), 200

    if 'pdf_file' not in request.files:
        return jsonify({"error": "No PDF file provided"}), 200

    file = request.files['pdf_file']

    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Invalid file. Please upload a PDF."}), 200

    document_text = extract_text_from_pdf(file.stream)
    if not document_text:
        return jsonify({"error": "Could not extract text from the PDF."}), 200

    prompt = f"""
    As a legal analysis AI, your task is to analyze the following legal document and provide a structured summary. The target audience is a non-lawyer, so use clear and simple language.
    Analyze the document from the perspective of the party who is signing it, not the one who wrote it.
    Based on the text below, generate a JSON object with the following three keys: "summary", "risks_benefits", and "key_clauses".

    1.  "summary": A concise, one-paragraph summary of the document's purpose and key terms.
    2.  "risks_benefits": An array of objects. Each object must have two keys: "type" (either "risk" or "benefit") and "text" (a description of that risk or benefit). Identify at least two risks and two benefits.
    3.  "key_clauses": An array of objects. Each object must have two keys: "term" (the name of the clause, e.g., "Termination Clause") and "definition" (a simple explanation of what the clause means for the signing party). Identify at least three critical clauses.

    Do not include any introductory text, explanations, or markdown formatting like ```json before or after the JSON object.

    Document Text:
    ---
    {document_text}
    ---
    """

    try:
        response = model.generate_content(prompt)
        # Clean up the response to ensure it's valid JSON
        cleaned_response_text = response.text.strip().replace('```json', '').replace('```', '')
        
        print("--- Gemini Raw Response ---")
        print(cleaned_response_text)
        print("--------------------------")
        
        analysis_result = json.loads(cleaned_response_text)
        
        return jsonify(analysis_result), 200

    except Exception as e:
        print(f"!!! An error occurred: {e} !!!")
        return jsonify({"error": "Failed to analyze the document with the AI model."}), 200

@app.route('/chat', methods=['POST'])
def chat_with_document():
    """
    Receives a user's question and document text, gets an answer from Gemini,
    and returns the response with a 200 status code.
    """
    if not model:
        return jsonify({"error": "Gemini API is not configured"}), 200

    data = request.get_json()
    if not data or 'question' not in data or 'document_text' not in data:
        return jsonify({"error": "Missing question or document text"}), 200

    question = data['question']
    document_text = data['document_text']

    prompt = f"""
    You are a helpful legal assistant. A user has uploaded a legal document and is now asking a specific question about it.
    Based *only* on the provided document text, answer the user's question in a clear and concise way.
    If the answer cannot be found in the document, state that the document does not contain that information.

    Document Text:
    ---
    {document_text}
    ---

    User's Question:
    "{question}"
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text}), 200
    except Exception as e:
        print(f"!!! Chat error: {e} !!!")
        return jsonify({"error": "Failed to get a response from the AI model."}), 200

@app.route("/health")
def health_check():
    """A simple endpoint for uptime monitoring."""
    return jsonify(status="ok"), 200

if __name__ == '__main__':
    # Use the PORT environment variable if available, otherwise default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
