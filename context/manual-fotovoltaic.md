# Decisions editorials del cas fotovoltaic

## Encàrrec i estructura acceptada

L'autor ha acceptat continuar els canvis locals de la incidència 1 i reorganitzar-los en set capítols. El preflight del 28 de setembre de 2026 només assenyala el checkout brut pel treball conegut de la mateixa sessió; no hi ha conflictes, altres reserves o sessions cooperatives actives. Es preserva aquest treball i es continua a `content/1-fonaments-geodisseny`, sense crear un checkout ni fer un commit d'aprovació.

1. Fonaments d'anàlisi espacial, estadística i geodisseny.
2. Connectivitat i accessibilitat: xarxes i superfícies de cost.
3. Visibilitat i paisatge.
4. Estadística espacial descriptiva, amb aplicació a l'autoconsum.
5. Autocorrelació espacial: Columbus, indicador censal i eines QGIS; transferència posterior a parcel·les agràries.
6. Geoestadística i interpolació, amb aplicació a temperatures màximes.
7. Avaluació multicriteri i geodisseny aplicat.

La sèrie TIGIT/TIG, els prerequisits i la preparació general de QGIS pertanyen a l'inici. Cada capítol introdueix les seves fonts, el suport de la dada i les eines quan el mètode les necessita. El capítol de fonaments ha de poder llegir-se com a teoria, amb un repàs estadístic reutilitzable. Cal desenvolupar paràgrafs, exemples citats, fórmules explicades, activitats i comprovacions, no reproduir l'esquema breu de l'encàrrec.

Indicació posterior de l'autor: el llibre és general de tècniques i geodisseny. Els fitxers estables són `04-estadistica-espacial.md`, `05-autocorrelacio-espacial.md` i `06-geoestadistica-interpolacio.md`; els casos són substituïbles. Aquest document recull les decisions de l'aplicació fotovoltaica, no una restricció permanent del temari. L'autor revisarà el serve abans d'indicar canvis per a una futura publicació `latest`; aquesta sessió no la publica.

### Precisió sobre la introducció i l'àrea de treball

Indicació de l'autor del 30 de setembre de 2026: la presentació semblava en part
una recepta de curs. El manual continua l'enfocament de TIG, amb una àrea propera
que facilita entendre i contrastar les tècniques. Camp de Tarragona i Tarragonès
són referències per als exemples, no un cas d'estudi únic ni un projecte
fotovoltaic que totes les pràctiques hagin de seguir. Tema, àmbit i fonts poden
variar. Els conceptes i els fonaments han de permetre aplicar els mètodes en
altres llocs i amb dades d'altres productors.

La presentació general s'ha reorientat cap a aquesta continuïtat i la consulta
dels mètodes. La programació de lliuraments, la comarca assignada i el pòster
obligatori no es fixen al manual; els enunciats vigents i la guia docent són
les referències corresponents. Al capítol 1 es revisen obertura, transicions,
presentació del territori i enunciats per reduir metadiscurs, repeticions i
floritures. Es conserven l'ancoratge històric cas-fotovoltaic, les fórmules,
els controls numèrics i les fonts dels exemples.

L'autor demana després aprofundir aquesta revisió del capítol 0: la primera
versió encara era esquemàtica i no explicava prou la relació amb el conjunt
del grau. La nova presentació desenvolupa la continuïtat conjunta de TIGIT i
TIG, l'ús transversal de SIG, R i Python, i l'aportació dels fonaments analítics.
El coneixement geogràfic orienta preguntes, dades, escales i interpretacions
per a la diagnosi i les propostes territorials, sense comparar el valor de
professions ni atribuir capacitats exclusives. El territori proper connecta
les aplicacions tècniques amb altres coneixements del grau. Es convida a
explorar noves aplicacions sense fixar una pràctica o lliurament universal.
La configuració detallada i la taula administrativa deixen de dominar l'obertura.

## Font ICAEN aportada per l'autor

URL: https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/

Inspecció del 2026-09-28:

- L'iframe obre l'Hipermapa amb `layers=ENERGIA_INSTALAUTOCONFV`.
- El productor declara que la localització és la del consumidor elèctric associat. En autoconsum col·lectiu és la d'un dels consumidors.
- El productor adverteix de cobertura incompleta; la pàgina consultada indica aproximadament el 93% de les instal·lacions d'autoconsum. Aquest percentatge és una descripció de la pàgina consultada, no una garantia per a qualsevol extracció futura.
- El conjunt és d'autoconsum fotovoltaic, no un cens de totes les centrals fotovoltaiques ni només de parcs sobre sòl.
- L'autor utilitza la descàrrega GeoPackage del visor i observa capes descarregables separadament. El manual documentarà nom de capa, filtres, data, fitxers i reconciliació de recomptes; no inventarà els noms literals dels camps sense inspeccionar el paquet.
- Els punts originals es conserven. Una localització corregida, un accés i una petjada de panells són objectes derivats diferents amb procedència i grau de comprovació.

