---
layout: manual-home
title: "Anàlisi Espacial i Geodisseny"
description: Fonaments d'anàlisi espacial i geodisseny per relacionar el coneixement geogràfic amb la diagnosi i les propostes territorials.
lang: "ca"
ref: home
profiles: [unaltremanual]
content_status: approved
permalink: "/ca/"
nav: false
show_chapter_index: true
figure_captions: true
manual_references: false
---

**Anàlisi Espacial i Geodisseny** continua l'aprenentatge iniciat a [TIGIT](https://geourv.github.io/tigit/ca/) i [TIG](https://geourv.github.io/tig/ca/) dins del Grau en Geografia, Anàlisi Territorial i Sostenibilitat de la Universitat Rovira i Virgili. Al llarg del grau, el treball amb dades i cartografia acompanya l'estudi del paisatge, la població, les activitats econòmiques i el medi físic. Les eines tècniques es van aprenent en relació amb les preguntes que sorgeixen d'aquests àmbits.

A TIGIT es treballa amb dades, indicadors i representació cartogràfica; a TIG s'aprofundeix en els models de dades, les consultes i el geoprocessament. Aquests coneixements també es posen en pràctica en altres assignatures. Els SIG, els llenguatges R i Python i altres eines de tractament de dades serveixen per explorar informació, fer càlculs i comunicar resultats. L'experiència adquirida en una assignatura es pot recuperar i ampliar quan apareix una pregunta diferent en una altra.

Anàlisi Espacial i Geodisseny aprofundeix en els **fonaments geogràfics i estadístics de l'anàlisi**. S'hi estudia com representar les relacions entre llocs, descriure distribucions, estimar valors i comparar alternatives. També s'examina per què dos mètodes poden donar resultats diferents, quins supòsits expliquen aquestes diferències i com es poden contrastar. Aquesta base dona criteri per escollir una tècnica i interpretar allò que se n'obté.

## El coneixement geogràfic en l'anàlisi {#recorregut}

Els SIG s'utilitzen en moltes disciplines i àmbits professionals. Les preguntes, la formació i l'experiència de qui els fa servir influeixen en l'ús que se'n fa. En la formació geogràfica, l'anàlisi relaciona processos físics, activitats humanes i formes d'ocupació del territori. Conèixer el paisatge, el relleu, els recursos hídrics o la distribució de les activitats econòmiques orienta la selecció de dades, l'escala de treball i la interpretació dels mapes.

Per estudiar un possible canvi d'ús del sòl, per exemple, un mapa de pendents descriu una part de les condicions del terreny. També interessa saber com drena l'aigua, quins usos hi ha, quines activitats en depenen i com es relaciona aquell lloc amb els espais veïns. Les problemàtiques conegudes i les observacions sobre el terreny poden assenyalar qüestions que encara no s'han incorporat al model. Comparar els càlculs amb aquest coneixement ajuda a precisar què s'ha representat i quina informació falta.

Així, l'ús de les eines contribueix a la **diagnosi territorial**: estudiar les condicions d'un lloc, reconèixer patrons i processos i precisar els problemes que s'hi volen abordar. Un resultat estadístic o cartogràfic aporta evidència que es llegeix juntament amb altres dades, observacions i estudis. La seva interpretació necessita tant conèixer el mètode com entendre el fenomen que s'analitza.

El **geodisseny** relaciona aquesta diagnosi amb la formulació de propostes. A partir del coneixement del lloc es poden plantejar alternatives, estimar-ne els efectes i discutir amb quins criteris es comparen. Aquesta discussió pot requerir aportacions de diferents disciplines i de les persones implicades. Els mètodes d'anàlisi ajuden a fer explícites les conseqüències previstes, les preferències i les incerteses que intervenen en la decisió.

## Aprendre sobre un territori proper {#camp-tarragona}

