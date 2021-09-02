DROP TABLE IF EXISTS vsi_izdelki;
DROP TABLE IF EXISTS trgovine; 
DROP TABLE IF EXISTS osebe; 

CREATE TABLE vsi_izdelki(
    id_izdelka    CHAR PRIMARY KEY, 
    ime_trgovine  CHAR NOT NULL,
    ime_izdelka   CHAR NOT NULL,
    firma         CHAR NOT NULL,
    okus          CHAR NOT NULL,
    redna_cena    INTEGER NOT NULL, 
    teza          CHAR NOT NULL
);


CREATE TABLE trgovine(
    id           INTEGER PRIMARY KEY, 
    ime          CHAR NOT NULL,
    kraj         CHAR NOT NULL
); 



CREATE TABLE osebe(
    uporabnisko_ime CHAR PRIMARY KEY, 
    geslo           CHAR NOT NULL,
    ime             CHAR NOT NULL,
    priimek         CHAR NOT NULL
); 