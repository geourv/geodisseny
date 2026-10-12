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

La fase `--organise` reutilitza la darrera pràctica segellada verificada en un
run de sandbox nou; no repeteix els càlculs ni modifica els originals.
`--docs` compila els documents; `--package` crea els ZIPs nets a dist després
de les verificacions. Un paquet existent no se sobreescriu.

La versió local `2026-10-07-r2/ca` ja està segellada. Els ZIPs es diuen
`accessibilitat-vilaseca-2026-10-07-r2-ca.zip` i
`accessibilitat-vilaseca-docent-2026-10-07-r2-ca.zip`. Per revalidar els ZIPs
exactes de dist en una ubicació nova, amb QGIS readonly i sense xarxa:

```bash
python3 practiques/accessibilitat-vilaseca/preparar.py --verify-deliverables
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
