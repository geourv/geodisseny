# Pràctiques territorials: dades, controls i reproducció

Preparacions locals del 29 de setembre al 4 d'octubre de 2026. Els ZIP es lliuren per Moodle;
no formen part dels assets del web. Les instruccions conceptuals i els passos
QGIS són als capítols de connectivitat, visibilitat, estadística descriptiva i
autocorrelació. Cal mantenir còpies originals de les dades en treballar-hi.

## Paquets

- Suplement municipal amb imputació explícita:
  `practica-punts-municipals-20261004.zip`,15.255.627bytes,30fitxers,
  SHA `b7ed57dc62db492c8dfd620449eb8dfa4f652a8efbd3096cc976e5f4247f767f`.
  Un projecte de8capes,672registres de tres municipis, tres escenaris,
  ortofoto local,5captures,3figures i controls. Punt mitjà com a convenció
  docent i comparació amb límits. Comprovat offline/readonly i segellat
  localment; no pujat a Moodle. Fonts a `context/dades/escenaris_potencia.py`.

- Punts del Tarragonès, nova pràctica de C4:
  `practica-punts-tarragones-20261004.zip`,13.853.420bytes,82fitxers,
  SHA `ee421cdc2ff89db787ea13ea7f032930cf5ae4c66da850c42bca8944cc9bebf7`.
  Sis projectes de18capes,14captures, GUIA14p/SOLUCIONS2p. Centres, dispersió,
  graella, kernels amb/sense pes i seccions. Connexions GeoPackage visibles,
  càlculs contrastats i portabilitat readonly/offline. Segellat localment;
  sense pujada a Moodle. Detall a `context/dades/punts-tarragones.md`.

- Revisió costa r3, recinte compacte, lots i ortofoto/MDS:
  `practica-visibilitat-costa-20261002-r3.zip`,161.155.091bytes,250fitxers,
  SHA `b7f2c5f38c8ee45cca592ce35db4aaeac77a413f6ace210948e47e338c3369cc`.
  Deu projectes,37capes,17captures,5SVG; GUIA26p i SOLUCIONS3p. Recinte
  petroquímic de222,94ha amb buffers +150/−150m. Inclou el lot executable
  des de QGIS, amb179execucions contrastades contra els controls.
  CRC/hashes i portabilitat verificats. Versió activa per a revisió:
  `context/dades/visibilitat-costa-r3.md`.

- Revisió costa r2 anterior, perímetre i accessos a eines:
  `practica-visibilitat-costa-20261002-r2.zip`,149.293.723bytes,231fitxers,
  SHA `afbce1dfcf05f300bb39e442c79a18da08bbcbe003765fa4ba5bb919bf165501`.
  Deu projectes,36capes,12captures,5SVG; GUIA19p i SOLUCIONS3p. Perímetre
  sense forats de184,44ha, font original i alternatives conservades.
  CRC/hashes i portabilitat QGIS verificats. Detalls i fonts històriques a
  `context/dades/visibilitat-costa-r2.md`; lliurament anterior conservat.

- Versió costa anterior: torxa de la Canonja → TV-3148 → àrea del
  MCSC2024. Preparació a `tmp/dades-docents/qgis/visibilitat-costa-20261002/`,
  font `context/dades/preparar_visibilitat_costa.py` i controls documentats
  a `context/dades/visibilitat-costa.md`. Nou projectes de34capes,37conques
  MDT de carretera i57mostres d'àrea més la torxa. Distribució per Moodle;
  dades i intermedis fora de Git.
  ZIP `practica-visibilitat-costa-20261002.zip`,149.167.797bytes,211fitxers,
  SHA `a5130ad5221a21e8e86350c485731c4384b44c720f1ce3a879815d65577946c1`.
  Guió16p i notes3p, CRC i hashes correctes; paquet segellat sense pujada.

