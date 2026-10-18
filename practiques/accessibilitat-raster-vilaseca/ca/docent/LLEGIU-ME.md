---
title: "Guia docent: model ràster de cost"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
---

# Abast i durada orientativa

Bloc de proximitat, fricció, barreres/passos i camí de cost. Es recomana separar la construcció de la superfície de la cadena r.cost/r.path.

| Component | Estimació |
| --- | --- |
| Aula | 150–180min, repartibles en dues sessions |
| Treball autònom i informe | 90–120min |
| Preparació docent | 45–60min |

Table: Durada orientativa del bloc ràster.

Estimació pendent de contrast amb una classe, amb QGIS/GDAL/GRASS preparats, dades locals i nocions de ràster. Comprova els proveïdors i una execució petita abans de classe. La selecció del70% pot reduir l'abast; canviar de zona o diagnosticar instal·lacions l'amplia. El temps de càlcul automàtic no equival al d'aprenentatge.

# Preparar Moodle

1. Crea una **Tasca** amb el nom **Accessibilitat: model ràster de cost**.
2. Adjunta `accessibilitat-raster-vilaseca-2026-10-18-ca.zip` a **Fitxers addicionals**.
3. Copia el bloc següent a **Descripció**, fins a «Qualificació», i afegeix la selecció anunciada a classe.
4. Revisa la vista d'estudiant. Conserva la resolució i els projectes docents per contrastar errors de graella, passos o NoData.

## Enunciat per copiar a la descripció

**Dades.** Descarregueu `accessibilitat-raster-vilaseca-2026-10-18-ca.zip`. Obriu inici de `accessibilitat-vilaseca.gpkg` amb QGIS3.44, GDAL i GRASS, i llegiu `LLEGIU-ME.pdf`. Manteniu O/D, EPSG:25831/NONE i graella5m.

**Treball de classe.** El professor indicarà els apartats obligatoris del70%: proximitat, reclassificació de cobertes, vials de pes1, barreres/passos, r.cost/r.path i comparació de longitud/cost. La guia completa no obliga a lliurar tots els passos. Comproveu alineació i la prioritat pas → barrera → vial → coberta.

**Ampliacions per aspirar a l'excel·lent.** Compareu el model només de cobertes amb el que integra vials, o canvieu pesos/resolució o zona amb una referència i controls. Què passa quan la coberta generalitza un camí dins d'un conreu? Desenvolupeu una aplicació geogràfica i identifiqueu les dades que faltaria contrastar.

**Informe i lliurament.** Entregueu vectors en GeoPackage, projecte relatiu, TIFF requerits i PDF amb pregunta, fonts, decisions, controls, mapes/taula i conclusions. Podeu enregistrar la pantalla i extreure captures llegibles i comentades; el vídeo només es lliura si el professor ho indica. Comproveu l'obertura des d'una altra carpeta.

**Qualificació.** 70% apartats indicats a classe;20% ampliacions;10% informe, captures, mapes i organització. Es valoren pregunta, controls i interpretació, no el nombre d'operacions.

# Graella, cobertes i vials

Graella EPSG:25831/NONE, X 343000–346000 i Y 4552000–4555200; cel·la de 5×5 m i 600×640 cel·les.

O = (344407; 4553668,36) m; D = (344473,01; 4554030,72) m. La proximitat entre centres és 370,742498 m; la recta vectorial, 368,323349 m.

Rasteritza **classe** de cobertes i reclassifica amb límits inclusius. Pesos1/2/3/4/6 i99com a codi de barrera. El fons desconegut0 es recodifica a99; no s'interpreta com cost zero. La base de cobertes es conserva per contrastar el model.

![La màscara de vials rasteritza els eixos RTT amb valor fix1 a la graella comuna.](captures/rasteritzar-vials.png){width=80% height=350pt}

La màscara té15.113cel·les;10.557 no tenien pes1 a la base. Comprova que s'ha triat **xarxa**, amb camp buit i valor1. La integració dona prioritat a barreres/passos abans dels eixos, per no obrir l'AP-7 pel simple encreuament d'una línia.

# Condicional i control de passos

P2obert:

```text
if("pas@1" > 0, 1,
   if("barrera@1" > 0, 99,
      if("vials@1" = 1, 1,
         if("base@1" = 0, 99, "base@1"))))
```

P2tancat:

```text
if("pas@1" = 1, 1,
   if(("pas@1" = 2) OR ("barrera@1" > 0), 99,
      if("vials@1" = 1, 1,
         if("base@1" = 0, 99, "base@1"))))
```

Només després s'assigna99com a NoData. Multiplicar la fricció integrada per5conserva el conjunt de cel·les admeses/excloses. Utilitzar base en lloc de fricció torna al model sense els passos i vials integrats.

| Control | Fricció oberta | Cost obert | Fricció tancada | Cost tancat |
| --- | ---: | ---: | ---: | ---: |
| P2,344372,5/4553742,5 | 1 | 5 | NoData | NoData |
| Alternatiu,344097,5/4553577,5 | 1 | 5 | 1 | 5 |
| AP-7 fora dels passos | NoData | NoData | NoData | NoData |

Table: Controls de cel·la abans d'acumular el cost.

![Vials i passos de pes1 es conserven amb cost per cel·la5.](captures/cost-cella-pas.png){width=100% height=350pt}

# Cost, direccions i reconstrucció

r.cost utilitza cost_cella, Origen O, nuls conservats, cost dels nuls buit i sense moviment de cavall. Regió comuna5m. r.path utilitza les direccions, formatdegree i D, no la banda de cost.

| Magnitud | Obert | Tancat |
| --- | ---: | ---: |
| Longitud del camí | 474,766594m | 1920,990258m |
| Cost acumulat a D | 474,766594m ponderats | 2840,376259m ponderats |
| Cel·les excloses | 16.987 | 17.078 |

Table: Controls de referència del model amb vials integrats.

![Els camins oberts i tancats provenen de les superfícies corregides.](captures/cost.png){width=100% height=350pt}

El camí obert recorre cel·les de pes1; per això cost i longitud coincideixen. En el tancat es travessen altres pesos. Les91cel·les de diferència d'exclusió són P2. La superfície permet un camí tancat, mentre que el graf del bloc vectorial no connecta O/D: són espais de moviment diferents.

# Projectes, revisió i fonts

El docent conserva les vistes00/01/02/05/06/07amb les dependències: inici, distàncies, xarxa de contrast, friccions i cost. Intermedis de cobertes, vials, passos, barrera i direccions permeten reprendre la diagnosi sense recalcular durant la classe.

Revisa els apartats anunciats, les quatre màscares, la graella, NoData, les unitats i la interpretació. En una altra zona, demana controls propis. Les ampliacions han d'explicar què es manté i què canvia; les captures d'un vídeo són evidències seleccionades, no un informe complet.

Fonts: [MCSC2024](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya), [RTT2024](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial), ortofoto2025/límit20/1/2026, [condicions ICGC](https://www.icgc.cat/condicions), [r.cost](https://grass.osgeo.org/grass84/manuals/r.cost.html), [r.path](https://grass.osgeo.org/grass84/manuals/r.path.html).
