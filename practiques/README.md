# Fonts reproduïbles de les pràctiques

Aquest directori conté **codi, configuració de recursos i documents editables**.
Es versiona a Git i està exclòs de Jekyll. Les activitats es publiquen com a
paquets de Moodle, amb una versió pròpia independent del manual.

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
dist/practiques/<practica>/<versio>/ca/
  <practica>-<versio>-ca.zip
  <practica>-docent-<versio>-ca.zip
  manifest.json
```

Per a les altres llengües, el document es diu `es/.../LEEME.md` o
`en/.../README.md`. Actualment aquest manual manté únicament català.
El nom dels ZIPs identifica la pràctica, la versió/data i l'idioma quan es
copia a Moodle. El lliurament d'inici no inclou «alumnat» o «estudiants» al
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
