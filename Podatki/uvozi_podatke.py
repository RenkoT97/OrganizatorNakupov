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
        

def uvoziSQL(cur, datoteka):
    with open(datoteka) as f:
        koda = f.read()
        print(koda)
        try:
            cur.executescript(koda)
        except sqlite3.OperationalError as error:
            print('error')
            print(error)

with sqlite3.connect(baza_datoteka) as baza:
    cur = baza.cursor()
    cur.execute(CREATE_VSI_IZDELKI)
    uvoziSQL(cur, 'vsi_izdelki.sql')
    #uvoziSQL(cur, 'trgovine.sql')
    #uvoziSQL(cur, 'osebe.sql')
