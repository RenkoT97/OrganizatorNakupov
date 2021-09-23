#Uvoz bottla
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth_public as auth 

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import sqlite3
import numpy
import math
import random
import plotly.graph_objects as gobject
from base64 import b64encode


#KONFIGURACIJA
baza_datoteka = 'organizator_nakupov.db'

#Odkomentiraj, če želiš sporočila o napakah 
debug(True) # za izpise pri razvoju 

#Privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
ROOT = os.environ.get('BOTTLE_ROOT', '/')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

   
# mapa za statične vire (slike,css, ...)
static_dir = "./static"

###################################
#### PRIJAVA in REGISTRACIJA
###################################

@get('/')
def index():
   redirect('/prijava')

# zahtevek GET s formo
@get('/prijava') # lahko tudi @route('/prijava')
def prijavno_okno():
    return template('prijava.html')

# zahtevek POST
@post('/prijava') # or @route('/prijava', method='POST')
def prijava():
    uime = request.forms.get('uime')
    geslo = request.forms.get('geslo')

    if preveri(uime, geslo):
        response.set_header("Set-Cookie", 'username={}'.format(uime))
        redirect('/vsi_izdelki')
    else:
        return '''<p>Napačni podatki za prijavo.
Poskusite <a href="/prijava">še enkrat</a></p>'''


def preveri(uime, geslo):
    cur = baza.cursor()
    cur.execute("SELECT * FROM osebe WHERE uporabnisko_ime=%s AND geslo=%s", (uime, geslo))
    result = cur.fetchone()
    
    return result is not None


@get('/registracija')
def registracijsko_okno():
    return template('registracija.html')

@post('/dodaj_registracija')
def registriraj():
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    uime  = request.forms.get('uime')
    geslo = request.forms.get('geslo')
    ponovno_geslo= request.forms.get('ponovno_geslo')
    cur = baza.cursor()
    if geslo == ponovno_geslo:
        cur.execute("INSERT INTO osebe (uporabnisko_ime,geslo,ime,priimek) VALUES (%s,%s,%s,%s)", (uime, geslo, ime, priimek))
    else:
        return '''<p>Gesli se ne ujemata.Poskusite <a href="/registracija">še enkrat</a></p>'''
    redirect('/prijava')

###################################
#### IZDELKI
###################################

@get('/vsi_izdelki')
def vsi_izdelki():
    cookie_uid = request.get_cookie('username')
    if cookie_uid is None:
        redirect('/prijava')

    cur = baza.cursor()
    cur.execute("SELECT id_izdelka, ime_trgovine, ime_izdelka, firma, okus, redna_cena, teza FROM izdelki")
    return template('vsi_izdelki.html', vsi_izdelki = cur.fetchall())

@post('/vsi_izdelki/search')
def vsi_izdelki_search():
    cookie_uid = request.get_cookie('username')
    if cookie_uid is None: 
        redirect('/prijava')

    search = request.forms.get('search')

    if len(search) == 0:
        redirect('/vsi_izdelki')

    cur = baza.cursor()
    cur.execute("SELECT id_izdelka, ime_trgovine, ime_izdelka, firma, okus, redna_cena, teza FROM izdelki " +
                "WHERE ime_izdelka=%s OR firma=%s OR okus=%s", (search, search, search))
    return template('vsi_izdelki.html', vsi_izdelki = cur.fetchall())


@route('/kosarica')
def kosarica(): 
    cookie_uid = request.get_cookie('username')
    if cookie_uid is None:
        redirect('/prijava')

    cur = baza.cursor()
    cur.execute("SELECT id_uporabnika FROM osebe WHERE osebe.uporabnisko_ime=%s", (cookie_uid,))

    cur.execute("SELECT k.id_izdelka, k.kolicina, v.ime_izdelka FROM kosarica k, izdelki v, osebe o " +
                "WHERE k.id_uporabnik=o.id_uporabnika " +
                "AND o.id_uporabnika=%s " +
                "AND v.id_izdelka=k.id_izdelka", (cur.fetchone(),))
    return template('kosarica.html', kosarica=cur.fetchall())

