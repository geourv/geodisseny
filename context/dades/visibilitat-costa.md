# Visibilitat: torxa, carretera i polígon de cobertes

Versió anterior conservada. La revisió activa de recinte compacte, lots i
captures és a `context/dades/visibilitat-costa-r3.md`. Aquest registre i el ZIP següent
descriuen exactament el primer lliurament costa; la font de preparació
corresponent es conserva a reproduccio/ dins del ZIP immutable.

Revisió del 2 d'octubre de 2026, incidència5. Respon a la petició de l'autor:
substituir la parcel·la cadastral irregular i ordenar els exemples com a punt
identificat, acumulació d'una carretera i visibilitat d'una àrea industrial.
Branca `content/5-visibilitat-mdt-mds`; capítol3 en draft, sense nova publicació.

Font executable: `context/dades/preparar_visibilitat_costa.py`.
Destinació privada: `tmp/dades-docents/qgis/visibilitat-costa-20261002/`.
El preparador separa --fetch, --build, --style, --sqlite, --docs i --package.
La verificació --verify-package funciona amb el paquet traslladat a /paquet,
readonly, sense repositori font i amb només la interfície de xarxa lo.

## Lliurament segellat

- `tmp/dades-docents/practica-visibilitat-costa-20261002.zip`:
  149.167.797bytes,211fitxers; SHA-256
  `a5130ad5221a21e8e86350c485731c4384b44c720f1ce3a879815d65577946c1`.
- Arrel interna `visibilitat-costa/`; nou projectes,34capes preparades,
 37conques MDT individuals,9captures i4SVG, fonts, controls i reproducció.
- GUIA16p,6.822.497bytes; SHA
  `918e072927bdf6dc568b490ff4457593322fe480e5b3af1ec4c0f5e68e22e814`.
- SOLUCIONS3p,46.234bytes; SHA
  `155b06bc7d9c8089d4f087d1f4ebb48d43e30320966acfd0f3e9adb2b14c9c5d`.
- CRC i tots els hashes dels membres verificats. Bases SQLite autònomes,
  sense WAL/SHM. La passada final QGIS verifica també l'expressió de validesa
  puntual:7visibles,21ocultes i9nul·les al contrast MDS de carretera.
- Guions amb límits correctes i figures inspeccionades; salts abans dels
  blocs B/C i del resum de receptors per mantenir la progressió visual.
  Cap pujada a Moodle ni publicació; lliurament per a revisió de l'autor.

## Fonts i selecció

- Torxa OSM7682543312, versió1 de 2020-07-04, etiqueta `man_made=flare`:
  https://www.openstreetmap.org/api/0.6/node/7682543312/1.
  Coordenades originals EPSG:25831:346894,824499;4552508,353399.
  Contrast amb ortofoto ICGC2025 i pic del retall MDS natiu d'1m. No es confon
  una xemeneia de procés amb una torxa ni s'atribueix propietat empresarial
  sense comprovació. La cota del LiDAR no és una mesura certificada de flama.
- MCSC2024, `cobertes_sol`, classe347 i id1459998:
  https://datacloud.icgc.cat/datacloud/cobertes-sol/gpkg_unzip/cobertes-sol-v1r0-2024.gpkg.
  Polígon original vàlid,1.625.929,156054m²; es conserven les19exclusions
  interiors,218.509,485m². Delimita l'àrea industrial seleccionada, no tota
  l'extensió legal o funcional del complex químic sud.
- RTT2024, eixos `_35_transports_l`, `codivia='TV-3148'`:
  https://datacloud.icgc.cat/datacloud/topografia-territorial/gpkg_unzip/topografia-territorial-v1r0-2024.gpkg.
  La selecció completa confirma63eixos. El retall anterior ja contenia aquests
  eixos; la continuació cap a l'interior de la Pineda té codiTV-3146. La hipòtesi
  inicial d'eixosTV-3148 absents s'ha corregit després de consultar la font.
  Un recorregut cartogràfic únic de3.652,272633m evita duplicar calçades.
  Tots els vèrtexs originals participen al graf; claus al mm. No és un model
  de restriccions de trànsit. QGIS natiu reprodueix la longitud exacta.
