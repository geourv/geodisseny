# Constantí: revisió pedagògica dels capítols 4 i 5

## Autorització de publicació — 6 d'octubre de 2026

L'autor ha demanat explícitament: «Publica el manual i ja veurém com va»,
després del lliurament de la revisió renderitzada i de la confirmació que
la feina tècnica era acabada. Registre exacte a
https://github.com/geourv/geodisseny/issues/7#issuecomment-6010267813.
Autoritza commit, push, PR, fusió i desplegament de la versió revisada.

La presentació, els capítols4i5 i la bibliografia passen a approved sobre
aquesta aprovació humana, no sobre els reports d'agent. Les indicacions
draft de les etapes següents són historial de preparació. Els guions i
paquets privats continuen conservats com a versions docents separades.

Es publiquen les19captures actives i les figures/fonts gestionades.
Els set bundles de captures descartats del primer pla queden arxivats
privadament, amb bytes i manifests originals, sense publicar captures
òrfenes de la recepta vigent. Els binaris del PDF són gestionats pel
workflow i no es versionen; originals SIG i ZIP de Moodle fora de Git/web.

### Verificació de la versió aprovada

Les12fonts públiques en català estan aprovades, amb0pendents.57computacions
actuals i19bundles actius. Prosa dels quatre fitxers revisats i qualitat de
fonts sense errors ni avisos. `editorial-publication-check` correcte sobre
font iHTML; es conserva l'avís ja verificat «I i» dels nombres romans al
capítol1.

PDF final sense marcadors draft:221p,49.424.633bytes, SHA
`93a690cbfd1e15eb86796457beda3c400fce5975452c1be8653a98e6982095c0`.
Límits de paraules correctes i pàgines dels exemples reinspeccionades.
Web local:18vistes —presentació, set capítols i bibliografia a1440/390px—,
108imatges, sense errors MathJax, imatges absents o desbordament. PDF
servit idèntic al generat;89ancoratges previs conservats i fonts privades404.

Reports d'agent actualitzats sobre les metadades approved i el perfil vigent
a revisions85–90; no són l'origen de l'aprovació humana. Captures descartades:
21fitxers arxivats a `tmp/dades-docents/arxiu-captures-descartades-20261006/`,
amb inventariSHA i manifests originals. Només les19captures actives entren
en el commit. Les fonts/figures de recerca es conserven com a bundles complets,
encara que no formin part del recorregut inicial del llibre.

La preparació `manual-release-prepare` ha creat el candidat latest ambPDF
`draft:false`. El wrapper pot respondre `Factory JSON output was truncated.`
tot i un procés correcte: s'exigeixen returncode0, manifest retingut i
comprovació estreta `manual-release-check`; no es pren una sortida truncada
com a prova de fracàs o èxit sense aquests controls.

La publicació es fa per PR i fusió sobre main, seguida del workflow manual
Deploy site amb `reviewed_sha` igual al SHA complet fusionat. PR, run i
comprovació del web/PDF públic es registren al rebut final de la incidència7.

Pràctica d'accessibilitat localitzada i verificada per a l'autor:
`tmp/dades-docents/practica-distancies-vilaseca-20261001-ampliada.zip`,
307fitxers,69.936.621bytes, SHA
`4c17e38e9d537838818568fea114b05304cf900aa7f7b9cbf6974452d0f164d3`.
GUIA38p,SOLUCIONS5p; inici `projectes/00-inici.qgz`. Nova preferència de
lliuraments compactes —GeoPackage multicapa i projecte principal— registrada
al perfil per a preparacions futures, amb originals i versions segellades
conservats.

