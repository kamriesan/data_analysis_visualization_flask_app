import pandas as pd
import streamlit as st
import plotly.express as px

# Set Streamlit page configuration
st.set_page_config(page_title="Dynamic Data Visualizer", page_icon="📊", layout="wide")

# Sidebar content
st.sidebar.title("Data Genie")

# Initialize session state
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "Visualize Data"

# Sidebar menu
menu_items = {
    "Visualize Data": "📊",
    "AskAI": "🤖"
}

for item, icon in menu_items.items():
    if st.sidebar.button(f"{icon} {item}"):
        st.session_state.active_menu = item

# Rule-based chatbot logic
def chatbot_response(user_input):
    if "hello" in user_input.lower():
        return "Hello! How can I assist you today?"
    elif "data" in user_input.lower():
        return "This application lets you upload and analyze data. Try the Visualize Data tab!"
    elif "help" in user_input.lower():
        return "Sure! You can ask me about this application's features or general inquiries."
    else:
        return "I'm not sure about that. Try asking something else!"

# Main content logic
if st.session_state.active_menu == "Visualize Data":
    st.header("Dynamic Survey Data Visualizer")
    st.subheader("Upload any CSV file to explore the data dynamically!")

    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("CSV file uploaded successfully!")
        st.dataframe(df.head())

        if st.button("Edit Data"):
            edited_df = st.data_editor(df)
            st.dataframe(edited_df)

        column_options = df.columns.tolist()
        filter_column = st.selectbox("Filter by column:", options=column_options)
        if df[filter_column].dtype == 'object':
            unique_values = df[filter_column].unique().tolist()
            filter_values = st.multiselect(f"Values to include:", unique_values, default=unique_values)
            filtered_data = df[df[filter_column].isin(filter_values)]
        else:
            min_val, max_val = df[filter_column].min(), df[filter_column].max()
            range_vals = st.slider(f"Select range:", min_val, max_val, (min_val, max_val))
            filtered_data = df[df[filter_column].between(range_vals[0], range_vals[1])]

        st.dataframe(filtered_data)

        x_axis = st.selectbox("X-axis column:", options=column_options)
        y_axis = st.selectbox("Y-axis column:", options=column_options)
        chart_type = st.selectbox("Chart type:", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])

        if st.button("Generate Visualization"):
            if chart_type == "Bar Chart":
                chart = px.bar(filtered_data, x=x_axis, y=y_axis)
            elif chart_type == "Line Chart":
                chart = px.line(filtered_data, x=x_axis, y=y_axis)
            elif chart_type == "Scatter Plot":
                chart = px.scatter(filtered_data, x=x_axis, y=y_axis)
            elif chart_type == "Pie Chart":
                chart = px.pie(filtered_data, names=x_axis, values=y_axis)
            st.plotly_chart(chart)

elif st.session_state.active_menu == "AskAI":
    st.title("AskAI")
    st.write("Interact with a simple AI for insights!")

    # User input for chat
    user_question = st.text_input("Ask your question:")
    if st.button("Send"):
        if user_question.strip() != "":
            # Get chatbot response
            response = chatbot_response(user_question)
            st.write(response)
        else:
            st.warning("Please enter a question.")
