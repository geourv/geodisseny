---
title: "Visibilitat: notes docents i solucions"
subtitle: "Torxa de la Canonja, TV-3148 i àrea industrial"
author: Benito Zaragozí
lang: ca
date: "Preparació: 2 d'octubre de 2026"
content_status: draft
---

# Progressió i preparació

Començar amb **T**, una torxa identificada, i les parelles R1–R3. Passar després a **37 observadors de carretera**, i acabar amb **57 mostres d'àrea més T** per detectar alguna part visible del polígon. El model d'obstacles és comú, però canvia què representa cada punt.

Deu projectes amb 37 capes locals; EPSG:25831/NONE. Controls de QGIS 3.44.11/GDAL 3.10.3. El guió base de carretera utilitza totes les 37 mostres amb MDT; el contrast MDT/MDS usa 28 posicions comparables. Els ZIP, ràsters i intermedis es distribueixen per Moodle, fora de Git.

## Geometries i cotes

| Control | Valor |
| --- | --- |
| Torxa | OSM 7682543312, versió 1, `man_made=flare` |
| T ràster | X 346892,5; Y 4552507,5 m |
| MDT / pic MDS | 20,941999 /151,311996 m |
| Altura estimada d'estructura | 130,369997 m |
| Cota T del model | 152,311996 m: pic +1 m |
| Altura relativa MDT / MDS | 131,369997 /1 m |
| TV-3148 | 3.652,272633 m; 37 intervals |
| Pas / desplaçament inicial | 98,710071 /49,355036 m |
| Polígon MCSC 2024 | id 1459998, categoria 347 |
| Àrea del recinte petroquímic d'estudi | 2.229.408,741960 m² |
| Mostreig A | 57 fragments de graella 250 m retallada |

La coberta MCSC original de 162,59 ha es conserva separadament. El recinte s'obté amb `native:buffer`, primer +150 m i després −150 m sobre l'intermedi, 32 segments per quadrant, unions arrodonides i dissolució. Resultat: 222,94 ha i cap forat. No és el límit legal de tot el Polígon Sud. La torxa singular no rep el pes d'un fragment d'àrea.

La distància és un paràmetre de generalització: 50 m dona 181,33 ha i 5 forats; 100 m, 199,97 ha i 2; 150 m, 222,94 ha i cap; 250 m, 224,49 ha i cap. El resultat de 150 m incorpora 38,50 ha fora de l'exterior original. La discretització dels arcs retira 3,77 m² de la font. L'elecció es contrasta amb l'ortofoto, conservant les alternatives; el buffer negatiu no restitueix els espais que s'han tancat.

Context: complex petroquímic de Tarragona, amb polígons Nord, Sud i port connectats. El sector docent pertany al Sud. Cronologia contrastada: Dow/IQA el 1967, BASF el 1969, construcció de refineria el 1973 i activitat el 1976. Fonts: Rosell, Museu del Port, Repsol i Farnós Marsal (2025); evitar assimilar aquest sector a tota la indústria petroquímica.

El domini comú té **3.490.455 cel·les**. Els originals presenten 296.442 cel·les sense elevació en almenys un model. Els buits dins del mar RTT es tracten a 0 m; els altres 21.167 no s'interpreten com terreny baix. Una passada de cobertura exclou els raigs que hi passen i elimina 211.025 destinacions addicionals del domini. NoData no és ocultació.

# Controls de resultats

| Resultat | MDT | MDS |
| --- | ---: | ---: |
| T: cel·les visibles | 2.962.199 | 447.860 |
| T: percentatge del domini | 84,87% | 12,83% |
| 57 A o T: cel·les | 2.977.704 | 470.444 |
| 57 A o T: percentatge | 85,31% | 13,48% |
| Almenys una A, sense T | 2.281.626 | 115.149 |

El conjunt final ha d'incloure tota la conca de T. Sense afegir-la, el mostreig d'àrea pot perdre l'element alt i estret. La visibilitat acumulada no és una demostració que s'hagin mostrejat totes les estructures.

## Carretera i denominadors

