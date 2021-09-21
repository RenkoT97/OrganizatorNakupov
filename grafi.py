import dash
import pandas as pd
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from plotly.tools import mpl_to_plotly
import plotly.graph_objects as gobject
from dash import html
import izracuni
import podatki

app = dash.Dash()
colors = {
    'background': 'powderblue',
    'text': 'rgb(255,48,79)'
}

#zgled
dom = izracuni.dom
koordinate = podatki.koordinate
koordinate.append(dom)


pot = izracuni.pot
trgovine = ['spar', 'spar', 'spar', 'spar', 'spar', 'mercator', 'mercator', 'mercator', 'mercator', 'mercator', 'tus', 'tus', 'hofer', 'hofer', 'hofer', 'hofer', 'lidl', 'lidl', 'lidl', 'lidl', 'trenutna lokacija']
izdelki = izracuni.razpredelnica
kolicine = podatki.kolicine

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
        color='rgb(255,48,79)',
        size=50,
        line=dict(color='slategrey', width=1)))
    
    layout = dict(plot_bgcolor='powderblue',
                  paper_bgcolor='powderblue',
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

def cena(nakup):
    return podatki.skupna_cena

def razdalja(nakup):
    return round(podatki.razdalja(nakup),2)

def kilometri(stevilo):
    if stevilo == 1:
        return 'kilometer'
    elif stevilo == 2:
        return 'kilometra'
    elif stevilo == 3 or stevilo == 4:
        return 'kilometre'
    else:
        return 'kilometrov'

def text(cena_nakupa, razdalja, kilometri):
    return """Za zelen nakup boste zapravili {cena}€. Pri nakupovanju boste prevozili {stevilo} {km}.
Spodaj lahko vidite pot nakupa ter seznam izdelkov, ki ga morate kupiti v posamezni trgovini.""".format(cena = cena_nakupa, stevilo = razdalja, km = kilometri)

#izdelki je slovar, kjer ima vsaka trgovina seznam izdelkov

def tabela(izdelki):
    data=[gobject.Table(header=dict(values=[el[0] for el in izdelki],
            line_color='darkslategray', fill_color='rgb(139, 212, 218)'), #176,224,230
                 cells=dict(values=[el[1] for el in izdelki], line_color='darkslategray',
               fill_color='powderblue'))]
    layout = gobject.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
    fig = gobject.Figure(data, layout)
    return fig

def tabela2(kolicine):
    data2=[gobject.Table(header=dict(values=[el[0] for el in kolicine],
            line_color='darkslategray', fill_color='rgb(139, 212, 218)'), #176,224,230
                 cells=dict(values=[el[1] for el in kolicine], line_color='darkslategray',
               fill_color='powderblue'))]
    layout2 = gobject.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
    fig2 = gobject.Figure(data2, layout2)
    return fig2

nakup = []
cena_nakupa = cena(nakup)
razdalja = razdalja(pot)
kilometri = kilometri(razdalja)
pot = izracuni.pot


figure1 = graf(koordinate, pot, trgovine)
figure1.write_image("slike/fig1.svg")

figure2 = tabela(izdelki)
figure2.write_image("slike/fig2.svg")

figure3 = tabela2(kolicine)
figure3.write_image("slike/fig3.svg")
