# Visibilitat costa r2: perímetre, accés a eines i context territorial

Registre històric del lliurament r2. La revisió activa és
`context/dades/visibilitat-costa-r3.md`; aquest ZIP es conserva immutable.

Revisió del2d'octubre de2026 a petició de l'autor, mateixa incidència5 i
branca `content/5-visibilitat-mdt-mds`. El capítol3 i la bibliografia amb la
referència nova queden en draft. No hi ha autorització nova de publicació.
Fonts i guions actius conserven els paths; la còpia exacta anterior és al ZIP
immutable `practica-visibilitat-costa-20261002.zip`, SHA
`a5130ad5221a21e8e86350c485731c4384b44c720f1ce3a879815d65577946c1`.

Destinació nova: `tmp/dades-docents/qgis/visibilitat-costa-20261002-r2/`.
El preparador `context/dades/preparar_visibilitat_costa.py` ha copiat17fonts
verificades directament del ZIP, sense obrir ni modificar els originals
QGIS del lliurament anterior. Nova fase --geometry abans de --build i --style,
en processos separats. Dades, intermedis i lliurament de Moodle fora de Git.

## Comparació de geometries

Totes les operacions s'han executat amb QGIS3.44.11, EPSG:25831 i el·lipsoide
NONE. Font: MCSC2024, id1459998. Es conserva la geometria original a
dades/coberta-original.gpkg i les cinc alternatives a dades/alternatives-perimetre.gpkg.

| Operació | Àrea m² | Forats | Afegit exterior m² |
| --- | ---: | ---: | ---: |
| Original | 1625929,156054 | 19 | 0 |
| native:deleteholes, MIN_AREA0 | 1844438,641113 | 0 | 0 |
| native:convexhull | 2443335,647898 | 0 | 598897,006785 |
| native:concavehull, ALPHA0,3 | 2380405,597543 | 0 | 535966,956430 |
| native:buffer, +25/−25m | 1709344,790779 | 15 | 33038,006009 |

La còncava usa els vèrtexs de l'exterior, sense forats i sense dividir
multipart. El doble buffer usa8segments, unions arrodonides i dissolució;
retira també10,765175m² de la font per discretització. No s'afirma que altres
llindars de còncava donin el mateix resultat.

S'adopta **eliminar forats**: omple218509,485059m² interiors i conserva exactament
l'exterior. Les entrades obertes del contorn romanen; no són anells interiors.
Es diferencia expressament el perímetre d'estudi de184,44ha de la coberta
industrial classificada de162,59ha i del conjunt del Polígon Sud.

La graella250m continua donant57fragments, però els seus pesos i algunes
posicions canvien. Suma de pesos1844438,641113m². La superfície d'obstacles
i les cotes absolutes segueixen el mateix criteri de la versió anterior.

## Controls de càlcul i portabilitat

- Mateix domini comparable3.490.455cel·les; mateixa torxa i carretera.
- T MDT/MDS:2.962.199/447.860cel·les visibles. Carretera MDT37conques:
  1.461.016cel·les amb alguna visió; màxim33. Contrast comú28posicions;
  T MDS als37registres:7visibles,21ocults,9no calculats.
- 57A sense T:2.168.972/101.832cel·les amb visió, MDT/MDS.
- Alguna de57A o T:2.972.765/461.007cel·les,85,17%/13,21%.
- R1 A_MDT81,906035%; R3 65,191662%; R4 74,951039%. A_MDS0% als quatre
  receptors de contrast. T/G i R5 nul conserven les respostes anteriors.
- QGIS natiu reprodueix deleteholes,57fragments i punts,37mostres de carretera,
  ruta, cota mínima, màscara, suma i consultes. Igualtat del perímetre amb
  l'exterior original contrastada també amb GEOS/Shapely.
- Deu projectes de36capes oberts readonly a /paquet, sense repositori font
  ni xarxa. Nou projecte09-perimetre. Report controls/verificacio-qgis.json.

## Captures i figures

- Recepta principal visibilitat-costa:10captures, inclòs el diàleg
  `native:deleteholes`. Recepta visibilitat-acces: menú Procés i botó de barra
  «Caixa d'eines», amb drecera real Ctrl+Alt+T. La cerca per nom s'explica
  al text; no s'atribueix al MCP una cerca que no ha mostrat.
- El probe `show_processing_toolbox` retornava el warning d'acció ignorada.
  Va generar tres fitxers de diagnòstic als paths configurats, tot i ser un
  probe; arxivats a tmp/dades-docents/arxiu-prova-acces-20261002 amb hashes.
  No es distribueixen com a captura de cerca. Això corregeix la previsió
  inicial de la reserva, que els havia considerat encara no creats.
- La revisió visual va detectar desplaçament del marcador en un crop amb
  DPR1,04268. S'ha seleccionat el backend públic x11 a les dues receptes:
  DPR1 i marcador sobre el botó correcte, sense canviar codi del proveïdor.
  L'anotació del paràmetre de forats s'ha escurçat a «0=tots» per evitar retall.
- Tots els manifests finals sense warnings; nou camp de comprovació al
  preparador refusa copiar captures amb warnings al paquet.
- Cinc QMD/SVG: mostreig, MDT/MDS, matriu, perfils i comparació de perímetres.
  Fonts executables regenerades amb el worker fixat.46computacions al projecte.

## Fonts històriques i terminologia

