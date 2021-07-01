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
            ["-","'moka'","'mlin_katic'","'ajdova_moka'","2.99","'1_kg'"],
            ["-","'kruh'","'zito'","'ajdov_kruh_z_orehi'","1.99","'0.4_kg'"],
            ["-","'kruh'","'zito'","'jelenov_mesani'","3.55","'1_kg'"],
            ["-","'kruh'","'zito'","'zlati_hlebec_crni'","3.75","'1_kg'"],
            ["-","'pivo'","'union'","'svetlo_pivo_steklenica'","1.14","'0.5_l'"],
            ["-","'pivo'","'union'","'svetlo_pivo_plocevinka'","1.09","'0.5_l'"],
            ["-","'pivo'","'union'","'svetlo_pivo_steklenica'","0.94","'0.33_l'"],
            ["-","'pivo'","'lasko'","'svetlo_pivo_steklenica'","1.14","'0.5_l'"],
            ["-","'pivo'","'lasko'","'svetlo_pivo_plocevinka'","1.09","'0.5_l'"],
            ["-","'pivo'","'lasko'","'svetlo_pivo_steklenica'","0.94","'0.33_l'"],
            ["-","'pivo'","'union'","'nefiltrirano_steklenica'","1.24","'0.5_l'"],
            ["-","'pivo'","'union'","'nefiltrirano_plocevinka'","1.29","'0.5_l'"],
            ["-","'pivo'","'heineken'","'brezalkoholno_0.0_plocevinka'","0.99","'0.33_l'"],
            ["-","'pivo'","'union'","'brezalkoholno_0.0_steklenica'","0.67","'0.5_l'"],
            ["-","'pivo'","'union'","'brezalkoholno_0.0_plocevinka'","0.73","'0.5_l'"],
            ["-","'pivo'","'heineken'","'svetlo_pivo_plocevinka'","0.99","'0.33_l'"],
            ["-","'pivo'","'union'","'temno_nefiltrirano_steklenica'","1.29","'0.5_l'"],
            ["-","'pivo'","'union'","'temno_nefiltrirano_plocevinka'","1.36","'0.5_l'"],
            ["-","'sok'","'fructal'","'borovnica_superior'","2.48","'1_l'"],
            ["-","'sok'","'fructal'","'crni_ribez_superior'","1.40","'1_l'"],
            ["-","'sok'","'fructal'","'hruska_superior'","1.55","'1_l'"],
            ["-","'sok'","'fructal'","'marelica_superior'","1.55","'1_l'"],
            ["-","'sok'","'fructal'","'jagoda_superior'","2.22","'1_l'"],
            ["-","'sok'","'fructal'","'ananas_superior'","2.08","'1_l'"],
            ["-","'sok'","'fructal'","'breskev_superior'","1.68","'1_l'"],
            ["-","'sok'","'sola'","'ledeni_caj_breskev'","0.99","'1.5_l'"],
            ["-","'sok'","'sola'","'ledeni_caj_breskev'","0.54","'0.5_l'"],
            ["-","'sok'","'sola'","'ledeni_caj_breskev'","0.49","'0.33_l'"],
            ["-","'sok'","'spar'","'ledeni_caj_breskev'","0.58","'1.5_l'"],
            ["-","'sok'","'s_budget'","'ledeni_caj_breskev'","0.49","'1.5_l'"],
            ["-","'sok'","'sola'","'ledeni_caj_brusnica'","0.99","'1.5_l'"],
            ["-","'sok'","'spar'","'ledeni_caj_brusnica'","0.58","'1.5_l'"],
            ["-","'sok'","'fructal'","'ledeni_caj_breskev'","1.09","'1.5_l'"],
            ["-","'sok'","'fructal'","'ledeni_caj_breskev'","0.59","'0.5_l'"],
            ["-","'sadje'","'-'","'banana'","1.29","'1_kg'"],
            ["-","'sadje'","'-'","'lubenica'","0.69","'1_kg'"],
            ["-","'sadje'","'-'","'limona'","1.99","'1_kg'"],
            ["-","'sadje'","'-'","'kivi'","3.99","'1_kg'"],
            ["-","'sadje'","'-'","'melona'","1.69","'1_kg'"],
            ["-","'sadje'","'-'","'marelice'","2.49","'1_kg'"],
            ["-","'sadje'","'-'","'cesnje'","5.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'korenje'","0.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'ohrovt'","1.39","'1_kg'"],
            ["-","'zelenjava'","'-'","'rdeca_paprika'","2.49","'1_kg'"],
            ["-","'zelenjava'","'-'","'por'","2.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'solata_endivja'","1.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'cebula'","0.89","'1_kg'"],
            ["-","'zelenjava'","'-'","'cesen'","5.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'rumena_paprika'","2.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'brokoli'","2.49","'1_kg'"],
            ["-","'zelenjava'","'-'","'rdeci_radic'","2.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'paradiznik'","1.99","'1_kg'"],
            ["-","'sladoled'","'ljubljanske_mlekarne'","'kakav_in_vanilija_otocec'","3.95","'1_l'"],
            ["-","'sladoled'","'ljubljanske_mlekarne'","'cokolada_piran'","4.18","'1_l'"],
            ["-","'sladoled'","'ljubljanske_mlekarne'","'vanilija_cokolada_piran'","6.29","'2_l'"],
            ["-","'sladoled'","'ljubljanske_mlekarne'","'vanilija_jagoda_piran'","6.29","'2_l'"],
            ["-","'sladoled'","'ledo'","'quattro_classic'","4.43","'0.9_l'"],
            ["-","'sladoled'","'ledo'","'quattro_banana_split'","3.99","'0.9_l'"],
            ["-","'sladoled'","'ledo'","'quattro_chocomania'","3.99","'0.9_l'"],
            ["-","'sladoled'","'ledo'","'quattro_rhapsody'","3.99","'0.9_l'"],
            ["-","'sladoled'","'ledo'","'quattro_jaffa'","3.99","'0.9_l'"],
            ["-","'cips'","'chio'","'paprika'","1.69","'0.125_kg'"],
            ["-","'cips'","'chio_exxtra'","'sol'","1.69","'0.125_kg'"],
            ["-","'cips'","'chio_exxtra'","'sol'","1.69","'0.125_kg'"],
            ["-","'cips'","'chio'","'paprika'","1.99","'0.150_kg'"],
            ["-","'cips'","'chio'","'s_sirom'","1.99","'0.150_kg'"],
            ["-","'cips'","'chio'","'kisla_smetana_in_cebula'","1.99","'0.150_kg'"],
            ["-","'cips'","'chio'","'slan'","1.51","'0.150_kg'"],
            ["-","'cips_tortilija'","'spar'","'koruzna'","0.89","'0.125_kg'"],
            ["-","'cips'","'spar'","'paprika'","1.05","'0.170_kg'"]
            ]
    a.writerows(data)

