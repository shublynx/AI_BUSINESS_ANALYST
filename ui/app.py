import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Business Analyst", layout="wide")
st.title("📊 AI Business Analyst")

st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

# Only show button if file is selected
if uploaded_file:
    st.sidebar.success(f"Selected file: {uploaded_file.name}")

    if st.sidebar.button("Upload & Process"):
        with st.spinner("Uploading dataset..."):
            files = {
                "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
            }

            try:
                response = requests.post(
                    f"{API_BASE_URL}/datasets/upload",
                    files=files,
                    timeout=30,
                )

                if response.status_code == 201:
                    data = response.json()
                    st.success("Dataset uploaded successfully ✅")
                    st.json(data)

                else:
                    st.error(f"Upload failed ❌ (Status: {response.status_code})")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
