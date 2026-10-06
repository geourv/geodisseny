# Captures QGIS per al manual

## Criteri pedagògic

Les figures calculades amb Python expliquen el model i els exemples numèrics.
Les captures QGIS mostren on es prenen decisions a la interfície. Una captura
de diàleg no acredita haver validat un resultat territorial. Conservar idioma,
versió real, prompt, recepta, paràmetres, selectors i manifest.

### Connexions GeoPackage a l'Explorador

Criteri de l'autor del3d'octubre de2026 per a les properes captures:
quan hi hagi GeoPackage, crear les connexions als fitxers i desplegar el node
GeoPackage, les connexions pertinents i les seves capes a l'Explorador de la
part superior esquerra. Els noms han de permetre relacionar les fonts amb
les capes utilitzades en el pas. Registrar aquest estat als prompts i receptes
de la propera preparació i comprovar-lo a la captura, amb selectors reals.

L'autor permet ajornar la regeneració de les captures actuals. Els17bundles
de r3 es conserven; el nou criteri s'aplicarà en preparar o regenerar captures.

## Integració actual — seqüència pedagògica de Constantí

19bundles actius:12de `constanti-pedagogia.yml` al capítol4i7de
`autocorrelacio-exemples.yml` al5. Context municipal també als accessos:
recompte, centres i kernel visibles a la Caixa d'eines; menú Vectorial
desplegat sobre Constantí. Cercle i el·lipse visibles al mapa amb124punts,
centre dels registres, límit i ortofoto. Registres de450i3kW etiquetats
en el capítol5; les potències dels vuit veïns es poden llegir en una ampliació.

La sessió d'autocorrelació arrenca amb només les capes pertinents: llegenda
local completa, sense totes les capes descriptives acumulades. Renda amb
municipi/codi i xifres veïnes, sense lletres de cas. Tots els manifests
x11/DPR1,català,sense avisos. Explorador amb GeoPackage desplegat.
Font/controls i paquet: `context/dades/constanti-pedagogia.md`.

## Integració anterior — autocorrelació, 5 d'octubre de 2026

`autocorrelacio-exemples.yml` incorpora nou bundles `c5-…`: eines,
renda-parametres, renda-resultat, renda-veins, constanti-dades,
constanti-parametres, constanti-resultat, gi-parametres i gi-resultat.
Explorador amb `autocorrelacio.gpkg` desplegat, català, x11/DPR1 i
nou manifests sense avisos. Quatre figures analítiques QMD complementen
les captures; C5 conté17imatges.

S'ha revisat el selector del grup LISA perquè «Local Moran's I» també
coincidia amb l'eina bivariant. L'accés mostra les tres eines i el peu
identifica la univariant. Les caselles de normalització s'han comprovat
visualment després de l'espera del diàleg: marcades a Moran, desmarcada a Gi*.
No s'han retocat PNG, SVG ni manifests; les captures surten de la recepta.

Processing ha executat els dos Moran i Gi* sobre les entrades corresponents.
Els diàlegs acrediten configuració, no un recorregut manual clic a clic.
Quadrants contrastats i Z de Gi* verificats amb fórmula independent.
Casos de renda A/B/C i punt A de450kW desenvolupats al text i als peus.
Controls, limitacions i paquet privat: `context/dades/autocorrelacio-exemples.md`.

## Integració anterior — pràctica municipal de Constantí

`punts-municipals.yml` afegeix cinc captures: `municipals-dades`,
`municipals-camp`, `municipals-centre`, `municipals-resultat` i `municipals-ellipse`.
Mateixos124punts, potència publicada conservada, camps d'escenari decimals.
L'ortofoto WMS ICGC2025 a8m/píxel dona context; el resultat utilitza àrees
proporcionals a w_mid i colors per distingir pesos publicats/assignats.

La connexió municipis.gpkg queda desplegada a l'Explorador. Cinc manifests
correctes, x11/DPR1, català, sense warnings; PNG/SVG revisats. Captures
configurades i càlculs verificats es documenten per separat. Dades i projecte
portable al suplement privat municipal; detall a `context/dades/punts-tarragones.md`.
Les captures comarcals d'accés i de les ampliacions continuen com a referència.

