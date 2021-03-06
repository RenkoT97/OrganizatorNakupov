import psycopg2

import csv

from conf_baza import *

conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, dbname, user, password)

def izbrisi():
    with psycopg2.connect(conn_string) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS izdelki CASCADE")
        cur.execute("DROP TABLE IF EXISTS trgovine CASCADE")
        cur.execute("DROP TABLE IF EXISTS osebe CASCADE")
        cur.execute("DROP TABLE IF EXISTS kosarica CASCADE")
    print("Baza je izbrisana!")

def ustvari_tabelo_osebe():
    with psycopg2.connect(conn_string) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS osebe(
                id_uporabnika SERIAL PRIMARY KEY UNIQUE,
                uporabnisko_ime TEXT UNIQUE ,
                geslo TEXT NOT NULL,
                ime TEXT NOT NULL,
                priimek TEXT NOT NULL
                );
        """)
    print("Tabela osebe ustvarjena!")

def ustvari_tabelo_trgovine():
    with psycopg2.connect(conn_string) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trgovine(
                id_trgovine SERIAL PRIMARY KEY,
                ime_trgovine TEXT,
                lokacija TEXT
                );
        """)
    print("Tabela trgovine ustvarjena!")

def ustvari_tabelo_izdelki():
    with psycopg2.connect(conn_string) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS izdelki(
                id_izdelka SERIAL PRIMARY KEY,
                ime_trgovine TEXT, 
                ime_izdelka TEXT ,
                firma TEXT,
                okus TEXT,
                redna_cena INTEGER,
                teza TEXT
                );
        """)
    print("Tabela izdelki ustvarjena!")

def ustvari_tabelo_kosarica():
    with psycopg2.connect(conn_string) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS kosarica(
                id_kosarice SERIAL PRIMARY KEY,
                kolicina INTEGER,
                id_uporabnik INTEGER,
                id_izdelka INTEGER
                );
        """)
    print("Tabela kosarica ustvarjena!")

if __name__ == '__main__':
    izbrisi()
    ustvari_tabelo_osebe()
    ustvari_tabelo_izdelki()
    ustvari_tabelo_trgovine()
    ustvari_tabelo_kosarica()
