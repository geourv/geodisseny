---
title: "Pràctica: visibilitat de la torxa, la carretera i el recinte petroquímic"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
---

# Tres preguntes de visibilitat

Començarem amb una torxa industrial de la Canonja: **es veu des d'un punt de la carretera?** Després estudiarem el recorregut de la TV-3148 entre Vila-seca i l'enllaç de la Pineda: **quines posicions es veuen al llarg de la via?** Finalment ampliarem els objectius: **des d'on es veu alguna part del recinte petroquímic?**

El punt dona una resposta 0/1; la carretera suma observadors; el recinte resumeix objectius industrials. Les elevacions, altures i cobertura són comunes, però els nombres no representen la mateixa magnitud. Cap resultat mesura directament persones exposades ni impacte paisatgístic.

**El professor indicarà a classe quins apartats i exercicis són obligatoris dins del 70% de la qualificació**, i ho recollirà a la tasca de Moodle. Aquesta guia ofereix la progressió completa de punt, línia i àrea; la selecció de classe determina què s'ha de lliurar. Les ampliacions permeten aprofundir i aspirar a l'excel·lent, amb una pregunta i resultats justificats, sense substituir els obligatoris.

## Obrir el paquet

1. Descomprimeix el ZIP complet i conserva les carpetes. Utilitza **QGIS 3.44 LTR**, amb Processament i GDAL.
2. Al panell **Explorador**, crea una connexió a `payload/data/visibilitat-costa.gpkg`, desplega-la i obre el projecte **inici** guardat dins del GeoPackage.
3. Comprova **EPSG:25831**, unitats mètriques i el·lipsoide **Cap / NONE**.
4. Crea `treball/` al costat de `payload/` i desa-hi les teues sortides i una còpia del projecte. Conserva el paquet d'inici.

| Entrada | Què representa |
| --- | --- |
| `mdt` / `mds` | Terreny i superfície opaca, graella de 5 m |
| `domini` | Cobertura comparable: 1 o NoData |
| `torxa` | T, estructura identificada i cotes de model |
| `carretera` / `mostres_carretera` | Recorregut i 37 posicions de treball |
| `coberta_original` | Polígon MCSC 2024 abans de generalitzar |
| `receptors` | R1–R5 per consultar respostes |
| `ambit` / `ortofoto` | Extensió comuna i context local |

Table: Dades preparades per al recorregut de punt, línia i àrea.

La capa de mostres de carretera s'anomena `mostres_carretera` al GeoPackage. La font local DejaVu Sans de `payload/data/fonts/` és un recurs del projecte i s'ha de conservar amb el paquet.

