# Historial de revisió d'Anàlisi Espacial i Geodisseny

## Estat actual — r.walk, girs i isòcrones, 1 d'octubre de 2026

L'autor ha valorat positivament el capítol anterior i ha demanat completar-lo
amb marxa anisòtropa, aclariment dels girs i mapes temporals entenedors, amb
SVG i captures. Reserva:issuecomment5938679144; mateix checkout i branca.

- Model r.walk amb MDT5m i fricció temporal0/0,5s/m, lambda1 i coeficients
  per defecte. Anada/tornada obertes6,630512/6,483451min; anada tancada17,486062min.
  Control pla5,639455min en tots dos sentits. Dijkstra independent concordant
  en cinc càlculs; rampa100m/+10m comprovada amb GRASS:132/52,002s.
- Isòcrones3/6/12min, barreres separades dels temps superiors a12min.
  Superfície fins a12min:91,9425/55,3875ha; cap truncament al límit del retall.
  Expressions de Calculadora ràster comprovades, amb conservació de NoData.
- Restriccions de gir diferenciades de sentits. Documentació i paràmetres
  públics de QGIS3.44: les eines natives usades no admeten taula de maniobres.
  Esquema fictici a→b prohibit / c→b permès, sense atribuir-ne suport al motor.
- Quatre figures QMD/SVG i sis captures d'unaltracaptura. Correccions a les
  fonts: ticks, punta de fletxa i col·lisió de QML entre ràster i contorns.
  41 computacions vigents; capítol2 amb29imatges dins de28figures.
- Guió ampliat amb blocs E–F; el nucli A–B continua identificat. GUIA38p,
  SOLUCIONS5p. Configuració Pandoc/XeLaTeX pròpia amb el runtime PDF fixat:
  no s'ha identificat plantilla específica de pràctiques a l'API pública0.5.0.
- Paquet nou `tmp/dades-docents/practica-distancies-vilaseca-20261001-ampliada.zip`,
  69.936.621bytes,307fitxers, SHA
  `4c17e38e9d537838818568fea114b05304cf900aa7f7b9cbf6974452d0f164d3`.
  CRC i tots els hashes comprovats. 77capes,15projectes,21captures i4SVGnous.
  QGIS obre els15projectes sense xarxa ni repositori font, amb paquet readonly;
  159fitxers de dades/estils/projectes vinculats als hashes de la verificació.
- Guia PDF SHA `d148d240d693a2b744fac491454de59404abd3f69adaab4752fc5248fe890192`;
  solucions SHA `0c74bad2808d45984c88c562e8573591d0323838fbbe44a82d7fadd6e71c6a2e`.
  Límits de text i pàgines de les noves figures revisats.
- Prosa i qualitat de fonts sense incidències ni avisos. site-check abans del
  build. PDF complet201pàgines; corregits dos desbordaments de noms de camps
  i fitxers mitjançant llistes. Límit de text correcte; captures, esquemes,
  mapes i taules nous inspeccionats. Web C2 a1440/390px sense incidències.
- Manual PDF SHA `8bf5d29bf6d51c7422450ce2f0b14220d70cc77018a37833f48c1db60a477646`,
  idèntic a `_site`; rebut preview
  `a5f05c6c18ebade6a787494e41bb3668d7946f1a87dc2b7ecaebdd1589a32b05`.
  HTML audit correcte amb l'avís conegut del demo Plotly. Serve32768 verificat
  després d'esperar l'arrencada de Jekyll; no s'han duplicat contenidors.
- Review `rwalk-isocrones-girs-linia-20261001`, revisió19, digest
  `e5fe151988a67122c0637afb5f902a8630276e6b1db342db884e3b2e51819995`.
  Cap troballa nova; no equival a aprovació humana ni resol registres històrics.
- Paquet inicial i originals RTT/ICAEN/ICGC amb hashes previs. metrics.yml sense
  diff, dades privades i fonts executables fora de `_site`. No s'ha llegit ni
  modificat codi dels proveïdors. Fonts noves en draft, sense commit ni publicació.

## Historial — pràctica de distàncies a Vila-seca, 1 d'octubre de 2026

Prioritat de l'autor: pràctica de la setmana vinent, amb dades locals, guió
autònom i captures QGIS anotades. Mateix checkout i branca. Reserves exactes:
issuecomments5927286154,5928010284 i5928607930 de la incidència1.

### Lliurament privat

- `tmp/dades-docents/practica-distancies-vilaseca-20261001.zip`:
  56.236.454 bytes, 168 fitxers, SHA-256
  `0a7ac7c331212ada3d1a0f2d2f728cb9c0513d4ca6e9ff6bedc87471f72bf2d5`.
- 48 capes amb estils, 10 projectes relatius, 15 captures QGIS amb SVG i
  manifest, fonts, resultats i controls. GUIA de 24 pàgines horitzontals i
  SOLUCIONS de 4 pàgines verticals, fonts Markdown conservades.
- CRC i SHA de cada membre correctes; GeoPackage autònoms i integritat SQLite
  comprovada. QGIS obre tots els projectes sense xarxa, amb el paquet readonly
  a `/paquet` i sense muntar el repositori original. Controls numèrics passats.
- Guions compilats amb Pandoc/XeLaTeX del runtime PDF fixat; marges comprovats
  i pàgines seleccionades inspeccionades. `prose-check` no admet targets de
  `context/`: revisió manual dels guions, sense atribuir-los un resultat automàtic.
- Fonts i preparació a `context/dades/preparar_distancies.py`; controls i
  reproducció documentats a `context/dades/practiques-territorials.md`.

### Contingut i captures

- Nucli A–B: euclidiana vectorial/ràster amb els mateixos O/D, EPSG:25831,
  cel·la de 5 m. Controls 368,323349 / 370,742493 m; diferència entre coordenades
  originals i centres de cel·la explicada i comprovada.
- Cas P2 del Camí del Mas de la Plana: xarxa oberta 454,104650 m, a 5 km/h
  5,449256 min. Tancada sense ruta, preservat com a resultat del graf seleccionat.
  No s'han inventat connexions ni presentat el tancament com una obra real.
- Àrees de servei de 3/6/12 min amb el paràmetre en hores; costos ràster
  470,624458 / 2217,680733 m ponderats. Longitud i cost es distingeixen.
- Friccions 1/4, barreres NoData i corredors declarats; l'MDT queda fora del
  model principal. Pineda conserva el model 1/20 i mostra fricció i cost acumulat.
