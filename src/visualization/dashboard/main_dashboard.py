import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from src.main import backtest_pairs_trading

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Roboto:wght@300;400&display=swap']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Stock Comparison Dashboard", style={'color': '#000000'}),

    html.Div([
        html.Label("Stock 1:", style={'color': '#000000', 'display': 'block'}),
        dcc.Input(id='stock-1', type='text', value='AAPL',
                  style={'color': '#000000', 'width': '100%'}),

        html.Label("Stock 2:", style={'color': '#000000', 'display': 'block'}),
        dcc.Input(id='stock-2', type='text', value='GOOGL',
                  style={'color': '#000000', 'width': '100%'}),

        html.Label("Start Date:", style={'color': '#000000', 'display': 'block'}),
        dcc.DatePickerSingle(id='start-date', date='2020-01-01',
                             style={'color': '#000000', 'width': '100%'}),

        html.Label("End Date:", style={'color': '#000000', 'display': 'block'}),
        dcc.DatePickerSingle(id='end-date', date='2023-01-01',
                             style={'color': '#000000', 'width': '100%'}),

        html.Label("Z-Score:", style={'color': '#000000', 'display': 'block'}),
        dcc.Input(id='z-score', type='number', value=1.0,
                  style={'color': '#000000', 'width': '100%'})
    ], style={'width': '30%', 'padding': '10px', 'boxSizing': 'border-box'}),

    dcc.Graph(id='stock-graph', style={'color': '#000000'}),

    html.Div(id='output-section')

], style={'fontFamily': 'Roboto', 'padding': '10px'})


@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-1', 'value'),
     Input('stock-2', 'value'),
     Input('start-date', 'date'),
     Input('end-date', 'date'),
     Input('z-score', 'value')]
)
def update_graph(stock1, stock2, start_date, end_date, z_score):
    df1 = pd.DataFrame({
        'Date': pd.date_range(start=start_date, end=end_date, freq='D'),
        'Price': [i + (i*0.02) for i in range(len(pd.date_range(start=start_date, end=end_date, freq='D')))]
    })
    df2 = pd.DataFrame({
        'Date': pd.date_range(start=start_date, end=end_date, freq='D'),
        'Price': [i + (i*0.03) for i in range(len(pd.date_range(start=start_date, end=end_date, freq='D')))]
    })

    trace1 = go.Scatter(x=df1['Date'], y=df1['Price'], mode='lines', name=stock1)
    trace2 = go.Scatter(x=df2['Date'], y=df2['Price'], mode='lines', name=stock2)

    return {'data': [trace1, trace2], 'layout': go.Layout(title='Stock Data', xaxis=dict(title='Date'), yaxis=dict(title='Price'))}

@app.callback(
    Output('output-section', 'children'),
    [Input('stock-1', 'value'),
     Input('stock-2', 'value'),
     Input('start-date', 'date'),
     Input('end-date', 'date'),
     Input('z-score', 'value')]
)
def update_output(stock1, stock2, start_date, end_date, z_score):
    cumulative_strategy_returns, max_drawdown, sharpe_ratio = backtest_pairs_trading(stock1, stock2, start_date, end_date, z_score)

    return [
        html.P(f"Cumulative Strategy Returns: {cumulative_strategy_returns}"),
        html.P(f"Maximum Drawdown: {max_drawdown:.2%}"),
        html.P(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    ]

if __name__ == '__main__':
    app.run_server(debug=True)