![Torxa, carretera i sector industrial sobre l'ortofoto.](captures/visibilitat-costa-dades.png){width=100% height=380pt}

La graella comuna té **2.000 × 2.000 cel·les de 5 m**: X 342000–352000, Y 4549000–4559000. MDT i MDS provenen del LiDAR ICGC **2021–2023**. L'MDT és natiu de 5 m; l'MDS d'1 m s'ha agregat pel màxim a 5 m. El màxim pot eixamplar obstacles estrets i les capçades es tracten com a opaques.

L'ortofoto és un retall local WMS de l'ICGC 2025, amb petició de context de 10 m/píxel. La capa d'origen és de 25 cm: resolució del producte i del retall són diferents. El paquet funciona sense consultar el servei.

![MDS amb el mateix enquadrament i llegenda de cotes en metres.](captures/visibilitat-costa-mds.png){width=100% height=380pt}

El domini comparable té **3.490.455 cel·les**. Els buits del mar cartografiat s'han tractat a 0 m; els altres buits i les línies afectades per elevacions desconegudes queden fora del domini. **NoData no és ocultació.**

# A. Torxa i parelles de visió

## Cota de T

T correspon al node OSM **7682543312**, classificat com a torxa industrial i contrastat amb l'ortofoto. El punt original és (346894,824499; 4552508,353399) m. El càlcul utilitza el centre de cel·la **(346892,5; 4552507,5) m**, amb un desplaçament de 2,48 m.

| Magnitud | Metres |
| --- | ---: |
| MDT a T | 20,941999 |
| Pic MDS | 151,311996 |
| Diferència pic–terreny | 130,369997 |
| Cota T del model, pic +1 m | 152,311996 |
| Altura relativa sobre MDT | 131,369997 |
| Altura relativa sobre MDS | 1 |

Table: Cotes i altures utilitzades per a T.

Els aproximadament 130,4 m són una estimació d'estructura a partir del LiDAR. El metre addicional separa el punt de model de la superfície digital: **no mesura la flama**. Els atributs de `torxa` conserven les cotes.

![Torxa identificada al detall de l'ortofoto.](captures/visibilitat-costa-torxa.png){width=100% height=380pt}

## Conca sobre MDT

Obre **Procés → Caixa d'eines** o **Ctrl+Alt+T**. Cerca **Viewshed** i comprova el proveïdor GDAL.

1. Eina `gdal:viewshed`, entrada `MDT`, banda 1.
2. Observador: `346892.5,4552507.5 [EPSG:25831]`.
3. Altura d'observador **131.36999702453613 m**; altura de destinació **1,7 m**; distància màxima **0**, tota la finestra.
4. Opcions addicionals:

```text
-vv 1 -iv 0 -ov 255 -a_nodata 255 -cc 0.85714
```

5. Desa la conca crua a `treball/` i carrega-la com **Conca T MDT**.
6. Amb Calculadora ràster, `native:rastercalc`, aplica:

```text
"Domini@1" * "Conca T MDT@1"
```

7. Mantén extensió, 5 m i EPSG:25831; desa `T-mdt.tif`. Comprova 1 visible, 0 ocult i NoData separat.

![Configuració de Viewshed per a la torxa T sobre l'MDT; l'altura de l'observador és de 131,369997 m.](captures/visibilitat-costa-punt.png){width=95% height=380pt}

El control és **2.962.199 cel·les visibles**, **84,87%** del domini. Si Calculadora ràster canvia el codi de NoData, consulta la banda; no l'interpretes com zero.

## Comparar amb MDS i consultar receptors

1. Repeteix Viewshed amb MDS, mateix T i altura d'observador **1 m**. Altura de destinació 0, distància màxima 0.
2. Opcions: `-om DEM -cc 0.85714 -a_nodata -9999`. Desa la sortida Float64 com **Cota mínima MDS**.
3. El mode DEM retorna cota absoluta mínima i ignora l'altura de destinació. Mantén els receptors a **MDT +1,7 m**:

```text
"Domini@1" * (("MDT@1" + 1.7) >= "Cota mínima MDS@1")
```

4. Desa `T-mds.tif`. Control: **447.860 cel·les**, **12,83%** del domini.
5. Executa **Mostreja els valors ràster**, `native:rastersampling`, sobre `receptors`, amb prefixos diferents per a MDT i MDS.

| Receptor | Mostra de carretera | MDT | MDS |
| --- | --- | ---: | ---: |
| R1 | C05 | 1 | 1 |
| R2 | C11 | 0 | 0 |
| R3 | C13 | 1 | 0 |
| R4 | C37 | 1 | 0 |
| R5 | Fora del retall | Nul | Nul |

Table: Parelles de contrast sense moure els extrems entre superfícies.

![Parelles visibles i ocultes amb el mateix origen T.](captures/visibilitat-costa-intervisibilitat.png){width=100% height=380pt}

**Conserva:** els dos mapes, la cota mínima, el domini i la taula de parelles. Distingeix relleu, obstacle superficial i lloc no calculat.

# B. Conca acumulada de carretera

El recorregut fa **3.652,272633 m** i segueix una trajectòria única de la TV-3148 fins a l'enllaç amb la TV-3146. No suma les dues calçades com si foren una línia única de longitud doble ni modela sentits de circulació.

1. Amb **Punts al llarg de la geometria**, `native:pointsalonglines`, sobre `carretera`, usa distància **98.71007115541471 m**, inici **49.355035577707355 m** i final 0.
2. Comprova 37 punts. `mostres_carretera` conserva `x`, `y` als centres de cel·la, `pk_m` i `pes` en metres representats; la suma de pesos recupera la longitud.
3. Calcula individualment Viewshed sobre MDT per a C05, C11 i C13: ulls d'origen/destinació **1,7 m**, abast 0 i mateixes opcions i màscara.

![Configuració de Punts al llarg de la geometria: interval de 98,710071 m i desplaçament inicial de 49,355036 m sobre la TV-3148.](captures/visibilitat-costa-carretera.png){width=95% height=380pt}

## Lot gràfic i suma

Viewshed calcula un punt per execució. Per repetir les 37 posicions, posa **C** com a nom de `mostres_carretera`, obre l'eina com a procés per lots i emplena OBSERVER per expressió:

```text
aggregate(
  layer := 'C', aggregate := 'array_agg',
  expression := to_string("x") || ',' || to_string("y")
                || ' [EPSG:25831]',
  order_by := "id"
)
```

Comprova 37 files útils, de C01 a C37. Emplena cap avall MDT, banda 1, altures 1,7/1,7, abast 0 i opcions `-vv 1 -iv 0 -ov 255 -a_nodata 255 -cc 0.85714`. Tria **37 rutes úniques** en una carpeta nova de `treball/` i revisa el registre. El lot encara no suma ni emmascara.

Amb **Estadístiques de cel·la**, `native:cellstatistics`, suma els 37 ràsters: estadística Suma, C01 de referència, **Ignora NoData desactivat** i NoData 255. Sobre la suma crua aplica Domini. Representa el recompte de 0 a 37.

![Suma de posicions amb visió: màxim possible 37 i observat 33.](captures/visibilitat-costa-acumulada.png){width=100% height=380pt}

El control té **1.461.016 cel·les** amb alguna visió i màxim **33**. Un valor 12 representa **1.184,52 m** i **32,43%** del recorregut mostrejat. No sumes les hectàrees de les 37 conques.

## Carretera des d'on es veu T

Mostreja la conca T als punts C. Amb MDT, 34/37 són visibles: **3.356,14 m**, el **91,89%**. Amb MDS, 9 posicions queden sota la superfície opaca i es conserven com no calculades.

Per MDS, després del mostreig amb prefix `T_mds_`, crea un camp amb:

```text
CASE WHEN "calculable" = 1 THEN "T_mds_1" ELSE NULL END
```

Les 28 posicions compatibles representen **2.763,88 m**, el **75,68%** de cobertura. Entre elles, 7 són visibles i 21 ocultes: **690,97 m**, el **25% del subconjunt**, no el 25% de tota la carretera. Per al contrast MDT/MDS usa les mateixes 28 posicions; la suma MDT de 37 és un altre resultat.

**Conserva:** mostres, suma, percentatge i taula de cobertura. Distingisca territori visible des de la carretera i carretera des d'on es veu T.

# C. Alguna part del recinte petroquímic

La font és el polígon MCSC 2024 **1459998**, categoria **347**, de **162,59 ha**, amb 19 forats. El sector pertany al Polígon Sud, a la Canonja; no representa tot el complex petroquímic de Tarragona ni la refineria del Polígon Nord.

1. Sobre `coberta_original`, executa `native:buffer`: **+150 m**, 32 segments per quadrant, unions arrodonides i dissolució.
2. Sobre l'intermedi anterior, executa un segon buffer **−150 m**, amb els mateixos altres paràmetres.
3. Comprova geometria vàlida, **222,94 ha** i cap forat. Dona-li el nom **Recinte petroquímic d'estudi** i contrasta'l amb l'ortofoto.

![Primer buffer positiu sobre la coberta original.](captures/visibilitat-costa-buffer-positiu.png){width=95% height=380pt}

![Buffer negatiu sobre l'intermedi positiu, no sobre l'original.](captures/visibilitat-costa-perimetre.png){width=95% height=380pt}

| Distància +n/−n | Àrea | Forats | Afegit exterior |
| --- | ---: | ---: | ---: |
| 50 m | 181,33 ha | 5 | 4,85 ha |
| 100 m | 199,97 ha | 2 | 15,52 ha |
| 150 m | 222,94 ha | 0 | 38,50 ha |
| 250 m | 224,49 ha | 0 | 40,04 ha |

Table: Alternatives de tancament amb els mateixos paràmetres d'arcs.

Les dues operacions no es cancel·len necessàriament: els entrants estrets poden desaparèixer. El recinte de 150 m incorpora 38,50 ha fora del contorn original; la discretització retira també uns 3,77 m² de vora. És una delimitació d'estudi, no un límit oficial nou.

## Mostrejar i comparar cotes

1. Crea una graella rectangular de **250 ×250 m**: X 345250–350000, Y 4551750–4552750, EPSG:25831.
2. Retalla-la amb el recinte, calcula `$area` amb NONE i obtín **un punt per fragment** amb `native:pointonsurface`.
3. Comprova **57 fragments** i suma **2.229.408,741960 m²**. Els pesos corresponen als fragments, no a quadrats complets.
4. Situa cada A **1 m sobre l'MDS local**. Mantén aquella cota absoluta en els dos models: `h_mdt_m` sobre MDT i `h_mds_m` sobre MDS.
5. Repeteix les conques per lots, compara cotes amb MDT +1,7 m en el mode DEM, aplica Domini i acumula. Són 57 execucions per superfície.

![Configuració d'una graella de 250 × 250 m abans de retallar-la amb el recinte petroquímic d'estudi.](captures/visibilitat-costa-area.png){width=95% height=380pt}

## Afegir T i interpretar els pesos

La suma de les 57 respostes A compta mostres visibles. Per preguntar si es veu **alguna part**, afegeix la torxa singular T, que una graella pot passar per alt:

```text
("Nombre A@1" > 0) OR ("Torxa T@1" = 1)
```

Control MDS: **470.444 cel·les**, **13,48%** del domini. MDT: **2.977.704**, **85,31%**. Conserva NoData.

![Mapa que inclou alguna mostra d'àrea o la torxa T.](captures/visibilitat-costa-poligon.png){width=100% height=380pt}

La fracció d'àrea és $100\sum_i w_iV_i/\sum_iw_i$, amb pesos en m². **T no rep un pes superficial inventat**. Als receptors, R1 dona T=1, alguna part=1 i A=0% amb MDS: es veu la torxa però cap de les 57 mostres d'àrea.

**Conserva:** fragments, mostres, pesos, recompte, mapa d'alguna part i percentatge ponderat. La conclusió ha d'identificar què es veu, des d'on, altures, superfície i cobertura de dades.

# Ampliacions, preguntes obertes i aplicacions

Escull una pregunta que vagi més enllà de repetir el recorregut seleccionat. Mantén una referència, registra els paràmetres i explica què canvia. No cal fer totes les propostes:

- **Altures i receptors.** Compara altres altures de model o receptors adequats. En quin cas canvia la resposta visible/ocult? Declara la cota absoluta de cada extrem per no confondre un canvi de superfície amb un canvi de receptor.
- **Densitat del mostreig.** Repeteix un recorregut amb més o menys posicions, o desplaça la graella de l'àrea. Es mantenen els llocs destacats? Compara pesos i cobertura, no només el nombre de mostres visibles.
- **Delimitació i objectius.** Prova altres distàncies de tancament +n/−n o compara objectius singulars i d'àrea. Quina superfície s'afegeix? Pot una graella ometre una estructura alta com T?
- **Un altre lloc.** D'acord amb el professor, aplica el mètode a un mirador, un itinerari o un altre objectiu amb elevacions adequades. Recalcula altures, domini i controls; els percentatges del cas de la Canonja no són valors esperats per al nou lloc.

Una aplicació geogràfica pot ser comparar visió geomètrica des d'un itinerari o ajudar a seleccionar punts per a una observació de paisatge. Què caldria observar al camp? Quines dades permetrien relacionar la visió amb usos, freqüentació o percepció? Explica què aporta el càlcul i què falta per estudiar exposició o impacte, sense atribuir-los directament a la conca visual.

Les repeticions han de respondre una pregunta de sensibilitat. Canvia un paràmetre cada vegada, mantén la resta i conserva també resultats que no confirmin la primera idea.

# Preparar l'informe

Organitza el PDF perquè cada resultat respongui una pregunta:

1. **Pregunta i selecció de classe.** Situa l'objectiu, els receptors i els apartats obligatoris anunciats pel professor. Identifica l'ampliació, si en fas una.
2. **Dades i decisions.** Explica MDT/MDS, dates, resolució, altures absolutes i relatives, domini i mostreig. Justifica la delimitació d'estudi quan sigui pertinent.
3. **Procediment i controls.** Mostra els paràmetres que condicionen les conques, el lot, la màscara i l'acumulació dels apartats seleccionats. Distingueix una execució individual del conjunt de repeticions.
4. **Resultats comparables.** Inclou mapes amb llegenda i el mateix enquadrament, i una taula amb unitats, cobertura i denominadors. Separa visible, ocult i no calculat.
5. **Interpretació i límits.** Explica què es veu i des d'on, i diferencia resposta binària, recompte i fracció ponderada. Identifica què no informa sobre persones o impacte paisatgístic.
6. **Ampliació i aplicació.** Compara les repeticions amb la referència i proposa una aplicació geogràfica o una observació que permeti contrastar-la.

## Enregistrar la pantalla i extreure captures

Pots enregistrar fragments de la sessió amb un enregistrador de pantalla, com OBS Studio. Fes una prova breu amb la finestra de QGIS i comprova que es llegeixen altures, coordenades i opcions. Documenta una configuració individual, la preparació del lot i els controls que corresponguin a la selecció de classe; anota els moments útils del vídeo.

Després, pausa'l en un reproductor i desa els fotogrames amb la funció de captura de fotograma. Retalla només les zones irrellevants, conserva el context dels paràmetres i afegeix número i peu explicatiu. Exporta els mapes finals amb llegenda, escala i unitats. Una captura d'un diàleg mostra la configuració; una de mapa mostra la representació. Relaciona-les amb controls numèrics del resultat.

No cal lliurar el vídeo tret que el professor ho indiqui. Selecciona les evidències que ajudin a seguir el raonament; l'informe no necessita tots els fotogrames ni una explicació de cada clic.

# Lliurament, fonts i portabilitat

Lliura `visibilitat-costa-cognom.gpkg`, amb els vectors generats; `visibilitat-costa-cognom.qgz`, amb rutes relatives; els TIFF referenciats; i `visibilitat-costa-cognom.pdf`, amb l'informe dels apartats seleccionats. Mantén els fitxers requerits dins de la carpeta de treball i comprova l'obertura després de moure-la completa.

El **70%** correspon als apartats obligatoris que indicarà el professor. Les ampliacions permeten aspirar a l'excel·lent segons els criteris comunicats a classe i recollits a Moodle; no substitueixen els obligatoris ni garanteixen una nota per haver-les intentat. En una zona alternativa, identifica el cas al nom dels fitxers i conserva les fonts i els controls propis.

- [ICGC, elevacions](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions): LiDAR 2021–2023, MDT 5 m i MDS 1 m agregat pel màxim.
- [Mapa de cobertes ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya), edició 2024, i [RTT](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial), edició 2024.
- Ortofoto ICGC 2025 i [condicions d'ús](https://www.icgc.cat/condicions).
- [OpenStreetMap](https://www.openstreetmap.org/copyright): node de torxa 7682543312, versió 1.
- [QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/), [processament per lots](https://docs.qgis.org/3.44/en/docs/user_manual/processing/batch.html) i [GDAL Viewshed](https://gdal.org/en/stable/programs/gdal_viewshed.html).
- Farnós Marsal, J. (2025). [La indústria petroquímica de Tarragona](https://publicacions.iec.cat/repository/pdf/00000528/00000061.pdf): polígons Nord/Sud, port i conduccions.

El GeoPackage prepara entrades locals; les sortides de l'activitat s'han de calcular. Conserva recursos i projecte amb rutes relatives. Comprova el treball des d'una altra carpeta, sense serveis en línia. Una visió calculada no substitueix observacions de camp ni un estudi de percepció o impacte.