- `practica-visibilitat-nord-20261001.zip`:152fitxers,119.669.778bytes; SHA-256
  `f760e14effcb88d51858d24a7d8c2261c1de0d9b206e510e465be7ac25bf0520`.
  Nou projectes,32capes,9captures i4figures; guió14p i notes3p. Punt interior,
  perímetre i àrea d'un sector cadastral de la refineria nord, amb MDT/MDS5m i
  extrems absoluts fixats. Verificació QGIS offline/readonly, càlculs natius,
  CRC i hashes correctes. Versió substituïda a petició de l'autor; les fonts
  no versionades del bundle s'han arxivat privadament, amb comprovació contra
  el ZIP. Detalls a `context/dades/visibilitat-nord.md`.

- `practica-distancies-vilaseca-20261001-ampliada.zip`: 307 fitxers,
  69.936.621 bytes; SHA-256
  `4c17e38e9d537838818568fea114b05304cf900aa7f7b9cbf6974452d0f164d3`.
  Versió ampliada amb 77 capes, 15 projectes, 21 captures, quatre SVG nous,
  GUIA de 38 pàgines i SOLUCIONS de 5 pàgines. Inclou tot el paquet inicial
  més els models r.walk i les isòcrones. CRC i hashes de tots els membres
  comprovats; el ZIP inicial es conserva amb el seu hash original.

- `practica-distancies-vilaseca-20261001.zip`: 168 fitxers, 56.236.454 bytes;
  SHA-256 `0a7ac7c331212ada3d1a0f2d2f728cb9c0513d4ca6e9ff6bedc87471f72bf2d5`.
  Pràctica autònoma amb 48 capes, 10 projectes QGIS relatius, 15 captures,
  guió d'alumnat de 24 pàgines i solucions de 4 pàgines. Inclou fonts,
  resultats, estils i controls. CRC, hashes de tots els membres i integritat
  SQLite correctes; projectes oberts offline des d'una ubicació independent.
  Rebut: `tmp/dades-docents/practica-distancies-vilaseca-20261001.receipt.json`.
  Paquet segellat localment, pendent de revisió de l'autor; no pujat a Moodle.

- `demos-ampliacio-20260930.zip`: 94 fitxers, 34.195.177 bytes; SHA-256
  `7f387cabca8dee8432a66ea287e5fed75da8191137dc875684ddaffc876eacc5`.
  Entrades i resultats QGIS, models de 28 mostres, temperatures XEMA originals
  i agregades, prediccions finals, controls i instruccions. CRC, tots els hashes
  i integritat SQLite comprovats; GeoPackage autònoms amb journal DELETE.
  Complementa els paquets originals següents, que es conserven sense canvis.

- `demos-practiques-territorials-20260929.zip`: extracte RTT sense adaptació
  d'atributs/topologia, límits, MDT/MDS, parcel·les, ortofotos de contrast i
  resultats de les proves de xarxa, fricció i visibilitat.
- `demos-seccions-autoconsum-20260929.zip`: seccions completes amb atributs
  agregats, fonts censals/cadastrals emprades, ICAEN, centres i taula de resultats.

Cada arxiu conté `MANIFEST.json`, amb paths del paquet, font al projecte,
SHA-256 i mida. El manifest de fonts conserva URLs, edicions i transformacions.
Els preparadors generals de `reproduccio/` esperen l'estructura del repositori
geodisseny i les seves rutes privades; no són un instal·lador autònom del
programari. Les activitats QGIS es poden fer obrint directament les dades.
El nou `lots_visibilitat.py` sí que reexecuta els lots dins de QGIS amb el
paquet de visibilitat, sense el repositori font; el guió n'explica l'ús.

## Ampliació: marxa anisòtropa i isòcrones

Font: `context/dades/preparar_accessibilitat.py`. Destinació privada:
`tmp/dades-docents/qgis/distancies-vilaseca-20261001-ampliada/`.
El preparador parteix del ZIP inicial verificat. Fases `--init`, `--build`,
`--style`, `--figure-inputs`, `--docs`, `--sqlite` i `--package`; càlcul i
estils en processos QGIS separats. La compilació dels guions precedeix el segellat.

