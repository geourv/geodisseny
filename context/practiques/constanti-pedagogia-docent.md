---
title: "Constantí: controls de la seqüència pedagògica"
author: Benito Zaragozí
lang: ca
content_status: draft
---

# Controls descriptius

124 registres; 98 potències publicades, suma 2.770 kW; 26 intervals sense xifra. L'escenari central assigna 2,5/15/62,5 kW als 19/6/1 casos respectius. Total 2.970 kW, 200 assignats. Les dades publicades es preserven.

- Malla: 90 quadrats d'1 km²; suma 124 punts i 2.770 kW coneguts. Quadrats de 48 registres/268 kW i 17 registres/891 kW.
- Centre dels registres: (349051,5269; 4557573,8792) m.
- Centre ponderat central: (347321,2104; 4558177,0408) m; canvi 1.832,4298 m.
- Radi 2.000,6564 m; semieixos 1.934,4377/510,4672 m; azimut 110,22°.
- Kernel Quartic 500/1.500 m, píxel 100 m: integrals 124,00168 i 124,00002 registres. NoData es conserva; les cel·les sense contribució calculada no són una comprovació d'absència d'instal·lacions.

# Controls d'autocorrelació

98 registres, 94 posicions; identificadors ordenats sense reutilitzar el FID del GeoPackage original. Potències en kW, kNN8 dirigit, files normalitzades, diagonal zero. Component únic; vincle màxim 2.565,7135 m.

- Mitjana 28,265306 kW. I global 0,191856301, esperança −0,0103093.
- 9.999 permutacions, llavor 20261005; 3 valors igualen/superen I: pseudo-p positiu 0,0004.
- Barreja il·lustrativa: mateixes posicions i potències, I = −0,0163491.
- Punt 450: veïns 100/100/60/30/100/20/60/50; mitjana 65 kW; HH, p_ref 0,0244.
- Punt 3: veïns 4/4/3/10/3/3/3/3; mitjana 4,125 kW; LL, p_ref 0,0027.
- QGIS nominal: 8 HH/45 LL/1 HL/3 LH/41 NS. Referència amb llavor explícita: després de Benjamini–Hochberg a 0,05, 7 HH/38 LL/1 HL/2 LH; els dos registres de lectura es mantenen.

No exigir pseudo-p idèntic en reexecutar el complement, que no exposa llavor. El mapa és exploratori; «semblança» no equival a causa, idoneïtat o influència entre instal·lacions. L'ús de kW originals permet explicar les mitjanes abans d'un logaritme. La I de 0,632 amb log1p és sensibilitat a una altra escala d'atribut, no una alternativa triada només perquè sigui més alta.

# Transferència i decisions editorials

Renda de 151 seccions, 2023 amb població d'1/1/2024; Queen I = 0,571917, p = 0,0001. Tarragona 07013: 23.239 i 21.496,67, HH; Tarragona 08012: 7.379 i 10.228,25, LL; Constantí 01002: 7.744 i 13.453,50, no destacada. A les captures les unitats s'identifiquen per municipi/codi o per potència visible, no per ABC.

L'ordre del capítol 4 segueix recompte → centres → dispersió → densitat. El capítol 5 reprèn atributs puntuals → mitjanes veïnes → Moran → permutacions → locals → renda. La regressió edat–potència i els gràfics sense una conclusió territorial establerta queden al context de recerca, fora del recorregut inicial. Les seccions tenen zero o diverses subseccions; els ancoratges anteriors s'han conservat com a aliases.

Figures de municipis amb zoom adaptat i barres d'escala: la comparació quantitativa es fa amb 323/2.278/2.001 m, no amb mida aparent. Cercle i el·lipse visibles a QGIS sobre els 124 punts, centre, límit i ortofoto. Accés a recompte, centres i kernel sobre Constantí.
