# Autorització de publicació del manual

L'1 d'octubre de 2026, després de revisar les previsualitzacions i les ampliacions
del capítol de connectivitat, l'autor ha demanat explícitament:

> Ara fem push, PR i fusió dels canvis per publicar el manual en ghpages.

Aquesta autorització correspon a la versió actual de la presentació, set
capítols, bibliografia i pàgines de redirecció en català. Les metadades passen
de draft a approved sobre aquesta base humana; els registres de revisió d'agent
continuen sense conferir aprovació. L'ampliació posterior de visibilitat és una
tasca nova i tornarà a draft el contingut que s'hi modifiqui.

Reserva i registre d'autorització:
https://github.com/geourv/geodisseny/issues/1#issuecomment-5940232775.

La versió revisada inclou 41 fonts de figures computades, les captures QGIS,
els exemples territorials i els blocs de marxa anisòtropa i isòcrones. Els
controls i les revisions visuals es documenten a
`context/revisio-manual-2026-09-28.md`. L'avís mecànic «I i» del títol
«Errors de tipus I i II» es conserva perquè correspon al nombre romà i la
conjunció, no a una duplicació accidental.

Els paquets de Moodle continuen a `tmp/dades-docents/`, exclosos de Git i del
lloc públic. El PDF del manual i la coberta són artefactes gestionats pel
proveïdor; no es versionen com a fitxers generats. La publicació utilitza el
workflow del repositori amb el SHA exacte del commit revisat de main.

La comprovació de publicació va detectar que `assets/plotly/demo.html`, una
demostració de la plantilla sense cap referència als capítols o les pàgines,
superava el límit de lectura del verificador editorial. Els assets del tema
no respectaven l'exclusió per path. S'utilitza la configuració pública de
defaults de Jekyll per marcar només aquesta demo amb `published: false`,
conservant `sitemap: false` per als assets. Les pàgines del consumidor tenen
llengua i layout explícits. Es manté el control complet de publicació.

Els SVG generats per Matplotlib i algunes captures contenen espais finals
propis de la serialització XML. Es conserven els bytes dels proveïdors i els
seus hashes; el control d'espais dels fitxers d'autoria exclou aquests dos
grups de sortides generades. No s'han retocat artefactes per silenciar l'avís.
