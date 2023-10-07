import dash
from dash import dcc, html, Input, Output
from dash import dash_table
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Import the utility functions from the utils module
from utils import (
    fetch_ratios, calculate_RSI, calculate_MACD, 
    validate_ticker, validate_date_range
)

external_stylesheets = ['https://fonts.googleapis.com/css?family=Roboto&display=swap']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.server.secret_key = 'noah3278'  # You should change this for security reasons

# Define layout
app.layout = html.Div([
    html.Img(src='/assets/my_logo.png', height='200px', style={'display':'block', 'margin':'auto'}),  # Logo

    html.H1("Comprehensive Stock Analysis Dashboard", style={'textAlign': 'center', 'color': '#2C3E50'}),

    html.Label("Stock Tickers (comma-separated):", style={'color': '#34495E', 'fontWeight': 'bold'}),
    dcc.Input(id='stock-input', value='NVDA, ARM', type='text'),

    html.Label("Date Range:"),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=pd.to_datetime('2023-01-01'),
        end_date=pd.to_datetime('2023-10-01'),
    ),

    dcc.Checklist(
    id='ma-checklist',
    style={'color': '#34495E', 'fontWeight': 'bold'},
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

    dcc.Graph(id='stock-plot'),

    html.Label("Financial Ratios (First Ticker In List Only):"),
    dash_table.DataTable(
        id='table',
        columns=[{"name": 'Indicator', "id": 'Indicator'}, {"name": 'Value', "id": 'Value'}],
        data=[]
    )
    ], style={'backgroundColor': '#FAF9F6', 'fontFamily': 'Roboto', 'padding': '20px'})
    
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

# Define callbacks for the financial ratios table
@app.callback(
    Output('table', 'data'),
    [Input('stock-input', 'value')]
)

def update_table(stock_tickers):
    first_stock = stock_tickers.split(",")[0].strip()
    
    if not validate_ticker(first_stock):
        return [{"Indicator": "Error", "Value": "Invalid Stock Ticker"}]
    
    ratios = fetch_ratios(first_stock)
    table_data = [{"Indicator": key, "Value": value} for key, value in ratios.items()]
    return table_data

if __name__ == '__main__':
    app.run_server(debug=True)
