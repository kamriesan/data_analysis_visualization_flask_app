import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import base64
from streamlit_extras.stylable_container import stylable_container


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

# Add app-bg.png as the background to the entire page
bg_image_base64 = get_base64_image("assets/app-bg.png")
st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_image_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)



# Function to encode an image as Base64 for fast loading
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Initialize session state for splash screen
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False  # Default value: splash screen not yet shown

#❌ # Display splash screen only once
# if not st.session_state.splash_shown:
#     placeholder = st.empty()  # Create a placeholder
#     bg_image_base64 = get_base64_image("assets/splash-screen-bg.png")  # Encode splash image

#     with placeholder.container():
#         st.markdown(
#             f"""
#             <div style="
#                 position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
#                 background-image: url(data:image/png;base64,{bg_image_base64}); 
#                 background-size: cover; background-position: center; z-index: 9999; 
#                 display: flex; justify-content: center; align-items: center; 
#                 animation: fadeOut 1s ease-in-out forwards;"> 
#                 <div style="
#                     display: flex; 
#                     justify-content: center; 
#                     align-items: center; 
#                     height: 100vh; 
#                     width: 100vw; 
#                     color:white;
#                     ">
#                     <h1 style="color: white; font-family: 'Poppins', sans-serif; font-size: 3rem; text-align: center;">
#                         DataGenie AI App
#                     </h1>
#                 </div>
#             </div>
#             <style>
#             @keyframes fadeOut {{
#                 0% {{ opacity: 1; }}
#                 100% {{ opacity: 0; visibility: hidden; }}
#             }}
#             </style>
#             """,
#             unsafe_allow_html=True,
#         )
#         time.sleep(4)  # Show the splash screen for 2 seconds
#     placeholder.empty()

#     # Mark splash screen as shown
#❌     st.session_state.splash_shown = True

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


# Initialize session state variables
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "Visualize Data"
if "generated_charts" not in st.session_state:
    st.session_state.generated_charts = []
if "chart_displayed" not in st.session_state:
    st.session_state.chart_displayed = False  # Ensure only one chart is displayed

# STYLES
st.markdown(
    """
    <div style='text-align: center;'>
        <h1 style='font-family: "Poppins", sans-serif; color: white; margin-top: -30px;'>
            🔮 DATAGENIE AI
        </h1>
        <h5 style='font-family: "Poppins", sans-serif; color: #BBBBBB; margin-top: -10px;'>
            Transform Your Data into Powerful Visualizations & AI Insights!
        </h5>
    </div>

    <style>
    /* Target the file uploader */
    div[data-testid="stFileUploader"] {
        border-radius: 10px; /* Rounded corners */
        background-color: white; /* Dark grey background */
        padding: 40px; /* Internal padding */
        color: #333333; /* Text color */
        font-size: 16px; /* Font size */
        width: 85%;
        margin: auto; /* Center align */
    }

    /* Target the horizontal block */
    div[data-testid="stHorizontalBlock"] {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        background-color: white;
        border-radius: 10px;
        padding: 40px;
        color: white;
        width: 85%;
        margin: auto;
    }
    div[data-testid="stSelectbox"] > div > input {
        font-size: 16px;
        padding: 8px;
        border: 1px solid #cccccc;
        border-radius: 5px;
    }
    div.stButton > button {
        background-color: #FF5152; /* Violet background */
        color: white; /* White text */
        border-radius: 10px; /* Rounded corners */
        padding: 10px 20px; /* Padding */
        font-size: 16px; /* Font size */
        font-weight: bold; /* Bold text */
        border: none; /* Remove border */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add shadow */
        cursor: pointer; /* Pointer cursor on hover */
    }
    div.stButton > button:hover {
        background-color: #E9292A; /* Darker violet on hover */
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# Main content logic

uploaded_file = st.file_uploader("Is your data ready for enchantment? 🧚‍♀️ Upload your CSV now! 📩", type="csv")


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df.convert_dtypes()
    df, cleaning_report = clean_data(df)

    # Create two columns with equal width
    # Create two columns with equal width
    col1, col2 = st.columns(2)

    # Display the data frame in the left column
    with col1:
        st.markdown(
            """
            <h3 style='color: #333333;  font-size: 24px; font-weight: bold;'>
                👀 Data Previews
            </h3>
            <h6 style='font-family: "Poppins", sans-serif; font-size: 12px; color: #333333; margin-top: -10px;'>
            Hover over the table to explore, search, or view it in full screen!
            </h6>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(df, width=900)  

    # Add a title and the cleaning report in the right column
    with col2:
        st.markdown(
            """
            <h3 style='color: #333333;  font-size: 24px; font-weight: bold;'>
                🧹 Let's Clean Your Data
            </h3>
            <h6 style='font-family: "Poppins", sans-serif; font-size: 12px; color: #333333; margin-top: -10px;'>
            Abracadabra, your data is now clean!
            </h6>
            """,
            unsafe_allow_html=True,
        )

        if cleaning_report:
            st.markdown(
                """
                <style>
                /* Apply Poppins font globally to the cleaning report section */
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

                .report {
                    margin-bottom: 10px; /* Reduce spacing between each report */
                    color: #1E1E1E;
                    font-size: 12px;
                    font-family: 'Poppins', sans-serif; /* Use Poppins font */
                }

                .report-title {
                    color: #1E1E1E;
                    font-size: 18px;
                    font-weight: bold;
                    font-family: 'Poppins', sans-serif; /* Use Poppins font */
                }

                .no-cleaning {
                    color: #333333;
                    font-size: 14px;
                    font-family: 'Poppins', sans-serif; /* Use Poppins font */
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            for report in cleaning_report:
                st.markdown(
                    f"<p class='report'>{report}</p>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                """
                <style>
                .no-cleaning { color: #333333; font-size: 16px; font-family: 'Poppins', sans-serif; }
                </style>
                <p class='no-cleaning'>No cleaning necessary; data was already clean ✨.</p>
                """,
                unsafe_allow_html=True,
            )




    col1, col2 = st.columns([1, 3])

    # Content for col1
    with col1:
        st.markdown(
            """
            <h3 style='color: #333333; font-size: 20px; font-weight: bold;'>
                🧙‍♂️ Chart Wizardry
            </h3>
            <h6 style='font-family: "Poppins", sans-serif; font-size: 12px; color: #333333; margin-top: -10px;'>
                Bring your chart to life!
            </h6>
            """,
            unsafe_allow_html=True,
        )

        column_options = df.columns.tolist()

        # Add your interactive widgets
        x_axis = st.selectbox("Choose your X column", options=column_options)
        y_axis = st.selectbox("Choose your Y column", options=column_options)
        chart_type = st.selectbox(
            "Any chart type in mind? 🤔",
            ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Tree Map"],
        )

        # Move the button to the bottom of col1
        generate_chart = st.button("Generate Visualization")

    # Content for col2
    if generate_chart:  # Check if the button is pressed
        with col2:
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

        # Visualizer AI Section
        st.subheader("Visualizer AI")
        if st.button("Analyze Chart with AI"):
            st.session_state.chart_displayed = False  # Prevent multiple analyses for the same chart
            with st.spinner("Analyzing the chart... Please wait."):
                # Convert the chart to an image for analysis
                chart_image = fig_to_pil(last_chart["chart"])
                # Generate AI insights
                response = get_gemini_response("Analyze this chart", chart_image)

                # Display the AI-generated insights
                st.subheader("AI Insights:")
                if response:
                    st.write(response)
                else:
                    st.write("No insights generated. Please try again.")

                