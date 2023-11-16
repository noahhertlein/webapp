from datetime import date
import dash
from dash import dcc, html, Input, Output
from dash.dependencies import State
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Import the utility functions from the utils module and Sec module
from sec import fetch_sec_filings

from utils import (calculate_RSI, calculate_MACD, validate_date_range, analyze_sentiment)

external_stylesheets = ['https://fonts.googleapis.com/css?family=Roboto&display=swap']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.server.secret_key = 'noah3278'  # You should change this for security reasons

# Define layout
app.layout = html.Div([
    html.Img(src='/assets/my_logo.png', height='300px', style={'display':'block', 'margin':'auto'}),  # Logo

    html.Title("Securities Analysis Dashboard", style={'textAlign': 'center', 'color': '#000000'}),
    
    # Button to trigger SEC analysis
    html.Button('Analyze SEC Filings', id='sec-analysis-button', n_clicks=0),

    # Container to display the results
    html.Div(id='sec-analysis-output'),

    html.Label("Stock Tickers (comma-separated):", style={'color': '#34495E', 'fontWeight': 'normal'}),
    dcc.Input(id='stock-input', value='', type='text'),

    html.Label("Date Range:"),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=pd.to_datetime('2023-01-01'),
        end_date=pd.to_datetime(date.today()),
    ),

    dcc.Checklist(
    id='ma-checklist',
    style={'color': '#34495E', 'fontWeight': 'normal'},
    options=[
        {'label': 'Show 20-day Moving Average', 'value': '20'},
        {'label': 'Show 50-day Moving Average', 'value': '50'},
        {'label': 'Show 100-day Moving Average', 'value': '100'},
        {'label': 'Show 200-day Moving Average', 'value': '200'},
    ],
    value=[]
),


    dcc.Dropdown(
        id='plot-type',
        options=[
            {'label': 'Price', 'value': 'price'},
            {'label': 'Volume', 'value': 'volume'},
            {'label': 'RSI', 'value': 'rsi'},
            {'label': 'MACD', 'value': 'macd'},
        ],
        value='price'
    ),

    dcc.Loading(
    id="loading",
    type="cube",  # 'default', 'circle', or 'cube'
    children=[dcc.Graph(id='stock-plot')]),

    ], style={'backgroundColor': '#F8F8F8', 'fontFamily': 'Roboto', 'padding': '20px'})

# Define callbacks for the graph
@app.callback(
    Output('stock-plot', 'figure'),
    [Input('stock-input', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('ma-checklist', 'value'),
     Input('plot-type', 'value')]
)

def update_graph(stock_tickers, start_date, end_date, ma_values, plot_type):
    # Split the stock tickers string into a list
    stock_list = [stock.strip() for stock in stock_tickers.split(",")]

    # Create an empty DataFrame
    stock_data = pd.DataFrame()

    # Fetch historical data for each stock
    for stock in stock_list:
        try:
            stock_data_fetch = yf.download(stock, start=start_date, end=end_date)
        except ValueError:
            return go.Figure().update_layout(title_text=f"Error fetching data for {stock}. Please check ticker and date range.")

        stock_data[f"{stock}_price"] = stock_data_fetch['Adj Close']
        stock_data[f"{stock}_volume"] = stock_data_fetch['Volume']
        stock_data[f"{stock}_rsi"] = calculate_RSI(stock_data[f"{stock}_price"], window=14)
        stock_data[f"{stock}_macd"], stock_data[f"{stock}_signal"] = calculate_MACD(stock_data[f"{stock}_price"], 12, 26, 9)

    # Create figure
    fig = go.Figure()

    # Add traces for each stock
    for stock in stock_list:
        if plot_type == 'price':
            y_value = stock_data[f"{stock}_price"]
        elif plot_type == 'volume':
            y_value = stock_data[f"{stock}_volume"]
        elif plot_type == 'rsi':
            y_value = stock_data[f"{stock}_rsi"]
        elif plot_type == 'macd':
            y_value = stock_data[f"{stock}_macd"]
            fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data[f"{stock}_signal"], mode='lines', name=f"{stock} Signal Line"))
        else:raise ValueError(f"Unsupported plot_type: {plot_type}")




        fig.add_trace(go.Scatter(x=stock_data.index, y=y_value, mode='lines', name=f"{stock} {plot_type.capitalize()}"))

        for ma in ma_values:
            ma = int(ma)
            ma_data = y_value.rolling(window=ma).mean()
            fig.add_trace(go.Scatter(x=stock_data.index, y=ma_data, mode='lines', name=f"{stock} {ma}-day MA"))

    fig.update_layout(title=f'Stock {plot_type.capitalize()} and Indicators',
                      xaxis_title='Date',
                      yaxis_title=plot_type.capitalize(),
                      xaxis_rangeslider_visible=False)

    return fig

#callback for date picker
@app.callback(
    Output('date-picker', 'style'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def check_date_range(start_date, end_date):
    if not validate_date_range(start_date, end_date):
        return {"border": "2px solid red"}  # Red border if invalid
    else:
        return {}  # Default style if valid
    
@app.callback(
    Output('sec-analysis-output', 'children'),
    [Input('sec-analysis-button', 'n_clicks')],
    [State('stock-input', 'value')]
)
def update_sec_analysis(n_clicks, stock_input):
    if n_clicks > 0:
        stock_list = [stock.strip() for stock in stock_input.split(",")]
        first_ticker = stock_list[0] if stock_list else None
        if first_ticker:
            text_data = fetch_sec_filings(first_ticker)
            if text_data and not text_data.startswith("No filings found"):
                sentiment = analyze_sentiment(text_data)
                return f"Sentiment for {first_ticker}: Polarity = {sentiment.polarity}, Subjectivity = {sentiment.subjectivity}"
            else:
                return text_data  # This will display the message from fetch_sec_filings
        else:
            return "No ticker provided."
        
if __name__ == '__main__':
    app.run_server(debug=True)