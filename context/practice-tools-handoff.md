# Eines de pràctiques: retorn a l'autor

9 d'octubre de 2026 · [gaContExt #32](https://github.com/dosquartsdedocs/gacontext/issues/32) / [Geodisseny #9](https://github.com/geourv/geodisseny/issues/9).

Workspace: `/home/benizar/git/geodisseny`; branca `content/9-accessibilitat-inici`; HEAD `5c904a386048bf317ca45cab6d42e0965f0ce0d6`. Aquest retorn habilita les eines; la finalització dels models, lectures i ZIPs queda a l'autor.

## Estat i selecció

- **CLI QGIS verificada:** `unaltracaptura-qgis 0.6.0rc2`, revision `sha256:5922d3dc411c14c7c3c2d9257a78b4d42f42fb1aae8451bcf245ca44a0e91992`; schema v2 `528c8be229c72c346f134ffaa60094f94224094a25b6fb11bcc87802ddc7fffb`. Consulta fresca `practice-schema`: `ok:true`.
- Client únic readonly: `/tmp/opencode/practice32-qgis-client-1a7456c0b81e/env/bin/python`. Wheel `1a7456c0b81e0a4729b702b60d9340456efea9a88b9f5c21b97c8ff4823d09bf`; ready SHA `6a51f1f9c77a0a333623e8332b886651ea497895b1736165404e79d8905983bd`.
- **CLI Web final verificada:** controller Docker `sha256:17ef0d24e8611a6802b3c01ff440e6e552eac728343733198056fdbc6cdf379e`; els dos dry-runs frescos passen amb 19 inputs i 15 bindings cadascun. Cap render nou en aquest handoff.
- **Connexió MCP Web real confirmada després de la recàrrega scoped:** `unaltraweb.runtime_identity` retorna `ok:true`, `observation:live-serving-process`, `lifecycle.state:connected`, paquet installed i `drift:false`. Controller, fingerprint, consumidor i worker PDF coincideixen amb la selecció final; observació detallada més avall. El `failed`/`Connection closed` anterior queda com a antecedent, no com a estat actual.
- `.opencode/opencode.json` SHA `f5eea95f897c73bcc8f493c0946583cd946e2bc18b93e5e29bd4b05f61a669d8`. Últim delta: només l'executable host de `mcp.unaltraweb`, sobre el baseline verificat `16c4c7431ffecb4d31998a3d68cdcbc54c3ef108f841cdb0041ab0231565f771`; tota la resta d'argv/environment/model/permisos/altres claus queda byte-idèntica. Shape inalterada respecte de la config validada amb l'schema oficial SHA `e8cb6e287a3852ee3403f4803be5ad6b19db94948037eaa9672125c333427922`. Continua ignorada per `.git/info/exclude`.
- **Adapter host compartit corregit, readonly:** `/tmp/opencode/practice32-web-adapter-2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a/venv/bin/unaltraweb-mcp-docker`; wheel pin `2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a`, ready SHA `7c7f98fb11f0aaab827644c201a6b8527079ec8b26a96da3f346dbf861c2f9ec`, manifest SHA `0cc8e3735c960924e4698909367d01cf711d536eebda5fe068835d519b94f554`. `USAGE.md` i manifest revisats/hashes coincidents. Identitat de l'adapter independent del fingerprint del controller; adapter anterior i contracte original preservats.

Referències públiques: `/tmp/opencode/practice32-final-cohort.md` (SHA `6455db67fee9f13da172be810b6ea29d60b05ba2fba9d5f84038c1a47f95e7a2`) i `/tmp/opencode/practice32-web-candidate04/ready.json` (SHA `ba9fbdb6170a0f51086bad310a636e8c3d2f93ea4317c106d313ab32f509718b`). La metadata Web `0.7.1` sola no identifica aquest candidat local.

## Comandos QGIS

Des del workspace, consulta readonly, amb l'entorn de `USAGE.md` del client seleccionat:

