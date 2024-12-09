import plotly.express as px
import streamlit as st
from io import BytesIO
from PIL import Image
import google.generativeai as genai

def display_chart(df, x_axis, y_axis, chart_type):
    st.subheader("Chart Display")
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
        st.plotly_chart(chart, use_container_width=True)
    return chart

def analyze_chart_with_ai(chart):
    st.subheader("Visualizer AI")
    if st.button("Analyze Chart with AI", key="analyze_ai"):
        with st.spinner("Analyzing the chart... Please wait."):
            chart_image = fig_to_pil(chart)
            response = get_gemini_response("Analyze this chart", chart_image)
        st.subheader("AI Insights:")
        st.write(response if response else "No insights generated. Please try again.")

def fig_to_pil(fig):
    buf = BytesIO()
    fig.write_image(buf, format="png")
    buf.seek(0)
    return Image.open(buf)

def get_gemini_response(input_text, image):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        if input_text and image:
            response = model.generate_content([input_text, image])
        elif input_text:
            response = model.generate_content([input_text])
        else:
            response = None
        return response.text if response else "No response available."
    except Exception as e:
        return f"Error in generating response: {e}"