## Criteris científics

- Potència en kW no equival a energia en kWh. Ponderar per kW localitza capacitat registrada, no producció real.
- La passada del 30 de setembre retira la secció desconnectada sobre el Francolí. L'orientació dels punts es descriu a partir dels resultats, sense atribuir-hi una causa territorial no contrastada.
- Separar distància plana, ortodròmica sobre esfera, geodèsica sobre el·lipsoide, distància de xarxa i cost. El transport pesant necessita accessos reals, girs, gàlibs, càrrega i permisos; la proximitat a l'A-7/AP-7 no implica connexió directa.
- El SIGPAC descriu parcel·les/recintes d'ús agrari; no acredita titularitat. No inferir latifundi o facilitat de compra a partir d'una parcel·la gran o d'un clúster HH.
- L'àrea d'una parcel·la és una magnitud quantitativa contínua sobre suport areal. No s'ha d'interpolar entre centroides com si fos un camp puntual continu. Aquesta crítica no prohibeix tots els mètodes d'interpolació areal ni tots els models de variables discretes.
- Distingir autocorrelació de l'àrea, agrupació de punts i distribució de potència. Explicar matrius, normalització, diagonals, permutacions, comparacions múltiples i sensibilitat.
- El camp interpolat és temperatura màxima de l'aire, no superfície parcel·lària. Distingir mitjana de màximes d'agost, màxima absoluta, percentil i episodi extrem coherent. El període i els dies vàlids han de ser comuns.
- Regressió amb altitud: pendent estimat, no gradient adiabàtic imposat. Estacions de Tarragona i entorn definides per cobertura, no una frontera provincial rígida. Validació espacial sense fuita, reajustant tota la cadena dins de cada partició.
- Temperatura d'aire, de mòdul i de cèl·lula són magnituds diferents. La pèrdua tèrmica necessita coeficient de potència i condicions d'irradiància/vent/muntatge. No convertir una mitjana d'agost en una estimació de producció anual.
- Model 3+3: màscares ambientals, agràries i hídriques/litorals; factors de pendent, temperatura i estructura parcel·lària. És una simplificació docent. Logística i visibilitat intervenen en la comparació posterior d'alternatives o en un escenari ampliat.

## Normativa i fonts acadèmiques verificades

- Decret llei 24/2021, ELI https://www.boe.es/eli/es-ct/dl/2021/10/26/24.
- Decret llei 16/2019: consolidació consultada de 30/10/2025, art. 9. Conté excepcions, regadius i criteris de classes agrològiques; no es pot representar tot amb tres prohibicions universals. El BOE avisa d'actualització en procés; per a ús jurídic cal comprovar el DOGC i els canvis posteriors.
- PLATER: https://icaen.gencat.cat/ca/plans_programes/PLATER/. La pàgina consultada remet a un projecte de decret en tramitació i descriu informació pública. No tractar el visor o una proposta com a aprovació definitiva.
- Llei de costes 22/1988, art. 23 i règim transitori: franja general des del límit interior de la ribera del mar, amb règims específics. Distingir DPH, DPMT, servitud de protecció i inundabilitat. Un buffer de 100 m és un exercici geomètric si no es recolza en delimitació i règim vigents.
- Geurs i van Wee (2004), accessibilitat, DOI 10.1016/j.jtrangeo.2003.10.005; Dijkstra (1959), DOI 10.1007/BF01386390.
- Bishop (2002), llindars d'impacte visual de turbines, DOI 10.1068/b12854. Transferir la distinció visibilitat/impacte, no llindars numèrics eòlics a plaques solars.
- Lefever (1926), el·lipse direccional, DOI 10.1086/214027; convenció de l'el·lipse declarada explícitament.
- Anselin (1995) i quadern GeoDa *Local Spatial Autocorrelation (1)*: exemple verificat de donacions per habitant als departaments francesos del conjunt Guerry; ús per explicar unitat i interpretació local, no per extrapolar resultats.
- Hengl, Heuvelink i Rossiter (2007), DOI 10.1016/j.cageo.2007.05.001; Roberts et al. (2017), DOI 10.1111/ecog.02881.
- Faiman (2008), DOI 10.1002/pip.813; Skoplaki i Palyvos (2009), DOI 10.1016/j.solener.2008.10.008; documentació pvlib del model Faiman.
- Uyan (2013), selecció de parcs solars a Karapinar, DOI 10.1016/j.rser.2013.07.042; exemple de transferència metodològica, sense copiar pesos locals.
- Wasserstein i Lazar (2016), interpretació de p-valors, DOI 10.1080/00031305.2016.1154108.

