# Fonts reproduïbles de les pràctiques

Aquest directori conté **codi, configuració de recursos i documents editables**.
Es versiona a Git i està exclòs de Jekyll. Les activitats es publiquen com a
paquets de Moodle, amb una versió pròpia independent del manual.

## Pauta per a l'organització del treball de l'alumnat

La pauta general del manual separa `data/` (entrades i `inici.qgz`),
`sandbox/` (projecte de treball, proves i intermedis) i `dist/` (selecció final).
En preparar o revisar les edicions següents, cada LLEGIU-ME ha de concretar
aquesta separació i les rutes de les seves expressions i configuracions de lot.
Els grups de capes poden reflectir les fases, però no substitueixen exportar
o desar els resultats als fitxers corresponents.

El lliurament de l'estudiant es prepara en un GeoPackage nou amb els vectors
seleccionats, un QGZ extern relatiu, l'informe PDF i els GeoTIFF o recursos
necessaris. Les proves descartades no s'hi inclouen. Carpeta/ZIP i fitxers
principals s'identifiquen amb codi de pràctica, tema i cognoms, per exemple
`pr1-visibilitat-cognoms`; el codi real correspon a l'enunciat. La comprovació
final es fa sobre una còpia traslladada o un ZIP acabat de descomprimir:
mateixes capes, valors, estils, etiquetes, fonts i ordre de dibuix, sense
dependències de temporals o fitxers que no s'han lliurat.

Els LLEGIU-ME també han d'identificar proveïdors i requisits, distingir
expressions QGIS d'ordres CLI i recuperar el registre de GDAL/GRASS/SAGA quan
sigui pertinent. Aquesta pauta docent és diferent dels directoris ignorats
de preparació i reconstrucció del repositori descrits més avall.

## Lliuraments actuals i enunciats de Moodle

El directori visible conté només l'edició actual de cadascuna de les cinc
pràctiques, amb noms estables. L'enunciat editable es lliura fora del PDF:

```text
dist/practiques/<practica>/ca/
  <practica>.zip
  <practica>-docent.zip
  LLEGIU-ME.pdf
  LLEGIU-ME-docent.pdf
  ENUNCIAT-MOODLE.md
  manifest.json
  SHA256SUMS
```

Cada ZIP desplega una arrel amb el mateix nom de la pràctica, amb aquesta
estructura:

```text
<practica>/
  LLEGIU-ME.pdf
  data/
    inici.qgz
    <cas>.gpkg
    rasters/
    ortofoto-wms.xml
```

El paquet docent afegeix `data/docent.qgz` o les vistes de `data/projectes/`,
els vectors resolts i els GeoTIFF de resultats. Els projectes són externs i
relatius; els GeoPackage contenen vectors, no ràsters ni projectes incrustats.
L'ordre de dibuix segueix l'arbre del panell Capes. La font local de les dues
pràctiques que la necessiten es conserva a `data/fonts/`.

Els noms visibles identifiquen les tècniques. La correspondència de lliurament
és explícita a `HANDOFFS` del preparador del curs:

| Pràctica | Carpeta i prefix de ZIP actual |
| --- | --- |
| Accessibilitat: xarxa vectorial | `accessibilitat-xarxa-vectorial` |
| Accessibilitat: model ràster de cost | `accessibilitat-raster` |
| Accessibilitat: temps d'accés | `accessibilitat-temps-acces` |
| Anàlisi d'intervisibilitat | `analisi-intervisibilitat` |
| Estadística espacial descriptiva | `estadistica-espacial-descriptiva` |

Els municipis i recintes es presenten com a casos dins dels documents. Les
fonts de preparació i els noms dels fitxers de dades conserven la seva identitat
geogràfica per a la reconstrucció; no es reescriu la procedència dels bundles.

El preparador específic del curs és
[`lliurament-geodisseny.py`](lliurament-geodisseny.py). Selecciona els deu ZIPs
aprovats de la base del18/10, els verifica i en prepara còpies en un run nou.
La fase `--context`, dins de l'engine QGIS100… fixat, agrupa l'ortofoto local
i el WMS oficial de2025 i comprova que vectors i mostres ràster no han canviat.
El servei es declara amb `ortofoto-wms.xml`, llegible sense internet, i queda
desactivat. Els píxels del servei només s'utilitzen com a context en línia;
no són una entrada d'anàlisi. Cal conservar l'XML amb el projecte.