@post('/kosarica')
def dodaj_kosarica():
    cookie_uid = request.get_cookie('username')
    if cookie_uid is None:
        redirect('/prijava')

    kolicina = request.forms.get('kolicina')
    id_izdelka = request.forms.get('id_izdelka')

    cur = baza.cursor()
    cur.execute("SELECT id_uporabnika FROM osebe WHERE osebe.uporabnisko_ime=%s", (cookie_uid,))

    cur.execute("INSERT INTO kosarica (kolicina, id_izdelka, id_uporabnik) VALUES  (%s, %s, %s)", (kolicina, id_izdelka, cur.fetchone()))
    baza.commit()
    redirect('/kosarica')

@route('/osebe')
def osebe():
    con = sqlite3.connect(baza_datoteka)
    cur = con.cursor()
    osebe = cur.execute("SELECT uporabnisko_ime, geslo, ime, priimek FROM osebe")
    return template('osebe.html', osebe = cur)

# straženje statičnih datotek 
@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)

@get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")

########################################
##### redirect
########################################

#########################################
######## funkcije
#########################################

#########################################
######## za prvo tabelo
#########################################
def preberi_lokacijo():
    x = random.randint(-1,61)
    y = random.randint(-1,41)
    return [x,y]

def pretvornik_trgovin_v_koordinate(slovar_koordinat):
    cur = baza.cursor()
    cur.execute("SELECT * FROM trgovine")
    trgovine = cur.fetchall()
    #print(trgovine)
    kraji = [trgovina[2] for trgovina in trgovine]
    trgovine = [trgovina[1] for trgovina in trgovine]
    koordinate = [slovar_koordinat[kraj] for kraj in kraji]
    return trgovine, koordinate

def id_izdelka_v_opis():
    #vsaka trgovina ima svoj list izdelkov
    cur = baza.cursor()
    cur.execute("SELECT ime_izdelka, firma, okus FROM izdelki")
    vsi_izdelki = cur.fetchall()
    n = len(vsi_izdelki)
    izdelki = [[None for i in range(3)] for i in range(n)]
    for i in range(n):
        for j in range(3):
            a = vsi_izdelki[i][j]
            a = a.replace('_', ' ')
            izdelki[i][j] = a
    return izdelki

def preberi_kosarico(oseba):
    cur = baza.cursor()
    cur.execute(f"SELECT * FROM kosarica")# WHERE id_kosarice={idk}")
    kosarice = cur.fetchall()
    print(kosarice)
    kos = []
    while kosarice:
        a = kosarice.pop()
        print(a)
        if a[2] == oseba:
            print(oseba)
            kos.append(a)
        else:
            return kos       
    return kos 


def trgovine_z_izdelki_f():
    slovar = {'spar':[], 'mercator':[],  'tus':[], 'hofer':[], 'lidl':[]}
    #vsaka trgovina ima svoj list izdelkov
    cur = baza.cursor()
    cur.execute("SELECT id_izdelka, ime_trgovine FROM izdelki")
    vsi_izdelki = cur.fetchall()
    for par in vsi_izdelki:
        slovar[par[1]].append(par[0])
    return slovar

def kombinacije_trgovin_f(mnozica_izdelkov_v_kosarici, seznam_trgovin, trgovine_z_izdelki):
    
    generator_kombinacij = (set(itertools.compress(seznam_trgovin, el)) for el in itertools.product(*[[0,1]]*len(seznam_trgovin)))
    kombinacije = []
    for mnozica_trgovin in generator_kombinacij:
        izdelki_kombinacije = set()
        for trgovina in mnozica_trgovin:
            for izdelek in trgovine_z_izdelki[trgovina]:
                izdelki_kombinacije.add(izdelek) #množica vseh izdelkov, ki jih lahko dobiš v danih trgovinah
        if mnozica_izdelkov_v_kosarici.issubset(izdelki_kombinacije):
            kombinacije.append(mnozica_trgovin)    
    for kombinacija in kombinacije:
        for kombinacija2 in kombinacije:
            if kombinacija.issubset(kombinacija2) and kombinacija != kombinacija2:
                kombinacije.remove(kombinacija2)
            elif kombinacija2.issubset(kombinacija) and kombinacija != kombinacija2:
                kombinacije.remove(kombinacija)
    for kombinacija in kombinacije:
        for kombinacija2 in kombinacije:
            if kombinacija.issubset(kombinacija2) and kombinacija != kombinacija2:
                kombinacije.remove(kombinacija2)
            elif kombinacija2.issubset(kombinacija) and kombinacija != kombinacija2:
                kombinacije.remove(kombinacija)          
    return kombinacije

