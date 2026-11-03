---
title: "Guia docent: estadística espacial descriptiva"
author: Benito Zaragozí
lang: ca
date: "Edició: 30 d'octubre de 2026"
content_status: review
---

# Preparar la tasca de Moodle

## Durada orientativa

| Component | Estimació |
| --- | --- |
| Aula: recompte, centres, dispersió i densitat | 120–150 min |
| Treball autònom i informe | 90–120 min |
| Preparació docent | 30–45 min |

Table: Estimació orientativa per al recorregut descriptiu complet.

S'assumeixen QGIS preparat, dades locals i experiència bàsica amb capes i taules. És una estimació pendent de contrast amb una classe, no un temps mesurat. La selecció del 70% pot reduir el recorregut; una altra zona, malla o escenari pot ampliar el treball autònom. El nombre de pàgines no mesura la càrrega de treball.

1. Activa l'edició del curs i tria **Afegir una activitat o un recurs → Tasca**. Posa-hi el nom **Estadística espacial descriptiva**.
2. Obre **`ENUNCIAT-MOODLE.md`**, lliurat al costat d'aquest PDF. Copia'n el text editable a **Descripció** i concreta els apartats seleccionats a classe i el codi real de pràctica. El marcador `prN` dels patrons de nom no fixa la numeració del curs.
3. A **Fitxers addicionals**, adjunta **`estadistica-espacial-descriptiva.zip`**, el paquet d'inici. L'alumnat hi trobarà les dades, els recursos locals i el `LLEGIU-ME.pdf`.
4. Revisa la tasca amb la vista d'estudiant i comprova la descàrrega. Utilitza la resolució i el paquet docent per preparar les explicacions i contrastar els treballs.

# Preparació i recorregut

La seqüència manté el mateix conjunt: **recompte → centres → dispersió → densitat**. `LLEGIU-ME.pdf` és a l'arrel i els recursos a `data/`. El paquet d'inici conté les entrades; el docent hi afegeix els resultats descriptius i **`data/docent.qgz`**. Obre aquest projecte, conservant els GeoPackage vectorials, els GeoTIFF de `data/rasters/` i els recursos locals. Les rutes són relatives i el dibuix segueix el panell Capes.

Selecciona els apartats que entraran al 70% obligatori, comunica'ls a classe i deixa la mateixa selecció a Moodle. Distingeix les demostracions docents dels resultats que l'alumnat haurà de calcular. Per a una ampliació, demana pregunta, referència, registre de paràmetres i interpretació; una repetició aporta valor quan permet explicar una diferència o estabilitat.

Treballa amb QGIS 3.44 LTR, EPSG:25831 i el·lipsoide NONE. Els resultats de referència provenen de la preparació de Constantí del 5/10/2026, amb QGIS 3.44.11. Els dos GeoPackage són còpies de lliurament noves: els originals de reconstrucció es conserven separadament.

# Dades i pesos

| Control | Valor |
| --- | ---: |
| Registres municipals | 124 |
| Potències publicades | 98 |
| Intervals sense xifra | 26 |
| Suma publicada | 2.770 kW |
| Pes central amb estimacions | 2.970 kW |
| Part assignada | 200 kW |

Table: Selecció municipal i diferència entre observacions i escenari de pesos.

Les assignacions són 2,5/15/62,5 kW en 19/6/1 registres, respectivament. `POT_KW` es conserva; `w_mid` i `imputat` distingeixen l'escenari central. No descriure els 200 kW com potència mesurada. Els punts són consumidors associats, no petjades de panells.

# Recompte per quadrats

`native:countpointsinpolygon` sobre `malla` i `punts` dona 90 quadrats d'1 km² i suma 124. La segona passada amb `coneguda` i pes `POT_KW` suma 2.770 kW coneguts.

| Quadrat, coordenades mínimes | Registres | Potència publicada |
| --- | ---: | ---: |
| 349500 / 4557000 m | 48 | 268 kW |
| 345500 / 4558000 m | 17 | 891 kW |

Table: Dos quadrats que diferencien concentració de localitzacions i de potència.

Revisar que es compten els 124 registres i no només els 98 coneguts. Un camp absent no és zero; les dues sumes tenen denominadors diferents. El suport regular d'1 km² permet llegir el recompte com registres/km², però no traslladar aquella equivalència a polígons d'una altra superfície.

# Centres i dispersió