Després, `--layout --layout-pass <pass-nou>` crea una còpia de lliurament a
`handouts/<pass>/`: selecciona els vectors amb GDAL, exporta els ràsters a
GeoTIFF, escriu els projectes QGZ i actualitza les seves dependències relatives.
Comprova FIDs, atributs i geometries, píxels, graella, CRS, NoData i màscares.
`--package` rep el mateix `--layout-pass`; un pass existent no se sobreescriu.
La disposició històrica dels ZIPs aprovats només es conserva a la reconstrucció.

Els PDFs de lectura es construeixen amb `manual_practice_pdf_build` d'unaltraweb
i es consumeixen amb `--package --pdf-receipts <carpeta>`. La fase comprova
hashes, fonts, A4 horitzontal, codi i límits del PDF abans de fer els ZIPs del
curs. L'enunciat es versiona a `ca/docent/ENUNCIAT-MOODLE.md` de cada pràctica;
el PDF docent només explica on trobar-lo i com carregar-lo a Moodle.
En el lliurament visible, els dos PDFs i l'enunciat queden directament al costat
dels ZIPs. `alumnat/` i `docent/` només organitzen les fonts o la reconstrucció.
Si només canvien aquestes rutes externes, `--reuse-packages-from <run-verificat>`
reutilitza els mateixos ZIPs, PDFs i rebuts de verificació en un run nou, sense
tornar a renderitzar lectures ni executar GIS.

El perfil natiu v2 conserva la base d'anàlisi **només local** i no admet capes
WMS. Per això els `edicio.json` continuen descrivint aquesta base local; el
lliurament actual amb el context opcional el prepara el script del curs. Els
seus manifests són de Geodisseny, no bundles nous del protocol natiu. Les
captures s'obtenen separadament amb el MCP publicat0.6.1 i pantalla privada.

Abans de `--publish-current`, els deu ZIPs exactes es reobren en una ubicació
nova de només lectura, sense xarxa ni muntatge del workspace original. La
promoció prepara i comprova tot el candidat abans de moure l'arbre anterior complet a
`sandbox/practiques/arxiu-lliuraments/<run>/dist-practiques/`, verifica tots els
hashes i promou un arbre actual nou. Els noms, dates i hashes originals queden
als inventaris i a l'arxiu. No es netegen originals, runs o ZIPs segellats.
Per reconstruir a partir d'un lliurament aprovat que ja és a l'arxiu,
`--stage --source-handoff <carpeta-aprovada>` selecciona explícitament aquell
inventari; no s'infereix una font nova a partir d'un nom de fitxer semblant.

Trasllat efectuat el21/10/2026: els184fitxers i67directoris anteriors són a
`sandbox/practiques/arxiu-lliuraments/2026-10-21-distribucions-anteriors-01/dist-practiques/`.
L'inventari `original-tree.json` i el rebut `verified.json` de l'arxiu acrediten
els hashes. La base aprovada del18/10 es troba allà a
`lliurament-moodle/2026-10-18/ca/`. Les rutes antigues de les seccions històriques
s'han de llegir sota aquesta arrel arxivada.

Després de la prova d'aula, l'edició del **21/10** va adoptar els noms tècnics de
la taula anterior. La reconstrucció d'aquella edició és
`sandbox/practiques/lliurament-geodisseny/2026-10-21-lots-01/`, amb els paquets
`packages/review01/` i reobertura de21projectes a `reopen01/`. L'arbre actual
anterior del20/10,37fitxers i20directoris, és íntegre a
`sandbox/practiques/arxiu-lliuraments/2026-10-21-abans-noms-tecnics-01/dist-practiques/`,
amb inventari i comprovació de tots els hashes.

Les proves de l'autocompletat i de la suma són a
`sandbox/practiques/visibilitat-costa/2026-10-21-lots-01/`: s'han comprovat les
taules natives de5/37files, les expressions dels casos28/57, una execució de
Viewshed amb NoData255, la suma multifitxer i una ponderació real. Són proves
programàtiques dins del contenidor; no substitueixen les captures MCP pendents.

