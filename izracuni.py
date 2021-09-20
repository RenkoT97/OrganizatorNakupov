import itertools
import numpy
import math
import psycopg2
import podatki

baza = podatki.baza
dom = podatki.preberi_lokacijo()
seznam_trgovin =["spar", "mercator", "tus", "hofer", "lidl"]
id_in_opis = podatki.id_izdelka_v_opis(baza) #[(1, 'cokolada'), ...]
seznam_izdelkov = [el[0] for el in id_in_opis] #['cokolada', 'sladoled', ...]
mnozica_izdelkov = set(seznam_izdelkov)
trgovine_z_izdelki = podatki.trgovine_z_izdelki_f(baza) #slovar: {'trgovina':['id1', 'id2'],...}
seznam_izdelkov_v_kosarici = [el[3] for el in podatki.kosarica]
'''
def zemljevid_trgovin(trgovine):
    sez = []
    for trgovina in trgovine:
        sez.append([trgovina, [])

def kombinacije_trgovin(seznam_izdelkov):
    sez_kombinacij = []
    for trgovina in trgovine:
        kombinacija = []
        izdelki = sez_izdelkov
        for izdelek in izdelki:
            if izdelek in trgovina:
                izdelki = izdelki.remove(izdelek)
'''
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
                
                
    return None

def razdalja(vozlisce1, vozlisce2):
    return math.sqrt((vozlisce2[1] - vozlisce1[1]) ** 2 + (vozlisce2[0] - vozlisce1[0]) ** 2)

#dom = [x,y]    
def doloci_trgovine(dom, baza, slovar_koordinat, seznam_izdelkov, kombinacija):
    skupine = [] #skupine vozlišč iste trgovine
    poti = []
    for trgovina in kombinacija:
        skupine.append(podatki.lokacije(baza, slovar_koordinat, trgovina))
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
                                        

        
    return (dolzina, sez_vozlisc)

def doloci_pot(dom, seznam_izdelkov, seznam_trgovin, seznam_izdelkov_v_kosarici, trgovine_z_izdelki):
    vozlisca = []
    dolzine = []
    trgovine = []
    for kombinacija in kombinacije_trgovin_f(set(seznam_izdelkov_v_kosarici), seznam_trgovin, trgovine_z_izdelki):
        par = doloci_trgovine(dom, baza, slovar_koordinat, seznam_izdelkov, kombinacija)
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

def razporeditev(obiskane_trgovine, izdelki, slovar):
    izdelki2 = izdelki.copy()
    razporeditev = []
    for trgovina in obiskane_trgovine:
        sez = []
        for izdelek in izdelki:
            if {izdelek}.issubset(slovar[trgovina]):
                izd = podatki.id_izdelka_v_opis(baza)[izdelek-1]
                sez.append(izd)
                izdelki2.remove(izdelek)
        razporeditev.append([trgovina, sez])
    return razporeditev
    
baza.commit()

slovar_koordinat = podatki.slovar_koordinat

kombinacije_trgovin = kombinacije_trgovin_f(set(seznam_izdelkov_v_kosarici), seznam_trgovin, trgovine_z_izdelki)
#print(kombinacije_trgovin)'
pot, obiskane_trgovine = doloci_pot(dom, seznam_izdelkov, seznam_trgovin, seznam_izdelkov_v_kosarici, trgovine_z_izdelki)
razpredelnica = razporeditev(obiskane_trgovine, seznam_izdelkov_v_kosarici, podatki.trgovine_z_izdelki)
