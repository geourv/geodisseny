---
title: "Notes docents i controls: distàncies a Vila-seca"
author: Benito Zaragozí
lang: ca
content_status: draft
---

# Preparació de la sessió

La guia de l'alumnat és `GUIA.md` / `GUIA.pdf`. El nucli de distància euclidiana es pot fer amb els blocs A–B; C–D desenvolupen xarxa i cost, i E–F marxa anisòtropa i isòcrones. La Pineda i la fricció isòtropa derivada de pendent són ampliacions. Aquesta seqüència no fixa criteris d'avaluació ni una durada oficial de l'assignatura.

Abans de la classe, obrir una còpia descomprimida del paquet i comprovar aquestes eines:

- Línia entre geometries: `native:shortestline`.
- Rasterització: `gdal:rasterize`.
- Distància ràster: `gdal:proximity`.
- Ruta per la xarxa: `native:shortestpathpointtopoint`.
- Àrea de servei: `native:serviceareafrompoint`.
- Cost acumulat: `grass:r.cost`.
- Reconstrucció del camí: `grass:r.path`.
- Marxa amb punts d'inici: `grass:r.walk.points`.
- Contorns temporals: `grass:r.contour`.
- Recompte de classes ràster: `native:rasterlayeruniquevaluesreport`.

El runtime de control és QGIS 3.44.11, GDAL 3.10.3 i GRASS 8.4.1.

Els projectes de la carpeta `projectes` permeten reprendre una etapa i mostrar el resultat. `00-inici.qgz` obre el lloc i els inputs; els resultats de referència hi són ocults al grup d'altres dades. Cal demanar que cada estudiant desi les pròpies sortides a `treball`.

# Resultats de control

Tots els càlculs plans utilitzen EPSG:25831 i el·lipsoide NONE. O=(344407;4553668,36) i D=(344473,01;4554030,72), en metres.

| Càlcul | Valor de control | Interpretació |
| --- | ---: | --- |
| Euclidiana vectorial | 368,323349 m | Entre les coordenades originals |
| Euclidiana ràster | 370,742493 m | Entre centres de les cel·les de 5 m |
| Xarxa, P2 obert | 454,104650 m | Sobre la xarxa preparada |
| Xarxa, P2 obert a 5 km/h | 0,090820930 h = 5,449256 min | Velocitat docent uniforme |
| Xarxa, P2 tancat | Sense ruta | No equival a zero ni a infinit desat com a dada ordinària |
| Camí ràster, P2 obert | 470,624458 m | Longitud de la línia reconstruïda |
| Cost ràster, P2 obert | 470,624458 m ponderats | Cost mínim a D |
| Camí ràster, P2 tancat | 1135,807358 m | Longitud del camí alternatiu |
| Cost ràster, P2 tancat | 2217,680733 m ponderats | Inclou passos per cel·les de fricció 4 |

Per comprovar longituds és suficient l'arrodoniment al decímetre; les dades i els valors complets són a `controls/resultats.json`. En una graella hi pot haver camins equivalents per empats: s'ha de comparar també el cost, no només la forma exacta de la línia.

## Unitats de les àrees de servei

En aquesta versió, `TRAVEL_COST2` és en **hores**. S'ha comprovat independentment en una línia de 1.000 m a 6 km/h: 5/60 hores han de retornar 500 m accessibles. La guia utilitza 3, 6 i 12 minuts, equivalents a 0,05, 0,10 i 0,20 hores, per evitar conversions poc llegibles al diàleg.

| Límit, pas obert | Longitud única de trams accessibles |
| --- | ---: |
| 3 min | 448,384607 m |
| 6 min | 1116,560723 m |
| 12 min | 3606,611447 m |
| 6 min, pas tancat | 68,418647 m |

La longitud total de branques accessibles no és la distància màxima d'un trajecte. A més, l'algorisme pot retornar segments coincidents en tots dos sentits: els controls anteriors fan la unió geomètrica abans de sumar. D queda fora dels 3 minuts i dins dels 6 amb el pas obert.

## Xarxa i topologia

La xarxa final té **189 parts d'eix**. Es retenen camins, corriols, vies no catalogades i altres vies seleccionades; es retiren els eixos d'autopista. Els sentits són bidireccionals i la velocitat és uniforme, sense afirmar que aquestes regles siguin les condicions reals de circulació.