```bash
PROJECT=/home/benizar/git/geodisseny
test "$(pwd -P)" = "$PROJECT" && test "$(git rev-parse --show-toplevel)" = "$PROJECT" || exit 1
env -u DOCKER_CONTEXT -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH -u DOCKER_API_VERSION \
  -u UNALTRACAPTURA_QGIS_PROJECT_ID -u UNALTRACAPTURA_QGIS_JOB_REGISTRY \
  -u UNALTRACAPTURA_QGIS_JOB_REGISTRY_HOST -u UNALTRACAPTURA_QGIS_JOB_GRANT \
  DOCKER_HOST=unix:///var/run/docker.sock \
  MCP_CONSUMER_WORKSPACE="$PROJECT" \
  UNALTRACAPTURA_QGIS_WORKSPACE="$PROJECT" \
  UNALTRACAPTURA_QGIS_HOST_WORKSPACE="$PROJECT" \
  UNALTRACAPTURA_QGIS_HOST_UID="$(id -u)" \
  UNALTRACAPTURA_QGIS_HOST_GID="$(id -g)" \
  /tmp/opencode/practice32-qgis-client-1a7456c0b81e/env/bin/python \
  -I -B -m veure_qgis_mcp.cli practice-schema --profile qgis-practice-v2
```

El mateix prefix públic admet `practice-run`, `practice-check` i `practice-reopen`; exemples complets a `/tmp/opencode/practice32-qgis-client-1a7456c0b81e/USAGE.md`. Request/model/inputs es resolen respecte del parent del request: no usar `../`. Engine preparat i verificat `sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2`; sense nova venv ni pull/build implícits.

## Comandos Web

La config local conté aquesta selecció per al client MCP. **La recàrrega scoped amb el nou adapter host2c9b0c21… ja s'ha efectuat i una crida a la connexió REAL confirma la identitat actual**. Imatge17ef0…, fingerprint5b8de… i PDF618163… no canvien; la identitat del host és independent del fingerprint del controller:

```bash
MCP_CONSUMER_WORKSPACE=/home/benizar/git/geodisseny \
  /tmp/opencode/practice32-web-adapter-2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a/venv/bin/unaltraweb-mcp-docker \
  serve --project /home/benizar/git/geodisseny \
  --image sha256:17ef0d24e8611a6802b3c01ff440e6e552eac728343733198056fdbc6cdf379e \
  --expected-image-id sha256:17ef0d24e8611a6802b3c01ff440e6e552eac728343733198056fdbc6cdf379e \
  --managed --offline \
  --worker-images '{"manual_pdf":{"reference":"ghcr.io/dosquartsdedocs/unaltraweb-manual-pdf@sha256:1bb3f2dafd741e96c28639ec1cc8ccaeb81cbaa73e649f787c0b4ef59997bd4b","expected_image_id":"sha256:618163d3f924439792b2306617bd9612f566c5881166102fa544b4e782d569fa"}}'
```

`unaltraweb.runtime_identity` s'ha cridat a la connexió REAL d'aquesta sessió després de recarregar: fingerprint observat **`sha256:5b8de154fc10665f71056b2887959d41a2a6f5fb5726611d1ee3482c7d7b3d36`**, igual al contracte i als hashes startup/current; `drift:false`. `mcp runtime-identity` **no és un subcomand de la CLI d'aquest candidat**; la consulta d'identitat viva pertany a MCP.

### Observació actual post-reload del nou adapter — 9/10/2026

Segons el coordinador: recàrrega scoped amb OpenCode1.18.35 i el nou host adapter pin `2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a`, un POST HTTP200/true, event disposed observat, tots els IDs d'historial preservats i mateix model/agent. Config `f5eea95f897c73bcc8f493c0946583cd946e2bc18b93e5e29bd4b05f61a669d8` sense canvis en aquest tancament.

Antecedent conservat: recàrrega anterior amb config16c4c743…, una sessió/2408missatges; instance `5d3e743322e44fdd8d8471f517a4fe1b`, session `1cf1d4a6d5b885a3ff812d4a4abd0842`, contenidor `732e208f193a99a4b70fb7176462c7c228aee2b4eaab70a66fe07ef0bfac1b7f`, inici `2026-10-09T21:15:54.605469+00:00`. No és la connexió actual.

Observació directa actual per MCP amb una única crida `unaltraweb.runtime_identity`, sense client temporal: `ok:true`, `observation:live-serving-process`, paquet installed, hashes startup/current5b8de… coincidents i `drift:false`:

