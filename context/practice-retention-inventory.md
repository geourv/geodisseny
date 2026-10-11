# Índex de retenció de la pràctica d'accessibilitat

Conservació de [Geodisseny #9](https://github.com/geourv/geodisseny/issues/9), abans de la cohort persistent. És un índex textual de fonts, artefactes i punts restaurables coneguts: **no és un backup complet**, no acredita una còpia externa i no autoritza eliminar originals. Cap dada s'ha mogut o restaurat per elaborar-lo.

Workspace de procedència: `/home/benizar/git/geodisseny`, branca `content/9-accessibilitat-inici`. Base anterior a la conservació: `5c904a386048bf317ca45cab6d42e0965f0ce0d6`.

Punt Git de les fonts draft: `eb98496dcc0f1cf2cd0d913da989658a11023b17` (segon commit de conservació). L'handoff i aquest índex s'afegeixen al commit de metadades següent.

## Fonts versionades i esborranys

Les dues lectures mantenen `content_status: draft`; les 17 captions no concedeixen aprovació editorial. El preparador legacy es conserva per reconstrucció històrica. El request/model compartit cobreix només D/E i encara reté el cas TFW fallit; no acredita un bundle final ni una reexecució completa A–G.

| Font | SHA-256 |
| --- | --- |
| `practiques/accessibilitat-vilaseca/ca/alumnat/LLEGIU-ME.md` | `729ab79061ff20133898e0c6c0974f6fc1ebf98f7c2db347fafa5da02b42f9d0` |
| `practiques/accessibilitat-vilaseca/ca/docent/LLEGIU-ME.md` | `e4b0f086759ec03bacecd62827becb37e417e8dc3ae32b986f246a85a8ba9e54` |
| `practiques/accessibilitat-vilaseca/preparar.py` | `ac118655cd13fed87074f7ca9e253d359da2a683a792b80e9301a081c4be9f23` |
| `practiques/accessibilitat-vilaseca/recursos.yml` | `7766ee3bb8327462f3eae7339eab072e0bd6c5615c6aa85c06b816117f46e307` |
| `practiques/accessibilitat-vilaseca/activity-cost-p2.json` | `b4e9494c889420cb12688456cb12310b8096bff9a7a5da1d54587623af9b54d2` |
| `practiques/accessibilitat-vilaseca/compute_cost_p2.py` | `12395d3742d1258ef56a506e0675402ffcb84a104a862cf7859400016015c4af` |
| `context/practice-tools-handoff.md` | `0eeb3d7effd2d6227af23cc1b84c3fe566229224492491002201a03759406b19` |

Prompt/recepta de captures: `context/qgis/accessibilitat-inici.md` i `context/qgis/accessibilitat-inici.yml`. Procedència i inventaris històrics: `context/dades/accessibilitat-inici.md`, `context/dades/practiques-territorials.md` i `recursos.yml` de la pràctica.

### Fonts anteriors recuperables

| Punt restaurable | SHA-256 | Procedència |
| --- | --- | --- |
| `context/practiques/distancies-vilaseca.md` al commit base | `78b71f998cf2f1da74801d512b26b050c043e258c2ecd1f99fd16b6c15688aa5` | Blob Git del commit `5c904a386048bf317ca45cab6d42e0965f0ce0d6` |
| `context/practiques/distancies-vilaseca-docent.md` al commit base | `7a93b5913ec08c615ececcedd62ba4edab301ac2a31cf144cbc64d51d9a323e8` | Mateix commit; versió docent anterior |
| Lectura d'inici abans de captions | `2b143ca541a6d5a84bea9d1c2b8e7e5641f6f81fe514f9141cebc06886057953` | `sandbox/practiques/accessibilitat-vilaseca/lectura-2026-10-09-pdf-01-ca-alumnat-ga32-alumnat-01/inputs/original.md` |
| Lectura docent abans de captions | `8b54fe7842cb0847a54f57dbfb2fa6edf46af9669b5f5bde0dae45b357d814` | `sandbox/practiques/accessibilitat-vilaseca/lectura-2026-10-09-pdf-01-ca-docent-ga32-docent-01/inputs/original.md` |

Recuperar aquestes versions com a còpies en una ubicació nova, mai sobre la font actual de l'autor. Els logs i inputs complets dels dos jobs fallits es conserven.

## Reconstrucció A–G i captures, fora de Git

Arbre essencial complet: `sandbox/practiques/accessibilitat-vilaseca/2026-10-07-organitzacio/`, amb fonts datades, projectes, estils, ràsters, controls, reproducció, captures editables i lliuraments. El segell declara `private-author-review`, `human_approved:false`; no equival a aprovació ni publicació.

| Inventari/rebut | SHA-256 |
| --- | --- |
| `MANIFEST.json` del run | `76797be19402c77838f986130545e8f07e48dda77570b58134dcb8e52e1b47fe` |
| `sealed.json` del run | `23380ef60b88149e5c6f256ce4207ca5e572c5dc38a7365b872c9dc814368ea0` |
| `fonts/fonts.json` del run | `cf41b4d9a58eeda9e51222c3e800ef80650ad3414efd7dfbae705041dbea0792` |

El GeoPackage d'inici `alumnat/accessibilitat-vilaseca.gpkg` té 29.130.752 bytes i SHA `46d326819ad05f328eec12d34026956adcd3bfec9facbefeee226068fee03593`; conserva dades, ràsters, estils i projecte incrustat. La preservació dels projectes docents requereix les dependències completes inventariades, no només els QGZ.

Captures: conservar `captures/` complet, incloent PNG originals, SVG editables, manifests i config/recepta derivades. Els quinze PNG utilitzats per les lectures estan enumerats amb hashes als trenta bindings d'`_config.yml`, SHA `6976747137ecc27bb35832cb86271b7fdd46a4857d42e9bb0266487b38833a0e` de la configuració completa d'aquesta conservació. El manifest del run reté l'arbre; els PNG incrustats al PDF no substitueixen els originals editables.

### Originals i baselines requerits

| Font/entrada retinguda | Punt conegut i procedència |
| --- | --- |
| Divisions ICGC20/1/2026 | `tmp/dades-docents/originals/icgc-20260120/divisions-administratives-v2r2-20260120.gpkg`, SHA `99b864527af667d8c1ac2dcb814039c8328d03f0cd3d3faf24274878f5b14e61` |
| RTT original local | `tmp/dades-docents/practiques/rtt-original.gpkg`, requerit pel preparador legacy; preservar el fitxer encara que aquest índex no n'acredite un checksum independent |
| Passos i geometria històrica | `tmp/dades-docents/qgis/distancies-vilaseca-20261001-ampliada/`, entrada readonly del preparador |
| Primera preparació compacta | `tmp/dades-docents/qgis/accessibilitat-vilaseca-20261006-inici/`, amb manifest/segell i rebuts dels paquets anteriors |
| Baseline de guies detallades | `tmp/dades-docents/qgis/accessibilitat-vilaseca-20261007-guies/`, origen de la fase d'organització i de captures històriques |
| PBF OSM/Geofabrik5/10/2026 | `fonts/cataluna-261005.osm.pbf` del run: 271.098.804 bytes, SHA `522f5a71ae966c02d76935b6cecabb09eea6f0c9ad8443c33867cb89c6417959`, ODbL1.0 |
| Retalls ICGC/OSM locals | `fonts/` del run; `fonts.json` enumera municipi, cobertes2024, eixosRTT2024, xarxaOSM, MDT5m i ortofoto2025 amb URLs, dates, derivació i hashes |

Les URL són procedència, no substituts dels snapshots datats. Conservar també els ZIPs històrics i receipts sota `tmp/dades-docents/` que enumera `context/dades/accessibilitat-inici.md`; aquest índex no autoritza netejar altres pràctiques o fonts.

## ZIPs r2, fora de Git

Directori `dist/practiques/accessibilitat-vilaseca/2026-10-07-r2/ca/`:

| Fitxer | Bytes / membres | SHA-256 |
| --- | --- | --- |
| `accessibilitat-vilaseca-2026-10-07-r2-ca.zip` | 27.598.739 / 2 | `d936d1b56b9ab811140493a9413843e81d362f0ccf350c4a848a9c77323a71e9` |
| `accessibilitat-vilaseca-docent-2026-10-07-r2-ca.zip` | 46.704.358 / 50 | `f7425f063993404ce1382f45e149fb172cdf8cc31b160a6ae4d13a501a05c5ab` |
| `manifest.json` | Inventaris, procedència i hashes dels membres | `d6df721994e61c8fd9896156023d77301371a438baf12d1e1e89296813c3be4b` |

El manifest declara `human_approved:false`, `site_release:null`; r2 canvia els noms externs, mantenint les bytes de `2026-10-07/ca/`. Conservar aquesta versió anterior i el candidat/rebut de noms `sandbox/practiques/accessibilitat-vilaseca/lliurament-2026-10-07-r2-1791389965658026899/`.

Reobertura exacta ja comprovada offline/readonly: onze capes inicials, onze projectes i52fitxers intactes. Rebuts `sandbox/practiques/accessibilitat-vilaseca/verificacio-1791376481466443348/verified.json` i `sandbox/practiques/accessibilitat-vilaseca/verificacio-1791389969352194110/verified.json`. Conservar-los amb els ZIPs; no s'ha repetit la verificació GIS en aquest torn.

## PDF revisats i snapshots de render, fora de Git

Roots de job:
- `sandbox/practiques/accessibilitat-vilaseca/lectura-2026-10-09-pdf-02-ca-alumnat-ga32-alumnat-02/`
- `sandbox/practiques/accessibilitat-vilaseca/lectura-2026-10-09-pdf-02-ca-docent-ga32-docent-02/`

Conservar els dos arbres sencers: `inputs/`, font original/efectiva, assets, plantilles/filters, outputs, logs i `receipt.json`. Cada receipt inventaria40artefactes verificats anteriorment. A4 horitzontal, fonts incrustades i primera pàgina inspeccionada; revisió visual completa de l'autor pendent.

| Lectura / artefacte relatiu al job | Bytes / pàgines | SHA-256 |
| --- | --- | --- |
| Alumnat `outputs/LLEGIU-ME.pdf` | 9.347.186 / 38 | `80c5a67275749acc1fada5904a8ba08b122b2a845149ae0ea67ef4678ab4feba` |
| Alumnat `receipt.json` | Inventari del job | `0ab625749998a2ffddd8737634e74a8c128fbaff54a7aaee644e57b333e4f4c3` |
| Docent `outputs/LLEGIU-ME.pdf` | 9.309.728 / 32 | `9e123b02bfd7bafba0db5938b3b3d1fc5dbb5eac7434b76345af688e12f50756` |
| Docent `receipt.json` | Inventari del job | `d6ead474522206086b3a89e4e36673995a4dcd4302f72541e8c74fb61cb4a34e` |

Proveïdor de render: PDF worker digest `1bb3f2dafd741e96c28639ec1cc8ccaeb81cbaa73e649f787c0b4ef59997bd4b`, image ID `sha256:618163d3f924439792b2306617bd9612f566c5881166102fa544b4e782d569fa`. Els receipts vinculen aquests pins amb font, `_config.yml`, quinze captures i logos. La plantilla està preservada als inputs; no s'ha rerenderitzat ni publicat.

## D/E: inputs i evidència parcial

Packet actual readonly `sandbox/practiques/accessibilitat-vilaseca/2026-10-09-cost-p2-inputs-04/`: `activity-cost-p2.json`, `compute_cost_p2.py`, `accessibilitat-vilaseca.gpkg` i `origin.json`. Els primers tres fitxers tenen els SHA de font/seed anteriors; `origin.json` SHA `2d17a5f3f0c197241dfa6d5f7dbef2b391476856abea427da2a5ffe84ecb1cce` registra source/target/bytes. Conservar també packets01–03.

Job de càlcul: `sandbox/qgis-practice-jobs/practice-1d1c629b35204b90b12e4e75bbeb69eb/`, report `compute-5d23f413f55a/report/result.json`, SHA `ae526c430e1bafd0541c5b50fb4f36720dfbabda46848e223e599e119b852f6e`. Reté13algorismes executats i24controls; costos aD1336,9900782009827/4548,731957466707m ponderats, rutes441,98484809834997/1639,2135623731024m. Preservar `work/`, TIFF/TFW raws, fonts, projectes/captura i `reopen-1fb66186cad9/report/result.json`.

Intents propis anteriors que també es conserven a `sandbox/qgis-practice-jobs/`:
- `practice-488409c0dd0f43c6ad2b44d2ae6e4422/`
- `practice-eff712044bde4dcd9a08130dbc090bf5/`
- `practice-a5582c9f98994eff9a188b81c334793e/`
- `practice-98a4d44ca63b480d8b07fa0f12f46958/`

No eliminar altres jobs per absència d'aquest índex. S'han enumerat els cinc roots presents al directori del consumidor, no auditat exhaustivament cada fitxer del registre. **No hi ha bundle D/E propi segellat acreditat.**

## Patró TFW del productor, rebut i no aplicat

Paquet públic `/tmp/opencode/practice32-grass-geotiff-readiness/`, ready SHA `7ee0a1f5980e629026a68d357bfbcb2fa50d25e0780f561048b9c792c5fbdf92`. Els cinc fitxers s'han contrastat amb el marker:

| Fitxer | SHA-256 |
| --- | --- |
| `GUIDE.md` | `42e4042f21d182be44657a80046b454a88eecc55b9e2bf3290ca1fcb30752f43` |
| `normalise.py` | `1feb01d4930e0475be95ba8263587ecbc08ff92ae36c80b9d53562df80dd83c2` |
| `equivalence.json` | `93e5124cb5571140efc6e25ede4a70307a68b4c212b0620965bb91b49b662505` |
| `results.json` | `68a5c4be24d0d16d32573ad0797bad94655d182ba33a6656789ebf3937249b84` |
| `mcp-identity.json` | `d0a3fa1de1e3e69601907c010f94684e9706bb2f6de8a608123274feb8c43581` |

Bundle tècnic del productor,31fitxers: `/tmp/opencode/practice32-grass-geotiff-01/consumer/runs/normalized01/bundle.json`, SHA `9fe6f9c334fcc8216028fe858ce4c31b0e9362f9f98e6d6932b54221a8820750`. L'owner/hub conserva l'arbre complet i els raws originals; la carpeta readiness conté només la guia/callback/evidència. No és el resultat científic de Geodisseny ni acredita l'adopció local. El patró `gdal:translate` és unitat posterior, amb els mateixos24controls/toleràncies i sortides noves; cap `.tfw` s'ha suprimit per fer passar el checker.

## Eines i pins: historial, no instal·lació persistent

El handoff registra adapter host pin `2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a`, controller17ef0…, fingerprint5b8de… i CLI QGISrc2 wheel1a7456… a `/tmp/opencode/`. La config local ignorada `.opencode/opencode.json` té SHA `f5eea95f897c73bcc8f493c0946583cd946e2bc18b93e5e29bd4b05f61a669d8`; no entra al commit.

Segons el coordinador, QGIS0.6.0 ja està merged/publicat amb18assets i receipts privats. Els owners/hub lliuraran els pins i la cohort persistent; **no es publicarà una wheel QGIS privada dins d'una imatge Web pública**. Web prepara la delegació al runtime QGIS privat; CI compartida pendent de Web0.7.2published. No s'ha instal·lat cap successor ni canviat Make/Gem/workflow en aquesta conservació.

Retenció durable posterior pels owners/hub: wheels, locks, schemas, guies, manifests i arxius OCI necessaris, amb hashes i accés corresponent. No copiar/moure venvs ni volums aliens. Els pins legacy de reconstrucció són a `recursos.yml`; els nous no substitueixen retrospectivament la procedència dels outputs antics.

## Restauració i límits

1. Recuperar les fonts des del punt Git indicat, i les versions anteriors des del commit base o dels snapshots de render, en una còpia nova permesa per l'autor.
2. Restaurar els arbres privats complets preservant paths relatius i totes les dependències. Contrastar manifest/segell/receipts, bytes i hashes; no sobreescriure material d'autor ni buscar fonts de substitució per coincidència de nom.
3. Per a una nova verificació, reobrir una còpia dels ZIPs/projectes en una ubicació separada, readonly/offline amb el runtime pinat i sense fallback al checkout. GIS i closure els verifica el productor; snapshots PDF es contrasten amb els seus receipts.
4. Preparar una còpia externa durable amb inventari en una destinació ja autoritzada per l'autor, i verificar-ne la restauració. **Aquesta operació no s'ha fet:** actualment es conserven els fitxers locals i aquest índex, no un backup integral certificat.

Fonts draft, revisió visual/aprovació, normalització D/E, bundle/reobertura/edició final, CI compartida i instal·lació persistent continuen pendents. Consolidar Git no publica el web ni Moodle. `make clean` eliminaria originals sota `tmp/`; aquest índex no autoritza clean ni cap altra neteja.
