import streamlit as st

def configure_options(df):
    st.subheader("Configure Chart Options")
    column_options = df.columns.tolist()

    x_axis = st.selectbox("X-axis column:", options=column_options, key="x_axis")
    y_axis = st.selectbox("Y-axis column:", options=column_options, key="y_axis")
    chart_type = st.selectbox(
        "Chart type:", 
        ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Tree Map"], 
        key="chart_type"
    )
    return x_axis, y_axis, chart_type