- 15 captures fetes amb unaltracaptura, 5 receptes i bundles complets.
  Detalls de selectors, noms de capes i enquadrament a `context/qgis-captures.md`.
- Capítol 2 ampliat dins del fil conceptual; 19 figures, dades recuperades
  a les activitats. Corregits dos desbordaments del primer PDF passant les
  coordenades a una taula i els noms de xarxa a una llista.

### Verificació final

- Preflight: mateix checkout, cap conflicte ni sessió aliena; dirty-checkout
  del treball en curs. site-context actualitzat, perfil unaltremanual/ca,
  versió0.5.0 current_customized, cap actualització prevista. Doctor sense errors.
- Prosa del capítol i qualitat de fonts sense incidències ni avisos. site-check
  executat abans del PDF i el build; tots correctes. 37 computacions vigents.
- Chrome: capítol 2 a 1440/390 px, 19 imatges, dues taules dins d'Activitats;
  cap imatge trencada, citació crua, error MathJax, ancoratge perdut ni overflow.
- PDF actual de 191 pàgines, autor Benito Zaragozí. Inspeccionades les 15
  captures noves i les activitats; 19 captions localitzades. Límits de text
  correctes i estat del proveïdor fresh/artifacts_valid true.
- PDF SHA-256 `34e7e0cfc68e948bc2cda0beb2a286f0999e669fcedd969ea2fe181962612a0a`,
  idèntic a la còpia de preview i a `_site`. Rebut de preview SHA-256
  `d089bc47a38b62d5bcc449c2e447caf86c75d29026825d2daa46a5f49992d61f`.
- HTML audit correcte, únic avís conegut UW-IMAGE-COVERAGE del demo Plotly.
  Cap GPKG/GML/GeoJSON/ZIP/TIFF/QMD al lloc generat. Originals RTT, ICAEN i
  divisions ICGC amb els hashes inicials; `_data/metrics.yml` sense diff.
- Review de línia `distancies-vilaseca-linia-20261001`, revisió18, digest
  `1c67e191f26b10def25369d47514f48e9c5a32899361a3193c0051ebbe5c5d74`.
  Cap troballa nova; registre vigent, sense aprovació de contingut ni resolució
  implícita de troballes històriques d'altres passades.
- Serve propi obert al port32768. Capítol:
  http://localhost:32768/geodisseny/ca/chapters/xarxes-accessibilitat/.
  PDF: http://localhost:32768/geodisseny/assets/pdf/manual-ca.pdf.
  Contingut draft per a revisió de l'autor; sense commit, push, càrrega a Moodle
  ni publicació latest. No s'ha llegit ni modificat codi dels proveïdors.

## Historial — estadística des de zero i exemples il·lustrats, 1 d'octubre de 2026

L'autor ha indicat que l'ampliació anterior pressuposava massa estadística.
Es refà la progressió per a estudiants dels primers cursos, amb situacions
concretes abans dels noms i les fórmules, captions llegibles i callouts de lectura.
La petició de figures per als dos exemples de Steinitz continua dins de la passada.
Reserves:issuecomments5921082380 i5921186692, al mateix checkout i branca.

- Inferència amb la comprovació d'una cinta mètrica sobre20m: cada error té
  signe i unitat explicats; es conserven les16dades, mitjana2,5cm i model de
  dispersió4cm. Regla i observació en un sol gràfic; errors I/II amb graelles
  de100proves i freqüències esperades arrodonides5/15, no resultats de camp.
- Covariància amb distància al centre i temps de bus, en km i minuts:
  covariàncies±22,5km·min i correlacions±0,9. La versió unitària anterior
  s'ha substituït per un cas amb magnituds interpretables.
- MAUP amb100habitants per cel·la, percentatge65+ i viatges diaris en bus
  per100habitants; mateixes dades numèriques i agregacions controlades.
- Les activitats incorporen de nou les taules d'estacions, agregació urbana,
  mitjanes d'habitatges i errors de cinta. No depenen de figures llunyanes.
- Dues figures noves de sis vinyetes per a hort solar i abocador, amb
  geometries fictícies coherents, processos, criteris, alternatives i retorns.

Render i revisió local completats; el text queda en draft per a nova lectura
de l'autor. La passada anterior de173pàgines es conserva com a historial.

### Comprovacions d'aquesta revisió

- 37fonts de computació vigents. Recalculats els exemples de covariància,
  contrast, errors, normal, intervals, MAUP i els dos casos de Steinitz.
  Controls numèrics dins de les fonts; fig.1.11 en un sol panell i fig.1.12
  amb100quadrats per situació. La simplificació gràfica conserva els supòsits.
- Qualitat de fonts sense incidències ni avisos de dimensions; site-check
  abans de la preparació del PDF i del build, tots dos correctes.
- Prosa sense incidències. L'únic avís és «I i» al títol «Errors de tipus I i II»:
  nombre romà i conjunció, no una paraula duplicada. Es conserva amb aquest motiu.
- Chrome:capítol1 a1440/390px,15figures carregades, cap error MathJax,
  enllaç intern sense destinació ni desbordament. Comprovades les quatre taules
  de dades dins d'Activitats. HTML audit amb l'avís conegut del demo Plotly.
- PDF de179pàgines, metadades d'autoria Benito Zaragozí, vigent segons el proveïdor.
  Revisades les15figures del capítol, el cas de camp i les taules de les activitats.
  Corregida una etiqueta que interrompia la campana de la figura1.11.
  Comprovació dels límits de text sense incidències.
- PDF SHA-256:a37bede16bdfd0ca99940a81de4c908ec1b2b7e3803e3aa8f041e2e7c20b48dd.
  La còpia servida a _site té el mateix hash.
  Rebut de preview SHA-256:224f4791f3d5295de2f64f5ed2b7fe446583f39ebf51acd56cc668c4fff40292.
- Passada de línia fonaments-estadistica-des-de-zero-20261001, revisió17,
  digest1bf793b628c550b4b8731208c04f77b2335c58175a1951178ed5cfdf8f53747c.
  Cap troballa nova registrada; la revisió d'agent no acredita comprensió de
  l'alumnat ni substitueix la revisió i aprovació de l'autor.
- Serve propi obert al port32768. metrics.yml sense diff; sense commit,
  push ni publicació latest. Dades de camp fictícies declarades com a tals.

## Historial — ampliació dels fonaments, 1 d'octubre de 2026

Ampliat el capítol 1 segons la petició de l'autor. Reserva exacta:
https://github.com/geourv/geodisseny/issues/1#issuecomment-5920127562.
Fonts en draft, amb refs i ancoratges anteriors conservats.

