import streamlit as st
from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages))):
        text += reader.pages[page_num].extract_text()
    return text

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_pattern, text)

st.title('Resume Filtering')

keywords = st.text_input('Enter Keywords (comma-separated):')

uploaded_files = st.file_uploader('Upload Resumes', accept_multiple_files=True)

if st.button('Upload'):
    if uploaded_files and keywords:
        keywords_list = [keyword.strip() for keyword in keywords.split(',')]
        matching_resumes = []
        unmatched_resumes = []
        matching_emails = set()

        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            if any(keyword.lower() in text.lower() for keyword in keywords_list):
                matching_resumes.append(file.name)
                emails = extract_emails(text)
                matching_emails.update(emails)
            else:
                unmatched_resumes.append(file.name)

        st.subheader('Matched Resumes')
        for resume in matching_resumes:
            st.write(resume)

        st.subheader('Unmatched Resumes')
        for resume in unmatched_resumes:
            st.write(resume)

        st.subheader('Emails From Matched Resumes')
        for email in matching_emails:
            st.write(email)
    else:
        st.warning('Please upload files and enter keywords.')
