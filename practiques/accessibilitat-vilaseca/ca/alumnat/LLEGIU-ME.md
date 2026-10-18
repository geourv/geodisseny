---
title: "Pràctica: accessibilitat de Vila-seca"
author: Benito Zaragozí
lang: ca
date: "Guia revisada: 14 d'octubre de 2026"
content_status: draft
---

# Distàncies, recorreguts i temps d'accés

Dos punts propers poden quedar separats per una autopista. Compararem la recta entre O i D, la distància entre cel·les, un itinerari per la xarxa i camins sobre superfícies de cost. Després incorporarem el relleu i delimitarem allò que s'assoleix en 3, 6 i 12 minuts. Mantindrem els mateixos punts per interpretar què canvia en cada model.

El cas és el **Camí del Mas de la Plana, al pas de l'AP-7 de Vila-seca**. P2 és el pas principal; els altres polígons identifiquen passos alternatius. Simularem el tancament i l'obertura de P2. Les velocitats, friccions i amplades dels corredors són decisions del model docent, no mesures de caminades ni una intervenció anunciada.

El recorregut es distribueix en tres subpràctiques: **xarxa vectorial**, **model ràster** i **temps d'accés i ampliacions**. Cadascuna té una lectura i un paquet propis. Aquest document reuneix els procediments i les fonts del cas complet.

La comparació principal relaciona **distància euclidiana, longitud del camí de menor cost en ràster i longitud de la ruta més curta en xarxa**. La proximitat ràster permet contrastar la representació amb cel·les. Per obtenir el camí de cost, cal construir la fricció, representar barreres i passos i distingir la longitud del recorregut del seu cost ponderat.

**El professor indicarà a classe quins apartats i exercicis són obligatoris dins del 70% de la qualificació**, i ho recollirà a la tasca de Moodle. La guia ofereix un recorregut complet, no una llista de passos que s'hagin de lliurar tots. En Vila-seca, les àrees de servei, la marxa anisòtropa i les isòcrones són propostes d'ampliació. També es pot desenvolupar una pregunta pròpia per aspirar a l'excel·lent, amb resultats justificats i sense substituir el treball obligatori.

# Preparar QGIS i obrir el GeoPackage

El lliurament d'inici té **dos fitxers**: `accessibilitat-vilaseca.gpkg` i aquest `LLEGIU-ME.pdf`. El GeoPackage conté les dades bàsiques, els estils i el projecte **inici**. Les sortides dels exercicis s'han de calcular.

Obre les eines des de **Procés → Caixa d'eines**. Escriu el nom o l'identificador indicat al cercador i fes doble clic a l'eina. Per desar una sortida vectorial, utilitza els **tres punts** del camp de sortida, tria **Desa en un fitxer…**, format **GeoPackage**, i introdueix un nom de capa nou. Per a un ràster, desa un **GeoTIFF `.tif`** a la carpeta `intermedis`.

1. Utilitza **QGIS 3.44**, amb els proveïdors **GDAL i GRASS** de la Caixa d'eines. A **Configuració → Opcions → Processament → Proveïdors**, comprova que GRASS està activat. Cerca `r.grow.distance`, `r.cost`, `r.path`, `r.walk.points` i `r.contour`; si no apareixen, revisa la instal·lació abans de començar. En instal·lacions gestionades d'aula, consulta l'administració.
2. Crea una carpeta pròpia i copia-hi el GeoPackage **conservant el nom del fitxer**. Treballa sobre aquesta còpia. Crea-hi també `intermedis` per als ràsters temporals.
3. Al panell **Explorador**, clic dret a **GeoPackage → Connexió nova**. Selecciona la teva còpia i desplega `accessibilitat-vilaseca.gpkg`.
4. Obre el projecte **inici**, amb la icona de QGIS, que apareix dins de la connexió. Si cal, utilitza **Projecte → Obre des de → GeoPackage** i selecciona el fitxer i aquell projecte.
5. A les propietats del projecte, comprova **EPSG:25831** i el·lipsoide **Cap / NONE**. Les coordenades i les longituds planes són en metres.
6. Desa el projecte de treball amb **Projecte → Desa a → GeoPackage**, a la teva còpia, amb un nom com **treball**. Els vectors resultants es poden desar al mateix GeoPackage amb noms de capa nous. Conserva els TIFF requerits pels mòduls GRASS a `intermedis`; el projecte ha de mantenir-ne les referències.

**Selecciona capes, no el fitxer complet.** En un diàleg de GRASS, tria la capa carregada **Origen O** o **Destí D**, o selecciona el node concret des de la connexió desplegada. El GeoPackage també conté el projecte, estils i taules. Indicar només el fitxer pot fer que l'importador intenti llegir totes les taules. Una capa vectorial identificada té una referència com `accessibilitat-vilaseca.gpkg|layername=origen`.

![La connexió GeoPackage desplegada permet distingir el projecte inici, les capes vectorials, els ràsters i la llegenda.](captures/inici.png){width=100% height=380pt}

## Dades bàsiques