## Integració anterior — punts del Tarragonès, 4 d'octubre de 2026

14captures noves de `punts-tarragones.yml`, amb prompt propi, dades i resultats
verificats. GeoPackage i connexions visibles a l'Explorador: declaració
`connections` de tipus `gpkg`, refresc amb `mActionRefresh` i desplegament
amb `expand_tree_item`. Els noms dels dos fitxers i les capes són reals.

Menú Vectorial/Analysis Tools i caixa Anàlisi vectorial oberts; controls
de centres, geometria per expressió, malla, recompte, kernel i seccions.
Requadres amb `margin: 0`, sense ombra, per respectar els textos veïns.
Els píxels X/Y del kernel es resolen amb els widgets natius, no amb el títol.
Selector «resum» verificat per evitar la coincidència aproximada amb «seccions».

Tots els manifests: x11/DPR1, català, sense warnings. Els diàlegs mostren
configuració; els càlculs i la portabilitat s'acrediten independentment.
C4:21imatges,14captures; revisió1440/390px i PDF231p. Fonts, controls,
incidències i hashes a `context/dades/punts-tarragones.md`.

## Integració de visibilitat — recinte compacte, caixa d'eines i MDS, r3

Disset captures: dotze de visibilitat-costa i cinc de visibilitat-acces.
Nom visible «Recinte petroquímic d'estudi», amb222,94ha; buffers +150/−150m
en dos diàlegs, distàncies emmarcades sense cobrir l'ajuda. Ortofoto WMS i
MDS inicials amb el mateix enquadrament i llegenda de cotes.

Caixa oberta amb trigger_action «Caixa d'eines»; expand_tree_item i
select_tree_item mostren Viewshed dins de GDAL/Miscel·lània ràster. Menú
Vectorial/Geoprocessing Tools/Àrea d'influència realment desplegat, i fila
correcta d'Àrea d'influència al panell. El selector per àlies havia apuntat
a Create wedge buffers: corregit amb el prefix «Àrea d'influ» i inspecció
visual. Requadres als botons i files;17manifests sense warnings, x11/DPR1.

La recepta de probes privats s'ha desregistrat. No s'ha publicat el menú
contextual de lots bloquejat; el text explica l'accés segons la documentació
QGIS i la cadena executable ha reproduït179càlculs amb controls exactes.

C3 té25imatges i24figures, revisades a1440/390px i al PDF219p. GUIA26p,
SOLUCIONS3p, cinc SVG regenerats. Deu projectes de37capes; registre i hashes
a `context/dades/visibilitat-costa-r3.md`. Material en draft per a l'autor.

## Integració anterior — accessos i perímetre, 2 d'octubre de 2026

Receptes `visibilitat-acces.yml` i `visibilitat-costa.yml`:12captures totals.
Accés a Procés → Caixa d'eines i al botó de la barra, amb glif de clic;
diàleg nou Suprimeix els forats. Dades de la revisió r2, amb el perímetre
de184,44ha sense forats i36capes en deu projectes.

Backend x11 explícit, DPR1, mateixa imatge QGIS3.44.11. S'ha corregit el
desplaçament del marcador que apareixia en el crop offscreen amb DPR1,04268.
L'etiqueta del llindar s'ha escurçat a «0=tots»; controls i captures inspeccionats.
No s'ha editat codi del proveïdor ni cap sortida manualment.

El probe d'una cerca no oberta, amb warning d'acció ignorada, es conserva
privadament a `tmp/dades-docents/arxiu-prova-acces-20261002/`; no és material
docent. Els12manifests finals són correctes i no tenen warnings.

C3:20imatges en19figures, revisades al web1440/390px i al PDF215p. Guió19p,
notes3p. Nova figura QMD/SVG que compara original, deleteholes, convexa,
còncava0,3 i tancament25m. Registre complet a `context/dades/visibilitat-costa-r2.md`.
Passada web final repetida després de corregir la metadada de la referència
bibliogràfica:20imatges carregades, cap ancoratge perdut ni overflow. Inspecció
directa de `_site`: el probe de cerca rebutjat no forma part del preview.

