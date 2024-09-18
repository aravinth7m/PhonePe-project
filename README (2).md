
# PhonePe Pulse Data Dashboard

This project is a **Streamlit** web application that visualizes the PhonePe transaction data stored in a **MySQL** database (TiDB Cloud). The dashboard presents various insights and analysis of transaction and user data using interactive charts and tables.

## Project Structure

- **PhonePe_pulse.ipynb**: A Jupyter notebook that handles the processing of PhonePe Pulse data.
- **streamlit_app.py**: The main Python script for the Streamlit web app that visualizes the processed data.

## Features

- **Home**: A landing page that welcomes users to the dashboard.
- **Count Information**: Shows the total transaction and user counts.
- **Transaction Information**: Provides detailed insights into transaction data.
- **User Information**: Displays user demographics and activity information.
- **Top Charts**: Ranks data such as top cities, states, or transaction types.
- **Insights**: Offers custom data analysis based on key performance metrics.

## Introduction

The **PhonePe Pulse Data Dashboard** is an interactive web application designed to provide insights into PhonePe's transaction and user data. Built using **Streamlit**, this dashboard connects to a **TiDB Cloud** MySQL database and visualizes key metrics through intuitive charts and graphs. The project enables users to explore detailed information about transaction volumes, user demographics, and trends across different regions of India.

The goal of this project is to offer a comprehensive view of PhonePe's growth and performance by transforming raw data into meaningful insights. The dashboard is easy to navigate and offers features like top transaction charts, usage insights, and demographic breakdowns, helping businesses and analysts make data-driven decisions.

## Installation

### Prerequisites
- **Python 3.9+**
- **MySQL Database** (TiDB Cloud for this project)
- The following Python packages:
  - `streamlit`
  - `streamlit_option_menu`
  - `pandas`
  - `plotly`
  - `matplotlib`
  - `mysql-connector-python`
  - `SQLAlchemy`

### Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/your-repo/phonepe-pulse-dashboard.git
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your MySQL database (in this case, a **TiDB Cloud** instance) with the necessary tables and data.

4. Update the database connection details in the `streamlit_app.py` file:
    ```python
    connection = mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="your-username",
        password="your-password",
        database="Phonepe"
    )
    ```

5. Run the Streamlit app:
    ```bash
    streamlit run streamlit_app.py
    ```

## Usage

- Access the app in your browser at `http://localhost:8501`.
- Use the sidebar to navigate between different sections like "Count Information", "Transaction Information", etc.
- Visualize transaction data, user demographics, top charts, and more using interactive graphs and plots.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