- Instance `2c696b2837094123ac15dda250040f8d`; session `3877d2bf576bdda73afd711517c5eb0b`; procés iniciat `2026-10-09T21:59:17.589698+00:00`.
- Contenidor viu `e3e02448522afb9e36575d62f3a6599f6fad01bb39d6ccd33d0dc9f228fcc9f6`, `state:matched`, image seleccionada/esperada/observada `sha256:17ef0d24e8611a6802b3c01ff440e6e552eac728343733198056fdbc6cdf379e`.
- Consumer/effective/daemon-host/launcher: `/home/benizar/git/geodisseny`; project ID `c904e3e417f00779`.
- Worker `manual_pdf`, `state:matched`, ID esperat/observat `sha256:618163d3f924439792b2306617bd9612f566c5881166102fa544b4e782d569fa`, digest `1bb3f2dafd741e96c28639ec1cc8ccaeb81cbaa73e649f787c0b4ef59997bd4b`.
- Inventari MCP real exposat en aquesta sessió: `manual_practice_pdf_build(source, version, run, dry_run)` i `manual_practice_compose(config, dry_run)` disponibles. Presència confirmada a l'inventari, sense executar-les.
- Lifecycle `connected`, operació activa nul·la, cua0, `resources_released:false`: connexió disponible per a l'autor, sense drain ni tancament.

CLI one-shot provada, dry-run de la lectura d'inici. Per a la docent, canviar només source i run a `ca/docent/LLEGIU-ME.md` / `ga32-tools-docent-01`:

```bash
PROJECT=/home/benizar/git/geodisseny
CLIENT=/tmp/opencode/practice32-web-adapter-2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a/venv
IMAGE=sha256:17ef0d24e8611a6802b3c01ff440e6e552eac728343733198056fdbc6cdf379e
PROFILE="$("$CLIENT/bin/unaltraweb-mcp-docker" path)"
PROJECT_ID="$(/bin/sh "$PROFILE/scripts/unaltraweb-mcp-project-id.sh" "$PROJECT")"
SESSION="$(od -An -N16 -tx1 /dev/urandom | tr -d ' \n')"
PM="$(/bin/sh "$PROFILE/scripts/unaltraweb-docker-mount.sh" "$PROJECT" "$PROJECT")"
SOCKET="$(realpath /var/run/docker.sock)"
SM="$(/bin/sh "$PROFILE/scripts/unaltraweb-docker-mount.sh" "$SOCKET" /var/run/docker.sock)"
CID="$(docker --context default create --pull never --network none --init \
  --name "unaltraweb-stdio-$SESSION" --cpus 2 --memory 4g --pids-limit 512 \
  --label io.context.mcp-factory=unaltraweb --label io.context.mcp-role=stdio \
  --label "io.context.mcp-project=$PROJECT_ID" --label "io.context.mcp-session=$SESSION" \
  --user "$(id -u):$(id -g)" --group-add "$(stat -c %g "$SOCKET")" \
  --mount "$PM" --mount "$SM" -e HOME=/tmp \
  -e "MCP_CONSUMER_WORKSPACE=$PROJECT" -e "UNALTRAWEB_DOCKER_ROOT=$PROJECT" \
  -e "UNALTRAWEB_RUNTIME_SESSION=$SESSION" \
  -e MANUAL_PDF_IMAGE=ghcr.io/dosquartsdedocs/unaltraweb-manual-pdf@sha256:1bb3f2dafd741e96c28639ec1cc8ccaeb81cbaa73e649f787c0b4ef59997bd4b \
  --entrypoint unaltraweb-mcp "$IMAGE" --project "$PROJECT" \
  mcp manual-practice-pdf-build \
  --source practiques/accessibilitat-vilaseca/ca/alumnat/LLEGIU-ME.md \
  --version 2026-10-09-pdf-02 --run ga32-tools-alumnat-01 --dry-run)" || exit 1
STATUS=0
docker --context default start --attach "$CID" || STATUS=$?
sleep 3
DOCKER_CONTEXT=default "$CLIENT/bin/unaltraweb-mcp-docker" reap-session \
  --project "$PROJECT" --session-id "$SESSION" --container-id "$CID" && test "$STATUS" -eq 0
```

Proves fresques: alumnat fingerprint de job `e3f64cee179fef457d73b7250b5205e729eab2d4d1acac89cda6a355a7f9d84e`; docent `e321d92326c175c4d6cd5ce46c8692972d96a1230388e9b0885be111358abac7`. Tots dos `ok:true`, `state:planned`, worker observat `618163…`, sense crear jobs nous; reapers `ok:true`. La mateixa imatge ofereix `mcp prose-check --target <source>`, `mcp editorial-review-prepare --target <source> --kind structure` i `mcp manual-practice-compose --config <edició indexada> --dry-run`; la composició necessita abans un bundle GIS propi verificat.

## Fonts i PDF conservats

Només s'hi afegiren **17 captions en català**, amb sintaxi normal `Table:`: set a alumnat i deu a docent. [Reserva](https://github.com/geourv/geodisseny/issues/9#issuecomment-6086153008) i [diff revisable](https://github.com/geourv/geodisseny/issues/9#issuecomment-6086244166). Zero línies anteriors eliminades o modificades; cel·les, valors, passos, captures, links i resta de prosa intactes. Les lectures continuen `draft`.