## Integració anterior — torxa, carretera i polígon, 2 d'octubre de 2026

Nou captures de `context/qgis/visibilitat-costa.yml`, prompt homònim:
identificació de dades i torxa, Viewshed puntual, intervisibilitat, Calculadora
ràster amb Domini, mostreig de carretera, suma de37conques MDT, graella d'àrea
i mapa d'alguna part del polígon (57A o T). Imatge QGIS3.44.11 fixada.

El client MCP va expirar mentre acabava el prefix de nou captures. Els nou
PNG/SVG/manifests s'han completat; manifests ok:true, sense avisos de selectors,
i contenidors de render retirats. Captures inspeccionades. La prova de càlcul
continua a controls/verificacio-qgis.json; els diàlegs només mostren paràmetres.

Quatre QMD/SVG actualitzats; perfils amb ampliació dels últims80m per veure
la intercepció prop del receptor. Corregit l'espai entre eixos i llegendes.
El capítol conserva16figures, ara16imatges, i substitueix l'assaig cadastral.
La recepta nord s'ha desregistrat i els seus bundles no versionats s'han
arxivat després de contrastar-los amb el ZIP immutable. Registre a
`context/dades/visibilitat-costa.md`.

Revisió final:16imatges/16figures de C3 al web1440/390px, cap incidència de
càrrega, MathJax, ancoratges o overflow. Manual PDF209p, guió16p i notes3p
inspeccionats. Controls QGIS natius i portabilitat de34capes per projecte
documentats al paquet segellat de211fitxers, sense pujada a Moodle.

## Integració substituïda — visibilitat nord, 1 d'octubre de 2026

Nou captures de `context/qgis/visibilitat-nord.yml`, prompt homònim, produïdes
pel MCP amb QGIS3.44.11. Crida final `visibilitat-nord.visibilitat-nord-mostreig`:
dades, punts lineals, graella, Viewshed, Calculadora ràster de cota mínima,
mapes MDT/MDS, acumulació ponderada i mostreig als receptors.

Bundles complets a `assets/captures/visibilitat-nord-*.png` i `.annotations.svg`,
amb manifests individuals. Cap avís de selectors. El capítol referencia els PNG.
R8 quedava massa prop del marge superior: ampliat l'enquadrament comparatiu a1,2.
Escurçada l'anotació «Cotes absolutes» per evitar el retall lateral del diàleg.
Labels de mapa20pt; cap canvi manual a les imatges generades.

Quatre figures QMD/SVG: mostreig, comparació MDT/MDS, taula de receptors i perfils.
Corregits marges i solapaments de llegendes a les fonts. Comparació amb cotes
absolutes fixes, no només els mateixos nombres d'altura relativa.

Capítol3:17imatges dins de16figures, revisió web a1440/390px, sense imatges
trencades, errors MathJax, ancoratges perduts ni overflow. Revisats els SVG,
captures i taules del PDF local213p, i els guions14/3p. Un enllaç intern a la
ponderació es va corregir afegint l'ancoratge estable a l'apartat corresponent.
L'auditoria HTML conserva avisos d'opacitat/inspecció limitada del proveïdor;
la revisió visual dels recursos nous està completada.

## Integració anterior — r.walk i isòcrones, 1 d'octubre de 2026

Sis captures addicionals amb unaltracaptura, totes amb PNG, SVG i manifest:

- `rwalk.rwalk-isocrones-tancat` executa `rwalk-parametres`, `rwalk-resultat`,
  `rwalk-contorns`, `rwalk-isocrones-obert` i `rwalk-isocrones-tancat`.
- `girs.xarxa-girs-parametres` mostra el criteri Més ràpid de l'eina nativa.
  La manca de taula de girs s'acredita amb l'esquema públic dels paràmetres i
  la documentació de QGIS3.44, no només amb els camps visibles de la captura.