- Suma MDT de 37 conques: **1.461.016 cel·les** amb alguna visió; màxim observat **33**.
- Valor 12: **1.184,52 m**, **32,43%** del recorregut representat.
- T amb MDT: 34 de 37 mostres visibles, **3.356,14 m**, **91,89%**.
- Contrast comú: 28 de 37 mostres, **2.763,88 m**, **75,68%** de cobertura.
- No calculades en MDS: C01, C06, C07, C09, C16, C19, C29, C33, C34. Els ulls a MDT + 1,7 m quedarien sota l'MDS opac.
- T amb MDS: 7 visibles i 21 ocultes entre les 28 calculables; **690,97 m**, **25% del subconjunt**.
- Les 9 desconegudes representen 888,39 m. Límits sobre les 37 mostres: 7/37=**18,92%**, 16/37=**43,24%**. No substituir les desconegudes per zeros.

No comparar directament una suma MDT de 37 posicions amb una suma MDS de 28. Els fitxers de contrast amb 28 mostres estan diferenciats dels acabats en `mdt-totes-nombre.tif` i `mdt-totes-percent.tif`.

## Parelles i perfils

| Receptor | Mostra | T MDT | T MDS |
| --- | --- | ---: | ---: |
| R1 | C05 | 1 | 1 |
| R2 | C11 | 0 | 0 |
| R3 | C13 | 1 | 0 |
| R4 | C37 | 1 | 0 |
| R5 | Fora del retall | Nul | Nul |

Els perfils independents a 0,5 m confirmen els quatre signes: R1 té marge mínim MDS d'uns +0,85 m; R2, marge MDT d'uns −1,33 m; R3, marge MDS d'uns −2,00 m; R4, d'uns −8,87 m. Prop del llindar, la resolució i el traçat discret poden alterar la classificació.

A R1, **T=1, G=1, A=0%** amb MDS: es veu la torxa però cap dels 57 punts de la graella interior. La resposta binària «alguna part» i la fracció d'àrea representada són indicadors diferents.

# Comprovacions i errors que cal discutir

La verificació nativa reprodueix els dos buffers i l'intermedi, la ruta, les 37 mostres lineals, els 57 fragments i els punts interiors. GDAL/QGIS reprodueix la cota mínima, la Calculadora ràster reprodueix totes les cel·les vàlides i NoData, i `native:cellstatistics` reprodueix la suma de les 37 conques. Els deu projectes es comproven des d'una ubicació nova, només lectura i sense xarxa.

Viewshed té un origen per execució. El lot GUI repeteix files de paràmetres i encara no aplica màscara ni pondera. L'expressió d'emplenament del guió retorna les 37 coordenades ordenades per id. La cadena `reproduccio/lots_visibilitat.py` automatitza també les operacions posteriors: 37 execucions C/MDT, 28 C/MDS i 57 A per model. Les 179 execucions natives s'han contrastat amb la preparació independent: igualtat de totes les cel·les, graella i NoData dels recomptes, percentatges i unions amb T. No són 179 introduccions manuals a la interfície.

Les captures inicials comparen ortofoto i MDS amb el mateix enquadrament. L'ortofoto prové de retalls WMS GetMap de 2025, desats en GeoTIFF: 10 m/píxel al context, 2,5 m al sector i 0,5 m a T. La resolució de la imatge demanada al servei és diferent de la resolució de l'ortofoto d'origen de 25 cm.

Una prova amb pantalla valida el mode DEM: observador a 102 m, obstacle a 115 m situat a 50 m i destinació a 100 m exigeixen cota 128 m. El mode GROUND no dona aquesta mateixa magnitud. Les captures de diàlegs mostren paràmetres preparats; l'evidència de càlcul és a `controls/verificacio-qgis.json`.

Errors per discutir: confondre cota i altura; moure els receptors damunt de l'MDS; equiparar MDS màxim amb obstacles exactes; convertir NoData en0; duplicar les dues calçades; sumar superfícies totals en comptes de cel·les; assignar el pes d'un quadrat complet als fragments; perdre la torxa en una graella; interpretar superfície visible com població o impacte.

Fonts i llicències a `fonts/fonts.json` i al guió. Les altures de model i la informació LiDAR no certifiquen una flama concreta ni substitueixen una comprovació de camp.
