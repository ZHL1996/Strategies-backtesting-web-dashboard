# Import all need libraries
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import os

'''
Change working dictionary here
'''
path = '/Users/a32294/PycharmProjects/LeFrancais'
os.chdir(path)

def compound(r):
    """
    returns the result of compounding the set of returns in r
    """
    return np.expm1(np.log1p(r).sum())

'''
Load all the data that needed and stored in the same working environment
'''
data = pd.read_csv('rets.csv')
data.index = data.Date
data = data.drop('Date',axis=1)

sp500 = pd.read_csv('sp500.csv')
sp500['perf'] = (1+sp500.Close).cumprod()
sp500['perf'].iloc[0] = 1

smb = pd.read_csv('smb.csv')
def smb_s(e):
    '''
    the function returns the performance of small minus big strategy
    :param e: it means quantile, used to select the data above or below the threhold
    :return: the performance of small minus big strategy
    '''
    smbb = smb
    smbb.index = smb.Date
    smbb = smbb.drop('Date',axis=1)
    smbb = smbb.shift(1)
    mask1 = smbb.T > smbb.quantile(1-e,axis=1)
    mask2 = smbb.T < smbb.quantile(e,axis=1)
    mask1 = mask1.replace(False,0).replace(True,1).T
    mask2 = mask2.replace(False,0).replace(True,1).T
    mask1 = mask1.set_index(data.index)
    mask2 = mask2.set_index(data.index)
    dat = data.drop('BALL',axis=1)
    short = np.mean(dat * mask1,axis=1)
    long = np.mean(dat * mask2,axis=1)
    return(long- short)

def mom(date, e):
    '''
    the function returns the performance of momentum strategy
    :param date: the estimation period, use to choose the winner/loser stock based on a number of consecutive day's return
    :param e: it means quantile, used to select the data above or below the threhold
    :return: the performance of momentum strategy
    '''
    dat = data.shift(1)
    win = dat.T[dat.T > dat.quantile(1 - e, axis=1)].T
    los = dat.T[data.T < dat.quantile(e, axis=1)].T

    signal_b = win.rolling(window=date, min_periods=1).apply(lambda x: not any(pd.isna(x))).fillna(0)
    signal_s = los.rolling(window=date, min_periods=1).apply(lambda x: not any(pd.isna(x))).fillna(0)

    long = np.mean(dat.shift(-1) * signal_b, axis=1)
    short = np.mean(dat.shift(-1) * signal_s, axis=1)
    mom = long - short
    return ((mom + 1).cumprod()), mom, mom.std()

# initinally charts setup
fig = go.Figure()
fig.add_trace(go.Scatter(x=sp500.Date, y=sp500.perf, name='S&P_500', mode='lines'))

# initinal the app and the first dropdown
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
dropdown1 = dcc.Dropdown(
    id='strategies',
    options=[
        {'label': 'SMB', 'value': 'smb'},
        {'label': 'MOMEMTUM', 'value': 'mom'},
        {'label': 'HML', 'value': 'hml'}
    ],
    value='Mkt_rf'
)

## web dashboard design here
app.layout = html.Div([
    dbc.Container([
        html.Br(),
        html.Center(html.H4('Backtesting Strategies Dashboard')),
        html.Br(),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                html.Center(html.H4('Backtesting Inputs')),
                html.Br(),
                html.P('Period Selection'),
                dbc.Col(
                    dbc.Input(placeholder="select estimation period",
                    type="number", value=1, id='period'
                              )),
                html.P('Risk free rate input'),
                dbc.Col(
                    dbc.Input(placeholder="select Rf rate",
                              type="number", value=0.03, id='Rf'
                              )
                ),
                html.P('Strategies Selection'),
                dbc.Col(html.Div([
                    dropdown1
                ])),
                html.P('Quantile Selection'),
                dbc.Col(
                    dcc.Slider(
                        0,1,value = 0.1,
                        id = 'quantile'
                    )),
                html.Button('Update Data', id='update-button'),
            ]),
        ]),
        dbc.Col([
            html.Center(html.H4('Strategies Backtesting Charts')),
            dcc.Graph(
                id='result'
            )
        ]),
        html.Div([
            html.H4('Performace display'),
            html.Hr(),
            html.Div(id='information')
        ])
    ])
])

# Callback function setup
@app.callback(
    [Output(component_id='information', component_property='children'),
    Output(component_id='result', component_property='figure')],
    [Input('Rf', 'value')],
    [Input(component_id='strategies', component_property='value')],
     [Input('update-button', 'n_clicks')],
     [Input(component_id='period', component_property='value')],
     [Input(component_id='quantile', component_property='value')]
)

def update_chart(rf, strategies,n_clicks, period,quantile):
    '''
    :param rf: risk free rate
    :param strategies: either Momentum or SMB, HML currently not available
    :param n_clicks: update button
    :param period: estimation period of strategy
    :param quantile: the quantile of threshld, used to seperate data
    :return: performance display, includes annual return, annual vol and ann_Sharp_ratio and the strategy charts
    '''
    if n_clicks is None:
        return dash.no_update
    if strategies == 'mom':
        d = mom(period, quantile)[0]
        d = pd.DataFrame([d.index, d.values],index = ['date','perf']).T
        d['perf'].iloc[-1] = d['perf'].iloc[-2]
        line = go.Scatter(x=d['date'], y=d['perf'].astype(float),
                          name = f'Momentum of estimation period {period} m under the quantile of {quantile}',
                          mode='lines')
        fig.add_trace(line)
        try:
            ret = round(np.mean(mom(period, quantile)[1])*12,2)
            vol = round(mom(period, quantile)[2] * np.sqrt(12),2)
            SR = round((ret - rf)/vol,2)
            str = [ret,vol,SR]

            rett =  round(np.mean(sp500.Close) * 12,2)
            volt = round(sp500.Close.std()*np.sqrt(12),2)
            SRT = round((rett - rf)/volt,2)
            ben = [rett,volt,SRT]
            res = pd.DataFrame([ben,str],index = ['SP500','Strategy'])
            res.columns = ['Ret_ann','Vol_ann','Sharp_ratio']
            res.insert(0, 'Account', res.index)
            output = dbc.Table.from_dataframe(res, style = {'textAlign':'center'},
                                              striped=True, bordered=True,hover=True)
        except:
            pass

        return output, fig

    elif strategies == 'smb':
        d = smb_s(quantile)
        d = (d+1).cumprod()
        line = go.Scatter(x=d.index, y=d.values.astype(float),
                          name = f'SMB strategy under the quantile of {quantile}',
                          mode='lines')
        fig.add_trace(line)
        try:
            ret = round(np.mean(smb_s(quantile))*12,2)
            vol = round(smb_s(quantile).std() * np.sqrt(12),2)
            SR = round((ret - rf)/vol,2)
            str = [ret,vol,SR]

            rett =  round(np.mean(sp500.Close) * 12,2)
            volt = round(sp500.Close.std()*np.sqrt(12),2)
            SRT = round((rett - rf)/volt,2)
            ben = [rett,volt,SRT]
            res = pd.DataFrame([ben,str],index = ['SP500','Strategy'])
            res.columns = ['Ret_ann','Vol_ann','Sharp_ratio']
            res.insert(0, 'Account', res.index)
            output = dbc.Table.from_dataframe(res, style = {'textAlign':'center'},
                                              striped=True, bordered=True,hover=True)
        except:
            pass
        return output, fig
    else:
        dash.no_update

# Tigger the app here at your local server: http://127.0.0.1:8050/
if __name__ == '__main__':
    app.run_server(debug=True)
