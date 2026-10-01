---
title: "Pràctica: distàncies i recorreguts a Vila-seca"
author: Benito Zaragozí
lang: ca
date: "Preparació: 1 d'octubre de 2026"
content_status: draft
---

# Quatre maneres d'arribar al mateix lloc

Dos punts propers poden quedar separats per una autopista. En aquesta pràctica compararàs la seva separació en línia recta, la distància calculada amb cel·les, una ruta per la xarxa i un camí sobre una superfície de cost. Mantindràs els mateixos punts O i D per entendre què canvia en cada model.

El lloc és l'entorn del **Camí del Mas de la Plana, al pas de l'AP-7 per Vila-seca**. El pas P2 està representat a la cartografia de l'ICGC i es reconeix a l'ortofoto. Simularem el seu tancament i la seva reobertura en les dades. Les velocitats, les friccions i l'amplada del corredor de pas són supòsits de l'exercici.

**Objectius:** calcular distàncies en metres; distingir punts vectorials i centres de cel·la; interpretar una ruta i una àrea de servei; separar fricció, cost acumulat i recorregut; comparar temps d'anada i tornada i llegir isòcrones.

Els blocs **A–B** són el nucli de distàncies euclidianes. **C–D** afegeixen xarxa i cost; **E–F**, marxa amb relleu i isòcrones. Es poden reprendre amb els projectes preparats.

## Abans de començar

1. Utilitza **QGIS 3.44**, amb la Caixa d'eines de processament i els proveïdors **GDAL i GRASS**. Els càlculs del paquet s'han comprovat amb QGIS 3.44.11, GDAL 3.10.3 i GRASS 8.4.1.
2. Descomprimeix tot el paquet. Conserva les carpetes juntes: els projectes utilitzen rutes relatives.
3. Obre `projectes/00-inici.qgz`. Crea una carpeta `treball` al costat de `dades` i desa-hi una còpia del projecte.
4. Comprova **ETRS89 / UTM zona 31N, EPSG:25831**, i el·lipsoide **Cap / NONE** a les propietats del projecte. Les coordenades i els càlculs plans s'expressen en metres.
5. Desa les teves sortides a `treball`. La carpeta `resultats` conté càlculs de referència; serveix per contrastar-los, no per substituir la feina.

Els projectes `01-dades` a `09-pineda-cost` són vistes preparades per inspeccionar cada etapa. Les captures poden abreujar algun nom de capa; els fitxers de les taules següents permeten identificar-la sense dubtes.

L'ampliació afegeix `10-marxa`, `11-marxa-relleu`, `12-isocrones-obert`, `13-isocrones-tancat` i `14-franges-xarxa`. Tots són a `projectes` i tenen extensió `.qgz`.

| Carpeta | Què conté |
| --- | --- |
| `fonts` | Ortofoto, MDT, extracte original d'eixos i edificis, amb procedència |
| `dades` | O, D, xarxes de treball, barreres, passos i ràsters d'entrada |
| `resultats` | Sortides comprovades per comparar amb les pròpies |
| `projectes` | Projectes QGIS amb estils i vistes preparades |
| `captures` | Imatges de QGIS per seguir els procediments |
| `controls` | Paràmetres, valors de comprovació i inventari de capes |

## Reconèixer el lloc i les dades

Activa l'ortofoto, la xarxa i els punts. Busca l'origen **O**, la destinació **D** i el pas **P2**. La línia de l'AP-7 i el camí que la creua a diferent nivell no són una cruïlla on es pugui girar de l'un a l'altra.

| Element | Fitxer | Significat |
| --- | --- | --- |
| O | `dades/origen.gpkg` | Punt de partida sobre un extrem d'eix cartografiat |
| D | `dades/desti.gpkg` | Punt d'arribada al Camí del Mas de la Plana |
| Xarxa oberta | `dades/xarxa-oberta.gpkg` | Eixos de treball, amb el pas P2 disponible |
| Xarxa tancada | `dades/xarxa-tancada.gpkg` | La mateixa xarxa sense el tram del pas P2 |
| Pas P2 | `dades/pas-p2.gpkg` | Corredor de pas representat al model ràster |
| Fricció | `dades/friccio-obert.tif` i `friccio-tancat.tif` | Dificultat relativa de cada cel·la |

