---
title: "Resolució docent: visibilitat de torxa, carretera i recinte petroquímic"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
---

# Preparar la tasca de Moodle

## Durada orientativa per bloc

| Bloc | Aula | Treball autònom i informe |
| --- | --- | --- |
| Torxa i parelles de visió | 60–90 min | 45–60 min |
| Carretera i procés per lots | 90–120 min | 60–90 min |
| Recinte, mostreig i ponderació | 120–150 min | 90–120 min |

Table: Estimacions orientatives segons la selecció dels tres blocs.

Preparació docent orientativa: 45–60 min amb QGIS/GDAL preparats, dades locals i resultats de referència disponibles. Les estimacions no provenen d'una prova d'aula; no inclouen instal·lacions ni descàrregues. Selecciona els apartats del 70% segons el temps disponible. Els lots repeteixen càlculs, però configurar-los, controlar cobertura i interpretar denominadors també demana temps. Les sis pàgines de la resolució anterior eren un resum de controls, no una mesura de durada.

1. Activa l'edició del curs i tria **Afegir una activitat o un recurs → Tasca**. Posa-hi el nom **Visibilitat: torxa, carretera i recinte petroquímic**.
2. A **Descripció**, enganxa el bloc següent, des de «Dades de partida» fins al final de «Qualificació».
3. A **Fitxers addicionals**, adjunta **`visibilitat-costa-2026-10-18-ca.zip`**, el paquet d'inici. Inclou les dades locals i el `LLEGIU-ME.pdf` de l'alumnat.
4. Revisa la tasca amb la vista d'estudiant i comprova la descàrrega. La resolució i els resultats del paquet docent permeten reprendre les diferents fases durant la classe.

## Enunciat per copiar a la descripció

**Dades de partida.** Descarregueu `visibilitat-costa-2026-10-18-ca.zip`, adjunt a aquesta tasca, i descomprimiu-lo en una carpeta pròpia, conservant-ne l'estructura. Llegiu `LLEGIU-ME.pdf` i obriu el projecte **inici** de `payload/data/visibilitat-costa.gpkg` amb QGIS 3.44 i GDAL. El paquet inclou MDT, MDS, domini comparable, ortofoto, torxa T, carretera i mostres, receptors i coberta industrial. Conserveu els recursos de `payload/data/fonts/`.

**Treball de classe.** El professor indicarà a classe quins apartats, exercicis i comprovacions són obligatoris dins del **70% de la qualificació** i ho recollirà en aquesta tasca. La guia desenvolupa la progressió completa: no tots els passos són automàticament obligatoris. Els blocs que es poden seleccionar estudien si es veu una torxa de la Canonja, quines posicions es veuen al llarg de la TV-3148 i des d'on es veu alguna part del recinte petroquímic:

1. **Punt.** Calculeu la conca de T sobre MDT i contrasteu-la amb MDS mantenint la mateixa cota dels receptors. Consulteu R1–R5 i distingiu visibilitat, ocultació i lloc no calculat.
2. **Carretera.** Reviseu el mostreig de 37 posicions. Feu les execucions individuals indicades a la guia i prepareu el lot i la suma de conques. Distingiu territori visible des de la carretera i carretera des d'on es veu T; declareu la cobertura de les posicions comparables entre MDT/MDS.
3. **Àrea.** Generalitzeu la coberta amb el buffer positiu i després el negatiu. Creeu la graella de 250 m, retalleu-la, mostregeu els fragments i conserveu-ne els pesos d'àrea. Prepareu els lots i compareu nombre de mostres visibles, percentatge ponderat i resposta d'alguna part del recinte o T.
4. **Interpretació.** Expliqueu com canvia la pregunta quan es passa de punt a línia i àrea. Identifiqueu superfície, altures, domini, denominadors i unitats de cada resultat.

**Ampliacions per aspirar a l'excel·lent.** Podeu comparar altures o receptors, repetir el mostreig amb altres intervals o graelles, provar altres distàncies de tancament del recinte, o estudiar un mirador, itinerari o objectiu en una zona alternativa. Manteniu una referència i canvieu un paràmetre cada vegada. Declareu cotes, pesos i domini perquè la comparació sigui interpretable. Justifiqueu què heu après; fer més conques no substitueix una pregunta ni els obligatoris.

**Preguntes obertes i aplicacions.** Quins resultats persisteixen quan canvia el mostreig? Pot una graella ometre una estructura alta? Quins punts seleccionaríeu per contrastar la visió al camp? Desenvolupeu una aplicació geogràfica, com comparar un itinerari o preparar observacions de paisatge, i expliqueu què falta per relacionar visió, freqüentació, percepció o impacte. En una zona alternativa acordada amb el professor, recalculeu altures, domini i controls propis.