- QGIS 3.44.11 exposa `grass:r.walk.points`, `.coords` i `.rast`; no un
  identificador genèric `grass:r.walk`. MDT en metres, fricció temporal
  0 s/m als camins i 0,5 s/m a la resta; lambda1, vuit veïns, nuls exclosos.
  No multiplicar aquesta fricció per la mida de cel·la.
- Coeficients 0,72 / 6 / 1,9998 / −1,9998, llindar −0,2125 m/m. Prova en
  rampa aïllada de 100 m i 10 m de desnivell: 132 s amunt, 52,002 s avall.
- O/D al mateix lloc de la pràctica; altituds 50,887 / 52,249 m. Els costos
  incorporen els desnivells intermedis. Possible simplificació del pas inferior
  al MDT de 5 m explícita al guió; no hi ha calibració amb temps observats.

| Escenari | Segons | Minuts | Longitud, m |
| --- | ---: | ---: | ---: |
| MDT obert, O→D | 397,830737 | 6,630512 | 466,482323 |
| MDT obert, D→O | 389,007040 | 6,483451 | 466,482323 |
| MDT tancat, O→D | 1049,163737 | 17,486062 | 1071,457070 |
| Pla obert, qualsevol sentit | 338,367272 | 5,639455 | 466,482323 |

Els cinc càlculs concorden amb Dijkstra independent, tolerància0,05 s.
Les geometries d'anada/tornada no són exactament iguals, tot i tenir la mateixa
longitud. No invertir només la línia: recalcular r.walk amb l'altre origen.

Isòcrones inclusives de 3/6/12 min: 1.624 / 7.481 / 36.777 cel·les obertes i
1.434 / 4.764 / 22.155 tancades. Fins a12min: 91,9425 / 55,3875 ha. Cap franja
arriba al límit del retall. r.contour rep minuts i nivells3,6,12, amb `cut=3`
per descartar línies degenerades. El recompte d'àrea es fa sobre el ràster.

Controls de portabilitat ampliats: 15 projectes oberts readonly a `/paquet`,
sense xarxa ni repositori font. 159 fitxers de dades/estils/projectes amb SHA
en el report. Expressions de la Calculadora ràster executades i comparades:
fricció0/0,5 i classes1–4 idèntiques als controls, incloent les màscares NoData.
Comprovat també l'estil pseudocolor dels ràsters d'isòcrones als projectes.

Incidències de preparació resoltes:

- GRASS requereix `outdir` en aquest wrapper. Els GeoPackage amb taules d'estil
  es passen amb `|layername=origen` o `desti` per importar només la capa espacial.
- r.contour amb `cut=0` generava elements puntuals que fallaven en netejar la
  topologia; mínim3punts conserva els nivells requerits i les àrees ràster.
- No compartir basename QML entre ràster i vector: els contorns es diuen
  `isocrones-contorns-*.gpkg` i les classes `isocrones-marxa-*.tif`.
- r.out.gdal emet el diagnòstic de taula de colors no suportada en TIFF float;
  els ràsters numèrics, NoData i georeferenciació s'han comprovat independentment.

Guions ampliats: GUIA38p, SHA
`d148d240d693a2b744fac491454de59404abd3f69adaab4752fc5248fe890192`;
SOLUCIONS5p, SHA `0c74bad2808d45984c88c562e8573591d0323838fbbe44a82d7fadd6e71c6a2e`.
Compilació amb Pandoc/XeLaTeX i rsvg-convert del runtime PDF fixat; configuració
de composició a `controls/handouts.json`. Les capacitats públiques0.5.0 exposen
el PDF del manual, sense una plantilla específica de guions identificada.
Els guions utilitzen la configuració pròpia declarada, no una plantilla de
pràctiques atribuïda al nucli. Límits i pàgines amb figures revisats.

## Distàncies a Vila-seca — preparació inicial de l'1 d'octubre de 2026

