from flask import request, render_template
from PyPDF2 import PdfReader
import re
from app import app

keywords = ["SQL", "React"]

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def extract_emails(text):
    # Regular expression pattern for matching emails
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_pattern, text)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploaded_files = request.files.getlist("file[]")
        matching_resumes = []
        unmatched_resumes = []
        matching_emails = set()  # Using a set to avoid duplicate emails
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            if any(keyword.lower() in text.lower() for keyword in keywords):
                matching_resumes.append(file.filename)
                emails = extract_emails(text)
                matching_emails.update(emails)
            else:
                unmatched_resumes.append(file.filename)
        return render_template("result.html", resumes=matching_resumes, unmatched_resumes=unmatched_resumes, emails=matching_emails)
    return render_template("upload.html")