## Ampliació territorial del 29 de setembre de 2026

La passada actual incorpora seccions censals de 2024, edificis cadastrals del
feed 2026-08-21 i autoconsum ICAEN. L'associació és ecològica i exploratòria:
126 seccions, r=−0,40095367; Moran del mateix indicador en 150 seccions,
I=0,14404677. Fonts, correspondència INE–DGC i auditoria són a
`context/inputs/seccions-resultats.json`; no s'infereix causalitat ni relació
individual entre instal·lació i edifici.

També s'han executat els casos acordats de xarxa ICGC, solar cadastral de la
Pineda i sector de la refineria nord. Els supòsits de sentit, velocitat, fricció
i altures es mantenen separats de les dades reals. MDT/MDS regionals, geometries,
resultats i instruccions són als dos paquets locals nous de Moodle, descrits a
`context/dades/practiques-territorials.md`. No s'han carregat al servei de Moodle.

El MDS s'ha preparat com a entrada de contrast; els controls petroquímics publicats
al capítol corresponen a MDT, sense simular que s'hagin verificat totes les altures
dels edificis. El motor de xarxa natiu no executa penalitzacions de gir.

## Ampliació pedagògica del 30 de setembre de 2026

- Introduccions i recordatoris de conceptes als set capítols; eines integrades
  en el desenvolupament, sense pràctica separada abans d'Activitats.
- Captures internes de centres, geometria per expressió, recompte, KDE,
  Moran local, Gi*, IDW, variograma, kriging, conca visual i mostreig.
- Exemple Columbus (49 barris) abans de les seccions; Moran sobre una variable.
  La regressió antiguitat–potència és una ampliació, no un requisit de Moran.
- XEMA: 182 estacions amb 48 intervals vàlids del 15-08-2025, màxima diària TU.
  El model cartogràfic principal compara IDW i kriging ordinari, sense altitud.
  Regressió-kriging es manté com a ampliació explicada, no com un resultat real
  validat. No s'ha executat validació fora de mostra de les temperatures.
- Model final de SAGA: a+b*x/100000, a=2.79123, b=19.5643; descartar els intents
  exponencial i de coeficients quadràtics per al lliurament final.
- Petroquímica: 28 mostres a 250 m, resultats nous a models-20260930; els models
  i paquets de quatre mostres del 29 de setembre queden com a historial.
- Steinitz aplicat a l'hort solar: sis models i tres iteracions, amb SVG propi.
- Nou paquet privat demos-ampliacio-20260930.zip, 94 fitxers, 34.195.177 bytes;
  SHA-256 7f387cabca8dee8432a66ea287e5fed75da8191137dc875684ddaffc876eacc5.
  Complementa les extraccions originals dels paquets previs; no s'ha pujat a Moodle.
- Indicació operativa de l'autor: utilitzar els MCP; no consultar codi dels
  proveïdors per continuar aquesta revisió.

### Historial de la primera passada

Quatre diagrames Mermaid amb diavisuals (Steinitz, regressió-kriging, model 3+3 i sensibilitat). Sis figures computades amb unaltraweb (distribucions, distàncies, perfil visual, centres ponderats, veïnatges i resposta tèrmica). Totes les dades sintètiques s'identifiquen com a docents; cap gràfic sintètic representa resultats mesurats al Tarragonès. Fonts, sortides i rebuts formen paquets atòmics de la reserva acceptada.

## Dades de demostració i distribució Moodle

L'autor ha indicat que les dades preparades s'han de distribuir per Moodle i mai com a descàrregues del manual. Els originals, els subconjunts, el procés de preparació i els paquets es conserven exclusivament a `tmp/dades-docents/`, ignorat per Git i exclòs de Jekyll. El manual només descriu fonts, mètodes, controls i resultats de les demos. No posar GeoPackages, GML, CSV de registres ni els enllaços temporals FME sota `assets/` o al text públic.

L'exportació temporal aportada el 2026-09-28 s'ha descarregat i preservat: SHA-256 `546be2aa2a44e26a005deb89028264b105b77992b9864585cb06ea7dd4214b9b`. Conté només `ENERGIA_INSTALAUTOCONFV`, en GML, més XML i SLD; les altres capes activades a les captures no estan incloses. Inventari original: 127.591 registres, EPSG:25831, MultiPoint amb un únic punt per registre. Camps: `gml_id`, `X`, `Y`, `CODI_MUN`, `MUNICIPI`, `COMARCA`, `PROVINCIA`, `POT_KW`, `UBICACIO`, `INTERVAL`, `OBJECTID`.

Les metadades indiquen revisió 2024-06-30 i segell 2024-12-03. La data efectiva del conjunt complet no es pot deduir de l'extracció de 2026. La informació legal específica de l'XML està buida: no atribuir automàticament a l'ICAEN la llicència dels límits ICGC.