Font executable: `context/dades/preparar_distancies.py`. Destinació privada:
`tmp/dades-docents/qgis/distancies-vilaseca-20261001/`; lliurament curat a
`lliurament/`, arrel interna del ZIP `distancies-vilaseca/`.
Guions editables: `context/practiques/distancies-vilaseca.md` i
`context/practiques/distancies-vilaseca-docent.md`.

### Fonts i geometria

- Ortofoto ICGC 2025, capa WMS `ortofoto_25cm_color_2025`, còpia de 1 m/píxel.
  MDT LiDAR 2021–2023, retall natiu de 5 m. Edificis del Cadastre de Vila-seca
  i eixos RTT 2024; URLs, edicions, transformacions i hashes a `fonts/fonts.json`.
- EPSG:25831, el·lipsoide NONE; extensió X 343600–345300, Y 4553000–4554700.
  Graella comuna de 340 × 340 cel·les de 5 m.
- O=(344407,00;4553668,36) m, D=(344473,01;4554030,72) m. P2 correspon al tram
  `rtt_id=1354754` del Camí del Mas de la Plana, sota l'AP-7. Tancament i
  reobertura són escenaris del model, no una intervenció anunciada.
- Xarxa preparada de 189 parts: sense autopista, amb contactes extrem–interior
  documentats, tolerància de preparació màxima de 5 mm i coordenades al mm.
  No es tallen indiscriminadament tots els creuaments. L'extracte original
  conservat a `fonts/rtt-vilaseca.gpkg` no incorpora aquesta preparació.

### Controls de càlcul

| Model | P2 obert | P2 tancat | Unitat |
| --- | ---: | ---: | --- |
| Euclidiana vectorial | 368,323349 | 368,323349 | m |
| Euclidiana ràster | 370,742493 | 370,742493 | m entre centres de cel·la |
| Ruta per la xarxa | 454,104650 | Sense ruta | m |
| Temps a 5 km/h | 5,449256 | Sense ruta | min |
| Camí ràster | 470,624458 | 1135,807358 | m |
| Cost ràster a D | 470,624458 | 2217,680733 | m ponderats |

- `native:shortestline` comprovat amb Pitàgores. O rasteritzat a 1, fons 0
  vàlid; `gdal:proximity` en unitats georeferenciades, no píxels. Centres:
  O=(344407,5;4553667,5), D=(344472,5;4554032,5) m.
- `native:shortestpathpointtopoint`: tolerància topològica 0 m i punt–xarxa
  0,1 m. El tancament deixa O sense connexió amb D en el graf seleccionat;
  l'absència de ruta es conserva com a null, mai com a 0 m.
- Àrees de servei: `TRAVEL_COST2` en hores, comprovat en una línia de 1.000 m
  a 6 km/h. 3/6/12 min = 0,05/0,10/0,20 h. Longitud única de branques:
  448,384607 / 1116,560723 / 3606,611447 m; 6 min amb P2 tancat: 68,418647 m.
  No sumar segments coincidents ni confondre suma de branques amb un trajecte.
- Fricció 1 als camins i 4 a la resta admesa; autopista i edificis NoData.
  Buffers de camí/autopista: 5/25 m. Corredors de 20 m, prolongats 40 m.
  Són hipòtesis docents; el terreny de fricció 4 explica l'alternativa ràster
  quan la xarxa tancada no dona ruta.
- `grass:r.cost` rep fricció × 5, vuit veïns, sense moviment de cavall i nuls
  exclosos. Cost i direccions desats; `grass:r.path` rep les direccions en graus
  i D per reconstruir el retorn a O. Dijkstra independent concordant a 0,02.
  Cel·les accessibles: 103.115 obertes / 103.062 tancades.
- L'MDT no intervé en aquesta fricció. Pendent i Pineda són ampliacions;
  el model anterior de la Pineda conserva friccions 1/20 i longituds
  608,284271 / 724,264069 m. Penalització finita no equival a barrera.

### Portabilitat, guions i segellat

- Projectes `00-inici` a `09-pineda-cost`: carregats amb QGIS 3.44.11,
  només el paquet muntat readonly a `/paquet`, xarxa desactivada i repositori
  font no muntat. Totes les capes vàlides i cap datasource fora del paquet.
