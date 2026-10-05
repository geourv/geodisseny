# Capítol 4: progressió, exercicis i captura QGIS

Revisió del 4 d'octubre de 2026, a petició de l'autor. Mateixa branca
`content/5-visibilitat-mdt-mds` i incidència5. Reserves ampliades:
https://github.com/geourv/geodisseny/issues/5#issuecomment-5974814916,
https://github.com/geourv/geodisseny/issues/5#issuecomment-5974989086 i
https://github.com/geourv/geodisseny/issues/5#issuecomment-5975078231.

## Estat actual: pràctica municipal i escenaris d'imputació

L'autor prefereix QGIS com a via docent i PySAL només quan una necessitat
concreta ho exigeixi. Constantí és ara el cas principal; el Morell i el Catllar
serveixen per comparar distribucions. La comarca queda com a referència de
conjunt i ampliació per a recomptes, kernel i seccions. La introducció de C5
també explica el problema, sense anticipar biblioteques o casos encara no presentats.
Les atribucions i les dependències del complement d'autocorrelació es conserven.

Reserva de fonts, figura, ortofoto i cinc bundles:
https://github.com/geourv/geodisseny/issues/5#issuecomment-5983539648.
Preparador `context/dades/escenaris_potencia.py`, input de figures
`context/inputs/punts-escenaris.json`, recepta/prompt `context/qgis/punts-municipals`.
Destinació privada `tmp/dades-docents/qgis/punts-municipals-20261004/`.

### Regles i controls

POT_KW no es modifica. Només per als camps buits s'assignen pesos:

| Classe | w_inf | w_mid | w_sup |
| --- | ---: | ---: | ---: |
| Fins a 5 kW | 0 | 2,5 | 5 |
| Més de 5 i fins a 25 kW | 5 | 15 | 25 |
| Més de 25 i fins a 100 kW | 25 | 62,5 | 100 |

Els llindars inferiors són valors límit, no potències observades. Punt mitjà
no significa mitjana empírica. Les tres assignacions conjuntes no delimiten
totes les posicions possibles ni constitueixen un interval de confiança.
El cas sense valor a la classe oberta és a Torredembarra; no apareix als tres
municipis seleccionats. Quan hi ha xifra publicada, es manté encara que sigui >100.

| Municipi | Registres / assignacions | Sumes inferior / central / superior, kW | Canvi del centre central, m | Separació inferior–superior, m |
| --- | --- | --- | ---: | ---: |
| El Morell | 111 / 24 | 651 / 771 / 891 | 22,328 | 8,108 |
| El Catllar | 437 / 111 | 1881 / 2338,5 / 2796 | 56,243 | 49,845 |
| Constantí | 124 / 26 | 2825 / 2970 / 3115 | 1832,430 | 193,671 |

Verificats els 672 registres amb native:fieldcalculator: valors publicats
idèntics i assignacions segons la classe. Dotze centres natius contrastats amb
NumPy; identitat del centre central a partir dels centres i sumes dels altres
dos escenaris comprovada. Els punts i les seleccions són els mateixos.

Constantí: 2770 kW publicats + 200 assignats. Registre A,450 kW publicats,
15,2% de l'escenari; cinc pesos més grans,37,4%. El mapa a àrees proporcionals
sobre ortofoto explica el desplaçament cap al grup occidental. Es diferencia
publicat/assignat per color. El centre sense pes queda entre grups, no es
presenta com un emplaçament òptim.

Dispersió sense pesos dels124punts: D=2000,656426 m, a=1934,437738 m,
b=510,467208 m, azimut axial110,220000°. Cercle/el·lipse i expressions natives
d'agregació sobre la capa municipal contrastats. Projecte amb8capes reobert
a `/project`, readonly, sense xarxa ni repositori d'origen; hashes conservats.

### Figures, captures i paquet