with open('izdelki_mercator.csv','w',newline='') as fp1:
    a = csv.writer(fp1, delimiter=',')
    data = [["'id_izdelka'","'ime_izdelka'","'firma'","'okus'", "'redna_cena'", "'teza'"],
            ["-","'cokolada'","'milka'","'mlecna'","2.79","'250_g'"],
            ["-","'cokolada'","'milka'","'celi_lesniki'","1.14","'100_g'"],
            ["-","'cokolada'","'milka'","'bela'","1.24","'100_g'"],
            ["-","'mleko'","'alpsko_mleko'","'3,5%'","1.14","'1_l'"],
            ["-","'mleko'","'alpsko_mleko'","'1,5%'","1.14","'1_l'"], #tle zna bit neki cenej
            ["-","'mleko'","'trajno_mlekO_zelene_doline'","'3,5%'","1.19","'1_l'"],
            ["-","'mleko'","'trajno_mlekO_zelene_doline'","'1,5%'","1.14","'1_l'"],
            ["-","'moka'","'mlin_katic'","'psenicna_bela_moka'","0.66","'1_kg'"],
            ["-","'moka'","'mlinotest'","'psenicna_mehka_moka'","1.19","'1_kg'"],
            ["-","'kruh'","'zito'","'ajdov_kruh_z_orehi'","2.19","'0.4_kg'"],
            ["-","'kruh'","'zito'","'polbeli_jelenov_kruh'","3.39","'1_kg'"],  
            ["-","'kruh'","'zito'","'stoletni_kruh_s_semeni'","3.59","'0.75_kg'"],
            ["-","'kruh'","'zito'","'mesani_hlebec_hribovc'","3.49","'1_kg'"],
            ["-","'kruh'","'zito'","'mesani_koruzni_kruh'","1.59","'0.5_kg'"],
            ["-","'kruh'","'zito'","'polnozrnati_jelenov_kruh'","3.39","'1_kg'"],
            ["-","'kruh'","'zito'","'mesani_kruh_krusnik'","2.79","'0.75_kg'"],
            ["-","'kruh'","'zito'","'jelenov_beli_kruh'","3.39","'1_kg'"],
            ["-","'kruh'","'zito'","'beli_kruh_hribovc'","3.49","'1_kg'"],



            ["-","'pivo'","'union'","'svetlo_pivo_steklenica'","1.14","'0.5_l'"],
            ["-","'pivo'","'union'","'svetlo_pivo_plocevinka'","1.09","'0.5_l'"],
            ["-","'pivo'","'union'","'svetlo_pivo_steklenica'","0.94","'0.33_l'"],
            ["-","'pivo'","'lasko'","'svetlo_pivo_steklenica'","1.14","'0.5_l'"],
            ["-","'pivo'","'lasko'","'svetlo_pivo_plocevinka'","1.09","'0.5_l'"],
            ["-","'pivo'","'lasko'","'svetlo_pivo_steklenica'","0.94","'0.33_l'"],
            ["-","'pivo'","'union'","'nefiltrirano_steklenica'","1.24","'0.5_l'"],
            ["-","'pivo'","'union'","'nefiltrirano_plocevinka'","1.29","'0.5_l'"],
            ["-","'pivo'","'heineken'","'brezalkoholno_0.0_plocevinka'","0.99","'0.33_l'"],
            ["-","'pivo'","'union'","'brezalkoholno_0.0_steklenica'","0.67","'0.5_l'"],
            ["-","'pivo'","'union'","'brezalkoholno_0.0_plocevinka'","0.73","'0.5_l'"],
            ["-","'pivo'","'heineken'","'svetlo_pivo_plocevinka'","0.99","'0.33_l'"],
            ["-","'pivo'","'union'","'temno_nefiltrirano_steklenica'","1.29","'0.5_l'"],
            ["-","'pivo'","'union'","'temno_nefiltrirano_plocevinka'","1.36","'0.5_l'"],














            
            ["-","'sadje'","'derby'","'banana'","1.29","'1_kg'"],
            ["-","'sadje'","'-'","'lubenica'","0.89","'1_kg'"],
            ["-","'sadje'","'-'","'limona'","1.69","'1_kg'"],
            ["-","'sadje'","'-'","'kivi'","3.69","'1_kg'"],
            ["-","'sadje'","'-'","'melona'","1.99","'1_kg'"],
            ["-","'sadje'","'-'","'marelice'","2.89","'1_kg'"],
            ["-","'sadje'","'-'","'cesnje'","2.99","'0.5_kg'"],
            ["-","'zelenjava'","'-'","'korenje'","1.09","'1_kg'"],
            ["-","'zelenjava'","'-'","'ohrovt'","1.39","'1_kg'"],   
            ["-","'zelenjava'","'-'","'rdeca_paprika'","3.29","'1_kg'"],
            ["-","'zelenjava'","'-'","'por'","3.69","'1_kg'"],
            ["-","'zelenjava'","'-'","'cebula'","1.19","'1_kg'"],
            ["-","'zelenjava'","'-'","'cesen'","2.19","'0.25_kg'"],
            ["-","'zelenjava'","'-'","'rdeci_radic'","2.89","'1_kg'"],
            ["-","'zelenjava'","'-'","'paradiznik_beef'","1.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'paradiznik_v_grozdu_premium'","1.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'slovenski_paradiznik_v_grozdih'","1.99","'1_kg'"],
            ["-","'zelenjava'","'-'","'cesnjev_paradiznik'","2.49","'0.25_kg'"]
            ]
    a.writerows(data)

with open('izdelki_tus.csv','w',newline='') as fp2:
    a = csv.writer(fp2, delimiter=',')
    data = [["'id_izdelka'","'ime_izdelka'","'firma'","'okus'", "'redna_cena'", "'teza'"],
            ["-","'cokolada'","'milka'","'mlecna'","2.99","'250_g'"],
            ["-","'cokolada'","'milka'","'celi_lesniki'","2.97","'250_g'"],
            ["-","'mleko'","'alpsko_mleko'","'3,5%'","1.07","'1_l'"],
            ["-","'moka'","'mlin_katic'","'psenicna_posebna_bela_moka'","0.74","'1_kg'"],
            ["-","'moka'","'mlin_katic'","'psenicna_bela_moka'","0.65","'1_kg'"],
            ["-","'moka'","'mlin_katic'","'ajdova_moka'","2.99","'1_kg'"]
            ]
    a.writerows(data)