| Capa o taula | Funció | Recurs i accés |
| --- | --- | --- |
| `origen`, `desti` | O i D, sobre nodes de la xarxa | Punts de l'exercici inclosos al GeoPackage |
| `xarxa` | Eixos RTT de Vila-seca i entorn preparats per al model a peu | [ICGC, Referencial Topogràfic Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial) |
| `municipi` | Límit oficial de Vila-seca, codi 431711 | [ICGC, divisions administratives](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives) |
| `cobertes` | Polígons MCSC2024: classe, categoria i data | [Mapa de cobertes ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya), [descàrrega per àrea](https://visors.icgc.cat/appdownloads/index.html?c=fmexomcsc) i [GeoPackage2024](https://datacloud.icgc.cat/datacloud/cobertes-sol/gpkg/cobertes-sol-v1r0-2024.zip) |
| `llegenda_costos` | Classes i pesos adoptats | Taula inclosa al GeoPackage; model de comparació de la pràctica |
| `autopista_eixos` | Eixos RTT de l'AP-7 | [ICGC, RTT i descàrregues](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial) |
| `passos` | P2: `pas_id=2`; alternatius: `pas_id=1` | Polígons del model inclosos; contrast amb RTT i ortofoto |
| `ambit_calcul` | Extensió comuna dels càlculs ràster | Rectangle inclòs al GeoPackage |
| `cobertura_sense_dades` | Diferències petites de cobertura | Capa inclosa per identificar àrees desconegudes |
| `mdt` | Altituds natives de 5 m | [ICGC, elevacions](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions) |
| `ortofoto` | Context d'ortofoto renderitzat a 2 m | [ICGC, ortofoto i serveis](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Imatge/Ortofoto-Territorial) |

Table: Capes i taules del GeoPackage d'inici: funció i accés als recursos.

Per resoldre el cas, utilitza les còpies locals del GeoPackage. Els enllaços permeten consultar les fonts i descarregar dades d'una zona alternativa. A la secció final s'explica què cal conservar de cada descàrrega.

La xarxa inclou vials urbans i rurals al nord i al sud de l'AP-7 i es deriva dels **eixos RTT2024 de l'ICGC**, amb escala òptima de treball d'1:5.000. Conserva `rtt_id`, els atributs cartogràfics i els identificadors de les parts preparades. S'han seleccionat eixos no classificats com autopista i s'han dividit contactes entre extrems i interiors d'eixos de terreny genèric. No s'han creat cruïlles a cada creuament visual. Un marge de carretera no és un eix d'itinerari. L'admissió de trams i la velocitat uniforme són supòsits docents, no certificacions d'accés a peu.

O i D són nodes de la xarxa de l'exercici. **Conserva'ls al mateix lloc durant tota la comparació**. Les coordenades següents permeten reproduir les eines de ruta sense seleccionar a ull:

```text
O: 344407.000000,4553668.360000 [EPSG:25831]
D: 344473.010000,4554030.720000 [EPSG:25831]
```

## Graella comuna

| Propietat | Valor |
| --- | --- |
| X mínim / màxim | 343000 / 346000 m |
| Y mínim / màxim | 4552000 / 4555200 m |
| Mida de cel·la | 5 × 5 m |
| Dimensions | 600 columnes × 640 files |
| CRS | EPSG:25831 |

Table: Extensió, resolució, dimensions i CRS de la graella comuna.

Utilitza **l'extensió de `ambit_calcul`**, sense dependre del zoom del mapa. A GRASS, fixa sempre regió i cel·la de 5 m. Coincidir en CRS i mida de cel·la no basta: també han de coincidir l'extensió i l'origen de la graella.

# A. Distància euclidiana vectorial

1. Cerca **Línia més curta entre objectes / Shortest line between features**, `native:shortestline`.
2. Font: **Origen O**; destinació: **Destí D**; mètode **distància al punt més proper**, **1** veí i distància màxima buida.
3. Desa la capa **euclidiana_vector** al GeoPackage de treball. Consulta'n la distància i mesura també la longitud de la línia.
4. Compara el resultat amb les diferències de coordenades: 66,01 m en X i 362,36 m en Y.

![La línia més curta utilitza Origen O, Destí D i un únic veí. Deixa buida la distància màxima.](captures/distancies-vector-parametres.png){width=85% height=380pt}

$$d=\sqrt{66,01^2+362,36^2}\simeq368,3\ \mathrm{m}.$$

La recta no considera barreres, camins ni permisos de pas. **Conserva la línia, la distància i una frase que expliqui per què això no és encara un itinerari.** Tancar P2 no canvia aquesta mesura.

# B. Distància ràster amb GRASS

## Rasteritzar l'origen

1. Cerca **Rasteritza — vectorial a ràster**, `gdal:rasterize`.
2. Entrada: **Origen O**; valor fix **1**, sense camp d'atributs. Unitats de mida: **georeferenciades**; amplada i alçada **5 m**.
3. Extensió: `ambit_calcul`. Tipus **Float32**; valor inicial **0** i NoData **−9999**. Així el fons zero és vàlid en aquesta primera còpia.
4. Desa `intermedis/origen_zero.tif`. Comprova dimensions i que només una cel·la té valor 1.
5. Amb **Converteix format / Translate**, `gdal:translate`, crea `origen_null.tif` assignant **0 com a NoData**. No canviïs resolució, extensió o CRS.

**GRASS busca les cel·les no nul·les.** A `origen_null`, només la cel·la d'O és origen. Un fons zero vàlid seria també no nul i produiria un resultat equivocat.

## Calcular i consultar la distància

1. Cerca **r.grow.distance**, `grass:r.grow.distance`. Entrada: **origen_null**; mètrica **euclidean**. No activis la cerca de la cel·la NULL més propera.
2. Mantén la regió comuna i 5 m. Amb aquest CRS, les unitats del mapa són metres. Desa **Distance** com `distancia_grass.tif`; la sortida de valor de la cel·la més propera pot ser temporal.
3. Representa la distància amb pseudocolor i llegenda en metres.
4. Executa **Mostreja valors ràster / Sample raster values**, `native:rastersampling`, amb **Destí D** i la distància. Desa el punt amb el valor mostrejat.

![r.grow.distance utilitza un ràster que només té la cel·la origen com a valor no nul. La regió i la mida de cel·la es fixen explícitament.](captures/distancia-grass.png){width=85% height=380pt}

El control a D és **370,74 m**. Els centres de cel·la no són exactament les coordenades dels punts: una diferència petita respecte dels 368,32 m vectorials és esperable.

Com a contrast, executa **Proximitat**, `gdal:proximity`, sobre **origen_zero**, amb píxels objectiu **1**, banda 1, unitats **georeferenciades**, Float32 i NoData −9999. Ha de donar aproximadament el mateix valor a D. No confonguis metres amb nombre de píxels.

**Conserva els dos ràsters d'origen, les distàncies, el valor a D i una explicació de la diferència vector–ràster.**

# C. Itineraris i àrees de servei

## Ruta amb P2 obert

1. Cerca **Camí més curt — punt a punt**, `native:shortestpathpointtopoint`.
2. Xarxa: **xarxa**; criteri **més curt**. Copia les coordenades d'O i D, sense les etiquetes `O:` o `D:`.
3. Direcció per defecte **ambdós sentits**; tolerància topològica **0 m** i tolerància punt–xarxa **0,1 m**.
4. Desa **ruta_obert**. Comprova aproximadament **454,10 m**, superior a la recta.
5. Repeteix amb criteri **més ràpid**, camp `v_kmh` i velocitat per defecte **5 km/h**. El cost és en hores: multiplica per 60 per obtenir **5,45 min**.

La velocitat uniforme és una hipòtesi de comparació. Els sentits dels vehicles no s'han de traslladar automàticament a un model a peu; tampoc aquesta xarxa incorpora una taula completa de maniobres.

## Simular el tancament sense alterar la xarxa inicial

1. Localitza l'eix de P2 a **xarxa**, amb **rtt_id = 1354754**, i contrasta'l amb el polígon **pas_id = 2** de `passos` i l'ortofoto.
2. Amb **Extreu per expressió**, `native:extractbyexpression`, conserva els trams amb `"rtt_id" <> 1354754`. Desa **xarxa_tancada** amb un nom de capa nou.
3. Retirar aquest eix representa el tancament de la connexió al model. No eliminis tots els eixos llargs que només toquen el corredor ràster: podries esborrar també l'accés a O.
4. Repeteix la ruta amb els mateixos O/D. QGIS retorna **sense ruta** en aquesta xarxa preparada. Conserva el missatge i representa la connexió retirada; no introdueixis zero a la columna de distància.

![La ruta oberta segueix els eixos ICGC per P2. En retirar l'eix de P2, la xarxa preparada no proporciona una ruta entre els mateixos O i D.](captures/xarxa.png){width=100% height=380pt}

Aquest resultat depèn dels eixos, exclusions i connexions de la xarxa preparada. No demostra que no hi hagi cap altra possibilitat de desplaçament al territori. Inspecciona el component d'O i els vials propers abans de proposar una ampliació de la xarxa; no augmentis una tolerància només per obtenir una ruta.

## Àrees de servei de 3, 6 i 12 minuts: ampliació a Vila-seca

1. Cerca **Àrea de servei — des d'un punt**, `native:serviceareafrompoint`.
2. Xarxa oberta, origen O, criteri **més ràpid**, `v_kmh` i ambdós sentits.
3. En aquesta versió, **Travel cost** espera **hores**: introdueix **0.05**, **0.10** i **0.20** per a 3, 6 i 12 minuts.
4. Desa les sortides en línies, amb noms diferenciats. Assigna blau, verd i taronja i posa les de temps curt damunt de les llargues.
5. Repeteix amb la xarxa tancada. Comprova si D entra en cada límit.

Les branques accessibles són línies. La suma de totes les seves longituds no és el recorregut d'una persona, i un polígon que les embolcalli no acredita accés a tota la superfície interior.

# D. Construir la fricció amb les cobertes

Una superfície de cost permet moviment entre cel·les. Primer assignarem una resistència relativa a les cobertes. Després identificarem la barrera de l'AP-7 i hi inserirem els passos explícits.

## Classes i pesos

Obre la taula **llegenda_costos** i consulta també `classe`, `categoria` i `data_font` a **cobertes**. El camp `cost_model` conserva els pesos adoptats per poder contrastar la reclassificació; no és una mesura observada de dificultat.

| Classes | Criteri del model | Valor |
| --- | --- | ---: |
| 351 | Xarxa viària | 1 |
| 228, 230, 346, 348, 352 | Prats, espais oberts, zones verdes/esportives i sòl nu | 2 |
| 233 | Platja | 3 |
| 221–227, 229, 344, 347 | Boscos, edificació rural i zones industrials | 6 |
| 234, 349, 354, 355, 461–466 | Zones excloses en aquest model | 99 |
| Altres classes presents | Conreus i altres àrees urbanes, entre altres | 4 |
| 0, sense cobertura | No es coneix la coberta | 99 |

Table: Classes de coberta i valors adoptats al model de fricció.

**99 és un codi de preparació**, que convertirem en NoData al final; no és un cost finit elevat. Les classes urbanes i industrials són àrees generalitzades: no distingeixen cada edifici, tanca o permís. Un camí de cost no és automàticament un itinerari físicament autoritzat.

## Rasteritzar i reclassificar

La font és el [MCSC2024 de l'ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya). Desplega la connexió GeoPackage, carrega **cobertes** i obre'n la taula. Comprova que **classe** és el codi numèric i **categoria** el nom de la coberta. El camp de text no s'ha de rasteritzar.

1. A la Caixa d'eines, cerca **Rasteritza — vectorial a ràster**, `gdal:rasterize`, i obre el diàleg.
2. A **Capa d'entrada**, selecciona **cobertes**. A **Camp per gravar un valor / Field to use for a burn-in value**, selecciona **classe**. No utilitzis un valor fix1: eliminaria la distinció entre les cobertes.
3. A **Unitats de mida de sortida**, selecciona **unitats georeferenciades**. Introdueix **5** a amplada/resolució horitzontal i **5** a alçada/resolució vertical. Són metres, no el nombre de columnes i files.
4. Al selector d'**extensió**, tria **Calcula a partir de la capa → ambit_calcul**. Comprova X343000–346000 i Y4552000–4555200.
5. Desplega els **paràmetres avançats**. Tipus de sortida **Float32**, valor inicial **0** i NoData **−9999**. No canviïs el CRS.
6. A **Rasteritzat**, desa `intermedis/classes.tif` i prem **Executa**. Obre **Propietats → Informació**: han de sortir **600 × 640** cel·les i resolució **5 × 5 m**.
7. Activa **Identifica els objectes** i consulta alguna cel·la: encara ha de contenir un codi de coberta, com111,351 o347, no el pes de fricció.

![Rasterització de cobertes: entrada vectorial, camp classe i resolució en unitats georeferenciades. L'extensió és la comuna de la pràctica.](captures/rasteritzar-cobertes.png){width=85% height=380pt}

Ara transforma els codis en els pesos de la taula:

1. Carrega la taula **llegenda_costos** des de la connexió GeoPackage i consulta-la.
2. Obre **Reclassifica per taula**, `native:reclassifybytable`. Entrada **classes**, banda **1**.
3. Prem els **tres punts** de la taula de reclassificació. Afegeix una fila per classe: mínim, màxim i nou valor. Per exemple **351 / 351 / 1**, **111 / 111 / 4**, **347 / 347 / 6**. Completa les classes de la llegenda i afegeix **0 / 0 / 99** per a la cobertura desconeguda.
4. A **Límits dels intervals**, tria **mínim ≤ valor ≤ màxim**. Amb límits estrictes, una fila amb mínim igual al màxim no inclouria cap valor.
5. Tipus **Float32**, NoData **−9999**, i activa NoData per als valors sense regla. Desa `intermedis/base.tif` i executa.
6. Identifica les mateixes cel·les: una classe351 ara val **1**, una111 **4** i una347 **6**. Les zones excloses tenen **99 numèric vàlid** en aquest pas. Si apareixen nuls inesperats, comprova la regla i els límits de l'interval.

Com a contrast, rasteritzar el camp `cost_model` ha de produir els mateixos pesos, canviant també el fons desconegut de 0 a 99. Encara no hi ha la modificació específica del pas P2.

## Integrar els eixos viaris amb pes 1

El MCSC generalitza les cobertes i pot incloure un camí estret dins d'un polígon de conreu. Per representar els vials admesos, rasteritza també **xarxa**, derivada de l'RTT, sobre la mateixa graella:

1. A `gdal:rasterize`, selecciona **xarxa**, sense camp d'atributs, i valor fix **1**.
2. Resolució georeferenciada **5/5 m**, extensió d'**ambit_calcul**, Float32, valor inicial **0** i NoData **−9999**.
3. Desa `intermedis/vials.tif`. Comprova valors 1 sobre els eixos i 0 vàlid fora; no canviïs l'alineació.

![Els eixos RTT es rasteritzen amb valor fix 1, sense camp, a la graella comuna.](captures/rasteritzar-vials.png){width=85% height=380pt}

La màscara de vials té **15.113 cel·les**. A la base de cobertes, **10.557** encara no tenien pes 1. El condicional integra els vials després de les barreres: no han de reobrir l'AP-7 fora dels passos ni P2 tancat.

## Identificar l'autopista

**No eliminis tota la classe 351:** també conté carrers i altres vials que volem mantenir.

1. Extreu de **cobertes** els polígons de **classe = 351**.
2. Crea un **buffer de 35 m** sobre **autopista_eixos**, amb dissolució. És una banda d'identificació del model, no una mesura exacta de la plataforma.
3. Executa **Intersecció** entre la coberta viària i aquella banda. Desa **barrera_autopista**. Revisa-la sobre l'ortofoto, especialment als enllaços i passos.
4. Rasteritza-la amb valor **1**, valor inicial **0**, NoData **−9999**, regió comuna i 5 m. Desa `barrera.tif`.

La fricció general prové de les cobertes reclassificades. La banda dels eixos s'utilitza només per distingir l'AP-7 dins d'una classe que agrupa tota la xarxa viària.

## Inserir els passos amb un condicional

Els polígons de **passos** connecten els dos costats de la infraestructura en el model ràster. Cal crear-ne una màscara abans de modificar la fricció:

1. Carrega **passos** des del GeoPackage i consulta **pas_id**. P2 té2; els alternatius,1.
2. Obre **Rasteritza — vectorial a ràster**. Entrada **passos**, camp **pas_id**, resolució georeferenciada **5/5m** i extensió d'**ambit_calcul**.
3. Als paràmetres avançats, **Float32**, **valor inicial0** i **NoData−9999**. Això conserva el0 exterior com a valor vàlid que es pot consultar al condicional.
4. Desa `intermedis/pas.tif` i executa. Comprova dimensions600×640, valors1/2 dins dels passos i0 fora. Si el fons és nul, corregeix la rasterització abans de continuar.

![Els passos es rasteritzen amb pas_id. El valor inicial és zero vàlid; les cel·les tenen la mateixa mida i alineació que les cobertes.](captures/rasteritzar-passos.png){width=85% height=380pt}

Els polígons tenen amplada modelada de 20 m i prolongacions de 40 m sobre eixos de travessa. En una altra zona, delimita i revisa els corredors sobre cartografia i ortofoto. Un polígon massa curt pot no arribar als dos costats de la barrera; un de massa ample pot obrir espais que no corresponen al pas.

A la **Calculadora ràster**, utilitza els noms de les bandes carregades. Per a P2 obert:

```text
if("pas@1" > 0, 1,
   if("barrera@1" > 0, 99,
      if("vials@1" = 1, 1,
         if("base@1" = 0, 99, "base@1"))))
```

Per a P2 tancat, mantenint els passos alternatius:

```text
if("pas@1" = 1, 1,
   if(("pas@1" = 2) OR ("barrera@1" > 0), 99,
      if("vials@1" = 1, 1,
         if("base@1" = 0, 99, "base@1"))))
```

En tots dos casos, fixa **600 × 640** cel·les i l'extensió comuna. Desa `friccio_numeric_obert.tif` i `friccio_numeric_tancat.tif`.

**L'ordre importa:** primer el pas admès, després la barrera, els vials i finalment la coberta. En el model tancat, el polígon P2 es marca com a barrera també a les seves prolongacions.

Ara executa **Converteix format / Translate**, assignant **99 com a NoData**, per obtenir `friccio_obert.tif` i `friccio_tancat.tif`. Conserva la mateixa graella. No converteixis el 99 en NoData abans del condicional: els nuls d'una entrada poden propagar-se a la Calculadora ràster i impedir reobrir el corredor.

![La fricció tancada manté els passos alternatius i exclou P2. Els colors representen pesos; les cel·les NoData són barreres.](captures/friccio.png){width=100% height=380pt}

**Comprova amb Identifica**: P2 obert val 1; tancat és NoData; els alternatius continuen amb 1; la plataforma de l'AP-7 fora dels passos és NoData. NoData, zero i un pes alt no són equivalents.

També es pot fer la integració en vector: retallar els polígons de pas contra la coberta viària, retirar aquella porció de la barrera amb **Diferència** i unir-hi els passos amb cost 1. Cal resoldre les superposicions i verificar la prioritat abans de rasteritzar. La cadena principal d'aquesta guia utilitza el condicional ràster, que permet inspeccionar les cel·les dels dos escenaris.

# E. Cost acumulat i camí de menor cost

## Fer que els passos es conservin al cost per cel·la

La capa d'entrada ha de ser **friccio_obert**, amb els passos ja inserits i el99 declarat NoData. Si utilitzes **base**, tornaràs a la fricció anterior als passos i a la barrera de l'AP-7.

1. Obre **Ràster → Calculadora ràster**. Fes doble clic a la banda **friccio_obert@1** de la llista i completa:

```text
"friccio_obert@1" * 5
```

2. Selecciona l'extensió comuna i **600 × 640** cel·les. Format **GeoTIFF**; desa `intermedis/cost_cella_obert.tif` i executa.
3. Desmarca temporalment fricció/base i activa el cost nou. Sobreposa el vector **passos** com a contorn, sense farciment. A **Simbologia**, assigna colors als valors5,10,15,20 i30; el5 permet identificar els vials i passos admesos.
4. Amb **Identifica**, comprova la correspondència següent. L'operació canvia la magnitud, no la possibilitat de pas:

| Cel·la | Fricció integrada | Cost per cel·la |
| --- | ---: | ---: |
| P2 obert | 1 | 5 |
| Pas alternatiu obert | 1 | 5 |
| Coberta de pes4 | 4 | 20 |
| Coberta de pes6 | 6 | 30 |
| Autopista fora dels passos | NoData | NoData |
| P2 en l'escenari tancat | NoData | NoData |

Table: Correspondència entre la fricció integrada i el cost per cel·la.

![Els passos oberts continuen al ràster de cost: les seves cel·les tenen valor5. Els polígons només se sobreposen com a contorn per comprovar-ho.](captures/cost-cella-pas.png){width=100% height=380pt}

Per comprovar una cel·la concreta de P2, consulta **X 344372,5 / Y 4553742,5**; un pas alternatiu té una cel·la de control a **X 344097,5 / Y 4553577,5**. En el cost obert totes dues valen5. En el tancat, P2 és NoData i l'alternatiu continua amb5. Repeteix la multiplicació amb **friccio_tancat** i desa `cost_cella_tancat.tif`.

Si P2 obert desapareix, comprova primer la **fricció**, després el **cost per cel·la** i finalment les opcions de r.cost. Si la fricció ja era nul·la al pas, torna al condicional; si el cost utilitza base en lloc de la fricció integrada, repeteix la conversió. No assignis un cost finit als nuls per intentar reparar la barrera.

## Acumular el cost amb r.cost

1. A la Caixa d'eines obre [r.cost](https://grass.osgeo.org/grass84/manuals/r.cost.html), identificador `grass:r.cost`.
2. **Unit cost layer**: **cost_cella_obert**. **Punts d'inici**: **Origen O**, seleccionat com a capa concreta de la connexió GeoPackage.
3. Deixa buides les coordenades alternatives d'inici, els punts d'aturada i el ràster d'inici. Sense moviment de cavall; activa conservar els nuls. Deixa buit el cost dels nuls.
4. Als paràmetres avançats de GRASS, extensió d'**ambit_calcul** i cel·la5m.
5. Desa **cost acumulat** com `cost_obert.tif` i **direccions de moviment** com `direccions_obert.tif`. Prem **Executa**. Les direccions també són necessàries encara que no les representis.

![r.cost rep el cost de travessar una cel·la i la capa Origen O. El camp de cost dels nuls queda buit per conservar la barrera.](captures/distancies-cost-parametres.png){width=85% height=380pt}

## Reconstruir amb r.path

1. Obre [r.path](https://grass.osgeo.org/grass84/manuals/r.path.html), `grass:r.path`.
2. **Name of input direction**: **direccions_obert**, no cost_obert. **Format**: **degree**.
3. **Vector layer containing starting points**: **Destí D**. La reconstrucció comença al final i retorna cap a O.
4. Mantén la mateixa regió i cel·la. Desa la sortida vectorial **ruta_cost_obert** al GeoPackage de treball; la sortida ràster del camí pot ser temporal.
5. Executa, representa la línia sobre el cost acumulat i repeteix la cadena amb **cost_cella_tancat**, amb noms de sortida nous.

![r.path selecciona les direccions, format degree i Destí D per reconstruir el recorregut.](captures/distancies-path-parametres.png){width=85% height=380pt}

El cost s'expressa en **metres ponderats**, no en minuts. El camí de r.path es reconstrueix des de D seguint les direccions que permeten tornar a O.

![El fons és cost acumulat. Els camins oberts i tancats deriven de friccions diferents, mantenint O i D.](captures/cost.png){width=100% height=380pt}

| Control a D | P2 obert | P2 tancat |
| --- | ---: | ---: |
| Longitud del camí ràster | 474,77 m | 1.920,99 m |
| Cost acumulat | 474,77 m ponderats | 2.840,38 m ponderats |

Table: Longitud del camí ràster i cost acumulat a D amb P2 obert i tancat.

La longitud i el cost no coincideixen quan es travessen cel·les amb pesos diferents. Un itinerari per xarxa i un camí ràster tampoc tenen el mateix espai de moviment. Amb P2 tancat, el ràster permet un camí dins de les cel·les admeses, mentre que la xarxa d'eixos preparada no connecta O i D.

# F. Anisotropia amb MDT i r.walk: ampliació a Vila-seca

Ara estimarem **temps de marxa**. El desnivell canvia de signe en invertir el sentit: pujar i baixar no tenen necessàriament el mateix cost. r.walk rep **altituds**, no un ràster de pendent.

## Preparar altitud i penalització temporal

1. Carrega **mdt** des de la connexió GeoPackage. Amb **Retalla ràster per extensió**, `gdal:cliprasterbyextent`, crea `mdt_ambit.tif` utilitzant `ambit_calcul`, sense canviar el CRS ni la resolució nativa de 5 m.
2. Comprova les dimensions i l'alineació amb la fricció.
3. Converteix els pesos de fricció en **penalització addicional en segons per metre**, amb aquesta regla docent:

```text
("friccio_obert@1" - 1) * 0.125
```

4. Conserva NoData i la graella. Desa `friccio_temporal_obert.tif`; repeteix per al tancat. El pes 1 es converteix en **0 s/m**, el 2 en **0,125**, el 4 en **0,375** i el 6 en **0,625**.

**No multipliquis aquesta penalització per 5.** r.walk incorpora la distància de travessa. Un zero aquí significa sense penalització addicional: continua havent-hi temps de desplaçament i efecte del desnivell.

## Anada i tornada

1. Obre **r.walk.points**. Elevació: **mdt_ambit**; fricció: **friccio_temporal_obert**; inici: **Origen O**.
2. Deixa buits els punts d'aturada i el cost dels nuls; conserva els nuls i desactiva el moviment de cavall.
3. Coeficients **0.72,6.0,1.9998,-1.9998**, **lambda 1** i **slope factor −0,2125**, en m/m. Regió comuna i 5 m.
4. Desa **segons acumulats** i **direccions**. Divideix els segons per **60** per crear una banda en minuts.
5. Mostreja D: aproximadament **401,80 s = 6,70 min**.
6. Reconstrueix amb r.path, direccions de l'anada, format degree i **D** com a punt de reconstrucció.
7. Torna a executar r.walk amb **D com a inici**. Reconstrueix des d'O i mostreja el temps a O: **394,47 s = 6,57 min**.

![r.walk té dues entrades diferents: elevació en metres i penalització temporal en segons per metre.](captures/marxa-parametres.png){width=85% height=380pt}

**Invertir la línia no recalcula el temps.** Les direccions i el temps de cada sentit han de provenir d'una execució amb el seu origen.

![L'anada i la tornada utilitzen càlculs separats sobre el mateix MDT i les mateixes friccions.](captures/marxa.png){width=100% height=380pt}

Per fer un control sense relleu, crea una altitud constant amb `"mdt_ambit@1" * 0`, conservant la graella. Repeteix anada i tornada: totes dues han de donar aproximadament **340,72 s = 5,68 min**. Només has canviat el relleu; fricció i barreres es mantenen.

El MDT de 5 m pot simplificar el perfil d'un pas inferior. Els temps són del model, sense calibració amb caminades observades. En una zona amb més pendent es pot veure una diferència d'anada/tornada més marcada.

# G. Isòcrones i franges de temps: ampliació a Vila-seca

1. Parteix de **marxa des d'O en minuts**. No utilitzis el cost ponderat de r.cost ni una banda en segons amb nivells en minuts.
2. Obre **r.contour**: nivells **3,6,12**, sense increment regular; mínim **3 punts** per línia. Regió comuna i 5 m. Desa **isocrones_obert**.
3. A la Calculadora ràster, crea franges:

```text
if("minuts@1" <= 3, 1,
   if("minuts@1" <= 6, 2,
      if("minuts@1" <= 12, 3, 4)))
```

4. Conserva NoData i la graella. Assigna **blau** a 0–3 min, **verd** a més de 3–6, **taronja** a més de 6–12 i gris clar a més de 12. Diferencia les barreres NoData.
5. Repeteix r.walk des d'O amb P2 tancat, mantenint MDT i paràmetres. Mostreja D: **25,92 min**. Crea contorns i franges amb els mateixos nivells i colors.

![Amb P2 obert, D queda entre les isòcrones de 6 i 12 minuts.](captures/isocrones-obert.png){width=100% height=380pt}

![Amb P2 tancat, D queda fora dels 12 minuts; els passos alternatius mantenen accessibles altres cel·les.](captures/isocrones-tancat.png){width=100% height=380pt}

Compta les classes amb **Informe de valors únics del ràster**. Cada cel·la fa **25 m²**. Per obtenir hectàrees acumulades, suma les cel·les fins al límit, multiplica per 25 i divideix per 10.000.

| Límit | Obert, cel·les | Tancat, cel·les |
| --- | ---: | ---: |
| Fins a 3 min | 2.831 | 2.552 |
| Fins a 6 min | 10.924 | 7.677 |
| Fins a 12 min | 35.430 | 22.109 |

Table: Recompte acumulat de cel·les fins als límits de temps amb P2 obert i tancat.

Les franges d'aquests controls no arriben al límit de càlcul. Si en una altra zona hi arriben, amplia la regió abans d'interpretar-ne la superfície.

# Exercici i síntesi

El cas de Vila-seca permet aprendre i comprovar els procediments. Una zona alternativa pot servir per transferir-los a una altra pregunta, d'acord amb la selecció que indiqui el professor. Dins de cada comparació mantén els mateixos O/D entre models i conserva les entrades, les sortides i un projecte amb rutes relatives.

## Comparacions proposades per al treball de classe

El professor seleccionarà quines d'aquestes operacions, comprovacions i interpretacions formen el treball obligatori del 70%. Anota la selecció de classe i consulta-la a Moodle abans de preparar el lliurament.

1. Calcula la recta euclidiana entre O i D i contrasta-la amb la proximitat ràster a la cel·la origen.
2. Construeix la fricció amb les cobertes, l'AP-7 i els passos. Calcula el cost amb **r.cost** i reconstrueix el camí amb **r.path**, a partir de les direccions i de D. Mesura la longitud del camí i conserva el cost acumulat com una magnitud separada.
3. Comprova les connexions de la xarxa a peu i calcula el camí més curt, amb cost de longitud. En el cas preparat, compara P2 obert i tancat amb O/D fixos.
4. Prepara un mapa del camí ràster, un mapa de les rutes de xarxa i una taula amb les **tres longituds en metres**. Afegeix-hi el control de proximitat i una columna diferenciada de cost ponderat.

Per als apartats seleccionats, explica les decisions, els passos importants, les comprovacions d'alineació, NoData i connectivitat, i els problemes que hagis resolt. Les captures han de permetre seguir aquestes decisions; no cal descriure cada clic.

## Ampliacions

Les ampliacions permeten aprofundir en el problema i aspirar a l'excel·lent. Escull una pregunta que puguis respondre amb dades i controls; la quantitat d'operacions, per si sola, no acredita una millor anàlisi. Separa els resultats addicionals del treball obligatori i declara les seves unitats.

- **Destins i accessos.** Compara diversos destins o un equipament proper. Quin origen queda més afectat pel tancament? Distància recta i accés per xarxa ordenen els destins de la mateixa manera?
- **Repeticions controlades.** Prova altres pesos de fricció, velocitats o resolucions. Canvia un paràmetre cada vegada, mantén una referència i compara longitud, cost o temps en una taula. En quin canvi apareix una resposta molt diferent?
- **Abast temporal.** Desenvolupa les àrees de servei, la marxa anisòtropa o les isòcrones. Quines connexions o superfícies es perden dins de cada límit de temps? Què explica la diferència entre anada i tornada?
- **Un altre territori.** Estudia un pas sobre una carretera, un ferrocarril o una barrera fluvial en una zona amb dades adequades. Justifica els corredors i calcula controls propis; no traslladis els pesos o les connexions de Vila-seca sense revisar-los.

Una aplicació geogràfica pot ser comparar accessos a un equipament, detectar connexions vulnerables o estudiar la sensibilitat d'un itinerari a una barrera. Formula què aportaria l'anàlisi i quines dades addicionals necessitaria: accessos autoritzats, obstacles detallats o temps observats, per exemple. Un resultat del model no és encara una proposta executiva.

## Preparar l'informe

Organitza el PDF perquè expliqui una anàlisi, no una successió de finestres de QGIS:

1. **Pregunta i abast.** Presenta el lloc, els O/D, la selecció obligatòria indicada a classe i la pregunta addicional, si en fas una.
2. **Dades i decisions.** Identifica fonts i dates, CRS, graella, trams admesos, pesos i passos. Explica per què són adequats per a la pregunta.
3. **Procediment i controls.** Mostra els paràmetres que condicionen el resultat i les comprovacions d'alineació, NoData i connectivitat. Explica un problema resolt, si n'hi ha hagut.
4. **Resultats comparables.** Inclou els mapes i les taules necessaris per als apartats seleccionats, amb unitats, llegendes i el mateix enquadrament quan comparis escenaris. Una resposta «sense ruta» no és una distància zero.
5. **Interpretació i límits.** Respon la pregunta, diferencia longitud, cost i temps, i explica què podria canviar amb altres dades o supòsits.
6. **Ampliació i continuïtat.** Si has fet una ampliació, relaciona-la amb la comparació principal i proposa una nova comprovació o aplicació professional.

### Enregistrar la pantalla i extreure captures

Un enregistrament pot ajudar a recuperar els passos que després explicaràs. Utilitza un enregistrador de pantalla, com OBS Studio, i fes una prova breu amb la finestra de QGIS: comprova que es llegeixen els camps, els paràmetres i els noms de capa. Enregistra fragments dels passos importants i anota el moment de cada decisió o resultat.

Després, obre el vídeo en un reproductor, pausa'l en el fotograma útil i desa'l amb la funció de captura de fotograma. Retalla només les zones que no aporten informació; conserva el nom de l'eina, els paràmetres rellevants i el context necessari. Numera cada captura i escriu un peu que expliqui què demostra. Per als mapes finals, prefereix una exportació cartogràfica amb llegenda, escala i unitats.

El vídeo és una ajuda per documentar el treball; no cal lliurar-lo tret que el professor ho indiqui. Selecciona evidències que sostinguin l'explicació, en lloc d'omplir l'informe amb tots els fotogrames.

## Lliurament i qualificació

Lliura aquests fitxers:

- `accessibilitat-vilaseca-cognom.gpkg`: capes generades i projecte incrustat.
- `accessibilitat-vilaseca-cognom.qgz`: còpia externa del projecte amb rutes relatives.
- `accessibilitat-vilaseca-cognom.pdf`: informe amb mapes, taules, captures comentades i conclusions dels apartats seleccionats.

Conserva també els TIFF als quals faci referència el projecte; si lliures la carpeta en un ZIP, mantén-ne l'estructura. En una zona alternativa, utilitza un nom de fitxer que identifiqui el cas.

La qualificació distribueix **70% als apartats obligatoris que el professor indicarà a classe**, **20% a les ampliacions** i **10% a la qualitat de l'informe, captures, mapes i organització**. Les ampliacions permeten aspirar a l'excel·lent, però no substitueixen els obligatoris ni garanteixen una nota per haver-les intentat. Comprova l'obertura del projecte després de moure la carpeta completa.

Per als models que hagis treballat a Vila-seca, pots orientar la discussió amb aquestes preguntes:

- Per què vector i ràster euclidians difereixen una mica?
- Per què tancar P2 modifica les rutes però no la separació recta?
- Què aporta separar fricció, cost acumulat i longitud?
- Per què un pas s'ha d'inserir abans de convertir la barrera en NoData?
- Quines dades permetrien saber si una alternativa calculada es pot recórrer realment?

Si treballes les ampliacions temporals, explica també per què l'anada i la tornada necessiten execucions separades i per què les branques d'una àrea de servei i les franges de temps ràster no són el mateix indicador.

En una zona alternativa, justifica O/D, àmbit, resolució, fonts, pesos i passos. Revisa connexions i barreres sobre la cartografia. La taula de pesos de Vila-seca no és una regla universal. Calcula els controls del nou cas; si hi afegeixes isòcrones, comprova que no estan retallades.

## Dades i descàrregues per a altres zones

| Necessitat | Productor i accés | Preparació |
| --- | --- | --- |
| Cobertes vectorials | [ICGC, Mapa de cobertes](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya) | Al visor de descàrregues, selecciona una àrea; o descarrega el GeoPackage de la versió triada. Retalla una còpia i conserva classe, data i llegenda. |
| Cobertes completes | [GeoPackage](https://datacloud.icgc.cat/datacloud/cobertes-sol/gpkg/) i [GeoTIFF](https://datacloud.icgc.cat/datacloud/cobertes-sol/tif_unzip/) de l'ICGC | Els fitxers complets són grans. En GeoTIFF, els valors 1–41 són `index_raster`, no els codis vectorials 111–466; consulta la llegenda abans de reclassificar. |
| Xarxa i elements topogràfics | [ICGC, Referencial Topogràfic Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial) | GeoPackage per [àrea](https://visors.icgc.cat/appdownloads/?c=fmetopoterritorial) o [full](https://visors.icgc.cat/appdownloads/?c=dlftopoterritorial), amb escala òptima d'1:5.000. Distingeix eixos, marges, tipus i passos a diferent nivell i comprova les connexions. |
| Vials OSM | [Geofabrik, Catalunya](https://download.geofabrik.de/europe/spain/cataluna.html) | El PBF conté nodes, vies i relacions. Prepara un extracte que conservi les referències i converteix-lo en capes locals GeoPackage amb índex espacial abans del treball interactiu. Revisa accessos i connexions. QuickOSM permet consultes d'àrees petites, subjectes a la disponibilitat d'Overpass. |
| Elevacions | [ICGC, Elevacions](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions) | Tria MDT, no MDS, i la resolució adequada. Desa un retall local i alinea la graella sense inventar més detall. |
| Context d'ortofoto | [ICGC, Ortofoto Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Imatge/Ortofoto-Territorial) | Servei WMS/WMTS per explorar; descàrrega o còpia local per continuar sense connexió. |
| Límits | [ICGC, Divisions administratives](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives) | Utilitza el límit per contrastar cobertura. Un retall massa ajustat pot eliminar una connexió externa necessària. |

Table: Fonts i preparació de dades per aplicar la cadena en una altra zona.

Per reunir una altra pràctica compacta, crea un GeoPackage, exporta-hi les capes amb noms clars i desa-hi el projecte. Mantén els originals, anota productor, data, transformacions i llicència, i comprova l'obertura després de moure la carpeta de treball.

# Fonts del cas i comprovació final

ICGC: divisions administratives del 20/1/2026, MCSC2024, RTT2024, MDT LiDAR 2021–2023 a 5 m i ortofoto2025, amb llicència CC BY4.0. La còpia de context es va demanar al WMS de 25 cm a **2 m per píxel de sortida**. La xarxa es prepara amb eixos RTT de l'ICGC; OSM s'explica com una font alternativa per a altres estudis, no com la font de la xarxa d'aquest paquet.

La cartografia de cobertes i el límit municipal tenen petites diferències: la capa **cobertura_sense_dades** les mostra i es conserven com a informació desconeguda. La classificació generalitzada no resol el detall de tots els obstacles.

Abans de lliurar, tanca QGIS i obre una còpia de tota la carpeta en una altra ubicació. Comprova capes, connexió GeoPackage, projecte, CRS, unitats, NoData, resultats i llegendes. Les notes docents contenen els controls complets; aquesta guia permet obtenir-los treballant a partir de les dades inicials.

Consulta també els manuals de [QGIS3.44](https://docs.qgis.org/3.44/en/docs/user_manual/), [r.grow.distance](https://grass.osgeo.org/grass84/manuals/r.grow.distance.html), [r.cost](https://grass.osgeo.org/grass84/manuals/r.cost.html), [r.path](https://grass.osgeo.org/grass84/manuals/r.path.html), [r.walk](https://grass.osgeo.org/grass84/manuals/r.walk.html) i [r.contour](https://grass.osgeo.org/grass84/manuals/r.contour.html).
