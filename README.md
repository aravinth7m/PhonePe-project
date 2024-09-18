PhonePe Pulse Data Dashboard
This project is a Streamlit web application that visualizes the PhonePe transaction data stored in a MySQL database (TiDB Cloud). The dashboard presents various insights and analysis of transaction and user data using interactive charts and tables.
Introduction
The PhonePe Pulse Data Dashboard is an interactive web application designed to provide insights into PhonePe's transaction and user data. Built using Streamlit, this dashboard connects to a TiDB Cloud MySQL database and visualizes key metrics through intuitive charts and graphs. The project enables users to explore detailed information about transaction volumes, user demographics, and trends across different regions of India.

The goal of this project is to offer a comprehensive view of PhonePe's growth and performance by transforming raw data into meaningful insights. The dashboard is easy to navigate and offers features like top transaction charts, usage insights, and demographic breakdowns, helping businesses and analysts make data-driven decisions.

Project Structure
PhonePe_pulse.ipynb: A Jupyter notebook that handles the processing of PhonePe Pulse data.
streamlit_app.py: The main Python script for the Streamlit web app that visualizes the processed data.
Features
Home: A landing page that welcomes users to the dashboard.
Count Information: Shows the total transaction and user counts.
Transaction Information: Provides detailed insights into transaction data.
User Information: Displays user demographics and activity information.
Top Charts: Ranks data such as top cities, states, or transaction types.
Insights: Offers custom data analysis based on key performance metrics.
Installation
Prerequisites
Python 3.9+
MySQL Database (TiDB Cloud for this project)
The following Python packages:
streamlit
streamlit_option_menu
pandas
plotly
matplotlib
mysql-connector-python
SQLAlchemy
