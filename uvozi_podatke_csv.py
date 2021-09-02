import sqlite3
import csv

baza_datoteka = 'organizator_nakupov.db'

def uvoziSQL(cur, datoteka): 
    with open(datoteka) as f:
        koda = f.read()
        cur.executescript(koda)

def uvoziCSV(cur, tabela): 
    with open('Podatki/{0}.csv'.format(tabela)) as csvfile:
        podatki = csv.reader(csvfile)
        vsiPodatki = [vrstica for vrstica in podatki]
        glava = vsiPodatki[0]
        vrstice = vsiPodatki[1:]
        cur.executemany("INSERT INTO {0} ({1}) VALUES ({2})".format(
            tabela, ",".join(glava), ",".join(['?']*len(glava))), vrstice)

#def uvoziCSV(cur, tabela): 
#    with open('Podatki/{0}.csv'.format(tabela)) as csvfile:
#        podatki = csv.reader(csvfile)
#        vsiPodatki = [vrstica for vrstica in podatki]
#        glava = vsiPodatki[0]
#        vrstice = vsiPodatki[1:]
#        sql_text = "INSERT INTO {0} ({1}) VALUES ({2})".format(
#            tabela, ",".join(glava), ",".join(['?']*len(glava)))
#        print(sql_text)
#        cur.executemany(sql_text, vrstice)
        

with sqlite3.connect(baza_datoteka) as baza:
    cur = baza.cursor()
    uvoziCSV(cur, 'vsi_izdelki')
    uvoziCSV(cur, 'trgovine')
    uvoziCSV(cur, 'osebe')