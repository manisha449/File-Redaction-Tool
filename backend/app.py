from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
from docx import Document
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "../uploads"
REDACTED_FOLDER = "../redacted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REDACTED_FOLDER, exist_ok=True)

patterns = [
    (r"\b\d{10}\b", "[REDACTED PHONE]"),
    (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED EMAIL]"),
    (r"\b\d{4} \d{4} \d{4}\b", "[REDACTED AADHAAR]"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED SSN]"),
    (r"\bSalary\b", "[REDACTED SALARY]", re.IGNORECASE),
]

def redact_pdf(file_path, extra_words):
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text()
        for pattern in patterns:
            regex = re.compile(pattern[0], pattern[2] if len(pattern) > 2 else 0)
            for match in regex.finditer(text):
                rects = page.search_for(match.group())
                for rect in rects:
                    page.add_redact_annot(rect, fill=(0, 0, 0))
        for word in extra_words:
            word = word.strip()
            if word:
                rects = page.search_for(word)
                for rect in rects:
                    page.add_redact_annot(rect, fill=(0, 0, 0))
        page.apply_redactions()
    output_pdf = os.path.join(REDACTED_FOLDER, "redacted.pdf")
    doc.save(output_pdf)
    return output_pdf

def redact_docx(file_path, extra_words):
    doc = Document(file_path)
    for p in doc.paragraphs:
        for pattern in patterns:
            regex = re.compile(pattern[0], pattern[2] if len(pattern) > 2 else 0)
            p.text = regex.sub(pattern[1], p.text)
        for word in extra_words:
            word = word.strip()
            if word:
                p.text = p.text.replace(word, "[REDACTED]")
    output_docx = os.path.join(REDACTED_FOLDER, "redacted.docx")
    doc.save(output_docx)
    return output_docx

@app.route("/redact", methods=["POST"])
def redact():
    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400
    file = request.files["file"]
    extra_words_input = request.form.get("redact_words", "")
    extra_words = [w.strip() for w in extra_words_input.split(",")] if extra_words_input else []
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)
    if file.filename.lower().endswith(".pdf"):
        redacted_file = redact_pdf(file_path, extra_words)
    elif file.filename.lower().endswith(".docx"):
        redacted_file = redact_docx(file_path, extra_words)
    else:
        return jsonify({"error": "Unsupported file type."}), 400
    return send_file(redacted_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