- Boxplot amb punts originals, quartils i tanques; variància i desviació amb
  separacions, quadrats i retorn a la unitat original; covariància amb quadrants
  i productes signats. Divisors n i n−1 i convenció de quantils explícits.
- Relleu i gràfic tèrmic comparteixen escala vertical. La temperatura continua
  sent la resposta de la regressió; els residus es dibuixen horitzontalment.
  Gradient adiabàtic i comparació d'estacions es mantenen diferenciats.
- MAUP:16cel·les, r=0; quatre franges horitzontals r=+1 i verticals r=−1.
  Mitjanes globals22/40 conservades. Fal·làcia ecològica:18habitatges ficticis,
  pendent negatiu dins de cada zona i positiu entre les tres mitjanes zonals.
- Inferència amb un únic model docent d'errors normals independents:
  σ coneguda4cm, n=16, SE=1cm. Mostra explícita de mitjana2,5cm;
  IC95% aproximat[0,54;4,46]cm, p bilateral0,01241933.
  Quaranta mostres simulades, seed20260930:37intervals cobreixen µ=0.
  Alternativa µ=3cm:β≈0,149 i potència≈0,851 amb α=0,05.
  Explicats cobertura freqüentista, t de Student i límits amb dependència espacial.
- «Precedents del geodisseny»:Geddes, McHarg, Tomlin i Goodchild.
  Quatre referències afegides (també Robinson per fal·làcia ecològica), amb
  metadades contrastades a Internet Archive/Open Library, Crossref i la revista.
  No s'ha completat amb conjectures el publisher de Geddes ni el rang de pàgines
  que Crossref no proporcionava per Robinson. Bibliografia total:51entrades.
- Steinitz amb puntes de fletxa explícites al SVG manual; dos exemples narrats,
  hort solar i abocador, amb referència, processos, alternatives i retorns.
- Terminologia anglesa selectiva i activitats sobre boxplot, agregació i inferència.
  Criteris incorporats a writing-profile.md.

Vuit figures computades noves i tres de revisades:35fonts executables en total;
el primer capítol referencia13imatges. Fonts renderitzades i inspeccionades amb Qt;
corregits solapaments en covariància, regressió i gradient. Comprovació de qualitat
de fonts sense incidències ni avisos de dimensions. El PDF anterior de155pàgines
queda substituït, a la previsualització local, pel nou de173pàgines.

Prosa:cap incidència; tres avisos mecànics de paraula repetida corresponen a
«tipus I i II» o «tipus I i un de tipus II». Es conserven perquè I és el nombre
romà del tipus d'error i i és la conjunció catalana: no hi ha cap duplicació.
site-check correcte abans de generar els artefactes nous.

### Verificació de la passada de fonaments

- site-check, build i HTML audit correctes. L'audit conserva l'avís conegut
  UW-IMAGE-COVERAGE del demo Plotly de la plantilla.
- Chrome:presentació i set capítols a1440/390px,57imatges referenciades;
  cap imatge trencada, error MathJax, citació crua ni desbordament del document.
- PDF de173pàgines, autor Benito Zaragozí. Revisades totes13figures del capítol1,
  els precedents, els dos exemples de Steinitz i les activitats noves.
  Text i figures dins dels límits comprovats, amb les puntes de fletxa correctes.
  manual-pdf-status:artifacts_valid i fresh true.
- PDF SHA-256:7dfd50118bc95454cb32f6bdb817d4ce09773dfbcd7b6861c5195f9718748e37.
  Rebut de preview SHA-256:6cc25307dd559e0acc0ed3e73df2156630afe198415252ec63cbe96da084d253.
- Passada de línia fonaments-estadistica-geodisseny-20261001, revisió16,
  digest d9df71decdbd0e8afe0d6311209491908c6eeaac9731a470a2c13abf4740692b.
  Cap troballa nova; no equival a aprovació humana ni resol registres històrics.
- context/, tmp/, sandbox/ i assets/quarto/ absents del lloc generat;
  metrics.yml sense diff. No s'han modificat dades territorials ni paquets privats.
- Operacions unaltraweb amb la CLI pública0.5.0 perquè el MCP està desconnectat;
  cap lectura ni canvi al codi dels proveïdors. Fonts de computació renderitzades
  pel proveïdor i SVG de Steinitz editat com a figura d'autoria del consumidor.
- Serve propi actiu:http://localhost:32768/geodisseny/ca/chapters/fonaments-geodisseny/.
  PDF:http://localhost:32768/geodisseny/assets/pdf/manual-ca.pdf.
  Contingut draft per a revisió de l'autor; sense commit ni desplegament latest.

## Historial — context geogràfic del capítol 0 i portada, 30 de setembre de 2026

Reescrit el capítol 0 després de la nova precisió de l'autor. El text desenvolupa
la continuïtat de TIGIT i TIG dins del grau, l'ús transversal de SIG, R i Python
i l'aportació dels fonaments geogràfics i estadístics. Relaciona coneixement del
paisatge, activitats, relleu i aigua amb preguntes, diagnosi i propostes territorials.
El territori proper connecta la part tècnica amb altres aprenentatges del grau;
la invitació final anima a explorar fonts, problemes i aplicacions diferents.
S'han retirat les subdivisions tècniques i la taula administrativa de l'obertura.
La perspectiva geogràfica es descriu sense jerarquitzar disciplines ni professions.

Portada configurada amb les mateixes entrades que TIG/TIGIT, sota
unaltraweb.manual.pdf.cover:

- series_logo: assets/img/brand/docs-quarts-logo-small-white.png.
  SHA-256 31facc4e29b8e3090770967e77442491899639990937fbc5236425cdc4c7136b.
- institution_logo: assets/img/brand/dgeo-apilat-color.pdf.
  SHA-256 77db013a3446bb5eba1a8a6ba47908930991d19ac53217d3f51443671ff96a20.

Els originals de TIG i TIGIT són idèntics. Les còpies locals conserven els bytes,
la transparència i els colors originals. Revisades la portada PNG i la pàgina1
del PDF: marca de la sèrie a la franja superior i URV/Departament de Geografia
a la part inferior. Cap canvi al proveïdor.

Controls: prosa del capítol0 sense incidències ni avisos, site-check i build
correctes, HTML audit correcte amb l'avís conegut del demo Plotly. Revisat el web
a1440/390px sense imatges trencades ni overflow, i les pàgines19–20 del PDF.
Comprovació de límits de text correcta. PDF vigent de155pàgines, SHA-256
13a81831857a5b4d0bb47058e9b0b3a04405ae93de7ded1389c38bdc322e9a2c.
Rebut de preview: 0d5517ee8dd3a6da649052897d77d12c96f453a71a3b63590a92c0a5b00854b7.