- Reports al ZIP: `controls/verificacio-qgis.json`, `portabilitat.json`,
  `resultats.json`, `resultats.csv`, `verificacio-pdf.json` i `handouts.json`.
- `GUIA.pdf`: 24 pàgines A4 horitzontal, 10.307.039 bytes; `SOLUCIONS.pdf`:
  4 pàgines A4 vertical, 52.414 bytes. Pandoc 3.1.11.1 i XeLaTeX del runtime
  PDF fixat; paràmetres a `handouts.json`. Límits de text i pàgines seleccionades
  revisats. Els guions de context no són targets admesos per `prose-check`:
  s'han revisat manualment; el capítol sí que passa la comprovació automàtica.
- Preparació en fases: `--fetch`, `--build`, `--style`, `--stage`,
  `--refresh-docs`, compilació dels guions, verificació offline i `--package`.
  `--build` i `--style` requereixen processos QGIS separats. Fonts originals
  readonly i només la destinació generada RW. El ZIP existent no se sobreescriu.
- `MANIFEST.json` verifica 167 membres; el manifest és el fitxer 168.
  Cap WAL/SHM; originals RTT, ICAEN i límits ICGC amb els hashes inicials.

## Xarxa ICGC — prova anterior de Vila-seca a Tarragona

1. Obrir `fonts/rtt-original.gpkg`, capa `_35_transports_l`, en EPSG:25831.
   Són 10.759 eixos seleccionats per tipus i finestra, amb geometries, atributs
   i identificadors del producte RTT 2024. No és tot el GeoPackage de Catalunya.
2. Llegir les taules `transports_*`; per a la prova seleccionar `tipus` en
   `vcu`, `vpu`, `aut`, `vpd`, `vnc`, `vcd`: 4.512 eixos. Exportar una còpia.
3. Afegir `sentit` de text, inicialment B, i `v_kmh` decimal, inicialment 30.
   Són hipòtesis de l'experiment. El fitxer original no conté un règim complet
   de circulació ni ha estat adaptat com a xarxa de navegació.
4. A `native:shortestpathpointtopoint`, mesura plana (el·lipsoide NONE),
   tolerància topològica 0, extrems (344141.54,4553070.82) i
   (353180.77,4553971.06), ajust màxim 100 m. Configurar F/R/B per a sentit.
   Control de ruta curta: 10989.256959 m.
5. Canviar només `id=1331675` a R: 11012.833919 m. Restituir B; canviar-ne
   només la velocitat a 3 i executar «Més ràpid» amb `SPEED_FIELD=v_kmh`:
   11012.833919 m i 0.367094464 h. La còpia de treball conservada correspon
   a aquest últim escenari; restablir 30 per reconstruir el cas base.
6. Examinar `resultats/xarxa-controls.json`: els primers extrems més pròxims
   no eren al mateix component. Els punts finals són accessos a la xarxa
   principal, no centres municipals. Dos altres canvis de sentit provats
   deixaven l'origen sense ruta. Conservar les absències de ruta com a resultat.

El motor natiu no interpreta taules de girs ni costos arbitraris. El camp de
velocitat és en km/h, no en minuts. Per estudiar girs cal un motor compatible
o un graf ampliat. No afirmar que aquesta prova els ha executat.

## Solar de la Pineda

- Parcel·la `7713904CF4571D`, 87112.330539 m²; geometria cadastral i contrast
  visual amb ortofoto ICGC 2025. El polígon no acredita drets de pas.
- Obrir `resultats/solar-pineda.gpkg`, `extrems-pineda.gpkg`, les dues friccions
  i `fonts/mdt-solar-pineda-5m.tif`. Graella 170 × 134 a 5 m.
- Extensió: x 347200–348050, y 4550750–4551420; centres de cel·la per als camins.
- Extrems sol·licitats: O=(347300,4551050), D=(347900,4551030).
- Cost isotrop: distància del moviment × mitjana de friccions, vuit veïns.
  Fricció uniforme 1: 608.284271 m i 234.916351 m dins del polígon.
  Fricció interior 20, exterior 1: 724.264069 m i 0 m dins del polígon.