def lokacije(slovar_koordinat, trgovina):
    sez_lokacij = []
    trgovine, koordinate = pretvornik_trgovin_v_koordinate(slovar_koordinat)
    for i in range(len(trgovine)):
        if trgovine[i] == trgovina:
            sez_lokacij.append(koordinate[i])
    return sez_lokacij

def razdalja(vozlisce1, vozlisce2):
    return math.sqrt((vozlisce2[1] - vozlisce1[1]) ** 2 + (vozlisce2[0] - vozlisce1[0]) ** 2)

def doloci_trgovine(dom, slovar_koordinat, kombinacija):
    skupine = [] #skupine vozlišč iste trgovine
    poti = []
    for trgovina in kombinacija:
        skupine.append(lokacije(slovar_koordinat, trgovina))
    for i in skupine[0]: #skupine[0] je seznam lokacij ene vrste trgovin
        dolzina = razdalja(dom, i)
        if len(kombinacija) > 1:
            for j in skupine[1]:
                dolzina += razdalja(i, j)
                if len(kombinacija) > 2:
                    for k in skupine[2]:
                        dolzina += razdalja(j, k)
                        if len(kombinacija) > 3:
                            for m in skupine[3]:
                                dolzina += razdalja(k, m)
                                if len(kombinacija) > 4:
                                    for n in skupine[4]:
                                        dolzina += razdalja(m, n)
                                        dolzina += razdalja(n, dom)
                                        poti.append([[dom, i, j, k, m, n], dolzina])
                                        dolzina = 0
                                else:
                                    dolzina += razdalja(m, dom)
                                    poti.append([[dom, i, j, k, m], dolzina])
                                    dolzina = 0
                        else:
                            dolzina += razdalja(k, dom)
                            poti.append([[dom, i, j, k], dolzina])
                            dolzina = 0
                else:
                    dolzina += razdalja(j, dom)
                    poti.append([[dom, i, j], dolzina])
                    dolzina = 0
        else:
            dolzina *= 2
            poti.append([[dom, i], dolzina])
            dolzina = 0
    dolzine = [el[1] for el in poti]
    if dolzine == []:
        print("Nakupa ni mogoče opraviti.")
        return None
    mini = numpy.argmin(dolzine)
    return poti[mini] #[[pot], dolzina]

def doloci_pot(dom, seznam_izdelkov, seznam_trgovin, seznam_izdelkov_v_kosarici, trgovine_z_izdelki,slovar_koordinat):
    vozlisca = []
    dolzine = []
    trgovine = []
    for kombinacija in kombinacije_trgovin_f(set(seznam_izdelkov_v_kosarici), seznam_trgovin, trgovine_z_izdelki):
        par = doloci_trgovine(dom, slovar_koordinat, kombinacija)
        dolzine.append(par[1])
        vozlisca.append(par[0])
        trgovine.append(kombinacija)
    if dolzine == []:
        return None
    i = numpy.argmin(dolzine)
    v = vozlisca[i]
    v.append(dom)
    obiskane_trgovine = trgovine[i]
    return v, obiskane_trgovine





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

#########################################
######## za prvo tabelo
#########################################

#########################################
######## za drugo tabelo
#########################################









def razporeditev(obiskane_trgovine, izdelki, slovar):
    izdelki2 = izdelki.copy()
    razporeditev = []
    for trgovina in obiskane_trgovine:
        sez = []
        for izdelek in izdelki:
            if {izdelek}.issubset(slovar[trgovina]):
                izd = id_izdelka_v_opis()[izdelek-1]
                sez.append(izd)
                izdelki2.remove(izdelek)
        razporeditev.append([trgovina, sez])
    return razporeditev



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