Tasca [#7](https://github.com/geourv/geodisseny/issues/7), branca `content/7-autocorrelacio-exemples`. Revisió sol·licitada per l'autor després de la primera ampliació de l'autocorrelació. Reserva addicional exacta acceptada explícitament; una sola sessió al checkout principal. Fonts de contingut en draft per a revisió humana.

## Decisions de recorregut

- Capítol4: mapa i unitat → recompte per quadrats → centres → dispersió → kernel. Es mantenen els124registres de Constantí com a conjunt principal, sobre la mateixa ortofoto i límit.
- Capítol5:98potències publicades → vuit veïns i mitjanes → diferències respecte de la mitjana → Moran global → potències barrejades → resultat local → transferència a renda poligonal.
- Registres de450i3kW identificats a QGIS. Per a renda, municipi i codi de secció; els valors veïns s'etiqueten directament. Les lletres HH/LL/HL/LH s'expliquen com a categories, no com a noms de casos.
- Els logaritmes, matrius i notació deixen de precedir les operacions numèriques i la lectura del mapa. La I principal de Constantí utilitza kW originals; el logaritme queda com a sensibilitat declarada.
- Fora del recorregut descriptiu la regressió edat–potència i els residus. Els càlculs de recerca es conserven a `context/dades/autocorrelacio-exemples.md` i als paquets anteriors. Compartir seccions permet unir indicadors, sense establir una correspondència família–edifici–instal·lació.
- Capítols sense seccions d'una sola subsecció.45ancoratges previs de capítol4i44de capítol5 conservats, inclosos els automàtics, mitjançant títols o aliases. Ref i permalinks conservats. Sense C4/C5 com a abreviatures en prosa del lector.

## Fonts i preparació

`context/dades/preparar_constanti_pedagogia.py` prepara una destinació nova `tmp/dades-docents/qgis/constanti-pedagogia-20261005/`. Originals i paquets anteriors en lectura; el preparador rebutja regenerar una destinació segellada.

Entrades retingudes del paquet municipal de4/10: `municipis.gpkg`, ortofoto local iQML; hashes a `controls.json`. Punts ICAEN de l'extracció28/9/2026, data efectiva no verificada; límits ICGC20/1/2026 i ortofoto2025WMS a8m/píxel. Cap inferència sobre petjada exacta dels panells.

Per a renda, còpies de presentació de `autocorrelacio-20261005/autocorrelacio.gpkg`: les dades i les proves locals es reutilitzen; només canvien etiquetes i estils. GeoPackage nou `renda.gpkg` i Shapefile complet `renda.shp`; els originals mantenen el seu hash. La prova de Queen confirma151casos i I0,571916933 amb geometries completes.

Runtime fixat `sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc`: QGIS3.44.11, libpysal4.13.0, esda2.7.1. Cap canvi al proveïdor, al runtime ni als seus pins.

### Controls que sostenen els exemples

| Resultat | Control |
| --- | --- |
| Registres / potències publicades |124/98;94posicions en el subconjunt conegut |
| Suma publicada / central amb estimacions |2770/2970kW;200assignats |
| Malla |90quadrats d'1km²; sumes124registres i2770kW |
| Quadrats comparats |48registres/268kW versus17/891kW |
| Canvi de centre |1832,4298m, cap a l'oest i lleument al nord |
| Cercle / semieixos |2000,6564m /1934,4377i510,4672m |
| Kernel500/1500m |Integrals124,00168i124,00002registres |
| Mitjana dels98kW |28,265306 |
| Registre450kW |Veïns100,100,60,30,100,20,60,50; mitjana65kW |
| Registre3kW |Veïns4,4,3,10,3,3,3,3; mitjana4,125kW |
| Moran global en kW,kNN8 |I0,191856301;9999permutacions;3igualen/superen,p0,0004 |
| Exemple de barreja il·lustrativa |Mateixes posicions i valors;I−0,0163491 |
| QGIS local nominal |8HH/45LL/1HL/3LH/41NS |

El global s'ha contrastat amb la fórmula matricial directa. Locals de referència amb llavor20261005; el complement no exposa llavor al diàleg. Pseudo-p dels dos registres de lectura0,0244i0,0027; es mantenen després de BH0,05. La prova aporta evidència d'associació atribut–posició sota la regla, no de causes, interacció física o idoneïtat.

### Incidències de preparació i reparació

La primera construcció del subconjunt conegut conservava el camp `fid` original: l'ordre de retorn al GeoPackage canviava malgrat ordenar les features en memòria. El control d'identificadors i I va rebutjar-la. La construcció final genera FID propis i preserva `gml_id`, amb ordenació estable abans del càlcul i dels pesos. No s'han eliminat coincidències ni canviat potències per fer passar un control.

Un error JSON amb enter NumPy va impedir només desar l'input de figures, després de calcular i conservar els controls. `--finish` reconstrueix l'input a partir d'aquella execució, sense reexecutar les permutacions del complement.

El clon de renda va emetre un avís de recompteGDAL en exportar; la comprovació posterior exigeix151features per a cada capa completa,4per al veïnatge, geometries vàlides i la I Queen esperada. Cap dada perduda en la còpia comprovada.

## Figures i captures

Tres figures noves: `constanti-recomptes`, `constanti-moran`, `constanti-permutacions`. Actualitzades `constanti-pesos`, `punts-municipis` i `renda-moran`. Fonts QMD, inputs i outputs amb lock gestionat pel worker Python fixat d'unaltraweb.

Els municipis utilitzen zoom adaptat amb barres d'escala; els radis323/2278/2001m són el criteri de comparació, no la mida aparent. Renda en euros per persona també al gràfic; sense exigir estandardització per llegir el primer resultat. Títols i anotacions retallats detectats en revisió visual: marges, llegendes i alineació corregits a les fonts i outputs regenerats. Cap retoc manual de PNG/SVG.

19bundles actius:12de `constanti-pedagogia.yml` per al capítol4i7de `autocorrelacio-exemples.yml` per al5. Segona sessió de captura neta per donar llegenda local completa, sense acumular totes les capes descriptives. Tots x11/DPR1,català, sense avisos. Connexions GeoPackage desplegades a l'Explorador.

La figura d'accés a centres ja mostra Constantí; recompte i kernel tenen caixa de Processament oberta. Cercle/el·lipse visibles amb124punts, centre dels registres, límit i ortofoto. Els diàlegs acrediten configuració; Processing i els controls independents acrediten execució. `manual_click_by_click:false`.

## Verificació i lliurament

- `prose-check` i `manual-source-quality-check`: sense errors ni avisos als dos capítols; fórmules apilades/compactades per encaixar en mòbil.
-57computacions actuals; `site-check` abans dels builds. Expressions Python i SQL exactes del capítol executades al runtime QGIS.
- Web1440/390px:4vistes,26imatges —16al capítol4i10al5— sense errors MathJax, recursos absents, IDs duplicats o desbordament de pàgina.
-89ancoratges anteriors preservats. Quatre rutes privades comproven404:inputJSON,GeoPackage,ZIP,QMD.
- PDF local223p,49.425.856bytes, SHA `bff4fe0b5c75bda364edb1aa0914cc018f69208473a73170cbe31ab8c16cad86`. Text, codi, figures i pàgines clau inspeccionats; cap paraula fora dels límits. PDF servit al preview idèntic al generat.
- Portabilitat:/classe,offline/readonly, sense muntar originals. Cinc projectes vàlids amb4/4/6/4/5capes i rutes locals relatives. MatriuMoran, geometria de dispersió, totals de malla i integrals del kernel contrastats; hashes sense canvis.
- GUIA9p/SOLUCIONS2p. Comprovats tots els encapçalaments del cos, tres línies de codi, sis captures íntegres i límits de paraules/imatges.

Paquet nou privat `tmp/dades-docents/practica-constanti-pedagogia-20261005.zip`:95fitxers,65.545.875bytes, SHA `ec2a5e4d1fa580a5633927e6ff642b85fc2d1863911dcce64e721ca8c1681ce2`. CRC i tots els membres verificats; `sealed.json`, estat `private-author-review`, sense aprovació humana ni pujada a Moodle.

Recuperat també el ZIP històricr2 que va fallar per disc ple:62fitxers,27.941.923bytes, SHA `62d79ef394a4a5ce3ec06a104b9bd8c23aaee49218fbb3613afd042f4768ca2f`. L'intent parcial s'ha conservat amb sufix `.failed-disk-full.zip` i rebut propi; cap modificació del directori segellat. No és el material vigent d'aquesta revisió pedagògica.

Diagnosi i retalls registrats a67–70; vuit findings resolts explícitament a71–78, inclòs el de literals SQL del PDF anterior. Sis reviews d'estructura/evidència/línia a79–84. Fonts en draft: aquestes revisions d'agent no atorguen aprovació de l'autor.

Preview local: `http://127.0.0.1:32768/geodisseny/ca/`. Rebut d'operació `.cache/unaltraweb/manual-pdf-preview.json`. Diagnòstics de treball a `/tmp/opencode/constanti-pedagogia-{portabilitat,web-pdf,editorial}.json`, manifests de captura i controls del paquet; la traça durable és aquest document i les fonts.