- `cost-*.tif` conté costos acumulats en metres ponderats; el petit arrodoniment
  Float32 és inferior a un mil·límetre en aquests controls.
- No hi intervenen pendent, vegetació ni tanques. Afegir-los és un model nou.
  Per obtenir minuts cal un model de marxa amb unitats, no reetiquetar el cost.

## Refineria nord: primera execució, conservada al paquet de 20260929

- Parcel·la `1406801CF5610C`, 1716263.871903 m², sector de la refineria a la
  Pobla de Mafumet; no representa tot el complex petroquímic de Tarragona.
- `fonts/mdt-regional-25m.tif` i `mds-regional-25m.tif`: derivats alineats de
  l'MDT LiDAR 5 m i l'MDS LiDAR 1 m 2021–2023. Mida 2560 × 1960;
  extensió x 311000–375000, y 4532000–4581000; EPSG:25831, NoData −9999.
  La mitjana i les piràmides del productor redueixen detall; 25 m no resol torres.
- Obrir `resultats/sector-petroquimic.gpkg` i `objectius-petroquimica.gpkg`.
  Centre i quatre mostres interiors d'una malla de 500 m. Altures de 30/60 m
  i receptors de 1,7/15 m assumides, no mesurades.
- Controls executats sobre MDT amb GDAL 3.10.3, mode edge, coeficient 0.85714,
  distància màxima 0 (finestra completa). Retorn binari 0/1 o suma 0–4;
  NoData de sortida 255. No interpolar aquests codis com si fossin altures.
- Mar fora de la màscara terrestre a 0 m com a supòsit. Hi ha 1791 cel·les
  terrestres sense elevació. S'exclouen també les línies potencialment afectades,
  amb entorn 3×3 i 16384 sectors angulars conservadors; 49049 cel·les addicionals.
- Mateix domini final: 1577539 cel·les. Visibles: centre 30 m / receptor 1,7 m,
  248127; almenys una mostra, 288108; centre 60 m, 372698; receptor 15 m, 498367.
- L'MDS és una entrada de contrast, no la superfície dels controls anteriors.
  Cal conservar les cotes absolutes dels extrems en comparar-lo amb l'MDT.

### Execució històrica del primer manual publicat: 28 mostres

`preparar_practiques.py --models --sample-spacing 250 --models-dir models-20260930`.
Mateixos inputs, 28 punts interiors i centre; domini comú d'1.570.262 cel·les.
Es descarten 56.326 cel·les addicionals per línies potencialment afectades pels
buits d'elevació. Visibles: centre30/receptor1,7, 247.343 (15,8%); almenys una
mostra, 310.200 (19,8%); centre60, 371.205 (23,6%); receptor15, 497.044 (31,7%).
`context/inputs/practiques-mapes.json` i el paquet nou corresponen a aquesta
execució; no atribuir els controls antics als mapes actuals.

## Centres, dispersió i densitat

3.762 punts ICAEN, mateix subconjunt per comparar amb/sense pes. Sense pes:
distància estàndard 8698,204203 m; semieixos 8152,141105 i 3033,373000 m;
orientació 12,327263° des de l'est, azimut QGIS 77,672737°. Convenció poblacional,
semieixos arrel dels autovalors. Expressions i covariància a controls/.
Graella d'1 km²: suma de n_punts = 3762. KDE quartic cru, radis 500/1500 m,
píxel 100 m; normalització 3e6/(pi*r²) per obtenir punts/km². Integral discreta
comprovada a menys del 3% del recompte; retall visual no és correcció de vora.

## XEMA i interpolació