- Mar RTT2024: `_50_hidrografia_p`, tipusmar, ids306758 i315562, retallat.
  La classe466 del MCSC només cobria una petita massa d'aigua del retall i
  no s'utilitza per inferir que la resta del mar és terra.
- MDT LiDAR ICGC2021–2023,5m natius; MDS1m del mateix producte, màxim a5m
  amb overviews desactivats. Ortofotos2025 de context10m/píxel, indústria
  2,5m/píxel i torxa0,5m/píxel. URLs, llicències i hashes a fonts/fonts.json.

## Geometria, cotes i cobertura

- Graella comuna2.000×2.000,5m, EPSG:25831/NONE; bounds
  `(342000,4549000,352000,4559000)`.
- T ràster `(346892.5,4552507.5)`, desplaçament2,476204m. MDT20,941999m,
  picMDS151,311996m; estructura estimada130,369997m. Objectiu de model1m
  sobre el pic: cota152,311996m, altures relatives131,369997m/1m.
- Carretera:37intervals de98,710071155m; primer punt a49,355035578m.
  Ulls a MDT+1,7m. Nou posicions queden sota l'MDS opac i són incompatibles
  amb la comparació d'orígens: C01,C06,C07,C09,C16,C19,C29,C33,C34.
  Contrast amb les mateixes28posicions en tots dos models:2.763,881992m.
- Àrea:57fragments de graella250m retallada; un punt interior per fragment,
  pesos en m². Cotes d'objectiu MDS+1m, conservades al model MDT. Les posicions
  ràster poden desplaçar-se fins a3,54m respecte dels punts vectorials.
- Fonts:296.442cel·les amb almenys una elevació absent. Els buits dins del
  mar RTT tenen condició de contorn0m en les còpies de càlcul; els21.167altres
  buits no es consideren terreny conegut. Una passada GDAL sobre pla0 i
  obstacles1 identifica els raigs afectats per a totes95posicions font.
  S'exclouen211.025destinacions addicionals. Domini final3.490.455cel·les.
  Les fonts originals queden intactes; el model resultant conserva NoData.
- MDS≥MDT comprovat als valors originals comuns, sense elevar artificialment
  superfícies vàlides. Comparació de cotes mínimes Float64 amb MDT+1,7m.
  Mode GDAL DEM, Edge, curvatura0,85714; no confondre DEM i GROUND.

## Controls

| Magnitud | MDT | MDS |
| --- | ---: | ---: |
| T, cel·les visibles | 2962199 | 447860 |
| 28posicions de carretera, alguna visió | 1442133 | 2075 |
| 57A, sense T, alguna visió | 2026459 | 57435 |
| Alguna de57A o T | 2972068 | 457775 |

Exercici base de carretera,37conques MDT:1.461.016cel·les amb visió;
màxim33. T és visible en34de37mostres MDT,3.356,142419m representats.
Amb MDS:7visibles,21ocultes,9no calculades;690,970498m i25% del subconjunt
comparable. La màscara de validesa puntual s'aplica als atributs després
del mostreig; no deriva automàticament del NoData del ràster de T.

«Alguna part del polígon» és `(nombre A > 0) OR (T = 1)`. Conserva la torxa
encara que la graella no l'hagi mostrejada. Els percentatges ponderats A usen
només els57pesos d'àrea; T no rep un pes superficial inventat.

Receptors didàctics R1=C05,R2=C11,R3=C13,R4=C37, triats explícitament per
contrastar resultats, no com a mostra representativa. T MDT/MDS:1/1,0/0,
1/0,1/0. R5=(352100,4552000), fora del retall. A R1 amb MDS:T1,G1,A0%.
Els perfils independents a0,5m confirmen els quatre signes. Figures amb
perfils a2,5m i ampliació dels últims80m; no es generalitza una equivalència
exacta entre mètodes prop del llindar.

## Verificació i material

- QGIS3.44.11/GDAL3.10.3, imatge
  `sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc`.