#########################################
######## za drugo tabelo
#########################################

#########################################
######## za tretjo tabelo
#########################################

def preberi_kosarico(oseba):
    cur = baza.cursor()
    cur.execute(f"SELECT * FROM kosarica")# WHERE id_kosarice={idk}")
    kosarice = cur.fetchall()
    print(kosarice)
    kos = []
    while kosarice:
        a = kosarice.pop()
        print(a)
        if a[2] == oseba:
            print(oseba)
            kos.append(a)
        else:
            return kos       
    return kos  

def pretvornik_za_tabelo_kolicin():
    slovar = {}
    cur = baza.cursor()
    cur.execute("SELECT id_izdelka, ime_izdelka FROM izdelki")
    izdelki = cur.fetchall()
    for el in izdelki:
        slovar[el[0]] = el[1]
    return slovar


def tabela_kolicin(kosarica, slovar):
    izdelek = []
    kolicina = []
    for el in kosarica:
        izdelek.append(slovar.get(el[3]))
        kolicina.append(el[1])
    tabela = [['izdelek', izdelek], ['kolicina', kolicina]]
    return tabela

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

#########################################
######## za tretjo tabelo
#########################################
def cene():
    cur = baza.cursor()
    cur.execute("SELECT id_izdelka, redna_cena FROM izdelki")
    izdelki = cur.fetchall()
    return izdelki


def cena(cene, kosarica):
    skupna_cena = 0
    for vrstica in kosarica:
        idi = vrstica[3]
        kolicina = vrstica[1]
        cena = cene[idi-1][1]
        skupna_cena += kolicina * cena
    return round(skupna_cena,2)

def razdalja_nova(list_koor):
    #delamo cikel
    razdalja = 0
    list_koordinat = list_koor.copy()
    dom = list_koordinat.pop(0)
    el = dom
    while list_koordinat:
        el2 = list_koordinat.pop(0)
        razdalja += math.sqrt((el[0] - el2[0]) ** 2 + (el[1] - el2[1]) ** 2)
        el = el2
    razdalja += math.sqrt((dom[0] - el2[0]) ** 2 + (dom[0] - el2[0]) ** 2) #vrnemo se domov
    return razdalja

def razdalja_st(nakup):
    return round(razdalja_nova(nakup),2)

def kilometri_st(stevilo):
    if stevilo == 1:
        return 'kilometer'
    elif stevilo == 2:
        return 'kilometra'
    elif stevilo == 3 or stevilo == 4:
        return 'kilometre'
    else:
        return 'kilometrov'


def text(cena_nakupa, razdalja, kilometri):
    return """Za željen nakup boste zapravili {cena}€. Pri nakupovanju boste prevozili {stevilo} {km}.
Spodaj lahko vidite pot nakupa ter seznam izdelkov, ki ga morate kupiti v posamezni trgovini.""".format(cena = cena_nakupa, stevilo = razdalja, km = kilometri)


