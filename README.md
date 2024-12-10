https://bit.ly/datagenie-ai

# 🔮 DataGenie AI

**DataGenie AI** is a powerful and user-friendly data visualization and analytics application designed to enable dynamic data exploration. It integrates cutting-edge AI capabilities to provide insights into your data.

---

## 🪄 Features

- **Dynamic Data Cleaning**: Automatically cleans data, removes duplicates, and handles missing values with detailed reporting.
- **Interactive Visualizations**: Create customizable charts including Bar Charts, Line Charts, Scatter Plots, Pie Charts, and Tree Maps.
- **AI-Powered Insights**: Leverages Google Generative AI to analyze charts and provide meaningful insights.
- **User-Friendly Interface**: Built with Streamlit for an intuitive and interactive web-based interface.
- **Customizable Themes**: Includes CSS styling for a polished user experience.

---

## Installation

Follow these steps to set up and run the application locally:

### Prerequisites
- Python 3.9 or higher
- Virtual Environment (optional but recommended)

### Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up a Virtual Environment** (Optional)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**
   - Create a `.env` file in the root directory.
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your-api-key
     ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

6. **Access the App**
   - Open the URL displayed in your terminal (e.g., `http://localhost:8501`) in your browser.

---

## Usage

1. Upload a CSV file to start analyzing your data.
2. Dynamically clean and visualize data with customizable charts.
3. Use the AI feature to analyze visualizations and gain insights.

---

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Framework for interactive web apps
- **Plotly**: Library for creating data visualizations
- **Google Generative AI**: Provides AI-powered insights
- **Pandas**: Data manipulation and cleaning

---

## Folder Structure

```
├── assets/          # Contains images and static files
├── components/      # Custom reusable components
├── styles.css       # CSS for styling
├── app.py           # Main application logic
├── requirements.txt # Python dependencies
├── README.md        # Application documentation
└── .env.example     # Example of environment variables (DO NOT COMMIT SECRETS!)
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

Developed by:
Mika Gangoso
John Vincent Racimo
Ma Corazon Macaraig
Vince Anthony Carlos
Korinne Verdillo
---

