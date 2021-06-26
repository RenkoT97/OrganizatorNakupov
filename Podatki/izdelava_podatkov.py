import csv 

with open('izdelki_spar.csv','w',newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    data = [["'id_izdelka'","'ime_izdelka'","'firma'","'okus'", "'redna_cena'", "'teza'"],
            ["-","'cokolada'","'milka'","'mlecna'","1.19","'100_g'"],
            ["-","'cokolada'","'milka'","'celi_lesniki'","1.14","'100_g'"],
            ["-","'cokolada'","'milka'","'bela'","1.19","'100_g'"],
            ["-","'mleko'","'alpsko_mleko'","'3,5%'","1.14","'1_l'"],
            ["-","'mleko'","'alpsko_mleko'","'1,5%'","1.14","'1_l'"],
            ["-","'mleko'","'lejko_mlejko'","'1,5%'","0.99","'1_l'"],
            ["-","'mleko'","'trajno_mleko'","'3,5%'","1.13","'1_l'"],
            ["-","'mleko'","'trajno_mleko'","'1,5%'","1.14","'1_l'"],
            ["-","'moka'","'mlin_katic'","'psenicna_posebna_bela_moka'","0.74","'1_kg'"],
            ["-","'moka'","'mlin_katic'","'psenicna_bela_moka'","0.65","'1_kg'"],
            ["-","'moka'","'mlin_katic'","'ajdova_moka'","2.99","'1_kg'"]
            ]
    a.writerows(data)

with open('izdelki_mercator.csv','w',newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    data = [["'id_izdelka'","'ime_izdelka'","'firma'","'okus'", "'redna_cena'", "'teza'"],
            ["-","'cokolada'","'milka'","'mlecna'","2.79","'250_g'"],
            ["-","'cokolada'","'milka'","'celi_lesniki'","1.14","'100_g'"],
            ["-","'cokolada'","'milka'","'bela'","1.24","'100_g'"],
            ["-","'mleko'","'alpsko_mleko'","'3,5%'","1.14","'1_l'"],
            ["-","'mleko'","'alpsko_mleko'","'1,5%'","1.14","'1_l'"], #tle zna bit neki cenej
            ["-","'mleko'","'trajno_mlekO_zelene_doline'","'3,5%'","1.19","'1_l'"],
            ["-","'mleko'","'trajno_mlekO_zelene_doline'","'1,5%'","1.14","'1_l'"],
            ["-","'moka'","'mlin_katic'","'psenicna_bela_moka'","0.66","'1_kg'"],
            ["-","'moka'","'mlinotest'","'psenicna_mehka_moka'","1.19","'1_kg'"]
            ]
    a.writerows(data)

with open('izdelki_tus.csv','w',newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    data = [["'id_izdelka'","'ime_izdelka'","'firma'","'okus'", "'redna_cena'", "'teza'"],
            ["-","'cokolada'","'milka'","'mlecna'","2.99","'250_g'"],
            ["-","'cokolada'","'milka'","'celi_lesniki'","2.97","'250_g'"],
            ["-","'mleko'","'alpsko_mleko'","'3,5%'","1.07","'1_l'"],
            ["-","'moka'","'mlin_katic'","'psenicna_posebna_bela_moka'","0.74","'1_kg'"],
            ["-","'moka'","'mlin_katic'","'psenicna_bela_moka'","0.65","'1_kg'"],
            ["-","'moka'","'mlin_katic'","'ajdova_moka'","2.99","'1_kg'"]
            ]
    a.writerows(data)
