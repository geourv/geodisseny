# Captures QGIS per al manual

## Criteri pedagògic

Les figures calculades amb Python expliquen el model i els exemples numèrics.
Les captures QGIS mostren on es prenen decisions a la interfície. Una captura
de diàleg no acredita haver validat un resultat territorial. Conservar idioma,
versió real, prompt, recepta, paràmetres, selectors i manifest.

## Integració actual — r.walk i isòcrones, 1 d'octubre de 2026

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
