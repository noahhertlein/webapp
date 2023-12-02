# webapp
Overview
The "webapp" repository, created by Noah Hertlein, is a Python-based web application that focuses on financial data analysis and visualization. It utilizes Dash, a Python framework for building analytical web applications, and integrates financial data from various sources. The repository contains several Python scripts and a requirements file, indicating a streamlined and focused project.

Repository Structure
app.py: This is the main file of the web application. It uses Dash to create a web interface for securities analysis. The app includes features for analyzing SEC filings, visualizing stock data, and computing financial indicators like RSI (Relative Strength Index) and MACD (Moving Average Convergence Divergence).
sec.py: This script handles fetching SEC filings for a given stock ticker. It uses an API to retrieve the most recent 10-K filings and returns the text content of these filings.
utils.py: This utility script includes functions for sentiment analysis, RSI calculation, MACD calculation, stock ticker validation, and date range validation. It uses libraries like yfinance, pandas, and textblob.
requirements.txt: Lists all the Python dependencies required for the web application. This file is crucial for setting up the project environment.
Key Features
Securities Analysis Dashboard: A central feature of the web app, allowing users to input stock tickers and select date ranges for analysis.
SEC Filings Analysis: Users can analyze SEC filings for specific companies, with sentiment analysis provided for the text of these filings.
Stock Data Visualization: The app provides functionality to plot stock prices, volumes, and financial indicators like RSI and MACD.
Date Range Selection: Users can select specific date ranges for their analysis, enhancing the flexibility of the tool.
Moving Average Visualization: The app supports visualization of different moving averages (20-day, 50-day, 100-day, 200-day) for stock data.
Installation and Setup
Clone the repository.
Install the required dependencies using pip install -r requirements.txt.
Run app.py to start the Dash server and access the web application.
Security and API Usage
The application uses an API key for fetching SEC filings, which is currently hardcoded in sec.py. Users should replace this with their own API key for security reasons.
The Dash server's secret key is also hardcoded in app.py. It is advisable to change this key when deploying the application.
Limitations and Further Development
The current version of the app has limited error handling, particularly in data fetching and API interactions.
Future enhancements could include more comprehensive financial analysis tools, improved user interface, and expanded data sources.
