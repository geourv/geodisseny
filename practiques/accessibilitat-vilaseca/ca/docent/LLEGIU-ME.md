---
title: "Resolució docent: accessibilitat de Vila-seca"
author: Benito Zaragozí
lang: ca
date: "Guia revisada: 14 d'octubre de 2026"
content_status: draft
---

# Preparar la tasca de Moodle

El cas es distribueix ara en tres tasques amb lectures pròpies: **xarxa vectorial**, **model ràster** i **temps d'accés i ampliacions**. Per preparar Moodle, utilitza els enunciats dels documents docents de cada subpràctica. Aquest guió conserva la resolució conjunta; l'enunciat general següent correspon al paquet combinat anterior.

1. Activa l'edició del curs i tria **Afegir una activitat o un recurs → Tasca**. Posa-hi el nom **Accessibilitat: distància, xarxa i cost**.
2. A **Descripció**, enganxa el bloc següent, des de «Dades de partida» fins al final de «Qualificació».
3. A **Fitxers addicionals**, adjunta **`accessibilitat-vilaseca-2026-10-14-r6-ca.zip`**, el paquet d'inici. Conté el GeoPackage i el `LLEGIU-ME.pdf` de l'alumnat.
4. Comprova la tasca amb la vista d'estudiant: el ZIP s'ha de poder descarregar i l'enunciat ha de quedar visible a la descripció. La resolució d'aquest document i el paquet docent serveixen per preparar la classe.

## Enunciat per copiar a la descripció

**Dades de partida.** Descarregueu `accessibilitat-vilaseca-2026-10-14-r6-ca.zip`, adjunt a aquesta tasca, i descomprimiu-lo en una carpeta local pròpia. Conté `accessibilitat-vilaseca.gpkg` i `LLEGIU-ME.pdf`. El GeoPackage incorpora el projecte **inici**, els punts O/D, la xarxa preparada amb eixos ICGC, les cobertes, els eixos de l'AP-7, els passos, el límit, l'àmbit de càlcul, el MDT i l'ortofoto. Obriu-lo amb QGIS 3.44, GDAL i GRASS, seguint la guia.

El cas preparat és el **Camí del Mas de la Plana, al pas de l'AP-7 de Vila-seca**. Els dos punts són als costats de la infraestructura i es mantenen fixos durant la comparació. La xarxa procedeix del **Referencial Topogràfic Territorial2024 de l'ICGC**, amb escala òptima de treball d'1:5.000. Les cobertes, elevacions, límit i ortofoto també són de l'ICGC. Els càlculs ràster utilitzen EPSG:25831 i una graella de **5 m**. Els pesos, trams admesos i corredors són supòsits docents, no mesures de caminades o permisos de pas.

**Treball de classe.** El professor indicarà a classe quins apartats, exercicis i comprovacions són obligatoris dins del **70% de la qualificació** i ho recollirà en aquesta tasca. La guia desenvolupa un recorregut complet: no tots els passos són automàticament obligatoris. La comparació principal relaciona tres longituds entre els mateixos O/D: **recta euclidiana, camí de menor cost en ràster i ruta més curta en xarxa**. Els blocs que es poden seleccionar són:

1. **Distància euclidiana i proximitat.** Calculeu la recta vectorial. Prepareu la cel·la origen i obteniu la distància ràster amb `r.grow.distance`; contrasteu-la amb Proximitat de GDAL. Expliqueu la diferència entre punts i centres de cel·la.
2. **Camí ràster.** Rasteritzeu les cobertes i apliqueu els pesos de `llegenda_costos`. Integreu l'AP-7 i els passos abans de convertir el codi de barrera en NoData. Executeu **r.cost** des d'O i reconstruïu el camí amb **r.path**, seleccionant les direccions i D. Mesureu-ne la longitud i conserveu el cost ponderat en una columna separada.
3. **Ruta en xarxa.** Comproveu les connexions dels eixos ICGC preparats i calculeu el camí més curt, amb cost de longitud. En Vila-seca, compareu P2 obert i tancat, retirant l'eix **rtt_id1354754**, mantenint O/D i documentant la selecció dels trams. Si el mòdul retorna sense ruta, conserveu aquest resultat i distingiu-lo d'una distància zero.
4. **Comparació.** Prepareu un mapa del camí ràster, un mapa de les rutes de xarxa i una taula amb les tres longituds en metres. Incloeu-hi el control de proximitat i distingiu-lo del cost acumulat. Expliqueu què considera cada model.