**Informe.** Presenteu pregunta i àmbit, dades i decisions, procediment amb controls, mapes i taules dels apartats seleccionats, i interpretació amb límits. Podeu enregistrar fragments de la pantalla i després pausar el vídeo per desar captures de configuració i resultats importants. Comproveu la llegibilitat, numereu-les i expliqueu què demostra cadascuna; exporteu els mapes finals amb llegenda, escala i unitats. El vídeo és una ajuda, no un lliurament obligatori tret que el professor ho indiqui. La guia detalla com preparar l'informe.

**Lliurament.** Entregueu `visibilitat-costa-cognom.gpkg`, amb els vectors generats; `visibilitat-costa-cognom.qgz`, amb rutes relatives; els TIFF de càlcul; i `visibilitat-costa-cognom.pdf`, amb l'informe. Manteniu els fitxers referenciats pel projecte dins de la carpeta de treball. En una zona alternativa, identifiqueu el cas al nom dels fitxers i conserveu fonts i controls propis.

**Comprovacions.** Reviseu EPSG:25831/NONE, graella de 5 m, extensió, bandes, cotes, altures i NoData. Comproveu l'ordre dels buffers, els pesos i la cobertura dels observadors. NoData no és ocultació; una visió geomètrica no mesura persones exposades ni impacte paisatgístic. Comproveu que el projecte s'obre després de moure la carpeta completa.

**Qualificació.** El **70%** correspon als apartats obligatoris que indicarà el professor. Les ampliacions permeten aspirar a l'excel·lent segons els criteris comunicats a classe i recollits en aquesta tasca. Es valoren pregunta, controls i interpretació, no només el nombre de conques. No substitueixen els obligatoris ni garanteixen una nota per haver-les intentat.

# Preparació i progressió

El recorregut és **T i parelles receptor–torxa → carretera → àrea més T**. Comparar nombres només quan comparteixen objectius, observadors, altures i cobertura.

Selecciona els apartats que entraran al 70% obligatori, comunica'ls a classe i deixa la mateixa selecció a Moodle. Distingeix demostració docent, execució individual i repetició per lots, segons el temps disponible. Per orientar una ampliació, demana pregunta, comparació de referència, registre de paràmetres i interpretació; una altra zona necessita controls propis.

Conserva el GeoPackage d'inici i obre el projecte **docent** des de `payload/data/visibilitat-costa-docent.gpkg`. Els resultats de referència corresponen al paquet costa r3 del 2/10/2026, amb QGIS 3.44.11/GDAL 3.10.3. EPSG:25831/NONE; ràsters de càlcul a 5 m i recursos locals.

# Geometries, cotes i cobertura

| Control | Valor |
| --- | --- |
| T ràster | (346892,5; 4552507,5) m |
| MDT / pic MDS | 20,941999 /151,311996 m |
| Cota T del model | 152,311996 m, pic +1 m |
| Altura relativa MDT /MDS | 131,369997 /1 m |
| TV-3148 | 3.652,272633 m; 37 intervals |
| Pas /inici | 98,710071 /49,355036 m |
| Coberta MCSC original | id1459998, categoria347, 162,59 ha, 19 forats |
| Recinte de +150/−150 m | 2.229.408,741960 m², cap forat |
| Mostreig d'àrea | 57 fragments de graella de250 m |
| Domini comparable | 3.490.455 cel·les |

Table: Controls comuns de la pràctica.

L'MDS màxim pot eixamplar obstacles estrets. El metre sobre la superfície és un desplaçament de model, no una mesura de flama. Els buits del mar s'han tractat a 0 m; els altres buits i les trajectòries afectades per elevacions desconegudes queden fora del domini. NoData no és ocultació.

El tancament es calcula amb `native:buffer`: positiu +150 m, després negatiu sobre l'intermedi, 32 segments i dissolució. Afegeix 38,50 ha fora de l'exterior original i retira uns 3,77 m² de vora per discretització. No és un límit oficial nou del Polígon Sud.

# Torxa i superfície

| Resultat | MDT | MDS |
| --- | ---: | ---: |
| T: cel·les visibles | 2.962.199 | 447.860 |
| T: percentatge del domini | 84,87% | 12,83% |
| 57A o T: cel·les visibles | 2.977.704 | 470.444 |
| 57A o T: percentatge | 85,31% | 13,48% |
| Almenys una A, sense T | 2.281.626 | 115.149 |

Table: Respostes amb el mateix domini; el recompte de mostres i el percentatge d'àrea responen altres preguntes.

