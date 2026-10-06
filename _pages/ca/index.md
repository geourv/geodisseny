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

## Treballar amb els exemples i ampliar-los {#projecte-reproduible}

Els [fonaments del primer capítol]({{ site.baseurl }}/ca/chapters/fonaments-geodisseny/) serveixen de referència per als mètodes que es desenvolupen després. Els exemples petits permeten seguir les operacions; les aplicacions amb dades territorials mostren les decisions que comporta treballar amb observacions i cartografia. Les explicacions indiquen la procedència de les dades i els supòsits, de manera que es pugui revisar el càlcul i entendre'n els límits.

[QGIS](https://qgis.org/) és l'entorn principal dels procediments del manual, amb la versió 3.44 LTR com a referència documental. Les eines i els complements concrets es presenten quan intervenen en una anàlisi. Els conceptes també són útils per treballar amb altres programes o biblioteques de R i Python: en comparar implementacions, interessa comprovar que les dades, els paràmetres i les convencions de càlcul siguin equivalents.

>> **Preparació del programari.** Les pràctiques d'autocorrelació utilitzen el complement **Hotspot Analysis**, versió 4.0.0, i les biblioteques Python **libpysal** i **esda**, del projecte PySAL. No totes les instal·lacions de QGIS les incorporen. Abans d'aquelles pràctiques, segueix la [instal·lació i la prova des de QGIS]({{ site.baseurl }}/ca/chapters/dependencia-espacial/#preparacio-pysal): s'hi distingeixen Windows amb OSGeo4W, macOS i Linux. Instal·lar un paquet en un altre Python de l'ordinador no garanteix que QGIS el pugui utilitzar.

La preparació tècnica permet treballar després des dels diàlegs de Processament, sense haver de programar cada càlcul. Quan s'inclou una comprovació breu a la consola, s'indica què executa i quin resultat s'espera. Les captures i els exemples d'autocorrelació s'han calculat amb QGIS 3.44.11, libpysal 4.13.0 i esda 2.7.1; aquesta parella de biblioteques requereix Python 3.11 o posterior.

Guardar les fonts originals, les dades preparades i els resultats per separat facilita reprendre una anàlisi i compartir-la. Les notes sobre dates, unitats, sistemes de coordenades, transformacions i paràmetres expliquen les decisions preses. El projecte de QGIS conserva la configuració, però també necessita les capes i altres dependències que utilitza. Aquesta cura en l'organització permet aprofitar el treball en altres exercicis i assignatures.

A mesura que avancis en el grau, pots recuperar una pregunta d'una altra assignatura, explorar un problema del teu entorn o provar una font de dades nova. Una tècnica estudiada per analitzar accessibilitat pot servir per comparar la cobertura d'un servei; un mètode d'interpolació pot donar peu a estudiar una altra variable ambiental, després de revisar-ne les condicions. Si un resultat sorprèn, contrastar-lo amb altres dades o discutir-ne la interpretació és una manera de continuar aprenent.

El manual acompanya l'assignatura obligatòria de tercer curs, amb codi `21234116`, impartida per Benito Zaragozí. Els enunciats vigents, els paquets de dades i les indicacions de lliurament es troben a Moodle; les condicions oficials de l'assignatura són a la guia docent. Els capítols enllacen també els catàlegs dels organismes productors per consultar les fonts o cercar dades d'altres territoris.