- Ruta nativa,37posicions,57fragments i punts interiors concordants; cota
  mínima, expressió ràster amb Domini i suma de37conques concordants en totes
  les cel·les. Mostreig de T/G/A concordant, inclòs R5 nul.
- Nou projectes relatius de34capes oberts offline/readonly sense el repositori.
  Proves de pantalla:102/115/128m; comprovació de la màscara d'elevacions
  desconegudes en pla. Report amb hashes a controls/verificacio-qgis.json.
- Nou captures MCP de context/qgis/visibilitat-costa.yml; tots els manifests
  indiquen ok:true i runtime correcte. La crida de render del prefix complet
  va superar el timeout del client; el treball va acabar i els contenidors
  es van retirar, amb els nou bundles complets verificats i inspeccionats.
- Quatre QMD/SVG regenerats. Entrada context/inputs/visibilitat-costa.json
  compacta: mapes de visualització cada25m, percentatges a0,01 i compressió
  sense pèrdua dels codis uint16. Les estadístiques i els TIFF de5m no es
  redueixen a aquella precisió de presentació.
- Guions a context/practiques/visibilitat-costa.md i -docent.md, compilats
  amb Pandoc/XeLaTeX del PDF fixat, fontfamily=fontspec, DejaVuSans11pt,
  A4vertical18mm. S'han corregit desbordaments i salts entre blocs.

## Git, Moodle i historial

Paquets, projectes QGIS, ràsters i intermedis són a tmp/dades-docents, ignorats
per Git i exclosos de Jekyll. Comprovat índex i història accessible: cap
ZIP/GPKG/TIFF ni contingut de tmp, sandbox, .cache o _site versionat.
Les fonts versionables prèvies ocupaven77.076.135bytes; el magatzem d'objectes,
uns51MiB. Es mantenen guions, scripts, petites entrades i visuals del web.

GitHub ordinari bloqueja fitxers de més de100MiB. La documentació de Git LFS
estableix2GB per fitxer tant a Free com a Pro; no es configura LFS ni es
canvia el pla. Fonts consultades:
https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
i https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage.

L'assaig nord es conserva al ZIP immutablef760e14e…0520 i a
tmp/dades-docents/arxiu-visibilitat-nord-20261002. Arxivats33fitxers que eren
no versionats, tots idèntics als membres del ZIP. Recepta antiga desregistrada.
El registre històric continua a context/dades/visibilitat-nord.md.

## Revisió final

Prosa i qualitat de fonts sense incidències. Site-check abans del build.
Capítol3 amb16imatges a1440/390px: sense imatges trencades, errors MathJax,
citacions crues, ancoratges perduts ni desbordament horitzontal. Una taula
recupera les dades7/21/9 a les activitats. SVG i captures inspeccionats als
guions i al PDF del manual; límits de text correctes.

PDF local209p, SHA
`278cc6448d96fd8f7ea98cc0437da49f5b551b0f01356e99212f9f6945490e11`,
idèntic a la còpia servida. Rebut de preview SHA
`980e2b15eecd23c2e5f416f77e5c05a028297a93040702decdf5fe80188fdd52`.
El proveïdor declara fresh/artifacts_valid. HTML audit correcte amb els
avisos coneguts de transparència dels logos i inspecció limitada dels SVG;
no s'han alterat sortides ni marques per silenciar-los.

Review de línia `visibilitat-torxa-carretera-poligon-linia-20261002`, revisió21,
digest `9cff7cb27ba31a46860e60fb720e534ef7a8b30a5759857aa75a5c3dfc8ea4ad`:
cap troballa nova, sense aprovació de contingut. El camp supersedes és
gestionat pel servei i no és admès com a camp del report d'entrada; consultat
el contracte públic i registrat el report sense aquell camp. Historial conservat.

Entrada compacta de figures:633.552bytes. Cap paquet, GeoPackage, TIFF,
GeoJSON, GML o font QMD al lloc generat; context, tmp i sandbox exclosos.
Originals RTT, Cadastre i divisions ICGC amb els hashes previs; metrics.yml
sense diff. Serve local32768 obert. Sense commit, push ni publicació d'aquesta
revisió; pendent de lectura de l'autor.
