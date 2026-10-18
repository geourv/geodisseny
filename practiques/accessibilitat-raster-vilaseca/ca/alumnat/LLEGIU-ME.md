---
title: "Pràctica: accessibilitat amb un model ràster de cost"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
---

# Cobertes, vials, barreres i camí de cost

El moviment entre cel·les permet comparar un itinerari amb una superfície territorial. Construirem la fricció amb cobertes MCSC, eixos viaris RTT i passos de l'AP-7. Integrar els camins és essencial: una coberta generalitzada pot incloure un vial estret dins d'un polígon de conreu.

**El professor indicarà a classe els apartats obligatoris dins del70%**, i els recollirà a Moodle. Aquesta guia desenvolupa el bloc ràster; temps de marxa i isòcrones es treballen en un altre bloc. Les ampliacions permeten aspirar a l'excel·lent amb una pregunta i controls.

# Preparació i graella

El ZIP conté `accessibilitat-vilaseca.gpkg` i aquest PDF. Obre el projecte **inici** des d'**Explorador → GeoPackage → Connexió nova**, amb QGIS3.44, GDAL i GRASS. Cerca `r.grow.distance`, `r.cost` i `r.path` a **Procés → Caixa d'eines**; revisa la instal·lació si no apareixen.

Treballa sobre una còpia i crea `intermedis/` per als TIFF. Guarda vectors amb noms nous en un GeoPackage i el projecte amb rutes relatives. Selecciona la capa concreta —Origen O, Destí D, cobertes o xarxa—, no el fitxer complet amb totes les taules.

| Propietat | Valor |
| --- | --- |
| CRS /el·lipsoide | EPSG:25831 /Cap–NONE |
| X mínim/màxim | 343000 /346000 m |
| Y mínim/màxim | 4552000 /4555200 m |
| Cel·la /dimensions | 5×5m /600columnes×640files |
| O | (344407;4553668,36) m |
| D | (344473,01;4554030,72) m |

Table: Graella i punts comuns de tots els càlculs.

Utilitza l'extensió d'**ambit_calcul**, sense dependre del zoom. Coincidir en CRS i cel·la no basta: extensió i origen de la graella també han de coincidir.

# Proximitat ràster

1. A `gdal:rasterize`, rasteritza **Origen O** amb valor1, sense camp, resolució georeferenciada5/5m i extensió comuna. Float32, inicial0, NoData−9999. Desa **origen_zero.tif**.
2. Amb `gdal:translate`, crea **origen_null.tif** assignant0 com a NoData. Només O queda no nul; conserva la graella.
3. A **r.grow.distance**, entrada origen_null, mètrica euclidean, cerca de NULL desactivada, regió comuna i5m. Desa **distancia_grass.tif**.
4. Mostreja D amb `native:rastersampling`: aproximadament **370,74m**. Contrasta amb `gdal:proximity`, sobre origen_zero, objectiu1 i unitats georeferenciades.

![r.grow.distance utilitza només la cel·la origen com a valor no nul.](captures/distancia-grass.png){width=80% height=350pt}

La recta vectorial fa368,32m. La diferència prové dels centres de cel·la, no d'una ruta que eviti barreres.

# Reclassificar les cobertes

Carrega **cobertes** i consulta `classe`, `categoria` i **llegenda_costos**. Rasteritza el camp numèric **classe**, amb la graella comuna, Float32, inicial0 i NoData−9999. Desa **classes.tif**; encara són codis de coberta.

![Rasterització de la classe de coberta, amb resolució georeferenciada i extensió comuna.](captures/rasteritzar-cobertes.png){width=80% height=350pt}

| Classes | Criteri del model | Pes |
| --- | --- | ---: |
| 351 | Xarxa viària de la coberta | 1 |
| 228,230,346,348,352 | Prats, espais oberts, zones verdes/esportives i sòl nu | 2 |
| 233 | Platja | 3 |
| 221–227,229,344,347 | Boscos, edificació rural i zones industrials | 6 |
| 234,349,354,355,461–466 | Classes excloses | 99 |
| Altres classes presents | Conreus i altres àrees urbanes | 4 |
| 0 | Cobertura desconeguda | 99 |

Table: Pesos docents de coberta;99 és un codi de preparació de barrera.

A **Reclassifica per taula**, `native:reclassifybytable`, entrada classes, banda1, afegeix una fila mínim/màxim/pes per classe. Exemples351/351/1,111/111/4,347/347/6 i0/0/99. Utilitza límits **mínim≤valor≤màxim**, Float32 i NoData per als valors sense regla. Desa **base.tif**.

Consulta les mateixes cel·les abans/després. El99 ha de continuar vàlid en aquest intermedi: la conversió a NoData es fa després d'integrar vials, barreres i passos.

# Integrar vials, autopista i passos

## Eixos viaris

Rasteritza **xarxa**, amb **valor fix1 i camp buit**, inicial0, NoData−9999, Float32 i la mateixa graella. Desa **vials.tif**. Els eixos provenen de l'RTT2024; la selecció admesa és la del model a peu.

