---
layout: manual-chapter
title: Connectivitat, accessibilitat i costos
description: Distàncies, connexions i costos per entendre per què un recorregut pot ser preferible a un altre.
lang: ca
ref: xarxes-rutes-accessibilitat
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/xarxes-accessibilitat/
weight: 20
part: Continguts
manual_references: true
---

Una escola pot ser molt a prop d'un barri i exigir una volta llarga si una via tancada els separa. Un camí curt pot costar més temps que una carretera una mica més llarga. La pregunta «a quina distància és?» necessita, per tant, alguns detalls: des d'on es parteix, on es vol arribar, per on es pot passar i què es vol reduir —metres, minuts o una altra dificultat.

El capítol comença comparant maneres de mesurar la separació. Després representa el moviment per trams connectats i per cel·les d'una graella. Els exemples permeten seguir com es calcula un recorregut i per què canvia quan es modifica un cost.

>>>>> En acabar el capítol, cal poder escollir i interpretar un model de recorregut.
>>>>>
>>>>> - Distingir separació en línia recta, longitud sobre el terreny i longitud de ruta.
>>>>> - Explicar nodes, arcs, sentits i impedàncies amb un exemple petit.
>>>>> - Relacionar fricció local i cost acumulat.
>>>>> - Llegir els paràmetres de ruta de QGIS i comprovar-ne el resultat.
>>>>> - Comparar alternatives mantenint clares les unitats i les condicions de pas.

## Distància i accessibilitat {#distancia-accessibilitat}

Un regle uneix dos punts sobre el mapa, però no sap si entre ells hi ha un riu, un edifici o una tanca. Aquesta mesura és útil: dona una primera referència de separació. Per descriure un desplaçament cal afegir-hi informació sobre els llocs per on es pot passar {% cite burrough1998principles %}.

Distància euclidiana
: Longitud del segment recte entre dos punts en un pla. També es pot dir distància en línia recta.

Distància de xarxa
: Longitud del recorregut més curt que permeten els trams i les connexions representats.

Cost de recorregut
: Suma de la dificultat dels passos o trams. Si es mesura en minuts, minimitzar-lo busca la ruta més ràpida; si es mesura en metres, busca la més curta.

Per a dos punts O i D amb coordenades en metres, el teorema de Pitàgores dona:

$$
d_E=\sqrt{(x_D-x_O)^2+(y_D-y_O)^2}.
\label{eq:euclidiana}
$$

Les diferències de coordenades són els dos costats perpendiculars d'un triangle. Si cal avançar 300 m cap a l'est i 400 m cap al nord, la diagonal mesura 500 m. Recórrer primer un costat i després l'altre del rectangle, en canvi, suma 700 m.

>> El **sistema de referència de coordenades**, o CRS, indica com s'interpreten les coordenades. Per als càlculs locals del capítol es treballa amb coordenades projectades en metres. La latitud i la longitud en graus no es poden introduir a la mateixa fórmula i interpretar el resultat com si fossin metres.

A distàncies grans també importa la forma de la Terra. Sobre una esfera, la ruta més curta per la superfície segueix un arc de cercle màxim: és una **ortodròmica**. Sobre l'el·lipsoide, una forma lleugerament aplanada que aproxima millor la Terra, es parla de **geodèsica**. Totes dues mesuren separació sobre una superfície de referència; encara no incorporen carreteres ni passos.

### Manhattan: avançar segons dos eixos {#distancia-manhattan}

Quan el moviment només és possible segons dos eixos perpendiculars, se sumen els desplaçaments en cadascun. Aquesta és la **distància Manhattan** o rectilínia:

$$
d_M=|x_D-x_O|+|y_D-y_O|.
\label{eq:manhattan}
$$

Les barres indiquen valor absolut: es compta la longitud sense que un signe negatiu la resti. En l'exemple, $300+400=700$ m. Fer diverses passes horitzontals i verticals també dona 700 m, sempre que no es retrocedeixi.

Una ciutat amb carrers en quadrícula ajuda a imaginar aquesta mesura. Però un carrer tallat o un sentit únic ja canvien les possibilitats de moviment. Manhattan no substitueix la informació d'una xarxa urbana completa. Tampoc és independent de l'orientació: girar els eixos de la graella pot canviar-ne el valor.

### Incorporar el relleu {#distancia-3d}

La **cota** és l'altura d'un punt respecte d'una referència. Si O és a cota 100 m i D a 220 m, el desnivell entre extrems és 120 m. La recta tridimensional incorpora aquesta diferència vertical:

$$
d_{3D}=\sqrt{d_E^2+(z_D-z_O)^2}.
\label{eq:distancia-3d}
$$

Amb 500 m de separació en planta i 120 m de desnivell, s'obtenen 514,2 m. Es continua unint només els dos extrems: el segment pot travessar l'interior d'un turó. Caminar per damunt del terreny exigeix seguir les pujades i baixades intermèdies.