Fonts: `context/qgis/rwalk.yml`, `girs.yml` i prompt `accessibilitat-ampliada.md`;
configuració `.unaltracaptura-qgis.yml`. Mateix runtime QGIS3.44.11 fixat.
Cap avís de selectors. Contingut visible en PNG anotat del proveïdor.

El primer render va revelar una col·lisió de noms QML entre el ràster de classes
i el vector de contorns: el mapa apareixia gris. Resolt a la font de preparació
amb basenames diferents, projectes regenerats i captures repetides. Comprovats
blau/verd/taronja, llegenda, O/D i la comparació oberta/tancada amb extensió igual.
Mogudes les anotacions de D cap a l'esquerra per preservar l'etiqueta del punt.

Quatre SVG calculats complementen les captures: rampa anisòtropa, gir condicionat
pel tram d'arribada i dos mapes comparatius d'isòcrones (xarxa/ràster). Els mapes
comparteixen límits i colors; les porcions de xarxa no s'embolcallen amb polígons.
Corregides densitat de ticks, marge del títol de l'eix i ordre de dibuix d'una
punta de fletxa a les fonts QMD. Cap edició de sortides generades.

Capítol2: 29 imatges dins de28figures numerades. Sis captures noves i quatre SVG
revisats al manual de201pàgines i al guió ampliat de38pàgines. Web a1440/390px
sense imatges trencades, errors MathJax, ancoratges perduts ni desbordaments.

## Integració anterior — distàncies, 1 d'octubre de 2026

15 captures noves amb unaltracaptura i QGIS 3.44.11, integrades al capítol 2
i al paquet privat `practica-distancies-vilaseca-20261001.zip`. Substitueixen
les dues referències antigues d'accessibilitat, que es conserven com a historial.
En aquella passada, el capítol tenia19figures: quatre de calculades i aquestes captures.

Fonts: prompt `context/qgis/distancies.md` i cinc receptes registrades a
`.unaltracaptura-qgis.yml`. Crides finals del MCP, amb aquesta configuració:

| Recepta | Darrer capture ID | Captures |
| --- | --- | ---: |
| `context/qgis/distancies.yml` | `distancies.distancies-vector-resultat` | 3 |
| `context/qgis/distancies-raster.yml` | `distancies-raster.distancies-raster-resultat` | 2 |
| `context/qgis/distancies-xarxa.yml` | `distancies-xarxa.distancies-isocrones-resultat` | 4 |
| `context/qgis/distancies-cost.yml` | `distancies-cost.distancies-cost-resultat` | 4 |
| `context/qgis/distancies-pineda.yml` | `distancies-pineda.distancies-pineda-cost` | 2 |

Cada crida final executa també les captures prèvies de la recepta. Bundles
complets a `assets/captures/distancies-*.png` i `.annotations.svg`, amb
manifests a `context/qgis/manifests/`. El contingut referencia els PNG anotats
del MCP; cap sortida s'ha retocat manualment.

- O/D/P2 visibles sobre ortofoto; vector 368,3 m, ràster 370,7 m, xarxa 454,1 m.
- Àrees de servei de 3/6/12 min: 0,05/0,10/0,20 h al paràmetre, camp de
  velocitat 5 km/h. La captura ressalta explícitament la conversió.
- Fricció i cost acumulat visibles com a ràsters diferents. `r.cost` parteix
  d'O; la captura addicional de `r.path` ressalta **D** com a punt de retorn.
- Pineda: dues captures específiques del model 1/20, sense MDT en la fricció.
- Etiquetes de mapa grans amb halo; callouts vinculats a paràmetres o extents
  cartogràfics. El diàleg vectorial es deixa sense callouts per no tapar valors.
- Les accions `open_project`/`load_project` no eren suportades i s'ignoraven.
  S'utilitzen càrregues explícites de capes en receptes separades. L'enquadrament
  es fixa als passos de cada captura amb `zoom_to_layer`, no només al setup.
