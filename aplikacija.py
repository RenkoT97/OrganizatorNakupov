#Uvoz bottla
from bottle import *

# uvozimo ustrezne podatke za povezavo
import auth_public as auth 
#from Baza import conf_baza as auth

# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import hashlib
import sqlite3
import runpy


#KONFIGURACIJA
baza_datoteka = 'organizator_nakupov.db'

#Odkomentiraj, če želiš sporočila o napakah 
debug(True) # za izpise pri razvoju 

#Privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
ROOT = os.environ.get('BOTTLE_ROOT', '/')
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)


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

import sys
#from pathlib import Path
#sys.path.append(str(Path().cwd().Shiny))
import izracuni
import podatki
from app import *


@get('/odpri')
def odpri():
    exec(open("app.py").read())
    redirect('/vsi_izdelki')



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
