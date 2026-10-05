# Visibilitat costa r3: recinte compacte, eines obertes, lots i dades inicials

Revisió de la mateixa incidència5 i branca `content/5-visibilitat-mdt-mds`.
Respon a quatre indicacions de l'autor: nom territorial del recinte,
tancament amb buffers, caixa d'eines i menús realment oberts amb requadres,
automatització explícita i presentació inicial d'ortofoto/MDS.
Capítol3 i bibliografia continuen en draft, sense aprovació de publicació.

Fonts: `context/dades/preparar_visibilitat_costa.py` i el nou guió executable
`context/dades/lots_visibilitat.py`. Destinació privada:
`tmp/dades-docents/qgis/visibilitat-costa-20261002-r3/`.
S'han copiat17fonts verificades del ZIP r2, sense obrir els GeoPackage anteriors.
El ZIP r2 conserva SHA
`afbce1dfcf05f300bb39e442c79a18da08bbcbe003765fa4ba5bb919bf165501`;
v1 conserva `a5130ad5221a21e8e86350c485731c4384b44c720f1ce3a879815d65577946c1`.

## Ajust editorial posterior: 3 d'octubre de 2026

El manual adopta títols que identifiquen els casos d'aplicació: visibilitat
puntual de la torxa de la Canonja, carretera Vila-seca–la Pineda i recinte
petroquímic. També s'han concretat quatre subtítols, preservant els ancoratges.
El criteri de connexions GeoPackage desplegades a l'Explorador queda registrat
per a les captures futures; l'autor permet ajornar la regeneració actual.

Aquest ajust no modifica el paquet r3 segellat descrit més avall. El PDF del
manual continua amb219p, amb nou SHA
`441bb4e6c2cb5b47bb57ab84493c039e8af28c925229bfb3310164ad12a1f6df`
i rebut preview `8c66bd43a008b18d6ab960bb0847176481f1f2d9321927ac300b2612c4e6322e`.
Títols comprovats al web1440/390px i al PDF, sense errors ni desbordaments.
Review copy de C3 `visibilitat-titols-copia-20261003`, revisió27, digest
`52fcbc367827be6348405edd26ed900c28c3ebfa99702a8b686b0d18f3bdac19`.
Cap troballa nova ni aprovació humana. Registre de la passada a
`context/revisio-manual-2026-09-28.md`.

## Geometria escollida

Nom visible: **Recinte petroquímic d'estudi**. Font: MCSC2024, id1459998,
classe347,162,59ha. Proves natives QGIS3.44.11, EPSG:25831/NONE, sobre la
geometria original; buffers positius dissolts i després negatius sobre
l'intermedi, amb32segments per quadrant i unions arrodonides.

| Distància +n/−n | Àrea m² | Forats | Afegit exterior m² |
| --- | ---: | ---: | ---: |
| 50m | 1813329,674904 | 5 | 48483,928033 |
| 100m | 1999668,313407 | 2 | 155232,042948 |
| 150m | 2229408,741960 | 0 | 384973,868392 |
| 200m | 2238444,651286 | 0 | 394011,994715 |
| 250m | 2244861,813172 | 0 | 400432,082847 |

També provats25,75,125,300i400m; tots consten a controls/geometria.json.
La comparació sobre l'ortofoto afavoreix150m: tanca els grans entrants i buits,
amb menys incorporació exterior que distàncies superiors. Resultat222,94ha,
38,50ha fora de l'exterior original. La discretització dels arcs retira també
3,767516m² de la font. No es declara que l'exterior es conservi exactament ni
que sigui el límit oficial del Polígon Sud.

Original a dades/coberta-original.gpkg; intermedi a dades/buffer-positiu.gpkg;
recinte a dades/poligon.gpkg. Conservades totes les alternatives, incloses les
envolupants i l'eliminació de forats de la comparació anterior.
La graella continua donant57fragments, amb pesos i posicions recalculats;
àrea de control2.229.408,741960m², comprovada amb tolerància0,01m².

## Controls actualitzats i lots

- Domini comú:3.490.455cel·les. Torxa, carretera, cobertura i altures conservades.
- T MDT/MDS:2.962.199/447.860cel·les. Suma de37C/MDT:1.461.016cel·les
  amb alguna visió i màxim33. C/MDS:7visibles,21ocultes,9no calculades.
- 57A sense T:2.281.626/115.149cel·les, MDT/MDS.
- 57A o T:2.977.704/470.444cel·les,85,31%/13,48%.
- R1/R3/R4 A_MDT:82,126681%/73,824922%/73,177796%; A_MDS0% als quatre
  receptors de contrast. R1 conserva T1/G1/A0% amb MDS; R5 continua nul.
- Deu projectes de37capes vàlides, amb rutes relatives, oberts a /paquet,
  readonly i sense xarxa ni repositori font. QGIS reprodueix buffers,
  intermedi, ruta, mostreig, cotes, màscara, suma i consultes. GEOS/Shapely
  confirma el tancament; perfils independents a0,5m confirmen els signes.

Viewshed és una execució per punt. El guió descriu el lot gràfic de37files,
els camps comuns, les coordenades obtingudes amb aggregate/array_agg ordenat
per id, noms de sortida únics, suma i màscara. L'expressió s'ha executat amb
QGIS i retorna exactament les37coordenades esperades.

