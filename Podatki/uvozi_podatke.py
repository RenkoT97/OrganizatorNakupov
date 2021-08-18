import sqlite3

#zdej se mormo priklopit na bazo

baza_datoteka = 'vsi_izdelki.db' #al .sql  to mi mal ni jasn kaj je 


def uvoziSQL(cur, datoteka):
    with open(datoteka) as f:
        koda = f.red()
        cc.executescript(koda)

with sqlite3.connect(baza_datoteka) as baza:
    cur = baza.cursor()
    uvoziSQL(cur, 'vsi_izdelki.sql')
# sam mi nč ne piše notri 
