# Índex de retenció de les pràctiques

Conservació inicial de [Geodisseny #9](https://github.com/geourv/geodisseny/issues/9), abans de la cohort persistent. És un índex textual de fonts, artefactes i punts restaurables coneguts: **no és un backup complet**, no acredita una còpia externa i no autoritza eliminar originals. En elaborar la primera versió no es van moure ni restaurar dades. Les seccions finals documenten els trasllats verificats de les distribucions del21,26,27i30/10/2026; els apartats anteriors conserven l'estat històric.

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
| Lectura docent abans de captions | `8b54fe7842cb0847a54f57dbfb2fa6edf46af9669b5f5b5bde0dae45b357d814` | `sandbox/practiques/accessibilitat-vilaseca/lectura-2026-10-09-pdf-01-ca-docent-ga32-docent-01/inputs/original.md`, 19.827 bytes; digest64recalculat sobre les bytes preservades i coincident amb el handoff |

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

## Restauració i límits de la conservació inicial

1. Recuperar les fonts des del punt Git indicat, i les versions anteriors des del commit base o dels snapshots de render, en una còpia nova permesa per l'autor.
2. Restaurar els arbres privats complets preservant paths relatius i totes les dependències. Contrastar manifest/segell/receipts, bytes i hashes; no sobreescriure material d'autor ni buscar fonts de substitució per coincidència de nom.
3. Per a una nova verificació, reobrir una còpia dels ZIPs/projectes en una ubicació separada, readonly/offline amb el runtime pinat i sense fallback al checkout. GIS i closure els verifica el productor; snapshots PDF es contrasten amb els seus receipts.
4. Preparar una còpia externa durable amb inventari en una destinació ja autoritzada per l'autor, i verificar-ne la restauració. **Aquesta operació no s'ha fet:** actualment es conserven els fitxers locals i aquest índex, no un backup integral certificat.

En aquella conservació continuaven pendents les fonts draft, revisió visual/aprovació, normalització D/E, bundle/reobertura/edició final, CI compartida i instal·lació persistent. Consolidar Git no publica el web ni Moodle. `make clean` eliminaria originals sota `tmp/`; aquest índex no autoritza clean ni cap altra neteja.

## Distribució i arxiu verificat, primera passada del 21 d'octubre de 2026

Aquest apartat conserva l'estat anterior a la revisió de noms tècnics i de lots
descrita a la secció següent. Les seves sumes no identifiquen el dist posterior.

La continuació de [Geodisseny #13](https://github.com/geourv/geodisseny/issues/13#issuecomment-6301371361) conserva els canvis de la mateixa branca `content/13-viewshed-lots`. L'autor ha demanat noms senzills i només el lliurament actual a dist. S'ha preparat i verificat el candidat nou abans de moure l'arbre antic; no s'ha eliminat cap versió.

L'arbre anterior complet de `dist/practiques/` és ara a:

`sandbox/practiques/arxiu-lliuraments/2026-10-21-distribucions-anteriors-01/dist-practiques/`

Es conserven **184 fitxers i 67 directoris**, incloent rebuts, fitxers ocults i directoris buits. L'inventari anterior al trasllat i la comprovació posterior coincideixen en paths, bytes i SHA-256. En particular, el lliurament aprovat del18/10 és a `dist-practiques/lliurament-moodle/2026-10-18/ca/` dins d'aquest arxiu; les rutes de dist dels apartats històrics s'han de resoldre sota aquesta arrel arxivada.

| Inventari o rebut | SHA-256 |
| --- | --- |
| `original-tree.json` de l'arxiu | `eb249013187a72ab14d988dc448b88a98606710b7b883d7b3f045a8d093039c5` |
| `verified.json` de l'arxiu | `d0a3ab8b238a4e3f27a031163f3feb584b0034bdde432085dca7dce57c14191b` |
| `dist/practiques/manifest.json` actual | `cb525f0baefd8f1839565034bf5f065d93acd76e7fa217a9e8839529457eab7e` |
| `published-current.json` del run del curs | `ee8085073341361fe2cd4cd5042349ec7d43cc27933900af9fb74a200bca4ca5` |

La distribució actual conté només les cinc activitats sota `dist/practiques/<slug>/ca/`: `accessibilitat-xarxa-vilaseca`, `accessibilitat-raster-vilaseca`, `accessibilitat-temps-vilaseca`, `estadistica-constanti` i `visibilitat-costa`. Cada carpeta té `<slug>.zip`, `<slug>-docent.zip`, les dues lectures `alumnat/LLEGIU-ME.pdf` i `docent/LLEGIU-ME.pdf`, l'enunciat editable `docent/ENUNCIAT-MOODLE.md`, manifest i `SHA256SUMS`. Els cinc fitxers de sumes s'han comprovat després de la promoció.

Reconstrucció actual: `sandbox/practiques/lliurament-geodisseny/2026-10-20-revisio-02/`. Conservar-ne tot l'arbre: `source/` amb els deu ZIPs aprovats, `source.json`, `classroom/`, `context.json`, `packages/review03/`, `reopen02/`, `published-current-source.py` i `published-current.json`. Els projectes inclouen el retall d'ortofoto local i el WMS oficial opcional, desactivat; conservar `ortofoto-wms.xml`. Les dades d'anàlisi vectorials i ràster s'han mantingut, però les taules de projecte dels GPKG han canviat: no són fitxers byte-idèntics als de la base aprovada.

Els deu ZIPs candidats exactes s'han reobert en una ubicació nova, sense xarxa, readonly i sense muntatge del workspace original: **21 projectes vàlids i 130 fitxers extrets inalterats**. Prova: `reopen02/proof/qgis.json`, SHA `a7a0c607852773840fab1967ac74588a514e690cabceb738f96a1e4fb0ae76b4`; vinculació als paquets: `packages/review03/verified.json`. L'engine és `sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2` (QGIS3.44.11/GDAL3.10.3).

Fonts i rebuts de la revisió de lectures, captures i manual: `sandbox/practiques/visibilitat-costa/2026-10-20-revisio-01/`. Conservar `final-pdf-receipts/`, `pdf-review-02/`, `browser-review-01/`, `manual-pdf-review-01/`, les comprovacions funcionals i els rebuts MCP de captures. El PDF complet local té225pàgines i SHA `5ad750b46cf63d9bf0d19cc205459d6451594416d6daa4e575c051018a42e08d`; la revisió visual seleccionada no equival a una nova lectura íntegra del manual.

L'edició actual és **review/ESBORRANY**, sense aprovació humana nova ni càrrega a Moodle/publicació web. Les captures noves0.6.1 acrediten pantalla privada Xvfb. Continuen pendents les captures de taula real de lots i del camp avançat desplegat: [unaltracaptura-qgis#26](https://github.com/dosquartsdedocs/unaltracaptura-qgis/issues/26). El nou collector és propi del curs, no un verificador natiu ni un runtime del proveïdor. L'arxiu és local; continua sense haver-se acreditat un backup extern durable.

## Noms tècnics i lots després de la prova d'aula, 21 d'octubre de 2026

Reserva de continuació:
[Geodisseny#13](https://github.com/geourv/geodisseny/issues/13#issuecomment-6313580131).
El dist actual conté `accessibilitat-xarxa-vectorial`, `accessibilitat-raster`,
`accessibilitat-temps-acces`, `analisi-intervisibilitat` i
`estadistica-espacial-descriptiva`, cadascun amb `ca/`, dos ZIPs de nom senzill,
les lectures separades i `docent/ENUNCIAT-MOODLE.md` fora del PDF.

Abans de substituir-lo s'ha arxivat tot l'arbre vigent del20/10: **37fitxers i
20directoris**, amb inventari abans del trasllat i comprovació independent de
paths, bytes i hashes després. Es troba a
`sandbox/practiques/arxiu-lliuraments/2026-10-21-abans-noms-tecnics-01/dist-practiques/`.
No s'ha alterat l'arxiu anterior de184fitxers, que continua conservant la base
aprovada del18/10 i els lliuraments més antics.

| Rebut | SHA-256 |
| --- | --- |
| `original-tree.json` del nou arxiu | `e8e07a8cddd2660d54d755f94a7fc3fcaf20e828411a887fd90d22dd6ac5b4cb` |
| `verified.json` del nou arxiu | `16aea344eeb0438355e6a1414d7118de23dd42960103137a78db2090c77138f7` |
| `dist/practiques/manifest.json` actual | `93f685b30170b2cd3762aa4cc90c51a138ff0fe8ccd6d67f2b4748a430cd3c0d` |
| `published-current.json` del run actual | `85d6e8b89257aea1644b91510ad5eb626abee8a17eecbd5234457635fa97a612` |

Conservar complet
`sandbox/practiques/lliurament-geodisseny/2026-10-21-lots-01/`: deu ZIPs aprovats
retinguts, projectes amb títols tècnics i context local/WMS, paquetsreview01,
reopen01, fonts i rebuts de promoció. Els **21projectes** dels ZIPs exactes s'han
reobert en una ubicació nova, readonly/offline, amb fonts confinades i tots els
fitxers extrets inalterats. Els noms interns dels casos geogràfics conserven la
procedència; només canvien els noms visibles i la presentació de projecte.

Conservar també
`sandbox/practiques/visibilitat-costa/2026-10-21-lots-01/`: reproduccionsui02,
provesworkflow02/later01/expressions01, rebuts PDF originals, els deu PDFs/ZIPs
seleccionats per hash, totes les pàgines de preview, revisió browser/manual,
`REVISIO-RETINGUDA.json` i `final-handoff-checks.json`. Els intents anteriors,
inclòs el job PDF acabat amb resposta de client perduda pel timeout, es conserven.
La segona crida utilitza jobs nous; no s'ha sobreescrit cap job segellat.

S'han reproduït els zeros de Calculate amb un array sencer, comprovat Add Values
amb retirada de la fila buida,5/37files amb coordenades i sortides correctes,
13expressions de la guia actual, casos escalars28/57, suma nativa dels5/37TIFF
i NoData255/−9999 en sortides reals. No s'han repetit les179conques.

Les deu lectures estan enreview; intervisibilitat té41pàgines d'inici i9docents.
El manual complet local continua amb225pàgines, ara amb SHA
`daed81f01c34609c55922b3327ca88f802a40edc54573cd9ebeedc7a60eb2428`.
Les captures de taula i EXTRA desplegat continuen pendents d'owner#26; les proves
programàtiques dels widgets no es fan passar per captures del MCP. Cap aprovació
humana nova, commit, push, deploy o càrrega Moodle. Continua essent retenció local,
no un backup extern certificat.

## GeoTIFF, projectes QGZ i carpetes de lliurament, 26 d'octubre de 2026

L'autor ha acceptat ràsters GeoTIFF separats, vectors GeoPackage i projectes QGZ
externs amb rutes relatives per a les cinc pràctiques. Els ZIPs actuals tenen
`pdf/LLEGIU-ME.pdf` i `data/`; els ràsters són sota `data/rasters/`, sense la
carpeta visible `payload`. L'enunciat Moodle continua en un fitxer editable
separat. La selecció d'inici no incorpora resultats resolts.

Reconstrucció completa:
`sandbox/practiques/lliurament-geodisseny/2026-10-26-pdf-data-01/`.
Conservar `source/`, `source.json`, `classroom/`, `context.json`, els dos passes
de `handouts/`, `diagnostics/uri01/`, els snapshots de documents/control,
rebuts PDF, `packages/review01/` i `review02/`, les tres reobertures, els previews,
`REVISIO-RETINGUDA.json`, `handoff-checks.json`, `published-current-source.py`,
`published-current.json` i `current-verified.json`. El passlayout01 es va aturar
per la diferència Undefined/Gray d'una banda numèrica; el passlayout02 conserva
els valors i normalitza explícitament només aquesta convenció de representació.
Es conserva també l'intent PDF inicial fallit pel muntatge Docker i la primera
prova de moviment aturada pel seu ordre d'inserció/eliminació de nodes; no s'han
reescrit com a execucions correctes.

Els22GeoTIFF extrets conserven píxels, tipus, graella, CRS, NoData i màscares.
Els vectors conserven FIDs, atributs i geometries. Els26projectes dels ZIPs
finals s'han reobert readonly/offline en una ubicació nova, sense muntar el
checkout: fonts confinades, ortofoto local/WMS opcional i ordre del canvas
coincident amb l'arbre després d'afegir i moure una capa de dalt a baix i amunt.
Els164fitxers extrets romanen inalterats. Els deu PDFs són A4horitzontal,
amb codi i límits de text comprovats; totes les pàgines s'han revisat visualment.

La fallada Viewshed aportada per l'autor s'ha reproduït amb QGIS3.44.11 i
GDAL3.10.3: un projecte incrustat dona `@project_folder` amb `geopackage:`;
desar-lo com a QGZ dona una carpeta ordinària. La mateixa concaC05 es calcula
correctament amb l'MDT GPKG i GeoTIFF i coincideix píxel a píxel. Només s'han
calculat aquestes dues conques de contrast, no les179històriques. Això no
diagnostica els altres episodis de compatibilitat de l'aula.

L'arbre anterior complet del21/10,37fitxers i20directoris, és íntegre a
`sandbox/practiques/arxiu-lliuraments/2026-10-26-abans-geotiff-01/dist-practiques/`.
Comprovació independent de paths, bytes i tots els hashes abans/després:

| Rebut | SHA-256 |
| --- | --- |
| `original-tree.json` del nou arxiu | `a534e345817a28c70974ed1363d2366860df9e51bbd6e38ac10f29a4f0619bfe` |
| `verified.json` del nou arxiu | `e08241377f939dc1ca3b425545d311a4eb5243d86815c087d6589e205cf50e3e` |
| `dist/practiques/manifest.json` actual | `b46eba7341e604b568ab6d52056370ae746490a5155d21efa1c77a726a0d56c5` |
| `published-current.json` del nou run | `9a31245106dce0e67eb573953c178ab49daeb8b9c01447607d09239a10da910d` |
| `packages/review02/packages.json` | `283b2b90c8d3d780d53bd81ca9cd7cb206ed16700c1c236037137a87790b00e6` |

Deu passes copy preparats/retinguts contra revision123 i enunciats revisats
manualment; estat editorial tool-owned intacte. Les captures existents es
reutilitzen; la taula nativa de lots i EXTRA desplegat continuen pendents de#26.
L'edició26/10és **review/ESBORRANY**. Sense aprovació humana nova, commit, push,
deploy o càrregaMoodle. Pins/scaffold i configuracióMCP preservats; la publicació
latest vigent no s'ha modificat. Continua sense acreditar-se un backup extern.

## Desenvolupament teòric descriptiu, continuació del 26 d'octubre de 2026

Run de comprovació i revisió:
`sandbox/practiques/estadistica-constanti/2026-10-26-teoria-01/`.
Conservar-ne `inputs/`, `sources.json`, `check01/`, `docker-check01.json`, les
tres passes de build/browser/PDF, `final-sources/`, `REVISIO-RETINGUDA.json`,
`final-checks.json` i `LLIURAMENT.md`. La font executable és
`practiques/estadistica-constanti/comprovar-teoria.py`.

El capítol4desenvolupa coordenades mitjanes, quadrats, variàncies, covariància,
semieixos i orientació amb cinc punts construïts, abans dels124registres.
Distingeix dades, càlculs i opcions de malla/KDE/dibuix. Els controls existents
es confirmen sense alterar les figures: radi2.000,66m, semieixos1.934,44/510,47m
i azimut110,22°. El recompte d'interiors és86al cercle i68a l'el·lipse; la
cobertura normal bidimensional s'explica amb font bibliogràfica verificada.

Font final del capítol:
`f90e52770ae931507a706a9f7fb7950bbe55cb35e88e2cc8f4961a5fd9e24fad`.
El manual local té231pàgines i SHA
`b80bad25082b24f574521702f0f5d7b379039bc700ccbc7014263c6c0d3f218d`.
Totes les pàgines passen els límits de text; les26pàgines del capítol s'han
revisat visualment, amb comparació de les pàgines inalterades entre passes.
Browser1440/430px, MathJax, prosa, fonts, computacions,site_check,build i
html_audit correctes. Tres passes structure/line/evidence retinguts contra
revision123; el registre editorial continua intacte al límit100.

La font passa a review, ambref/permalink/ancoratges conservats. Sense aprovació
humana, commit, push o publicació. Els ZIPs de pràctiques26/10 romanen segellats
i la publicació latest no canvia. Les57figures computades continuen fresques;
pins/scaffold i els originals GIS no s'han modificat en aquesta revisió.

## Arrel mínima i captura de suma, 27 d'octubre de 2026

Continuació de la mateixa tasca13 i checkout, amb reserva a
[Geodisseny#13](https://github.com/geourv/geodisseny/issues/13#issuecomment-6432786500).
L'autor ha corregit explícitament l'estructura del26/10: **`LLEGIU-ME.pdf`
directament a l'arrel de cada pràctica, al costat de `data/`**, sense `pdf/`
ni `payload`. Els deu ZIPs actuals i totes les instruccions ho reflecteixen.
Els vectors continuen als GeoPackage, els ràsters són GeoTIFF separats i els
projectes QGZ mantenen rutes relatives i l'ordre de dibuix lligat al panell Capes.

Run complet de reconstrucció:
`sandbox/practiques/lliurament-geodisseny/2026-10-27-minimal-01/`.
`reuse.json` vincula el layout02verificat del26/10amb les còpies byte-idèntiques
del run nou. Conservar `classroom/`, `context.json`, `handouts/layout02/`,
`document-sources01/`, `pdf-receipts01/`, `packages/review01/`, `pdf-review01/`,
`reopen01/`, `review-sources/`, `REVISIO-RETINGUDA.json`, `reading-changes.diff`,
`reading-image-checks01.json`, `handoff-checks.json`, els rebuts de promoció i
`current-verified.json`. No s'ha repetit cap anàlisi GIS ni les179conques.

Els deu PDFs s'han construït amb la CLI pública Web0.7.4 i el worker PDF618…
fixat.132pàgines revisades visualment; A4horitzontal, límits de text i codi
comprovats. Les lectures d'intervisibilitat tenen43pàgines d'inici i11docents.
Els26projectes dels ZIPs exactes s'han reobert readonly/offline, sense muntar el
checkout, amb tots els164fitxers extrets inalterats. La inserció i el moviment
d'una capa de dalt a baix i amunt continuen arribant al canvas en l'ordre visible.
Els cinc enunciats Moodle editables es conserven separats dels PDFs docents.

L'arbre26/10anterior íntegre,37fitxers i20directoris, és a:
`sandbox/practiques/arxiu-lliuraments/2026-10-27-abans-arrel-minima-01/dist-practiques/`.
La comprovació independent contrasta paths, bytes i tots els hashes de l'arxiu,
tots els membres dels ZIPs nous i els cinc `SHA256SUMS` del dist actual.

| Rebut | SHA-256 |
| --- | --- |
| `original-tree.json` del nou arxiu | `5e53b0762a6847563ed24b9142b4ca9618800133108a0e0340306eb238a96cd6` |
| `verified.json` del nou arxiu | `6ff808aeefcaa27d669ed61a9b77257983957ca4217b7333a501ccfedb3f3cc7` |
| `dist/practiques/manifest.json` actual | `00d33cd16af175a0e8521a57f360fb8d63c08ae0bb00a09b6294fc20f5fb65bc` |
| `published-current.json` del nou run | `14bee131fdd791ad2829e5750b3211fffccd3786f36e40afffe8b80769d90440` |
| `packages/review01/packages.json` | `cd1800db357593dc6ffc3e49204f134f5555fdb14e9a2fbc44fc068b13980345` |

La captura nova `visibilitat-lots-suma` mostra el diàleg normal d'Estadístiques
de cel·la amb cinc entrades, Suma, Ignora NoData desactivat i Conca C05 de
referència. PNG, SVG autocontingut i manifest els ha escrit el productor públic
MCP0.6.1amb engine100… i `private-xvfb-v1`, sense avisos. La figura mostra
configuració, no execució, i els avançats hi estan col·lapsats.
Fonts i intents a
`sandbox/practiques/visibilitat-costa/2026-10-27-captures-01/`:
`suma01/` és el primer sondeig correcte; `suma02/` es va aturar pel canvi de
capa activa en carregar la referència; `suma03/` és el render final després de
preparar la capa abans d'aplicar la presentació. No s'han reescrit els intents.

PNG `assets/captures/visibilitat-lots-suma.png`:
`b56f181410298e7798823294ad619686079bd73ea350d053294745ac71c4b7d5`.
Manifest `context/qgis/manifests/visibilitat-lots-suma.yml`:
`44eeee78e85be00d82b705f44f49f7fad27a94b07a54f39e9ce295b3d15e7bca`.
La taula de lots, Autofill i EXTRA desplegat continuen sense captura acceptada.
QGIS#26està tancada i el suport és publicat a QGIS0.7+; el cohort viu conserva
QGIS0.6.1i l'adopció compatible es segueix a
[Web#117](https://github.com/dosquartsdedocs/unaltraweb/issues/117), encara oberta.

El capítol4també indica l'arrel mínima. Font actual:
`6290f7950554d71a8053ec84666bef809c61dc6794949846e8870de10776db86`.
El manual local reconstruït manté231pàgines, SHA
`e24babc1fb486048124c997cc6da65460495d49896a9b4e235dd41ba34e41ef5`.
`site-build01/` conserva el buildnormal amb imatge immutable i el PDF anterior.
`manual-pdf-review01/` conserva el PDF nou, límits de text de totes les pàgines
i revisió visual de portada i pàgines148–150, que inclouen la frase modificada.
`browser-review01/` documenta el preview etiquetat a1440/430px: zero overflow,
imatges carregades i121expressions MathJax sense errors. Les57computacions
continuen fresques; site_check i html_audit passen.

L'intent de preview pel MCP va esgotar el timeout i el contenidor de preview
que havia creat va desaparèixer. La CLI pública del mateix Web0.7.4, amb accés al loopback del host,
ha iniciat un preview etiquetat propi i verificat. Els processos i respostes
queden a `.cache/practiques-minimal-20261027-01/`; no s'ha canviat el proveïdor.
El control genèric de fons no resol els bindings privats de les lectures:
`reading-image-checks01.json` contrasta els PNG efectius per hash i comprova
que són opacs, sense modificar imatges.

Deu passes copy i el pass del capítol preparats contra els digests actuals;
estat editorial gestionat intacte a revision123, al límit100. L'edició continua
**review/ESBORRANY**, sense aprovació humana nova ni càrrega Moodle o desplegament.
La integració tècnica Web0.7.4de la tasca19 ja estava completada abans d'aquesta
represa; els seus pins i resultatAPPLIED s'han preservat. Cap commit, stash o
canvi de branca en aquesta correcció. Els arxius continuen sent locals, sense
acreditar backup extern.

## PDFs i enunciat al costat dels ZIPs, correcció posterior del 27 d'octubre

L'autor assenyala que s'havia mantingut una carpeta `alumnat/` superflua fora
dels ZIPs. La disposició actual a `dist/practiques/<practica>/ca/` és plana:
els dos ZIPs, `LLEGIU-ME.pdf`, `LLEGIU-ME-docent.pdf`, `ENUNCIAT-MOODLE.md`,
manifest i sumes. No hi ha subcarpetes de destinatari dins de `ca/`.

Run: `sandbox/practiques/lliurament-geodisseny/2026-10-27-pdfs-plans-01/`.
`reuse-packages.json` vincula els paquets i la verificació retinguda del run
minimal01. Els deu ZIPs, deu PDFs i cinc enunciats conserven exactament els
mateixos bytes; només canvien les rutes externes i les metadades que les
descriuen. No s'ha tornat a renderitzar PDF ni executar GIS. El generador del
curs incorpora la disposició plana per als lliuraments següents.

Arbre anterior complet:37fitxers i20directoris, a
`sandbox/practiques/arxiu-lliuraments/2026-10-27-abans-pdfs-plans-01/dist-practiques/`.
`current-verified.json` del run nou acredita tots els hashes de l'arxiu,
la igualtat dels documents/ZIPs i els cinc `SHA256SUMS` actuals.

| Rebut | SHA-256 |
| --- | --- |
| `dist/practiques/manifest.json` actual | `dbfbf913152048d68939dfba5ae7c676e7668fe4078284450839895bbfea8ac1` |
| `original-tree.json` del nou arxiu | `5e31def5becfc60968a3ecd4b3a60a77b3faccaa9e18152af3f3f2bc9792dd87` |
| `verified.json` del nou arxiu | `e25f53248095dfcbbebdef0a204d870610a3179706115d9fe6cc0fbdeddb3f4b` |
| `published-current.json` del nou run | `675bc930f88ee02677acf4ff26a835856edd3260bb2b11d89c20c76fce004fd6` |

Es corregeixen AGENTS, el perfil de redacció i el README. Fonts editables i
reconstruccions històriques conserven els paths de procedència. La petició de
captures reals de la taula de lots i dels menús d'autoemplenat continua oberta;
la captura de suma i el botó d'accés no les substitueixen.

## Taula i autoemplenat natius, prerequisits i alertes, 27 d'octubre

Després de l'autorització explícita d'un render puntual amb el capturador
publicat0.7.0s'han obtingut9bundles PNG/SVG/manifest amb les mostres reals
C05/C11/C13/C25/C37. Fonts: `context/qgis/visibilitat-batch.md` i `.yml`.
Controller `45fd7b5ec04a6a5ec44ca5250ccc64ec548e4637f212933b3030387caf612233`;
engine1003721d… fixat. La CLI pública obre controls QGIS, menús i editors reals,
comprova valors acceptats i usa pantalla privada autenticada. La taula plena
té5execucions sense fila buida i5sortides úniques; el primer array conserva
la fila inicial buida fins que es retira. Els tres menús estan etiquetats
segons la seva funció. EXTRA és visible al diàleg individual.

Retenció completa a
`sandbox/practiques/visibilitat-costa/2026-10-27-batch-01/`:
`before-sources/`, `before.json`, probes01–03, `final01/`,
`captures-verified.json` i `prerequisits01/`–`02/`.
El primer render va refusar el valor temporal de sortida del diàleg individual;
el següent es conserva com a prova de maquetació, amb retalls/etiquetes revisats
abans del final. El primer control de prerequisits es va aturar en intentar
desar els punts amb el fid heretat repetit; aquella exportació no era necessària
per comprovar els camps i es conserva l'intent. No s'han eliminat originals.

`practiques/visibilitat-costa/comprovar-prerequisits-lot.py` acredita que els
37punts generats tenen fid,nom,long_m,distance,angle, sense x/y; addxyfields
amb EPSG:25831afegeix x/y a tots. Desa i recupera5files d'un `.batch` natiu
`batch_3.40` i comprova10rutes amb format Windows/mixt amb l'expressió exacta
de la guia. És una comprovació del parser a Linux, no una execució Windows.
No s'ha executat Viewshed ni repetit les179conques.

Les lectures expliquen el fitxer `.batch` com a text JSON recuperable i editable
a partir del format propi de la versió. S'afegeix com a evidència amb expressions,
captura de taula i registre; no se'n declara validada l'admissió automàtica a
Unaltramesa. La distinció entre punts nous i mostres preparades és explícita.
Les alertes de camps i rutes utilitzen l'entorn `manualcallout` i el color
`ManualCalloutWarning` existents a la plantilla compartida. El Markdown `>>>>`
es va renderitzar com a cites normals en el primer intent privat; els jobs
PDFbatch01es conserven i els finals són batch02, sense copiar ni canviar plantilles.

Run final de lliurament:
`sandbox/practiques/lliurament-geodisseny/2026-10-27-batch-01/`.
Conservar tot l'arbre: layout02reutilitzat, `pdf-receipts01/` i `02/`, snapshots,
`packages/review01/`, `reopen01/`, `pdf-review01/`, `REVISIO-RETINGUDA.json`,
`current-verified.json` i `final-checks.json`. Les lectures finals tenen52/14pàgines,
amb totes66revisades visualment. Codi, A4horitzontal i límits de text correctes.
Els altres8ZIPs/PDFs són byte-idèntics. Els26QGZ es reobren offline/readonly,
amb164fitxers extrets inalterats i ordre de dibuix lligat a l'arbre.

El dist conserva `LLEGIU-ME.pdf`, `LLEGIU-ME-docent.pdf` i `ENUNCIAT-MOODLE.md`
al costat dels ZIPs. L'arbre pla substituït,37fitxers i10directoris, és íntegre a
`sandbox/practiques/arxiu-lliuraments/2026-10-27-abans-captures-batch-01/dist-practiques/`.
Tots els hashes i els cinc `SHA256SUMS` s'han comprovat independentment.

| Rebut | SHA-256 |
| --- | --- |
| `dist/practiques/manifest.json` actual | `76b04b4fb894caea00219af9d11e6663cb7dcae9dc89deb7f53d958436b8c3b7` |
| `original-tree.json` del nou arxiu | `4be398d22913fd2bf270abdfeb4601a19f7c640e1b14e72767fabc6da9157f58` |
| `verified.json` del nou arxiu | `31af3c26f5acc5d99d57e6077f2022210fa24218ba123a5383b683bfabefdf0c` |
| `published-current.json` del nou run | `a9a38ba5ac88026306b36fba9d206b288ed38091dcf759e39ee52219e58dab5f` |
| `captures-verified.json` del run de captures | `8912db6e54b496297751f9d72f887e1bcd7042716fe0f6ea98946f662a9470c7` |
| `prerequisits02/verified.json` | `9ec51c0dd3ca940db34bf88386164befb6ccf53d981c3f37f673bcdad5b1f0a7` |

Les fonts continuen enreview; l'autorització del capturador no és aprovació
dels nous textos. Estat editorial gestionat i pins/scaffold preservats;
cap commit, desplegament o càrrega Moodle. La selecció global del MCP/helper
no canvia amb aquest render puntual. La captura de batch ja no queda pendent
d'aquell canvi global. La retenció continua sent local.

## Organització i lliurament portable, 30 d'octubre de 2026

Continuació de la mateixa sessió autoritzada a
[Geodisseny#13](https://github.com/geourv/geodisseny/issues/13#issuecomment-6535286068),
després de retenir els pendents de treball. Els82pathsWIP, el HEAD
`da7fb8b63111e6300702e80fef4c49aa95ffc001` i els pins/scaffold s'han preservat.
El preflight readonly només assenyala el dirty-checkout conegut; cap branca,
stash o sessió editora nous. Web0.7.4no proposa actualitzacions gestionades.

Les deu lectures, cinc enunciats, recursos i locks d'edició concreten
`data/`–`sandbox/`–`dist/`. El capítol4ja indica la mateixa pauta. El lliurament
de l'estudiant selecciona vectors en un GeoPackage nou, QGZ extern relatiu,
informe i GeoTIFF/recursos necessaris, amb noms codi–tema–cognoms. No s'ha
inferit una numeració real de pràctiques: els patrons `prN` la remeten a Moodle.
Es distingeix el paquet inicial del directori final que prepara l'alumnat.

La sessió i els seus fonts/rebuts són a
`sandbox/practiques/lliurament-geodisseny/2026-10-30-organitzacio-01/`:
`before.json`, `before-sources/`, `before-artifacts/`, `web-checks/`,
`document-sources01/`, `prerequisits01/`, `portabilitat01/`, `build01/`,
`browser-review01/`, `manual-pdf-review01/`, `REVISIO-RETINGUDA.json`,
`autocorrelacio-inventari01/`, fonts finals i `final-checks.json`.

El verificador específic de lots comprova37punts sense x/y, la seva creació
conjunta,70rutes de carretera i10formats Windows amb les expressions exactes.
La configuració original de cinc files es desa i recupera amb widgets natius.
Canviar la carpeta del QGZ deixa intactes les sortides guardades al `.batch`;
una còpia reassigna l'entrada ràster i recalcula les cinc destinacions. Es
comprova la recàrrega i es preserven els bytes originals. No s'executa Viewshed.
És una prova de format/parser a Linux, no una execució Windows.

Les cinc seleccions tècniques de `portabilitat01/` utilitzen resultats retinguts,
exporten un GeoPackage nou i desen un QGZ extern relatiu. Després de comprimir
i extreure les còpies, es reobren en un altre contenidor offline/readonly,
sense els inputs originals: atributs, camps, FIDs, geometries i bytes dels
ràsters iguals; mapa igual píxel a píxel, amb estils, etiquetes i ordre.
Els mapes s'han inspeccionat. Són probes de la pauta, no lliuraments d'estudiants
ni bundles natius nous.

El run del curs és
`sandbox/practiques/lliurament-geodisseny/2026-10-30-organitzacio-02/`:
`reuse.json`, `classroom/`, `handouts/layout02/`, `pdf-receipts01/`,
`packages/review01/`, `reopen01/`, `pdf-review01/`, promoció i verificació.
Els154membres de dades/projectes/recursos dels ZIPs són byte-idèntics als del27/10.
Els deu PDFs nous, Web0.7.4/worker618…, tenen150pàgines revisades visualment,
amb A4horitzontal, codi i límits comprovats. Els26QGZ dels ZIPs exactes s'han
reobert amb164fitxers extrets inalterats i el moviment de capes arriba al canvas.
Els cinc enunciats i els dos PDFs són directament al costat dels ZIPs.

L'arbre pla anterior complet —37fitxers i10directoris— és íntegre a
`sandbox/practiques/arxiu-lliuraments/2026-10-30-abans-organitzacio-01/dist-practiques/`.
Paths, bytes, hashes i directoris contrastats independentment, també els cinc
`SHA256SUMS` nous i la correspondència PDF separat/interior del ZIP.

| Rebut | SHA-256 |
| --- | --- |
| `dist/practiques/manifest.json` actual | `b87346bbd213176de551be8e074d8f5a6d82ccb251356219b629456d590e8c3e` |
| `original-tree.json` del nou arxiu | `7c647c494ffd2d535f1052bbaa978e88325068a105ab488aac04ebf93313881b` |
| `verified.json` del nou arxiu | `fe485f346fea0eabb825c89ab0196c1aa27ed817d0b6e668c0f899740c58aa5f` |
| `published-current.json` del run02 | `9dcd0c0bb8c315708ba594bab9c68f76b15158cf33a51d2c8dc9e3faa6c8707a` |
| `packages/review01/packages.json` del run02 | `840e279613f9faec5174b644b0f3f220e8c0b8e9a6b36f4073758ce6b23de884` |

El manual local manté231pàgines, SHA
`479b70089e26cecb39bbe8a556f8bdd689e4eba77708fcf10194a55028391718`.
Prosa, fonts, site_check, build i html_audit passen. Revisió visual del canvi
a les pàgines148–151; totes les paraules del PDF dins dels límits. Web1440/430px
amb imatges carregades, zero errors MathJax/JavaScript i sense overflow. Còpies
generada, de preview i servida coincidents; cinc rutes privades continuen404.

L'inventari readonly d'autocorrelació verifica94membres del segell municipal
i els dos ZIPs originals amb CRC/hashes. Confirma98punts amb `POT_KW`,98resultats
Moran i151seccions de renda. Es retenen hashes de fonts, captures i manifests;
no s'ha executat preparació ni anàlisi. Queda pendent preparar l'activitat
separada, seleccionar entrades/resultats, qualificar el runtime actual i
concretar lectures, codi i abast. Queen requereix tenir present l'exportació
Shapefile de treball; la distribució vectorial preferida continua GeoPackage.

Onze passes editorials es retenen contra els digests preparats, sense findings;
el registre gestionat continua intacte a revision123, al límit100. Els pendents
són a la memòria de projecte `edd48b8eae204f13bb990cad9a029fe6` i al traspàs local.
Tot continua review/ESBORRANY. No s'ha concedit aprovació humana, fet commit,
publicat el web o pujat res a Moodle. La retenció continua sent local.

## Dimensions de dispersió transferibles, 3 de novembre de 2026

Tasca pròpia [Geodisseny#22](https://github.com/geourv/geodisseny/issues/22),
branca `content/22-calcul-dispersio` des de main
`a644a6a3ddcff3ad09e8684207968ee1c826868f`, amb preflightELIGIBLE abans d'editar.
L'autor demana calcular radi i semieixos al manual i a la lectura d'alumnat:
altres municipis no poden reutilitzar les dimensions de Constantí.

Reconstrucció de sessió:
`sandbox/practiques/estadistica-constanti/2026-11-03-dispersio-01/`.
Conservar `before.json`, fonts/artefactes anteriors, `check01/` fallit i
`check02/` correcte, `web-checks/`, `build01/`, `browser-review01/`,
`manual-pdf-review01/`, `REVISIO-RETINGUDA.json`, fonts finals i `final-checks.json`.

El procediment usa una capa municipal P, CRS real mètric, centre no ponderat i
nou camps a la fila d'aquell centre. Les variàncies/covariància amb divisor n
alimenten D, delta, a, b i azimut. Les funcions de dibuix llegeixen aquests camps.
Es distingeixen selecció d'objectes i capa d'anàlisi, geometria de P i del
`@parent`, precisió de càlcul i presentació, angle/radians i semieixos/eixos.
Es documenten isotropia, alineació i coincidència sense forçar polígons.

El verificador específic executa les expressions literals del manual i de la
lectura amb `native:fieldcalculator`, `native:meancoordinates` i
`native:geometrybyexpression` a QGIS3.44.11/engine100…, sense xarxa i amb inputs
readonly. Nou casos: Constantí124, el Morell111, el Catllar437, cinc punts
construïts, dos girs, isotropia, alineació i coincidència. Contrast independent
amb NumPy/autovalors i covariància dels vèrtexs;86/68registres interiors de
Constantí. El primer intent només falla serialitzant un bool NumPy; no es
reescriu. El report íntegre és `check02/verified.json`.

Les lectures d'alumnat/docent tenen19/8pàgines, amb27pàgines inspeccionades,
A4horitzontal, codi i límits correctes. La primera dona procediment i expressions;
la segona, controls i diagnosi del càlcul. Enunciat, recursos i locks d'edició
coherents. Els paràmetres i resultats del cas no es converteixen en constants
esperades per a altres municipis.

Reconstrucció del lliurament actual:
`sandbox/practiques/lliurament-geodisseny/2026-11-03-dispersio-01/`.
Conservar `reuse.json`, `classroom/`, `handouts/layout02/`, `pdf-receipts01/`,
`packages/review01/`, `reopen01/`, `pdf-review01/`, els rebuts de promoció i
`current-verified.json`. El collector revisa un sol slug i consumeix els
paquets no afectats verificats; els vuit ZIPs/PDFs originals mantenen els bytes
i l'edició30/10. Només estadística passa a03/11. Els manifests declaren l'edició
real de cada activitat, independentment de la data de revisió del conjunt.

Els154membres de dades/projectes/recursos no canvien.26QGZ dels ZIPs exactes
reoberts offline/readonly i164fitxers extrets inalterats. El dist anterior
complet —37fitxers/10directoris— és a
`sandbox/practiques/arxiu-lliuraments/2026-11-03-abans-calcul-dispersio-01/dist-practiques/`.
La comprovació independent contrasta paths, bytes, hashes i directoris, els
cinc SHA256SUMS, els PDFs separats i els membres de dades dels ZIPs.

| Rebut | SHA-256 |
| --- | --- |
| `dist/practiques/manifest.json` actual | `e666ba6473cc14c96242b875269372c7178f5635475e7ad015745c1881c7cdb5` |
| `original-tree.json` del nou arxiu | `1ab04bc647929d7ac41a56026ffab2af9f5f6fbf0bbf40cc756c9d24168753f8` |
| `verified.json` del nou arxiu | `71c3379b7cf8d90b9dce405086d8d3eeb72f8b640494bab75d29b45177d81288` |
| `published-current.json` del nou run | `ff994e0a27fb86bca15d019daa14f76d111bba36056fdbf71b7757afb954a4c6` |
| `packages/review01/packages.json` | `0eb53d6112021b4a564f3653f5ef7f8294df0ee70f90936e7ef5e9f4de9f6c92` |

Manual local233pàgines, SHA
`5dfb4483e75c1b8bd89b573431aa7f5273d786ac939688fdaf540d1cb4e7dc25`.
Prosa, fonts, site_check, build i html_audit passen. Tots els límits de paraula
comprovats; pàgines163–167inspeccionades. Web1440/430px sense overflow, errors
JavaScript/MathJax o imatges absents; còpies PDF generada/preview/servida iguals.

Tres passes editorials es preparen contra els digests actuals i es retenen;
registre gestionat intacte al límit100/revision123. Fonts i candidata enreview,
sense commit ni nova publicació autoritzats pel simple lliurament d'aquesta
revisió. La beta pública del03/11resta documentada separadament a
`context/publication-beta-20261103.md`. La retenció continua sent local.