Passada de línia presentacio-context-geografic-20260930, revisió15,
digest faeeeaca2ac1ba9a213d562d5abc87bf5b032691f43b8fa4ac260ac9a3af57a8.
Cap troballa nova; no equival a aprovació humana. Serve propi obert al port32768,
contingut draft, sense commit ni publicació latest.

## Historial — estil de la introducció, 30 de setembre de 2026

Revisades la presentació general i el primer capítol a petició de l'autor.
L'àrea de treball es presenta en continuïtat amb TIG: Camp de Tarragona i
Tarragonès com a territori proper per entendre i contrastar els mètodes,
amb pràctiques que poden variar i fonaments aplicables a altres llocs i fonts.

- Retirats el cas conductor fix, la comarca assignada, el pòster obligatori
  i les activitats d'organització del curs de la presentació general.
- Simplificats obertura, transicions, passatges abstractes i enunciats del
  primer capítol. Es conserven fórmules, valors, cites, figures i ancoratges.
- Títol introductori del PDF: «Presentació», configurat a _config.yml.
- Criteris recollits a writing-profile.md i manual-fotovoltaic.md.
- Prosa dels dos textos sense incidències ni avisos; site-check i build correctes.
- Revisió en Chrome de presentació i primer capítol a 1440 i 390 px: sense
  errors MathJax, imatges trencades ni desbordaments. HTML audit correcte,
  amb l'avís conegut sobre el demo Plotly de la plantilla.
- PDF actual de 159 pàgines, vigent; revisades obertura, àrea de treball i
  activitats. Comprovació de límits de text correcta.
  SHA-256: fc58f8056c6b6c1d6d22654c38ba1ff4dd862f3f22518517087231d31f96a9fb.
  Rebut: df8b1bd72136356cac43f19830aec2ee43150f846240645d26236646fe2faa79.
- Registre editorial a revisió 14, amb dues passades de línia vigents:
  presentacio-area-propera-20260930-final, digest
  bcee42d59611c9ea0becf338c30348b7526689a2e8827f8414258cf6cb83442a;
  fonaments-estil-area-propera-20260930, digest
  4c8337693de3516de598086ce3171c483644ec6e4f902ec984627d34972051f0.
  Cap troballa nova en aquestes passades; no són aprovació humana.
- Serve obert al port 32768. Contingut draft, sense commit ni desplegament.

## Historial — progressió pedagògica i QGIS, 30 de setembre de 2026

Fonts dels set capítols revisades, en draft. Es mantenen autoria de Benito
Zaragozí i els refs/permalinks. Sense commit, push ni publicació latest.
Verificació web/PDF completada: 161 pàgines i 49 imatges referenciades.
El recompte de 143 pàgines de la secció històrica següent correspon a la versió anterior.

- Vocabulari i símbols introduïts gradualment, callouts variats, exemples i
  eines integrats. Retirada de la secció inconnexa del Francolí i de Moran
  dels residus a la primera figura de regressió.
- Distàncies: relleu i perfil 596,6 m; alternativa inferior de xarxa 1.400 m;
  tres escenaris de costos 4/5/6 min. Pineda amb ortofoto 2025.
- Visibilitat: etiquetes O1–O6, mapa i matriu amb pantalles opaques,
  28 mostres petroquímiques i dos mapes en files. Mateix domini d'1.570.262 cel·les.
- Centres, dispersió, graella i KDE sobre 3.762 punts; Columbus, 49 barris, abans
  del cas censal; Moran i Gi* diferenciats de KDE/agrupació exploratòria.
- XEMA: 182 estacions del 2025-08-15, 48 intervals V/SH per estació. Metadades
  confirmen dia TU i etiqueta inicial. IDW p=2, semivariograma 12 classes/150 km,
  kriging lineal amb a=2,79123 i b=19,5643. Sense validació fora de mostra.
- Steinitz solar: nou SVG manual amb sis models i tres iteracions, relacionat
  amb la narració del capítol 1. Bibliografia de 47 entrades, Anselin (1988) verificat
  amb Crossref, DOI 10.1007/978-94-015-7799-1.
- 27 computacions vigents. 16 captures noves en quatre receptes MCP, més el
  detall viari repetit amb zoom menys tancat. Revisades imatges i valors.
  Corregida la superposició accidental de Moran damunt del mapa Gi*.
- SDEllipse retirat de l'arrencada després d'un error modal per resources
  absent al ZIP de fonts. S'utilitzen expressions natives. Complements fixats:
  Hotspot Analysis v4.0.0 i SAGA NextGen 1.3.0; cache 139383569f94, hashes conservats.
- Paquet privat nou: tmp/dades-docents/demos-ampliacio-20260930.zip,
  34.195.177 bytes, 94 fitxers, SHA-256
  7f387cabca8dee8432a66ea287e5fed75da8191137dc875684ddaffc876eacc5.
  CRC/hashes i integritat SQLite comprovats; no s'ha pujat a Moodle.

Controls de fonts i editorials correctes; no hi ha placeholders ni metatext
editorial al contingut. La primera revisió PDF va detectar anotacions SVG
petites i requadres desplaçats en captures retallades. Les 14 referències amb
callouts utilitzen ara les sortides PNG anotades del mateix MCP, que preserven
l'alineació amb els controls; els SVG es conserven al bundle. No s'han editat
generats ni codi dels proveïdors. La qualitat de fonts queda sense avisos de
dimensions, però les fonts rasteritzades de QGIS requereixen revisió visual.
Una indicació informativa de 43 paraules al resum dels capítols s'ha mantingut:
és una enumeració paral·lela amb referents clars, no una errada de prosa.

Revisió de línia final: pedagogia-qgis-linia-20260930-final, revisió 11,
digest 7fd4cfe59181185367a864b7bf9b7189803710cef377cbc476ec3b29b64de8d1,
cap troballa nova en aquella passada. La revisió 10 es conserva com a historial.
No equival a aprovació humana i no resol automàticament els registres històrics
acceptats de pràctiques.

### Verificació final del render

- `site-check` abans del build; qualitat de fonts sense incidències ni avisos
  de dimensions. Prosa correcta, amb l'únic consell informatiu descrit.
- Chrome: set capítols a 1440 i 390 px, 49 imatges carregades, zero errors
  MathJax, cites sense resoldre, imatges trencades o desbordaments del document.
