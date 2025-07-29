import streamlit as st
import requests

st.title("🧠 OCR + LLM Question Answering")

# Upload
st.subheader("Upload PDF or Image")
uploaded_file = st.file_uploader("Upload", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    st.info("Processing file. Please wait...")
    res = requests.post("http://localhost:8001/upload/", files={"file": uploaded_file})
    if res.status_code == 200:
        st.success("File processed successfully!")
    else:
        st.error(res.json()["error"])

# Ask Question
st.subheader("Ask a Question")
question = st.text_input("Your Question")

if st.button("Get Answer") and question:
    res = requests.post("http://localhost:8001/ask/", data={"question": question})
    if res.status_code == 200:
        st.markdown(f"**Answer:** {res.json()['answer']}")
    else:
        st.error(res.json()["error"])