**Ampliacions per aspirar a l'excel·lent.** Desenvolupeu una pregunta que vagi més enllà de repetir els passos seleccionats. Podeu comparar diversos destins, calcular àrees de servei, marxa anisòtropa o isòcrones, repetir l'anàlisi amb altres pesos o resolucions, o estudiar una zona alternativa. Canvieu un paràmetre cada vegada i conserveu una referència. Justifiqueu què heu après; més operacions no impliquen una millor conclusió. Les ampliacions no substitueixen els obligatoris.

**Preguntes obertes i aplicacions.** Quin destí o origen és més vulnerable al tancament? Canvia l'ordre dels destins segons el model? Quina connexió convindria inspeccionar sobre el terreny? Proposeu una aplicació geogràfica, com comparar accessos a un equipament o connexions vulnerables, i expliqueu quines dades farien falta per desenvolupar-la. Si treballeu una zona alternativa, d'acord amb el professor, justifiqueu fonts, O/D, extensió, resolució, pesos i passos; reviseu la connectivitat i calculeu controls propis.

**Informe.** Presenteu la pregunta i l'àmbit, les dades i decisions, el procediment amb controls, els mapes i taules dels apartats seleccionats, i una conclusió amb límits. Separeu metres, cost ponderat i temps. Podeu enregistrar fragments de la pantalla mentre treballeu i després pausar el vídeo per desar captures dels paràmetres o resultats importants. Comproveu la llegibilitat, numereu-les i expliqueu què demostra cadascuna; per als mapes finals, feu una exportació cartogràfica. El vídeo és una ajuda, no un lliurament obligatori tret que el professor ho indiqui. La guia detalla aquesta manera de documentar el treball.

**Lliurament.** Entregueu `accessibilitat-vilaseca-cognom.gpkg`, amb les capes generades i el projecte incrustat; una còpia externa `accessibilitat-vilaseca-cognom.qgz`; i `accessibilitat-vilaseca-cognom.pdf`, amb l'informe. Afegiu els TIFF referenciats pel projecte, conservant l'estructura de carpetes si ho empaqueteu en un ZIP. Comproveu que s'obre des d'una altra ubicació sense rutes trencades. En una zona alternativa, identifiqueu el cas al nom dels fitxers.

**Qualificació.** **70% als apartats obligatoris que el professor indicarà a classe**; **20% a les ampliacions**; **10% a la qualitat de l'informe, captures, mapes i organització**. Una ampliació permet aspirar a l'excel·lent quan planteja una pregunta, aplica el mètode amb controls i interpreta els resultats. Intentar-la no garanteix una nota ni substitueix els obligatoris.

# Preparació de la resolució docent

Selecciona abans de la classe els apartats que entraran al 70% obligatori i comunica'ls a l'alumnat; deixa la mateixa selecció a Moodle. Les parts A–E ofereixen la comparació principal. Les àrees de servei de C i les parts F/G ofereixen ampliacions, juntament amb les preguntes obertes. Ajusta l'abast al temps de classe i distingeix una demostració docent d'un resultat que l'alumnat haurà de calcular.

La resolució següent conserva els controls de tot el recorregut. Per orientar les ampliacions, demana una pregunta concreta, una comparació de referència, un registre de paràmetres i una discussió dels límits. Si es canvia de zona, els controls de Vila-seca deixen de ser valors esperats. Valora la justificació d'una aplicació geogràfica i les dades que requeriria, no només la semblança visual amb les captures de referència.

## Pregunta i preparació de la pràctica

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
| Xarxa a peu | [ICGC, Referencial Topogràfic Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial) | Eixos2024 seleccionats/nodificats; rtt_id i atributs originals; velocitat docent5km/h |
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
| O | 344407,000000 | 4553668,360000 |
| D | 344473,010000 | 4554030,720000 |

Table: Coordenades d'O i D per al càlcul de la distància vectorial.

Les diferències són **66,01m** en X i **362,36m** en Y. Pitàgores dona **368,323349m**. Tancar P2 no modifica aquesta separació geomètrica. La interpretació esperada és que una recta entre punts encara no és un itinerari possible.

# B. Resolució de la distància ràster

## Crear la cel·la origen i conservar el fons correcte

1. A `gdal:rasterize`, selecciona **Origen O**, valor fix1, sense camp d'atributs.
2. Unitats georeferenciades, resolució5/5m, extensió d'**ambit_calcul**, Float32, inicial0 i NoData−9999. Desa **origen_zero.tif**.
3. Comprova una única cel·la amb1. Amb `gdal:translate`, crea **origen_null.tif** assignant0 com a NoData, sense canviar la graella.
4. Aquesta còpia té únicament O com a cel·la no nul·la; és l'entrada de GRASS. Conserva origen_zero per al contrast GDAL amb llista de valors objectiu1.

## r.grow.distance i control dels centres