![Rasterització dels eixos RTT amb valor fix1, sense camp d'atributs.](captures/rasteritzar-vials.png){width=80% height=350pt}

Control:15.113cel·les de vial,10.557 de les quals no tenien pes1 a la base de cobertes. La màscara representa els eixos amb cel·les, no l'amplada exacta de cada camí ni un permís d'accés.

## Plataforma de l'AP-7

Extreu **classe351** de cobertes. Crea un buffer35m sobre **autopista_eixos**, dissolt, i intersecta'l amb aquella coberta viària. Desa **barrera_autopista** i revisa-la sobre ortofoto. Rasteritza-la amb valor1, inicial0, NoData−9999 i la graella comuna: **barrera.tif**.

No eliminis tota la classe351: conté altres vials que s'han de conservar. Els35m són un paràmetre d'identificació, no una mesura exacta de la plataforma.

## Corredors

Rasteritza **passos** amb camp **pas_id**, mateixa graella, inicial0 vàlid i NoData−9999. Desa **pas.tif**: alternatius1, P2=2 i exterior0. Comprova que els corredors arriben als dos costats de la barrera.

![La màscara conserva pas_id i un fons zero consultable pel condicional.](captures/rasteritzar-passos.png){width=80% height=350pt}

## Prioritat del condicional

A Calculadora ràster, fixa600×640cel·les i l'extensió comuna. Per a P2 obert:

```text
if("pas@1" > 0, 1,
   if("barrera@1" > 0, 99,
      if("vials@1" = 1, 1,
         if("base@1" = 0, 99, "base@1"))))
```

Per a P2 tancat, mantenint els alternatius:

```text
if("pas@1" = 1, 1,
   if(("pas@1" = 2) OR ("barrera@1" > 0), 99,
      if("vials@1" = 1, 1,
         if("base@1" = 0, 99, "base@1"))))
```

Desa **friccio_numeric_obert/tancat**. La prioritat és **pas admès → barrera/P2 tancat → vial → coberta**. Els vials no reobren l'autopista fora dels passos. Ara utilitza Translate assignant99 com a NoData: **friccio_obert/tancat.tif**.

![Fricció tancada amb vials integrats i les barreres conservades.](captures/friccio.png){width=100% height=350pt}

# Cost acumulat i camí

1. Multiplica la **fricció integrada**, no base, per5. Desa **cost_cella_obert/tancat.tif**. Mantén NoData i graella.
2. A **r.cost**, entrada cost_cella_obert, inici **Origen O**, altres formes d'inici/aturada buides. Sense moviment de cavall, conserva nuls i deixa buit el cost dels nuls. Regió comuna i5m.
3. Desa **cost_obert.tif** i **direccions_obert.tif**.

![r.cost rep el cost per cel·la i conserva les barreres nul·les.](captures/distancies-cost-parametres.png){width=80% height=350pt}

4. A **r.path**, entrada **direccions_obert**, formatdegree i **Destí D** com a punt de reconstrucció. Desa la ruta vectorial al GeoPackage de treball.
5. Repeteix la cadena tancada amb noms nous. Mesura la longitud i mostreja el cost a D.

![r.path parteix de D i segueix les direccions de retorn cap a O.](captures/distancies-path-parametres.png){width=80% height=350pt}

| Control | Obert | Tancat |
| --- | ---: | ---: |
| Longitud del camí | 474,77m | 1.920,99m |
| Cost acumulat | 474,77m ponderats | 2.840,38m ponderats |

Table: Longitud i cost amb els mateixos O/D, vials i passos integrats.

![Camins de cost recalculats amb els eixos viaris incorporats a la fricció.](captures/cost.png){width=100% height=350pt}

Amb P2 obert, cost i longitud coincideixen perquè el camí recorre cel·les de pes1. Això no és general: el tancat travessa altres pesos. El ràster permet moviment entre cel·les admeses; la xarxa d'eixos del bloc vectorial queda sense ruta en tancar P2.

# Ampliacions, informe i fonts

Compara la base de cobertes amb el model que incorpora vials. Quin traçat canviaria si els camins quedessin amagats dins d'un polígon de conreu? Prova altres pesos o resolucions, canviant un paràmetre cada vegada. En una altra zona, justifica fonts, punts, graella i passos i calcula controls propis.

Proposa una aplicació geogràfica: comparar accessos o estudiar una barrera. Quines dades detallades, accessos autoritzats o observacions farien falta? Un camí de menor cost no certifica un itinerari físic.

L'informe ha d'explicar pregunta, dades, decisions, controls d'alineació/NoData, mapes i taula, i interpretació. Pots enregistrar fragments de pantalla i desar fotogrames llegibles des d'un reproductor; numera'ls i comenta'ls. Exporta els mapes finals amb llegenda, escala i unitats. El vídeo només es lliura si el professor ho indica.

Lliura GeoPackage amb vectors, projecte `.qgz` relatiu, TIFF referenciats i informe PDF, amb el prefix **accessibilitat-raster-vilaseca-cognom**. Comprova l'obertura després de moure la carpeta completa.

Qualificació: **70% apartats obligatoris indicats a classe**, **20% ampliacions**, **10% informe, captures, mapes i organització**. Les ampliacions no substitueixen els obligatoris ni garanteixen una nota.

Fonts: [ICGC MCSC2024](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya), [RTT2024](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial), límit20/1/2026 i ortofoto2025; [condicions ICGC](https://www.icgc.cat/condicions), [QGIS3.44](https://docs.qgis.org/3.44/en/docs/user_manual/), [r.cost](https://grass.osgeo.org/grass84/manuals/r.cost.html) i [r.path](https://grass.osgeo.org/grass84/manuals/r.path.html).