| Resum | Valor de referència |
| --- | --- |
| Centre dels registres | (349051,53; 4557573,88) m |
| Centre ponderat amb `w_mid` | (347321,21; 4558177,04) m |
| Desplaçament | 1.832,43 m |
| Radi de dispersió | 2.000,66 m |
| Semieixos de l'el·lipse | 1.934,44 / 510,47 m |
| Azimut major | 110,22° |

Table: Centres i resums de dispersió en EPSG:25831, amb xifres impreses arrodonides.

El centre ponderat es desplaça a l'oest i lleument al nord. Els 450 kW aporten aproximadament el 15,2% del pes central; els cinc pesos més grans, el 37,4%. Demanar que l'explicació relacione aquests pesos amb llocs recognoscibles, no només amb una distància.

Els dos resums de dispersió utilitzen **124 punts i el centre no ponderat**. El radi correspon a l'arrel de la suma de variàncies poblacionals X/Y; els semieixos provenen dels autovalors de la covariància, amb divisor n. No són resums ponderats ni intervals inferencials.

![Resums sobre els mateixos punts, centre, límit i ortofoto.](captures/c4-cercle-ellipse.png){width=95% height=380pt}

La guia practica el dibuix amb constants arrodonides sobre el centre produït per l'estudiant. La capa docent conserva els paràmetres i geometries complets. Una diferència mínima de vora per arrodoniment no justifica moure punts, eliminar coincidències o canviar el conjunt de referència.

Discutir un punt exterior i un espai interior amb pocs registres. El contorn no implica que tots els registres hi siguen dins, ni una cobertura de servei o probabilitat fixa.

# Densitat i normalització

| Kernel Quartic sense pes | Píxel | Integral de la densitat |
| --- | ---: | ---: |
| Radi 500 m | 100 m | ≈124 registres |
| Radi 1.500 m | 100 m | ≈124 registres |

Table: Controls de massa dels ràsters normalitzats amb àrea de píxel de 0,01 km².

La normalització de Raw és $3\times10^6/(\pi h^2)$, amb h en metres. Utilitzar la mateixa escala de color i distingir radi de contribució, discretització i unitat. NoData es conserva; no s'interpreta com absència comprovada d'instal·lacions.

# Revisió del treball i fonts

El lliurament de l'estudiant ha de contenir resultats propis dels apartats anunciats, projecte relatiu, paràmetres i interpretació. Comprovar sumes, CRS/NONE, centre emprat en la dispersió, unitats del kernel i portabilitat segons la selecció de classe. La semblança amb el resultat docent no substitueix l'explicació de cada resum.

Per a les ampliacions, contrastar què s'ha mantingut i què s'ha canviat. Una altra malla altera l'agregació; un altre radi altera la contribució espacial; un pes assignat altera l'escenari, no l'observació publicada. En un altre municipi, els controls de Constantí no són resultats esperats. Valorar també l'aplicació geogràfica proposada i les dades que requeriria.

L'informe ha de respondre una pregunta amb taules i mapes comparables, captures comentades i límits. Les imatges extretes d'un enregistrament poden documentar decisions; ni la gravació completa ni una successió de finestres substitueixen l'explicació.

## Selecció i portabilitat del lliurament

L'alumnat conserva `data/`, desa el projecte de treball, proves i intermedis a `sandbox/` i prepara la selecció final a `dist/`. Els grups de capes no mouen fitxers. El paquet docent conserva els resultats de referència; el lliurament de l'estudiant conté els apartats realment demanats.

Comprova un GeoPackage **nou** amb els vectors seleccionats i els camps necessaris per interpretar-los, un QGZ **extern** relatiu, l'informe PDF i els GeoTIFF pertinents, amb noms codi–tema–cognoms. Si s'ha lliurat densitat, la guia conserva raw i normalitzat amb els seus controls. Les proves descartades no s'afegeixen automàticament.

Reobre una carpeta traslladada o un ZIP extret, sense xarxa. Les capes del QGZ final han de llegir els fitxers de la còpia, sense dependències de `data/` o `sandbox/` originals. Revisa dades, estils, etiquetes, ordre i disponibilitat de la font tipogràfica. Conserva `fonts/` si és necessària; l'XML del WMS només cal si aquella capa es manté, amb el context local com a alternativa offline.

ICAEN: extracció del 28/9/2026, sense data efectiva establerta. ICGC: límit del 20/1/2026, ortofoto WMS 2025. [Localització ICAEN](https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/), [condicions ICGC](https://www.icgc.cat/condicions) i [QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/).

Moran, LISA i renda no formen part d'aquesta activitat. Es conserven en la preparació històrica per a un recorregut posterior.