La preparació divideix eixos en contactes d'un extrem amb l'interior d'un altre eix genèric, amb tolerància màxima de 5 mm. No aplica una divisió general a tots els creuaments; els contactes i identificadors queden registrats. Les coordenades de treball s'arrodoneixen al mil·límetre. L'extracte original conservat a `fonts/rtt-vilaseca.gpkg` no incorpora aquestes transformacions.

Tancar P2 elimina el tram `rtt_id=1354754`. En la xarxa seleccionada, O queda en un tram sense una segona sortida connectada. Es va comprovar que augmentar la tolerància no resolia el problema i no es van inventar connexions per forçar una volta. La diferència amb el ràster és instructiva: el ràster admet travessar terreny amb fricció 4 i pot arribar a un altre pas.

## Ràsters i controls independents

- Graella comuna: 340 × 340, 5 m, extensió X 343600–345300, Y 4553000–4554700.
- O rasteritzat ocupa una única cel·la de valor 1; el fons és zero vàlid.
- Fricció: camins 1, resta admesa 4; autopista i edificis NoData, amb corredors de pas explícits. Els edificis són un retall cadastral de Vila-seca.
- La banda d'autopista es deriva d'un buffer de 25 m dels eixos. Els passos tenen amplada modelada de 20 m i prolongació de 40 m dels eixos de travessa per connectar tota la banda. Aquests paràmetres no són mesures de l'obra real.
- r.cost rep 5 o 20 unitats de travessa de cel·la, amb diagonals i sense Knight's move. El NoData no rep cap cost finit.
- Els costos a D s'han contrastat amb un Dijkstra independent sobre la mateixa graella: coincideixen amb tolerància de 0,02 m ponderats.
- Cel·les accessibles: 103.062 amb P2 tancat, 103.115 amb P2 obert. La resta de cel·les són les barreres; no s'han confós NaN amb valors vàlids.
- r.path utilitza el ràster de direccions en graus i **D** com a punt de reconstrucció. El recorregut retorna cap a O.

# Errors habituals per comentar a classe

| Símptoma | Comprovació |
| --- | --- |
| Resultats en graus o de magnitud estranya | CRS de cada capa, CRS de projecte i unitats del mòdul |
| Proximitat aproximadament cinc vegades menor | S'han deixat distàncies en píxels en lloc de metres |
| Tot el ràster dona distància zero | S'ha gravat 1 a tot arreu o s'han escollit tots els valors com a objectiu |
| Diferència petita entre vector i ràster | Centres de cel·la i resolució; no és necessàriament un error |
| Xarxa tancada sense resultat | És el control previst: llegir la connectivitat i no assignar 0 m |
| La franja temporal és desmesurada | Minuts introduïts com hores, o camp de velocitat no seleccionat |
| Ruta que travessa una barrera | NoData canviat per zero, null_cost definit, o corredor massa ample |
| r.path falla o retorna un camí incoherent | S'ha triat cost acumulat en lloc de direccions, o O en lloc de D |
| Cost diferent malgrat mateixa fricció | Mida i alineació de cel·la, multiplicació per 5, veïns o regió GRASS |
| Ràster que sembla un MDT | Llegir nom, unitats i valors: altitud, pendent, fricció i cost són magnituds diferents |

# Cas de la Pineda

La parcel·la és `7713904CF4571D`, aproximadament 8,71 ha. Es conserva el model anterior, amb fricció 1 a l'exterior i 20 a l'interior, vuit veïns i cel·les de 5 m. L'MDT no intervé en aquest experiment. Les dues captures noves mostren expressament els ràsters de fricció i cost acumulat.

La ruta uniforme fa 608,284271 m i passa per la parcel·la; la penalitzada fa 724,264069 m i la voreja. El model no incorpora tanques ni usos del sòl. És adequat per explicar el contrast entre resistència finita i barrera, no per presentar una ruta autoritzada.

# Marxa anisòtropa i isòcrones

L'MDT entra com a elevació en metres; r.walk calcula desnivells amb signe. La fricció temporal és **0 s/m als camins i 0,5 s/m a la resta admesa**, lambda 1, barreres NoData. No es multiplica per la cel·la ni es reutilitzen els pesos 1/4 com si fossin segons.

Coeficients per defecte: 0,72 / 6 / 1,9998 / −1,9998; llindar de baixada −0,2125 m/m. Vuit veïns, sense moviment de cavall. Prova independent amb GRASS sobre una rampa aïllada de 100 m i 10 m de desnivell: **132 s amunt, 52,002 s avall**, amb fricció addicional zero.