- PDF de 161 pàgines, autor Benito Zaragozí, vigent segons manual-pdf-status.
  SHA-256 `3ef819bddaec054e4c6ce5a8981a18f1ea04d8bc737ad52fcf6bb8a2f58cc273`.
  Rebut de preview: `b4e470fc1785bb645413b58c0853f340e97d12b46a047efdccb0c76b558fcf8c`.
- Revisades pàgines de figures, captures, matrius i Steinitz. Corregits tres
  desbordaments d'identificadors llargs i compactada la taula del perfil O–D.
  La comprovació de caixes de paraules no troba sortides del límit comprovat
  al cos; la línia de crèdit de coberta té una composició a marge pròpia.
- `html-audit` correcte; avís conegut UW-IMAGE-COVERAGE al demo Plotly de la
  plantilla. La inspecció de les figures del manual s'ha completat en navegador.
- Cap context/, sandbox/, tmp/ o assets/quarto/ al lloc generat. Originals
  ICAEN/ICGC amb els SHA inicials i cap taula alterada; metrics.yml sense diff.
- El MCP unaltraweb va perdre connexió durant un render llarg. S'ha acabat
  amb la CLI pública de la mateixa distribució 0.5.0, sense llegir ni modificar
  codi del proveïdor. QGIS s'ha renderitzat amb el seu MCP.
- Serve propi actiu: http://localhost:32768/geodisseny/ca/ i PDF a
  http://localhost:32768/geodisseny/assets/pdf/manual-ca.pdf.

## Historial — casos territorials i revisió final del 29 de setembre de 2026

Passada completada per a revisió humana. Set capítols en `draft`; autoria visible
i metadades PDF de Benito Zaragozí, amb retirada temporal de Yolanda Pérez.
No hi ha commit, push ni desplegament de `latest`.

### Contingut i figures afegits

- McHarg i *Design with Nature*; SVG propi del marc de Steinitz, amb sis models,
  tres iteracions avall/amunt/avall, participació i retorns. Revisats web i PDF.
- Pearson, coeficients de regressió, gradient adiabàtic, Manhattan, recta 3D i
  recorregut sobre terreny; figures executables amb controls numèrics.
- Visibilitat acumulada des de sis observadors d'una carretera simulada,
  calculada sobre relleu explícit, amb valors diversos a la graella.
- Casos reals: xarxa RTT ICGC Vila-seca–Tarragona, solar cadastral de la Pineda,
  sector de la refineria nord sobre Tarragonès i Baix Camp, i seccions censals
  amb potència registrada i antiguitat cadastral. Supòsits i dades diferenciats.
- Captures QGIS reals en dos grups de subfigures: accés/configuració i resultat
  per a centres ICAEN i ruta ICGC. Fonts, dades privades, PNG, SVG i manifests.
- Diagrama d'hort solar; propostes d'escoles, abocadors, centres penitenciaris
  i hotels rurals; lectures comentades de Uyan, Kontos et al. i Başeğmez et al.
- 22 fonts Quarto/Python executades i vigents; quatre diagrames referenciats,
  un SVG d'autoria manual i quatre captures: 31 imatges dins de 29 figures.
  El bundle Mermaid antic de Steinitz es conserva sense referència visible.
- Bibliografia de 46 entrades. Els mapes censals conserven inputs agregats
  a `context/inputs/`, fora del web. `assets/quarto/` també queda exclòs de Jekyll.

### Dades i controls

La documentació operativa és `context/dades/practiques-territorials.md`.
Dos paquets locals nous, verificats per CRC, SHA-256 de cada membre i integritat
SQLite; les còpies de lliurament de GeoPackage són autònomes, sense dependència WAL:

- `tmp/dades-docents/demos-practiques-territorials-20260929.zip`, 38.980.140 bytes,
  SHA-256 `0fbe2c1a5a2c859eb72cb80ea04f44fb0625d698b102887f9873c1dfaa5e35d9`.
- `tmp/dades-docents/demos-seccions-autoconsum-20260929.zip`, 48.306.598 bytes,
  SHA-256 `33d6cd4d75104d5e647d502a5f46add13d5cf7b73743cd3786d08fc4ff4d3d9a`.

No s'han carregat a Moodle ni s'han incorporat al web. Les extraccions incompletes
o amb correspondències municipals exploratòries incorrectes no entren als paquets.

Controls principals:

- Centres ICAEN sobre els mateixos 3.762 registres coneguts, 36.633 kW;
  desplaçament ponderat/no ponderat de 2.902,715 m, contrast QGIS–numpy.
- Ruta original de prova: 10.989,257 m; canvi de sentit local: 11.012,834 m;
  velocitat local penalitzada: mateix desviament, 0,367094464 hores assumides.
  No s'han executat penalitzacions de gir, que el motor natiu no admet.
- Solar de 8,71 ha: 608,284 m travessant-lo, 724,264 m vorejant-lo amb fricció 20.
  Metres ponderats, no temps real. Només canvia la fricció interior.
- Visibilitat MDT: 1.577.539 cel·les comunes de 25 m. Fonts amb 1.791 cel·les
  terrestres sense elevació; se n'exclouen 49.049 més potencialment afectades
  per línies de visió amb aquests buits. Altures de 30/60 i 1,7/15 m assumides.
  MDS preparat com a entrada de contrast; no es declara una comparació controlada
  amb receptors reals d'edificis ni altures de torres verificades.
- Seccions: 151 geometries completes al GPKG; Moran sobre 150, I=0,14404677,
  pseudo-p=0,0024; una HH després del procediment BH-FDR declarat. Regressió
  ecològica en 126 seccions, r=−0,40095367, R²=0,16076385; residus autocorrelacionats.
- QGIS va canviar capçaleres SQLite en una prova amb entrades en escriptura.
  Es va verificar que totes les taules i l'esquema eren idèntics i restaurar
  els bytes exactes ICAEN/ICGC dels ZIP originals comprovats. Preparacions
  posteriors amb fonts muntades de només lectura; originals amb SHA inicial.

### Verificació del resultat renderitzat

- `site_check`, `prose_check` i qualitat de fonts correctes. Sense avisos de
  dimensions de figures. Computacions vigents i rebut diavisuals actualitzat.
- `make build` complet, amb previsualització PDF gestionada pel rebut del nucli.
  PDF actual: **143 pàgines**, autor Benito Zaragozí, SHA-256
  `5cd9522eb43b487885230304f790c6e7da78563edb89876ef7d4e376bdbb3230`.
- Rebut `.cache/unaltraweb/manual-pdf-preview.json`, SHA-256
  `3a13326438c29a3d4d114ba5f81cdb8380fbe40aa0de9f2bf2e7390160f9f823`.