Nova ortofoto ICGC2025: WMS GetMap,8m/píxel,1250×1125, extensió
343500/4554000/353500/4563000, EPSG:25831. La capa font és de25cm; no s'ha
presentat el retall com a resolució nativa. PNG i rebut a context/inputs;
SHA `87a1b6507d0cd345a2e6a4497a4313be3a083cf608825ac9b70366dbdaafd9b5`.
SVG nous: `constanti-pesos` i `punts-escenaris`, amb fonts QMD.

Cinc captures municipals: dades, camp decimal, centre, resultat i el·lipse.
Connexió GeoPackage desplegada, x11/DPR1, català, sense warnings; inspecció
visual feta. Càlcul programàtic i diàlegs configurats són evidències separades.

Suplement privat `tmp/dades-docents/practica-punts-municipals-20261004.zip`:
30fitxers,15.255.627bytes, SHA
`b7ed57dc62db492c8dfd620449eb8dfa4f652a8efbd3096cc976e5f4247f767f`.
Inclou GeoPackage, ortofoto, projecte relatiu, figures, captures, fonts,
controls, README i manifest. CRC i tots els hashes comprovats. No modifica
el paquet comarcal anterior ni s'ha pujat a Moodle.

### Revisió actual

50computacions actuals. C4amb23imatges i C5amb8, revisats a1440/390px:
4vistes,31imatges, sense errors MathJax, imatges trencades ni desbordament.
PDF235p, SHA
`6d29bba2ea6c5e2967d518636580fb115d1b28cbfd466c75d0a5b289954840ca`.
Límits globals correctes i passos, mapes i escenaris revisats visualment.
Les cometes davant de C dels dos filtres es transformaven en Ç al PDF en
codi inline; s'han passat a blocs SQL i s'ha comprovat el text extret.
No s'ha modificat codi del proveïdor. L'avís dimensional de la figura
comparativa de tres municipis continua documentat a la revisió anterior.

Reviews d'evidència/estructura C4 i còpia C5 a revisions52–54. Troballes de
cas principal i escenaris resoltes amb motiu a55/56. Estat56, sense aprovació
humana; cap commit ni publicació. Preview local32768 disponible.

## Historial: cobertura, municipis i Snow

L'autor ha demanat distingir el 93% de cobertura del mapa de les potències
buides, concretar la utilitat dels resums i comparar municipis. Reserva:
https://github.com/geourv/geodisseny/issues/5#issuecomment-5979748028.
També s'ha corregit la introducció: explica recompte i disposició espacial
amb les biblioteques ja presentades, sense anunciar Snow, ICAEN o QGIS.
El perfil conserva aquest criteri; troballa registrada i resolta a revisions43–45.

### Verificació del GML i significat del 93%

La pàgina oficial de localització i l'XML de metadades de l'extracció diuen
que s'hi representa aproximadament el 93% de l'autoconsum de Catalunya amb
georeferenciació vàlida. No és una taxa local del Tarragonès ni una proporció
de camps POT_KW disponibles.

`analitzar_punts_municipis.py` llegeix directament el GML original, amb SHA
`58eddc54d79e15a3c348f13c874b9ef92abf9af6c5b7672169f7c7883597dd4b`,
i contrasta cada registre del Tarragonès amb el GeoPackage per gml_id,
coordenades i potència. Dels127.591registres del GML,5.102corresponen al
Tarragonès i tots tenen geometria. Hi ha3.762POT_KW numèrics i1.340elements
POT_KW presents però buits; no és una pèrdua produïda en convertir a GPKG.

Els1.340conserven INTERVAL:1074fins a5kW,257de més de5fins a25kW,
8de més de25fins a100kW i1de més de100kW. No s'ha establert la causa
dels camps buits ni si la mancança és de la base productora o només de
l'exportació; no atribuir-la a privacitat o absència d'instal·lacions.

El capítol pren cada capa com a univers de treball complet per a la
descripció. Tots els punts intervenen en la comparació municipal sense pes;
la comparació recompte–kW conserva les mateixes observacions amb valor
numèric. No s'imputen pesos a partir dels intervals. El desplaçament per
selecció és244,383m, diferent dels2902,715m per ponderació.

### Comparació municipal i interpretació