Productor: Meteocat; conjunts nzvn-apee, yqwd-vj5e i 4fb2-n3yi del portal
analisi.transparenciacatalunya.cat. Fonts, URL, bytes i hashes a fonts.json.
Variable40, temperatura màxima en °C, dia2025-08-15 en TU; data_lectura etiqueta
l'inici de l'interval, segons descripció de columna del productor. Dades V/SH,
48 intervals únics per estació; 8784 registres, 183 estacions inicials i 182
amb metadades admeses. UG exclosa per manca de correspondència. Rang17,6–42,6°C.

IDW qgis:idwinterpolation, p2; SAGA sagang:variogram amb 12 classes, 150km,
salt1 (executat: 12 files, camps Distance, Count, Variance...). Kriging
sagang:ordinarykriging, model a+b*x/100000, a2,79123 b19,5643 positius;
cerca global, tots els punts, sense log ni blocs, variància en °C².
Graella135×133, 2km, bbox260000,530000,4486000,4752000, EPSG25831. Alineació
comprovada amb IDW; màscara Catalunya, NoData−9999. Model final: kriging-ajustat*,
variancia-ajustada*, saga-ajustat-log.txt. Els intents previs no entren al ZIP.
Sense validació fora de mostra: els mapes no acrediten superioritat predictiva.
Llicència declarada SEE_TERMS_OF_USE amb avís legal Meteocat, no CC BY atribuït.

Columbus: 49 barris de libpysal, CRIME per1000llars; I0,5001885572, p0,0001,
9999permutacions, llavor20260930. Coordenades arbitràries, no CRS mètric.
GUI censal: LISA nominal unilateral0,05 i Gi* bilateral0,05 sense correcció
múltiple. Gi*: 7 altes,13baixes,130no destacades; no confondre amb BH-FDR.

## Seccions censals i autoconsum

- `seccions-analisi.gpkg` conserva les 151 geometries completes de 2024 i els
  atributs agregats. El GeoJSON de dibuix està simplificat i no substitueix
  aquestes geometries per construir Queen. Clau estable: `cusec`.
- `pv_edifici_kw`: suma positiva coneguda ICAEN de categoria Edifici;
  `functional_n`: objectes cadastrals Building funcionals;
  `kw_per_100_buildings`: 100 × suma / recompte.
- `age_median_exact`: mediana de 2026 menys l'any, només quan `beginning` i
  `end` tenen el mateix any. El sufix exact és un nom intern; no acredita
  exactitud històrica. Any inicial/final correspon a unitats constructives.
- `association_sample`: almenys deu edificis d'any únic i una potència coneguda;
  `moran_sample`: indicador calculable. Els nuls no es converteixen en potència 0.
- `moran_z`, `moran_lag`, `moran_i`, `moran_p_sim`, `moran_quadrant`, `moran_fdr`
  i `neighbors` conserven resultats i correspondències.
- `seccions-resultats.json`: auditoria completa, versions, dates, fonts i sumes.
  Controls: Moran I=0.14404677, n=150, 9999 permutacions; r=−0.40095367, n=126.
- Les fonts cadastral i ICAEN tenen dates diferents de la partició censal.
  Els punts ICAEN representen consumidors associats, no petjades de panells.

## Reproducció al repositori

Runtime fixat: `sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc`.
Executar els preparadors des de l'arrel del checkout, amb les entrades originals
muntades de només lectura i només les destinacions generades com a escriptura.
QGIS pot canviar capçaleres SQLite en obrir un GeoPackage amb permisos d'escriptura.

```bash
python3 context/dades/preparar_practiques.py --fetch --only rasters
python3 context/dades/preparar_practiques.py --fetch --only roads
python3 context/dades/preparar_practiques.py --fetch-detail
# Les execucions següents es fan sense xarxa:
python3 context/dades/preparar_practiques.py --models
python3 context/dades/preparar_practiques.py --network-model
python3 context/dades/preparar_seccions.py --analyse
```

Les descàrregues amb manifest comproven hashes. Els models ràster admeten represa
només si les sortides existents coincideixen; els resultats de xarxa i captures
exigeixen destinacions noves. Les entrades incompletes o exploratòries descartades
no entren als ZIP. La publicació del web i la càrrega a Moodle són accions separades.