- Chrome sobre set capítols a 1440 i 390 px: 31 imatges carregades, zero errors
  MathJax, cites Liquid, imatges trencades i desbordaments del document.
  Primera comprovació durant la regeneració va coincidir amb fitxers encara
  en publicació local; la comprovació final amb el serve estable és correcta.
- Revisades coberta, Steinitz, figures noves, subfigures i pàgines representatives
  del PDF. Ampliades les captures de resultat i ajustat el diagrama de l'hort solar.
- `html_audit`: 14 HTML, zero troballes; continua l'avís conegut `UW-IMAGE-COVERAGE`
  sobre l'HTML Plotly del paquet. No s'ha modificat el nucli per eludir-lo.
- Comprovació d'exclusions: cap QMD, Python, GPKG, GML, GeoJSON, ZIP o TIFF a `_site`.
  Les figures SVG/PNG són els assets visibles, no les dades dels paquets.
- Persisteixen els avisos d'inspecció estàtica de SVG generats i la transparència
  dels logotips originals. Figures revisades renderitzades; les mostres de canvas
  de Chrome tenen alpha mínim 251–255 per rasterització, sense grans àrees transparents.
- Serve obert: `http://localhost:32768/geodisseny/ca/` i
  `http://localhost:32768/geodisseny/assets/pdf/manual-ca.pdf`.

Registre editorial a revisió **9**: passada de línia
`casos-territorials-linia-20260929`, digest
`dd887209504206ad0886137cc9542dfb5149a23de584a2c82df41225ae8abffb`, sense
troballes noves i sense aprovació humana. S'ha actualitzat el motiu de
`practiques-no-autonomes`, que continua acceptada i oberta per a les ampliacions
generals de temperatures observades, MDS amb receptors reals i altres activitats.

## Passada pedagògica anterior — 29 de setembre de 2026

L'autor ha demanat ampliar tots set capítols i fer-los comprensibles per a grau
de Geografia: els esquemes i les cauteles tècniques anteriors no oferien prou
exemples ni explicació gradual. Aquesta secció substitueix les xifres i l'estat
de la revisió inicial conservada més avall. El contingut continua en `draft` i
la publicació `latest` resta ajornada per indicació expressa de l'autor.

### Desenvolupament i recursos

- Set capítols amb títols generals, refs i URLs conservades. S'han desenvolupat
  definicions, contextos geogràfics, notació, unitats, operacions intermèdies,
  interpretacions i preguntes amb respostes de control.
- Capítol 1: les potències són ara explícitament fictícies; mitjana, mediana,
  variància, ponderació poblacional, covariància, regressió, residu i validació
  tenen exemples resolts. Afegides definicions i callouts. La taula d'estacions
  permet fer l'activitat sense esperar dades externes.
- Capítol 2: nova comparació de recta, xarxa completa amb nodes/arcs i graella
  de fricció; detall de cruïlla connectada i pas a diferent nivell. Càlcul manual
  de ruta de 4 minuts i reconstrucció del cost ràster de 1.550 unitats.
- Capítol 3: perfil amb cotes i altures, taules de control, matriu receptor–objectiu
  amb visible/ocult/no calculat i exemples sobre denominadors i mostreig.
- Capítol 4: productes de ponderació, centres, covariància i autovalors de l'exemple,
  comparació gràfica ponderada/no ponderada i dos kernels amb escala comuna.
- Capítol 5: dos patrons concrets, matriu W completa, retards i productes per
  reconstruir Moran, i enumeració de les sis disposicions possibles amb contrast
  unilateral exacte de 1/3. Separades configuració i significació local.
- Capítol 6: IDW resolt, suport temporal, càlcul experimental de semivariàncies,
  model teòric identificat com a il·lustratiu, kriging ordinari residual executat
  sobre camp sintètic i comparació de prediccions i errors ficticis.
- Capítol 7: tres estats de coneixement, funció de pendent calculable, matriu AHP
  coherent 6:3:1, contribucions de la suma i llindar de canvi d'ordre 17/70.
- Afegit *OpenIntro Statistics*, 4a edició de Diez, Çetinkaya-Rundel i Barr, 2019;
  verificades autoria a Leanpub i data/edició al web d'OpenIntro. La bibliografia
  té 39 entrades. Els exemples, les explicacions catalanes i les figures són propis.

Hi ha 14 fonts Quarto/Python amb SVG gestionats per unaltraweb: les sis anteriors
revisades quan corresponia i vuit de noves. Totes han estat executades al worker
fixat per digest i estan vigents. Els scripts comproven magnituds com mitjana,
covariància, rutes, Moran, parells de variograma i suma dels pesos de kriging.
Amb els quatre diagrames i les dues captures QGIS, els capítols contenen 20 figures.

Les captures reals de QGIS 3.44.11 mostren configuració de ruta i de coordenades
mitjanes amb entrades sintètiques pròpies. Es conserven PNG, SVG amb captura
original incrustada, receptes, prompts i manifests. La imatge QGIS està fixada
per ID immutable a `.unaltracaptura-qgis.yml`; el pla de continuació i els límits
són a `context/qgis-captures.md`. Són captures de configuració, no una execució
completa de totes les pràctiques territorials.

### Comprovació de la versió actual

- `site_context`: paquet 0.5.0 vigent, sense actualització pendent; `site_doctor`
  correcte. Preflight de la mateixa branca amb canvis locals propis preservats,
  sense conflictes ni una altra sessió cooperativa.
- `prose_check`: sense incidències ni avisos. `site_check`: correcte, amb
  computacions vigents i qualitat de fonts/figures sense avisos de dimensions.
- Corregits dos problemes de renderitzat mòbil: notació de covariàncies que
  interferia amb Markdown i una equació de semivariograma massa ampla.
  Ajustat el layout del kernel perquè els títols no quedin retallats.
- Web: Chrome a 1440 i 390 px, set capítols en ordre, 20 figures carregades,
  zero errors MathJax, zero cites Liquid sense resoldre i zero desbordaments
  del document. Les taules amples es desplacen dins dels seus contenidors.
- Revisió visual dels onze gràfics nous o modificats, captures QGIS i pàgines
  representatives de text, exemples i figures al PDF. No substitueix la revisió humana.
- PDF actual de 114 pàgines, fresc i vàlid. SHA-256:
  `87718decb9c20086c45b62fea18cdcc4375fd5b0b3b270d38f21bbbbed500d36`.
  Rebut de còpies ignorades: `.cache/unaltraweb/manual-pdf-preview.json`, SHA-256
  `9ef179ac4bfdc3def5054a82bb70403a824cc44a535d9d1e31a47a22377db9cb`.