Font i petit input de figura: `context/dades/analitzar_punts_municipis.py`
i `context/inputs/punts-municipis.json`. Centres dels22municipis contrastats
amb `native:meancoordinates`, UID=CODI_MUN, sense pes i amb POT_KW; tolerància
absoluta1e-6m. Els resums descriptius utilitzen covariància poblacional.
Agrupació pel codi publicat; límits ICGC20260120 com a context, simplificats
5m només per dibuixar. La nova figura conserva la mateixa escala als tres panells.

| Municipi | Tots els punts | Distància estàndard, m | Punts comparables amb kW | kW publicats | Desplaçament per pes, m |
| --- | ---: | ---: | ---: | ---: | ---: |
| El Morell | 111 | 323,3 | 87 | 611 | 25,2 |
| El Catllar | 437 | 2278,2 | 326 | 1761 | 125,9 |
| Constantí | 124 | 2000,7 | 98 | 2770 | 1645,5 |

El resum comarcal continua com a context; s'explica el significat de la
ponderació amb les quotes de Constantí(2,60% dels registres coneguts/7,56%
dels kW) i el Catllar(8,67%/4,81%). La comparació municipal permet llegir
compacitat, grups separats i allargament. No interpreta aquests resums com
taxes d'adopció o ubicacions òptimes. Activitat municipal afegida.

Les expressions mostren la convenció de radi/semieixos i es diferencien d'un
cercle envolupant mínim. El kernel de la pràctica és QGIS, automatitzable
amb PyQGIS; PySAL/libpysal/esda correspon a Moran/LISA del capítol següent.

### Figura de Snow i revisió renderitzada

SVG amb JPEG original incrustat byte a byte i13cercles blaus vectorials.
Font executable `assets/quarto/figures/john-snow-pous.qmd`; coordenades
documentades a `context/inputs/snow-pous.json`. Comprovats els13símbols
PUMP en retalls locals i en el mapa complet. El domini públic permet
l'anotació; el peu diferencia original i cercles, sense radis geogràfics.

48computacions actuals. C4 té22imatges, revisades a1440/390px; sense
errors ni desbordament. PDF233p, SHA
`84b0f29cfab223419f7bee878f816b96a789e2160562bb1ce536054899aec9f9`.
Pàgines143–145,150i159–160inspeccionades; límits globals correctes.
La figura municipal té text estimat de9,62pt al PDF; es manté54rem al web
per a tres mapes comparables, amb etiquetes lleugerament més grans que el
cos(18px/16,32px). Avís dimensional revisat visualment, sense modificar
generats per silenciar-lo. SVG de Snow verificat també al tree construït.

Reviews d'evidència i línia a revisions47/48; dues troballes resoltes amb
motiu a revisions49/50. La introducció anterior i la resta de l'historial
es conserven. El paquet docent segellat anterior continua idèntic: aquesta
ampliació utilitza els seus punts i afegeix figures al manual, no un ZIP nou.

## Decisions de la preparació inicial

- Introducció amb situacions recognoscibles i significat dels resums.
  Snow és el primer cas; es desenvolupa la seva importància abans del registre
  ICAEN. Distribucions puntuals, exemple de centres amb nombres, formulació i
  aplicació precedeixen dispersió, graella, kernel i seccions.
- Els títols de transició s'han revisat semànticament a C1/C4/C5/C6/C7.
  Identifiquen regressió, modelització cartogràfica, matriu de pesos,
  semivariograma, prediccions IDW i alternatives/impactes/decisió.
  Tots els ancoratges de C1/C4 del render anterior es conserven; també el
  de l'activitat IDW. C5/C6/C7 tornen a draft per la revisió dels títols.
- Autoria i llicències de Snow/Wald, amb enllaços, són a `data-caption-source`.
  No queden els paràgrafs administratius al cos. Les imatges són idèntiques.
- Retirades les versions QGIS redundants dels peus C3/C4. El capítol0 manté
  QGIS3.44LTR com a referència; els manifests conserven3.44.11.
