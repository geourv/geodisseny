# Pràctica de visibilitat: sector de la refineria nord

## Versió substituïda

L'autor ha demanat substituir aquest assaig cadastral per la progressió
torxa identificada → carretera Vila-seca–la Pineda → polígon de cobertes.
La versió activa es documenta a `context/dades/visibilitat-costa.md`.
El ZIP següent es conserva immutable. Els 33 fitxers no versionats del bundle
antic s'han contrastat byte a byte amb aquell ZIP i s'han arxivat a
`tmp/dades-docents/arxiu-visibilitat-nord-20261002/`, amb inventari propi.
Les quatre figures compartides del manual s'han regenerat per al cas nou;
les versions antigues continuen dins del ZIP, amb les seves fonts.

## Registre del primer lliurament

Preparació local de l'1 d'octubre de 2026, incidència5. Font executable:
`reproduccio/preparar_visibilitat.py` dins del ZIP. Destinació privada:
`tmp/dades-docents/qgis/visibilitat-nord-20261001/`.

## Lliurament

- ZIP: `tmp/dades-docents/practica-visibilitat-nord-20261001.zip`.
- 119.669.778 bytes,152fitxers; SHA-256
  `f760e14effcb88d51858d24a7d8c2261c1de0d9b206e510e465be7ac25bf0520`.
- Nou projectes relatius,32capes preparades,9captures amb els bundles complets,
  4SVG nous, fonts, resultats, estils, matrius, perfils i controls.
- GUIA14p, SHA `16b3d4ae904b39ef926dcbb3e29632448ea69f2abd544ad5ae2734a272dc9b36`.
- SOLUCIONS3p, SHA `7cd543041b7f508a0c4716fe10ee4575aa761068864a013c5eac2e0bf05c97d8`.
- CRC i SHA de tots els membres correctes; bases SQLite autònomes, sense WAL.
  Paquet segellat per a revisió, sense pujada a Moodle ni publicació web.

## Fonts i representació

- Cadastre: parcel·la1406801CF5610C,1716263,871903m². La geometria és vàlida;
  make_valid no en canvia l'àrea. El centroide cau fora del contorn irregular:
  P és un punt sobre la superfície, no el centre geomètric del cas regional antic.
- Original cadastral: `tmp/dades-docents/practiques/parceles-dgc-43111.zip`, SHA
  `30c89194f41f14d16f400e1eef7bd73ed4f09df82aedf0ddc7cf2c2e096c2304`.
  La parcel·la és un sector, no tot el perímetre de la petroquímica nord.
- MDT ICGC natiu5m: SHA
  `5284bab360f142d545cb285e33476d089ef19dc95fe1a7213566b06f06a258b3`.
- MDS ICGC1m agregat pel màxim a5m, overviews desactivats: SHA
  `83a09cf125b18902d467b2570edab0f0f6818635a2c13c07666dd5e0402f1b3e`.
  Tots dos són LiDAR2021–2023; dates i derivacions a fonts/fonts.json.
- Graella comuna EPSG:25831,2000×2000,5m; extensió
  X346000–356000,Y4555000–4565000. Cap buit d'elevació i MDS≥MDT a totes les cel·les.
  No s'ha imposat aquesta desigualtat modificant les elevacions.
- Ortofoto de context a10m/píxel i detall del sector a2,5m/píxel, WMS2025.
  No intervenen com a elevacions. Caps municipals de divisions ICGC2026-01-20.
- Perímetre exterior9774,820708m,49mostres de199,486136895m; mig interval inicial.
- Àrea: graella250m retallada,46fragments; pesos en m² que recuperen l'àrea total.
- P i les95mostres es representen als centres de cel·la; originals i distàncies
  de desplaçament conservats. El màxim teòric és3,535534m.

## Comparació controlada

P=(350417,5;4560117,5)m; MDT74,893997m, MDS76,148003m. Objectiu a cota
104,893997m:30m sobre MDT i28,745994568m sobre MDS. Mateixa regla per a cada
mostra. Són altures hipotètiques, no un inventari d'estructures.

GDAL Viewshed, Edge, curvatura0,85714, distància màxima0 sobre el retall.
El mode DEM dona cota absoluta mínima. La comparació amb MDT+1,7m fixa també
els receptors. Les cotes mínimes es conserven en Float64 per evitar alterar
llindars en desar-les. El mode GROUND tindria un altre significat.

| Grup | N | Cel·les amb alguna visió, MDT | Cel·les amb alguna visió, MDS |
| --- | ---: | ---: | ---: |
| P | 1 | 2165812 | 40394 |
| Perímetre | 49 | 2504988 | 214767 |
| Àrea | 46 | 2489472 | 202279 |

Domini comú de4.000.000cel·les. Els192càlculs de cota mínima, més els controls,
conserven la inclusió de visibilitat MDS dins MDT. Es distingeixen nombre visible,
fracció ponderada del mostreig i fracció de territori amb alguna visió.

R1–R7: punts d'exercici prop de capitals municipals, cel·la descoberta més propera
dins de100m amb MDS−MDT≤1m. R8, el Rourell, queda fora. R9–R11: llavors fixes
construïdes al sud, est i nord, sotmeses al mateix criteri de cel·la descoberta.
No són un inventari de miradors ni una mostra de població.

R10 amb MDS: P0, perímetre10,204081633% i àrea0,575959193%; aproximacions
997,430684m i0,9885ha representats. El punt únic no resumeix tota la instal·lació.

## Verificació i reproducció

- Runtime QGIS3.44.11/GDAL3.10.3, mateix ID fixat a la configuració d'unaltracaptura.
- Rampa amb pantalla: observador102m, pantalla115m a50m, destinació a100m;
  cota mínima128m comprovada analíticament i amb GDAL.
- Conversió de cota mínima idèntica al mode normal de Viewshed sobre MDT.
- Perfils independents P–R1 i P–R3, pas2,5m i mateixa curvatura, concordants
  amb els casos clars del mapa. La representació discreta pot diferir prop del límit.
- Nou projectes oberts readonly a `/paquet`, sense xarxa i sense repositori font.
- Native QGIS:49punts lineals coincidents amb les posicions originals;46fragments
  amb suma d'àrea coincident; punt sobre superfície coincident amb P original.
- gdal:viewshed en mode DEM reprodueix la cota mínima de l'API C de GDAL.
- native:rastercalc reprodueix totes les cel·les del binari MDS; rastersampling
  coincideix amb la taula, inclòs el nul de R8. Report: controls/verificacio-qgis.json.
- Els guions es compilen amb Pandoc/XeLaTeX del worker PDF fixat; A4 vertical,
  DejaVu Sans11pt, marges18mm. Paràmetres a controls/handouts.json. Correcció de
  dos desbordaments i salt abans de fonts per deixar espai a les figures pendents.
- Fases: --init, --fetch, --build, --style, --docs, --sqlite, verificacions i --package.
  Càlcul i estil en processos separats, originals readonly i només destinació nova RW.
- La font de preparació inclosa espera el repositori i els originals per regenerar
  extraccions; la pràctica QGIS funciona amb les dades locals distribuïdes.

El mostreig i el MDS màxim condicionen fortament el resultat. Les dates de les
fonts són diferents; no hi ha calibració de visió real ni valoració paisatgística.
