import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time

# Load environment variables from .env
st.write("Debug: Loading environment variables...")
load_dotenv()

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Debug: GOOGLE_API_KEY is missing! Check your .env file or Streamlit secrets.")
else:
    st.write("Debug: API key loaded successfully.")
    genai.configure(api_key=api_key)

# Function to convert a plotly figure to binary data
def fig_to_pil(fig):
    st.write("Debug: Converting figure to PIL image...")
    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    return Image.open(buf)

# Function to get response from Gemini AI API
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    if input_text and image:
        response = model.generate_content([input_text, image])
    elif input_text:
        response = model.generate_content([input_text])
    else:
        response = None
    return response.text if response else "No response available."
    st.write("Debug: Calling Gemini AI API...")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Use the correct model ID
        if input_text and image:
            response = model.generate_content([input_text, image])
        elif input_text:
            response = model.generate_content([input_text])
        else:
            response = None
        return response.text if response else "No response available."
    except Exception as e:
        st.error(f"Debug: Error in calling Gemini AI API - {e}")
        return "Error in generating response."

# Function to clean data with detailed reporting
def clean_data(df):
    cleaning_report = []
    original_shape = df.shape
    
    # Remove duplicates
    df_before = df.copy()
    df.drop_duplicates(inplace=True)
    if df.shape[0] < df_before.shape[0]:
        cleaning_report.append(f"Removed {df_before.shape[0] - df.shape[0]} duplicate rows.")

    # Handle missing values with detailed reporting
    for col in df.columns:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            df_missing = df[df[col].isnull()]
            for index, row in df_missing.iterrows():
                cleaning_report.append(f"Line {index + 1} in header '{col}' has no value: removed the line.")
            df.dropna(subset=[col], inplace=True)  # Removing rows with NaN in specific column

    return df, cleaning_report

# Set Streamlit page configuration
st.write("Debug: Setting Streamlit page configuration...")
st.set_page_config(
    page_title="DataGenie AI",
    page_icon="icon.png",  # Path to your new logo
    layout="wide"
)

# Sidebar content
st.sidebar.title("Data Genie")
st.write("Debug: Sidebar initialized.")

# Initialize session state
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "Visualize Data"
    st.write("Debug: Session state 'active_menu' initialized.")
if "generated_charts" not in st.session_state:
    st.session_state.generated_charts = []
    st.write("Debug: Session state 'generated_charts' initialized.")

# Main content logic
st.write("Debug: Rendering main content...")
st.header("DataGenie AI")
st.subheader("Upload any CSV file to explore the data dynamically!")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
st.write("Debug: File uploader rendered.")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Convert data types of all columns to more appropriate types
    df = df.convert_dtypes()
    # Clean data
    df, cleaning_report = clean_data(df)
    
    if cleaning_report:
        st.success("Data cleaning report:")
        for report in cleaning_report:
            st.text(report)
    else:
        st.info("No cleaning necessary; data was already clean.")
    
    st.dataframe(df)
    st.write("Debug: File uploaded, reading CSV...")
    try:
        df = pd.read_csv(uploaded_file)
        st.success("CSV file uploaded successfully!")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Debug: Error reading CSV file - {e}")

    column_options = df.columns.tolist()
    st.write("Debug: Columns loaded from CSV file:", column_options)
    
    x_axis = st.selectbox("X-axis column:", options=column_options)
    st.write(f"Debug: X-axis selected: {x_axis}")
    
    y_axis = st.selectbox("Y-axis column:", options=column_options)
    st.write(f"Debug: Y-axis selected: {y_axis}")
    
    chart_type = st.selectbox(
        "Chart type:", 
        ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Tree Map"]
    )
    st.write(f"Debug: Chart type selected: {chart_type}")

    if st.button("Generate Visualization"):
        st.write("Debug: Generate Visualization button clicked.")
        chart = None
        if chart_type == "Bar Chart":
            chart = px.bar(df, x=x_axis, y=y_axis)
        elif chart_type == "Line Chart":
            chart = px.line(df, x=x_axis, y=y_axis)
        elif chart_type == "Scatter Plot":
            chart = px.scatter(df, x=x_axis, y=y_axis)
        elif chart_type == "Pie Chart":
            chart = px.pie(df, names=x_axis, values=y_axis)
        elif chart_type == "Tree Map":
            chart = px.treemap(df, path=[x_axis], values=y_axis)

        if chart:
            st.write("Debug: Chart generated successfully.")
            st.plotly_chart(chart)
            pil_image = fig_to_pil(chart)
            # Save the last generated chart
            st.session_state.generated_charts.append({"chart": chart, "image": pil_image})
            st.write("Debug: Chart saved to session state.")

# Use the last generated chart for AI analysis
if st.session_state.generated_charts:
    st.write("Debug: Found generated charts in session state.")
    last_chart = st.session_state.generated_charts[-1]  # Get the last chart
    if st.button("Visualizer AI"):
        st.write("Debug: Visualizer AI button clicked.")
        st.image(last_chart["image"], caption="Last Generated Chart", use_container_width=True)

        # Display a loading spinner while generating the AI response
        with st.spinner("Analyzing the chart... Please wait."):
            time.sleep(2)  # Simulate delay (can be removed)
            response = get_gemini_response("Analyze this chart", last_chart["image"])
        
        st.subheader("AI Insights:")
        st.write(response)