- Quatre troballes ancorades registrades abans de corregir-les, resoltes
  explícitament a revisions32–35. El perfil de redacció conserva els criteris.

## Preparació i controls

Font: `context/dades/preparar_punts_tarragones.py`. Destinació privada:
`tmp/dades-docents/qgis/punts-tarragones-20261004/`.
Resum versionat: `context/inputs/punts-tarragones.json`.

Tres fonts retingudes, amb SHA-256 comprovat:

| Entrada | SHA-256 |
| --- | --- |
| autoconsum-tarragona-20260928.gpkg | 1c8b4bda31ac5bfa35fd8ac4b1fbf36990d01065590c673b579e0670291ac9c8 |
| icaen-ambit.gpkg | 2acf61341b97e3120a6668aed34973b1238daa413efd5f281513f0e8948fa709 |
| seccions-analisi.gpkg | 84d7a33bfa8dab8089bb852e447947c92a95da3bf733161663e24a2be98523af |

No es modifiquen originals ni paquets anteriors. Els denominadors cadastrals
de les seccions ja estaven preparats: no s'afirma haver refet aquí la ingestió
dels edificis. Es conserva `seccions-resultats.json` amb dates, correspondències
INE/DGC, URLs i controls de la preparació anterior.

- 5.102 registres; 3.762 amb potència coneguda, 36.633 kW. Centres natius contrastats
  amb NumPy; desplaçament per ponderació2902,714732m.
- Cercle de 8.698,204203 m; semieixos de 8.152,141105/3.033,373000 m;
  azimut77,672737°. Expressions QGIS d'agregació i geometria contrastades
  amb covariància independent i coordenades dels vèrtexs.
- 680 quadrats d'1 km²: recompte i suma comprovats **cel·la per cel·la** amb
  assignació independent de coordenades. Totals3762 i36633.
- Kernels quartic, h=500/1.500 m, píxel de 100 m, pesos iguals o POT_KW; Raw
  normalitzat amb3e6/(πh²). Integrals3762,002337/3761,999764registres i
 36633,587271/36633,014610kW. Les parelles comparteixen escala de colors
  dins de la mateixa unitat; llegendes natives amb límits finits.
- La fórmula del guió s'ha executat també amb **QgsRasterCalculator**:
  totes les cel·les i les màscares coincideixen amb tolerància de Float32.
  Error màxim0,00048828125kW/km² en la sortida ponderada de500m.
- 151 seccions; 5.096 registres Edifici, 3.757 coneguts, 36.058 kW.
  Correspondència comprovada secció per secció amb la preparació anterior.
  Un indicador NULL, cusec4314806003, diferenciat de zero i amb classe grisa.
- Sis projectes, 18 capes cadascun, reoberts sense xarxa a `/project`, només
  lectura i sense muntar el repositori. Referències confinades i relatives;
  hashes conservats. Comprovat també el subset URI de la captura de seccions.

El muntatge readonly va impedir desar estadístiques auxiliars `.aux.xml` en
la verificació; els ràsters no es van modificar. Una incidència inicial del
resum posterior a escriptures d'estil/projecte retornava un iterador buit:
corregida amb el recompte de les entitats validades abans de representar i
amb reobertura SQLite en un procés separat. El registre inicial es conserva
a `controls/calculs-inicial-incidencia.json`. La vida de QgsApplication es
manté fins després d'alliberar les capes; verificació i CLI finalitzen amb èxit.

## Captures i interfícies públiques

Prompt i recepta: `context/qgis/punts-tarragones.{md,yml}`.
14bundles, amb PNG, SVG anotat i manifest; x11/DPR1, català, sense warnings.
Les imatges mostren dades, dos accessos a centres, paràmetres i resultats,
dispersió, graella, recompte, kernel i agregació censal.

Les connexions es declaren a `connections`, amb `type: gpkg`. Després de
configurar-les, `trigger_action` amb `name: mActionRefresh` refresca
l'Explorador. `expand_tree_item` desplega GeoPackage, `dades.gpkg` i
`resultats.gpkg`; els noms són visibles a les vistes generals. El selector
«resum» arriba a `seccions_resum`: el nom complet havia resolt la capa
«seccions» pel reconeixement aproximat del motor. Inspecció visual feta.

