import pandas as pd
import streamlit as st

def upload_csv():
    st.subheader("Upload CSV File")
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv", key="upload_csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = df.convert_dtypes()
        df, cleaning_report = clean_data(df)

        if cleaning_report:
            st.success("Data cleaning report:")
            for report in cleaning_report:
                st.text(report)
        else:
            st.info("No cleaning necessary; data was already clean.")

        st.dataframe(df)
        return df
    return None

def clean_data(df):
    cleaning_report = []
    df.drop_duplicates(inplace=True)
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            df.dropna(subset=[col], inplace=True)
            cleaning_report.append(f"Removed {missing_count} missing values from column '{col}'.")
    return df, cleaning_report
