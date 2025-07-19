# pages/10_CSV_Data_Upload.py

import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Robust CSV Data Upload", layout="centered")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem;
    }
    label, textarea, input, select {
        font-size: 0.95rem !important;
    }
    @media screen and (max-width: 600px) {
        h1, h2, h3 {
            font-size: 1.4rem !important;
        }
        button[kind="primary"] {
            font-size: 1rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("📑 Robust CSV Data Upload")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("CSV file uploaded successfully!")
        
        st.write("### Data Preview")
        st.dataframe(df.head(10))

        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()

        st.write("### CSV File Information")
        st.text(s)

        if st.button("Save CSV File"):
            file_path = f"./uploaded_csv/{uploaded_file.name}"
            df.to_csv(file_path, index=False)
            st.success(f"CSV file saved to: `{file_path}`")

    except pd.errors.ParserError as e:
        st.error(f"ParserError: {e}")
    except UnicodeDecodeError as e:
        st.error(f"UnicodeDecodeError: Ensure your file is UTF-8 encoded. Details: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
else:
    st.info("👆 Upload a CSV file to get started.")