Fonts: `practiques/accessibilitat-vilaseca/ca/<alumnat|docent>/LLEGIU-ME.md`.

| Lectura | SHA anterior preservat | SHA revisat |
| --- | --- | --- |
| Alumnat | `2b143ca541a6d5a84bea9d1c2b8e7e5641f6f81fe514f9141cebc06886057953` | `729ab79061ff20133898e0c6c0974f6fc1ebf98f7c2db347fafa5da02b42f9d0` |
| Docent | `8b54fe7842cb0847a54f57dbfb2fa6edf46af9669b5f5b5bde0dae45b357d814` | `e4b0f086759ec03bacecd62827becb37e417e8dc3ae32b986f246a85a8ba9e54` |

Les fonts anteriors i logs romanen a `sandbox/practiques/accessibilitat-vilaseca/lectura-2026-10-09-pdf-01-ca-<destinatari>-ga32-<destinatari>-01/inputs/original.md`. Els dos renders fallits per captions es conserven. Prosa: una font per destinatari, sense findings/issues/warnings. Revisions d'estructura `accessibilitat-taules-alumnat-estructura-20261009` i `accessibilitat-taules-docent-estructura-20261009`, digests preparats `3bdfec0c4835cef6b125795a46192bebf9f626f72465a1fef62705f057816225` / `fe6c35f29c8ff5a4037e5a5082dd75b07d4aa69aa175741cc5edfc92637099bb`, registrades revisions91/92, sense troballes ni aprovació humana.

PDFs ja construïts: root de job `sandbox/practiques/accessibilitat-vilaseca/lectura-2026-10-09-pdf-02-ca-<destinatari>-ga32-<destinatari>-02/`; PDF `outputs/LLEGIU-ME.pdf`, primera pàgina `outputs/preview.png`, rebut `receipt.json`.

| Lectura | Pàgines / bytes PDF | SHA PDF | SHA receipt |
| --- | --- | --- | --- |
| Alumnat | 38 / 9.347.186 | `80c5a67275749acc1fada5904a8ba08b122b2a845149ae0ea67ef4678ab4feba` | `0ab625749998a2ffddd8737634e74a8c128fbaff54a7aaee644e57b333e4f4c3` |
| Docent | 32 / 9.309.728 | `9e123b02bfd7bafba0db5938b3b3d1fc5dbb5eac7434b76345af688e12f50756` | `d6ead474522206086b3a89e4e36673995a4dcd4302f72541e8c74fb61cb4a34e` |

Inspecció readonly amb pypdf al worker pinat: 40 artefactes verificats per receipt, A4 horitzontal841,89×595,28pt, numeració de pàgina completa, fonts incrustades. Primeres pàgines revisades: codi21234116, versió, logos i títol correctes; sense curs acadèmic al header. Revisió visual completa i prova no-clobber d'un job segellat pendents; no s'atribueixen al sol `ok:true` del render.

Captures històriques: quinze PNG a `sandbox/practiques/accessibilitat-vilaseca/2026-10-07-organitzacio/captures/`, resoltes pels trenta bindings de `_config.yml` (SHA `6976747137ecc27bb35832cb86271b7fdd46a4857d42e9bb0266487b38833a0e`). Aquesta recompilació A–G no acredita una reexecució GIS A–G.

## D/E: punt de represa

