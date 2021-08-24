import sqlite3

baza_datoteka = 'vsi_izdelki.db'

def uvoziSQL(cur, datoteka):
    with open(datoteka) as f:
        koda = f.read()
        print(koda)
        try:
            cur.executescript(koda)
        except sqlite3.OperationalError:
            pass

with sqlite3.connect(baza_datoteka) as baza:
    cur = baza.cursor()
    uvoziSQL(cur, 'vsi_izdelki.sql')
