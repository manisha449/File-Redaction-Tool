# 🔏 File Redaction Tool

A clean, frontend-backend separated Flask + Tailwind portfolio project to automatically redact personal information from PDFs and DOCX files.

## 🚀 Features

✅ Automatically redacts:
- Phone numbers
- Emails
- Aadhaar numbers
- SSN
- Salary mentions
- User-specified words (typed or spoken)

✅ Frontend:
- Tailwind CSS simple UI
- Speech-to-text input for additional words

✅ Backend:
- Flask API with CORS
- Uses PyMuPDF for PDFs, python-docx for DOCX
- Supports clean REST API POST /redact with file upload

---

## 📂 Project Structure

```
FileRedactionTool/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── index.html
├── uploads/
├── redacted/
└── README.md
```

---

## ⚡ Usage

### 1️⃣ Backend

```bash
cd FileRedactionTool/backend
pip install -r requirements.txt
python app.py
```

or using Docker:

```bash
docker build -t file-redaction-tool-backend .
docker run -p 5000:5000 file-redaction-tool-backend
```

---

### 2️⃣ Frontend

Open `FileRedactionTool/frontend/index.html` in your browser.

- Upload a `.pdf` or `.docx` file.
- Optionally type words to redact or use 🎤 Speak Words for speech-to-text entry.
- Click 📝 Upload & Redact.
- Download your redacted file automatically.

---

## 🩹 To Improve

- Add progress indicators on upload
- JWT authentication for production
- Additional test suite for backend routes

---

MIT License.
