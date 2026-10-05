---
title: "Pràctica: de la torxa al polígon industrial"
subtitle: "Intervisibilitat puntual, carretera i àrea amb QGIS"
author: Benito Zaragozí
lang: ca
date: "Preparació: 2 d'octubre de 2026"
content_status: draft
---

# Tres preguntes, en aquest ordre

Comença amb una torxa industrial de la Canonja: **es veu des d'un punt de la carretera?** Després estudia el recorregut de la TV-3148 entre Vila-seca i l'enllaç de la Pineda: **quines posicions es veuen al llarg de la via?** Finalment amplia els objectius a una àrea industrial: **des d'on es veu alguna part del polígon?**

Els tres exercicis comparteixen elevacions i àmbit, però no compten el mateix. El primer dona una resposta 0/1; el segon suma observadors; el tercer resumeix objectius industrials. Cap resultat mesura directament persones exposades o impacte paisatgístic.

## Preparar la sessió

1. Utilitza **QGIS 3.44**, amb Processament i GDAL. Els controls corresponen a QGIS **3.44.11** i GDAL **3.10.3**.
2. Descomprimeix tot el paquet de Moodle i obre `projectes/00-inici.qgz`.
3. Comprova **EPSG:25831**, unitats mètriques i el·lipsoide **Cap / NONE**. Crea `treball` al costat de `dades` i desa-hi les teves sortides.
4. Conserva juntes les carpetes. `fonts` conté les fonts; `dades`, les entrades preparades; `resultats`, els controls. Les capes addicionals estan al grup plegat del projecte.

| Projecte | Vista preparada |
| --- | --- |
| `00-inici.qgz` | Torxa, carretera i polígon |
| `01-torxa.qgz` | Detall de la torxa sobre ortofoto |
| `02-intervisibilitat.qgz` | Parelles entre T i receptors |
| `03-conca-mdt.qgz` | Conca puntual amb MDT |
| `04-conca-mds.qgz` | Conca puntual amb MDS |
| `05-carretera.qgz` | Mostres de carretera i visió de T |
| `06-acumulada.qgz` | Suma de 37 conques MDT |
| `07-poligon.qgz` | Visió d'algun objectiu industrial |
| `08-area-ponderada.qgz` | Fragments i mostres d'àrea |
| `09-perimetre.qgz` | Coberta original i recinte petroquímic d'estudi |

