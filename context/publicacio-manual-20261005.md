# Autorització de la versió ampliada del manual

El 5 d'octubre de 2026, després de les revisions i previsualitzacions de la
conversa, l'autor ha demanat explícitament:

> Fes commit, push, PR, fusionar, cal publicar la última versió del manual en ghpages

Registre a la incidència5:
https://github.com/geourv/geodisseny/issues/5#issuecomment-5985904533.
Branca de treball: `content/5-visibilitat-mdt-mds`.
Base revisada: `e7f41e9bfe6c9d652fe1bbf48c51936057b2c369`.

## Abast de l'aprovació

L'autorització cobreix la versió actual del manual, incloses les ampliacions
de visibilitat, Snow i Wald, la pràctica municipal de Constantí, els escenaris
d'imputació, la comparació municipal, les captures, les figures, la bibliografia
i les correccions de títols i redacció. Les set fonts pendents passen a approved:

- `_chapters/ca/01-fonaments-geodisseny.md`.
- `_chapters/ca/03-visibilitat.md`.
- `_chapters/ca/04-estadistica-espacial.md`.
- `_chapters/ca/05-autocorrelacio-espacial.md`.
- `_chapters/ca/06-geoestadistica-interpolacio.md`.
- `_chapters/ca/07-avaluacio-multicriteri.md`.
- `_chapters/ca/90-bibliografia.md`.

Aquesta transició reflecteix l'aprovació humana. Els registres d'agent no
concedeixen aprovació; l'historial de troballes, resolucions i revisions
obsoletes es conserva a `context/editorial-state.json`.

## Evidència revisada

La darrera previsualització del manual té235pàgines, SHA-256
`6d29bba2ea6c5e2967d518636580fb115d1b28cbfd466c75d0a5b289954840ca`.
Els controls numèrics, projectes reoberts offline/readonly, fonts històriques,
drets i comprovacions web/PDF es documenten a:

- `context/revisio-manual-2026-09-28.md`.
- `context/dades/visibilitat-costa-r3.md`.
- `context/dades/punts-tarragones.md`.
- `context/dades/snow-wald.md`.

Hi ha50computacions actuals. La revisió final C4/C5 inclou31imatges a
1440/390px; les revisions anteriors cobreixen els altres capítols modificats.
Les noves sortides es conserven amb fonts, inputs i manifests. L'inventari
previ de la publicació té176paths i65.259.178bytes abans d'afegir aquest
registre i les metadades d'aprovació; el màxim individual és4.352.856bytes.
No s'hi han detectat credencials ni fitxers de dades privades.

## Publicació

Es manté el canal `latest`. El PDF i la coberta són artefactes gestionats,
regenerats pel workflow; no es versionen els binaris de la previsualització.
Els GeoPackage, TIFF, projectes i ZIP de Moodle continuen a `tmp/`, fora de
Git i del lloc públic. Els petits inputs necessaris de figures queden a
`context/`, exclòs de Jekyll.

Abans de publicar s'executen els controls de font, computacions, aprovació,
prosa, site-check i editorial-publication-check, i es revisa la construcció.
Els avisos coneguts «I i» dels nombres romans, inspecció SVG/logos i mida
web lleugerament superior de la comparació municipal no s'han silenciat
modificant generats.

El desplegament es fa després de la PR i la fusió, mitjançant `Deploy site`,
amb `reviewed_sha` igual al SHA complet fusionat de main. Es comproven el
run de GitHub Actions, les pàgines públiques i el PDF servit. La PR i els
rebuts finals es registren a la incidència5.
