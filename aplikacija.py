#from sys import ps1
from bottle import *
import psycopg2
import hashlib
import sqlite3
from Baza import conf_baza
import auth_public as auth 


#KONFIGURACIJA
baza_datoteka = 'organizator_nakupov.db'

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
        redirect('/vsi_izdelki')
    else:
        return '''<p>Napačni podatki za prijavo.
Poskusite <a href="/prijava">še enkrat</a></p>'''


def preveri(uime, geslo):
    cur = baza.cursor()
    cur.execute("SELECT * FROM osebe WHERE uporanisko_ime=%s AND geslo=%s", (uime, geslo))
    result = cur.fetchone()
    
    return result is not None

@get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")

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
        cur.execute("INSERT INTO osebe (uporanisko_ime,geslo,ime,priimek) VALUES (%s,%s,%s,%s)", (uime, geslo, ime, priimek))
    else:
        return '''<p>Gesli se ne ujemata.Poskusite <a href="/registracija">še enkrat</a></p>'''
    redirect('/prijava')

###################################
#### IZDELKI
###################################

@get('/vsi_izdelki')
def vsi_izdelki():
    cur = baza.cursor()
    cur.execute("SELECT id_izdelka, ime_trgovine, ime_izdelka, firma, okus, redna_cena, teza FROM vsi_izdelki")
    return template('vsi_izdelki.html', vsi_izdelki = cur.fetchall())

@post('/vsi_izdelki/search')
def vsi_izdelki_search():
    search = request.forms.get('search')

    if len(search) == 0:
        redirect('/vsi_izdelki')

    cur = baza.cursor()
    cur.execute("SELECT id_izdelka, ime_trgovine, ime_izdelka, firma, okus, redna_cena, teza FROM vsi_izdelki " +
                "WHERE ime_izdelka=%s OR firma=%s OR okus=%s", (search, search, search))
    return template('vsi_izdelki.html', vsi_izdelki = cur.fetchall())

# @post('vsi_izdelki/dodaj')
# def dodaj_izdelke():
#     id_izdelka = request.forms.get('id_izdelka')
#     ime_trgovine = request.forms.get('ime_trgovine')
#     ime_izdelka = request.forms.get('ime_izdelka')
#     firma = request.forms.get('firma')
#     okus = request.forms.get('okus')
#     redna_cena = request.forms.get('redna_cena')
#     teza = request.forms.get('teza')
#     cur = baza.cursor()
#     cur.execute("INSERT INTO vsi_izdelki (id_izdelka, ime_trgovine, ime_izdelka, firma, okus, redna_cena, teza) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id_izdelka, ime_trgovine, ime_izdelka, firma, okus, redna_cena, teza))
#     redirect('/vsi_izdelki')

@get('/kosarica')
def kosarica(): 
    return template('kosarica.html')

@post('/dodaj_kosarica')
def dodaj_kosarica():
    kolicina = request.forms.get('kolicina')
    id_izdelka = request.forms.get('id_izdelka')
    #uporabnik = request.forms.get('uporabnik')
    #
    #kako dobiš uporabnika vn --> nekak si ga shran 
    cur = baza.cursor()
    cur.execute("INSERT INTO kosarica (id,kolicina,id_izdelka,uporabnik) VALUES (%s,%s,%s,%s)", (neki, kolicina, id_izdelka, neki_neki))
    return template('kosarica.html')



@get('/osebe')
def osebe():
    con = sqlite3.connect(baza_datoteka)
    cur = con.cursor()
    osebe = cur.execute("SELECT uporabnisko_ime, geslo, ime, priimek FROM osebe")
    return template('osebe.html', osebe = cur)

# straženje statičnih datotek 
@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)

#_________________________________________________________________________________________________________________________________
#POVEZAVA NA BAZO
baza = psycopg2.connect(database=auth.dbname, host=auth.host, user=auth.user, password=auth.password)
cur = baza.cursor()
print(cur)
cur.execute("SELECT * FROM vsi_izdelki")
vsi_izdelki = cur.fetchall()
print(vsi_izdelki.pop())
template('vsi_izdelki.html', vsi_izdelki=vsi_izdelki)
print('tp')
baza.commit()

# reloader=True nam olajša razvoj (osveževanje sproti - razvoj) 
run(host='localhost', port=8080, debug=True)