| Escenari | Segons | Minuts | Longitud, m |
| --- | ---: | ---: | ---: |
| MDT, P2 obert, O→D | 397,830737 | 6,630512 | 466,482323 |
| MDT, P2 obert, D→O | 389,007040 | 6,483451 | 466,482323 |
| MDT, P2 tancat, O→D | 1049,163737 | 17,486062 | 1071,457070 |
| Pla, P2 obert, O→D | 338,367272 | 5,639455 | 466,482323 |
| Pla, P2 obert, D→O | 338,367272 | 5,639455 | 466,482323 |

Els cinc costos s'han contrastat amb Dijkstra independent sobre arcs dirigits de la graella, tolerància 0,05 s. Anada/tornada tenen longituds iguals però les geometries no són exactament iguals; hi ha petites alternatives locals. El control pla manté fricció i barreres i només elimina el relleu.

O/D són a cota 50,887 / 52,249 m a l'MDT. El desnivell total entre extrems no substitueix les pujades i baixades intermèdies. El perfil d'un pas a diferent nivell pot estar simplificat al MDT de 5 m; el model no s'ha calibrat amb temps observats.

## Controls acumulats d'isòcrones

| Límit | Cel·les, obert | Hectàrees, obert | Cel·les, tancat | Hectàrees, tancat |
| --- | ---: | ---: | ---: | ---: |
| 3 min | 1624 | 4,0600 | 1434 | 3,5850 |
| 6 min | 7481 | 18,7025 | 4764 | 11,9100 |
| 12 min | 36777 | 91,9425 | 22155 | 55,3875 |

Els llindars són inclusius. Es compten cel·les del ràster, 25 m² cadascuna. Cap d'aquestes franges toca el límit del retall. R.contour rep minuts i nivells 3,6,12; `cut=3` elimina contorns degenerats de menys de tres punts, sense modificar els recomptes del ràster. NoData i més de 12 minuts es representen amb grisos diferents.

Les franges de xarxa són porcions de línia disjuntes; la superfície ràster admet moviment fora dels eixos. D cau dins dels 6 min de xarxa, però fora dels 6 min de marxa amb relleu. No comparar hectàrees d'un buffer de carreteres amb aquestes superfícies com si fossin el mateix indicador.

## Restriccions de gir

Comprovats els paràmetres públics de les eines natives de QGIS 3.44: no hi ha taula de maniobres. El sentit és una propietat de l'arc; un gir necessita com a mínim tram d'entrada i tram de sortida. Penalització i prohibició també són diferents. L'esquema a→b / c→b és fictici i explica aquesta dependència, sense simular que s'hagin aplicat restriccions amb el motor natiu.

# Procedència i reproducció

Els inputs territorials són de l'ICGC i la Dirección General del Catastro. `fonts/fonts.json` conserva URLs, edicions o dates disponibles, transformacions i hashes. `MANIFEST.json` identifica cada fitxer del lliurament. No cal connexió als serveis web per treballar amb les còpies del paquet.

Les captures s'han fet amb **unaltracaptura** i el mateix runtime QGIS dels controls. PNG, SVG anotats i manifests es conserven. Els projectes per a l'alumnat utilitzen dades locals i rutes relatives.

L'ampliació té 15 projectes, 77 capes, 21 captures i quatre figures SVG noves. Els projectes 10–14 reprenen marxa, relleu i isòcrones. `controls/ampliacio.json` i `algorismes-ampliacio.json` conserven controls i paràmetres.

La font `reproduccio/preparar_distancies.py` documenta la preparació al repositori geodisseny. Espera les rutes originals del repositori i s'executa en les fases `--fetch`, `--build` i `--style`, aquestes dues últimes en processos QGIS separats. No és un instal·lador autònom de QGIS. Els procediments de la guia es poden reproduir directament amb les dades distribuïdes.

`reproduccio/preparar_accessibilitat.py` parteix del ZIP anterior verificat i escriu en una destinació nova. Requereix `--init`, `--build`, `--style` i `--figure-inputs`; càlcul i estil en processos QGIS separats. Els inputs vectorials de GRASS identifiquen explícitament la capa espacial del GeoPackage per no importar també taules d'estils. Ràsters i contorns tenen noms base diferents per evitar que comparteixin accidentalment un fitxer QML.
