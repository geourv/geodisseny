---
title: "Resolució docent: accessibilitat de Vila-seca"
author: Benito Zaragozí
lang: ca
date: "Guia revisada: 7 d'octubre de 2026"
content_status: draft
---

# Pregunta i preparació de la pràctica

La pregunta és com canvia l'accés entre **O i D** quan s'admet moviment en línia recta, sobre vials o entre cel·les, i quan es tanca el pas **P2** de l'AP-7. La resolució utilitza les mateixes coordenades durant tota la cadena. No s'ha de substituir el punt quan un resultat sembli poc favorable: cal revisar el model i les entrades.

L'alumnat rep `accessibilitat-vilaseca.gpkg` i `LLEGIU-ME.pdf`. El projecte **inici** està incrustat al GeoPackage. Aquesta lectura del professorat desenvolupa la resolució i utilitza les sortides i projectes per etapa per reprendre un resultat durant la classe.

## Obrir i comprovar les dades

1. Obre QGIS 3.44, amb GDAL i GRASS disponibles a **Procés → Caixa d'eines**.
2. A **Explorador → GeoPackage → Connexió nova**, selecciona la còpia de treball i desplega-la. Obre el projecte **inici**.
3. Comprova **EPSG:25831** i el·lipsoide **Cap / NONE**. Activa O, D, xarxa i ortofoto i localitza P2 i els passos alternatius.
4. Obre les taules d'origen/destí i consulta les coordenades. A `passos`, comprova `pas_id`: P2=2, alternatius=1.
5. A cada eina GRASS, selecciona la **capa espacial concreta**. La ruta del GeoPackage sola també identifica altres capes, estils i el projecte; no equival a seleccionar `origen`.

![La connexió desplegada permet seleccionar el projecte, els punts, els passos, les cobertes i el MDT de manera inequívoca.](captures/inici.png){width=100% height=380pt}

