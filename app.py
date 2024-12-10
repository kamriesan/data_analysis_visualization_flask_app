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
import pdfkit
from datetime import datetime


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

def create_pdf(html_content, output_filename):
    pdfkit.from_string(html_content, output_filename)

def prepare_html(insights):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Split the insights into lines and process each line
    insights_lines = insights.split('\n')
    formatted_insights = ""  # Initialize the content holder
    
    for line in insights_lines:
        # Check if the line starts with a single asterisk for bullet points
        if line.startswith('*'):
            line = line[1:].strip()  # Remove the leading asterisk and any whitespace
            line_corrected = ""
        else:
            line_corrected = line  # Process as a regular paragraph

        # Apply bold formatting for words enclosed in **...**
        in_bold = False
        i = 0
        while i < len(line):
            if line[i:i+2] == '**':  # Detecting bold markers
                if not in_bold:
                    line_corrected += '<strong>'
                    in_bold = True
                else:
                    line_corrected += '</strong>'
                    in_bold = False
                i += 2  # Skip the next star as part of the bold marker
            else:
                line_corrected += line[i]
                i += 1

        # Wrap bullet points in <li> tags and normal lines in <p> tags
        if line.startswith('*'):
            formatted_insights += f"<li>{line_corrected}</li>"
        else:
            formatted_insights += f"<p>{line_corrected}</p>"

    # Wrap all bullet points in <ul> if there are any
    if '<li>' in formatted_insights:
        formatted_insights = f"<ul>{formatted_insights}</ul>"

    html_content = f"""
    <html>
    <head>
        <title>AI Insights Report</title>
    </head>
    <body>
        <h1>AI Insights Report</h1>
        <p>Generated on {current_time}</p>
        <h2>Insights:</h2>
        <div>{formatted_insights}</div>
    </body>
    </html>
    """
    return html_content

def generate_and_download_pdf(insights):
    html_content = prepare_html(insights)
    filename = "AI_Insights_Report.pdf"
    create_pdf(html_content, filename)
    return filename

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
            st.markdown(
                """
                <h3 style='color: #333333; font-size: 20px; font-weight: bold;'>
                    📊 Your Chart
                </h3>
                """,
                unsafe_allow_html=True,
            )
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

            # Ensure the session state is initialized
            if "chart_displayed" not in st.session_state:
                st.session_state.chart_displayed = False
            if "ai_analysis_started" not in st.session_state:
                st.session_state.ai_analysis_started = False

            # Chart generation logic
            if chart:
                st.plotly_chart(chart, use_container_width=True)
                st.session_state.generated_charts = [{"chart": chart}]  # Store the latest chart
                st.session_state.chart_displayed = True

    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(
            """
            <h3 style='color: #333333; font-size: 20px; font-weight: bold;'>
    📜 Summon AI Insights
            </h3>
            <h6 style='font-family: "Poppins", sans-serif; font-size: 12px; color: #333333; margin-top: -10px;'>
    Let's consult the magic of Artificial Intelligence to gain insights of your chart!
            </h6>
            """,
            unsafe_allow_html=True,
        )
        # Display the latest chart only when not already displayed
        if st.session_state.chart_displayed:
            last_chart = st.session_state.generated_charts[-1]  # Get the last chart
            st.plotly_chart(last_chart["chart"], key="unique_chart")  # Display the chart once

            # Visualizer AI Section
            if st.button("Analyze Chart with AI"):
                st.session_state.chart_displayed = False  # Prevent multiple analyses for the same chart
                with st.spinner("Analyzing the chart... Please wait."):
                    # Convert the chart to an image for analysis
                    chart_image = fig_to_pil(last_chart["chart"])
                    # Generate AI insights
                    # Add custom CSS for the AI Insights text
                    # Add custom CSS for the AI insights text
                    st.markdown(
                        """
                        <style>
                        .ai-insights-text {
                            color: #333333; /* Dark gray text */
                            font-family: 'Poppins', sans-serif; /* Modern font */
                            font-size: 16px; /* Standard font size */
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                    # AI-generated insights logic
                    response = get_gemini_response("Analyze this chart", chart_image)

                    # Display the AI-generated insights with the custom color
                    if response:
                        st.markdown(f"<p class='ai-insights-text'>{response}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(
                            "<p class='ai-insights-text'>No insights generated. Please try again.</p>",
                            unsafe_allow_html=True,
                        )
                    
                    # Add a button in the Streamlit UI to generate and download the PDF
                    if st.button("Download AI Insights as PDF"):
                        if "AI_insights" in st.session_state:
                            pdf_file = generate_and_download_pdf(st.session_state.AI_insights)
                            with open(pdf_file, "rb") as file:
                                st.download_button(
                                    label="Download PDF",
                                    data=file,
                                    file_name=pdf_file,
                                    mime="application/pdf"
                                )
                        else:
                            st.error("Generate insights before downloading.")