- `html_audit`: 14 pàgines, sense troballes d'HTML/enllaços; persisteix l'avís
  de cobertura d'imatges per `_site/assets/plotly/demo.html` del paquet.
- Opacitat: les dues captures passen el comprovador; els SVG de Matplotlib i
  Mermaid continuen declarats no verificables automàticament pel comprovador
  estricte. S'han revisat renderitzats. Els tres logotips originals transparents
  continuen pendents de decisió humana i no s'han repintat.
- HTTP: inici, capítols i PDF disponibles. Proves negatives de `context/`,
  dades a `tmp/`, configuració oculta QGIS i `sandbox/` retornen el 404 esperat.
- Registre editorial a revisió 7: `pedagogia-set-capitols-linia-20260929`, passada
  de línia amb zero troballes i digest vigent. La troballa històrica sobre receptes
  territorials no autònomes continua acceptada i oberta; no s'ha donat aprovació humana.

La previsualització queda oberta a `http://localhost:32768/geodisseny/ca/` i el PDF
a `http://localhost:32768/geodisseny/assets/pdf/manual-ca.pdf`. Les demos originals
continuen fora del web, a `tmp/dades-docents/`, per a distribució per Moodle.
Falten execucions territorials completes i les captures addicionals que en depenen.
No s'han fet commits, push, PR ni desplegaments.

## Revisió inicial — 28 de setembre de 2026

Les seccions següents documenten la primera passada, anterior a la reorganització
en set capítols, els paquets de dades i la revisió pedagògica del dia 29.

## Abast i coordinació

- Encàrrec: revisar el tercer manual de la sèrie TIGIT → TIG → Geodisseny i afegir un primer capítol de fonaments, amb reordenació i correcció dels errors detectats.
- Reserva de fitxers acceptada per l'autor a la conversa; incidència https://github.com/geourv/geodisseny/issues/1 i branca local `content/1-fonaments-geodisseny`.
- Checkout verificat: `/home/benizar/git/geodisseny`, sense canvis inicials ni altres sessions cooperatives detectades. Preflight del control plane favorable després de crear la branca.
- Perfil `unaltremanual`, català, unaltraweb/MCP 0.5.0 i integració gestionada coherent. No hi ha actualització pendent respecte del paquet MCP actiu.
- Contingut mantingut en `draft`. Aquest informe no acredita revisió ni aprovació humana.

## Referències de la sèrie inspeccionades

S'han consultat els perfils de redacció de TIGIT i TIG i, com a mostres desenvolupades, `tig/_chapters/ca/01-tig-fonts.md` i `tigit/_chapters/ca/04-terra-dades-espacials.md`. També s'ha comprovat l'inventari públic de capítols de tots dos repositoris. Patró adoptat: prosa explicativa, conceptes anteriors al procediment, exemples amb límits, objectius observables i activitats amb evidència conservable. Els capítols inicials de geodisseny eren esquemes breus i no oferien una profunditat equivalent.

## Canvis realitzats

- Nou capítol 1: anàlisi espacial i cartografia; descripció, explicació, predicció i proposta; objectes, camps i xarxes; distància, veïnatge, dependència, escala, suport i incertesa; geodisseny, actors i alternatives; sis preguntes de Steinitz; Camp de Tarragona; exemple multicriteri fictici; entorn, fonts i sis activitats.
- Reanomenats els vuit capítols tècnics com a 2–9 i ajustats els pesos a 20–90. Conservats els `ref` i permalinks existents. Bibliografia final no numerada.
- Presentació vinculada explícitament a TIGIT i TIG. Distingits Camp de Tarragona i Tarragonès, fonts institucionals i col·laboratives, i projecte desat de dades incrustades.
- Condicions categòriques d'avaluació sense font explícita substituïdes per remissió a guia docent i normativa vigents. No s'han verificat en aquesta passada el detall de la guia docent, les ponderacions, el règim de terminis ni les sancions.
- Perfil editorial local adaptat a la sèrie; `context/` exclòs explícitament del lloc; pàgina arrel traduïda al català i marcada com a esborrany.
- Configurats `first_name` i `last_name`, que utilitza la metadada HTML d'autoria, i el títol curt de navegació `Geodisseny`. La fórmula de suma ponderada s'ha fet més compacta, mantenint les condicions dels pesos en la prosa, per eliminar el desbordament de MathJax en mòbil.

## Errors conceptuals corregits

1. **CRS:** no totes les mesures exigeixen reprojecció prèvia; diferenciats càlcul pla, mesura el·lipsoidal, CRS de capa i transformació de visualització.
2. **Xarxes:** corregida la referència a una barrera d'un capítol anterior que encara no s'havia explicat. L'àrea de servei nativa és una sortida de xarxa, no un polígon universalment accessible.
3. **Cost:** una penalització alta no prohibeix el pas. Separats fricció, cost acumulat, longitud i temps. Documentat el seguiment de direccions per reconstruir rutes i l'ús restringit d'«isòcrona».
4. **Marxa:** retirada la cita de Tobler (1970) com a font d'una funció de marxa. La secció explica ara el model anisòtrop documentat de GRASS `r.walk` i no l'atribueix a Tobler ni l'extrapola a bicicletes.
5. **Visibilitat:** retirada l'afirmació que el MDT proporciona sempre una cota superior de l'impacte. Distingides altures absolutes/relatives, no visible/no calculat i exposició/impacte.
6. **Patrons:** KDE cru no equival automàticament a intensitat per hectàrea; la coordenada mitjana no calcula tots els estadístics; una graella hexagonal no és universalment millor; clustering no equival a contrast inferencial.
7. **Autocorrelació:** diferenciats model nul, intercanviabilitat, LISA i Moran local, diagonal de Gi* i comparacions múltiples. Retirada la invalidació automàtica per autocorrelació residual i l'equiparació dels residus d'EMC als predictius.
8. **Interpolació:** corregides les afirmacions «IDW sense model», «sense semivariograma és una caixa negra» i «error conegut a cada cel·la». Diferenciats supòsits de kriging, incertesa condicional, error observat, abast pràctic i disseny de validació.
9. **Multicriteri:** CR < 0,10 no prova validesa social; una unió d'atributs no és obligatòria per aplicar pesos ràster; AND/OR no mesuren risc territorial; variar pesos exigeix renormalitzar; estabilitat no equival a probabilitat; mitjana parcel·lària no anul·la exclusions.