Preparació amb GDAL 3.8.4 i límits ICGC 1:5.000 v2r2 de 2026-01-20 (CC BY 4.0), ZIP ICGC SHA-256 `563fb7d81e143509d88569a9e8fe86d7c44ae9ce9e96c75b888379a7f0554162`:

| Selecció | Registres | POT_KW conegut positiu | POT_KW nul | Registres Edifici / Terra |
| --- | ---: | ---: | ---: | --- |
| Atribut PROVINCIA = Tarragona | 20.447 | 15.331 | 5.116 | 20.415 / 32 |
| Atribut COMARCA = Tarragonès | 5.102 | 3.762 | 1.340 | 5.096 / 6 |
| Intersecció amb buffer docent de 20 km del Tarragonès | 17.110 | 12.656 | 4.454 | 17.087 / 23 |

No hi ha geometries absents, registres multipunt amb més d'una localització ni `gml_id` duplicats en els subconjunts. Hi ha coincidències de coordenades: no s'han eliminat com si fossin duplicats acreditats. Les seleccions provincial i comarcal coincideixen amb els límits geomètrics de control en aquesta extracció. Els tres subconjunts se solapen i no s'han de fusionar.

Paquet: `tmp/dades-docents/demos-autoconsum-tarragona-20260928.zip`, SHA-256 `9a6d7da59f8df7f4e3213ff2b33c36ebe3c523d6f4a9df73546d98e0193fb940`. Inclou dos GeoPackages, metadades, estil original, manifest, instruccions i procés de preparació. Encara no inclou XEMA, relleu, SIGPAC, xarxes ni les altres capes FME. La preparació per Moodle no implica que el paquet s'hagi pujat a l'aula virtual.

## Set paquets de sandbox i preparació complementària

L'autor ha aportat set ZIP a `sandbox/`, que es mantenen intactes. Inventari complet amb hashes, camps i abstracts a `tmp/dades-docents/inventari-sandbox.json`. El primer ZIP és idèntic al recuperat de l'enllaç temporal.

| Capa | Original | Selecció provincial | Ús docent |
| --- | ---: | ---: | --- |
| `ENERGIA_PARCSSOLARS_MULTIPOLI` | 488 | 165 | Propostes i estat administratiu; no totes estan en servei |
| `ENERGIA_SOLAR_PARCS` | 155 | 13 | Plantes anteriors al DL 16/2019 segons la fitxa; no tot el parc actual |
| `ENERGIA_PARCSEOLICSSOLARS_LIN` | 884 | 298 | Traçats d'expedients: 255 RASA i 43 LAAT; no tota la xarxa en servei |
| `ENERGIA_BATERIES_STANDALONE` | 104 | 26 | Ampliació d'emmagatzematge; separada de la generació solar |
| `ENERGIA_SOLAR_PROTECESPECIE` | 30.096 | 7.764 | 1.193 registres No apta i 6.571 Ponderació; no convertir-los tots en exclusió |
| `ENERGIA_SOLAR_CAPACITACOLLI` | Ràster 28.173 × 27.905 | 12.694 × 11.591 | Comparació amb una sortida composta de capacitat 0–1 |

Les entitats vectorials s'han seleccionat per intersecció amb la província i es conserven senceres, sense retallar projectes o alterar atributs de superfície. No s'hi han detectat geometries invàlides en la selecció. Les sol·licituds contenen 76 autoritzades, 17 en servei, 17 no autoritzades, 49 en tramitació, 5 desistides i una sense estat.

El GeoTIFF no tenia codi d'autoritat a l'arrel del WKT, però `IsSame(EPSG:25831)` retorna cert i `FindMatches` identifica EPSG:25831 amb confiança 100. No s'ha tractat com un ràster de CRS desconegut. El retall preserva l'alineació original a 10 m, sense interpolació dels valors, amb 62.575.991 cel·les vàlides i 55.772.740 zeros. `NoData` queda separat; les metadades declaren escala 1:40.000.

Paquet complementari: `tmp/dades-docents/demos-complements-tarragona-20260928.zip`, SHA-256 `6c9beca900b1a63eb8354710e414833c8691eec1dcdb0a4cc5dfe2d2342a9216`. Inclou GeoPackage vectorial, GeoTIFF provincial, metadades, estils, manifest i instruccions. Falta incorporar XEMA, MDT/MDS, SIGPAC/Cadastre, vies i les altres restriccions per executar totes les demos. Les capes completes es destinen a l'arxiu al núvol que gestiona l'autor; no s'ha fet cap pujada.

Els SVG Mermaid utilitzen el nom complet de font, com `steinitz.mmd.svg`, d'acord amb el contracte del proveïdor. Les fonts computades i els SVG de les figures conceptuals no incorporen cap registre real dels paquets docents.