Els rectangles utilitzen `margin: 0` i `shadow: false` per no solapar les
files veïnes. Al kernel es ressalten els widgets reals `mCellXSpinBox` i
`mCellYSpinBox`; el selector genèric PIXEL_SIZE només cobria el títol del grup.
La figura mostra els controls bàsics; el text indica desplegar els avançats.

El director genèric va produir l'exemple de Vila-seca, no aquesta pràctica.
Se n'ha utilitzat la sortida pública per confirmar el contracte de connexions,
sense renderitzar fixtures alienes. La configuració canònica temporal s'ha
retirat; els probes privats queden desregistrats. No s'ha llegit ni modificat
codi intern del proveïdor. No s'han retocat PNG/SVG generats.

Els càlculs Processing, els diàlegs configurats i els resultats representats
són evidències diferents. `manual_click_by_click` continua false.

## Paquet docent

`tmp/dades-docents/practica-punts-tarragones-20261004.zip`:
82fitxers,13.853.420bytes; SHA-256
`ee421cdc2ff89db787ea13ea7f032930cf5ae4c66da850c42bca8944cc9bebf7`.
CRC i hashes de tots els membres verificats. Segellat localment, fora de Git
i del web, sense pujada a Moodle. Cal una versió nova per canviar-ne el contingut.

- GUIA: 14 pàgines, 2.076.486 bytes; SHA
  `ebf530e662dcabb1bf82eebe4eb3ff519dbe49a47e1c9a61bde13b393076ad84`.
- SOLUCIONS: 2 pàgines, 41.540 bytes; SHA
  `1a494148a4ff243c02bbe5bca209298fa94f7b78dc3fc4d0247e8ef28d28d2a8`.
- Fonts dels guions a `context/practiques/punts-tarragones*.md`; PDFs i
  captures inspeccionats, sense desbordaments. Compilació Pandoc/XeLaTeX
  amb la imatge PDF fixada i `fontfamily=fontspec`.

Ordre de reproducció: `--build`, `--style`, `--finalise`, render de les
captures, `--finalise`, `--verify /project --report …`, `--record --report …`,
`--docs`, verificació dels PDFs i `--package`. Les fases QGIS utilitzen el
runtime fixat i entrades readonly; només la destinació nova és writable.
La preparació espera l'estructura del repositori; els exercicis i els projectes
del paquet funcionen de manera autònoma amb les seves dades.

## Revisió del lloc

- C4 té 21 imatges, 14 de captura. Web dels sis capítols modificats i bibliografia
  revisat a1440/390px:14vistes,82imatges, sense MathJax erroni, citacions
  crues, imatges trencades ni desbordament. Drets enllaçats dins del peu.
- PDF de 231 pàgines, SHA
  `d81ced19bd53c5914814e173dbc010444df6d056d7a2251d9c25b03a45c3c210`.
  Límits correctes després de separar l'identificador llarg de KDE en un
  bloc de codi; peus, mapes, procediments i taules inspeccionats.
- Site-check executat abans del build, qualitat de fonts sense warnings.
  Prose-check només conserva «I i» dels nombres romans de C1.
- Reviews fresques d'estructura/evidència C4 i còpia dels altres cinc capítols:
  revisions36–42. Estat42,35reviews,28històriques stale; les quatre troballes
  originals conserven resolució i motiu. Cap aprovació humana implícita.
- HTML-audit correcte, amb els avisos coneguts dels logos transparents,
  les limitacions d'inspecció SVG i el pressupost global d'imatges. Revisió
  complementària al navegador; cap font privada al tree real d'_site.
  No s'han alterat generats ni logos per silenciar els avisos.

Preview local32768; PDF fresh/artifacts_valid i còpia servida idèntica.
Els capítols modificats continuen en draft. Cap commit ni publicació d'aquesta
revisió; el main públic anterior no s'ha alterat.