El nou lots_visibilitat.py és autònom dins de QGIS amb les dades del paquet:
37execucions C/MDT,28C/MDS i57A per model. Les179execucions natives s'han
comparat cel·la a cel·la amb la preparació independent: error màxim0 en
recomptes, percentatges i unions amb T, amb graella i NoData coincidents.
Conserva intermedis, binaris i lot.json; exigeix una destinació nova.
La verificació és programàtica, no una afirmació d'haver introduït totes les
files a mà en el diàleg GUI. El lot GUI repeteix l'algorisme; el guió encadena
també màscara, cotes i ponderació.

controls/verificacio-lots.json vincula els inputs, controls i guió amb hashes.
SHA del guió verificat:
`57718e2cbae6c95c36cb0d206bc317241c9541eafddd53570103d49ca74440f4`.
El segellat refusa un report de lots amb inputs o guió modificats.

## Captures i procedència de les imatges

- Dotze captures principals i cinc d'accés:17bundles PNG/SVG/manifest,
  sense warnings, mateixa imatge QGIS fixada i backend x11/DPR1.
- Ortofoto i MDS al començament, amb el mateix enquadrament; llegenda de
  cotes i cel·la5m. Nom del recinte als projectes, captures, figures i text.
- Ortofoto: peticions WMS GetMap ICGC2025, desades com a GeoTIFF locals;
  context10m/píxel, sector2,5m i torxa0,5m. Capa d'origen25cm. No és un
  mosaic de fulls descarregats ni un WMTS. URL, BBOX i resolució a fonts/fonts.json.
- Acció pública `trigger_action`, name «Caixa d'eines», obre el dock real.
  `expand_tree_item` i `select_tree_item` despleguen GDAL → Miscel·lània ràster
  → Viewshed. Menú Vectorial → Geoprocessing Tools → Àrea d'influència obert.
  Botons i files marcats amb requadres.
- El selector complet d'Àrea d'influència es resolia per àlies a Create wedge
  buffers tot i no retornar warnings. Corregit amb el prefix inequívoc
  «Àrea d'influ» i verificació visual de la fila correcta. No s'ha retocat
  cap sortida ni llegit codi intern del proveïdor.
- Probes privats a tmp/qgis/visibilitat-r3-probe; recepta desregistrada després
  de la prova. open_processing_toolbox i setters de text no eren accions
  suportades. El context-menu de Processing va quedar bloquejat; es va parar
  només el contenidor propi38cd2d680570, després d'inspeccionar-ne les etiquetes.
  Les captures docents finals utilitzen les accions públiques comprovades.
- Als dos buffers, requadres sobre Distància sense etiqueta damunt de l'ajuda.
  Cinc QMD/SVG regenerats;46computacions del manual vigents.

## Lliurament segellat i revisió

- ZIP `tmp/dades-docents/practica-visibilitat-costa-20261002-r3.zip`:
  **161.155.091bytes,250fitxers**, SHA
  `b7f2c5f38c8ee45cca592ce35db4aaeac77a413f6ace210948e47e338c3369cc`.
  Deu projectes,37capes,17captures,5SVG, fonts, intermedis, controls i guions.
  CRC i hashes de tots els membres comprovats. Sense pujada a Moodle.
- GUIA26p,9.552.178bytes, SHA
  `a10daf2971b98120ff5d7c8130f0edf9466df726b2574c7769059a2e8e708869`.
- SOLUCIONS3p,49.172bytes, SHA
  `b4f475b44c8c985e1e38bace3055585c89278cbe6702791ee4ec87cf1483ea16`.
- Web C3/bibliografia a1440/390px:25imatges de C3, cap error MathJax,
  imatge trencada, ancoratge perdut, citació crua ni overflow.
- PDF manual219p,24figures de C3; límits correctes després de dividir dos
  passatges amb paths/nombres llargs. Pàgines d'ortofoto/MDS, eines, buffers,
  lots, comparació geomètrica i controls inspeccionades; guions26/3p revisats.
- PDF SHA `506ad1461d61dd3c0cccf4d007951029e4ab1d3ee08db76661a83084151a6193`;
  còpia servida idèntica, fresh/artifacts_valid. Rebut preview SHA
  `53fc57cf7e426f7e4a1a8ebd4c76dece145e488098c7b801ea2322f4be0fbad1`.
- Prosa, qualitat de fonts i site-check correctes. HTML audit conserva els
  avisos coneguts de logos, SVG i pressupost d'inspecció; navegador i revisió
  visual/PDF cobreixen els recursos actuals. Cap canvi a marques o generats
  per silenciar avisos.
- Inspecció directa de _site sense dades privades ni fonts de càlcul. El
  notebook públic de mostra assets/jupyter/blog.ipynb,865bytes, és anterior
  a la tasca i estava servit al main des de l'1d'octubre; no és una font privada.
  La referència Farnós continua visible. metrics.yml, pins i desplegament
  sense canvis en aquesta revisió.
- Review C3 `visibilitat-recinte-lots-dades-linia-20261002`, revisió25,
  digest `22d4301bba6ab3ad2c4875207e064166b4e6edc1d9470e8813ac0950baf813e4`.
- Review bibliografia `bibliografia-recinte-lots-copia-20261002`, revisió26,
  digest `2b076cc30032b9cf6174fbbb0968056b8bf7352990a43d86a3b34f10bd2b6fcb`.
  Cap troballa nova;23reviews/21stale. La revisió d'agent no aprova contingut.

Serve local32768 obert. Canvis locals sense commit ni publicació; públic
encara a main e7f41e9,199p. Dades i paquets de Moodle fora de Git.