![T és la torxa; la línia segueix la TV-3148 i el contorn delimita el recinte petroquímic d'estudi.](captures/visibilitat-costa-dades.png){width=100%}

L'ortofoto és una imatge del servei **WMS de l'ICGC**, obtinguda amb GetMap i desada com a GeoTIFF georeferenciat. La petició general té **10 m per píxel**; els retalls industrial i de la torxa, **2,5 i 0,5 m per píxel**. La capa del servei és l'ortofoto de 25 cm de 2025; la resolució demanada per a cada retall queda a `fonts/fonts.json`.

![L'MDS es mostra amb el mateix enquadrament que l'ortofoto. La llegenda expressa cotes superficials en metres; la cel·la de càlcul és de 5 m.](captures/visibilitat-costa-mds.png){width=100%}

Compara la localització de les instal·lacions a l'ortofoto amb les elevacions de l'MDS. L'MDT representa el terreny; l'MDS incorpora també cobertes i vegetació. Les cotes procedeixen del LiDAR 2021–2023, una data diferent de la imatge de 2025.

## Situar el cas: dos polígons i el port

El **complex petroquímic de Tarragona** agrupa instal·lacions de diverses empreses als polígons **Nord**, **Sud** i al **Port de Tarragona**. El nostre sector pertany al Polígon Sud, a l'entorn de la Canonja: no representa tot el complex ni la refineria del Polígon Nord.

La implantació petroquímica s'intensificà als anys seixanta. Jordi Rosell, a Enciclopèdia.cat, situa la posada en marxa de Dow i IQA el **1967**, i la producció de poliestirè de BASF el **1969**. La cronologia de Repsol data la construcció de la refineria a partir de **1973** i l'inici d'activitat el **1976**.

El port facilitava l'arribada de matèries primeres per mar: inicialment, Dow importava etilè. L'agrupació de plantes permetia també utilitzar productes d'altres processos. Avui, els racks de conduccions connecten plantes i port, com explica Farnós Marsal (2025). Aquesta relació productiva i logística ajuda a entendre la localització i el paisatge de torres, dipòsits, molls i canonades. Les fonts històriques s'indiquen al final del guió.

## Entrades comunes

La graella té **2.000 × 2.000 cel·les de 5 m**: X **342000–352000**, Y **4549000–4559000**. L'MDT és el retall natiu de 5 m de l'ICGC; l'MDS d'1 m s'ha agregat pel màxim a 5 m. Les elevacions corresponen al producte LiDAR **2021–2023**; l'ortofoto és de **2025**.

Per calcular, carrega `dades/mdt-calcul.tif` amb el nom **MDT**, `dades/mds-calcul.tif` com **MDS** i `dades/domini-valid.tif` com **Domini**. Aquestes còpies tracten els buits del mar cartografiat com una superfície a 0 m. Domini exclou mar, buits d'elevació i línies afectades per altres elevacions desconegudes: val **1 en 3.490.455 cel·les** i NoData a la resta.

El màxim de l'MDS pot eixamplar obstacles estrets. Les capçades es tracten com a opaques; el model no representa transparència vegetal ni canvis de la flama o de l'atmosfera.

# A. Primer, una torxa i unes línies de visió

## A1. Identificar T i fixar-ne la cota

Obre `01-torxa.qgz`. T prové del node **7682543312** d'OpenStreetMap, classificat com a *flare*, i s'ha contrastat amb l'ortofoto. El punt original és a **(346894,824499;4552508,353399) m**. La posició ràster és **(346892,5;4552507,5) m**: el desplaçament al centre de cel·la és de 2,48 m.

![T correspon a una torxa identificable. L'ortofoto aporta la localització; la cota s'obté del model d'elevació.](captures/visibilitat-costa-torxa.png){width=100%}

| Magnitud | Metres |
| --- | ---: |
| MDT a T | 20,941999 |
| Pic MDS, comprovat també al retall d'1 m | 151,311996 |
| Diferència pic–terreny | 130,369997 |
| Cota de T en l'exercici, pic + 1 m | 152,311996 |
| Altura de T sobre MDT | 131,369997 |
| Altura de T sobre MDS | 1 |

Els aproximadament **130,4 m** són una estimació d'estructura a partir del LiDAR. El metre addicional és una separació de model respecte de la superfície digital: **no és una mesura de la flama**. Consulta `dades/torxa.gpkg`: `z_abs_m`, `h_mdt_m` i `h_mds_m` conserven les cotes i altures utilitzades.

## A2. Calcular la conca puntual amb MDT

Obre **Procés → Caixa d'eines** o utilitza **Ctrl+Alt+T**. El botó de la barra obre el mateix panell. A la cerca, escriu **Viewshed** i comprova el proveïdor **GDAL**.

![El menú Procés dona accés a Caixa d'eines i mostra la drecera.](captures/visibilitat-acces-menu.png){width=90%}

![El botó de la barra és un altre accés al mateix panell de Processament.](captures/visibilitat-acces-barra.png){width=90%}

![Caixa de Processament oberta: GDAL → Miscel·lània ràster → Viewshed. El requadre marca l'eina.](captures/visibilitat-acces-caixa-viewshed.png){width=90%}

1. Obre **Conca visual / Viewshed**, `gdal:viewshed`.
2. Entrada: **MDT**, banda **1**.
3. Observador: `346892.5,4552507.5 [EPSG:25831]`.
4. Altura d'observador: **131.36999702453613**; altura de destinació: **1.7**.
5. Distància màxima: **0**, tota la finestra.
6. Paràmetres addicionals:

```text
-vv 1 -iv 0 -ov 255 -a_nodata 255 -cc 0.85714
```

7. Desa la conca crua a `treball` i carrega-la com **Conca T MDT**.
8. A **Calculadora ràster**, `native:rastercalc`, aplica:

```text
"Domini@1" * "Conca T MDT@1"
```

9. Mantén la graella comuna, cel·la 5 m i EPSG:25831. Desa `treball/T-mdt.tif`.

![Viewshed demana altura relativa sobre la superfície d'entrada. Després cal aplicar Domini per conservar els llocs no calculats.](captures/visibilitat-costa-punt.png){width=90%}

Configura **1 visible**, **0 ocult** i NoData separat. El codi numèric de NoData pot canviar en una sortida de Calculadora ràster; comprova'n la propietat de banda, no el tractis com un zero. El control és **2.962.199 cel·les visibles**, el **84,87%** del domini comparable.

## A3. Consultar parelles receptor–torxa

Executa **Mostreja els valors ràster**, `native:rastersampling`, amb aquestes entrades:

- Punts: `dades/receptors.gpkg`.
- Ràster: el teu `T-mdt.tif`.
- Prefix: `T_mdt_`.

Llegeix els valors de R1–R4. R5, fora del retall, ha de quedar nul.

Els receptors es troben en quatre mostres del recorregut: **R1=C05, R2=C11, R3=C13, R4=C37**. S'han triat per mostrar casos diferents. No representen població, ús de la carretera ni accés públic als emplaçaments.

## A4. Repetir amb MDS sense moure els extrems

1. Repeteix Viewshed amb **MDS**, T a les mateixes coordenades i altura d'observador **1 m**.
2. Altura de destinació **0** i distància màxima **0**. A les opcions addicionals:

```text
-om DEM -cc 0.85714 -a_nodata -9999
```

3. Desa la sortida, en Float64, com **Cota mínima MDS**.
4. Obre Calculadora ràster amb MDT, Domini i Cota mínima MDS:

```text
"Domini@1" * (("MDT@1" + 1.7) >= "Cota mínima MDS@1")
```

El mode **DEM** retorna cota absoluta mínima; ignora l'altura de destinació. La comparació manté els receptors a **MDT + 1,7 m**. No introdueix els ulls a 1,7 m sobre una teulada.

![La fórmula compara cotes absolutes i conserva NoData mitjançant Domini.](captures/visibilitat-costa-cota-minima.png){width=95%}

Repeteix el mostreig als receptors. Amb MDS, el control global és **447.860 cel·les visibles**, el **12,83%** del domini.

| Parella | MDT | MDS | Interpretació |
| --- | ---: | ---: | --- |
| T–R1 | 1 | 1 | Visió en els dos models |
| T–R2 | 0 | 0 | Obstacle al relleu |
| T–R3 | 1 | 0 | L'MDS afegeix una intercepció |
| T–R4 | 1 | 0 | Canvi de resposta amb superfície |
| T–R5 | Nul | Nul | Fora del retall |

![Les línies verdes mostren parelles visibles amb MDS; les discontínues, ocultes. R5 és no calculat.](captures/visibilitat-costa-intervisibilitat.png){width=100%}

![Els perfils comparteixen escales dins de cada fila. El detall dels últims 80 m permet localitzar l'obstacle pròxim a R3.](figures/visibilitat-perfils.svg){width=100%}

**Conserva:** els dos mapes, la cota mínima, el domini, la taula de parelles i l'explicació d'un perfil. Distingeix el resultat del model d'una observació de camp.

\clearpage

# B. Després, la conca acumulada de carretera

## B1. Preparar 37 observadors

El recorregut fa **3.652,272633 m** i segueix una trajectòria única sobre els eixos RTT de la TV-3148. Arriba fins a l'enllaç amb la TV-3146, a l'entrada de la Pineda. Les dues calçades i les rotondes són a la font; la capa preparada evita sumar-les com si fossin un únic trajecte de longitud doble. No és un model de sentits de circulació.

A **Punts al llarg de la geometria**, `native:pointsalonglines`, utilitza `dades/carretera.gpkg`:

- Distància: **98.71007115541471 m**.
- Desplaçament inicial: **49.355035577707355 m**.
- Desplaçament final: **0**.

![El pas divideix el recorregut en 37 intervals iguals i cada mostra queda a mig interval.](captures/visibilitat-costa-carretera.png){width=90%}

Comprova **37 punts**. A `dades/mostres-carretera.gpkg`, els camps `x`, `y` són els centres de cel·la del càlcul; `pk_m`, la distància des de l'inici; `pes`, els metres representats. La suma dels pesos recupera la longitud del recorregut.

## B2. Calcular i sumar conques

Repeteix Viewshed sobre MDT per a C05, C11 i C13. Utilitza les coordenades dels atributs, altura d'origen **1,7 m**, altura de destinació **1,7 m** i els mateixos codis, curvatura i màscara. Conserva les tres sortides per comprovar que una posició de carretera no dona el mateix mapa que una altra.

**Viewshed calcula un punt per execució; QGIS pot repetir-lo per lots.** Les tres execucions individuals anteriors serveixen per entendre i contrastar el procediment. El càlcul complet de les 37 posicions s'automatitza: no cal introduir 37 vegades les coordenades a mà.

### Preparar el lot gràfic de 37 files

1. Carrega `dades/mostres-carretera.gpkg` i posa **C** com a nom de la capa.
2. A la caixa d'eines, fes clic dret sobre Viewshed i tria **Execute as batch process…**, o el botó equivalent del diàleg de paràmetres.
3. A la columna **OBSERVER**, obre l'emplenament automàtic i l'opció **Add Values by Expression…**. Aquesta expressió retorna les coordenades ordenades per identificador:

```text
aggregate(
  layer := 'C',
  aggregate := 'array_agg',
  expression := to_string("x") || ',' || to_string("y")
                || ' [EPSG:25831]',
  order_by := "id"
)
```

4. Comprova **37 files útils**, de C01 a C37. Si hi ha una fila inicial buida, elimina-la. Les coordenades provenen dels camps ajustats als centres de cel·la.
5. Introdueix els valors comuns a la primera fila i aplica **Fill Down** a cada columna: **MDT**, banda **1**, altura d'origen **1,7**, altura de destinació **1,7**, abast **0** i opcions `-vv 1 -iv 0 -ov 255 -a_nodata 255 -cc 0.85714`.
6. Tria una carpeta nova sota `treball` per a les sortides. L'opció **Fill with numbers** genera noms diferents per a cada fila. Comprova que hi ha **37 rutes úniques**; no reutilitzis un sol nom per a tot el lot.
7. Executa el lot i revisa el registre. Cada fila produeix un ràster; l'execució per lots encara **no els suma ni aplica Domini**.
8. Desa la configuració JSON del lot des del diàleg si vols recuperar les mateixes files en una altra sessió. Revisa les rutes quan canviïs de carpeta.

Les opcions es descriuen a la [documentació del processament per lots de QGIS](https://docs.qgis.org/3.44/en/docs/user_manual/processing/batch.html). Els noms poden aparèixer traduïts a la instal·lació utilitzada.

### Sumar i emmascarar

Els **37 ràsters** de `resultats/conques-carretera-mdt` ja incorporen la màscara. Un subconjunt de tres conques no s'ha de comparar amb el control de 37. Per treballar amb les conques que acabes de produir, suma les sortides crues i aplica Domini al resultat final.

1. Obre **Estadístiques de cel·la**, `native:cellstatistics`.
2. Entrades: els 37 ràsters C01–C37; estadística: **Suma**.
3. Referència: C01; **Ignora NoData: desactivat**; valor NoData de sortida: **255**.
4. Desa `treball/carretera-suma.tif` i representa'l amb una escala de **0 a 37**.

Si has sumat les conques crues del lot, carrega aquella suma com **Suma C bruta** i aplica `"Domini@1" * "Suma C bruta@1"` a Calculadora ràster, amb la graella comuna. Amb una mateixa màscara per a totes les entrades, aquesta operació equival a emmascarar cada conca abans de sumar-la.

![El mapa compta posicions amb visió. El màxim observat és 33; el màxim possible és 37.](captures/visibilitat-costa-acumulada.png){width=100%}

El control té **1.461.016 cel·les amb almenys una visió** i màxim **33**. En una cel·la amb valor 12, la longitud representada és $12\times98,710071=1.184,52$ m i la fracció, $12/37=32,43\%$. La suma és cel·la a cel·la: no sumis les hectàrees de les 37 conques.

### Executar la cadena automatitzada del paquet

El fitxer `reproduccio/lots_visibilitat.py` llegeix les files preparades i executa `gdal:viewshed` per a cada punt. Aplica la màscara i desa cada binari, la suma i el percentatge ponderat. Obre la consola Python de QGIS amb un dels projectes del paquet obert i executa:

```python
from pathlib import Path
from qgis.core import QgsProject
p = Path(QgsProject.instance().homePath()).parent
exec((p / 'reproduccio/lots_visibilitat.py').read_text())
calcula_lot(p, 'carretera', 'mdt')
```

La sortida és `treball/lot-carretera-mdt/`: 37 binaris C, `nombre.tif`, `percent.tif`, intermedis i `lot.json` amb els paràmetres. El directori ha de ser nou; el guió refusa sobreescriure'l. Per a una altra execució, passa una destinació nova amb `sortida=p / 'treball/repeticio-1'`.

Aquest guió executa automàticament la cadena de càlcul. El lot gràfic de Viewshed repeteix l'algorisme individual; la màscara, la suma i la ponderació són operacions posteriors.

## B3. Quina part del recorregut veu T?

Mostreja la conca de T als punts C. Amb MDT, **34 de 37** donen 1: uns **3.356,14 m** de recorregut representat. Consulta aquests fitxers:

- Capa de resultats: `resultats/carretera-torxa.gpkg`.
- Taula de control: `controls/carretera.csv`.

Amb MDS apareix un problema de representació: en **9 posicions**, la cota dels ulls quedaria sota la superfície opaca. Es conserven com a **no calculades**; no es mouen automàticament els ulls damunt dels obstacles. Les altres **28 posicions** representen **2.763,88 m**, el **75,68%** del recorregut.

Després de mostrejar la conca MDS amb prefix `T_mds_`, aplica també la validesa de cada observador. Crea el camp `T_mds` amb la Calculadora de camps:

```text
CASE WHEN "calculable" = 1 THEN "T_mds_1" ELSE NULL END
```

La màscara ràster controla la cobertura del territori; aquest camp controla la compatibilitat de la posició de l'observador. Un zero retornat sota una coberta no s'utilitza com una observació comparable del recorregut.

En aquest subconjunt hi ha **7 mostres amb visió de T** i **21 ocultes**. Les set representen **690,97 m**, el **25% del recorregut comparable**. No és el 25% de tota la carretera. Per comparar MDT/MDS en igualtat de mostres, els fitxers `carretera-mdt-nombre.tif` i `carretera-mds-nombre.tif` utilitzen només aquestes 28 posicions.

**Conserva:** mostres, suma de 37 conques, percentatge i una taula de cobertura. Explica la diferència entre territori visible des de la carretera i longitud de carretera des d'on es veu T.

\clearpage

# C. Finalment, des d'on es veu el polígon?

## C1. De la coberta industrial al recinte petroquímic

La font és el polígon **1459998** del **Mapa de cobertes del sòl de Catalunya 2024**, categoria **347**, «Zones industrials, comercials i/o de serveis». Té **162,59 ha**, 19 forats i entrants que separen peces industrials. Un **tancament morfològic** permet delimitar un recinte més compacte: primer un buffer positiu i després un de negatiu de la mateixa magnitud, aplicat al resultat anterior.

1. Obre `09-perimetre.qgz` i identifica **Coberta original MCSC** i **Recinte petroquímic d'estudi**.
2. Obre **Vectorial → Geoprocessing Tools → Àrea d'influència…**, o localitza **Àrea d'influència**, `native:buffer`, a **Geometria vectorial** dins de la caixa de Processament.
3. Primera entrada: `dades/coberta-original.gpkg`. Distància **+150 m**, **32 segments per quadrant**, estils arrodonits i **dissolució activada**. Desa `treball/buffer-positiu.gpkg`.
4. Segona entrada: **el buffer positiu anterior**. Distància **−150 m**, mateixos altres paràmetres. Desa `treball/recinte.gpkg` i posa el nom **Recinte petroquímic d'estudi**.
5. Comprova una geometria vàlida, **222,94 ha** i cap forat. Compara-la amb l'ortofoto. El tancament incorpora també espais dels entrants: no conserva exactament l'exterior original.

![Menú Vectorial i submenú de geoprocessament desplegats. El requadre marca Àrea d'influència.](captures/visibilitat-acces-menu-buffer.png){width=100%}

![Àrea d'influència també és accessible des de la caixa de Processament.](captures/visibilitat-acces-caixa-buffer.png){width=90%}

![Primera operació: +150 m sobre la coberta original, amb 32 segments per quadrant i dissolució.](captures/visibilitat-costa-buffer-positiu.png){width=94%}

![Segona operació: −150 m sobre Buffer intermedi +150 m. La capa d'entrada és el resultat de la primera operació.](captures/visibilitat-costa-perimetre.png){width=94%}

La distància controla l'escala dels espais que es poden tancar. Un pas estret, d'amplada aproximadament inferior a dues vegades la distància, pot desaparèixer durant l'expansió; la forma també hi intervé. Les dues operacions no es cancel·len necessàriament. Compara aquestes alternatives, totes amb 32 segments:

| Mètode | Àrea, ha | Forats | Afegit exterior, ha |
| --- | ---: | ---: | ---: |
| Original | 162,59 | 19 | 0 |
| Buffers +50/−50 m | 181,33 | 5 | 4,85 |
| Buffers +100/−100 m | 199,97 | 2 | 15,52 |
| Buffers +150/−150 m | 222,94 | 0 | 38,50 |
| Buffers +250/−250 m | 224,49 | 0 | 40,04 |

![La comparació manté escala i contorn de referència. El tancament de 150 m produeix el recinte compacte utilitzat en l'exercici.](figures/visibilitat-perimetre.svg){width=100%}

El resultat escollit és una delimitació generalitzada d'estudi, no un nou límit oficial del Polígon Sud. Afegeix 38,50 ha fora del contorn original; l'aproximació dels arcs retira també uns 3,77 m² de la font en punts de vora. Es conserven la coberta original, el buffer positiu i les alternatives per revisar la decisió. El mostreig següent utilitza **el recinte de 222,94 ha**.

## C2. Preparar les mostres d'àrea

1. Executa **Crea una graella**, `native:creategrid`: rectangles poligonals, **250 × 250 m**, sense superposició.
2. Extensió: X **345250–350000**, Y **4551750–4552750**, EPSG:25831.
3. Retalla amb `dades/poligon.gpkg`, mitjançant `native:clip`.
4. Calcula `$area` amb el·lipsoide NONE i conserva un identificador.
5. Executa `native:pointonsurface`: un punt per fragment, no un per cada part multipart.

![La graella es retalla amb el recinte abans d'obtenir les mostres i els pesos.](captures/visibilitat-costa-area.png){width=90%}

El control és **57 fragments**, amb suma **2.229.408,741960 m²**. Les posicions i els pesos corresponen al recinte generalitzat, inclosos els espais incorporats. Els punts preparats es representen als centres de cel·la; les coordenades originals i els desplaçaments, de com a màxim 3,54 m, queden als atributs.

![T identifica una estructura singular; C mostreja el recorregut i A representa fragments d'àrea industrial.](figures/visibilitat-mostreig.svg){width=100%}

Cada A és **1 m sobre l'MDS local**. Per calcular amb MDT es manté la mateixa cota absoluta: utilitza `h_mdt_m`, que varia segons la mostra. Per MDS, utilitza `h_mds_m`; conserva els receptors a MDT + 1,7 m amb cota mínima i Domini, com a l'apartat A4.

Són **57 execucions per model**, seguides de la comparació de cotes, màscara i acumulació. Amb el guió carregat a la consola com a B2, la cadena completa es repeteix amb:

```python
calcula_lot(p, 'area', 'mdt')
calcula_lot(p, 'area', 'mds')
```

Es creen `treball/lot-area-mdt` i `treball/lot-area-mds`. Cada carpeta conté els 57 binaris, els intermedis, el recompte, el percentatge ponderat i `alguna-part.tif`, que incorpora la conca T del paquet. `lot.json` permet consultar les coordenades, altures i pesos aplicats. Per a carretera amb MDS, `calcula_lot(p, 'carretera', 'mds')` calcula només les 28 posicions compatibles; compara-les amb el resultat MDT preparat de 28, no amb la suma de 37.

## C3. Unir els objectius sense perdre la torxa

La suma de les 57 respostes A dona el nombre de mostres visibles. La graella pot haver passat per alt una estructura estreta: **afegeix T com a objectiu singular** a la pregunta «alguna part visible».

Carrega el recompte A amb nom **Nombre A** i la conca de T amb nom **Torxa T**, de la mateixa superfície. A Calculadora ràster:

```text
("Nombre A@1" > 0) OR ("Torxa T@1" = 1)
```

Conserva la graella i NoData. El resultat MDS de referència és `resultats/poligon-mds-alguna.tif`: **470.444 cel·les visibles**, el **13,48%** del domini. Amb MDT són **2.977.704**, el **85,31%**.

![El mapa final inclou qualsevol de les 57 mostres d'àrea o la torxa T. Tota la conca de T queda inclosa.](captures/visibilitat-costa-poligon.png){width=100%}

La fracció ponderada A respon una altra pregunta: $100\sum_i w_iV_i/\sum_i w_i$, amb pesos en m² dels 57 fragments. La torxa singular **no rep un pes superficial inventat**. Els mapes ponderats estan disponibles com `area-mdt-percent.tif` i `area-mds-percent.tif`.

![T i G són respostes binàries. C compara les mateixes 28 posicions, mentre que l'exercici inicial MDT utilitza 37. Blanc significa no calculat.](figures/visibilitat-mdt-mds.svg){width=100%}

\clearpage

## C4. Interpretar el resum als receptors

Mostreja les sortides als receptors i compara-les amb `resultats/receptors-resultats.gpkg`. Mantén prefixos amb significat i unitats: T i G són binaris; A és percentatge de superfície representada.

![Amb MDS, R1 veu T i algun element industrial, encara que cap de les 57 mostres A sigui visible. R5 queda nul.](figures/visibilitat-matriu-real.svg){width=100%}

**Conserva:** fragments, mostres, pesos, mapa d'alguna part visible i percentatge ponderat. Explica R1 amb **T=1, G=1, A=0%** i per què aquesta combinació justifica afegir estructures destacades al mostreig regular.

\clearpage

# Fonts i comprovació final

- Farnós Marsal, J.(2025). [La indústria petroquímica de Tarragona. Situació i transformacions](https://publicacions.iec.cat/repository/pdf/00000528/00000061.pdf). *Catalan Social Sciences Review*,15,107–110: polígons Nord/Sud, port i conduccions.
- [Jordi Rosell, Enciclopèdia.cat](https://www.enciclopedia.cat/tecnics-i-tecnologia-en-el-desenvolupament-de-la-catalunya-contemporania/el-complex-petroquimic-de), [història de Repsol](https://tarragona.repsol.es/ca/sobre-complejo/nuestra-historia/index.cshtml) i [Museu del Port](https://visitmuseum.gencat.cat/ca/museu/museu-del-port-de-tarragona/objecte/la-petroquimica): cronologia i relació entre indústria i transport marítim.
- [ICGC, models d'elevacions](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions/Elevacions-territorial/Models-delevacions): LiDAR 2021–2023; MDT natiu 5 m i MDS natiu 1 m, amb derivació màxima documentada.
- [ICGC, Mapa de cobertes del sòl](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya): edició 2024 i categoria 347.
- [ICGC, Referencial Topogràfic Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial): eixos de carretera i mar, edició 2024. Ortofoto ICGC 2025.
- [Col·laboradors d'OpenStreetMap](https://www.openstreetmap.org/copyright): node de torxa 7682543312, versió 1. La cartografia col·laborativa es contrasta amb l'ortofoto; no acredita per si sola l'altura.
- [QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/) i [GDAL Viewshed](https://gdal.org/en/stable/programs/gdal_viewshed.html): eines i significat dels paràmetres.

Les URLs, edicions, derivacions i hashes són a `fonts/fonts.json`; els controls, a `controls`. Les condicions ICGC són a [icgc.cat/condicions](https://www.icgc.cat/condicions). Les dades i els projectes del paquet són locals: comprova que obren des d'una altra ubicació, sense serveis en línia.

La conclusió ha d'identificar **què es veu, des d'on, amb quines altures, quina superfície i quina cobertura de dades**. Afegeix una observació o dada que encara necessitaries per estudiar percepció o impacte paisatgístic.
