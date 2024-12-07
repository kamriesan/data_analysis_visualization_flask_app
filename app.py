import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import base64

# Set Streamlit page configuration
st.set_page_config(
    page_title="DataGenie AI",
    page_icon="assets/icon.png",  # Path to your logo
    layout="wide"
)

# Load custom CSS from the external file
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to encode an image as Base64 for fast loading
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Display full-screen loading screen with a background image
placeholder = st.empty()  # Create a placeholder
bg_image_base64 = get_base64_image("assets/splash-screen-bg.png")  # Path to the splash background image

with placeholder.container():
    st.markdown(
        f"""
        <div style="
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background-image: url(data:image/png;base64,{bg_image_base64}); 
            background-size: cover; background-position: center; z-index: 9999; 
            display: flex; justify-content: center; align-items: center; 
            animation: fadeOut 4s ease-in-out forwards;">
            <div style="
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                width: 100vw; 
                color:white;
                ">
                <h1 style="color: white; font-family: 'Poppins', sans-serif; font-size: 3rem; text-align: center;">
                    DataGenie AI
                </h1>
            </div>
        </div>
        <style>
        @keyframes fadeOut {{
            0% {{ opacity: 1; }}
            100% {{ opacity: 0; visibility: hidden; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(2)  # Show the loading screen for 2 seconds
placeholder.empty()

# Load environment variables
load_dotenv()

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Function to convert a plotly figure to binary data
def fig_to_pil(fig):
    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    return Image.open(buf)

# Function to get response from Gemini AI API
def get_gemini_response(input_text, image):
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
        return f"Error in generating response: {e}"

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

# Sidebar content
st.sidebar.title("Data Genie")

# Initialize session state variables
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "Visualize Data"
if "generated_charts" not in st.session_state:
    st.session_state.generated_charts = []
if "chart_displayed" not in st.session_state:
    st.session_state.chart_displayed = False  # Ensure only one chart is displayed

# Header with logo and title
logo_path = "assets/icon.png"  # Replace with the path to your logo
col1, col2 = st.columns([1, 10])  # Adjust the ratio for proper alignment
with col1:
    st.image(logo_path, use_container_width=True)  # Display the logo
with col2:
    st.title("DataGenie AI")

# Subheader with text only
st.subheader("Upload any CSV file to explore the data dynamically!")

# Main content logic
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

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

    column_options = df.columns.tolist()

    x_axis = st.selectbox("X-axis column:", options=column_options)
    y_axis = st.selectbox("Y-axis column:", options=column_options)
    chart_type = st.selectbox(
        "Chart type:", 
        ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Tree Map"]
    )

    if st.button("Generate Visualization"):
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
            st.session_state.generated_charts = [{"chart": chart}]  # Update with only the latest chart
            st.session_state.chart_displayed = True  # Mark the chart as displayed

# Display the latest chart only when not already displayed
if st.session_state.chart_displayed:
    last_chart = st.session_state.generated_charts[-1]  # Get the last chart
    st.plotly_chart(last_chart["chart"], key="unique_chart")  # Display the chart once

    if st.button("Visualizer AI"):
        st.session_state.chart_displayed = False  # Hide the chart after AI analysis
        with st.spinner("Analyzing the chart... Please wait.") as spinner:
            time.sleep(1)  # Simulate delay (can be removed)
            response = get_gemini_response("Analyze this chart", fig_to_pil(last_chart["chart"]))
        
        st.subheader("AI Insights:")
        st.write(response)
