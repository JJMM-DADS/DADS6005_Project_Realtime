from dash import Dash, dcc, html, Input, Output
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


def get_data():
    df1 = pd.read_csv("C:/Users/kan_2/Downloads/record_bitkub.csv")
    df1["market"] = "bitkub"
    df2 = pd.read_csv("C:/Users/kan_2/Downloads/record.csv")
    df2["market"] = "binance"
    df1 = df1.rename(columns={"last": "last_price(THB)"})
    df1_cut = df1[["timestamp", "last_price(THB)", "market"]].sort_values(by=["timestamp"])
    df2_cut = df2[["timestamp", "last_price(THB)", "market"]].sort_values(by=["timestamp"])
    out = pd.concat([df1_cut, df2_cut])
    # print(out.shape)
    out2 = out.sort_values(by=["timestamp"]).reset_index()
    out2['timestamp'] = pd.to_datetime(out2['timestamp'], format='%Y/%m/%d %H:%M:%S')
    time_max = out2[out2["market"] == "binance"]["timestamp"].max()
    out3 = out2[out2["timestamp"] <= time_max]
    return out3

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([

        dcc.Graph(id='graph',figure={}),
        dcc.Interval(id="interval" ,interval=2*1000),
html.Div([
        dcc.Graph(id='graph2',figure={},className='three columns'),
        dcc.Graph(id='graph3', figure={},className='three columns'),
        dcc.Graph(id='graph4', figure={}, className='three columns'),
])

])



@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input('interval', 'n_intervals')])

def update_data(n_intervals):
    out3=get_data()
    color_discrete_map = {'bitkub': 'rgb(255,0,0)', 'binance': 'rgb(0,0,255)'}
    fig = px.line(data_frame=out3.tail(100), x='timestamp', y='last_price(THB)',color="market",color_discrete_map=color_discrete_map)
    fig.update_layout(
        autosize=False,
        width=1200,
        height=450, )
    #print(out2)
    return fig

@app.callback(
    Output(component_id='graph2', component_property='figure'),
    [Input('interval', 'n_intervals')])

def update_data(n_intervals):
    out3=get_data()
    df2 = out3[out3["market"] == "binance"]
    dff=df2.sort_values(by=["timestamp"]).tail(2)
    before,now=dff["last_price(THB)"].to_list()
    fig2 = go.Figure(go.Indicator(
        mode="number+delta",
        value=float(now),
        number={'prefix': "฿"},
        delta={'position': "top", 'reference': float(before)},
        domain={'x': [0, 1], 'y': [0, 1]},
        title ="binance price(THB)"))

    fig2.update_layout(
        autosize=False,
        width=250,
        height=250, )
    #print(out2)
    return fig2

@app.callback(
    Output(component_id='graph3', component_property='figure'),
    [Input('interval', 'n_intervals')])

def update_data(n_intervals):
    out3=get_data()
    df2 = out3[out3["market"] == "bitkub"]
    dff=df2.sort_values(by=["timestamp"]).tail(2)
    before,now=dff["last_price(THB)"].to_list()
    fig3 = go.Figure(go.Indicator(
        mode="number+delta",
        value=float(now),
        number={'prefix': "฿"},
        delta={'position': "top", 'reference': float(before)},
        domain={'x': [0, 1], 'y': [0, 1]},
        title ="bitkub price(THB)"))
    #print(out2)
    fig3.update_layout(
        autosize=False,
        width=250,
        height=250, )
    return fig3

@app.callback(
    Output(component_id='graph4', component_property='figure'),
    [Input('interval', 'n_intervals')])

def update_data(n_intervals):
    out3=get_data()
    df2 = out3[out3["market"] == "bitkub"]
    dff=df2.sort_values(by=["timestamp"]).tail(2)
    before_k,now_k=dff["last_price(THB)"].to_list()

    df2 = out3[out3["market"] == "binance"]
    dff=df2.sort_values(by=["timestamp"]).tail(2)
    before_n,now_n=dff["last_price(THB)"].to_list()

    fig4 = go.Figure(go.Indicator(
        mode="number+delta",
        value=float(now_n-now_k),
        number={'prefix': "฿"},
        domain={'x': [0, 1], 'y': [0, 1]},
        title ="Arbitrage"))
    #print(out2)
    fig4.update_layout(
        autosize=False,
        width=250,
        height=250, )
    return fig4

if __name__ == '__main__':
    app.run_server()
