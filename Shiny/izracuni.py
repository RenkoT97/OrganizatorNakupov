import itertools
import numpy
import math

seznam_trgovin =["1", "2", "3"] 
seznam_izdelkov = ["bla1", "bla2"] #seznam nizov

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
def kombinacije_trgovin(seznam_izdelkov, seznam_trgovin):
    generator_kombinacij = (set(itertools.compress(seznam_trgovin, el)) for el in itertools.product(*[[0,1]]*len(seznam_trgovin)))
    kombinacije = []
    for mnozica_trgovin in generator_kombinacij:
        izdelki_kombinacije = set()
        for trgovina in mnozica_trgovin:
            for izdelek in trgovina:
                izdelki_kombinacije.add(izdelek)
        if seznam_izdelkov.issubset(izdelki_kombinacije):
            kombinacije.append(mnozica_trgovin)
    for kombinacija in kombinacije:
        for kombinacija2 in kombinacije:
            if kombinacija.issubset(kombinacija2):
                kombinacije.remove(kombinacija2)
            elif kombinacija2.issubset(kombinacija):
                kombinacije.remove(kombinacija)
    return kombinacije
                
                
    return None

def razdalja(vozlisce1, vozlisce2):
    return math.sqrt((vozlisce2[1] - vozlisce1[1]) ** 2 + (vozlisce2[0] - vozlisce1[0]) ** 2)

#dom = [x,y]    
def doloci_trgovine(dom, seznam_izdelkov, kombinacija):
    skupine = [] #skupine vozlišč iste trgovine
    poti = []
    for trgovina in kombinacija:
        skupine.append(skupina_trgovine) #skupina trgovine je seznam z elementi [trgovina, [x, y]]
    for i in skupine[0]:
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
                                        poti.append([[i, j, k, m, n], dolzina])
                                else:
                                    dolzina += razdalja(m, dom)
                                    poti.append([[i, j, k, m], dolzina])
                        else:
                            dolzina += razdalja(k, dom)
                            poti.append([[i, j, k], dolzina])
                else:
                    dolzina += razdalja(j, dom)
                    poti.append([[i, j], dolzina])
        else:
            dolzina *= 2
            poti.append([[i], dolzina])
    dolzine = [el[1] for el in poti]
    mini = numpy.argmin(dolzine)
    return poti[mini] #[[pot], dolzina]
                                        

        
    return (dolzina, sez_vozlisc)

def doloci_pot(seznam_izdelkov):
    vozlisca = []
    dolzine = []
    for kombinacija in kombinacije_trgovin(seznam_izdelkov, seznam_trgovin):
        par = doloci_trgovine(seznam_izdelkov, kombinacija)
        dolzine.append(par[1])
        vozlisca.append(par[0])
    i = numpy.argmin(dolzine)
    return vozlisca[i]
    
    
