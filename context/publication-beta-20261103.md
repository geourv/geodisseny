# Publicació de la beta del manual, 3 de novembre de 2026

## Autorització i abast

L'autor, després del lliurament de la revisió local del web/PDF i de les cinc
pràctiques, demana: «Si falta alguna cosa per publicar, endavant. Em sembla que
estem apunt d'una beta del manual.» Autoritza preparar i publicar l'edició beta
a `latest`, amb la traça normal de commit, PR, fusió i desplegament sobre el SHA
de `main` revisat. No s'infereix una versió estable congelada.

Reserva i autorització registrades a
https://github.com/geourv/geodisseny/issues/13#issuecomment-6593836662.
Mateix checkout i branca `content/13-viewshed-lots`; els82paths de treball
preexistents s'han retingut abans de formalitzar l'aprovació.

La presentació i els capítols de visibilitat i d'estadística passen a
`content_status: approved` per aquesta decisió humana. La metadada d'edició
identifica la beta. A visibilitat es corregeixen tres referències de format i
carpeta: els ràsters són GeoTIFF a `data/rasters/`, les proves van a `sandbox/`
i la selecció final a `dist/`. No es canvien els resultats científics.

## Paquet prioritari per a la classe

La darrera edició de **Estadística espacial descriptiva**, amb els punts de
consumidors associats a instal·lacions fotovoltaiques de Constantí, és la del
30/10/2026. Directori vigent:

`dist/practiques/estadistica-espacial-descriptiva/ca/`

- `estadistica-espacial-descriptiva.zip`: inici per a l'alumnat.
- `estadistica-espacial-descriptiva-docent.zip`: resultats i lectura docent.
- `LLEGIU-ME.pdf` i `LLEGIU-ME-docent.pdf`:16i7pàgines.
- `ENUNCIAT-MOODLE.md`: editable per concretar els apartats i el codi real.

S'han comprovat els sis hashes declarats a `SHA256SUMS`. La verificació retinguda
vincula els ZIPs exactes a la reobertura offline/readonly. Entrades124registres,
98potències publicades; centres, dispersió i kernel. La publicació del manual
no altera aquests bytes ni carrega el paquet a Moodle.

## Comprovacions i publicació

Fonts, artefactes anteriors i comprovacions d'aquesta publicació es conserven a
`sandbox/manual-beta/2026-11-03-01/`. Inclou prosa, qualitat de fonts, aprovació,
control editorial de publicació, build i revisió del web/PDF de la beta.
Les revisions d'agent no substitueixen l'autorització humana anterior.

El control de fons retorna un avís de transparència al mapa històric de John Snow
i SVG no verificables automàticament. S'ha presentat la decisió a l'autor, que
ha seleccionat explícitament **«Publicar amb figures actuals (Recomanat)»**.
La beta conserva aquelles figures i registra els avisos com a pendents; no es
certifiquen com a opaques les imatges que l'inspector no ha pogut verificar.

La candidata local té229pàgines, amb «Edició beta, curs2026/2027» als crèdits
i sense marcadors ESBORRANY. El PDF revisat té SHA
`cdddabefd0fa42eb75b319d7d7c04b564484efd59acf18b4ffcdf5b5aa12e28b`.
Prosa, fonts,12/12fonts públiques aprovades, site_check, build,
editorial_publication_check i html_audit passen. Les còpies generada, de preview
i servida localment coincideixen. La revisió de navegador comprova presentació,
visibilitat i estadística a1440/430px, sense errors de JavaScript/MathJax,
imatges absents o desbordament de pàgina.

El snapshot local del productor havia refusat un symlink dins de `.opencode`;
la incidència és separada del build/preview del manual. Es conserva aquell
diagnòstic i no s'eliminen recursos privats per forçar-lo. La publicació utilitza
el workflow oficial fixat, amb comprovacions de fonts i publicació al checkout
net del runner i `reviewed_sha` exactament igual al commit de `main`.

La PR, el SHA fusionat, el run i les verificacions públiques es registren al
rebut de la sessió i al comentari final de la incidència13. Els PDFs i ZIPs
privats romanen fora de Git i del web.

## Actualitzacions dels proveïdors

La petició també demana revisar la disponibilitat d'Unaltraweb i els altres
components del hub per a Geodisseny, TIGIT i TIG. Es contrastaran release
publicada, admissió del hub i selecció observada del consumidor; aquests tres
estats no s'equiparen. La consulta no autoritza canviar pins ni reiniciar altres
sessions. L'adopció segueix el pla revisat i la decisió explícita de cada consumidor.
