import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Business Analyst", layout="wide")

st.title("📊 AI Business Analyst")

# -----------------------------------------
# SESSION STATE INIT
# -----------------------------------------
if "dataset_id" not in st.session_state:
    st.session_state.dataset_id = None

# -----------------------------------------
# SIDEBAR: FILE UPLOAD
# -----------------------------------------
st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    st.sidebar.info(f"Selected file: {uploaded_file.name}")

    # Upload button
    if st.sidebar.button("Upload to Server"):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(
            f"{API_BASE_URL}/datasets/upload",
            files=files
        )

        if response.status_code == 201:
            data = response.json()
            st.session_state.dataset_id = data["dataset_id"]
            st.sidebar.success("Dataset uploaded successfully!")

            st.sidebar.write("📌 Dataset ID:")
            st.sidebar.code(st.session_state.dataset_id)

            st.sidebar.write("Backend Response:")
            st.sidebar.json(data)
        else:
            st.sidebar.error("Upload failed")
            st.sidebar.json(response.json())

# -----------------------------------------
# MAIN: SHOW ACTIVE DATASET
# -----------------------------------------
st.subheader("Active Dataset")

if st.session_state.dataset_id:
    st.success(f"Using dataset: {st.session_state.dataset_id}")
else:
    st.warning("No dataset uploaded yet.")

# -----------------------------------------
# MAIN: ASK QUESTION
# -----------------------------------------
st.subheader("Ask a Question")

question = st.text_input("Enter your question")

if st.button("Submit Question"):
    if not st.session_state.dataset_id:
        st.error("Upload a dataset first.")
    else:
        params = {
            "question": question
        }

        response = requests.post(
            f"{API_BASE_URL}/query/{st.session_state.dataset_id}",
            params=params
        )

        st.write("🔍 Raw API Status:", response.status_code)

        try:
            result = response.json()
            st.write("📦 Raw API Response:")
            st.json(result)

            if response.status_code == 200:
                st.success(result["answer"])
            else:
                st.error(result)

        except Exception:
            st.error("Could not decode response")