El lliurament local del **26/10** utilitza els nous formats i les rutes de
`sandbox/practiques/lliurament-geodisseny/2026-10-26-pdf-data-01/`.
Els paquets són a `packages/review02/`, amb selecció de rebuts PDF a
`pdf-receipts03/` i reobertura dels ZIPs exactes a `reopen03/`. S'han contrastat
els22ràsters extrets dels GeoPackage i s'han reobert26projectes QGZ offline:
afegir i moure una capa canvia l'ordre que rep el mapa. Els164fitxers extrets
es mantenen inalterats. Les lectures tenen9/4,18/8,9/8,42/10i15/7pàgines
d'inici/docents, en l'ordre de la taula.

Abans de substituir el dist, els37fitxers i20directoris de l'edició del21/10
s'han arxivat íntegres a
`sandbox/practiques/arxiu-lliuraments/2026-10-26-abans-geotiff-01/dist-practiques/`.
`current-verified.json` comprova independentment tots els hashes de l'arxiu,
els ZIPs actuals i els cinc `SHA256SUMS`. No s'ha sobreescrit cap versió.

La prova `diagnostics/uri01/verified.json` reprodueix la sortida GeoTIFF amb
prefix `geopackage:` i la resol en desar el projecte com a QGZ. Les dues conques
C05 amb entrada GPKG i GeoTIFF coincideixen píxel a píxel. Això no diagnostica
altres incidències de compatibilitat observades a classe.

`REVISIO-RETINGUDA.json` conserva deu passes copy preparats contra digests i
revision123; el registre tool-owned continua al límit i no s'ha alterat. Les
captures existents es reutilitzen, no es presenten com a captures noves del
format de fitxers. La taula de lots i el camp EXTRA desplegat continuen pendents
del proveïdor. El compositor natiu v2 és una font històrica d'anàlisi: els nous
formats els prepara el collector del curs, no un nou bundle natiu declarat.

L'edició local del **27/10** corregeix l'arrel de tots els ZIPs:
**`LLEGIU-ME.pdf` al costat de `data/`**, sense carpeta `pdf/` ni `payload`.
Lectures i enunciats indiquen les mateixes rutes. El run és
`sandbox/practiques/lliurament-geodisseny/2026-10-27-minimal-01/`:
`--reuse-layout-from 2026-10-26-pdf-data-01 --layout-pass layout02` conserva
byte a byte les dades i els projectes verificats; no torna a executar anàlisi.
Els deu PDFs s'han construït amb Web0.7.4 i el mateix worker PDF fixat.
Tenen9/4,18/8,9/8,43/11i15/7pàgines d'inici/docents, en l'ordre de la taula;
s'han revisat les132pàgines. `packages/review01/` i `reopen01/` vinculen els
ZIPs exactes a la reobertura dels26projectes i als164fitxers extrets inalterats.

Abans de substituir el dist, l'edició26/10completa —37fitxers i20directoris—
s'ha arxivat a
`sandbox/practiques/arxiu-lliuraments/2026-10-27-abans-arrel-minima-01/dist-practiques/`.
`current-verified.json` del run nou comprova tots els membres dels ZIPs,
els PDFs separats, els cinc fitxers de sumes i l'arxiu anterior íntegre.

La correcció posterior del mateix dia aplana també el directori visible:
`LLEGIU-ME.pdf`, `LLEGIU-ME-docent.pdf` i `ENUNCIAT-MOODLE.md` són directament
al costat dels dos ZIPs, sota `ca/`, sense carpetes `alumnat/` ni `docent/`.
La reconstrucció d'aquesta disposició és
`sandbox/practiques/lliurament-geodisseny/2026-10-27-pdfs-plans-01/`.
Reutilitza els deu ZIPs i PDFs anteriors byte a byte; l'arbre substituït és
íntegre a `sandbox/practiques/arxiu-lliuraments/2026-10-27-abans-pdfs-plans-01/`.
Els nous manifests i fitxers de sumes identifiquen les rutes planes.

