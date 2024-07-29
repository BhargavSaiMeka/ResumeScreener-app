import streamlit as st
from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_pattern, text)

st.title('📄 Resume Screening')

st.markdown('''
    This application helps you filter resumes based on specific keywords.
    Simply upload the resumes and enter the keywords to get started.
''')

keywords = st.text_input('**Enter Keywords (comma-separated):**')

uploaded_files = st.file_uploader('**Upload Resumes**', accept_multiple_files=True, type=['pdf'])

if st.button('Upload'):
    if uploaded_files and keywords:
        keywords_list = [keyword.strip() for keyword in keywords.split(',')]
        matching_resumes = []
        unmatched_resumes = []
        matching_emails = set()

        progress_bar = st.progress(0)
        total_files = len(uploaded_files)

        for i, file in enumerate(uploaded_files):
            text = extract_text_from_pdf(file)
            if any(keyword.lower() in text.lower() for keyword in keywords_list):
                matching_resumes.append(file.name)
                emails = extract_emails(text)
                matching_emails.update(emails)
            else:
                unmatched_resumes.append(file.name)
            progress_bar.progress((i + 1) / total_files)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader('✅ Matched Resumes')
            if matching_resumes:
                for resume in matching_resumes:
                    st.write(f"• {resume}")
            else:
                st.write("No matched resumes")

        with col2:
            st.subheader('❌ Unmatched Resumes')
            if unmatched_resumes:
                for resume in unmatched_resumes:
                    st.write(f"• {resume}")
            else:
                st.write("No unmatched resumes")

        with col3:
            st.subheader('📧 Emails From Matched Resumes')
            if matching_emails:
                for email in matching_emails:
                    st.write(f"• {email}")
            else:
                st.write("No emails found")

    else:
        st.warning('⚠️ Please upload files and enter keywords.')
