import dash
import pandas as pd
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from plotly.tools import mpl_to_plotly
import plotly.graph_objects as gobject

app = dash.Dash()
colors = {
    'background': '#FFFFFF',
    'text': '#b83d57'
}

#zgled
koordinate = [(1,1), (2,5), (7,3), (-3,4), (2,3), (7,8)]
pot = [(1,1), (2,5), (7,3), (1,1)] #cikel: zaporedna vozlisca
trgovine = ["dom", "lidl", "tus", "hofer", "spar", "tus"]
izdelki = [['spar', ['cokolada', 'marcipan', 'maslo']], ['lidl', ['mleko']], ['tus', ['kruh', 'kvas']]]

def graf(koordinate, pot, trgovine):
    x_koor = [k[0] for k in koordinate]
    y_koor = [k[1] for k in koordinate]
    xr_koor = [k[0] for k in pot]
    yr_koor = [k[1] for k in pot]
    
    robovi = gobject.Scatter(
    x = xr_koor, y = yr_koor,
    line=dict(color='black', width=1),
    hoverinfo='none',
    showlegend=False,
    mode='lines')

    vozlisca = gobject.Scatter(
    x = x_koor, y = y_koor, text=trgovine,
    mode='markers+text',
    showlegend=False,
    hoverinfo='none',
    marker=dict(
        color='pink',
        size=50,
        line=dict(color='black', width=1)))
    
    layout = dict(plot_bgcolor='antiquewhite',
                  paper_bgcolor='white',
                  margin=dict(t=10, b=10, l=10, r=10, pad=0),
                  xaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True),
                  yaxis=dict(linecolor='black',
                             showgrid=False,
                             showticklabels=False,
                             mirror=True))

    fig = gobject.Figure(data=[robovi, vozlisca], layout=layout)
    return fig

#izdelki je slovar, kjer ima vsaka trgovina seznam izdelkov

def tabela(izdelki):
    fig = gobject.Figure(data=[gobject.Table(header=dict(values=[el[0] for el in izdelki],
            line_color='darkslategray', fill_color='wheat'),
                 cells=dict(values=[el[1] for el in izdelki], line_color='darkslategray',
               fill_color='antiquewhite'))])
    return fig
   

app.layout = dash.html.Div(style={'backgroundColor': colors['background']}, id = 'parent',
                           children = [
    dash.html.Div([
    dash.html.H1(id = 'H1', children = 'Načrt poti', style = {'textAlign':'center',
                                                         'color': colors['text'],
                                                        'marginTop':40,'marginBottom':40}),
        
        dash.dcc.Graph(id = 'line_plot', figure = graf(koordinate, pot, trgovine))
    ]),

    dash.html.Div([
        
    dash.html.H1(id = 'H2', children = 'Razpredelnica izdelkov', style = {'textAlign':'center',
                                                         'color': colors['text'],
                                                        'marginTop':40,'marginBottom':40}),
        
        dash.dcc.Graph(id = 'line_pl', figure = tabela(izdelki))
    ])


    ])


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)

