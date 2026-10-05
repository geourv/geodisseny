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

## Fusió i vinculació del workflow PDF

La PR https://github.com/geourv/geodisseny/pull/2 s'ha fusionat en
`0bf16fb5a33e1cc28f7e62c904dc424b1713ec53`, amb el mateix arbre de contingut
que el commit revisat `e31bcfdd03c978b8c6814ecaf416986a7cdacd65`.

El primer desplegament, run36928642568, ha detectat una vinculació inconsistent
del scaffold: el workflow esperava que la seva revisió fos la mateixa que
l'etiqueta OCI del PDF. La release oficial0.5.0 confirma que el PDF fixat
es va construir independentment a `d857f8c9f5fea90cf450c0b30b4e77a37b541275`.

La incidència https://github.com/geourv/geodisseny/issues/3 corregeix només
el commit del workflow reutilitzable perquè coincideixi amb aquest origen.
El fitxer és idèntic en les revisions02af700 i d857f8c: blob Git
`b81f2c26f286c334f4f590035a65e2caf50edd3e`,12.516bytes, verificat mitjançant
metadades GitHub. Es mantenen tots els digests i la implementació del workflow;
la comprovació de procedència continua activa. No s'ha llegit ni modificat
codi del proveïdor per aplicar aquesta vinculació.

## Publicació confirmada

La PR4 s'ha fusionat a `e7f41e9bfe6c9d652fe1bbf48c51936057b2c369`.
El desplegament https://github.com/geourv/geodisseny/actions/runs/36929459366
ha acabat correctament, amb procedència PDF, controls de figures, contingut,
compilació i publicació Pages. Les branques de les PR2 i4 s'han retirat després
de comprovar la fusió i la igualtat de l'arbre revisat.

- Web: https://geourv.github.io/geodisseny/ca/.
- PDF: https://geourv.github.io/geodisseny/assets/pdf/manual-ca.pdf.
- PDF publicat:199pàgines, autor Benito Zaragozí; SHA-256
  `1bb9e96893116785e01f032fd37297266b0132319b1cd3e8b061cfda980eab72`.
- `manual-release.json` públic confirma latest. Presentació i capítol2 revisats
  al web publicat a1440/390px;29figures, sense errors ni desbordaments.

La preparació posterior de visibilitat pertany a la incidència5 i a la branca
`content/5-visibilitat-mdt-mds`. El capítol3 torna a draft en aquella branca;
la previsualització ampliada local no és una segona publicació autoritzada.

El 2 d'octubre, l'autor ha demanat revisar aquesta pràctica amb torxa,
carretera Vila-seca–la Pineda i polígon de cobertes. Es manté en la mateixa
branca de la incidència5, en draft. Els paquets i intermedis són per a Moodle,
fora de Git; el nou treball no amplia l'autorització de publicació anterior.

La revisió r2 posterior incorpora perímetre sense forats, accessos a les eines
i context històric del complex. El capítol3 i la bibliografia queden en draft;
el PDF local de215pàgines i el paquet r2 són per a la revisió de l'autor.
El registre de comprovacions és `context/dades/visibilitat-costa-r2.md`.

La revisió r3 de la mateixa tasca substitueix l'àmbit per un recinte compacte
obtingut amb buffers i afegeix eines desplegades, lots i MDS inicial. El PDF
local té219pàgines; registre a `context/dades/visibilitat-costa-r3.md`.
Continua pendent de revisió de l'autor, amb el mateix abast d'aprovació anterior.