Sobre MDS, el mode DEM retorna cota absoluta mínima i ignora l'altura de destinació. Comparar-la amb **MDT +1,7 m**, no amb ulls damunt de la teulada, preserva els receptors entre models. El mapa d'alguna part ha d'incloure tota la conca de T.

| Receptor | Mostra | T MDT | T MDS |
| --- | --- | ---: | ---: |
| R1 | C05 | 1 | 1 |
| R2 | C11 | 0 | 0 |
| R3 | C13 | 1 | 0 |
| R4 | C37 | 1 | 0 |
| R5 | Fora del retall | Nul | Nul |

Table: Parelles que diferencien relleu, obstacles superficials i lloc no calculat.

Els perfils independents a 0,5 m confirmen els signes: marge MDS de R1 aproximadament +0,85 m; MDT de R2 −1,33 m; MDS de R3 −2,00 m i de R4 −8,87 m. Prop del llindar importen resolució i traçat discret.

# Carretera: recompte i denominador

- La suma MDT de **37 conques** té 1.461.016 cel·les amb alguna visió i màxim 33.
- Un valor12 representa 1.184,52 m i 32,43% del recorregut mostrejat.
- T amb MDT: 34/37 visibles, 3.356,14 m, 91,89%.
- Contrast MDS: 28/37 compatibles, 2.763,88 m i 75,68% de cobertura.
- Les no calculades són C01, C06, C07, C09, C16, C19, C29, C33 i C34.
- T amb MDS: 7 visibles i 21 ocultes entre les28, 690,97 m i25% del subconjunt.

Les9 desconegudes representen888,39 m. Sobre totes les37, els límits de visió són18,92% i43,24%; no substituir-les perzeros. La suma MDT de37 i el contrast MDT/MDS de28 estan diferenciats al projecte i als noms de capa.

Viewshed té un origen per execució. El lot GUI repeteix37files; encara no emmascara ni suma. Les tres execucions individuals de la guia serveixen per comprendre el procediment. No exigir179 introduccions manuals de coordenades per reproduir els quatre lots històrics.

# Recinte, pesos i torxa singular

| Tancament +n/−n | Àrea | Forats | Afegit exterior |
| --- | ---: | ---: | ---: |
| 50 m | 181,33 ha | 5 | 4,85 ha |
| 100 m | 199,97 ha | 2 | 15,52 ha |
| 150 m | 222,94 ha | 0 | 38,50 ha |
| 250 m | 224,49 ha | 0 | 40,04 ha |

Table: Alternatives per discutir l'escala de generalització.

Els57 fragments representen el recinte generalitzat, inclosos entrants incorporats. Els pesos són les seues àrees. A és1m sobre l'MDS local; en MDT es manté la mateixa cota absoluta mitjançant `h_mdt_m`.

Amb MDS, R1 dona **T=1, alguna part=1 i A=0%**: es veu la torxa però cap mostra interior. Afegir-la al binari evita perdre una estructura singular; no li assigna un pes d'àrea arbitrari. Demanar que l'explicació diferencie resposta binària, nombre de mostres i fracció ponderada.

# Revisió del treball i fonts

Comprovar CRS/NONE, banda, codis de NoData, extensió, altures, ordre dels buffers, geometria vàlida, pesos, cobertura d'observadors i rutes relatives. Les captures acrediten configuració i representació; els controls del paquet històric acrediten càlcul, no una seqüència manual clic a clic.

Revisar els apartats obligatoris anunciats i la comparabilitat de les ampliacions: cotes, domini, pesos i denominadors han de permetre entendre què ha canviat. Demanar una aplicació geogràfica proporcionada i una proposta de contrast al camp. Les captures extretes d'un vídeo són evidències seleccionades; la gravació completa no substitueix l'informe ni els controls numèrics.

Fonts: ICGC elevacions LiDAR2021–2023, MCSC/RTT2024 i ortofoto WMS2025; OSM node7682543312v1. [Condicions ICGC](https://www.icgc.cat/condicions), [OSM](https://www.openstreetmap.org/copyright), [GDAL Viewshed](https://gdal.org/en/stable/programs/gdal_viewshed.html) i [QGIS3.44](https://docs.qgis.org/3.44/en/docs/user_manual/). Context històric: [Farnós Marsal2025](https://publicacions.iec.cat/repository/pdf/00000528/00000061.pdf), Polígons Nord/Sud, port i conduccions.

Cap resposta de la pràctica certifica una flama concreta, persones exposades, accés públic als receptors ni impacte paisatgístic. La conclusió ha de formular què falta observar per estudiar aquelles qüestions.