Les coordenades dels punts, en metres, són:

| Punt | Est, X | Nord, Y |
| --- | ---: | ---: |
| O | 344407,00 | 4553668,36 |
| D | 344473,01 | 4554030,72 |

![O és al costat sud del pas i D és al camí del costat nord. El requadre identifica P2, la connexió que es modifica en el model.](captures/distancies-dades.png){width=100%}

**Comprovació inicial.** No comencis a calcular fins que puguis assenyalar O i D al mapa i explicar quina barrera els separa. Els punts són localitzacions de l'exercici, no centres municipals.

# A. Distància euclidiana vectorial

La pregunta és: **quina longitud té el segment recte entre O i D?** Aquesta mesura no considera l'autopista, els edificis ni els camins.

1. A la Caixa d'eines, cerca **Shortest line between features**, identificador `native:shortestline`.
2. A **Source layer**, tria **Origen O**; a **Destination layer**, **Destí D**.
3. Mantén **Distance to Nearest Point on feature** i **1** veí. Amb un punt a cada capa, això uneix O amb D.
4. Deixa buida la distància màxima i desa la sortida com `treball/recta.gpkg`.
5. Obre la taula del resultat i consulta el camp de distància. Compara també la línia amb l'ortofoto.

![El diàleg de línia més curta utilitza Origen O com a capa de partida i Destí D com a capa d'arribada.](captures/distancies-vector-parametres.png){width=75%}

La comprovació manual utilitza les diferències de coordenades:

$$d=\sqrt{66,01^2+362,36^2}\simeq368,3\ \mathrm{m}.$$

![El segment discontinu uneix O i D en 368,3 m, encara que travessi espais on el moviment podria no estar permès.](captures/distancies-vector-resultat.png){width=100%}

**Conserva:** la línia, la distància en metres i una frase que expliqui per què això no és encara una ruta. Canviaria aquesta distància si es tanqués P2?

# B. Distància euclidiana ràster

Ara la pregunta es fa per a totes les cel·les: **a quina distància queda cada centre de cel·la de la cel·la que conté O?** La graella comuna té cel·les de **5 × 5 m**.

## Convertir O en una cel·la

1. Cerca **Rasteritza — vectorial a ràster**, `gdal:rasterize`.
2. Entrada: **Origen O**. Valor fix a gravar: **1**. No seleccionis cap camp d'atributs.
3. Unitats de mida de sortida: **unitats georeferenciades**; amplada i alçada de cel·la: **5 m**.
4. Utilitza l'extensió de `dades/ambit.gpkg` o introdueix els límits de la taula.
5. A les opcions avançades, valor inicial del fons **0** i tipus de dada **Byte**. Deixa sense definir el NoData: aquí zero és el fons vàlid.
6. Desa `treball/origen-5m.tif`.

| Límit | Valor en EPSG:25831 |
| --- | ---: |
| X mínim | 343600 |
| X màxim | 345300 |
| Y mínim | 4553000 |
| Y màxim | 4554700 |
| Dimensions | 340 columnes × 340 files |

**Comprova** que només una cel·la té valor 1. El paquet inclou `dades/origen-5m.tif` per comparar la georeferenciació. Si totes les cel·les fossin 1, totes serien orígens de distància.

## Calcular la proximitat

1. Cerca **Proximitat — distància ràster**, `gdal:proximity`.
2. Entrada: el ràster d'origen; banda **1**; llista de píxels objectiu: **1**.
3. Unitats de distància: **coordenades georeferenciades**. En aquest CRS són metres. No deixis l'opció de distància en píxels.
4. Mantén la distància màxima a **0**, que en aquesta eina deixa el càlcul sense aquest límit. Tipus de sortida: **Float32**; NoData de sortida: **−9999**.
5. Desa `treball/distancia.tif`. Representa'l amb pseudocolor i una llegenda en metres.
6. Per consultar D amb precisió, executa **Sample raster values / Mostreja valors ràster**, `native:rastersampling`, amb **Destí D** i el teu ràster. Desa la capa de punts amb el valor mostrejat.

![El valor 1 identifica la cel·la origen. L'opció de coordenades georeferenciades fa que la sortida sigui en metres, no en nombre de píxels.](captures/distancies-raster-parametres.png){width=75%}

![La distància augmenta des de la cel·la d'O en totes les direccions. A la cel·la de D s'obtenen aproximadament 370,7 m. L'autopista no altera aquesta distància recta.](captures/distancies-raster-resultat.png){width=100%}

El resultat no ha de coincidir exactament amb els 368,3 m vectorials. O i D passen a representar-se mitjançant els centres de les seves cel·les:

| Centre de cel·la | X, m | Y, m |
| --- | ---: | ---: |
| Cel·la d'O | 344407,5 | 4553667,5 |
| Cel·la de D | 344472,5 | 4554032,5 |

**Conserva:** el ràster 0/1, el de distància, el valor mostrejat a D i una explicació de la diferència de 2,4 m respecte del vector. El ràster no està calculant una volta pels camins.

# C. Ruta per la xarxa i àrees de servei

## Seguir els eixos connectats

1. Activa **Xarxa · pas obert**. Cerca **Camí més curt — punt a punt**, `native:shortestpathpointtopoint`.
2. Capa de xarxa: `dades/xarxa-oberta.gpkg`. Criteri: **Més curt**.
3. Copia les coordenades exactes de les dues línies següents. En aquest camp s'utilitza punt decimal i una coma per separar X de Y; seleccionar a ull al mapa pot desplaçar el punt fora de l'eix.
4. A les opcions avançades, direcció per defecte **ambdós sentits**, tolerància topològica **0 m** i distància màxima del punt a la xarxa **0,1 m**.
5. Desa `treball/ruta-oberta.gpkg`. Mesura'n la longitud i compara-la amb la recta.

```text
O: 344407.00,4553668.36 [EPSG:25831]
D: 344473.01,4554030.72 [EPSG:25831]
```

Copia la cadena després de `O:` o `D:`, sense aquesta etiqueta.

![L'origen i la destinació s'introdueixen explícitament. El criteri Més curt minimitza la longitud dels trams de la xarxa.](captures/distancies-xarxa-parametres.png){width=75%}

![La ruta blava segueix els eixos i passa per P2: fa aproximadament 454,1 m. La recta discontínua fa 368,3 m. O i D són els mateixos en tots dos càlculs.](captures/distancies-xarxa-resultat.png){width=100%}

Repeteix el càlcul amb `dades/xarxa-tancada.gpkg`. S'ha retirat el tram de pas amb `rtt_id = 1354754`. El resultat de control és **sense ruta**.

**Què significa sense ruta?** En aquesta selecció cartogràfica, O queda en un tram sense cap altra connexió amb D. No s'ha de substituir l'absència de ruta per zero metres. L'ortofoto pot mostrar vials que no formen part de la xarxa: el resultat descriu el graf preparat, no tota la mobilitat possible al territori.

## Passar de metres a minuts

El camp `v_kmh` conté **5 km/h** a tots els trams: és una velocitat uniforme escollida per a l'exercici. Amb **Més ràpid**, selecciona aquest camp de velocitat. La ruta oberta dona aproximadament **0,09082 hores**, és a dir, **5,45 minuts**. No llegeixis el cost en hores com si fossin minuts.

## Què passa amb els girs?

La direcció d'un arc i una restricció de gir són coses diferents. En aquest exemple fictici, a→b està prohibit però c→b està permès. Tancar b eliminaria també la maniobra permesa.

![La regla depèn del tram d'arribada. El carrer de sortida continua obert.](figures/restriccions-gir.svg){width=85%}

Les eines natives de rutes de **QGIS 3.44** utilitzades aquí admeten sentits i velocitats, però no una taula de maniobres. El camp `sentit` no representa un gir prohibit i afegir una columna anomenada `gir` no faria que l'eina l'apliqués.

![Més ràpid minimitza el temps segons els sentits i les velocitats configurats. Aquesta eina nativa no incorpora una taula de restriccions de gir.](captures/xarxa-girs-parametres.png){width=70%}

**Conserva:** un esquema que distingeixi prohibició de maniobra, sentit únic i tancament de carrer. Si un projecte requerís restriccions o temps d'espera als girs, necessitaria un motor i unes dades que els representessin explícitament.

## Quins trams s'assoleixen abans d'un temps límit?

1. Cerca **Àrea de servei — des d'un punt**, `native:serviceareafrompoint`.
2. Entrada: xarxa oberta; criteri **Més ràpid**; origen O; camp de velocitat `v_kmh`; ambdós sentits.
3. El camp **Travel cost** d'aquesta versió de QGIS espera **hores**. Calcula tres sortides:

| Temps que es vol representar | Valor a introduir |
| --- | ---: |
| 3 minuts | 0,05 hores |
| 6 minuts | 0,10 hores |
| 12 minuts | 0,20 hores |

En els camps de les captures s'utilitza punt decimal: `0.05`, `0.10` i `0.20`.

4. Desa les **sortides en línies** i assigna'ls colors diferents. Posa les de temps curt damunt de les de temps llarg perquè es vegin totes.
5. Compara la franja de 6 minuts amb la que s'obté amb el pas tancat.

![Per obtenir dotze minuts s'introdueixen 0,20 hores, amb el criteri Més ràpid i la velocitat de l'exercici.](captures/distancies-isocrones-parametres.png){width=75%}

![Blau, verd i taronja mostren els trams accessibles en 3, 6 i 12 minuts amb el pas obert. El tram vermell mostra l'abast amb P2 tancat. Les línies no omplen els camps ni impliquen que qualsevol lloc entre carreteres sigui accessible.](captures/distancies-isocrones-resultat.png){width=100%}

![Mapes amb els mateixos colors i extensió. Amb el pas tancat, augmentar el límit temporal no permet sortir del component connectat a O.](figures/isocrones-xarxa.svg){width=90%}

El projecte `14-franges-xarxa.qgz` conté les porcions disjuntes de línia. Un polígon que les embolcalli o un buffer al voltant de les carreteres no acredita accessibilitat a tota la superfície interior.

**Conserva:** les rutes, el resultat sense ruta, les tres àrees de servei i un mapa amb O, D, P2 i llegenda. D és accessible en 3 minuts? I en 6? La suma de la longitud de totes les branques no és el recorregut d'una sola persona.

# D. Una superfície de cost

Una xarxa només permet seguir els seus arcs. Un ràster pot permetre passar per altres cel·les, amb una dificultat diferent. En aquest model la fricció val **1 als camins** i **4 a la resta del terreny admès**. Els edificis i la banda de l'autopista són **NoData**, exclosos del pas, excepte els corredors oberts sota o sobre la infraestructura.

La banda de l'AP-7 s'ha construït amb un buffer de 25 m dels seus eixos; els corredors de pas tenen 20 m d'amplada al model. Són simplificacions declarades, no mesures de la plataforma ni de la capacitat dels passos. El ràster permet travessar terreny fora dels eixos amb cost 4; per això pot donar un camí quan la xarxa seleccionada no en dona.

## Llegir la fricció abans de calcular

Obre `projectes/06-friccio.qgz` o activa els dos ràsters de fricció del projecte. Alterna `friccio-tancat.tif` i `friccio-obert.tif` i consulta algunes cel·les amb **Identifica els objectes**.

| Lloc | Fricció | Què implica |
| --- | ---: | --- |
| Camí admès | 1 | Pas relativament fàcil |
| Resta del terreny admès | 4 | El mateix pas costa quatre vegades més |
| Autopista fora dels passos i edificis | NoData | Cel·la exclosa del càlcul |
| Corredor P2 | NoData o 1 | Canvia entre l'escenari tancat i l'obert |

![La fricció és visible com un ràster de valors 1 i 4. Les cel·les excloses deixen veure la banda grisa de l'autopista i els edificis. El requadre marca P2 tancat.](captures/distancies-friccio.png){width=100%}

**L'MDT no és aquesta fricció.** L'MDT guarda altituds en metres; la fricció guarda resistències relatives. En el model principal no s'hi sumen elevacions. El paquet conserva l'MDT i el pendent per a una ampliació diferenciada.

## Del cost local al cost acumulat amb r.cost

1. A la Calculadora ràster, multiplica la banda de la fricció oberta per **5**, perquè cada cel·la fa 5 m de costat. Per exemple, seleccionant la banda de la llista: `"Fricció · pas obert@1" * 5`.
2. Conserva l'extensió de la graella comuna i **340 × 340** cel·les. Desa `treball/cost-cella-obert.tif`.
3. Comprova valors **5** als camins i **20** a la resta admesa. Els NoData s'han de conservar. El paquet inclou el mateix resultat a `dades/cost-cella-obert.tif`.
4. Obre **r.cost**, identificador `grass:r.cost`. Entrada: cost per cel·la; punts d'inici: **Origen O**.
5. Deixa buides les altres maneres de donar punts d'inici i els punts d'aturada. No assignis cost als nuls: han de continuar exclosos.
6. No activis el moviment de cavall (*Knight's move*); aquí es treballa amb vuit veïns. Mantén l'opció de conservar els nuls.
7. A les opcions de regió GRASS, fixa l'extensió comuna i la mida de cel·la a **5 m**.
8. Desa dues sortides: **cost acumulat** i **direccions de moviment**, per exemple `treball/cost-obert.tif` i `treball/direccions-obert.tif`.

![r.cost rep el cost de travessar una cel·la i comença a O. Els punts d'aturada queden buits per calcular tota la superfície accessible.](captures/distancies-cost-parametres.png){width=75%}

El cost acumulat d'una cel·la és el menor cost d'arribar-hi des d'O. En aquesta pràctica s'expressa en **metres ponderats**. No són minuts: els pesos 1 i 4 no provenen d'un model de velocitat.

## Reconstruir el camí amb r.path

1. Obre **r.path**, `grass:r.path`.
2. A **Name of input direction**, selecciona el ràster de **direccions** de r.cost, no el de cost acumulat. Format: **degree**.
3. A **Start points**, tria **Destí D**. En aquesta eina es comença al final del recorregut i se segueixen les direccions de retorn cap a O.
4. Conserva la mateixa regió i cel·la de 5 m. Desa la sortida vectorial com `treball/ruta-cost-obert.gpkg` i, si es vol, el camí en ràster.
5. Repeteix la cadena amb la fricció tancada, canviant els noms de totes les sortides per poder comparar-les.

![A r.path es tria D com a punt de partida de la reconstrucció. Les direccions guardades per r.cost indiquen com tornar cap a O.](captures/distancies-path-parametres.png){width=75%}

![El camí blau utilitza P2 obert. El taronja correspon al model amb P2 tancat i passa per un altre corredor. El fons és el cost acumulat de l'escenari obert, no un MDT.](captures/distancies-cost-resultat.png){width=100%}

| Resultat a D | P2 obert | P2 tancat |
| --- | ---: | ---: |
| Longitud del camí ràster | 470,6 m | 1.135,8 m |
| Cost acumulat | 470,6 m ponderats | 2.217,7 m ponderats |

**Interpreta la diferència.** Amb el pas obert, el camí segueix cel·les de fricció 1 i longitud i cost coincideixen numèricament. Amb el pas tancat es travessen també cel·les més cares. No comparis 2.217,7 metres ponderats amb minuts ni amb una distància euclidiana com si fossin la mateixa magnitud.

**Conserva:** les dues friccions, costos per cel·la, costos acumulats, direccions i camins; una taula amb longitud, cost i unitats; i un mapa on es distingeixin O, D, la barrera i els passos.

# E. Pujar i baixar amb r.walk

Ara s'estima **temps de marxa**, incorporant el desnivell entre cel·les. Obre `projectes/10-marxa.qgz`; `11-marxa-relleu.qgz` mostra el mateix lloc sobre l'MDT. Es mantenen els O/D i les barreres del cas anterior.

## Entendre l'anisotropia

En un perfil construït de 100 m horitzontals i 10 m de pujada, els coeficients per defecte donen 132 s. Baixar pel mateix perfil costa uns 52 s. El cost depèn del sentit: és **anisòtrop**. L'exemple no afirma que baixar qualsevol pendent sigui favorable; per a baixades fortes el model torna a afegir cost.

![El mateix perfil, sense fricció addicional, dona temps diferents en pujar i baixar. L'escala vertical del dibuix està exagerada.](figures/anisotropia-pendent.svg){width=85%}

## Preparar les entrades

| Entrada | Fitxer | Unitat o regla |
| --- | --- | --- |
| Altitud | `fonts/mdt-5m.tif` | Metres d'altitud; no graus de pendent |
| Fricció oberta | `dades/friccio-marxa-obert.tif` | 0 s/m als camins, 0,5 s/m a la resta |
| Fricció tancada | `dades/friccio-marxa-tancat.tif` | Mateixes unitats, P2 exclòs |
| Control pla | `dades/mdt-pla-control.tif` | Altitud constant zero |

Pots reconstruir la fricció temporal a la Calculadora ràster a partir de la fricció 1/4: assigna **0** on val 1 i **0,5** on val 4, conservant NoData. Per exemple, seleccionant la banda corresponent:

```text
if("Fricció · pas obert@1" = 1, 0, 0.5)
```

**Comprova** els valors i les barreres abans de continuar. Aquí zero vol dir sense penalització addicional; r.walk encara calcula el temps de desplaçament. No reutilitzis els pesos 1/4 com si fossin segons i **no multipliquis aquesta fricció temporal per 5**.

## Calcular el temps des d'O

1. Cerca **r.walk.points**, `grass:r.walk.points`.
2. Elevació: MDT de 5 m. Fricció: `friccio-marxa-obert.tif`. Punts d'inici: **Origen O**.
3. Deixa buits els punts d'aturada i el cost dels nuls. Mantén els nuls exclosos i desactiva el moviment de cavall.
4. Conserva els coeficients `0.72,6.0,1.9998,-1.9998`, **lambda 1** i **slope factor −0,2125**. El llindar és en m/m, no en graus.
5. Fixa la regió comuna i la cel·la a **5 m**.
6. Desa **temps acumulat en segons** i **direccions**, per exemple `treball/marxa-O-segons.tif` i `treball/marxa-O-direccions.tif`.
7. Divideix el temps per **60** amb la Calculadora ràster, conservant extensió, resolució i NoData. Desa `treball/marxa-O-minuts.tif`.
8. Mostreja D amb `native:rastersampling`. Control: **397,83 s = 6,63 min**.

![r.walk rep dues entrades diferents: MDT en metres i penalització temporal en segons per metre.](captures/rwalk-parametres.png){width=70%}

## Reconstruir els dos sentits

1. Executa **r.path** amb les direccions iniciades a O, format **degree** i **D** com a punt de reconstrucció.
2. Torna a executar r.walk des de **D**, amb les mateixes entrades. Desa sortides amb noms nous.
3. Reconstrueix la tornada amb aquestes direccions i **O** com a punt de r.path.
4. Compara el temps des de D mostrejat a O: **389,01 s = 6,48 min**.

![El fons és el temps des d'O. Les dues rutes són semblants, però els temps d'anada i tornada provenen de càlculs separats.](captures/rwalk-resultat.png){width=100%}

**No n'hi ha prou amb invertir la línia:** cal recalcular amb l'altre origen. Per a un control isòtrop, repeteix els dos càlculs amb `mdt-pla-control.tif`. S'han d'obtenir **338,37 s = 5,64 min** en tots dos sentits.

| Model | O→D | D→O |
| --- | ---: | ---: |
| Pla, P2 obert | 5,64 min | 5,64 min |
| MDT, P2 obert | 6,63 min | 6,48 min |
| MDT, P2 tancat | 17,49 min | No calculat com a referència |

**Conserva:** els dos orígens de càlcul, segons, minuts, direccions, rutes i taula de temps. Les cotes d'O/D són 50,887 i 52,249 m, però r.walk utilitza també els desnivells intermedis.

El MDT pot simplificar el perfil d'un pas sota l'autopista. Els corredors i els temps són els del model docent, sense calibració amb caminades observades.

# F. Isòcrones de 3, 6 i 12 minuts

Una isòcrona uneix llocs amb el mateix temps mínim d'accés. Les franges acolorides ajuden a respondre si es pot arribar a D dins d'un límit temporal.

## Crear contorns i franges

1. Entrada: el ràster **en minuts** des d'O. No seleccionis per error el de segons ni el cost ponderat de r.cost.
2. Cerca **r.contour**, `grass:r.contour`. Llista de nivells: **3,6,12**. Deixa sense definir l'increment regular.
3. Mínim de punts per línia: **3**. Això evita contorns degenerats molt petits; no modifica els valors de temps.
4. Regió comuna i cel·la de **5 m**. Desa els contorns com `treball/isocrones-obert.gpkg`.

![Els contorns prenen les unitats de l'entrada: 3,6,12 amb minuts o 180,360,720 amb segons.](captures/rwalk-contorns.png){width=70%}

Per acolorir franges, classifica la banda temporal amb la Calculadora ràster. Selecciona el nom de la teva banda i aplica:

```text
if("Temps des d’O · minuts@1" <= 3, 1,
   if("Temps des d’O · minuts@1" <= 6, 2,
      if("Temps des d’O · minuts@1" <= 12, 3, 4)))
```

Mantén **340 × 340** cel·les, extensió comuna i NoData. Assigna colors discrets:

| Classe | Temps | Color |
| --- | --- | --- |
| 1 | 0–3 min | Blau |
| 2 | Més de 3–6 min | Verd |
| 3 | Més de 6–12 min | Taronja |
| 4 | Més de 12 min | Gris clar |
| NoData | Barrera | Transparent o gris diferenciat |

Repeteix la cadena amb la fricció temporal tancada, mantenint l'MDT i O. Utilitza els mateixos colors, límits i enquadrament als dos mapes. Les sortides de referència són `isocrones-marxa-obert.tif` i `isocrones-marxa-tancat.tif`; els vectors de contorns es diuen `isocrones-contorns-obert.gpkg` i `isocrones-contorns-tancat.gpkg`, dins de `resultats`.

![Amb P2 obert, D és entre 6 i 12 minuts.](captures/rwalk-isocrones-obert.png){width=100%}

![Amb P2 tancat, D costa 17,49 minuts i queda fora de les tres franges acolorides.](captures/rwalk-isocrones-tancat.png){width=100%}

![Comparació de les superfícies assolibles: 91,9 ha fins a 12 minuts amb P2 obert i 55,4 ha amb el pas tancat.](figures/isocrones-rwalk.svg){width=90%}

## Comprovar les superfícies

Compta les cel·les de les classes 1, 2 i 3 amb l'informe de valors únics del ràster, `native:rasterlayeruniquevaluesreport`. Cada cel·la fa **25 m²**. Suma els recomptes, multiplica per 25 i divideix per 10.000 per obtenir hectàrees.

| Límit acumulat | P2 obert, cel·les | P2 tancat, cel·les |
| --- | ---: | ---: |
| Fins a 3 min | 1.624 | 1.434 |
| Fins a 6 min | 7.481 | 4.764 |
| Fins a 12 min | 36.777 | 22.155 |

**Conserva:** dos mapes comparables, ràsters, contorns i taula de recomptes. Explica per què D era dins dels 6 minuts a la xarxa a velocitat constant i fora dels 6 al model de marxa amb MDT. Distingir barrera i més de 12 minuts és essencial: només la primera exclou el pas.

# Altres ampliacions i comprovació final

## La Pineda: penalitzar no és prohibir

Obre `projectes/08-pineda-friccio.qgz` i `09-pineda-cost.qgz`. En aquest cas hi ha fricció 1 a l'exterior i 20 dins d'una parcel·la cadastral. Són valors finits: es podria travessar si qualsevol altra alternativa fos més cara.

![A la Pineda, l'interior de la parcel·la val 20 i l'exterior 1. El camí discontinu correspon a cost uniforme; el blau evita les cel·les encarides.](captures/distancies-pineda-friccio.png){width=100%}

![El cost acumulat és baix prop d'O i augmenta en arribar a altres cel·les. A l'interior de la parcel·la augmenta ràpidament. Aquest relleu de colors és cost, no altitud.](captures/distancies-pineda-cost.png){width=100%}

Explica la diferència entre posar **20** a una cel·la i convertir-la en **NoData**. Comprova les longituds de referència: 608,3 m amb fricció uniforme i 724,3 m vorejant la parcel·la penalitzada.

## Incorporar pendent com a experiment nou

El fitxer `dades/pendent-graus.tif` deriva de l'MDT de 5 m. Es pot assajar una nova fricció, per exemple multiplicant la inicial per `1 + pendent / 10`. Cal explicar aquesta regla, mantenir les barreres i recalcular costos i camins. Els resultats anteriors no són els controls d'aquest model nou, i els costos continuen sense ser temps de marxa calibrats.

## Taula de síntesi

Completa una taula amb **pregunta, eina, entrada, sortida, unitat i resultat a D** per als models treballats. Afegeix aquestes conclusions:

- per què vector i ràster euclidians difereixen una mica;
- per què tancar P2 no canvia la distància recta però sí la connectivitat;
- per què fricció i cost acumulat són dues capes diferents.
- per què r.walk necessita recalcular la tornada;
- per què un buffer de la xarxa no substitueix una superfície d'isòcrones.

El projecte final ha de tornar-se a obrir amb totes les capes necessàries. Comprova-ho després de tancar QGIS i de moure una còpia de tota la carpeta de treball a una altra ubicació.

# Fonts i condicions del cas

- **ICGC:** Referencial Topogràfic Territorial 2024, ortofoto de Catalunya 2025 i MDT LiDAR 5 m de 2021–2023. L'ortofoto inclosa és una petició del servei WMS renderitzada a 1 m per píxel.
- **Dirección General del Catastro:** geometries d'edificis de Vila-seca i parcel·la de la Pineda. Les dates, fonts de les còpies i hashes es conserven a `fonts/fonts.json` i `controls/resultats.json`.
- Xarxa de treball retallada, sense eixos d'autopista, amb contactes extrem–interior explicitats. No s'han connectat arbitràriament totes les línies que es creuen. La cartografia no és una base completa de navegació.
- Les friccions, la velocitat de 5 km/h, les bandes i els corredors són decisions de model. Les captures mostren aquesta preparació docent, no una intervenció anunciada al territori.

Consulta els productors: [ICGC](https://www.icgc.cat/), [condicions d'ús ICGC](https://www.icgc.cat/condicions), [servei d'ortofoto](https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?SERVICE=WMS&REQUEST=GetCapabilities), [Cadastre INSPIRE](https://www.catastro.hacienda.gob.es/webinspire/index.html), [manual de QGIS](https://docs.qgis.org/3.44/en/docs/user_manual/), [anàlisi de xarxes de QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/networkanalysis.html), [r.cost](https://grass.osgeo.org/grass84/manuals/r.cost.html), [r.path](https://grass.osgeo.org/grass84/manuals/r.path.html), [r.walk](https://grass.osgeo.org/grass84/manuals/r.walk.html) i [r.contour](https://grass.osgeo.org/grass84/manuals/r.contour.html).
