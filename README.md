
# DataGenie AI

**DataGenie AI** is an intuitive and powerful data visualization and analytics tool that helps users upload, clean, and explore their data dynamically. This app integrates advanced AI capabilities to provide insightful visualizations and analyses.

---

## Features

- **Dynamic Data Cleaning**: Automatically cleans data, removes duplicates, and identifies missing values with detailed reports.
- **Intuitive Visualizations**: Generate charts, including Bar Charts, Line Charts, Scatter Plots, Pie Charts, and Tree Maps, using simple selections.
- **AI-Powered Analysis**: Leverages generative AI to provide detailed insights into your data visualizations.
- **Interactive Interface**: Easy-to-use interface designed with Streamlit.
- **Customizable Themes**: Includes custom CSS for a seamless user experience.

---

## Installation

Follow these steps to set up and run the application:

### Prerequisites
- Python 3.8 or later
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

4. **Set Up Environment Variables**
   - Create a `.env` file in the root directory.
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=<your-google-api-key>
     ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

6. **Access the App**
   - Open the provided URL (e.g., `http://localhost:8501`) in your web browser.

---

## Usage

1. Upload a CSV file to begin analyzing your data.
2. Clean data dynamically using the built-in data cleaning features.
3. Choose the type of chart and columns for visualization.
4. Optionally, use the AI feature to analyze and gain insights into your charts.

---

## Folder Structure

```
├── assets/          # Contains images, icons, and splash screen resources
├── components/      # Custom reusable components
├── styles.css       # Custom CSS for styling
├── app.py           # Main application file
├── requirements.txt # Required Python packages
├── setup.sh         # Shell script for environment setup
└── README.md        # Application documentation
```

---

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Framework for interactive web applications
- **Plotly**: Library for creating visualizations
- **Google Generative AI**: Integrated for chart analysis
- **Pandas**: Data manipulation and cleaning

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Author

Created by **Mika Gangoso**. For inquiries or support, contact: [your-email@example.com].
