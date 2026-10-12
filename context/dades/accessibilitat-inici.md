# Accessibilitat: paquet d'inici compacte

Preparació privada de la incidència [9](https://github.com/geourv/geodisseny/issues/9).
Reserva acceptada per l'autor el 6/10/2026: «Per mi pots anar fent».
Rebut: https://github.com/geourv/geodisseny/issues/9#issuecomment-6023953001.

Lliurament local vigent: `dist/practiques/accessibilitat-vilaseca/2026-10-07-r2/ca/`,
amb `accessibilitat-vilaseca-2026-10-07-r2-ca.zip`,
`accessibilitat-vilaseca-docent-2026-10-07-r2-ca.zip` i `manifest.json`. Les lectures continuen en
draft per a revisió de l'autor; el segellat i les comprovacions no equivalen
a aprovació humana ni a càrrega a Moodle.

## Abast acordat

Un GeoPackage multicapa amb projecte QGIS incrustat i una guia PDF per a
l'alumnat. Entrades bàsiques, sense resultats resolts: origen, destí, xarxa
completa de Vila-seca, límit municipal, cobertes, MDT i passos explícits.
Preparació docent separada amb càlculs, projectes per moments i captures.

La cadena inclou euclidiana vectorial, distància ràster amb GRASS i contrast
GDAL, rutes/temps/àrees de servei, rasterització i reclassificació de cobertes,
inserció condicional de passos, r.cost/r.path, r.walk en tots dos sentits i
isòcrones. La guia ha de permetre continuar a casa. Exercici amb opció de
reproducció o transferència a una zona alternativa i enllaços de descàrrega.
L'autor retira tota preparació del campus i el bloc separat de la Pineda.
El manual publicat queda fora d'aquesta tasca.

## Diagnosi de la xarxa anterior

El retall de 1700×1700m no era tota Vila-seca. La xarxa tenia189parts;
el component d'O tenia93parts/8407,53m amb P2 obert, principalment al nord.
Retirar el tram RTT1354754 deixava només l'eix2502964 de68,42m. Era una
limitació del graf preparat, no només de la vista. Les línies cartogràfiques
RTT no són automàticament un graf de navegació: els marges de vial no s'han
de convertir en eixos ni connectar tots els creuaments a diferent nivell.

La font anterior de10.759eixos era ja una selecció per tipus/finestra.
La preparació nova conserva l'extracte complet de transports del municipi
i entorn per al contrast, incloent-ne els marges com a cartografia de
referència. Es contrastarà amb identitats nodals OSM per als itineraris de
vials urbans i rurals, amb procedència i exclusions explícites.

## Fonts i destinació

- ICGC, divisions administratives20/1/2026. Vila-seca: CODIMUNI431711,
 21,6558km² declarats. La selecció per cobertura municipal més500m té
 extensió X339400–349900,Y4547100–4555500.
- ICGC, cobertes MCSC2024, GeoPackage original remot:
 https://datacloud.icgc.cat/datacloud/cobertes-sol/gpkg_unzip/cobertes-sol-v1r0-2024.gpkg.
 Extracte local de5207polígons amb IDs originals i taules de llegenda.
- ICGC, transports RTT2024, extracte de12817elements amb atributs originals:
 https://datacloud.icgc.cat/datacloud/topografia-territorial/gpkg_unzip/topografia-territorial-v1r0-2024.gpkg.
- ICGC, MDT LiDAR2021–2023 a5m; ortofoto2025 per a context. No inventar
 resolució més fina ni atribuir al MDT el perfil exacte dels passos inferiors.
- OSM/Geofabrik, snapshot datat5/10/2026 de Catalunya, amb nodes identificats:
  https://download.geofabrik.de/europe/spain/cataluna-261005.osm.pbf.
  SHA `522f5a71ae966c02d76935b6cecabb09eea6f0c9ad8443c33867cb89c6417959`.
  Mida del publisher271.098.804bytes i descodificació PBF comprovades; checksum
  MD5 upstream no disponible per errors de servei, sense atribuir-lo a validat.
  Extracte ambosmium4.1.1, dependència temporal de preparació, ODbL1.0.

Font executable actual: `practiques/accessibilitat-vilaseca/preparar.py`.
Recursos declarats: `practiques/accessibilitat-vilaseca/recursos.yml`.
Treball actual: `sandbox/practiques/accessibilitat-vilaseca/2026-10-07-organitzacio/`.
La preparació inicial conservada és
`tmp/dades-docents/qgis/accessibilitat-vilaseca-20261006-inici/`.
Les fonts originals i els paquets segellats anteriors es munten readonly.
La preparació és pròpia de la pràctica; captures i PDF utilitzen els
proveïdors seleccionats. Guia en draft fins a revisió humana.

## Paquets inicials segellats, conservats

Segellat local del 7/10/2026, estat `private-author-review`, sense aprovació
humana ni publicació. El paquet d'alumnat inclou només GeoPackage i guia PDF;
el paquet docent conserva fonts, resultats, captures, projectes, controls i
fonts de reproducció.

- `tmp/dades-docents/practica-accessibilitat-vilaseca-20261006-alumnat.zip`:
  26.895.817 bytes, 2 fitxers, SHA-256
  `95082dbcc3c25c7082b1af7ac666b6884337974631bf8655de88fb24384bf0a7`.
- `tmp/dades-docents/practica-accessibilitat-vilaseca-20261006-docent.zip`:
  385.887.881 bytes, 171 fitxers, SHA-256
  `284c087c48f1f9863306c82c637ee54cd2b767d0570afe8bcab30965e7b3a00c`.

Rebuts: `tmp/dades-docents/practica-accessibilitat-vilaseca-20261006-alumnat.receipt.json`
i `tmp/dades-docents/practica-accessibilitat-vilaseca-20261006-docent.receipt.json`.
Manifest segellat: `tmp/dades-docents/qgis/accessibilitat-vilaseca-20261006-inici/MANIFEST.json`.

## Verificació del lliurament inicial

Projecte incrustat amb11capes —9vectors i2ràsters— reobert a una ubicació
nova, readonly/offline i sense muntar el repositori. Onze projectes docents i
118fitxers de dades/estils/projectes contrastats amb SHA abans/després.
GPKG inicial SHA `46d326819ad05f328eec12d34026956adcd3bfec9facbefeee226068fee03593`.
MDT Float32 incrustat amb valors exactes.9captures PNG/SVG/manifests actuals,
runtimex11, sense avisos; GUIA23p/SOLUCIONS3p,25/7encapçalaments complets,
12línies de codi i9imatges dins de pàgina. Floats fixats a prop del procediment.

Euclidiana361,318253m/vector i361,835598m/ràster; xarxa oberta448,048353m,
tancada4876,695005m, totes dues amb ruta. r.cost contrastat amb Dijkstra;
r.walk amb un graf dirigit independent. Anada489,156143s i tornada483,173590s;
control pla430,104744s en tots dos sentits. Condicionals i reclassificació
contrastats cel·la a cel·la; passos inserits abans del NoData99 final.

`prose_check` rebutja explícitament els guions privats decontext/; revisió
manual de les fonts i comprovacions completes del PDF, sense presentar-les
com un report MCP. Diagnòstic de fonts públiques correcte,57/57computacions
actuals i `site_check` correcte. Cap canvi de fonts/assets del manual publicat.
CRC, SHA dels ZIP i manifest segellat revalidats en lliurar-los a l'autor.

## Revisió de les guies del 7/10

Petició de l'autor: recuperar instruccions concretes i captures, completar
rasterització de cobertes i recursos enllaçats, substituir la informació de
canvis per una resolució docent detallada i explicar la conservació dels
passos de fricció al cost. Reserva de #9 mantinguda:
https://github.com/geourv/geodisseny/issues/9#issuecomment-6032538643.

Destinació nova `tmp/dades-docents/qgis/accessibilitat-vilaseca-20261007-guies/`.
GPKG d'inici i càlculs idèntics als segellats;11capes/11projectes reoberts
readonly/offline,119fitxers comprovats. Captures conservades i tres de noves:
rasterització de cobertes, de passos i cost per cel·la amb passos de valor5.
PNG/SVG/manifests del proveïdor amb pin950ee7…,x11 i0avisos.

GUIA33p i resolució docent28p,15imatges a cadaPDF,28/22encapçalaments i
13/11línies de codi comprovats. Links actius a cada recurs; passos amb fricció1
es conserven amb cost5 i les barreresNoData continuenNoData. Cel·les de control:
P2 X344372,5/Y4553742,5 i alternatiu X344097,5/Y4553577,5. Els PDF complets
s'han comprovat amb límits de paraules/imatges i revisió de pàgines renderitzades.

- `practica-accessibilitat-vilaseca-20261007-guies-alumnat.zip`:
  27.598.638bytes,2fitxers,SHA
  `714d59da2d8961a9a12155653244155ea69b6729275cf314bba2cdb513a7bdbb`.
- `practica-accessibilitat-vilaseca-20261007-guies-docent.zip`:
  396.941.925bytes,191fitxers,SHA
  `0afa47fa4b0e1cac6e18ea978c43f4cdfbc58641e15ef8a7c55310893cc1860e`.

CRC i SHA de tots els membres correctes. Estat private-author-review;
els paquets anteriors i el manual públic es conserven.

## Organització i lliuraments del 7/10

Reserva de reorganització acceptada amb noms de lectura per idioma:
https://github.com/geourv/geodisseny/issues/9#issuecomment-6037300264.
Fonts editables a `practiques/accessibilitat-vilaseca/`, treball i evidències a
`sandbox/practiques/accessibilitat-vilaseca/`, lliuraments a `dist/practiques/`.
Les tres carpetes queden excloses de Jekyll; sandbox i dist, també ignorades
per Git. Les dades SIG, els PDF i els ZIP de la pràctica no es versionen.

Lectures actuals:

- `practiques/accessibilitat-vilaseca/ca/alumnat/LLEGIU-ME.md`.
- `practiques/accessibilitat-vilaseca/ca/docent/LLEGIU-ME.md`.

La fase `--organise` ha reutilitzat la preparació segellada de les guies,
verificant el manifest i els fitxers copiats. Dades i càlculs idèntics;
el GeoPackage inicial conserva SHA `46d326819ad05f328eec12d34026956adcd3bfec9facbefeee226068fee03593`.
La recepta/configuració derivada de captures es conserva a `captures/`
dins del run actual, amb paths confinats al sandbox i validació del proveïdor
correcta per a 12 captures. No s'ha substituït cap paquet anterior.

La reconstrucció encara necessita les entrades locals històriques declarades
al preparador: divisions administratives ICGC a
`tmp/dades-docents/originals/icgc-20260120/divisions-administratives-v2r2-20260120.gpkg`
i passos de la preparació
`tmp/dades-docents/qgis/distancies-vilaseca-20261001-ampliada/`.
La fase d'organització necessita també la baseline segellada
`tmp/dades-docents/qgis/accessibilitat-vilaseca-20261007-guies/`.
Són entrades de només lectura, no destinacions noves de treball. Aquesta
reorganització no acredita una reconstrucció completa sense snapshots locals.

### ZIPs de Moodle de la primera organització

- `dist/practiques/accessibilitat-vilaseca/2026-10-07/ca/alumnat.zip`:
  **27.598.739 bytes, 2 fitxers**. Arrel `accessibilitat-vilaseca/`,
  amb GeoPackage/projecte inicial i `LLEGIU-ME.pdf` de 33 pàgines.
  SHA-256 `d936d1b56b9ab811140493a9413843e81d362f0ccf350c4a848a9c77323a71e9`.
- `dist/practiques/accessibilitat-vilaseca/2026-10-07/ca/docent.zip`:
  **46.704.358 bytes, 50 fitxers**. Arrel `accessibilitat-vilaseca-docent/`,
  amb `LLEGIU-ME.pdf` docent de 28 pàgines, dades inicials, 11 projectes,
  resultats i intermedis necessaris per resoldre la pràctica.
  SHA-256 `f7425f063993404ce1382f45e149fb172cdf8cc31b160a6ae4d13a501a05c5ab`.

El paquet docent selecciona les dependències dels projectes i les sortides
de les operacions explicades. Originals regionals, caches, logs, captures
editables i scripts d'agent queden al sandbox de reconstrucció.
El manifest de dist declara inventaris, mides, hashes, run de reconstrucció,
`human_approved: false` i `site_release: null`.

Els PDF tenen 15 imatges cadascun, amb encapçalaments, expressions i límits
comprovats. SHA alumnat `5fbb6e6d4147d58c2a102eb23eb4790b11b4274210853c224bd9e18531041c49`;
SHA docent `bf3e86c43a4de307b98de8d6d421104e7fd6765cb0d1ed4062f7b66a8a871005`.

### Verificació dels ZIPs exactes

Executada des de l'arrel del checkout:

```bash
python3 practiques/accessibilitat-vilaseca/preparar.py --version 2026-10-07 --verify-deliverables
```

Rebut a
`sandbox/practiques/accessibilitat-vilaseca/verificacio-1791376481466443348/verified.json`,
amb execució a `qgis-receipt.json`. ZIPs extrets a una altra ubicació i oberts
amb el runtime QGIS fixat, sense xarxa, muntatge readonly i sense repositori
font: 11 capes del projecte incrustat vàlides, 11 projectes docents oberts i
**52 fitxers intactes** abans/després. CRC i hashes dels ZIP correctes.
P2 conserva cost 5 en obert i NoData en tancat; el pas alternatiu conserva
cost 5 en tots dos escenaris. El run de preparació i la versió de dist ja
estan segellats; una revisió necessita run i versió nous.

### Contracte compartit

La plantilla de lectures/PDF i l'adopció als altres manuals es proposen a
[unaltraweb#98](https://github.com/dosquartsdedocs/unaltraweb/issues/98).
La preparació i inspecció GIS es coordinen amb
[unaltracaptura#4](https://github.com/dosquartsdedocs/unaltracaptura-qgis/issues/4#issuecomment-6037676887).
Diapositives ajornades. No s'ha modificat cap proveïdor ni migrat implícitament
les altres pràctiques.

### Comprovacions del consumidor

Amb el runtime fixat d'unaltraweb 0.5.0: doctor correcte, sense errors ni
avisos; `site_check` i build correctes; 57/57 computacions actuals.
`prose_check` públic sense errors, amb l'avís preexistent «I i» dels nombres
romans al capítol 1. Les lectures privades s'han revisat amb les comprovacions
PDF indicades, sense atribuir-los un report editorial MCP.

Preview etiquetat del mateix projecte revisat a 1440 i 390 px: **20 vistes**
—inici i nou paths de capítol— sense imatges absents, errors MathJax,
cites sense resoldre, enllaços als directoris privats ni desbordament
horitzontal. Deu paths privats d'activitats, sandbox, dist, context i tmp
retornen 404. `_site` no conté les carpetes excloses, dades SIG, ZIPs,
fonts executables o documents LLEGIU-ME. Rebut i dues captures de revisió a
`sandbox/practiques/accessibilitat-vilaseca/verificacio-web-1791386242812070197/`.

L'inspector de fons, executat per separat als capítols 4 i 5, deixa aquests
SVG existents del manual com a **no verificables**, no com a opacs comprovats:

- `assets/img/generated/john-snow-pous.svg`: límit o timeout del descodificador.
- `assets/img/generated/constanti-pesos.svg`.
- `assets/img/generated/punts-municipis.svg`.
- `assets/img/generated/constanti-recomptes.svg`.
- `assets/img/generated/constanti-moran.svg`.
- `assets/img/generated/constanti-permutacions.svg`.
- `assets/img/generated/renda-moran.svg`.

Els sis darrers retornen «SVG declarations and external stylesheets are not
allowed in inspection». No s'han pintat fons ni retocat outputs gestionats.
Cal resoldre la verificació o registrar la decisió de l'autor abans d'una
futura publicació d'aquests recursos; no s'ha desplegat el manual en aquesta
tasca. Rebuts a `/tmp/opencode/geodisseny-image-background-check-1791385601821688695.log`
i `/tmp/opencode/geodisseny-image-background-check-1791385607457512021.log`.

L'autor ha triat mantenir el consumidor a 0.5.0 davant l'oferta del MCP
connectat 0.7.0, que detecta un conflicte amb el workflow de desplegament.
Cap canvi de pins o scaffold. El preview s'ha aturat i s'ha retirat només
la còpia de PDF propietat del rebut de preview, amb SHA del rebut revisat.
Git no indexa dades SIG, projectes QGIS o ZIPs; sandbox/dist ignorats.
CRC i SHA dels ZIPs de dist es mantenen correctes després de les comprovacions.

Rebut final de lliurament i comprovacions:
https://github.com/geourv/geodisseny/issues/9#issuecomment-6041053380.

## Noms de Moodle i revisió r2

L'autor demana noms descriptius amb pràctica i data/versió, sense «alumnat»
o «estudiants» al nom del lliurament d'inici. Continuació de reserva:
https://github.com/geourv/geodisseny/issues/9#issuecomment-6041965735.

ZIPs vigents a `dist/practiques/accessibilitat-vilaseca/2026-10-07-r2/ca/`:

- `accessibilitat-vilaseca-2026-10-07-r2-ca.zip`, 27.598.739 bytes, 2 fitxers.
- `accessibilitat-vilaseca-docent-2026-10-07-r2-ca.zip`, 46.704.358 bytes, 50 fitxers.

Arrel interna de l'inici `accessibilitat-vilaseca/`, sense destinatari al nom;
les claus de destinatari dels manifests i les rutes de fonts es conserven.
La revisió r2 afecta els noms externs, no les dades o les lectures:
**els bytes i SHA-256 dels dos ZIPs són idèntics als de la primera organització**.
Copies i rebuts de noms a
`sandbox/practiques/accessibilitat-vilaseca/lliurament-2026-10-07-r2-1791389965658026899/`.
El manifest de dist identifica versió, run d'empaquetat i manifest d'origen.
Les versions anteriors segellades es conserven.

```bash
python3 practiques/accessibilitat-vilaseca/preparar.py \
  --rename-deliverables-from 2026-10-07 --version 2026-10-07-r2 \
  --verify-deliverables
```

Executat amb nova verificació QGIS offline/readonly: 11 capes inicials,
11 projectes, 52 fitxers intactes i controls dels passos correctes.
Rebut `sandbox/practiques/accessibilitat-vilaseca/verificacio-1791389969352194110/verified.json`.
La comanda de canvi de nom exigeix una versió nova; per revalidar l'actual,
executar només `--verify-deliverables`.

### Desglossament de la reducció docent

Inspecció del directori central dels ZIPs, sense extreure ni alterar originals.
Mides de contingut ja comprimit, amb MB decimals:

| Categoria del paquet anterior de guies | Mida comprimida |
| --- | ---: |
| `fonts/`, 8 fitxers de font | 300.476.776 bytes |
| PBF de Catalunya, inclòs dins de fonts | 270.837.917 bytes |
| `captures/`, 45 PNG/SVG/manifests | 25.639.015 bytes |
| `docent/`, resultats i resolució anteriors | 43.111.125 bytes |
| `alumnat/`, dades i lectura anteriors | 27.598.393 bytes |

El paquet anterior de guies tenia 396.941.925 bytes i 191 fitxers; el primer
paquet docent, 385.887.881 bytes i 171 fitxers. El lliurament net té
46.704.358 bytes: dades inicials i lectura 27.598.387 bytes comprimits,
resolució docent 8.283.575 i projectes/resultats seleccionats 10.812.054,
més capçaleres ZIP. La reducció respon a separar reconstrucció i material
de classe, no a una compressió nova o a menys cobertura de les dades d'inici.
Els PDF conserven les captures incrustades; les dependències dels projectes
han estat comprovades al ZIP exacte.

### Path policy i actualitzacions

Al consumidor s'han afegit normes AGENTS, ignores i exclusions Jekyll.
Encara no s'ha instal·lat una declaració formal `workspace_rule.path_policies`
al manifest compartit del proveïdor. La declaració/adopció del perfil pertany
a unaltraweb/unaltremanual i es demana a #98.

L'autor proposa fer habitual l'actualització compatible dels consumidors MCP.
Cal distingir MCP actiu, pins del consumidor, tema/dependències, renderers
i outputs gestionats. Un canvi de l'orquestrador no ha d'invalidar per si sol
captures, diagrames o càlculs; canvis efectius de fonts, dades, tokens, renderer
o contracte sí que requereixen comprovació i regeneració selectiva.
El pla actiu 0.5.0→0.7.0 continua amb el conflicte del workflow personalitzat;
no s'ha aplicat una sincronització amb conflictes ni sobreescrit aquell control.

### Prompt per a la sessió al core unaltraweb

Requisits de noms, path policy i actualitzacions compartits al core:
https://github.com/dosquartsdedocs/unaltraweb/issues/98#issuecomment-6042225633.

```text
Continua unaltraweb#98: https://github.com/dosquartsdedocs/unaltraweb/issues/98.
Vull consolidar el contracte de pràctiques d'unaltremanual i fer habitual
l'actualització compatible dels consumidors. Llegeix AGENTS i el contracte
del repositori, identifica el treball existent i reserva els paths exactes.

1. Fonts específiques a practiques/<slug>/; dades, snapshots, proves i
   reconstrucció a sandbox/practiques/<slug>/<run>/; ZIPs de Moodle a
   dist/practiques/<slug>/<versio>/<lang>/. Declaracions compartides de
   workspace_rule.path_policies amb l'schema vigent: fonts versionades,
   sandbox/dist ignorats i conservació explícita. Cleanup no autoritza
   esborrar runs, snapshots o ZIPs segellats. Git ignore i exclusions Jekyll
   són controls separats; comprova també les fugues al web/PDF.

2. ZIP d'inici <slug>-<versio>-<lang>.zip, sense alumnat/estudiants al nom
   o arrel interna; docent <slug>-docent-<versio>-<lang>.zip. Lectures
   LLEGIU-ME(ca), LEEME(es), README(en), amb idioma/destinatari al path.
   Inici: dades/projecte i lectura PDF. Docent: resolució i projectes/resultats
   de classe. Originals regionals, logs i captures editables a reconstrucció.
   Versió independent del manual, no-clobber i verificació offline/hashes.
   La plantilla de lectures/PDF pertany al core; diapositives ajornades.

3. Inclou el contracte als scaffolds futurs i una adopció revisada als manuals
   existents mitjançant scaffold_sync. Preserva personalitzacions i posa en
   evidència els conflictes; no reinitialitzis llocs ni moguis fonts, esborris
   dades o canviïs l'aprovació editorial implícitament.

4. Actualitzar a releases publicades compatibles ha de ser el camí habitual
   dins de l'autorització i reserva vigents: mostrar versions/pla, revisar
   conflictes, aplicar amb CAS/plan_sha256 i comprovar el consumidor.
   Diferencia MCP actiu de pin consumit i workers de render. Mantén frescos
   els artefactes verificats si les seves dependències continuen compatibles:
   canviar només l'orquestrador MCP no és motiu de reconstrucció. Si canvien
   fonts, inputs, tokens, renderer o contracte, identifica les peces afectades
   i regenera només les necessàries. No forcis una reconstrucció global ni
   declaris fresc un resultat realment obsolet. Actualitzar no publica.

5. Prova instal·lació nova i adopció, customitzacions/conflictes, noms i
   contingut dels ZIPs, exclusions, actualització només de MCP amb outputs
   preservats i canvi efectiu de dependència amb obsolescència selectiva.
   Pilot geourv/geodisseny#9: consumidor0.5.0, MCP actiu0.7.0; pla amb
   Makefile/Gemfile/Gemfile.lock/scaffold i conflicte al workflow deploy.yml.
   Preserva el seu desplegament manual per reviewed_sha. Coordina el contracte
   comú d'actualització amb gacontext i el GIS amb unaltracaptura; no dupliquis
   executors genèrics al consumidor ni alteris altres checkouts.

Lliura implementació, proves, contracte i release/adopció revisats. Si el flux
d'actualització requereix una incidència separada de #98, enllaça-les.
```

Comprovacions finals r2: `site_check` correcte, `prose_check` públic sense
errors —avís preexistent «I i»—, Git sense dades/ZIPs indexats i outputs del
manual/pins preservats. Intent de repetir r2 rebutjat abans d'escriure:
guard no-clobber comprovat. Hashes dels quatre ZIPs de les dues versions
coincideixen per destinatari. Fonts i lectures continuen per a revisió humana.

Rebut r2 i resposta a la petició de noms Moodle:
https://github.com/geourv/geodisseny/issues/9#issuecomment-6042364691.