- Inputs GRASS identificats pels noms de capes carregades. Bàner de missatges
  netejat després del zoom; cap camp essencial buit ni modal de plugin.
- Dades i resultats preparats abans amb el mateix runtime; mostrar el diàleg
  no s'utilitza com a prova del càlcul. Controls independents al paquet privat.
- Revisió final: 15 captures inspeccionades al PDF complet de 191 pàgines;
  web del capítol a 1440/390 px, 19 imatges carregades, sense errors MathJax,
  ancoratges perduts ni desbordaments. Els guions autònoms també estan revisats.

## Integració anterior — 30 de setembre de 2026

Quatre receptes noves, totes renderitzades pel MCP amb QGIS 3.44.11:

- `visibilitat.intervisibilitat-mostreig`: Viewshed (30/1,7 m) i mostreig.
- `estadistica.kernel-resultat`: sis captures de centres, dispersió, recompte
  i KDE. La captura del centre inclou POT_KW i agrupació buida. La de dispersió
  utilitza Geometria segons l'expressió amb els atributs calculats del centre.
- `autocorrelacio.hotspots-resultat`: Moran i Gi*, paràmetres i mapes. Desactivar
  la capa de Moran abans de mostrar Gi*: altrament tapa el resultat inferior.
- `temperatures.temperatures-resultat`: IDW, Variogram, Ordinary Kriging i mapa.
  A IDW la variable efectiva és tx_c a la fila afegida de la taula, encara que
  el desplegable de preparació mostri fid. Els ràsters desats tenen 135×133
  cel·les de 2.000 m, alineades; comprovar les propietats de sortida.

La recepta de xarxa s'ha repetit amb `scale: 2.5` sobre l'àmbit del detall.
Els originals i resultats de càlcul són privats a tmp/dades-docents/qgis/.
Les captures referenciades conserven PNG, SVG amb fons incrustat i manifest.

Complements actius: processing, HotSpotAnalysis_v3 (nom de carpeta; versió
real 4.0.0) i processing_saga_nextgen 1.3.0. Commits i hashes exactes a
context/qgis/plugins-lock.json. Cache vigent: sufix 139383569f94.
SDEllipse es va retirar de l'arrencada: el ZIP de fonts fixat no incloïa el
mòdul resources compilat i obria un error modal. No s'ha modificat el proveïdor;
el cercle i l'el·lipse del manual utilitzen expressions natives. El cache
anterior i la descàrrega automàtica del repositori de plugins es conserven.

La revisió va detectar lletra més petita i desplaçament de requadres en els
SVG anotats, especialment després de retallar amb DPR1,0426788. Les sortides
PNG anotades del mateix MCP mantenen la correspondència amb els controls.
El manual referencia aquestes PNG per a les14captures noves visibles amb
callouts; els SVG i manifests es conserven dins dels bundles. S'ha escurçat
l'etiqueta de l'el·lipse per evitar el retall lateral del text.
`size` i `font_size` no modificaven els callouts i s'han retirat de la recepta.
Les comprovacions tipogràfiques vectorials ja no s'apliquen als textos rasteritzats:
cal inspecció visual web/PDF, no declarar automàticament que la interfície
sencera tingui lletra de8pt. No s'han modificat generats a mà ni el proveïdor.

## Integració anterior amb dades reals — 29 de setembre de 2026

- Subfigures d'accés/configuració i resultat als capítols 2 i 4, amb dades
  territorials i paràmetres comprovats. Les captures sintètiques anteriors ja
  no es referencien al manual; es conserva la seva font com a historial.
- ICAEN: menú `Vectorial > Analysis Tools > Coordenades mitjanes` i mapa dels
  centres sobre 3.762 registres amb potència coneguda. Centre sense pes
  (357387.9674,4556891.1709), ponderat (354528.5181,4556391.8690), desplaçament
  2902.7147 m. `context/qgis/preparar_icaen.py` contrasta QGIS amb numpy.
- Xarxa: diàleg de ruta sobre 4.512 eixos RTT i detall del desviament en invertir
  el sentit de l'eix 1331675. Base 10989.257 m, alternativa 11012.834 m.