- Request `practiques/accessibilitat-vilaseca/activity-cost-p2.json`, SHA `b4e9494c889420cb12688456cb12310b8096bff9a7a5da1d54587623af9b54d2`; model `compute_cost_p2.py`, SHA `12395d3742d1258ef56a506e0675402ffcb84a104a862cf7859400016015c4af`. Sense canvis en aquest handoff.
- Input normalitzat readonly: `sandbox/practiques/accessibilitat-vilaseca/2026-10-09-cost-p2-inputs-04/`, request/model/GPKG i `origin.json`. Seed GPKG SHA `46d326819ad05f328eec12d34026956adcd3bfec9facbefeee226068fee03593`, originari del run històric; 22 membres declarats, incloent projecteinici/ràsters/estils, font explícita. Packets01–04 i intents fallits es conserven.
- Report `sandbox/qgis-practice-jobs/practice-1d1c629b35204b90b12e4e75bbeb69eb/compute-5d23f413f55a/report/result.json`: `ok:true`, 13 algorismes i24controls. Cost a D obert/tancat1336,9900782009827/4548,731957466707m ponderats; longitud441,98484809834997/1639,2135623731024m. Dijkstra concordant, P2obert5/tancatNoData, alternatiu5/5; expectatives/toleràncies preservades. Aquest report no és el segell d'un bundle.
- Blocker actual de rc2: `unsupported or empty Shapefile sidecar` sobre quatre `.tfw` de cost/direccions. [Retorn real](https://github.com/dosquartsdedocs/unaltracaptura-qgis/issues/4#issuecomment-6085650070). Segons el coordinador, la prova de normalització `gdal:translate` ja és positiva amb píxels/dtype/NoData/CRS/transform idèntics; **guia/paquet final pendents de transferència i verificació**. No s'ha aplicat al consumidor ni repetit el model.
- Encara sense bundle propi segellat, seleccions/reobertura finals, edició D/E o ZIPs nous. Destí previst `sandbox/practiques/accessibilitat-vilaseca/2026-10-09-cost-p2-01/`. Després del patró verificat cal un intent create-only i comprovacions del productor; l'abast docent D/E s'ha de definir abans de compondre.

Històric conservat: `sandbox/practiques/accessibilitat-vilaseca/2026-10-07-organitzacio/`, originals de `tmp/dades-docents/`, tots els jobs, snapshots i `dist/practiques/accessibilitat-vilaseca/2026-10-07-r2/ca/`. ZIPs r2 SHA `d936d1b56b9ab811140493a9413843e81d362f0ccf350c4a848a9c77323a71e9` / `f7425f063993404ce1382f45e149fb172cdf8cc31b160a6ae4d13a501a05c5ab`. Plantilla aprovada i controls Make/Gem/workflow preservats; `make clean` esborraria originals de `tmp/`.

## Pendents conservats després de la recàrrega

Recàrrega amb el nou executable host i identitat real del controller completades en l'observació actual. Es mantenen pendents la guia TFW verificada/aplicació posterior al pilot, el segell i reobertura GIS finals, i la revisió visual/aprovació de l'autor. Els altres tres MCPs constaven connected en l'observació del coordinador; no s'han reconfigurat.

Historial conservat: la prova negativa del subcomand inexistent deixà un contenidor exited2/PID0; dos intents amb l'adapter antic retornaren **`Exited resource changed during recovery`**. El provider corregí el fals refusal per ordre de mounts, sense canviar els registres ni relaxar els guards.

Recuperació explícitament autoritzada a Geodisseny amb l'adapter nou: `session-status` fresc identificà només aquest mateix orfe propi, role stdio, project `c904e3e417f00779`, exited/PID0, sense workers actius ni xarxes. **Un únic `reap-session`** retornà `ok:true`, `state:stopped`, `resources_released:true`; l'observació nativa posterior confirmà l'absència exacta amb recursos/xarxes buits. Cap retry, rm manual ni neteja general. Aquests IDs són diferents dels de la connexió activa:

```bash
DOCKER_CONTEXT=default /tmp/opencode/practice32-web-adapter-2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a/venv/bin/unaltraweb-mcp-docker \
  session-status --project /home/benizar/git/geodisseny \
  --session-id 1adcd48c944a902e4c8041fddcfddca9 \
  --container-id f22296a8b75d96e938ca1db5fe203ed7242c5bf737b55f3a8a75ae14b2faabf5
```

Reserva d'aquest handoff: [#9](https://github.com/geourv/geodisseny/issues/9#issuecomment-6089121939). Només config local i aquest fitxer editats en aquesta unitat; cap staging/commit/push, scaffold, canvi de branca/worktree, clean, regeneració general o publicació.

Tancament post-reload anterior: només aquest fitxer actualitzat. Consultes limitades a identitat/inventari; cap site_doctor, render, dry-run repetit, reaper o drain. Retorn idle amb el MCP actiu disponible.

Ajust compartit anterior de l'adapter: només config local i aquest handoff actualitzats; baseline i shape/hashes comprovats, un executable substituït, reap exacte resolt. Cap nova prova de models/PDF/ZIP ni build/render/dry-run; quedà idle per a la recàrrega posterior del coordinador, ara completada.

Tancament actual amb el nou adapter recarregat: només aquest fitxer actualitzat, una crida d'identitat real satisfactòria i presència de les dues eines de pràctiques a l'inventari. Cap descoberta addicional, client temporal, render, dry-run, site_doctor, prova del paquet host, reaper o drain. Retorn idle per a l'autor amb la connexió oberta.
