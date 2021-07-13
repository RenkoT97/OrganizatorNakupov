import psycopg2

import csv

from conf_baza import *

conn_string = "host='{0}' dbname='{1}' user='{2}' password='{3}'".format(host, dbname, user, password)

def izbrisi():
    with psycopg2.connect(conn_string) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS vsi_izdelki CASCADE")
        cur.execute("DROP TABLE IF EXISTS trgovine CASCADE")
        cur.execute("DROP TABLE IF EXISTS osebe CASCADE")
    print("Baza je izbrisana!")

def ustvari_tabelo_osebe():
    with psycopg2.connect(conn_string) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS osebe(
              uporanisko_ime TEXT PRIMARY KEY,
              geslo TEXT NOT NULL
              ime TEXT NOT NULL,
              priimek TEXT NOT NULL,
              );
        """)
    print("Tabela osebe ustvarjena!")

def ustvari_tabelo_trgovine():
    with psycopg2.connect(conn_string) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trgovine(
              id_trgoine TEXT PRIMARY KEY,
              ime_trgovine TEXT,
              lokacija TEXT ,
              );
        """)
    print("Tabela trgovine ustvarjena!")

def ustvari_tabelo_vsi_izdelki():
    with psycopg2.connect(conn_string) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vsi_izdelki(
              id_izdelka TEXT PRIMARY KEY,
              ime_trgovine TEXT, #REFERENCES
              ime_izdelka TEXT ,
              firma TEXT,
              okus TEXT,
              redna_cena INTEGER,
              teza TEXT
              );
        """)
    print("Tabela vsi_izdelki ustvarjena!")
