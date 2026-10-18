---
title: "Resolució docent: punts, centres i dispersió a Constantí"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
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

1. Activa l'edició del curs i tria **Afegir una activitat o un recurs → Tasca**. Posa-hi el nom **Estadística espacial: punts, centres i dispersió a Constantí**.
2. A **Descripció**, enganxa el bloc següent, des de «Dades de partida» fins al final de «Qualificació».
3. A **Fitxers addicionals**, adjunta **`estadistica-constanti-2026-10-18-ca.zip`**, el paquet d'inici. L'alumnat hi trobarà les dades, els recursos locals i el `LLEGIU-ME.pdf`.
4. Revisa la tasca amb la vista d'estudiant i comprova la descàrrega. Utilitza la resolució i el paquet docent per preparar les explicacions i contrastar els treballs.

## Enunciat per copiar a la descripció

**Dades de partida.** Descarregueu `estadistica-constanti-2026-10-18-ca.zip`, adjunt a aquesta tasca, i descomprimiu-lo en una carpeta pròpia, conservant-ne l'estructura. Llegiu `LLEGIU-ME.pdf` i obriu el projecte **inici** de `payload/data/estadistica-constanti.gpkg` amb QGIS 3.44. El paquet conté els punts de Constantí, les potències publicades i els pesos de l'escenari, una malla d'1 km de costat, el límit municipal i l'ortofoto. Conserveu també els recursos de `payload/data/fonts/`.

**Treball de classe.** El professor indicarà a classe quins apartats, exercicis i comprovacions són obligatoris dins del **70% de la qualificació** i ho recollirà en aquesta tasca. La guia desenvolupa un recorregut complet: no tots els passos són automàticament obligatoris. Compareu nombre de registres, potència, localització, dispersió i densitat mitjançant els blocs seleccionats:

1. Compteu els punts per quadrats i sumeu-hi la potència publicada. Localitzeu i compareu el quadrat amb més registres i el de més potència.
2. Calculeu el centre dels registres i el centre ponderat amb `w_mid`. Expliqueu el desplaçament i distingiu pesos publicats de valors assignats per interval.
3. Dibuixeu el cercle i l'el·lipse sobre el centre no ponderat, amb els paràmetres de la guia. Identifiqueu un punt exterior i un espai interior amb pocs registres.
4. Calculeu dos mapes de calor sense pes, amb radis de 500 i 1.500 m i píxel de 100 m. Normalitzeu-los a registres/km², conserveu NoData i compareu-los amb la mateixa escala de color.

**Ampliacions per aspirar a l'excel·lent.** Podeu canviar la mida o l'origen de la malla, comparar escenaris de pesos per als intervals sense xifra, provar altres radis i mides de píxel, o treballar un altre municipi amb dades adequades. Manteniu una referència, canvieu un paràmetre cada vegada i conserveu els valors publicats. Justifiqueu què canvia i què persisteix. Si canvieu de conjunt, recalculeu centres i dispersió; no reutilitzeu les constants de Constantí.

**Preguntes obertes i aplicacions.** Coincideixen els llocs amb més registres i els de més potència? Quina influència tenen els pesos grans o els valors absents? Quines dades addicionals sobre edificis, habitants o activitats ajudarien a interpretar una concentració? Desenvolupeu una idea de diagnosi territorial o comparació municipal i distingiu el que mostren els resums del que caldria investigar.

**Informe.** Presenteu pregunta i àmbit, dades i decisions, procediment amb controls, mapes i taules dels apartats seleccionats, i interpretació amb límits. Podeu enregistrar fragments de la pantalla i després pausar el vídeo per desar captures dels paràmetres o resultats importants. Comproveu que es llegeixen, numereu-les i expliqueu què demostra cadascuna; exporteu els mapes finals amb llegenda, escala i unitats. El vídeo és una ajuda, no un lliurament obligatori tret que el professor ho indiqui. La guia detalla com preparar l'informe.

**Lliurament.** Entregueu `estadistica-constanti-cognom.gpkg`, amb els vectors generats; `estadistica-constanti-cognom.qgz`, amb rutes relatives; els TIFF utilitzats; i `estadistica-constanti-cognom.pdf`, amb l'informe. Manteniu els fitxers referenciats pel projecte dins de la carpeta de treball. En una zona alternativa acordada amb el professor, identifiqueu el cas al nom dels fitxers i conserveu fonts i controls propis.

**Comprovacions.** Reviseu les sumes, les unitats, EPSG:25831/NONE, els centres, els paràmetres de dispersió i la normalització del kernel. Expliqueu què resumeix cada resultat: un contorn de dispersió no és una cobertura de servei i un pic de densitat no és un contrast estadístic. Comproveu que el projecte s'obre després de moure la carpeta completa.

**Qualificació.** El **70%** correspon als apartats obligatoris que indicarà el professor. Les ampliacions permeten aspirar a l'excel·lent segons els criteris comunicats a classe i recollits en aquesta tasca. Es valoren la pregunta, els controls i la interpretació, no només el nombre d'operacions. No substitueixen els obligatoris ni garanteixen una nota per haver-les intentat.

# Preparació i recorregut

La seqüència manté el mateix conjunt: **recompte → centres → dispersió → densitat**. El paquet d'inici conté les entrades; el docent hi afegeix els resultats descriptius i el projecte **docent**. Obre'l des de la connexió a `payload/data/estadistica-constanti-docent.gpkg`, conservant també el GeoPackage d'inici i els recursos locals.

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
| Centre dels registres | (349051,5269; 4557573,8792) m |
| Centre ponderat amb `w_mid` | (347321,2104; 4558177,0408) m |
| Desplaçament | 1.832,4298 m |
| Radi de dispersió | 2.000,6564 m |
| Semieixos de l'el·lipse | 1.934,4377 / 510,4672 m |
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
| Radi 500 m | 100 m | 124,00168 registres |
| Radi 1.500 m | 100 m | 124,00002 registres |

Table: Controls de massa dels ràsters normalitzats amb àrea de píxel de 0,01 km².

La normalització de Raw és $3\times10^6/(\pi h^2)$, amb h en metres. Utilitzar la mateixa escala de color i distingir radi de contribució, discretització i unitat. NoData es conserva; no s'interpreta com absència comprovada d'instal·lacions.

# Revisió del treball i fonts

El lliurament de l'estudiant ha de contenir resultats propis dels apartats anunciats, projecte relatiu, paràmetres i interpretació. Comprovar sumes, CRS/NONE, centre emprat en la dispersió, unitats del kernel i portabilitat segons la selecció de classe. La semblança amb el resultat docent no substitueix l'explicació de cada resum.

Per a les ampliacions, contrastar què s'ha mantingut i què s'ha canviat. Una altra malla altera l'agregació; un altre radi altera la contribució espacial; un pes assignat altera l'escenari, no l'observació publicada. En un altre municipi, els controls de Constantí no són resultats esperats. Valorar també l'aplicació geogràfica proposada i les dades que requeriria.

L'informe ha de respondre una pregunta amb taules i mapes comparables, captures comentades i límits. Les imatges extretes d'un enregistrament poden documentar decisions; ni la gravació completa ni una successió de finestres substitueixen l'explicació.

ICAEN: extracció del 28/9/2026, sense data efectiva establerta. ICGC: límit del 20/1/2026, ortofoto WMS 2025. [Localització ICAEN](https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/), [condicions ICGC](https://www.icgc.cat/condicions) i [QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/).

Moran, LISA i renda no formen part d'aquesta activitat. Es conserven en la preparació històrica per a un recorregut posterior.