Les dues lectures d'intervisibilitat incorporen la nova captura
`assets/captures/visibilitat-lots-suma.png`: cinc entrades, Suma, Ignora NoData
desactivat i Conca C05 de referència. El bundle PNG/SVG/manifest l'ha generat
el MCP0.6.1 amb pantalla privada, sense executar noves conques. Documenta
configuració, no una execució. Fonts i intents anteriors es conserven a
`sandbox/practiques/visibilitat-costa/2026-10-27-captures-01/`.
La revisió posterior incorpora **nou captures natives del productor0.7.0**,
en un render puntual autoritzat: taula plena, tres menús d'autoemplenat amb
etiquetes, editors d'expressions, fila buida inicial, selecció d'entrades i
EXTRA desplegat. La font és `context/qgis/visibilitat-batch.yml`; proves i
bundles són a `sandbox/practiques/visibilitat-costa/2026-10-27-batch-01/`.
Aquest ús puntual no reetiqueta les seleccions globals del helper de Web;
[Web#117](https://github.com/dosquartsdedocs/unaltraweb/issues/117) continua
descrivint aquell altre punt d'adopció.

El lliurament d'aquella revisió és
`sandbox/practiques/lliurament-geodisseny/2026-10-27-batch-01/`, amb
`pdf-receipts02/`, `packages/review01/`, `reopen01/` i `pdf-review01/`.
Només canvien els dos PDFs/ZIPs d'intervisibilitat i el seu enunciat:
**52pàgines d'inici i14docents**, totes revisades. S'han reobert26QGZ dels
ZIPs exactes i els164fitxers extrets romanen inalterats. Els altres vuit
ZIPs/PDFs són byte-idèntics als anteriors. El dist conserva la disposició plana.

La guia avisa de x/y no creats per pointsalonglines i mostra native:addxyfields
amb EPSG:25831; explica desament/recuperació i edició del `.batch`, les evidències
del procediment i la normalització de rutes Windows. La comprovació específica
és `visibilitat-costa/comprovar-prerequisits-lot.py`:37punts, cinc files desades
i recarregades amb el format natiu i10casos de format de ruta. No és una
execució Windows ni un nou càlcul de conques. Les alertes dels PDFs utilitzen
el component `manualcallout` ja present a la plantilla compartida.

L'arbre pla anterior complet,37fitxers i10directoris, s'ha arxivat a
`sandbox/practiques/arxiu-lliuraments/2026-10-27-abans-captures-batch-01/`.
`current-verified.json` contrasta tots els hashes de l'arxiu i les sumes del
dist nou. `REVISIO-RETINGUDA.json` conserva les passes copy preparades; el
registre editorial gestionat continua intacte.

## Organització de l'alumnat: edició del 30 d'octubre

Les cinc pràctiques concreten ara la pauta `data/`–`sandbox/`–`dist/` a les
deu lectures i als cinc enunciats Moodle. Les entrades es preserven, les proves
es fan a `sandbox/` i el lliurament es prepara en un GeoPackage nou, amb QGZ
extern relatiu, informe PDF i els GeoTIFF/recursos seleccionats. Els noms
segueixen codi–tema–cognoms; `prN` és un marcador que el docent substitueix pel
codi real de la tasca. Els grups de capes no mouen fitxers.

Reconstrucció del lliurament actual:
`sandbox/practiques/lliurament-geodisseny/2026-10-30-organitzacio-02/`.
Reutilitza `layout02` del run batch del27/10; els154membres de dades, projectes
i recursos dins dels deu ZIPs són byte-idèntics. Els PDFs nous tenen9/4,
19/8,10/8,53/16i16/7pàgines d'inici/docents, en l'ordre de la taula de pràctiques.
S'han revisat les150pàgines i s'han reobert els26QGZ dels ZIPs exactes
offline/readonly, amb164fitxers extrets inalterats. Es manté el dist pla.

La verificació de la sessió és a
`sandbox/practiques/lliurament-geodisseny/2026-10-30-organitzacio-01/`:
fonts abans/després, prosa i passes editorials preparades, `prerequisits01/`,
`portabilitat01/`, build del manual, revisió web/PDF i inventari d'autocorrelació.
El verificador de lots comprova70destinacions de carretera des de `sandbox/`,
10casos de format Windows i una còpia nativa de cinc files amb entrada i
sortides reassignades. Moure el QGZ no modifica el `.batch` original; les
lectures separen aquesta traça de la còpia preparada per reexecutar.

Les cinc mostres tècniques de `portabilitat01/` exporten un GeoPackage nou,
copien els recursos seleccionats i desen un QGZ extern relatiu. Els ZIPs
s'extreuen en una ubicació nova i es reobren sense els inputs originals:
atributs, FIDs, geometries i ràsters es mantenen, i el mapa coincideix píxel a
píxel. Són proves tècniques amb resultats retinguts, no treballs d'estudiants
ni nous paquets docents. No s'ha repetit cap anàlisi ni les179conques.

Abans de substituir el dist s'ha arxivat l'arbre anterior complet,
37fitxers i10directoris, a
`sandbox/practiques/arxiu-lliuraments/2026-10-30-abans-organitzacio-01/`.
`current-verified.json` del run02comprova independentment l'arxiu, les sumes,
els PDFs separats i els membres dels ZIPs. Els rebuts de la sessió són a
`final-checks.json` del run01; l'estat editorial gestionat continua intacte.

També s'ha inventariat la base per a una activitat d'autocorrelació separada:
94membres del segell municipal i dos ZIPs originals verificats,98potències
publicades i151seccions de renda. L'inventari no prepara una nova edició ni
qualifica el runtime actual per a aquella activitat. La continuació, els
apartats assignats, el codi i els requisits pendents són al traspàs del run01.

Les lectures són **candidates en review**, amb PDF marcat ESBORRANY.
L'aprovació anterior s'aplica només a la base retinguda, no a aquests documents
o projectes revisats. Càrrega a Moodle i publicació web continuen sent explícites.
Les seccions següents conserven l'historial dels preparadors i edicions anteriors.

## Estructura

```text
practiques/<practica>/
  preparar.py
  recursos.yml
  ca/alumnat/LLEGIU-ME.md
  ca/docent/LLEGIU-ME.md
sandbox/practiques/<practica>/<execucio>/
  fonts/
  controls/
  alumnat/
  docent/
  captures/
dist/practiques/<practica>/ca/
  <practica>.zip
  <practica>-docent.zip
  manifest.json
sandbox/practiques/arxiu-lliuraments/<execucio>/
  dist-practiques/
  original-tree.json
  verified.json
```

Per a les altres llengües, el document es diu `es/.../LEEME.md` o
`en/.../README.md`. Actualment aquest manual manté únicament català.
El nom dels ZIPs identifica la pràctica; la llengua és al directori i les dates
i versions són al manifest. El lliurament d'inici no inclou «alumnat» o «estudiants» al
nom del ZIP ni a l'arrel interna; els manifests sí que conserven el destinatari.

## Propietat i reconstrucció

- `practiques/`: fonts versionades, conservació permanent.
- `sandbox/`: dades originals/còpies datades, treball i evidència d'agent;
  ignorat, conservació explícita. Cap neteja general automàtica.
- `dist/`: ZIPs i manifest verificats de lliurament; ignorat, conservació
  explícita. S'hi copien només candidates completes des de sandbox.

Les URL, dates, llicències i hashes de `recursos.yml` i dels manifests de fonts
identifiquen les entrades. Els snapshots originals es conserven fora de Git;
si una font canvia, es prepara una versió nova en lloc d'atribuir-li el hash antic.
No s'inclouen GPKG, TIFF, PBF, QGZ, PDF o ZIP en aquest directori versionat.

Els recursos gràfics publicats al web segueixen els contractes dels seus
proveïdors. Les captures de les activitats es preparen amb la recepta/prompt
versionats i es conserven amb PNG, SVG i manifest del capturador a sandbox.
Els càlculs GIS es fan amb scripting/PyQGIS/GDAL/GRASS al contenidor QGIS fixat;
el PDF de lectura es compila amb el runtime PDF d'unaltraweb.

## Accessibilitat de Vila-seca

Fonts: [preparar.py](accessibilitat-vilaseca/preparar.py),
[recursos.yml](accessibilitat-vilaseca/recursos.yml),
[lectura de l'alumnat](accessibilitat-vilaseca/ca/alumnat/LLEGIU-ME.md) i
[resolució docent](accessibilitat-vilaseca/ca/docent/LLEGIU-ME.md).

La fase històrica `--organise` reutilitza el snapshot OSM de 2026-10-07;
no és la base de les revisions ICGC. Per revisar les lectures conservant el GIS
ICGC, utilitza `--reuse-icgc-from <run-ICGC-segellat>` amb `--run-id` i `--version`
nous. Comprova el manifest, les dades i les captures i en copia els bytes a un
run nou, sense recalcular ni modificar l'origen.
`--docs --pdf-receipts <carpeta>` incorpora els PDF construïts amb
`manual_practice_pdf_build` d'unaltraweb; `--package` crea els ZIPs nets a dist després
de les verificacions. Un paquet existent no se sobreescriu.

La versió local `2026-10-07-r2/ca` ja està segellada. Els ZIPs es diuen
`accessibilitat-vilaseca-2026-10-07-r2-ca.zip` i
`accessibilitat-vilaseca-docent-2026-10-07-r2-ca.zip`. Per revalidar els ZIPs
exactes de dist en una ubicació nova, amb QGIS readonly i sense xarxa:

```bash
python3 practiques/accessibilitat-vilaseca/preparar.py --verify-deliverables --version 2026-10-07-r2
```

La comprovació conserva un rebut en un run `verificacio-<id>` nou a sandbox.
No altera els ZIPs, les dades o els controls del run segellat. Per preparar
una revisió, cal seleccionar `--run-id` i `--version` nous i obtenir controls
QGIS/PDF actuals abans de `--package`; no executar les fases de preparació
amb els defaults de la versió segellada.

La revisió r2 canvia només els noms externs: s'han copiat els bytes dels ZIPs
verificats de `2026-10-07/ca` i els SHA-256 són idèntics. La fase
`--rename-deliverables-from <versio-anterior> --version <versio-nova>` conserva
candidats i rebuts en un run nou de sandbox i exigeix una versió de dist nova.
No recompila els PDF, recalcula dades o regenera captures.

Les fases GIS (`--fetch`, `--prepare`, `--build`, `--style-start` i
`--style-teacher`) s'executen amb aquest script dins del contenidor QGIS
declarat a recursos.yml, muntant el repositori readonly i només el run de
sandbox writable. Per als càlculs, xarxa desactivada; per descarregar, accés
explícit a les fonts declarades. `--run-id` selecciona un run nou i `--version`
una versió de dist nova. La recepta derivada `captures/config.yml` manté
el mateix consumidor i els seus paths, sense copiar runtime del proveïdor.

Contracte/plantilla comuna proposats a
[unaltraweb#98](https://github.com/dosquartsdedocs/unaltraweb/issues/98),
coordinats amb la preparació portable i ampliació GIS
[d'unaltracaptura](https://github.com/dosquartsdedocs/unaltracaptura-qgis/issues/4#issuecomment-6037676887).

## Edicions amb la plantilla compartida

La versió final aprovada s'identifica amb la data `2026-10-18`. El cas d'accessibilitat
es distribueix en tres subpràctiques, amb lectures d'inici/docents i ZIPs propis:

- [Xarxa vectorial](accessibilitat-xarxa-vilaseca/ca/docent/LLEGIU-ME.md): recta,
  connexions, ruta curta/ràpida i tancament de P2.
- [Model ràster](accessibilitat-raster-vilaseca/ca/docent/LLEGIU-ME.md): proximitat,
  cobertes, eixos viaris amb pes1, barreres/passos i r.cost/r.path.
- [Temps d'accés](accessibilitat-temps-vilaseca/ca/docent/LLEGIU-ME.md): àrees de
  servei, marxa, control pla i isòcrones. Rep friccions com a entrades inicials.

Les fonts de càlcul comunes continuen a `accessibilitat-vilaseca/preparar.py`.
Els preparadors dels tres blocs seleccionen elements existents del run comú
verificat; no repeteixen el càlcul ni copien un renderer o runtime del proveïdor.
`--seal-common` conserva l'índex/hash del càlcul i de les captures; el preparador
de cada bloc fa `--stage-module-from <run-comu> --run-id <run-nou> --version <data>`,
incorpora les lectures de `manual_practice_pdf_build` i selecciona els projectes
i recursos d'aula amb `--package`. No calen nous contractes d'edició nativa per
separar aquests elements. Constantí i visibilitat reutilitzen els seus bundles
natius i `edicio.json`, amb la mateixa versió de data.

Les guies docents inclouen estimacions de temps d'aula, treball autònom i
preparació, amb prerequisits i abast explícits. Són orientatives, no mesurades en
una classe. `context/writing-profile.md` conserva aquesta preferència opcional
del manual. La llargada del PDF no es fa servir com a indicador de durada.

Les versions `r2`–`r6` identifiquen les candidates anteriors i es conserven.
La data és suficient quan hi ha una edició al dia; un sufix només és necessari
per distingir-ne més d'una. Els SHA-256 dels manifests, inputs, fonts i paquets
identifiquen els bytes; no s'incorporen al nom visible del lliurament.

L'autor ha confirmat la finalització de les cinc pràctiques i la publicació del
web. Les deu lectures de lliurament tenen `content_status: approved`; els PDF es
tornen a construir amb el proveïdor compartit. El càlcul GIS i les captures
verificats del14/10es reutilitzen, amb rebuts nous de paquets i comprovacions.
Les dues lectures combinades d'accessibilitat continuen com a referència draft;
els lliuraments actuals són els tres blocs independents.

### Antecedents de les candidates

Preparació local de [la tasca11](https://github.com/geourv/geodisseny/issues/11),
amb els primers pilots de visibilitat/Constantí i l'actualització d'accessibilitat:

- `visibilitat-costa`: torxa de la Canonja, carretera TV-3148 i recinte
  petroquímic, conservant el domini, les cotes, el mostreig i els resultats r3.
- `estadistica-constanti`: 124 punts; recompte, centres, cercle/el·lipse i kernel.
  Moran/LISA/renda queden fora d'aquest pilot descriptiu.
- `accessibilitat-vilaseca`: comparació de distància euclidiana, camí ràster i ruta
  en xarxa al pas de l'AP-7. En el cas de Vila-seca, àrees de servei, marxa anisòtropa
  i isòcrones són propostes d'ampliació. L'enunciat conserva la qualificació 70/20/10 indicada
  per l'autor.

La revisió d'accessibilitat `2026-10-14-r5` substitueix físicament la xarxa OSM
de r4 per eixos RTT2024 de l'ICGC. `--stage-icgc --run-id <run-nou>` copia només
els cinc snapshots institucionals verificats; `--prepare` crea la xarxa amb
`rtt_id`, parts i connexions documentades. Els extrems són els de la demo ICGC;
la ruta oberta fa454,10m i retirar l'eix1354754 de P2 deixa el graf sense ruta.
Es recalculen la resta de controls afectats pels extrems, amb el runtime100…,
i es regeneren les quinze captures. OSM queda com a font alternativa explicada,
fora de les entrades actives d'aquesta edició.

Visibilitat i Constantí contenen el model d'activitat `preparar.py`, la declaració
de recursos, `activitat.json`, `edicio.json` i les dues fonts catalanes `LLEGIU-ME.md`.
Les primeres lectures es van preparar en **draft**. El camp `approved_sha256` del contracte del
compositor fixa els bytes seleccionats per l'autor; no modifica l'estat editorial
ni acredita aprovació humana d'aquesta preparació.

`--snapshot --run-id <nom-nou>` comprova el SHA del ZIP històric segellat i dels
membres seleccionats i els copia a un run nou de `sandbox/practiques/<slug>/`.
La petició executable resultant és `inputs/activitat.json`; el fitxer versionat
és la definició que el snapshot completa amb els hashes de totes les entrades.
No executar les fases antigues amb els defaults dels originals segellats.

La CLI pública QGIS0.6.0 `practice-run` executa aquesta petició amb l'engine100…
ja preparat, xarxa desactivada, fonts readonly i outputs create-only. El productor
és l'autoritat de membres GPKG, projectes, fonts, captures, closure i seal. Les
funcions de l'activitat seleccionen capes, controls i presentació; no implementen
un segon verificador GIS.

Els projectes **inici** i **docent** estan incorporats als seus GeoPackage.
El paquet d'inici selecciona només `initial-data` i la seua font local requerida:
dos productes GIS més `LLEGIU-ME.pdf`. El docent afegeix els resultats i recursos
necessaris, preservant rutes `payload/data/`. Fonts regionals, intermedis, controls,
rebuilds, captures de recuperació i scripts de reconstrucció no s'envien al Moodle.

`manual_practice_compose` d'unaltraweb0.7.2 consumeix `edicio.json`, comprova els
IDs/closures amb el verificador privat1fe… i construeix les dues lectures amb el
PDFworker618… i la plantilla comuna A4horitzontal. Retorna PDF separat, ZIP i
receipts; els logos, metadades i tipografia pertanyen al core, no al consumidor.
La configuració d'edició ha d'estar registrada a l'índex Git i no ignorada; la
preparació inicial només havia autoritzat stage dels dos `edicio.json`. La
confirmació posterior de l'autor autoritza commit/PR i publicació del web.

Versió d'aquesta revisió: `2026-10-14-r6/ca`, sota `dist/practiques/` de cadascun
dels tres slugs, amb noms de lliurament sense l'etiqueta provisional «pilot».
Les versions `pilot-01`, `pilot-02`, accessibilitat r2/r3 i els intents previs
romanen conservats. Les proves dels pilots `final-zip-proof-02` comproven inventari, CRC,
hashes, PDF separat idèntic a l'inserit, A4/límits de text i reobertura QGIS
offline sobre datasets/font extrets dels ZIP finals. El checkpoint QGZ de control
necessari per la interfície pública es conserva en el paquet privat de validació;
no s'afegeix al handout que utilitza el projecte incorporat al GPKG.

Accessibilitat r4 reutilitzava el GeoPackage i els projectes/resultats segellats;
r5 es reconstrueix amb els snapshots ICGC i controls QGIS nous. Executar les fases
QGIS en processos separats, amb el repositori readonly i el run writable.
`--verify-run` reobre les onze vistes docents i comprova la xarxa ICGC i la resposta
sense ruta abans de `--package`. La captura host necessita el consumidor explícit
a `MCP_CONSUMER_WORKSPACE`, les variables natives de workspace/host-workspace i
UID/GID; la carpeta de configuració no és un checkout alternatiu.
`manual_practice_pdf_build` prepara les lectures amb el mateix PDFworker
compartit; `preparar.py --package --run-id <run-nou> --version <versio-nova>` incorpora
els PDF comprovats i els recursos d'aula. `--verify-deliverables --version <versio>`
reobre els ZIP finals readonly, sense xarxa, amb el runtime fixat de la pràctica.
Els rebuts del nou run identifiquen el productor dels PDF i els hashes de les fonts.

Els tres documents docents comencen amb les instruccions per adjuntar el ZIP
d'inici a **Fitxers addicionals** d'una Tasca de Moodle i un enunciat per copiar a
**Descripció**. Les dades/projecte i la lectura d'inici van al paquet de l'alumnat;
la resolució i els resultats són al paquet docent. La pujada a Moodle la fa l'autor.

La revisió r6 canvia les sis lectures: el professor seleccionarà a classe els
apartats obligatoris del 70% i els recollirà a Moodle. Les ampliacions obren
preguntes, canvis de zona, repeticions controlades i aplicacions geogràfiques per
aspirar a l'excel·lent. La pauta d'informe inclou l'enregistrament de pantalla com
a ajuda per extreure captures comentades, sense convertir el vídeo en un
lliurament obligatori. Aquest contingut específic de les pràctiques del grau
pertany al consumidor, no a la plantilla o al runtime d'unaltraweb.

Per a accessibilitat r6 es reutilitza el run ICGC segellat `2026-10-14-r5-02`:

```bash
python3 practiques/accessibilitat-vilaseca/preparar.py --reuse-icgc-from 2026-10-14-r5-02 --run-id 2026-10-14-r6-01 --version 2026-10-14-r6
```

Les captures conservades mantenen els manifests originals i s'identifiquen com
a reutilitzades, no com un render nou. Les verificacions QGIS/PDF i els paquets
s'obtenen en el run nou. Constantí i visibilitat reutilitzen els bundles natius
segellats declarats a `edicio.json`. Totes les versions anteriors es conserven.
