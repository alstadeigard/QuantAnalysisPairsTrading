import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from src.trading.pairs_trading import backtest_pairs_trading

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Roboto:wght@300;400&display=swap']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Pairs Trading Analysis Dashboard", style={'color': '#000000', 'text-align': 'center'}),

    html.Div([
        html.Div("Input Parameters", style={'font-weight': 'bold', 'font-size': '20px', 'margin-bottom': '10px',
                                            'border-bottom': '2px solid #ccc'}),

        html.Label("Stock 1:"),
        dcc.Input(id='stock-1', type='text', value='AAPL',
                  style={'color': '#000000', 'width': '100%', 'padding': '10px', 'margin-bottom': '10px'}),

        html.Label("Stock 2:"),
        dcc.Input(id='stock-2', type='text', value='GOOGL',
                  style={'color': '#000000', 'width': '100%', 'padding': '10px', 'margin-bottom': '10px'}),

        html.Label("Start Date:"),
        dcc.DatePickerSingle(id='start-date', date='2020-01-01',
                             style={'color': '#000000', 'width': '100%', 'margin-bottom': '10px'}),

        html.Label("End Date:"),
        dcc.DatePickerSingle(id='end-date', date='2023-01-01',
                             style={'color': '#000000', 'width': '100%', 'margin-bottom': '10px'}),

        html.Label("Z-Score:"),
        dcc.Input(id='z-score', type='number', value=1.0,
                  style={'color': '#000000', 'width': '100%', 'padding': '10px', 'margin-bottom': '15px'}),

        html.Button("Evaluate Pairs Trading Strategy", id="evaluate-button", n_clicks=0,
                    style={'background-color': '#2196F3', 'color': '#fff', 'border': 'none', 'cursor': 'pointer',
                           'padding': '10px 20px', 'border-radius': '2px', 'font-size': '16px'})

    ], style={'width': '30%', 'padding': '20px', 'boxSizing': 'border-box', 'background-color': '#f8f8f8',
              'border-radius': '5px', 'margin': '20px auto'}),

    html.Div("Visualization and Results",
             style={'font-weight': 'bold', 'font-size': '20px', 'margin': '20px 0', 'border-bottom': '2px solid #ccc'}),
    dcc.Graph(id='stock-graph', style={'color': '#000000', 'display': 'none'}),
    html.Div(id='output-section', style={'display': 'none', 'margin': '20px 0'})

], style={'fontFamily': 'Roboto', 'padding': '30px', 'max-width': '1200px', 'margin': '0 auto'})


@app.callback(
    [Output('stock-graph', 'figure'),
     Output('stock-graph', 'style'),
     Output('output-section', 'children'),
     Output('output-section', 'style')],
    [Input('evaluate-button', 'n_clicks')],
    [State('stock-1', 'value'),
     State('stock-2', 'value'),
     State('start-date', 'date'),
     State('end-date', 'date'),
     State('z-score', 'value')]
)
def update_results(n_clicks, stock1, stock2, start_date, end_date, z_score):
    if n_clicks == 0:
        return dash.no_update, {'display': 'none'}, dash.no_update, {'display': 'none'}

    stock1_data, stock2_data, are_cointegrated, p_value, cumulative_strategy_returns, max_drawdown, sharpe_ratio, total_returns = backtest_pairs_trading(
        stock1,
        stock2,
        start_date,
        end_date,
        z_score)

    trace1 = go.Scatter(x=stock1_data.index, y=stock1_data['Adj Close'], mode='lines', name=stock1)
    trace2 = go.Scatter(x=stock2_data.index, y=stock2_data['Adj Close'], mode='lines', name=stock2)
    trace3 = go.Scatter(x=cumulative_strategy_returns.index, y=cumulative_strategy_returns, mode='lines',
                        name='Cumulative Returns', yaxis='y2')

    title_text = f"Adjusted Close Price of {stock1} vs {stock2} ({start_date} to {end_date})"
    graph_data = {
        'data': [trace1, trace2, trace3],
        'layout': go.Layout(
            title=title_text,
            xaxis=dict(title='Date'),
            yaxis=dict(title='Adjusted Close Price'),
            yaxis2=dict(title='Cumulative Returns', overlaying='y', side='right')
        )
    }
    graph_style = {'display': 'block'}

    cointegration_result = f"The stocks are cointegrated with p-value: {p_value:.5f}" if are_cointegrated else f"The stocks are not cointegrated with p-value: {p_value:.5f}"

    output_data = [
        html.P(cointegration_result),
        html.P(f"Total Returns: {total_returns:.2%}"),
        html.P(f"Maximum Drawdown: {max_drawdown:.2%}"),
        html.P(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    ]
    if not are_cointegrated:
        cointegration_disclaimer = html.P(
            "Disclaimer: For the results of pairs trading to be reliable, the stocks ideally should be cointegrated, meaning a p-value of under 0.05. Proceed with caution as these stocks are not cointegrated.",
            style={'color': 'red'})
        output_data.append(cointegration_disclaimer)
    output_style = {'display': 'block'}

    return graph_data, graph_style, output_data, output_style



if __name__ == '__main__':
    app.run_server(debug=True)
