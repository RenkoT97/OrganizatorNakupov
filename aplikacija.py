from bottle import *
import sqlite3

#KONFIGURACIJA
baza_datoteka = 'vsi_izdelki.sql'

#Odkomentiraj, če želiš sporočila o napakah 
debug(True) # za izpise pri razvoju 


# zahtevek GET s formo
@get('/prijava') # lahko tudi @route('/prijava')
def prijavno_okno():
    return """
<html>
<head>

<link rel="StyleSheet" type="text/css" href="/static/stili.css" />

</head>

<body>

<h1>Pozdravljeni v</h1>

<img src="/static/img/logo.png" alt="logo" width="450" height="450"> 
<form action="/prijava" method="post">

<div class="prijava-container">
    <span style="font-size:xx-large;text-decoration: underline">Uporabniško ime:</span> <input name="uime" type="text" />
    <span style="font-size:xx-large;text-decoration: underline">Geslo:</span> <input name="geslo" type="password" />
    <input value="Prijava" type="submit" />
</div>

</form>
</body>
</html>
"""

# mapa za statične vire (slike,css, ...)
static_dir = "./static"

# straženje statičnih datotek 
@route("/static/<filename:path>")
def static(filename): 
    return static_file(filename, root=static_dir)



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

@get('vsi_izdelki')





baza = sqlite3.connect(baza_datoteka, isolation_level=None)
baza.set_trace_callback(print) #kakšne SQL stavke pošilja nazaj - izpis SQL stavkov (za debugiranje pri razvoju)
# zapoved upoštevanja omejitev FOREIGN KEY
cur = baza.cursor()
cur.execute("PRAGMA foreign_key = ON;")

# reloader=True nam olajša razvoj (osveževanje sproti - razvoj) 
run(host='localhost', port=8080, debug=True)