## Fonts contrastades en aquesta passada

- Steinitz, *A Framework for Geodesign* (Esri Press, 2012), ISBN 9781589483330: fitxa editorial i mostra oficial del capítol 1. Verificades les sis preguntes i el caràcter col·laboratiu. El desenvolupament català i els exemples són propis, no traduccions literals.
- Observatori del Paisatge: pàgina del Catàleg del Camp de Tarragona, aprovació de 2010 i distinció respecte del llibre de 2012; unitats, cartografia i documents disponibles.
- QGIS: documentació 3.44 i calendari oficial LTR. La clau bibliogràfica existent s'ha mantingut, amb URL específica de versió.
- GRASS: documentació de `r.walk` i `r.cost` com a fonts tècniques de costos, barreres i reconstrucció de recorreguts.
- Meteocat: portal de serveis i accés de dades obertes; ACA: consulta de dades i geoserveis. No s'han descarregat dades ni provat aquí les consultes analítiques.

## Treball pendent per completar el manual al nivell de la sèrie

La revisió i les correccions no converteixen els capítols 2–9 en pràctiques completes. Continuen necessitant desenvolupament substantiu abans de considerar acabat el manual:

- Fixar el cas amb l'autor: dimensió i servei de les alternatives, horitzó, comarques, restriccions documentades i relació amb les activitats avaluables.
- Seleccionar productes i edicions reals, conservar metadades/llicències, preparar dades de pràctica i establir camps, filtres i resultats de control.
- Desenvolupar teoria, fórmules quan aportin comprensió, exemples treballats, procediments QGIS, comprovacions i interpretacions als capítols 2–9 amb la profunditat de TIG/TIGIT.
- Identificar i executar una recepta completa de GRASS, estadística espacial i geoestadística en un entorn versionat. Especialment oberts LISA/Gi*, K de Ripley, el·lipse direccional i kriging. La documentació consultada no certifica una execució a l'aula.
- Incorporar mapes i figures docents justificats, amb fonts editables i captures de passos que realment necessitin suport visual. Actualment els capítols no inclouen figures de procediment.
- Verificar la bibliografia heretada completa i les cobertes de llibres: aquesta passada ha contrastat les noves fonts centrals i les referències tècniques utilitzades, no totes les metadades històriques ni tots els drets d'imatge.
- Confirmar les condicions docents amb la guia vigent i els enunciats. No s'han inventat percentatges, llindars legals ni opinions locals.
- Revisió humana web/PDF i decisió explícita sobre els tres logotips SVG transparents existents. No s'han modificat ni repintat.

## Verificació

- `site_doctor`, política lingüística i contracte del perfil: correctes, sense conflictes de scaffold ni actualització pendent.
- `prose_check` i diagnòstics editorials de l'últim `site_check`: sense incidències ni avisos de prosa. `manual_source_quality_check`: sense taules nues, components invàlids ni avisos.
- Computacions i captures: no hi ha fonts executables ni sortides declarades; no hi ha artefactes d'aquests tipus obsolets. Aquesta absència no acredita que les pràctiques SIG estiguin executades.
- Bibliografia: 19 entrades, sense claus duplicades; noves cites resoltes al web i al PDF. Verificació aritmètica exacta de l'exemple: A/B = 0,625/0,5125 i 0,64/0,70.
- `build_site`: construcció correcta. Auditoria HTML: 14 pàgines, cap incidència d'enllaços o estructura detectada. Limitació del subcontrol d'imatges renderitzades: el recurs de paquet `_site/assets/plotly/demo.html` supera el límit d'entrada del comprovador (`UW-IMAGE-COVERAGE`). És una incidència de cobertura del nucli, no una certificació completa d'opacitat del lloc.
- `manual_pdf_preview_prepare`: PDF de 57 pàgines, esborrany, amb índex i capítols 1–9 coherents; bibliografia sense número i presentació del curs com a apartat 0 del nucli. Revisades visualment l'obertura, la taula de Steinitz i la pàgina de l'exemple; comprovades les equacions (1.1) i (1.2), les cites i l'índex. Estat final de PDF: fresc i vàlid.
- Revisió amb Chrome: títols dels nou capítols en ordre, sis taules al capítol inicial, matemàtiques renderitzades sense errors, cap imatge visible trencada i cap cita Liquid sense resoldre. Amplada de document correcta a 1440 px i a 390 px; les taules amples conserven el desplaçament dins del seu contenidor.
- La captura inicial amb taules blanques provenia de canviar directament l'atribut del tema sense sincronitzar les classes de les taules. La inicialització normal del tema dona text visible. No s'ha introduït cap pedaç al nucli per aquesta incidència de la prova.
- `http_check`: inici, nou capítol, vuit capítols reordenats, bibliografia i PDF retornen HTTP 200. Els tres fitxers de `context/` comprovats retornen 404, tal com correspon a contingut privat.
- `git diff --check`: correcte. Tots els fitxers modificats pertanyen a la reserva acceptada; els noms antics dels capítols corresponen als reanomenaments, no a pèrdua de contingut.
- El control `bibliometrics_check`, malgrat retornar `dry_run: true`, va reescriure `_data/metrics.yml` amb zeros en mode offline. S'ha restaurat exactament la versió prèvia per no perdre les mètriques de l'autor; `git diff --exit-code -- _data/metrics.yml` ho confirma. Cal revisar aquest comportament al proveïdor abans d'utilitzar-lo com a comprovació estrictament de lectura.
- Registres editorials a revisió 5: mancança de fonaments resolta; ampliació de les pràctiques acceptada però oberta; passada de línia final del nou capítol amb zero troballes. Les revisions anteriors es conserven, encara que hagin esdevingut obsoletes.

La previsualització local queda disponible per a l'autor a `http://127.0.0.1:32768/geodisseny/ca/`. El PDF de revisió és `tmp/manual-pdf/ca/manual-ca.pdf`; la còpia ignorada que serveix el web és `assets/pdf/manual-ca.pdf`. Rebut vigent de preparació: `.cache/unaltraweb/manual-pdf-preview.json`, SHA-256 `caa152c1c31d92a2c7de7262a5f4b78cf1647728e17320305703545ee2bed663`. La neteja, quan acabi la revisió humana, s'ha de fer amb `manual_pdf_preview_clean` i el rebut revisat en aquell moment.

Els artefactes són locals i no constitueixen publicació. Els tres logotips transparents continuen requerint decisió de l'autor; la coberta generada és opaca. No s'han fet commits, push, PR ni desplegament.