- Fonts: `icaen-centres.md/.yml`, `accessibilitat.md/.yml`; manifests individuals
  a `context/qgis/manifests/`; PNG i SVG incrustats a `assets/captures/`.
- Reproducció MCP: `icaen-centres.icaen-resultat` i
  `accessibilitat-real.accessibilitat-resultat`, sempre amb configuració explícita
  `.unaltracaptura-qgis.yml`. El proveïdor renderitza també els passos anteriors.
- Declarar `plugins: [processing]` perquè es carreguin els menús. La traducció
  instal·lada combina català i anglès; s'utilitzen els noms realment visibles.
- El retall de càmera del menú/diàleg preserva píxels, no reconstrueix controls.
  Entrades calculades abans de la captura amb el mateix QGIS 3.44.11 fixat per ID.
- Muntar fonts GeoPackage en només lectura durant les preparacions: QGIS pot
  canviar capçaleres SQLite fins i tot sense alterar cap taula. Es van comparar
  taules i esquema i restaurar exactament els bytes ICAEN/ICGC des dels ZIP
  verificats després d'observar aquest comportament en una primera prova.

## Primera integració, substituïda al contingut visible

- Capítol 2: configuració de `native:shortestpathpointtopoint`; xarxa sintètica
  de la figura de distàncies, ruta més curta i extrems explícits.
- Capítol 4: configuració de `native:meancoordinates`; quatre punts de l'exemple,
  camp `POT_KW` i agrupació buida. Comparar amb l'execució sense pes.
- Dades: `python3 context/qgis/generar_dades.py` les crea a
  `tmp/dades-docents/qgis/`. Els punts del capítol 4 es traslladen a UTM sumant
  350.000 m i 4.550.000 m: el centre esperat és (352.800, 4.553.200) m.
- Les receptes específiques utilitzen l'acció genèrica disponible
  `open_processing_algorithm_dialog`; es mantenen com a fonts d'autor amb
  els prompts respectius, sense reutilitzar el generador especialitzat de buffer.
- Només PNG/SVG de captures es referencien al manual; dades i manifests són privats.
- Dues captures renderitzades amb el MCP, sense avisos de selectors. Revisats els PNG:
  capa, pes, agrupació, estratègia i extrems correctes; el ressalt és un requadre
  sobre el control real i no tapa l'ajuda ni altres valors.
- QGIS 3.44.11, Qt 5.15.17, Python 3.13.7, GDAL 3.10.3; locale `ca`.
  La traducció disponible manté alguns camps i ajudes en anglès.
- Imatge fixada a `sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc`.
  Comandes MCP de reproducció: `render_recipe(config=".unaltracaptura-qgis.yml",
  capture="centres-ficticis.centres-parametres")` i
  `render_recipe(config=".unaltracaptura-qgis.yml", capture="xarxa-ficticia.ruta-parametres")`.

## Seqüència prevista per a altres tècniques

| Capítol | Captura útil | Decisió que ha d'explicar | Prerequisit |
| --- | --- | --- | --- |
| 1 | Taula i resum del mateix exemple | Valor absent, variable i nombre de casos | Taula petita completa |
| 3 | Diàleg viewshed i consulta d'un píxel | Altura relativa i codis de sortida | MDT/MDS i perfil verificat |
| 5 | Veïnatge, mapa de valors i LISA | Matriu i inferència, no només color | Motor de Moran local amb pesos i permutacions verificats |
| 6 | Mostreig del MDT i resultat residual | Covariable i reconstrucció | Observacions comparables i cadena geoestadística validada |
| 7 | Calculadora ràster i inspecció d'una cel·la | Suma de factors normalitzats i màscara | Factors, alineació i nuls comprovats |

Una ampliació ha d'afegir la captura quan la dada i l'eina estiguin preparades,
amb una explicació anterior i una comprovació posterior. No representar finestres
buides o paràmetres fictíciament traduïts com si fossin una execució completa.