El treball sobre una àrea propera, habitual a TIGIT, TIG i altres assignatures del grau, facilita la relació entre la part tècnica i el coneixement geogràfic. El **Camp de Tarragona**, amb molts exemples al **Tarragonès**, ofereix una referència compartida. Els seus espais agraris, nuclis urbans, activitats industrials, infraestructures i entorns litorals es poden estudiar des de les diverses qüestions que es tracten al llarg del grau. El [Catàleg de paisatge del Camp de Tarragona](https://www.catpaisatge.net/ca/catalegs/6-camp-de-tarragona) és una de les fonts per situar aquests elements i les seves relacions.

Sobre aquest territori, un mapa de pendents es pot interpretar amb coneixements de geomorfologia; la distribució d'equipaments, amb els de població i mobilitat; o una qüestió de drenatge, amb el que se sap del relleu i del funcionament de l'aigua. Les observacions de camp i els treballs d'altres assignatures ajuden a discutir els resultats del SIG. Alhora, un càlcul pot revelar una relació poc evident o suggerir una pregunta que mereixi una observació més detallada.

Aquesta referència propera s'adapta a cada problema. Una xarxa de transport pot necessitar connexions que travessen el límit comarcal; una estimació climàtica, observacions d'un àmbit més ampli. Els temes, les àrees i les dades de les pràctiques poden variar. Treballar també en altres llocs permet reconèixer què es manté del mètode i què cal revisar segons les condicions del territori, la cobertura de les fonts o l'escala d'anàlisi.

## Programari i organització del treball {#projecte-reproduible}

Els [fonaments del primer capítol]({{ site.baseurl }}/ca/chapters/fonaments-geodisseny/) serveixen de referència per als mètodes que es desenvolupen després. Els exemples petits permeten seguir les operacions; les aplicacions amb dades territorials mostren les decisions que comporta treballar amb observacions i cartografia. Les explicacions indiquen la procedència de les dades i els supòsits, de manera que es pugui revisar el càlcul i entendre'n els límits.

### QGIS i els proveïdors d'eines {#qgis-proveidors}

[QGIS](https://qgis.org/) és l'entorn principal dels procediments del manual, amb la versió 3.44 LTR com a referència documental. Integra eines pròpies, complements, biblioteques i altres programes d'anàlisi geogràfica. El [sistema de Processament](https://docs.qgis.org/3.44/en/docs/user_manual/processing/intro.html) ofereix una interfície comuna per executar algorismes de diferents **proveïdors**. GDAL/OGR aporta biblioteques i utilitats per a dades ràster i vectorials; GRASS GIS i SAGA GIS són sistemes d'informació geogràfica amb eines que es poden incorporar a aquest entorn. Els complements també poden afegir funcions, menús o proveïdors. El conjunt pot reunir centenars d'eines, segons els components instal·lats.

Una mateixa pregunta es pot abordar amb més d'una eina. Dues eines de distància ràster, per exemple, poden demanar representacions diferents dels punts d'origen o tractar de manera diferent el NoData. La comparació requereix revisar el mètode, les unitats, els valors inicials, la graella i les dades d'entrada. La coincidència entre resultats pot servir de comprovació; una diferència s'ha d'interpretar a partir d'aquelles decisions. El manual desenvolupa aquestes distincions quan ajuden a entendre una anàlisi, i les pràctiques identifiquen el proveïdor i l'algorisme que s'utilitza.

A TIGIT i TIG havien tingut menys pes les eines de proveïdors externs a `native:`. En aquesta assignatura se n'amplia l'ús i es presta una atenció especial, sobretot a les pràctiques, a les **ordres de línia de comandes** de GDAL, GRASS, SAGA i altres eines. Una ordre identifica un programa o mòdul, les entrades, les sortides i les opcions de càlcul. Llegir-la al registre de Processament, quan el proveïdor la mostra, permet relacionar la configuració del diàleg amb allò que s'ha executat, interpretar errors i repetir el procediment. Les expressions de QGIS que calculen valors de camps o omplen un lot tenen una sintaxi i una funció pròpies, que es distingeixen d'aquestes ordres.

>> **Preparació del programari.** Les pràctiques d'autocorrelació utilitzen el complement **Hotspot Analysis**, versió 4.0.0, i les biblioteques Python **libpysal** i **esda**, del projecte PySAL. No totes les instal·lacions de QGIS les incorporen. Abans d'aquelles pràctiques, segueix la [instal·lació i la prova des de QGIS]({{ site.baseurl }}/ca/chapters/dependencia-espacial/#preparacio-pysal): s'hi distingeixen Windows amb OSGeo4W, macOS i Linux. Instal·lar un paquet en un altre Python de l'ordinador no garanteix que QGIS el pugui utilitzar.

La preparació tècnica permet combinar el treball des dels diàlegs amb la lectura de les ordres i, quan l'activitat ho requereix, amb l'execució des de la línia de comandes. Quan s'inclou una comprovació breu a la consola, s'indica què executa i quin resultat s'espera. Les captures i els exemples d'autocorrelació s'han calculat amb QGIS 3.44.11, libpysal 4.13.0 i esda 2.7.1; aquesta parella de biblioteques requereix Python 3.11 o posterior.

### Carpetes de treball i lliurament {#carpetes-practiques}

Cada pràctica parteix d'un paquet amb el `LLEGIU-ME.pdf` a l'arrel i les dades preparades a `data/`, incloent-hi el projecte `inici.qgz`. La pauta de treball separa les entrades, l'experimentació i la selecció final:

::: table "Funció de les carpetes dins de cada pràctica"
| Carpeta | Contingut i ús |
| --- | --- |
| `data/` | Dades i projecte d'inici, conservats com a referència |
| `sandbox/` | Còpia del projecte de treball, proves, intermedis i alternatives |
| `dist/` | Capes seleccionades, projecte final i documents que es lliuren |
:::

En preparar el lliurament es crea **un GeoPackage nou a `dist/`** i s'hi desen els vectors seleccionats. Els ràsters necessaris es conserven com a GeoTIFF, agrupats en una carpeta `rasters/` quan convé. El **projecte QGIS és un fitxer `.qgz` extern al GeoPackage**, desat amb rutes relatives. El lliurament inclou també l'informe en PDF i les evidències que demani l'activitat. Els fitxers descartats i les proves que no s'han utilitzat es queden a `sandbox/`; les dades de context imprescindibles per mostrar o revisar el resultat s'incorporen a la selecció final.

Els fitxers principals s'identifiquen amb el **codi de la pràctica, el tema i els cognoms**, amb el codi que estableixi l'enunciat. Per exemple:

```filetree
pr1-visibilitat-cognoms.qgz
pr1-visibilitat-cognoms.gpkg
pr1-visibilitat-cognoms.pdf
```

La carpeta `dist/` es pot reanomenar amb aquest mateix prefix i comprimir en un ZIP. L'elecció dels lliurables respon als apartats demanats i als resultats que s'han seleccionat.

Els grups del panell Capes ajuden a distingir **dades de partida, proves i resultats seleccionats**. Aquesta organització visual es complementa amb el desament dels fitxers: moure una capa a un grup no la copia a una altra carpeta. El projecte final conserva només les capes i els recursos necessaris, amb un ordre de dibuix, estils i etiquetes que permetin interpretar-los.

**El lliurament ha d'obrir-se i representar-se igual que a l'ordinador de treball.** Abans de lliurar-lo, copia la carpeta final en una ubicació diferent o descomprimeix el ZIP en una carpeta nova i obre'n el `.qgz`. Comprova que totes les capes són vàlides, que mantenen els estils, les etiquetes i l'ordre de dibuix i que el projecte no depèn de fitxers temporals o de proves que s'han quedat fora del paquet. El `.qgz` conserva la configuració, però necessita les dades i altres dependències que utilitza. Els fitxers `.batch` també requereixen revisar les seves rutes quan es canvia la ubicació del treball.

A mesura que avancis en el grau, pots recuperar una pregunta d'una altra assignatura, explorar un problema del teu entorn o provar una font de dades nova. Una tècnica estudiada per analitzar accessibilitat pot servir per comparar la cobertura d'un servei; un mètode d'interpolació pot donar peu a estudiar una altra variable ambiental, després de revisar-ne les condicions. Si un resultat sorprèn, contrastar-lo amb altres dades o discutir-ne la interpretació és una manera de continuar aprenent.

El manual acompanya l'assignatura obligatòria de tercer curs, amb codi `21234116`, impartida per Benito Zaragozí. Els enunciats vigents, els paquets de dades i les indicacions de lliurament es troben a Moodle; les condicions oficials de l'assignatura són a la guia docent. Els capítols enllacen també els catàlegs dels organismes productors per consultar les fonts o cercar dades d'altres territoris.
