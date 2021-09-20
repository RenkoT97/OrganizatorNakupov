import psycopg2
import math
import random
import sys
from pathlib import Path
sys.path.append(str(Path().cwd().parent))
import auth_public as auth
#from Baza import conf_baza
#Rabiš:
#za vsako trgovino seznam izdelkov
#seznam trgovin z lokacijami

def pridobi_uporabnika():
    kosarica = []
    cur = baza.cursor()
    cur.execute("SELECT * FROM kosarica")
    kosarice = cur.fetchall()
    return kosarice.pop()[2]

def pridobi_id_kosarice(uporabnik):
    kosarica = []
    cur = baza.cursor()
    cur.execute(f"SELECT * FROM kosarica WHERE id_uporabnik = {uporabnik}")
    kosarice = cur.fetchall()
    zadnja_vrstica = kosarice.pop()
    return zadnja_vrstica[0]

def cene(baza):
    cur = baza.cursor()
    cur.execute("SELECT id_izdelka, redna_cena FROM izdelki")
    izdelki = cur.fetchall()
    return izdelki

def pretvornik_trgovin_v_koordinate(baza, slovar_koordinat):
    cur = baza.cursor()
    cur.execute("SELECT * FROM trgovine")
    trgovine = cur.fetchall()
    #print(trgovine)
    kraji = [trgovina[2] for trgovina in trgovine]
    trgovine = [trgovina[1] for trgovina in trgovine]
    koordinate = [slovar_koordinat[kraj] for kraj in kraji]
    return trgovine, koordinate

def lokacije(baza, slovar_koordinat, trgovina):
    sez_lokacij = []
    trgovine, koordinate = pretvornik_trgovin_v_koordinate(baza, slovar_koordinat)
    for i in range(len(trgovine)):
        if trgovine[i] == trgovina:
            sez_lokacij.append(koordinate[i])
    return sez_lokacij

def trgovine_z_izdelki_f(baza):
    slovar = {'spar':[], 'mercator':[],  'tus':[], 'hofer':[], 'lidl':[]}
    #vsaka trgovina ima svoj list izdelkov
    cur = baza.cursor()
    cur.execute("SELECT id_izdelka, ime_trgovine FROM izdelki")
    vsi_izdelki = cur.fetchall()
    for par in vsi_izdelki:
        slovar[par[1]].append(par[0])
    return slovar

def preberi_kosarico(baza, oseba):
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

def preberi_lokacijo():
    x = random.randint(-1,61)
    y = random.randint(-1,41)
    return [x,y]

def razdalja(list_koor):
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

def cena(cene, kosarica):
    skupna_cena = 0
    for vrstica in kosarica:
        idi = vrstica[3]
        kolicina = vrstica[1]
        cena = cene[idi-1][1]
        skupna_cena += kolicina * cena
    return round(skupna_cena,2)
    
def id_izdelka_v_opis(baza):
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

def pretvornik_za_tabelo_kolicin(baza):
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


baza = psycopg2.connect(database=auth.dbname, host=auth.host, user=auth.user, password=auth.password)

slovar_koordinat = {'Corfe Alley' : [0,0], 'Highlands Cliff' : [25,8], 'Broad Heights' : [15,30], 'Gibson Loke' : [52,3],
                    'Ellicks Close' : [45,30], 'Hornhatch' : [4, 38], 'Laburnum Lane' : [30, 32], 'Thorpe Leys' : [10, 15],
                    'Waterside Boulevard' : [38,2], 'Millbrook Market' : [55,20], ' Beeches Oak' : [58,12],
                    'Priory Crescent' : [22,18], 'Cromer Point' : [60,40], 'Dingle Close' : [1,20], 'Rydal Square' : [13,3],
                    'Beechcroft Wynd' : [42,10], 'Mount Pleasant Woodlands' : [35,22], 'Priors Bridge' : [18,30],
                    'Bull Isaf' : [31,19], 'Bernard Fairway' : [55,27]}

slovar_za_tabelo_kolicin = pretvornik_za_tabelo_kolicin(baza)
oseba = pridobi_uporabnika()
trgovine, koordinate = pretvornik_trgovin_v_koordinate(baza, slovar_koordinat)
trgovine_z_izdelki = trgovine_z_izdelki_f(baza)
idk = pridobi_id_kosarice(oseba)
kosarica = preberi_kosarico(baza, oseba)
skupna_cena = cena(cene(baza),kosarica)
kolicine = tabela_kolicin(kosarica, slovar_za_tabelo_kolicin)
baza.commit()
