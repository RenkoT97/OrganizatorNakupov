import sqlite3

baza_datoteka = 'organizator_nakupov.db'

CREATE_VSI_IZDELKI = '''
    CREATE TABLE IF NOT EXISTS vsi_izdelki (
        id_izdelka TEXT PRIMARY KEY,
        ime_izdelka TEXT NOT NULL,
        ime_trgovine TEXT NOT NULL,
        firma TEXT,
        okus TEXT,
        redna_cena INTEGER,
        teza INTEGER
    )
'''
      
CREATE_TRGOVINE = '''
    CREATE TABLE IF NOT EXISTS trgovina (
        id INTEGER PRIMARY KEY,
        ime TEXT NOT NULL,
        kraj TEXT NOT NULL
    )
'''

CREATE_OSEBE = '''
    CREATE TABLE IF NOT EXISTS osebe (
        uporabnisko_ime TEXT PRIMARY KEY,
        geslo TEXT NOT NULL,
        ime TEXT NOT NULL,
        priimek TEXT NOT NULL
    )
'''

def uvoziSQL(cur, datoteka):
    with open(datoteka) as file:
        for koda in file:
            #print(koda)
            cur.execute(koda)

with sqlite3.connect(baza_datoteka) as baza:
    cur = baza.cursor()
    cur.execute(CREATE_VSI_IZDELKI)
    cur.execute(CREATE_TRGOVINE)
    cur.execute(CREATE_OSEBE)
    uvoziSQL(cur, 'vsi_izdelki.sql')
    uvoziSQL(cur, 'trgovine.sql')
    uvoziSQL(cur, 'osebe.sql')
    baza.commit()