| Entrada | Font i accés | Què s'utilitza |
| --- | --- | --- |
| Xarxa a peu | [OSM/Geofabrik, Catalunya](https://download.geofabrik.de/europe/spain/cataluna.html) | Vials i connexions nodals; velocitat docent5km/h |
| Cobertes | [MCSC de l'ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya), [àrea seleccionada](https://visors.icgc.cat/appdownloads/index.html?c=fmexomcsc) i [GeoPackage2024](https://datacloud.icgc.cat/datacloud/cobertes-sol/gpkg/cobertes-sol-v1r0-2024.zip) | Classe vectorial i llegenda per assignar pesos |
| Autopista i passos | [ICGC, RTT](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial) | Eixos AP-7 i corredors de travessa del model |
| Altitud | [ICGC, elevacions](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions) | MDT de5m, en metres d'altitud |
| Context | [ICGC, ortofoto](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Imatge/Ortofoto-Territorial) | Localització, continuïtat de la barrera i connexió dels passos |
| Límit | [ICGC, divisions administratives](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives) | Cobertura municipal i entorn de les connexions |

Table: Entrades de la pràctica, fonts i ús en el model.

## Graella i noms de sortida

| Propietat | Valor |
| --- | --- |
| CRS / unitats | EPSG:25831 / metres |
| Extensió X | 343000–346000 |
| Extensió Y | 4552000–4555200 |
| Cel·la | 5×5m |
| Dimensions | 600 columnes ×640 files |

Table: CRS, extensió, resolució i dimensions de la graella comuna.

Les sortides ràster són TIFF locals; les vectorials es desen amb noms de capa nous al GeoPackage de treball. Cada escenari té un sufix **obert/tancat**, i cada sentit de marxa **anada/tornada**. Conservar el cost, les direccions i el camí evita confondre una representació amb el resultat d'un càlcul diferent.

# A. Resolució de la distància vectorial

1. Obre **Línia més curta entre objectes**, `native:shortestline`.
2. Font **Origen O**, destinació **Destí D**, mètode **Distance to Nearest Point on feature**, **1** veí i distància màxima buida.
3. Desa **euclidiana_vector** i consulta'n la longitud.

![El diàleg relaciona un punt origen amb un punt destí; un únic veí és suficient per a aquest cas.](captures/distancies-vector-parametres.png){width=85% height=380pt}

| Punt | X, m | Y, m |
| --- | ---: | ---: |
| O | 344407,565081 | 4553669,673733 |
| D | 344475,279609 | 4554024,590093 |

Table: Coordenades d'O i D per al càlcul de la distància vectorial.

Les diferències són **67,714528m** en X i **354,916360m** en Y. Pitàgores dona **361,318253m**. Tancar P2 no modifica aquesta separació geomètrica. La interpretació esperada és que una recta entre punts encara no és un itinerari possible.

# B. Resolució de la distància ràster

## Crear la cel·la origen i conservar el fons correcte

1. A `gdal:rasterize`, selecciona **Origen O**, valor fix1, sense camp d'atributs.
2. Unitats georeferenciades, resolució5/5m, extensió d'**ambit_calcul**, Float32, inicial0 i NoData−9999. Desa **origen_zero.tif**.
3. Comprova una única cel·la amb1. Amb `gdal:translate`, crea **origen_null.tif** assignant0 com a NoData, sense canviar la graella.
4. Aquesta còpia té únicament O com a cel·la no nul·la; és l'entrada de GRASS. Conserva origen_zero per al contrast GDAL amb llista de valors objectiu1.

## r.grow.distance i control dels centres

1. Obre [r.grow.distance](https://grass.osgeo.org/grass84/manuals/r.grow.distance.html), amb **origen_null**, mètrica **euclidean** i cerca de NULL desactivada.
2. Fixa la regió comuna i5m; desa **distancia_grass.tif**.
3. Amb `native:rastersampling`, mostreja **Destí D**. El resultat és **361,835598m**.
4. Repeteix amb `gdal:proximity`, entrada origen_zero, objectiu1, unitats georeferenciades, Float32 i NoData−9999. Ha de concordar amb GRASS al mil·límetre.

![La mètrica euclidiana s'aplica a la cel·la origen; el fonsNULL evita que el fons es tracti com un conjunt d'orígens.](captures/distancia-grass.png){width=85% height=380pt}

| Centre de cel·la | X, m | Y, m |
| --- | ---: | ---: |
| O | 344407,5 | 4553667,5 |
| D | 344477,5 | 4554022,5 |

Table: Coordenades dels centres de cel·la d'O i D en la graella comuna.

La separació de centres és70m en X i355m en Y. El control és `sqrt(70²+355²)`. La diferència de **0,517345m** respecte del vector és una conseqüència de representar els punts amb cel·les, no una ruta que eviti l'autopista.

# C. Xarxa, tancament i àrees de servei

## Itinerari obert

1. A `native:shortestpathpointtopoint`, selecciona **xarxa**, criteri **més curt**, direcció per defecte ambdós sentits i tolerància topològica0m.
2. Utilitza O/D de les capes amb tolerància punt–xarxa0,1m. Les coordenades per als camps són:

```text
O: 344407.565081,4553669.673733 [EPSG:25831]
D: 344475.279609,4554024.590093 [EPSG:25831]
```

3. Desa **ruta_obert**: **448,048353m**. La longitud supera la recta361,318253m perquè segueix els trams connectats.
4. Amb **més ràpid**, camp `v_kmh`, velocitat5km/h i mateixos punts, s'obtenen **0,089609671h =5,376580min**. La velocitat és una hipòtesi uniforme de l'exercici.

## Itinerari tancat

1. Extreu `passos` per atribut **pas_id=2** i desa **pas_p2**.
2. A `native:extractbylocation`, entrada xarxa, comparació amb pas_p2, predicat **disjoint**. Desa **xarxa_tancada**.
3. Repeteix la ruta amb els mateixos punts: **4876,695005m**, o **58,520340min** a5km/h.
4. Representa totes dues rutes i apropa la vista a l'extensió completa de la tancada. Identifica el pas alternatiu i la connexió amb el sud.

![La volta de la ruta tancada es compara amb el trajecte curt per P2. Els punts es mantenen al mateix lloc.](captures/xarxa.png){width=100% height=380pt}

La diferència no modifica la distància euclidiana. Tampoc totes les línies que es creuen són connexions: cal conservar la separació entre l'autopista i el vial que la travessa a un altre nivell.

## Àrees de servei

1. A `native:serviceareafrompoint`, entrada xarxa, criteri més ràpid, origen O, `v_kmh`, ambdós sentits i tolerància0.
2. Introdueix0,05/0,10/0,20h per als límits3/6/12min. Desa les sortides en línies.
3. Repeteix amb xarxa_tancada i mantén els mateixos colors i límits.

| Límit | Obert, longitud única | Tancat, longitud única |
| --- | ---: | ---: |
| 3min | 1863,763322m | 1480,689265m |
| 6min | 5586,766059m | 4565,420436m |
| 12min | 16315,694568m | 12706,175167m |

Table: Longitud única de les branques accessibles per xarxa amb P2 obert i tancat.

Els controls de longitud fan la unió geomètrica per no sumar trams coincidents. Són longituds de **branques accessibles**, no d'un trajecte únic. D entra en6min amb P2 obert i queda fora de12min amb la ruta tancada.

# D. Desenvolupament de la fricció

## Rasteritzar les cobertes i reclassificar

La capa vectorial és el [MCSC2024](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya). Per a un altre àmbit es pot descarregar un [retall](https://visors.icgc.cat/appdownloads/index.html?c=fmexomcsc) o el [GeoPackage complet](https://datacloud.icgc.cat/datacloud/cobertes-sol/gpkg/cobertes-sol-v1r0-2024.zip).

1. Carrega **cobertes** des de la connexió. Comprova classe numèrica i categoria textual.
2. A `gdal:rasterize`, entrada cobertes i **camp classe**, sense valor fix. Unitats georeferenciades,5/5m, regió comuna, Float32, inicial0 i NoData−9999.
3. Desa **classes.tif**. Identifica algunes cel·les: han de ser codis de coberta.

![El camp classe conserva els tipus de coberta. Resolució i extensió determinen la graella comuna.](captures/rasteritzar-cobertes.png){width=85% height=380pt}

4. Obre `native:reclassifybytable`, entrada classes, banda1. Utilitza **llegenda_costos** per completar les columnes mínim, màxim i pes. Exemples de files: **351 / 351 / 1**, **111 / 111 / 4**, **347 / 347 / 6**.
5. Afegeix0/0/99. Límits **mínim≤valor≤màxim**, NoData−9999, Float32 i NoData per als valors no previstos. Desa **base.tif**.
6. Consulta les mateixes cel·les:351→1,111→4,347→6. El99 encara és vàlid en aquest intermedi.

| Classes | Pes de la fricció |
| --- | ---: |
| 351 | 1 |
| 228,230,346,348,352 | 2 |
| 233 | 3 |
| 221–227,229,344,347 | 6 |
| 234,349,354,355,461–466 | 99, codi de barrera |
| Altres classes de la llegenda | 4 |
| 0, cobertura desconeguda | 99 |

Table: Pesos de fricció i codis de barrera assignats a les classes de coberta.

Una rasterització del camp **cost_model** proporciona un contrast dels pesos. La classe351 agrupa tota la xarxa viària, mentre que la347 generalitza zones industrials i de serveis; no resol els accessos de cada edifici o recinte.

## Identificar la plataforma de l'AP-7

1. Extreu cobertes on **classe=351**.
2. Crea un buffer35m dels **autopista_eixos** RTT, amb dissolució.
3. Intersecta coberta viària i banda. Desa **barrera_autopista** i contrasta-la sobre l'ortofoto.
4. Rasteritza-la amb valor1, inicial0, NoData−9999, Float32 i la mateixa graella. Desa **barrera.tif**.

La banda identifica la infraestructura dins d'una coberta viària que també conté carrers. Convertir tota la classe351 en NoData eliminaria també vials que es volen conservar. Els35m són un paràmetre declarat del model, no una mesura exacta de la plataforma.

## Rasteritzar els passos

1. A `gdal:rasterize`, selecciona **passos** i el camp **pas_id**.
2. Utilitza5/5m, mateixa extensió, Float32, inicial0 i NoData−9999.
3. Desa **pas.tif** i identifica les cel·les:1 als alternatius,2 a P2 i0 vàlid al fons.

![La màscara de passos conserva el seu identificador. El fons zero ha de ser vàlid perquè el condicional el pugui consultar.](captures/rasteritzar-passos.png){width=85% height=380pt}

El control de la graella és **375cel·les alternatives** i **91cel·les de P2**. Una graella diferent pot donar un altre recompte i desplaçar el contacte amb la barrera. Els corredors tenen amplada modelada20m i prolongacions40m sobre els eixos de travessa.

## Aplicar els condicionals

1. A la Calculadora ràster, selecciona les bandes **pas**, **barrera** i **base**. Fixa600×640 cel·les i la regió comuna.
2. Per a l'obert, dona prioritat a qualsevol pas:

```text
if("pas@1" > 0, 1,
   if("barrera@1" > 0, 99,
      if("base@1" = 0, 99, "base@1")))
```

3. Per al tancat, mantén els alternatius i marca P2 com a barrera:

```text
if("pas@1" = 1, 1,
   if(("pas@1" = 2) OR ("barrera@1" > 0), 99,
      if("base@1" = 0, 99, "base@1")))
```

4. Desa **friccio_numeric_obert/tancat**. Només ara executa Translate assignant99 com a NoData per crear **friccio_obert/tancat**.
5. Amb Identifica, comprova els dos costats de la plataforma i l'interior dels corredors. El pas ha d'arribar als dos costats; un polígon curt pot quedar desconnectat i un d'ample pot obrir més terreny del previst.

![La fricció tancada manté els passos alternatius i la distinció entre costos finits i barreres.](captures/friccio.png){width=100% height=380pt}

# E. Dels passos de fricció als costos

## Entrada correcta i valors intermedis

1. Selecciona la banda de **friccio_obert**, amb els passos ja inserits. No utilitzis **base** ni el numeric99 sense convertir-lo en NoData.
2. A la Calculadora ràster, aplica `"friccio_obert@1" * 5`. Mantén regió/dimensions i desa **cost_cella_obert.tif**.
3. Repeteix amb friccio_tancat. La conversió ha de conservar el conjunt de cel·les admeses i excloses.

| Comprovació | Fricció oberta | Cost obert | Fricció tancada | Cost tancat |
| --- | ---: | ---: | ---: | ---: |
| P2, X 344372,5 / Y 4553742,5 | 1 | 5 | NoData | NoData |
| Alternatiu, X 344097,5 / Y 4553577,5 | 1 | 5 | 1 | 5 |
| Coberta amb pes4 | 4 | 20 | 4 | 20 |
| Coberta amb pes6 | 6 | 30 | 6 | 30 |
| Autopista fora dels passos | NoData | NoData | NoData | NoData |

Table: Fricció integrada i cost per cel·la als passos i les cobertes dels dos escenaris.

![Els corredors oberts apareixen amb cost per cel·la5. La multiplicació canvia la magnitud del cost però no tanca un pas admès.](captures/cost-cella-pas.png){width=100% height=380pt}

**Diagnosi quan el pas desapareix:** identifica primer la fricció al corredor i després el cost. Si la primera ja és nul·la, revisa la màscara i el condicional. Si la fricció val1 però el cost és nul, revisa la banda triada i la graella. Si el cost val5 però no s'acumula, revisa origen, opcions de nuls i regió de r.cost.

## r.cost i r.path

1. A [r.cost](https://grass.osgeo.org/grass84/manuals/r.cost.html), entrada **cost_cella_obert**, capa d'inici **Origen O**, altres formes d'inici/aturada buides.
2. Moviment de cavall desactivat, conservar nuls activat i cost dels nuls buit. Regió comuna i5m.
3. Desa **cost_obert.tif** i **direccions_obert.tif**. Consulta el valor mostrejat a D.

![r.cost utilitza el cost per cel·la i Origen O, conservant les barreres nul·les.](captures/distancies-cost-parametres.png){width=85% height=380pt}

4. A [r.path](https://grass.osgeo.org/grass84/manuals/r.path.html), entrada **direccions_obert**, formatdegree i **Destí D** com a punt de reconstrucció.
5. Desa la ruta vectorial **ruta_cost_obert**. Repeteix la cadena amb el tancat, sense sobreescriure les sortides obertes.

![La reconstrucció parteix de D i segueix les direccions que retornen cap a O.](captures/distancies-path-parametres.png){width=85% height=380pt}

| Resultat | Obert | Tancat |
| --- | ---: | ---: |
| Longitud del camí ràster | 441,984848m | 1639,213562m |
| Cost acumulat a D | 1336,990078m ponderats | 4548,731957m ponderats |
| Cel·les excloses | 17.224 | 17.315 |

Table: Longitud del camí ràster, cost acumulat a D i cel·les excloses amb P2 obert i tancat.

Les91cel·les de diferència coincideixen amb P2. El cost és superior a la longitud perquè el recorregut travessa pesos diferents. No són minuts ni es poden sumar metres ponderats i temps com una mateixa magnitud.

![Comparació dels camins de cost sobre la superfície acumulada. Els passos i O/D es mantenen identificables.](captures/cost.png){width=100% height=380pt}

# F. Desenvolupament de la marxa anisòtropa

1. Carrega el [MDT ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions) **mdt** i retalla'l a ambit_calcul amb `gdal:cliprasterbyextent`, sense refinar la resolució. Desa **mdt_ambit.tif** i comprova600×640 cel·les de5m.
2. Converteix la fricció integrada en penalització temporal amb `("friccio_obert@1" - 1) * 0.125`. Conserva NoData. Els pesos1/2/4/6 passen a0/0,125/0,375/0,625s/m.
3. A [r.walk.points](https://grass.osgeo.org/grass84/manuals/r.walk.html), elevació **mdt_ambit**, fricció **friccio_temporal_obert**, inici **Origen O**.
4. Coeficients0.72,6.0,1.9998,-1.9998; lambda1; slope factor−0,2125m/m. Sense moviment de cavall, nuls exclosos, regió comuna5m.
5. Desa segons acumulats i direccions. Divideix els segons per60 per representar minuts. Reconstrueix la ruta amb les direccions i D.

![El MDT i la penalització temporal són entrades diferents. El cost dels nuls queda buit.](captures/marxa-parametres.png){width=85% height=380pt}

6. Executa r.walk de nou des de **D**, amb les mateixes entrades. Reconstrueix des d'O. No n'hi ha prou amb invertir la línia de l'anada.
7. Per al control pla, crea una elevació constant amb `"mdt_ambit@1" * 0`, mantenint la graella. Repeteix tots dos sentits.

| Model | O→D | D→O |
| --- | ---: | ---: |
| MDT, P2 obert | 489,156143s =8,152602min | 483,173590s =8,052893min |
| Elevació constant, P2 obert | 430,104744s | 430,104744s |
| MDT, P2 tancat | 1600,131968s =26,668866min | No necessari per a aquest control |

Table: Temps de marxa segons el relleu, el sentit del recorregut i l'estat de P2.

El control pla és simètric; amb MDT l'anada i la tornada difereixen gairebé6s. Els coeficients distingeixen desnivells amb signe. Un zero de penalització addicional no vol dir temps zero: r.walk continua calculant desplaçament i efecte del relleu. No multipliquis la penalització temporal per5.

![Els recorreguts d'anada i tornada provenen d'execucions diferents sobre el mateix lloc.](captures/marxa.png){width=100% height=380pt}

El MDT de5m pot simplificar el pas inferior i els temps del model no estan calibrats amb caminades observades.

# G. Resolució de les isòcrones

1. Selecciona la banda **marxa des d'O en minuts**. A [r.contour](https://grass.osgeo.org/grass84/manuals/r.contour.html), nivells3,6,12, mínim3punts per línia, regió comuna5m.
2. Desa **isocrones_obert**. A la Calculadora ràster crea les franges:

```text
if("minuts@1" <= 3, 1,
   if("minuts@1" <= 6, 2,
      if("minuts@1" <= 12, 3, 4)))
```

3. Blau0–3min, verd>3–6, taronja>6–12 i gris>12. NoData és una barrera, no un temps superior a12.
4. Repeteix amb P2 tancat, mateix MDT, origen i coeficients. Utilitza els mateixos colors i enquadrament.

![D entra entre les isòcrones6/12min amb P2 obert.](captures/isocrones-obert.png){width=100% height=380pt}

![Amb P2 tancat, D queda fora dels12min. Les franges encara mostren accés a altres cel·les.](captures/isocrones-tancat.png){width=100% height=380pt}

5. Compta les cel·les de classes1/2/3. La superfície acumulada és el recompte×25/10.000ha. Comprova que cap franja toca el límit de càlcul.

| Límit | Obert, cel·les | Obert, ha | Tancat, cel·les | Tancat, ha |
| --- | ---: | ---: | ---: | ---: |
| Fins a 3 min | 2704 | 6,7600 | 2484 | 6,2100 |
| Fins a 6 min | 10177 | 25,4425 | 7573 | 18,9325 |
| Fins a 12 min | 33205 | 83,0125 | 21949 | 54,8725 |

Table: Recomptes de cel·les i superfícies acumulades fins als límits de temps amb P2 obert i tancat.

La xarxa a velocitat uniforme arriba a D en 5,38 min, mentre que la marxa amb penalitzacions de coberta i MDT requereix 8,15 min. Són models diferents. La superfície de franges ràster no s'ha de substituir per un buffer de les branques de xarxa.

# Posada en comú i zona alternativa

La resposta final ha de separar **distància recta, itinerari de xarxa, cost ponderat i temps de marxa**. Tancar P2 modifica les connexions i les superfícies de cost, però no les posicions. Els passos han de seguir oberts en el cost per cel·la abans d'acumular-lo.

Per a la zona alternativa, demana justificar fonts, O/D, regió, resolució, pesos i corredors. Els enllaços de la taula inicial porten als recursos de descàrrega. En un GeoTIFF MCSC, 1–41 són l'índex ràster; els codis vectorials 111–466 són una altra codificació i necessiten la seva llegenda.

Comprovació de tancament: obrir el projecte en una altra carpeta amb les dades de treball, inspeccionar els passos al cost, revisar les unitats de cada sortida i assegurar que les isòcrones no queden truncades.