1. Obre [r.grow.distance](https://grass.osgeo.org/grass84/manuals/r.grow.distance.html), amb **origen_null**, mètrica **euclidean** i cerca de NULL desactivada.
2. Fixa la regió comuna i5m; desa **distancia_grass.tif**.
3. Amb `native:rastersampling`, mostreja **Destí D**. El resultat és **370,742498m**.
4. Repeteix amb `gdal:proximity`, entrada origen_zero, objectiu1, unitats georeferenciades, Float32 i NoData−9999. Ha de concordar amb GRASS al mil·límetre.

![La mètrica euclidiana s'aplica a la cel·la origen; el fonsNULL evita que el fons es tracti com un conjunt d'orígens.](captures/distancia-grass.png){width=85% height=380pt}

| Centre de cel·la | X, m | Y, m |
| --- | ---: | ---: |
| O | 344407,5 | 4553667,5 |
| D | 344472,5 | 4554032,5 |

Table: Coordenades dels centres de cel·la d'O i D en la graella comuna.

La separació de centres és65m en X i365m en Y. El control és `sqrt(65²+365²)`. La diferència de **2,419149m** respecte del vector és una conseqüència de representar els punts amb cel·les, no una ruta que eviti l'autopista.

# C. Xarxa, tancament i àrees de servei

## Itinerari obert

1. A `native:shortestpathpointtopoint`, selecciona **xarxa**, criteri **més curt**, direcció per defecte ambdós sentits i tolerància topològica0m.
2. Utilitza O/D de les capes amb tolerància punt–xarxa0,1m. Les coordenades per als camps són:

```text
O: 344407.000000,4553668.360000 [EPSG:25831]
D: 344473.010000,4554030.720000 [EPSG:25831]
```

3. Desa **ruta_obert**: **454,104650m**. La longitud supera la recta368,323349m perquè segueix els trams connectats.
4. Amb **més ràpid**, camp `v_kmh`, velocitat5km/h i mateixos punts, s'obtenen **0,090820930h =5,449256min**. La velocitat és una hipòtesi uniforme de l'exercici.

## Itinerari tancat

1. Identifica **rtt_id1354754** a `xarxa` i contrasta aquest eix de P2 amb **pas_id2** i l'ortofoto.
2. A `native:extractbyexpression`, conserva `"rtt_id" <> 1354754` i desa **xarxa_tancada**. El tancament es defineix per l'eix ICGC identificat, no per tots els eixos llargs que toquen el polígon ràster.
3. Repeteix la ruta amb els mateixos punts. QGIS i el graf de control retornen **sense ruta**. La capa de ruta tancada és buida i el control conserva longitud/temps nuls, no zeros.
4. Representa la ruta oberta, l'eix retirat i el component d'O. La manca de ruta en aquesta xarxa preparada no certifica la manca de tota alternativa física al territori.

![La ruta oberta segueix la xarxa ICGC per P2. En retirar l'eix1354754, el graf preparat deixa de connectar els mateixos O i D.](captures/xarxa.png){width=100% height=380pt}

La diferència no modifica la distància euclidiana. Tampoc totes les línies que es creuen són connexions: cal conservar la separació entre l'autopista i el vial que la travessa a un altre nivell.

## Àrees de servei: ampliació a Vila-seca

1. A `native:serviceareafrompoint`, entrada xarxa, criteri més ràpid, origen O, `v_kmh`, ambdós sentits i tolerància0.
2. Introdueix0,05/0,10/0,20h per als límits3/6/12min. Desa les sortides en línies.
3. Repeteix amb xarxa_tancada i mantén els mateixos colors i límits.

| Límit | Obert, longitud única | Tancat, longitud única |
| --- | ---: | ---: |
| 3min | 448,384607m | 68,418647m |
| 6min | 1116,560723m | 68,418647m |
| 12min | 3606,611447m | 68,418647m |

Table: Longitud única de les branques accessibles per xarxa amb P2 obert i tancat.

Els controls de longitud fan la unió geomètrica per no sumar trams coincidents. Són longituds de **branques accessibles**, no d'un trajecte únic. D entra en6min amb P2 obert. En retirar P2, augmentar el límit de3 a12min no permet sortir del component d'O: l'abast es manté en68,42m.

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

## Rasteritzar els vials RTT

La coberta MCSC pot generalitzar un camí dins d'una classe de conreu o d'un recinte. Rasteritza **xarxa** amb valor fix 1, sense camp, resolució5/5m, regió comuna, Float32, inicial0 i NoData−9999. Desa **vials.tif**.

![Els eixos RTT admesos es rasteritzen amb pes 1 abans d'integrar-los amb cobertes, barreres i passos.](captures/rasteritzar-vials.png){width=85% height=380pt}

Control:15.113cel·les de vial;10.557 no tenien pes1 a la base de cobertes. La màscara no és un permís de pas: conserva les exclusions i les connexions del model. Vials es consulta després de barrera/P2 tancat i abans de base.

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

1. A la Calculadora ràster, selecciona les bandes **pas**, **barrera**, **vials** i **base**. Fixa600×640 cel·les i la regió comuna.
2. Per a l'obert, dona prioritat a qualsevol pas:

```text
if("pas@1" > 0, 1,
   if("barrera@1" > 0, 99,
      if("vials@1" = 1, 1,
         if("base@1" = 0, 99, "base@1"))))
```

3. Per al tancat, mantén els alternatius i marca P2 com a barrera:

```text
if("pas@1" = 1, 1,
   if(("pas@1" = 2) OR ("barrera@1" > 0), 99,
      if("vials@1" = 1, 1,
         if("base@1" = 0, 99, "base@1"))))
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
| Longitud del camí ràster | 474,766594m | 1920,990258m |
| Cost acumulat a D | 474,766594m ponderats | 2840,376259m ponderats |
| Cel·les excloses | 16.987 | 17.078 |

Table: Longitud del camí ràster, cost acumulat a D i cel·les excloses amb P2 obert i tancat.

Les91cel·les de diferència coincideixen amb P2. Amb el pas obert, cost i longitud coincideixen perquè el camí recorre cel·les de pes1; en el tancat es travessen pesos diferents. No són minuts ni es poden sumar metres ponderats i temps com una mateixa magnitud.

![Comparació dels camins de cost sobre la superfície acumulada. Els passos i O/D es mantenen identificables.](captures/cost.png){width=100% height=380pt}

# F. Desenvolupament de la marxa anisòtropa: ampliació a Vila-seca

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
| MDT, P2 obert | 401,797517s =6,696625min | 394,465679s =6,574428min |
| Elevació constant, P2 obert | 340,724610s | 340,724610s |
| MDT, P2 tancat | 1555,331669s =25,922194min | No necessari per a aquest control |

Table: Temps de marxa segons el relleu, el sentit del recorregut i l'estat de P2.

El control pla és simètric; amb MDT l'anada i la tornada difereixen uns7,33s. Els coeficients distingeixen desnivells amb signe. Un zero de penalització addicional no vol dir temps zero: r.walk continua calculant desplaçament i efecte del relleu. No multipliquis la penalització temporal per5.

![Els recorreguts d'anada i tornada provenen d'execucions diferents sobre el mateix lloc.](captures/marxa.png){width=100% height=380pt}

El MDT de5m pot simplificar el pas inferior i els temps del model no estan calibrats amb caminades observades.

# G. Resolució de les isòcrones: ampliació a Vila-seca

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
| Fins a 3 min | 2831 | 7,0775 | 2552 | 6,3800 |
| Fins a 6 min | 10924 | 27,3100 | 7677 | 19,1925 |
| Fins a 12 min | 35430 | 88,5750 | 22109 | 55,2725 |

Table: Recomptes de cel·les i superfícies acumulades fins als límits de temps amb P2 obert i tancat.

La xarxa a velocitat uniforme arriba a D en 5,45 min, mentre que la marxa amb penalitzacions de coberta, vials integrats i MDT requereix 6,70 min. Són models diferents. Amb P2 tancat, la superfície ràster conserva un camí a D, però la xarxa d'eixos preparada no hi connecta; cal explicar les condicions de moviment i cobertura de cada model.

# Posada en comú i zona alternativa

La resposta final ha de separar **distància recta, itinerari de xarxa, cost ponderat i temps de marxa**. Tancar P2 modifica les connexions i les superfícies de cost, però no les posicions. Els passos han de seguir oberts en el cost per cel·la abans d'acumular-lo.

Revisa els resultats dels apartats obligatoris anunciats, la qualitat dels controls i la interpretació. En l'ampliació, pregunta què canvia respecte de la referència, quin supòsit explica el canvi i com es podria contrastar. Les captures extretes d'un vídeo són evidències seleccionades: una gravació completa no substitueix l'informe ni la comprovació de les dades.

Per a la zona alternativa, demana justificar fonts, O/D, regió, resolució, pesos i corredors. Els enllaços de la taula inicial porten als recursos de descàrrega. En un GeoTIFF MCSC, 1–41 són l'índex ràster; els codis vectorials 111–466 són una altra codificació i necessiten la seva llegenda.

Comprovació de tancament: obrir el projecte en una altra carpeta amb les dades de treball, inspeccionar els passos al cost, revisar les unitats de cada sortida i assegurar que les isòcrones no queden truncades.