- Farnós Marsal, Jeroni(2025), «La indústria petroquímica de Tarragona.
  Situació i transformacions», Catalan Social Sciences Review15:107–110,
  ISSN2014-6035. PDF IEC i metadades Dialnet10274197 concordants:
  https://publicacions.iec.cat/repository/pdf/00000528/00000061.pdf.
  Referència `farnos2025petroquimica`, biblioteca total52entrades. Només
  s'utilitzen les descripcions d'àmbits i connexions, no afirmacions absolutes
  de seguretat ni eslògans empresarials del text.
- Jordi Rosell, Enciclopèdia.cat: Dow/IQA1967, BASF1969, importació inicial
  d'etilè via port i integració productiva. Text consultat:
  https://www.enciclopedia.cat/tecnics-i-tecnologia-en-el-desenvolupament-de-la-catalunya-contemporania/el-complex-petroquimic-de.
- Repsol, «La nostra història»: construcció1973, activitat1976; es distingeix
  la cronologia de la refineria de la implantació del conjunt:
  https://tarragona.repsol.es/ca/sobre-complejo/nuestra-historia/index.cshtml.
- Museu del Port/Visitmuseum: transformació dels tràfics i infraestructures
  a partir dels anys1960:
  https://visitmuseum.gencat.cat/ca/museu/museu-del-port-de-tarragona/objecte/la-petroquimica.
- AEQT, apartat de sinergies: rack compartit Dixquímics que connecta empreses
  entre elles i amb el port: https://www.aeqtonline.com/qui-som/#sinergies.

El manual identifica el complex petroquímic de Tarragona com un conjunt
distribuït entre Nord, Sud i port. El sector docent és al Sud; no s'etiqueta
com a refineria nord ni com tota l'extensió del complex.

## Lliurament i revisió final

- ZIP `tmp/dades-docents/practica-visibilitat-costa-20261002-r2.zip`:
  149.293.723bytes,231fitxers, SHA-256
  `afbce1dfcf05f300bb39e442c79a18da08bbcbe003765fa4ba5bb919bf165501`.
  CRC i SHA de tots els membres comprovats;10projectes,36capes,12captures,
  5SVG,37conques individuals, geometries alternatives i controls.
- GUIA19p,6.762.712bytes, SHA
  `fd493cd0bb972e4e4286fa723f46856fa89b27c6c0772653d43097aaa7303a2b`.
- SOLUCIONS3p,48.517bytes, SHA
  `a668b84074700fd90f98c4bc44df827ae46bdac9f09c034781a2a07395639169`.
- Prosa de C3/bibliografia i qualitat de fonts correctes. Site-check abans
  del build. Web C3 a1440/390px:20imatges, cap imatge trencada, error MathJax,
  citació crua, ancoratge perdut ni overflow.19figures numerades al PDF.
- PDF local215p, SHA
  `2ca8078fd7853e785900c486b58eee983c6af38ce59ba971b488ae36f296cd13`.
  Còpia servida idèntica; rebut preview SHA
  `dc76b7bdef1764cff64b2e2c7107f8b0be365bfcf0cd95ae1e70c4b54f7af8a5`.
  Límits correctes; revisats context històric, accessos, geometria, taules,
  resultats i referència nova. Protegit `{Tarragona}` a la font BibTeX perquè
  el canvi de caixa del format bibliogràfic conservi el nom propi.
- La comprovació final de la bibliografia HTML fallava tot i constar Farnós
  al PDF. Resolt declarant `manual_selected = {false}` a l'entrada. Regenerats
  PDF i web; bibliografia revisada a1440/390px, amb nom, títol, majúscula de
  Tarragona i enllaç IEC correctes. Repetit el control de C3:20imatges, cap
  error ni overflow. PDF vigent i artefactes vàlids segons manual-pdf-status.
  Comprovació directa de `_site`, sense dependre dels filtres de Git:
  cap dada privada, font QMD ni captura rebutjada publicada al preview.
  Evidències locals: `/tmp/opencode/geodisseny-publication-r2.json`,
  `/tmp/opencode/geodisseny-seven-browser.json` i captures de bibliografia
  `geodisseny-area-bibliografia-{1440,390}.png` i `geodisseny-bibliografia-r2-final.png`.
- HTML audit correcte amb avisos coneguts de transparència dels logos,
  limitació d'inspecció dels SVG i pressupost d'imatges. Cap canvi a marques
  ni sortides gestionades per silenciar-los. Dades, intermedis i fonts QMD
  absents del lloc; metrics.yml sense diff.
- Review C3 `visibilitat-perimetre-context-acces-linia-20261002`, revisió22,
  digest `91c24370a6b66609061e34d4af202765bc19df9bd3daca28bdde36d161e51624`.
- Review bibliografia `bibliografia-petroquimica-web-copia-20261002`, revisió24,
  digest `c888c78fa0627ada046d1be8a787f309585a9e3bb382351bd7dc3ea3fe6c170e`.
  Substitueix la passada23 després de la comprovació web/PDF. El digest de
  prosa només cobreix el Markdown de bibliografia; la font BibTeX revisada
  té SHA `b2aeb29aac77448d506e6ed9ffbd7c792ea57ec5bba91217e7add29c765c33a1`.
  Cap troballa nova; no confereixen aprovació humana. Estat final revisió24,
  21reviews,18stale, amb les passades actuals de C3 i bibliografia vigents.

Serve local32768 obert. Canvis sense commit ni publicació. El manual públic
continua a main e7f41e9 amb199pàgines. El paquet costa anterior conserva
el hash a5130ad5…46c1; els lliuraments de Moodle no es versionen a Git.
