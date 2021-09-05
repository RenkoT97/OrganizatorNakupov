#from sys import ps1
from bottle import *
import sqlite3
import hashlib

#KONFIGURACIJA
baza_datoteka = 'organizator_nakopov.db'

#Odkomentiraj, če želiš sporočila o napakah 
debug(True) # za izpise pri razvoju 

# napakaSporocilo = None

def nastaviSporocilo(sporocilo = None):
    # global napakaSporocilo
    staro = request.get_cookie("sporocilo", secret=skrivnost)
    if sporocilo is None:
        response.delete_cookie('sporocilo')
    else:
        response.set_cookie('sporocilo', sporocilo, path="/", secret=skrivnost)
    return staro 
   
# mapa za statične vire (slike,css, ...)
static_dir = "./static"

#skrivnost =  <---- to ne vem kaj je

###################################
#### PRIJAVA in REGISTRACIJA
###################################

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
        return "<p>Dobrodošel {0}.</p>".format(uime)
    else:
        return '''<p>Napačni podatki za prijavo.
Poskusite <a href="/prijava">še enkrat</a></p>'''


def preveri(uime, geslo):
    return uime=="janez" and geslo=="kranjski"

@get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")

@get('/registracija')
def prijavno_okno():
    return template('registracija.html')



###################################
#### IZDELKI
###################################

@get('/vsi_izdelki')
def vsi_izdelki(): 
    cur = baza.cursor()
    vsi_izdelki = cur.execute("SELECT id_izdelka, ime_trgovine, ime_izdelka, firma, okus, redna_cena, teza FROM vsi_izdelki")
    return template('vsi_izdelki.html', vsi_izdelki = vsi_izdelki)


# straženje statičnih datotek 
@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)


baza = sqlite3.connect(baza_datoteka, isolation_level=None)
baza.set_trace_callback(print) #kakšne SQL stavke pošilja nazaj - izpis SQL stavkov (za debugiranje pri razvoju)
# zapoved upoštevanja omejitev FOREIGN KEY
cur = baza.cursor()
cur.execute("PRAGMA foreign_key = ON;")

# reloader=True nam olajša razvoj (osveževanje sproti - razvoj) 
run(host='localhost', port=8080, debug=True)