@get('/potrdi')
def potrdi(): 

    ############### VELJA ZA VSE 
    slovar_koordinat = {'Corfe Alley' : [0,0], 'Highlands Cliff' : [25,8], 'Broad Heights' : [15,30], 'Gibson Loke' : [52,3],
                    'Ellicks Close' : [45,30], 'Hornhatch' : [4, 38], 'Laburnum Lane' : [30, 32], 'Thorpe Leys' : [10, 15],
                    'Waterside Boulevard' : [38,2], 'Millbrook Market' : [55,20], ' Beeches Oak' : [58,12],
                    'Priory Crescent' : [22,18], 'Cromer Point' : [60,40], 'Dingle Close' : [1,20], 'Rydal Square' : [13,3],
                    'Beechcroft Wynd' : [42,10], 'Mount Pleasant Woodlands' : [35,22], 'Priors Bridge' : [18,30],
                    'Bull Isaf' : [31,19], 'Bernard Fairway' : [55,27]}
    seznam_trgovin =["spar", "mercator", "tus", "hofer", "lidl"]
    trgovine = ['spar', 'spar', 'spar', 'spar', 'spar', 'mercator', 'mercator', 'mercator', 'mercator', 'mercator', 
                'tus', 'tus', 'hofer', 'hofer', 'hofer', 'hofer', 'lidl', 'lidl', 'lidl', 'lidl', 'trenutna lokacija']
    cur = baza.cursor()
    cur.execute("SELECT * FROM kosarica")
    kosarice = cur.fetchall()
    oseba = kosarice.pop()[2]
    ############### VELJA ZA VSE 
    ############### PRVA TABELA DELA: KLJUKCA, KLJUKCA  

    ## najprej koordinate
    dom = preberi_lokacijo()
    koordinate = pretvornik_trgovin_v_koordinate(slovar_koordinat)[1]
    koordinate.append(dom)

    ## pot
    # dom mamo že 
    #seznam_izdelkov
    id_in_opis = id_izdelka_v_opis()
    seznam_izdelkov = [el[0] for el in id_in_opis]
 
    #seznam_trgovin - mamo že
    #seznam_izdelkov_v_kosarici
    kosarica = preberi_kosarico(oseba)
    seznam_izdelkov_v_kosarici = [el[3] for el in kosarica]
 
    #trgovine z izdelki
    trgovine_z_izdelki = trgovine_z_izdelki_f()

    pot, obiskane_trgovine = doloci_pot(dom, seznam_izdelkov, seznam_trgovin, seznam_izdelkov_v_kosarici, trgovine_z_izdelki, slovar_koordinat)


    figure1 = graf(koordinate, pot, trgovine)
    figure1.write_image("static/img/fig1.png")
    ############### PRVA TABELA DELA: KLJUKCA, KLJUKCA  

    ############### DRUGA TABELA DELA: 



    ############### obiskane_trgovine ---> imamo ze v prvi tabeli --> kljukca
    


    ############### seznam_izdelkov_v_kosarici

    ############### trgovine_z_izdelki

    izdelki = razporeditev(obiskane_trgovine, seznam_izdelkov_v_kosarici, trgovine_z_izdelki)

    figure2 = tabela(izdelki)
    figure2.write_image("static/img/fig2.png")

    ############### DRUGA TABELA DELA: 


    ############### TRETJA TABELA DELA: KLJUKCA, KLJUKCA  
    cur = baza.cursor()
    cur.execute("SELECT * FROM kosarica")
    kosarice = cur.fetchall()
    oseba = kosarice.pop()[2]
    kosarica = preberi_kosarico(oseba)
 
    slovar_za_tabelo_kolicin = pretvornik_za_tabelo_kolicin()
 
 
    kolicine = tabela_kolicin(kosarica, slovar_za_tabelo_kolicin)
 
    figure3 = tabela2(kolicine)
    figure3.write_image("static/img/fig3.png")
    ############### TRETJA TABELA DELA: KLJUKCA, KLJUKCA  

    ############### cena_nakupa
    cen = cene()
    cena_nakupa = cena(cen,kosarica)
    
    ############### razdalja
    razdalja = razdalja_st(pot)

    ############### kilometri
    kilometri = kilometri_st(razdalja)

    
    besedilo = text(cena_nakupa, razdalja, kilometri)
    return template('potrdi.html', besedilo=besedilo,
                fig1=b64encode(figure1.to_image()),
                fig2=b64encode(figure2.to_image()),
                fig3=b64encode(figure3.to_image()))
    



########################################
##### ODJAVA
########################################

@get('/odjava')
def odjava():
    cookie_uid = request.get_cookie('username')
    if cookie_uid is None:
        redirect('/prijava')

    response.set_header("Set-Cookie", 'username=; Expires=Wed, 21 Oct 2015 07:28:00 GMT')
    redirect('/prijava')
#_________________________________________________________________________________________________________________________________
#POVEZAVA NA BAZO
baza = psycopg2.connect(database=auth.dbname, host=auth.host, user=auth.user, password=auth.password)
baza.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

#Poženemo strežnik na podanih vratih, npr. http://localhost:8080/
run(host='localhost', port=SERVER_PORT, reloader=RELOADER)