![Moviment en planta, vista tridimensional d'un relleu i perfil del traçat amb mostres cada cinquanta metres]({{ site.baseurl }}/assets/quarto/figures/metriques-distancia.qmd "La recta plana mesura 500 m i el recorregut Manhattan, 700 m. La recta 3D uneix O i D en 514,2 m; seguir el perfil mostrejat del terreny suma 596,6 m. Els panells B i C mostren el mateix traçat i les mateixes cotes."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

La figura utilitza el relleu d'exemple següent. La primera fila dona la distància en planta, $d$; la segona, la cota, $z$. Totes dues s'expressen en metres. La distància es mesura sobre la projecció plana del traçat, no sobre les pujades.

::: table "Mostres del perfil O–D de la figura"
| $d$, m | 0 | 50 | 100 | 150 | 200 | 250 | 300 | 350 | 400 | 450 | 500 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $z$, m | 100 | 126 | 184 | 215 | 207 | 256 | 290 | 252 | 264 | 238 | 220 |
:::

>>> Entre les dues primeres mostres hi ha 50 m en planta i una pujada de 26 m. El tram inclinat mesura $\sqrt{50^2+26^2}\simeq56,4$ m. Repetir l'operació en els deu trams i sumar-los dona 596,6 m. Amb més mostres es podrien representar ondulacions més petites; la suma és una aproximació a la longitud sobre aquell traçat.

>>>> Longitud sobre el terreny, desnivell acumulat i temps a peu són coses diferents. Una pujada i una baixada de la mateixa longitud poden exigir esforços diferents. A més, algunes eines mesuren només en 2D encara que la capa contingui cotes Z: cal llegir què calcula el mòdul.

L'**accessibilitat** afegeix a la distància les oportunitats que es poden assolir. Ser a cinc minuts d'un equipament tancat no resol l'accés al servei. Horaris, capacitat, mitjà de transport i característiques de les persones també hi intervenen {% cite geurs2004accessibility %}.

## Distància euclidiana amb QGIS {#distancia-euclidiana-qgis}

### Les dades: dos costats de l'AP-7 a Vila-seca {#dades-distancies}

El Camí del Mas de la Plana permet comparar quatre maneres de relacionar dos punts propers: una recta vectorial, una distància ràster, una ruta per la xarxa i un camí sobre una superfície de cost. **O** és el punt de partida al costat sud del pas de l'autopista; **D** és un punt del camí al costat nord. Es conserven els mateixos extrems en els quatre càlculs.

El paquet de la pràctica inclou dades locals i projectes QGIS amb rutes relatives. Cal descomprimir-lo complet, obrir `projectes/00-inici.qgz` i desar les sortides pròpies en una carpeta `treball`. Les carpetes `dades` i `resultats` separen les entrades i els resultats de referència.

::: table "Dades del cas de Vila-seca i funció de cada capa"
| Dada | Procedència | Per a què serveix |
| --- | --- | --- |
| Ortofoto 2025, còpia a 1 m per píxel | ICGC | Reconèixer autopista, camins i edificacions |
| Eixos viaris 2024 | Referencial Topogràfic Territorial, ICGC | Preparar la xarxa de connexions |
| Edificis de Vila-seca | Cadastre INSPIRE | Excloure petjades edificades del model ràster |
| MDT de 5 m, LiDAR 2021–2023 | ICGC | Conèixer el relleu i preparar una ampliació amb pendent |
| O, D, bandes i corredors | Preparació de l'exercici | Fixar extrems i condicions de pas comparables |
:::

El pas **P2** es reconeix a l'ortofoto i correspon a una connexió cartografiada sota l'AP-7. Es simula tancar-lo i tornar-lo a obrir **en el model**. Això no modifica la separació en línia recta, però pot modificar els recorreguts i els llocs accessibles.

![QGIS mostra O i D sobre l'ortofoto de Vila-seca i destaca el corredor P2 sota l'AP-7]({{ site.baseurl }}/assets/captures/distancies-dades.png "O i D són els extrems de tots els càlculs. El requadre assenyala el pas P2 que es tanca o s'obre al model. L'ortofoto permet comprovar on són els camins i la infraestructura que els separa."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICGC, RTT 2024 i ortofoto 2025; punts i corredor de l'exercici."}

::: table "Coordenades dels extrems en ETRS89 / UTM 31N, EPSG:25831"
| Punt | Est, X, m | Nord, Y, m |
| --- | ---: | ---: |
| O | 344407,00 | 4553668,36 |
| D | 344473,01 | 4554030,72 |
:::

### Un segment vectorial entre O i D

L'eina **Shortest line between features**, `native:shortestline`, uneix les dues capes de punts. A *Source layer* es tria O; a *Destination layer*, D; es manté el mètode de distància al punt més proper i un únic veí. Amb un punt a cada capa, el resultat és el segment O–D {% cite qgisUserGuide %}.

![Diàleg de línia més curta amb Origen O i Destí D seleccionats]({{ site.baseurl }}/assets/captures/distancies-vector-parametres.png "La capa de partida conté O i la d'arribada conté D. L'eina calcula la separació recta entre geometries; encara no utilitza una xarxa ni una capa de barreres."){: data-figure-width-web="42rem" data-figure-width-pdf="100%"}

En la taula de sortida es pot llegir la distància. La comprovació amb les coordenades és $\sqrt{66,01^2+362,36^2}\simeq368,3$ m. Es treballa en metres i, per comparar les longituds planes de la pràctica, amb l'el·lipsoide del projecte a **Cap / NONE**.

![Segment discontinu entre O i D a QGIS, amb la distància de 368,3 metres destacada]({{ site.baseurl }}/assets/captures/distancies-vector-resultat.png "La recta uneix els punts en 368,3 m. Travessa la infraestructura perquè aquest càlcul només mesura separació: no busca per on es pot circular."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

### Una distància per a cada cel·la {#distancia-raster}

En un ràster es pot calcular la distància des d'O fins a totes les cel·les de l'àmbit. Primer es representa O en una graella: la cel·la que el conté rep valor **1** i les altres, **0**. Després es calcula la distància des del centre de cada cel·la al centre de la cel·la origen.

La graella de la pràctica té **340 × 340 cel·les de 5 m**, amb límits X 343600–345300 i Y 4553000–4554700. A **Rasteritza — vectorial a ràster**, `gdal:rasterize`, s'escull O com a entrada, valor fix 1, fons inicial 0, resolució 5 × 5 m i aquesta extensió. El zero és un fons vàlid; no s'ha de convertir tota la graella en origen.

L'eina **Proximitat — distància ràster**, `gdal:proximity`, rep aquest ràster, banda 1 i valor objectiu 1. La distància s'ha de demanar en **coordenades georeferenciades**: en EPSG:25831 són metres. L'altra opció compta píxels i donaria una magnitud diferent.

![Paràmetres de Proximitat GDAL amb origen de valor 1 i distància en coordenades georeferenciades]({{ site.baseurl }}/assets/captures/distancies-raster-parametres.png "El valor 1 identifica l'origen. Escollir coordenades georeferenciades fa que la distància s'expressi en metres; amb l'opció de píxels es comptarien cel·les."){: data-figure-width-web="42rem" data-figure-width-pdf="100%"}

Amb **Identifica els objectes** es pot consultar una cel·la. Per conservar el valor exacte a D, **Sample raster values**, `native:rastersampling`, afegeix el valor del ràster a la capa del destí. El resultat de la pràctica és aproximadament **370,7 m**.

![Ràster de distància euclidiana des d'O, amb D i el valor de 370,7 metres]({{ site.baseurl }}/assets/captures/distancies-raster-resultat.png "La distància creix des de la cel·la origen en totes les direccions. A D val 370,7 m. La banda de l'autopista no altera la superfície: continua sent una distància recta, no un cost de travessar el territori."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

>> **Per què no surt 368,3 m?** En vector s'utilitzen les coordenades originals. En ràster, O queda representat pel centre (344407,5; 4553667,5) m i D pel centre (344472,5; 4554032,5) m. La diferència d'uns 2,4 m prové d'aquesta representació en cel·les. No és una volta per evitar l'autopista.

## Representar les connexions amb una xarxa {#grafs}

Una xarxa es pot simplificar com una sèrie de punts units per trams. Els punts són **nodes**; els trams, **arcs**. El conjunt s'anomena **graf**. En una carretera, un node pot representar una cruïlla i un arc el tram fins a la cruïlla següent. La geometria ens diu on són i quina longitud tenen; la **topologia** ens diu quins estan connectats.

La figura conserva origen O, destinació D i barrera. El segment directe dona una referència de 600 m. A la xarxa hi ha diverses alternatives, però el moviment ha de seguir-ne els arcs. A la graella es pot avançar entre les cel·les admeses.

![Segment directe, xarxa amb recorreguts alternatius per damunt i per baix, graella i dos tipus d'encreuament]({{ site.baseurl }}/assets/quarto/figures/distancies.qmd "El blau identifica el recorregut escollit. La xarxa permet una ruta de 1.200 m per dalt i una de 1.400 m per baix. La graella ofereix un camí de 1.000 m afavorit per la franja de menor fricció. El segment discontinu serveix per comparar-los amb la separació directa de 600 m."){: data-figure-width-web="45rem" data-figure-width-pdf="100%"}

En la ruta superior, O–A, A–B i B–D mesuren 300, 600 i 300 m: en total, 1.200 m. La volta inferior és possible, però és més llarga. En la graella, en canvi, la franja inferior és barata de travessar i es pot assolir seguint cel·les que no coincideixen necessàriament amb carreteres. No s'està preguntant el mateix als dos models.

>>> Dues vies que es creuen en un pont no permeten necessàriament canviar de l'una a l'altra. En el quart panell, només la cruïlla amb node permet el gir. Tallar automàticament totes les línies que es creuen podria crear connexions inexistents.

Un graf és **dirigit** quan distingeix sentits de pas. Una carretera d'anada pot no ser utilitzable de tornada. També es poden assignar costos diferents a cada sentit, com passa quan pujar requereix més temps que baixar.

### Què és una impedància?

La **impedància** és el cost assignat a travessar un arc. El terme pot semblar abstracte, però en un model de temps és simplement el nombre de minuts del tram. Un pas lent, una espera o una obra poden augmentar-lo sense canviar la carretera dibuixada.

Si un recorregut P utilitza diversos arcs, el seu cost és la suma:

$$
C(P)=\sum_{e\in P}c_e.
\label{eq:cost-cami}
$$

$c_e$ és el cost de l'arc e. La fórmula es llegeix «sumar els costos de tots els trams del recorregut». Quan són minuts, el resultat són minuts. No es poden afegir-hi directament euros o pendents: un cost que combini magnituds diferents necessita una regla de conversió explicada.

### Per què canvia la ruta preferida? {#exemple-graf}

Considerem quatre ciutats imaginàries O, A, B i D. Els cinc trams són bidireccionals. Els nombres de la taula són temps de viatge, no distàncies del dibuix.

::: table "Temps dels trams en tres situacions, en minuts"
| Situació | O–A | O–B | B–A | A–D | B–D |
| --- | ---: | ---: | ---: | ---: | ---: |
| Inicial | 3 | 1 | 1 | 2 | 5 |
| Obres a B–A | 3 | 1 | 10 | 2 | 5 |
| Obres a B–A i retard al tram A–D | 3 | 1 | 10 | 6 | 5 |
:::

![Tres mapes de les mateixes ciutats i connexions amb costos diferents i rutes de quatre, cinc i sis minuts]({{ site.baseurl }}/assets/quarto/figures/impedancies-xarxa.qmd "Canvien els temps, no les ciutats ni les carreteres. Inicialment convé passar per B i A; les obres fan preferible el tram directe O–A; amb el segon retard, convé passar només per B. Els costos modificats es destaquen amb fons taronja."){: data-figure-width-web="48rem" data-figure-width-pdf="100%"}

En la primera situació, O–B–A–D suma $1+1+2=4$ minuts. O–A–D en suma 5 i O–B–D, 6. Si B–A passa a costar 10 minuts, el primer camí deixa de ser el millor: ara guanya O–A–D. Quan també augmenta A–D, la ruta O–B–D esdevé preferible. «La millor ruta» sempre vol dir **la millor segons els costos introduïts**.

L'algorisme de **Dijkstra** organitza aquesta comparació quan els costos no són negatius {% cite dijkstra1959graphs %}. Comença per l'origen i conserva el menor cost conegut d'arribar a cada node. En el primer cas, el tram directe O–A costa 3; després de passar per B es descobreix una alternativa d'1+1=2. El cost conegut del node A s'actualitza, i continuar fins a D dona 4. Així no cal triar a ull el tram que sembla apuntar millor cap al destí.

>> Un cost alt encara permet passar. Un pas prohibit s'ha de tancar en el model. Aquesta distinció reapareixerà amb les barreres del ràster.

### Connexions i tolerància

Una **tolerància** és la separació màxima que s'accepta per considerar que dos extrems representen el mateix node. Pot resoldre una petita desconnexió de coordenades, però també pot unir dues calçades que no tenen pas entre elles si és massa gran. Primer s'inspecciona el lloc i després es decideix la tolerància.

Un **component connectat** és una part de la xarxa dins de la qual es pot anar d'un node a un altre. Dos punts poden estar propers i pertànyer a components diferents. Un resultat sense ruta pot reflectir aquesta desconnexió; no és sempre una fallada del programa.

## Calcular una ruta amb QGIS {#procediment-xarxes}

L'eina **Camí més curt — punt a punt**, de la Caixa d'eines de processament, permet escollir entre longitud mínima i temps mínim. El seu identificador és `native:shortestpathpointtopoint`. La primera opció utilitza longituds; la segona les divideix per velocitats per estimar temps {% cite qgisUserGuide %}.

### Seguir el Camí del Mas de la Plana {#cas-xarxa-icgc}

El [Referencial Topogràfic Territorial de l'ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial) proporciona els eixos viaris de l'exemple. El paquet conserva l'extracte original i una xarxa de treball de **189 parts d'eix**. Els eixos d'autopista no hi entren com a vies de circulació: es vol estudiar com connecten els altres trams a través dels passos.

La cartografia s'ha preparat per al càlcul dividint alguns eixos on un extrem contacta amb l'interior d'un altre. No s'han convertit en cruïlles tots els creuaments del dibuix. Aquesta preparació queda documentada perquè una capa de línies no és automàticament una xarxa completa de navegació.

S'utilitzen els mateixos O i D de la distància euclidiana. A **Camí més curt — punt a punt** es tria la xarxa oberta i el criteri **Més curt**. Les coordenades es poden copiar amb punt decimal: `344407,4553668.36 [EPSG:25831]` per a O i `344473.01,4554030.72 [EPSG:25831]` per a D.

::: table "Paràmetres que donen significat a la ruta de l'exemple"
| Paràmetre de QGIS | Valor inicial | Significat |
| --- | --- | --- |
| Capa de xarxa | `xarxa-oberta.gpkg` | Trams del model amb P2 disponible |
| Tipus de camí | Més curt | Es minimitzen metres |
| Origen i destinació | Coordenades indicades | Extrems del recorregut |
| Direcció per defecte | Ambdós sentits | Supòsit inicial de pas |
| Tolerància topològica | 0 m | No s'uneixen extrems separats |
| Distància màxima del punt a la xarxa | 0,1 m | Els extrems proporcionats ja són sobre els eixos |
:::

![Diàleg de Camí més curt amb les coordenades exactes d'O i D i la xarxa oberta]({{ site.baseurl }}/assets/captures/distancies-xarxa-parametres.png "El diàleg fixa la xarxa, el criteri de longitud i els dos extrems. Utilitzar les coordenades proporcionades evita començar en un tram diferent del que es vol estudiar."){: data-figure-width-web="42rem" data-figure-width-pdf="100%"}

La ruta oberta fa **454,1 m**. És més llarga que la recta de 368,3 m perquè segueix les connexions representades. A la captura es veuen els extrems, el recorregut i el lloc on travessa l'autopista a diferent nivell.

![Ruta blava per la xarxa i recta discontínua entre els mateixos O i D, amb el pas P2 enquadrat]({{ site.baseurl }}/assets/captures/distancies-xarxa-resultat.png "La línia blava segueix la xarxa i utilitza P2; la discontínua només uneix O amb D. El recorregut de xarxa fa 454,1 m. El pas no és una entrada a l'autopista: connecta els eixos situats als seus dos costats."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

La capa `xarxa-tancada.gpkg` retira el tram `rtt_id = 1354754`. Amb aquesta entrada el mòdul retorna **sense ruta**: O queda en un tram que no té una segona connexió amb D dins de la xarxa seleccionada. És un resultat sobre les dades preparades; no demostra que l'ortofoto no contingui altres vials o connexions no recollits.

>> **Sense ruta no vol dir zero metres.** Conserva aquest resultat i explica quina connexió falta. Augmentar una tolerància a cegues pot unir línies que no s'haurien d'unir; primer s'inspeccionen les dades i el lloc.

Per calcular temps s'utilitza **Més ràpid** i el camp `v_kmh`, que aquí val **5 km/h** a tots els trams com a supòsit docent. La ruta oberta dona 0,09082 hores, aproximadament **5,45 minuts**. El camp de velocitat espera km/h; el cost retornat per aquesta estratègia és en hores.

### Un sentit únic no és una restricció de gir {#restriccions-gir}

En un encreuament pot estar prohibit girar a l'esquerra des d'un carrer, mentre es permet continuar recte des del carrer oposat. El tram de sortida continua obert. La restricció depèn de **quin tram s'ha recorregut abans d'arribar al node**, no només del sentit permès al tram següent.

![El mateix encreuament amb la maniobra a cap a b prohibida i el pas c cap a b permès]({{ site.baseurl }}/assets/quarto/figures/restriccions-gir.qmd "En aquest exemple fictici, arribar per a no permet continuar per b. Arribar per c sí que ho permet. Tancar b o canviar-ne el sentit eliminaria també un moviment que hauria de continuar disponible."){: data-figure-width-web="48rem" data-figure-width-pdf="100%"}

Les eines **natives** de QGIS 3.44 utilitzades aquí admeten sentits, velocitats i toleràncies, però no una taula de maniobres prohibides o penalitzades. Les opcions avançades inclouen aquests dos camps {% cite qgisUserGuide %}:

- **Camp de direcció**, `DIRECTION_FIELD`: sentit de cada arc.
- **Camp de velocitat**, `SPEED_FIELD`: velocitat del tram.

Cap dels dos expressa la combinació «arribar per a i sortir per b».

![Eina nativa de ruta amb la xarxa oberta i el criteri Més ràpid seleccionat]({{ site.baseurl }}/assets/captures/xarxa-girs-parametres.png "Més ràpid minimitza el temps calculat amb longituds i velocitats. En aquesta pràctica els sentits i la velocitat es configuren a les opcions avançades. Aquest motor natiu no incorpora una taula de restriccions de gir."){: data-figure-width-web="42rem" data-figure-width-pdf="90%"}

Una **penalització de gir** afegeix temps a una maniobra, com una espera per travessar una cruïlla; una prohibició l'exclou. Per representar-les cal un motor que les admeti i una xarxa preparada amb identificadors dels trams d'entrada i sortida. Hi ha solucions especialitzades, com les funcions de [rutes amb restriccions de pgRouting](https://docs.pgrouting.org/3.8/en/TRSP-family.html), que requereixen preparació i verificació pròpies. Obrir les dades a QGIS no les activa automàticament.

>>>> Crear un camp anomenat «gir» no fa que l'eina nativa l'utilitzi. Les rutes i les àrees de servei d'aquest exemple descriuen els costos i els sentits configurats, sense restriccions de maniobra ni temps d'espera a les cruïlles.

## Àrees de servei i taules origen–destinació {#arees-servei}

Una **àrea de servei** indica quins llocs es poden assolir abans de superar un cost. Amb un límit de deu minuts, per exemple, s'inclouen els trams de xarxa on es pot arribar dins d'aquest temps. QGIS ofereix **Àrea de servei — des d'un punt**, `native:serviceareafrompoint`. El resultat en línies mostra els trams accessibles; un polígon que els embolcalli no garanteix que tots els espais interiors siguin transitables.

En el cas de Vila-seca es calculen franges de **3, 6 i 12 minuts** des d'O, amb el mateix camp de velocitat. A la versió de QGIS utilitzada, el paràmetre *Travel cost* espera hores: s'hi introdueixen **0,05, 0,10 i 0,20**, respectivament. A la captura s'utilitza punt decimal, `0.20`, per als dotze minuts.

![Àrea de servei configurada amb la xarxa oberta, O, criteri Més ràpid i cost 0,20 hores]({{ site.baseurl }}/assets/captures/distancies-isocrones-parametres.png "Dotze minuts són 0,20 hores. La mateixa conversió s'aplica als altres límits. El camp de velocitat de l'exercici val 5 km/h; canviar-lo també canviaria l'abast."){: data-figure-width-web="42rem" data-figure-width-pdf="100%"}

![Trams accessibles en 3, 6 i 12 minuts i petit tram accessible amb P2 tancat, sobre l'ortofoto]({{ site.baseurl }}/assets/captures/distancies-isocrones-resultat.png "Blau, verd i taronja indiquen trams accessibles amb P2 obert. D queda fora dels 3 minuts i dins dels 6. En vermell es veu l'abast amb el pas tancat. Són franges sobre la xarxa, no àrees contínues que permetin passar per qualsevol camp."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

La longitud de totes les branques accessibles pot ser superior a la distància que recorre una sola persona en aquell temps. Cada branca s'avalua des d'O; no se sumen totes com si fossin un únic itinerari.

### Llegir un mapa de temps d'accés

Per comparar escenaris, convé conservar l'extensió, els colors i els límits de temps. El mapa següent reserva el blau per als primers 3 minuts, el verd per als trams assolits entre 3 i 6, i el taronja per als assolits entre 6 i 12. Cada porció de línia té un sol color; els límits inclouen els valors 3, 6 i 12 en la franja anterior.

![Dos mapes de la mateixa xarxa amb franges temporals disjuntes i el pas P2 obert o tancat]({{ site.baseurl }}/assets/quarto/figures/isocrones-xarxa.qmd "Amb P2 obert, D queda a la franja de més de 3 i fins a 6 minuts. Amb P2 tancat, l'origen només connecta amb 68,4 m de xarxa: augmentar el límit de 3 a 12 minuts no permet sortir d'aquest component. La banda grisa situa l'AP-7; les línies fines mostren altres eixos."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Font: eixos RTT 2024, ICGC; sentits i velocitat de l'exercici."}

En QGIS es pot obtenir aquesta lectura superposant les sortides de 12, 6 i 3 minuts, amb la més curta al damunt. El paquet inclou també dues capes amb porcions disjuntes i un camp de classe:

- `franges-xarxa-obert.gpkg`: connexions amb P2 disponible.
- `franges-xarxa-tancat.gpkg`: connexions amb P2 retirat.

Totes dues representacions descriuen **trams accessibles**, no tot l'espai entre carreteres.

>> Un polígon que embolcalli les línies, o un buffer al seu voltant, pot ajudar a presentar un mapa, però no acredita que es pugui caminar per qualsevol punt interior. Les superfícies temporals requereixen un model explícit de moviment fora de la xarxa.

### Resumir diversos orígens i destinacions

Quan hi ha diversos orígens i destinacions, els costos es poden ordenar en una **matriu**, és a dir, una taula: files per als orígens i columnes per a les destinacions. El mínim de cada fila identifica la destinació menys costosa. Comptar quants valors són inferiors a deu minuts respon una altra pregunta: quantes alternatives són accessibles.

>>> Un barri arriba a tres equipaments en 4, 7 i 12 minuts. Té dues opcions dins de deu minuts. Un altre barri és a sis minuts d'un únic equipament. No n'hi ha prou amb dir que tots dos tenen un servei proper: difereixen en el nombre d'alternatives. Una destinació inaccessible s'anota com a tal, no amb zero minuts.

## Fricció local i cost acumulat {#superficies-cost}

Fora d'una xarxa explícita, es pot dividir el terreny en cel·les i assignar una dificultat a cadascuna. Aquesta dificultat és la **fricció**. Un sòl fàcil de travessar rep un valor baix i un de difícil, un valor alt. El **cost acumulat** d'una cel·la, en canvi, és el menor cost de tots els camins que hi arriben des de l'origen.

>> La fricció descriu el lloc; el cost acumulat descriu com s'hi arriba. Una cel·la fàcil de travessar pot tenir un cost acumulat alt si és lluny de l'origen o està envoltada d'obstacles.

Si $f_i$ i $f_j$ són friccions per metre de dues cel·les veïnes i $d_{ij}$ és la longitud del pas, una regla possible és:

$$
c_{ij}=\frac{f_i+f_j}{2}\,d_{ij}.
\label{eq:cost-pas}
$$

Primer es fa la mitjana de les dues friccions i després es multiplica per la distància recorreguda. A la graella inicial, un pas de 100 m entre valors 4 costa 400 unitats. Entre 4 i 0,5 costa 225; entre dos valors 0,5 costa 50. La ruta té dos passos cars, dos de transició i sis de barats: $2\times400+2\times225+6\times50=1550$ unitats. La longitud continua sent 1.000 m.

### Quatre o vuit veïns

Amb quatre veïns només es comparteix moviment pels costats. Amb vuit també es permeten diagonals. En una cel·la de 100 m, el pas diagonal mesura $100\sqrt{2}\simeq141,4$ m, no 100. Aquesta decisió explica que un camí calculat sobre cel·les pugui tenir petites ziga-zagues.

GRASS **r.cost**, disponible a Processament quan el proveïdor està instal·lat, calcula costos acumulats {% cite grassRCost %}. Interpreta el cost de travessar cel·les i ajusta les diagonals. Per reproduir una fricció per metre cal convertir-la segons la mida de cel·la: amb cel·les de 5 m, una fricció 1 per metre correspon a 5 unitats de travessa ortogonal. El mapa de direccions de retorn permet reconstruir després el camí amb **r.path**.

### Veure la superfície i obrir el pas de l'AP-7 {#cost-ap7}

En el model ràster de Vila-seca, les cel·les dels camins tenen fricció **1** i la resta del terreny admès, **4**. La banda de l'autopista i els edificis són **NoData**, exclosos del pas. Els corredors que es mantenen oberts connecten els dos costats; P2 es pot activar o tancar sense canviar O ni D.

La banda s'ha construït amb un buffer de 25 m dels eixos de l'AP-7, i els corredors de pas tenen 20 m d'amplada al model. Aquests valors defineixen l'experiment; no són mesures de la plataforma ni de la capacitat del pas. Els ràsters comparteixen extensió, CRS i cel·les de 5 m.

![Ràster de fricció amb camins clars de valor 1, terreny de valor 4 i barreres de l'autopista i els edificis]({{ site.baseurl }}/assets/captures/distancies-friccio.png "Aquesta és l'entrada del model de cost: les cel·les clares valen 1 i les ocres, 4. L'autopista i els edificis queden exclosos. El requadre assenyala P2 tancat; en l'altre escenari es restitueix un corredor de cel·les transitables."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

>> **Altitud i fricció no són el mateix.** El MDT guarda elevacions en metres. Aquesta fricció guarda resistències relatives. En el model principal no se sumen les altituds a cap penalització; el pendent es conserva com una possible ampliació diferenciada.

Per executar **r.cost**, primer es multiplica la fricció per 5 amb la Calculadora ràster: els costos de travessa ortogonal són 5 i 20. Es conserva la mateixa graella i els NoData. Després s'introdueix O com a capa de punts d'inici, es deixa sense definir el cost dels nuls i no s'activa el moviment de cavall. Es desen **cost acumulat** i **direccions de moviment**.

![Paràmetres de r.cost amb cost per cel·la, origen O i nuls exclosos]({{ site.baseurl }}/assets/captures/distancies-cost-parametres.png "r.cost rep el cost de travessar una cel·la i comença a O. Els camps d'aturada queden buits per obtenir tota la superfície accessible. Les cel·les NoData no reben un cost finit que permeti travessar-les."){: data-figure-width-web="42rem" data-figure-width-pdf="100%"}

Per reconstruir el camí s'utilitza **r.path** amb el ràster de **direccions**, format en graus, i **D** com a punt de partida. La funció segueix les direccions de retorn fins a O. Introduir el cost acumulat en lloc de les direccions seria una entrada diferent de la que espera l'eina.

![Diàleg de r.path amb el ràster de direccions i Destí D com a punt de reconstrucció]({{ site.baseurl }}/assets/captures/distancies-path-parametres.png "A r.path es comença a D per reconstruir el recorregut cap a O. Les direccions provenen del càlcul anterior de r.cost. La sortida vectorial permet dibuixar i mesurar el camí."){: data-figure-width-web="42rem" data-figure-width-pdf="100%"}

![Cost acumulat amb P2 obert, ruta blava pel pas i ruta taronja corresponent al pas tancat]({{ site.baseurl }}/assets/captures/distancies-cost-resultat.png "El fons és el cost acumulat amb P2 obert. La ruta blava utilitza aquest pas; la taronja correspon a P2 tancat i busca un altre corredor. Es mantenen els mateixos O i D. Els colors del ràster són costos, no elevacions."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

::: table "Longitud i cost dels camins ràster de Vila-seca"
| Escenari | Longitud del camí | Cost acumulat a D |
| --- | ---: | ---: |
| P2 obert | 470,6 m | 470,6 m ponderats |
| P2 tancat | 1.135,8 m | 2.217,7 m ponderats |
:::

Amb P2 obert el camí segueix cel·les de fricció 1; per això longitud i cost coincideixen numèricament. Amb P2 tancat es passa també per cel·les més cares. El ràster encara permet arribar a D perquè admet travessar terreny fora dels eixos amb cost 4. La xarxa seleccionada, en canvi, només permetia seguir-ne els arcs i havia quedat desconnectada.

### Fer més costós el pas per un solar {#cas-cost-pineda}

Al nord de la Pineda, la parcel·la `7713904CF4571D` permet comparar travessar i vorejar una mateixa peça. La base és la [cartografia cadastral](https://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels/43/ES.SDGC.CP.atom_43.xml) i l'[ortofoto ICGC de 2025](https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?SERVICE=WMS&REQUEST=GetCapabilities). L'àrea geomètrica és d'uns 8,71 ha.

Es manté una graella de 5 m, vuit veïns i els mateixos extrems. Primer es posa fricció 1 a tot arreu. Després es canvia només l'interior de la parcel·la a 20. L'objectiu és entendre l'efecte d'aquesta penalització, sense afegir encara pendent, vegetació o tanques.

![Dos recorreguts sobre ortofoto, amb el contorn de la parcel·la i els extrems O i D]({{ site.baseurl }}/assets/quarto/figures/accessibilitat-territorial.qmd "Amb fricció uniforme, el camí de 608,3 m travessa la parcel·la. En encarir-ne l'interior, el camí de 724,3 m la voreja. La base aèria permet situar el càlcul entre els vials i els espais de l'entorn."){: data-figure-width-web="48rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ortofoto ICGC 2025 i parcel·lari de la Dirección General del Catastro."}

Els punts sol·licitats són O=(347.300;4.551.050) m i D=(347.900;4.551.030) m; el camí es calcula entre els centres de les cel·les corresponents. Les capes de fricció i de cost acumulat permeten repetir el càlcul a QGIS. Un altre programa pot triar un camí equivalent si hi ha empats, però ha de respectar els mateixos costos i regles de moviment.

La captura següent mostra el ràster utilitzat: dos valors, **1** i **20**. La superfície plana de color no és un MDT al qual s'hagin afegit nombres. El MDT és una altra capa del paquet, que en aquest experiment no intervé en el càlcul.

![QGIS mostra el ràster de fricció 1 a l'exterior i 20 dins de la parcel·la de la Pineda, amb els dos recorreguts]({{ site.baseurl }}/assets/captures/distancies-pineda-friccio.png "El color clar representa fricció 1 i el taronja, fricció 20. El camí discontinu travessa la parcel·la amb cost uniforme; el blau correspon a la penalització interior. O, D, els valors de les cel·les i les longituds es poden llegir al mateix projecte."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

![Cost acumulat des d'O a la Pineda, amb el camí que voreja la parcel·la de fricció alta]({{ site.baseurl }}/assets/captures/distancies-pineda-cost.png "El cost acumulat és baix prop d'O i creix en arribar a altres cel·les. Dins de la parcel·la augmenta ràpidament perquè travessar cada cel·la és més car. El camí blau minimitza aquest cost; la superfície acolorida no representa altura."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

>>> La fricció 20 no tanca la parcel·la. Si totes les alternatives fossin encara més cares, podria continuar sent preferible travessar-la. Per representar una prohibició de pas caldria una **barrera estricta**, exclosa del càlcul, i no una penalització finita.

Una dada desconeguda tampoc és automàticament una barrera. Una **màscara** és una capa que marca on s'aplica una condició; convé separar la màscara de pas prohibit de la manca de cobertura. També cal comprovar que una cel·la massa grossa no faci desaparèixer un pont o un pas estret.

## Temps de marxa amb relleu: r.walk {#marxa-anisotropa}

Recórrer un camí de pujada i tornar pel mateix camí no exigeix necessàriament el mateix temps. Un cost **isòtrop** no canvia en invertir el sentit d'un pas entre dues cel·les. Un cost **anisòtrop** sí que pot canviar. Un ràster calculat multiplicant la fricció pel pendent local continuaria sent isòtrop si assignés el mateix cost a pujar i baixar entre les mateixes cel·les.

GRASS **r.walk** utilitza les altituds de l'MDT per calcular el desnivell amb signe entre cel·les veïnes. Distingeix pujada, baixada moderada i baixada forta; a més, admet una fricció que representa dificultats addicionals {% cite grassRWalk %}. L'entrada de relleu és l'**MDT en metres**, no un mapa de graus de pendent.

### Un perfil petit per entendre la direcció

En un exemple construït amb 100 m horitzontals i 10 m de desnivell, els coeficients per defecte assignen 0,72 s a cada metre horitzontal i 6 s addicionals a cada metre de pujada. Sense fricció addicional, pujar costa $0,72\times100+6\times10=132$ s. En baixar aquest pendent moderat, el model resta aproximadament 2 s per metre de descens: uns 52 s en total.

![Perfil esquemàtic de cent metres horitzontals i deu de desnivell, recorregut en els dos sentits]({{ site.baseurl }}/assets/quarto/figures/anisotropia-pendent.qmd "El mateix perfil dona 132 s de pujada i aproximadament 52 s de baixada amb els coeficients de r.walk i fricció addicional zero. Són temps del model per a un exemple construït; l'escala vertical del dibuix està exagerada."){: data-figure-width-web="48rem" data-figure-width-pdf="100%"}

La regla no diu que baixar sempre sigui millor. El coeficient canvia quan la baixada supera el llindar −0,2125 m/m, aproximadament −12°: el descens fort afegeix cost. Els coeficients per defecte són `0.72,6.0,1.9998,-1.9998`, en l'ordre horitzontal, pujada, baixada moderada i baixada forta. Són una regla de marxa, no una velocitat observada de cada persona.

### Entrades i unitats del model de Vila-seca

Es mantenen O, D, els passos i la graella de 5 m. L'MDT ICGC dona 50,887 m a la cel·la d'O i 52,249 m a la de D. El programa utilitza també els desnivells intermedis: conèixer només aquestes dues cotes no és suficient per calcular el temps.

La nova fricció val **0 s/m als camins** i **0,5 s/m a la resta del terreny admès**. És temps addicional per metre: zero no fa que el moviment sigui instantani, perquè el temps de marxa ja el calcula r.walk. L'autopista i els edificis conserven NoData fora dels corredors admesos.

::: table "Entrades de r.walk en el cas de Vila-seca"
| Entrada | Valor | Interpretació |
| --- | --- | --- |
| Elevació | MDT de 5 m | Altitud en metres |
| Fricció addicional | 0 o 0,5 s/m | Temps afegit per camins o resta admesa |
| Punts d'inici | O per a l'anada; D per a la tornada | Origen de cada superfície |
| Lambda | 1 | Multiplicador de la fricció addicional |
| Coeficients de marxa | Valors per defecte | Regla horitzontal i de desnivell |
| Moviment | Vuit veïns | Sense moviment de cavall |
| Regió i resolució | Graella comuna de 5 m | Mateixa extensió que la pràctica |
:::

A Processament, l'eina és **r.walk.points**, identificador `grass:r.walk.points` en aquesta instal·lació. S'hi trien l'MDT, la fricció de marxa i O. Es deixa buit el cost dels nuls i els punts d'aturada; es desen el temps acumulat i les direccions.

![Diàleg de r.walk.points amb l'MDT, la fricció temporal i O com a punt d'inici]({{ site.baseurl }}/assets/captures/rwalk-parametres.png "L'MDT aporta altituds en metres i la fricció aporta segons addicionals per metre. La sortida de r.walk és en segons. Els coeficients i el llindar de pendent es mantenen explícits al diàleg."){: data-figure-width-web="42rem" data-figure-width-pdf="90%"}

>>>> La fricció 1/4 de r.cost expressava resistència relativa; no és la nova fricció temporal. A r.walk no s'introdueixen aquests pesos com si fossin segons, ni es multiplica la fricció temporal per 5: l'eina ja té en compte la distància entre cel·les.

### Comparar anada i tornada

Amb el temps en segons, dividir per 60 amb la Calculadora ràster produeix un mapa en minuts. Per recuperar O→D, **r.path** utilitza les direccions de la superfície iniciada a O i D com a punt de reconstrucció. Per estudiar D→O, es torna a executar r.walk des de D i després r.path des d'O. Invertir només la geometria de la línia no recalcula el temps de tornada.

![Mapa del temps de marxa des d'O amb els camins d'anada i tornada i el valor a D]({{ site.baseurl }}/assets/captures/rwalk-resultat.png "Amb P2 obert, arribar d'O a D costa 6,63 min en el model; tornar de D a O costa 6,48 min. Les línies són molt semblants, però provenen de dos càlculs. El fons representa només el temps acumulat des d'O."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

::: table "Temps i longitud del model de marxa de Vila-seca"
| Superfície i escenari | O→D | D→O | Longitud del camí O→D |
| --- | ---: | ---: | ---: |
| Terreny pla de control, P2 obert | 5,64 min | 5,64 min | 466,5 m |
| MDT, P2 obert | 6,63 min | 6,48 min | 466,5 m |
| MDT, P2 tancat | 17,49 min | No calculat en aquesta prova | 1.071,5 m |
:::

El control pla posa totes les altituds a zero, mantenint la fricció temporal i les barreres. Així es comprova que, sense desnivells, invertir els extrems dona el mateix temps. Amb l'MDT, l'anada i la tornada difereixen, encara que en aquest cas les longituds arrodonides coincideixin.

>> Un MDT de 5 m simplifica els passos a diferent nivell: pot no representar el perfil real d'un camí sota una infraestructura. Aquest experiment utilitza el relleu i els corredors declarats, sense calibració amb trajectes observats. Abans d'estimar temps per a una aplicació real, caldria revisar especialment aquests punts.

## Isòcrones sobre la superfície de marxa {#isocrones-marxa}

Una **isòcrona** uneix llocs amb el mateix temps mínim d'accés des d'un origen. En el mapa de r.walk, els contorns de 3, 6 i 12 minuts delimiten franges que es poden representar amb colors. Ara hi ha una superfície temporal: les cel·les fora dels camins també tenen una regla de pas i les barreres queden excloses.

Primer es converteix la sortida de segons a minuts. A **r.contour**, `grass:r.contour`, s'utilitza aquest ràster i la llista de nivells `3,6,12`, deixant sense definir l'increment regular. En aquesta pràctica es conserven línies amb almenys 3 punts, per evitar petits contorns degenerats. Aquesta selecció només afecta les línies de representació, no els temps de la graella.

![Diàleg de r.contour amb el ràster de minuts i els nivells 3, 6 i 12]({{ site.baseurl }}/assets/captures/rwalk-contorns.png "Els nivells prenen la unitat del ràster d'entrada. Amb una entrada en minuts, 3,6,12 produeix aquests tres contorns temporals. Si s'utilitzessin directament segons, els nivells equivalents serien 180,360,720."){: data-figure-width-web="42rem" data-figure-width-pdf="90%"}

Per omplir les franges, es classifica el ràster en 0–3, més de 3–6, més de 6–12 i més de 12 minuts. Els NoData es conserven. Les superfícies accessibles es compten sobre les cel·les de temps, no mesurant un polígon dibuixat a ull al voltant dels contorns.

![Dos mapes de franges de marxa amb les mateixes classes, límits i barreres, comparant P2 obert i tancat]({{ site.baseurl }}/assets/quarto/figures/isocrones-rwalk.qmd "Amb el pas obert, D queda entre 6 i 12 minuts; amb el pas tancat, queda fora dels 12. La superfície assolible fins a 12 minuts passa de 91,9 a 55,4 ha dins d'aquest model. El gris de les barreres es distingeix del gris clar dels temps superiors a 12 minuts."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Font: MDT ICGC, eixos RTT i edificis cadastrals; friccions i passos de l'exercici."}

::: subfigures a/b "Comparació de les isòcrones a QGIS, amb la mateixa extensió"
![QGIS mostra les franges i els contorns amb P2 obert]({{ site.baseurl }}/assets/captures/rwalk-isocrones-obert.png "P2 obert: D és a la franja de més de 6 i fins a 12 minuts."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}
![QGIS mostra les franges i els contorns amb P2 tancat]({{ site.baseurl }}/assets/captures/rwalk-isocrones-tancat.png "P2 tancat: arribar a D requereix 17,49 minuts, fora de les franges acolorides."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}
:::

La xarxa a 5 km/h situava D dins dels 6 minuts; el model de marxa amb relleu l'hi deixa fora. La discrepància respon a entrades i regles diferents, no a un canvi de color. En tots dos casos s'estudia sortir d'O: una superfície anisòtropa des d'O tampoc descriu automàticament el temps de tornar-hi des de qualsevol lloc.

## Accessos i connexions en una proposta territorial {#cas-accessos}

Per a un hort solar cal distingir accés de vehicles i connexió elèctrica. El primer segueix vies i necessita considerar amplada, alçada de pas —el **gàlib**—, pendent i girs. La segona pot requerir un corredor de cable, excavació i encreuaments. La proximitat a una autovia no identifica una entrada; la proximitat a una línia elèctrica no informa de la capacitat de connexió.

El punt d'un consumidor publicat per l'ICAEN tampoc és necessàriament una porta d'accés {% cite icaenLocalitzacio %}. Cal situar l'entrada de la proposta i connectar-la amb el tram adequat. Les línies d'expedients de l'Hipermapa ajuden a estudiar traçats de projectes, però no representen tota la xarxa elèctrica en servei.

Canviar un cost, un sentit o un extrem i comparar la resposta és una **anàlisi de sensibilitat**. Si un canvi petit altera molt la ruta, aquella dada mereix una comprovació més detallada. El resultat útil per al geodisseny és explicar on apareix una dificultat i com una alternativa la resol, no només dibuixar una línia òptima.

## Activitats {#activitats-distancies}

### Comparar les dues distàncies euclidianes

Amb les dades de la pràctica, conserva aquests dos punts en EPSG:25831:

::: table "Coordenades per a l'activitat de distància euclidiana"
| Punt | Est, X, m | Nord, Y, m |
| --- | ---: | ---: |
| O | 344407,00 | 4553668,36 |
| D | 344473,01 | 4554030,72 |
:::

Calcula el segment vectorial i un ràster de proximitat amb cel·les de 5 m, sobre l'extensió X 343600–345300 i Y 4553000–4554700. Desa la línia, el ràster d'origen 0/1 i el de distància.

Comprova els valors aproximats de 368,3 m i 370,7 m. Explica per què no coincideixen exactament i per què cap dels dos càlculs sap si P2 està obert. Conserva el valor del ràster mostrejat a D, no només una captura amb el color de la cel·la.

### Seguir els tres escenaris de ciutats

En una xarxa fictícia bidireccional, suma els temps dels camins O–A–D, O–B–D i O–B–A–D amb aquestes dades. Són minuts, no longituds del dibuix.

::: table "Dades per a l'activitat de canvi de costos"
| Situació | O–A | O–B | B–A | A–D | B–D |
| --- | ---: | ---: | ---: | ---: | ---: |
| Inicial | 3 | 1 | 1 | 2 | 5 |
| Primer canvi | 3 | 1 | 10 | 2 | 5 |
| Segon canvi | 3 | 1 | 10 | 6 | 5 |
:::

Identifica el camí preferit en cada fila i conserva la taula de sumes: els mínims han de ser 4, 5 i 6 minuts. Proposa després un únic canvi que faci empatar dues alternatives i explica què podria retornar el programa.

### Obrir i tancar P2 a QGIS

Calcula una ruta amb cadascuna de les dues xarxes, mantenint els mateixos extrems i paràmetres:

- `xarxa-oberta.gpkg`: el pas P2 està disponible.
- `xarxa-tancada.gpkg`: s'ha retirat el tram del pas.

Conserva les capes d'entrada i la sortida que existeixi. Identifica el tram retirat, `rtt_id = 1354754`, i explica per què la segona prova no dona ruta dins del graf seleccionat.

Calcula els trams accessibles en 3, 6 i 12 minuts a 5 km/h amb el pas obert; compara els 6 minuts amb el pas tancat. Desa les sortides en línies i presenta un mapa amb O, D, P2 i llegenda. La fitxa ha de distingir hores introduïdes al paràmetre, minuts representats al mapa i metres de longitud.

### Distingir fricció, cost acumulat i camí

Repeteix `r.cost` i `r.path` amb les friccions oberta i tancada de Vila-seca. Conserva les entrades, els costos per cel·la, els costos acumulats, les direccions i els camins. Una taula ha d'indicar per a cada sortida què representa i en quina unitat s'expressa.

Comprova 470,6 m ponderats a D amb P2 obert i 2.217,7 amb P2 tancat. Per què el ràster troba un camí quan la xarxa tancada no en trobava cap? Relaciona la resposta amb els llocs on cadascun dels dos models permet moure's.

Al cas de la Pineda, compara una cel·la de fricció 20 amb una barrera NoData. Explica per què un valor alt encara permet passar i per què el mapa de cost acumulat no és un mapa d'altituds.

### Canviar el detall de la graella

Com a ampliació, repeteix un recorregut amb cel·les de 5 i de 10 m. Revisa especialment P2 i conserva les dues màscares de pas. Comprova si canvien connexió, longitud o cost, mantenint les unitats de la fricció. El cost per cel·la s'ha de convertir amb la mida corresponent en cada cas.

### Comparar temps d'anada i tornada

Amb l'MDT de 5 m, prepara fricció addicional 0 s/m als camins i 0,5 s/m a la resta admesa, conservant les barreres. Executa r.walk des d'O i des de D amb els coeficients `0.72,6.0,1.9998,-1.9998`, lambda 1 i vuit veïns. Desa segons, minuts, direccions i camins amb noms diferents per a cada sentit.

Comprova aproximadament 6,63 i 6,48 minuts amb P2 obert. Repeteix amb altitud constant: el control és 5,64 minuts en tots dos sentits. Explica per què invertir una línia ja calculada no substitueix aquest segon càlcul.

### Dibuixar i interpretar les isòcrones

Classifica el temps des d'O amb els mateixos límits de 3, 6 i 12 minuts als dos escenaris de P2. Conserva els ràsters, els contorns, la llegenda i un mapa comparatiu. A D els controls són 6,63 minuts amb el pas obert i 17,49 amb el pas tancat. En quina franja cau cada resultat?

Compta les cel·les fins a 12 minuts i multiplica-les per 25 m²: els controls són 36.777 i 22.155 cel·les, aproximadament 91,9 i 55,4 ha. Separa les barreres NoData dels llocs que simplement costen més de 12 minuts. Explica per què un buffer de les línies accessibles de la xarxa respondria a una altra operació.

### Distingir gir i sentit

En un encreuament, la maniobra a→b està prohibida i c→b està permesa. Dibuixa les dues arribades i explica per què tancar b seria incorrecte. Indica quina informació necessita el motor per distingir-les i quina limitació tenen les eines natives de la pràctica.

### Accés de vehicles i corredor de cable

Prepara dues fitxes per a una mateixa proposta: origen, destinació, unitats, barreres i dades necessàries. Una estudiarà l'accés de vehicles i l'altra, un corredor de cable. Justifica quines parts dels costos es poden comparar i quines responen a preguntes diferents.
