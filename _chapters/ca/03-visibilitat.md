---
layout: manual-chapter
title: Visibilitat i paisatge
description: Línies de visió, models d'elevació, conques visuals i receptors per interpretar exposició i canvis paisatgístics.
lang: ca
ref: visibilitat-territori
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/visibilitat/
weight: 30
part: Continguts
manual_references: true
---

Una instal·lació pot ser visible des d'un camí i quedar oculta des d'un nucli més proper. Un llom, un edifici o una pantalla vegetal poden tapar-la. Per entendre-ho cal situar des d'on es mira, què es vol veure i què hi ha entremig. Després es podrà preguntar quin significat té aquella vista per al paisatge i per a les persones.

Primer es comprova una línia entre dos punts. A continuació es repeteix el càlcul cap a moltes posicions per construir una conca visual, i des de diversos llocs per comparar vistes. Una torxa industrial de la Canonja, la carretera Vila-seca–la Pineda i una àrea industrial permeten avançar de punt a línia i a polígon amb les eines de QGIS.

>>>>> En acabar el capítol, cal poder calcular i explicar una estimació de visibilitat.
>>>>>
>>>>> - Relacionar línia de visió, altures i obstacles.
>>>>> - Distingir MDT, MDS i incertesa de representació.
>>>>> - Construir una selecció justificada de receptors i punts de la proposta.
>>>>> - Comparar escenaris d'exposició sense equiparar-los automàticament a impacte.

## Paisatge, exposició i impacte {#paisatge-impacte}

El paisatge és un recurs territorial i una dimensió de la qualitat de vida, no només una imatge des d'un punt. La seva valoració pot incorporar caràcter, activitats, memòria, identitat i objectius de transformació. El Catàleg de paisatge del Camp de Tarragona ofereix caracteritzacions, valors, itineraris i objectius que permeten situar una proposta dins d'aquest marc {% cite observatori2010camp %}.

La **visibilitat geomètrica** pregunta si hi ha una línia lliure d'obstacles entre dos punts. L'**exposició** pregunta des de quins llocs, durant quant de temps o sobre quina extensió es podria observar l'element. La **valoració de l'impacte** interpreta si aquell canvi és important per al paisatge. Un mapa que només distingeixi visible i ocult respon la primera pregunta, però no les altres dues.

Es pot entendre la diferència pensant en un dipòsit d'aigua visible des d'un sender. El càlcul geomètric determina si un turó talla la línia de visió. L'estudi d'exposició pot mesurar quants metres de sender ofereixen aquella vista. La valoració paisatgística encara necessita saber com s'integra el dipòsit, quina experiència ofereix el sender i quins valors del lloc es transformen. Són preguntes successives, no tres noms per al mateix mapa.

Observador
: Extrem des del qual es traça una línia de visió; es defineix amb posició i altura.

Objectiu
: Punt o part d'un objecte que es vol saber si és visible. La seva altura també forma part del problema.

Obstacle
: Element intermedi representat en el model que pot interceptar la línia: relleu, edificació o vegetació segons la superfície utilitzada.

Receptor paisatgístic
: Persona, itinerari o lloc des del qual s'interpreta el canvi. Pot requerir diversos punts d'observació per representar-lo.

Les aplicacions van des de la localització d'una torre de vigilància fins a l'estudi de vistes en arqueologia o la comparació d'infraestructures energètiques. Bishop estudia llindars d'impacte visual de turbines i ajuda a distingir existència d'una línia de visió, detecció i valoració {% cite bishop2002visual %}. La transferència útil és aquesta distinció metodològica; els llindars d'un objecte alt i mòbil no s'han de copiar a una superfície fotovoltaica baixa.

La distància, la mida aparent, el contrast i les condicions atmosfèriques intervenen en la percepció. Dos punts classificats com a visibles poden oferir experiències molt diferents. Una anàlisi pot limitar-se inicialment a visibilitat potencial, sempre que el títol i la conclusió conservin aquest abast.

## Geometria de la línia de visió {#linia-visio}

Per comprovar una vista es pot imaginar un fil ben tens entre els ulls de l'observador i el punt que es vol veure. Si el fil travessa el terreny o un obstacle, aquell punt queda ocult. La cota dels ulls és $z_O$ i la del punt observat, $z_T$. Amb separació horitzontal L, la cota del fil quan s'ha avançat una distància d és:

$$
z_{\mathrm{visio}}(d)=z_O+\frac{d}{L}(z_T-z_O).
\label{eq:linia-visio}
$$

Si el terreny o un obstacle supera aquesta línia en una posició intermèdia, l'objectiu queda ocult segons el model. Les altures absolutes es construeixen amb la cota de la superfície i l'altura relativa de l'observador o l'objectiu. Cal saber a quina superfície es refereix cadascun dels valors abans de sumar-los.

La fracció $d/L$ indica quina part del trajecte s'ha recorregut. A mig camí val 0,5: la cota del segment és a mig camí entre les cotes dels dos extrems. No cal memoritzar la fórmula abans d'entendre aquesta interpolació al llarg d'una recta.

### Resoldre un perfil abans de calcular una conca {#perfil-resolt}

En el perfil d'exemple, O és en un terreny de cota 100 m i té els ulls a 1,7 m sobre el sòl: $z_O=101,7$ m. T és la part superior d'un element de 2 m sobre un terreny de cota 108 m: $z_T=110$ m. Els separen 1.000 m. Són dues sumes diferents: **cota del sòl més altura relativa** en cada extrem.

::: table "Altura de la línia de visió en un perfil fictici de 1.000 m"
| Distància des de l'observador | Fracció del trajecte | Altura de la línia, m | Superfície intermèdia, m | Lectura local |
| --- | ---: | ---: | ---: | --- |
| 250 m | 0,25 | 103,775 | 100,586 | No intercepta |
| 500 m | 0,50 | 105,850 | 108 | Intercepta |
| 750 m | 0,75 | 107,925 | 104,586 | No intercepta |
:::

Al mig del recorregut, la superfície supera la línia en $108-105,85=2,15$ m. Aquest obstacle és suficient per ocultar l'objectiu encara que els altres punts comprovats quedin per sota. No es decideix per majoria de punts visibles: la visió necessita un segment lliure en **tot** el recorregut representat. Una conca visual repeteix aquest raonament cap a moltes destinacions, amb les convencions de mostreig de l'algorisme.

>>> Si la part superior de l'objectiu s'eleva de 110 a 115 m, la línia a mig camí puja fins a 108,35 m i supera l'obstacle de 108 m en 0,35 m. En aquest perfil discret ja no l'intercepta, però el marge és petit: un error vertical d'un metre podria canviar la classificació. El resultat mostra per què l'altura i l'exactitud importen especialment prop del límit de visió.

![Perfil amb cotes i altures d'observador, objectiu i obstacle; segon panell amb els trams visibles i ocults]({{ site.baseurl }}/assets/quarto/figures/visibilitat.qmd "A: una pantalla interromp la línia entre els ulls d'O i el punt T. B: es comprova la visió cap a cada posició de la superfície, ara amb altura d'objectiu zero. El verd identifica les parts visibles i el marró, les ocultes. L'escala vertical està exagerada."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

Una manera de programar aquest càlcul és el **traçat de raigs**, conegut com a *ray tracing*: es recorren posicions intermèdies d'una línia i es comparen amb la cota del segment de visió. El mateix raonament es repeteix cap a altres destinacions. Hi ha algorismes que organitzen la comprovació d'una manera més eficient, per exemple recorrent el ràster per sectors; el concepte d'obstacle intermedi continua sent el mateix.

>> Per preguntar si es veu el sòl, l'altura de l'objectiu és 0. Per preguntar si es veu una persona, una coberta o el capdamunt d'una torre, cal afegir-ne l'altura. Per això els dos panells responen preguntes relacionades, però no idèntiques.

### Abast, curvatura i refracció

En un perfil curt es pot aproximar la Terra com un pla. A distàncies grans, la **curvatura** fa que la superfície s'allunyi d'aquell pla. La **refracció** és la desviació de la llum en travessar aire amb propietats diferents. Algunes eines aproximen tots dos efectes amb un coeficient; aquest valor forma part del model, no descriu exactament qualsevol dia atmosfèric.

L'abast màxim defineix fins on es calcula. Una cel·la fora d'aquest abast és **no calculada**, no necessàriament oculta. La mateixa distinció afecta els buits de dades. Si l'exportació codifica no visible, fora de domini i sense informació amb el mateix valor, l'anàlisi posterior pot atribuir significat a una absència de càlcul.

La intervisibilitat és recíproca quan es conserva exactament la mateixa parella d'extrems absoluts i el mateix model d'obstacles. Si s'inverteixen origen i destinació però es mantenen incorrectament les altures relatives, s'ha canviat el problema. Aquesta comprovació és especialment important quan se situa el punt emissor a la instal·lació per calcular des d'on podria veure's.

## Models digitals d'elevació {#models-elevacio}

**Model digital d'elevacions** és una expressió general. Un **model digital del terreny** representa el sòl; un **model digital de superfície** pot incorporar vegetació i edificacions. Tots dos necessiten data, resolució, exactitud i referència vertical. Una font amb cel·les petites pot contenir errors o representar una superfície inadequada per a la pregunta {% cite burrough1998principles %}.

La cota d'un MDS a la coberta d'un edifici no és la cota del carrer. Situar un observador a 1,7 m sobre aquella superfície pot col·locar-lo damunt de la teulada, quan la pregunta es refereix a una persona al vial. Per això no es pot afirmar que un MDS dona sempre una conca menor que un MDT sense fixar els extrems absoluts i les condicions comparades.

::: table "Quina altura representa cada dada?"
| Dada fictícia | Valor | Què significa |
| --- | ---: | --- |
| Cota del sòl | 100 m | Posició vertical del terreny respecte de la referència del model |
| Altura d'una persona | 1,7 m | Separació dels ulls respecte del sòl en aquest exemple |
| Cota dels ulls | 101,7 m | Suma de cota del sòl i altura relativa |
| Cota d'una coberta al MDS | 112 m | Superfície de l'edificació, no el nivell del carrer |
:::

>>>> Introduir 101,7 en un paràmetre que demana **altura sobre el terreny** col·locaria els ulls a 201,7 m si el sòl és a 100 m. Cal llegir la definició del paràmetre: cota absoluta i altura relativa no són intercanviables.

Amb extrems fixats, afegir obstacles intermedis pot reduir la visibilitat potencial. Aquesta és una comparació controlada. En canvi, substituir tota la superfície i redefinir-hi observador i objectiu modifica diverses peces alhora. La interpretació ha d'indicar què s'ha canviat i quin efecte s'ha volgut aïllar.

### Resolució, obstacles estrets i estacionalitat

Una pantalla més estreta que la cel·la pot desaparèixer o ocupar una amplada exagerada. L'agregació d'elevacions pot suavitzar cims i marges que interceptaven la visió. Cal comprovar obstacles crítics amb el detall disponible, sense deduir precisió de la mida aparent del píxel al mapa.

La vegetació també canvia amb el temps i no és necessàriament una paret opaca uniforme. Un MDS capturat en una data no representa totes les condicions estacionals. Una comparació entre sòl nu i una superfície amb vegetació pot servir de sensibilitat, però no s'ha de presentar com una simulació estacional completa si no s'han modelitzat aquests canvis.

Les altures també necessiten el mateix origen de mesura. Unes cotes es refereixen a una superfície pròxima al nivell mitjà del mar —ortomètriques— i d'altres, a l'el·lipsoide de referència. No es poden barrejar directament. En comprovar la font, cal mirar tant com situa els punts al mapa com a què refereix les altures.

## Receptors i representació de la proposta {#receptors}

Un **receptor** pot ser una persona en un mirador, un tram d'itinerari, un nucli o un lloc amb una funció paisatgística determinada. La selecció necessita una justificació: ús, freqüència, relació amb el projecte o valor documentat. Els miradors del catàleg són una font, però no representen totes les experiències quotidianes.

Un nucli representat per un únic centroide no equival a totes les seves façanes i carrers. Per a una via, convé mostrejar punts a distància controlada o estudiar trams, indicant la densitat del mostreig. Més punts al mateix itinerari no haurien d'incrementar automàticament la importància d'aquell receptor només per una decisió de discretització.

>>> Un mirador es pot representar amb un punt, però una carretera té molts llocs des d'on mirar i un hort solar ocupa una superfície. Molts algorismes comproven la visió **entre punts**: un origen i els centres de les cel·les, o parelles d'orígens i destinacions. Per aplicar-los a una línia es poden prendre mostres cada certa distància; per a una àrea, punts del perímetre i de l'interior.
>>>
>>> Després cal decidir com resumir-los. «Es veu almenys un punt de l'hort» no significa «es veu tot l'hort». Igualment, veure'l des de tres mostres d'una carretera no equival directament a tres metres ni a tres persones. La separació de les mostres i la regla de resum donen significat al resultat.

En una proposta fotovoltaica cal situar la superfície dels panells i la seva altura. El punt ICAEN correspon al consumidor associat i no proporciona directament aquesta geometria {% cite icaenLocalitzacio %}. Mantenir una mateixa altura en dues alternatives ajuda a estudiar l'efecte de la localització; variar també aquella altura canviaria dues condicions alhora.

## Conca visual, acumulació i exposició {#conques}

Una **conca visual** és un mapa de les posicions visibles des d'un punt segons la superfície i les altures escollides. Sovint és **binària**, és a dir, només té dues respostes: 1 per a visible i 0 per a ocult. Un lloc sense dades o fora de l'abast necessita una tercera categoria, «no calculat».

Una conca acumulada suma els resultats de diversos observadors. Si tots tenen el mateix pes, una cel·la amb valor 4 és visible des de quatre punts del mostreig. No significa que quatre persones hi estiguin exposades ni que l'impacte sigui quatre vegades superior. Per interpretar-la com a freqüència o població caldria justificar pesos i evitar dobles recomptes.

Una matriu d'intervisibilitat relaciona receptors i punts de la proposta. Permet identificar quines parts expliquen l'exposició i provar modificacions de disseny. Si reduir una peça perifèrica elimina molta visibilitat des d'un receptor rellevant, el resultat suggereix una revisió concreta. Aquesta informació pot ser més útil que una superfície visible total.

### Acumular conques visuals al llarg d'una carretera {#visibilitat-acumulada}

Una persona que circula no observa el territori des d'un únic punt. Per aproximar la successió de vistes es poden mostrejar posicions al llarg de la carretera i calcular una conca visual des de cadascuna. Tots els resultats han de compartir graella, resolució i domini vàlid. Després se sumen **cel·la a cel·la**, no les superfícies totals dels mapes.

En l'experiment numèric següent es construeix un relleu amb dos lloms i una carretera amb sis observadors. La graella té 24 columnes i 18 files, amb cel·les de 50 m. Cada observador se situa 1,7 m sobre el terreny; es comprova la visió d'un objectiu de 2 m a cada cel·la. Les elevacions són simulades per veure el paper dels obstacles, abans de treballar amb un MDT real.

![Relleu, conca d'O3 i suma de les sis conques, amb O1 a O6 identificats en tots els panells]({{ site.baseurl }}/assets/quarto/figures/visibilitat-acumulada.qmd "Les etiquetes O1–O6 permeten seguir els mateixos observadors. B mostra la vista des d'O3; C suma les sis vistes. Una cel·la amb 4 és visible des de quatre posicions. Cel·les de 50 m, observadors a 1,7 m i objectius a 2 m sobre el sòl."){: data-figure-width-web="45rem" data-figure-width-pdf="100%"}

El primer panell explica l'entrada: geometria del recorregut i elevacions que poden ocultar vistes. El segon mostra una única conca, amb 0 i 1. El tercer conserva la varietat d'acumulacions: una cel·la amb 6 es veu des de totes les posicions; una amb 1, només des d'una; i una amb 0 queda oculta des de les sis sota aquests supòsits. L'ombra visual d'un llom canvia segons el costat des d'on s'observa, i per això la suma no és una ampliació uniforme d'una sola conca.

Si $V_k(c)$ val 1 quan l'observador k veu la cel·la c i 0 quan no la veu, la conca acumulada és:

$$
A(c)=\sum_{k=1}^{N}V_k(c).
\label{eq:conca-acumulada}
$$

N és el nombre d'observadors, sis en aquesta figura. Per exemple, una cel·la amb resultats 1, 0, 1, 1, 0 i 1 acumula 4; dividir per sis dona una proporció de posicions del mostreig de 2/3. No s'han comptat persones, vehicles ni minuts. Si es duplica un observador, la suma augmenta encara que el territori no hagi canviat: cal mantenir el mateix disseny de mostreig quan es comparen alternatives.

### Donar significat a la freqüència acumulada {#visibilitat-ponderada}

La suma simple tracta totes les posicions igual. Amb mostreig regular i una convenció per als extrems es pot aproximar quina part d'un itinerari ofereix visió. Si els intervals són desiguals, cal ponderar per la longitud de carretera que representa cada mostra. Per estudiar temps d'exposició, els pesos han de representar temps, que també depèn de la velocitat; per estudiar persones, caldrien dades d'ús i una regla que evités duplicacions.

Amb pesos $w_k$ no negatius i coneguts, una proporció ponderada es calcula així:

$$
F(c)=\frac{\sum_k w_k V_k(c)}{\sum_k w_k}.
\label{eq:visibilitat-ponderada}
$$

El numerador suma els pesos de les posicions amb visió i el denominador els de totes les posicions considerades. Si els pesos són metres representats, F aproxima una fracció de longitud; si són segons, una fracció de temps. Un pes d'importància paisatgística produeix un índex de valoració amb un altre significat, no una freqüència física.

>> Les cel·les no calculades no entren silenciosament com a zeros. Si una conca té un buit en una cel·la, es conserva també el nombre de contribucions vàlides. Per comparar acumulacions convé treballar amb un domini comú complet o mostrar explícitament on el denominador és diferent.

La mateixa operació es pot plantejar des dels punts d'una instal·lació cap al territori. En aquest cas, una acumulació alta indica que des d'aquell receptor serien visibles més punts mostrejats de la proposta. El nombre ja no compta posicions d'una carretera: ha canviat què representa l'índex k. Aquesta és la distinció que s'utilitzarà en el cas de la petroquímica.

### Llegir una matriu receptor–objectiu {#exemple-intervisibilitat}

Una **matriu d'intervisibilitat** és una taula de parelles: cada fila és un lloc des d'on es mira i cada columna un punt que es vol observar. Per llegir una casella es creuen una fila i una columna. En l'exemple, R1–R4 són receptors i P1–P3 són parts d'una proposta.

![Mapa de receptors, punts de proposta i pantalles, al costat de la taula amb les mateixes etiquetes]({{ site.baseurl }}/assets/quarto/figures/intervisibilitat.qmd "El mapa i la taula expliquen les mateixes relacions. Els punts es consideren al mateix nivell i els rectangles representen pantalles opaques. Una línia lliure dona 1; una línia interceptada, 0. R4 queda fora de l'àmbit de càlcul i conserva un guió."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}

>>> La casella **fila R2, columna P1** conté 1: des de R2 es veu P1. Al mapa es pot seguir la línia verda entre aquests punts. La casella **R1–P2** conté 0 perquè una pantalla talla aquella línia. El 0 no és un valor baix de qualitat paisatgística: vol dir que no hi ha visió en aquesta parella.

Llegir una fila respon què veu un receptor. R2 veu dues de les tres parts mostrejades: la fracció és 2/3, però no equival necessàriament a dos terços de superfície del projecte. Llegir una columna respon des d'on es veu una part. P1 és visible des de R1 i R2, mentre que P3 queda oculta des dels tres receptors calculats.

Hi ha visió d'almenys una part en dos dels tres receptors amb informació completa: aproximadament el 67%. Dividir per quatre i obtenir 50% amagaria R4 com si s'hagués comprovat que no veu res. Cal conservar el denominador i la cobertura. Tampoc és el 67% de la població: cada receptor del mostreig compta una vegada, sigui un mirador o un punt d'un camí.

>>> Si una alternativa elimina P1 i manté P2 i P3, R1 deixa de veure punts mostrejats i R2 encara veu P2. La matriu permet explicar **què** ha produït el canvi. Per decidir si l'alternativa és millor cal comprovar també quin servei o capacitat s'ha perdut en eliminar aquella part i quins receptors s'han representat.

Per a un itinerari convé passar de punts a longitud. Si un tram s'ha mostrejat regularment cada 50 m, els punts poden servir per aproximar la fracció de recorregut amb visió, amb un error que depèn de la separació i de la variació real entre punts. Si es mostregen molts més punts al voltant d'un mirador, una simple proporció de punts ja no representa longitud de camí. El disseny del mostreig determina què es pot resumir.

### Visibilitat i reflexos

La possibilitat de veure un panell no equival a rebre un reflex molest. L'enlluernament requereix considerar geometria solar, orientació, inclinació, propietats de reflexió, receptor i instant. Una conca visual del relleu no conté aquests elements. Tampoc no és correcte concloure absència de qualsevol efecte perquè un únic punt del parc resulti ocult.

L'anàlisi docent d'aquest capítol tracta exposició geomètrica potencial. La valoració paisatgística posterior pot incorporar distància, durada de l'exposició, mida aparent, caràcter i efectes acumulats. Si una decisió depèn d'enlluernament, caldrà un model específic i dades adequades, no una reclassificació improvisada del viewshed.

## Visibilitat puntual: torxa de la Canonja {#procediment-visibilitat}

### El complex petroquímic de Tarragona {#context-petroquimic}

El **complex petroquímic de Tarragona** és un conjunt d'instal·lacions i empreses relacionades, distribuïdes principalment entre el **Polígon Nord**, el **Polígon Sud** i el **Port de Tarragona**. No és una única fàbrica ni una sola parcel·la. El sector d'aquest exercici se situa al Polígon Sud, a l'entorn de la Canonja; no és la refineria del Polígon Nord. La distinció importa quan es dona nom a una capa i quan s'interpreta què representa el seu perímetre {% cite farnos2025petroquimica %}.

La implantació petroquímica s'intensificà durant els **anys seixanta**. La síntesi històrica de [Jordi Rosell a Enciclopèdia.cat](https://www.enciclopedia.cat/tecnics-i-tecnologia-en-el-desenvolupament-de-la-catalunya-contemporania/el-complex-petroquimic-de) situa l'entrada en funcionament de Dow i d'Indústries Químiques Associades el **1967**, i la producció de poliestirè de BASF el **1969**. La construcció de la refineria començà el **1973** i l'activitat s'inicià el **1976**, segons la [cronologia de Repsol](https://tarragona.repsol.es/ca/sobre-complejo/nuestra-historia/index.cshtml). Són etapes d'una implantació successiva, no una inauguració simultània de tot el conjunt.

El port ajuda a explicar aquesta localització. Les primeres plantes necessitaven rebre grans volums de matèries primeres: Dow importava etilè per via marítima abans de disposar dels subministraments de la refineria. El [Museu del Port de Tarragona](https://visitmuseum.gencat.cat/ca/museu/museu-del-port-de-tarragona/objecte/la-petroquimica) relaciona l'expansió petroquímica amb nous tràfics de vaixells tanc i amb la construcció de canonades. A l'accés marítim s'hi afegeixen les decisions d'inversió i la proximitat entre plantes que utilitzen productes d'altres processos.

La relació entre Nord, Sud i port és, per tant, també productiva i logística. La refineria i les plantes de química de base proporcionen matèries que es transformen en altres instal·lacions, i els **racks** —estructures que agrupen conduccions— permeten transportar matèries primeres i productes entre àmbits. L'[AEQT documenta el rack compartit Dixquímics](https://www.aeqtonline.com/qui-som/#sinergies), que connecta empreses entre elles i amb el port. El paisatge visible de torres, dipòsits, canonades i molls expressa aquestes relacions; el mapa de visibilitat només n'estudia una dimensió, que s'ha de distingir dels fluxos, els riscos o la valoració social.

### Dades de la torxa i de l'entorn {#dades-visibilitat-nord}

La primera pregunta és concreta: **es veu la part alta d'una torxa des d'un punt de la carretera?** El cas se situa a la Canonja, al polígon químic sud, prop del recorregut entre Vila-seca i la Pineda. Les torxes són les estructures on es poden observar flames de combustió. Per identificar-ne una es contrasta el [punt d'OpenStreetMap classificat com a torxa](https://www.openstreetmap.org/node/7682543312) amb l'ortofoto ICGC de 2025 i les elevacions LiDAR de 2021–2023.

L'ortofoto s'ha obtingut amb peticions **GetMap al servei WMS de l'ICGC**, capa de 2025, i s'ha desat localment com a GeoTIFF georeferenciat. La vista general té 10 m per píxel; els retalls industrial i de la torxa, 2,5 i 0,5 m per píxel. Són resolucions de les imatges demanades al servei, que ofereix una ortofoto d'origen de 25 cm. L'extensió i la resolució de cada petició es conserven a `fonts/fonts.json`.

![Torxa, carretera i recinte petroquímic sobre l'ortofoto]({{ site.baseurl }}/assets/captures/visibilitat-costa-dades.png "T és la torxa; la línia blava segueix la TV-3148. El contorn taronja delimita el recinte petroquímic d'estudi, generalitzat a partir de la coberta industrial. Són els tres objectes que s'estudiaran successivament."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICGC, RTT i MCSC 2024, ortofoto 2025 obtinguda per WMS; col·laboradors d'OpenStreetMap."}

El càlcul de visibilitat necessita també elevacions. L'**MDT** representa el terreny, mentre que l'**MDS** incorpora les superfícies d'edificis, instal·lacions i vegetació. La captura següent mostra l'MDS amb el mateix enquadrament que l'ortofoto: permet relacionar les estructures reconegudes a la imatge amb les cotes que intervenen en el model.

![Model digital de superfície, recinte i carretera amb el mateix enquadrament que l'ortofoto]({{ site.baseurl }}/assets/captures/visibilitat-costa-mds.png "Els colors representen cotes superficials en metres. L'MDS LiDAR d'1 m s'ha agregat pel màxim a cel·les de 5 m; el recinte, la carretera i T mantenen la mateixa posició que a l'ortofoto. La llegenda d'elevacions és al panell de capes."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Font: model digital de superfície ICGC, LiDAR 2021–2023; derivació a 5 m."}

El punt T es representa al centre de la cel·la de 5 m situada a **(346892,5;4552507,5) m**, en EPSG:25831. Les coordenades vectorials originals es conserven als atributs; l'ajust a la graella és de 2,48 m. A l'emplaçament, l'MDT indica una cota d'uns 20,94 m i el pic de l'MDS, comprovat també en el retall natiu d'1 m, arriba a 151,31 m: aproximadament **130,4 m sobre el terreny**.

![Detall de la torxa identificada en l'ortofoto de QGIS]({{ site.baseurl }}/assets/captures/visibilitat-costa-torxa.png "La posició de T correspon a una estructura identificable, no al centroide d'una parcel·la. L'estimació vertical prové del LiDAR; l'ortofoto aporta el contrast de localització."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ortofoto ICGC 2025 i col·laboradors d'OpenStreetMap."}

Per al càlcul es fixa T **1 m per damunt del pic representat**, a cota 152,311996 m. És una separació de model respecte de la superfície digital, no una mesura de l'altura de la flama. Les flames varien; les elevacions tampoc no certifiquen per si soles l'altura física exacta de l'estructura.

### Intervisibilitat entre la torxa i la carretera {#perfils-visibilitat-nord}

R1, R2 i R3 són posicions de consulta al recorregut, amb els ulls a **1,7 m sobre l'MDT**. S'han triat per il·lustrar respostes diferents: no són una mostra representativa de persones. La capa `resultats/intervisibilitat.gpkg` relaciona aquests receptors amb T i permet seguir cada parella sobre el mapa.

::: table "Tres parelles amb la mateixa torxa"
| Receptor | Mostra del recorregut | MDT | MDS | Lectura |
| --- | --- | ---: | ---: | --- |
| R1 | C05 | 1 | 1 | Hi ha visió en tots dos models |
| R2 | C11 | 0 | 0 | El relleu ja intercepta la línia |
| R3 | C13 | 1 | 0 | Els obstacles de l'MDS canvien la resposta |
:::

![Línies entre T i receptors de carretera, amb R5 fora del retall]({{ site.baseurl }}/assets/captures/visibilitat-costa-intervisibilitat.png "Amb MDS, el verd indica visió de T i les línies discontínues, ocultació. R5 queda fora de l'àmbit i conserva una resposta no calculada. Les línies representen relacions visuals, no trajectes d'accés."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

El perfil explica la classificació. A R1, la línia queda per damunt de les dues superfícies. A R3, passa per sobre del terreny, però un obstacle pròxim al receptor representat a l'MDS la supera. El detall dels últims 80 m ajuda a veure una diferència que quedaria amagada en un perfil de més d'un quilòmetre.

![Perfils complets T–R1 i T–R3 amb ampliació dels últims vuitanta metres]({{ site.baseurl }}/assets/quarto/figures/visibilitat-perfils.qmd "R1 conserva visió amb MDT i MDS; a R3, l'MDS intercepta la línia. Cada fila comparteix escala vertical entre els dos casos. Els detalls inferiors es llegeixen cap al receptor, de 80 a 0 m, i mostren els obstacles propers."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}

### Conca visual de la torxa {#passar-de-les-parelles-al-mapa}

Una conca repeteix la comprovació cap a les cel·les de l'entorn. El paquet de Moodle inclou les fonts, les còpies de càlcul, els resultats de referència i deu projectes QGIS amb rutes relatives. `00-inici.qgz` situa el cas; `01-torxa.qgz` i `02-intervisibilitat.qgz` permeten començar pels punts. Les sortides pròpies es desen a `treball`.

La graella comuna té **2.000 × 2.000 cel·les de 5 m**, amb límits X 342000–352000 i Y 4549000–4559000. L'MDT conserva la resolució nativa; l'MDS d'1 m s'ha agregat pel màxim a 5 m. Aquesta operació reté cotes altes, però pot eixamplar arbres, fanals i altres obstacles estrets.

El mar i els buits d'elevació es tracten abans del càlcul. Les còpies preparades representen els buits del mar cartografiat a 0 m i exclouen les línies afectades per altres elevacions desconegudes. La capa **Domini** val 1 a les **3.490.455 cel·les comparables** i NoData a la resta. Els originals es conserven a `fonts`; les còpies i la màscara, a `dades`.

Per localitzar l'eina, obre **Procés → Caixa d'eines**, prem el botó corresponent de la barra o utilitza **Ctrl+Alt+T**. A la cerca de la caixa de Processament, escriu **Viewshed** i comprova que el resultat correspon al proveïdor **GDAL**. Els noms traduïts i els identificadors permeten reconèixer la mateixa eina entre instal·lacions {% cite qgisUserGuide %}.

::: subfigures a/b "Dos accessos a la caixa d'eines de Processament"
![Menú Procés amb l'opció Caixa d'eines i la drecera]({{ site.baseurl }}/assets/captures/visibilitat-acces-menu.png "El menú Procés mostra Caixa d'eines i la drecera disponible."){: data-figure-width-web="44rem" data-figure-width-pdf="90%"}
![Botó de la barra que obre la caixa de Processament]({{ site.baseurl }}/assets/captures/visibilitat-acces-barra.png "El botó de la barra obre el mateix panell. Després s'hi cerca el nom de l'algorisme."){: data-figure-width-web="44rem" data-figure-width-pdf="90%"}
:::

A **Conca visual / Viewshed**, `gdal:viewshed`, es trien l'MDT de càlcul, banda 1, T com a origen, altura **131,369997 m** sobre MDT i altura de destinació **1,7 m**. S'aprofita la reciprocitat per preguntar des d'on es veu T. Distància màxima 0 significa tota la finestra ràster; es fixen els codis 1/0, NoData separat i curvatura/refracció **0,85714**.

![Caixa de Processament oberta amb GDAL, Miscel·lània ràster i Viewshed desplegats]({{ site.baseurl }}/assets/captures/visibilitat-acces-caixa-viewshed.png "A la versió capturada, Viewshed és dins de GDAL → Miscel·lània ràster. El requadre identifica la fila que obre l'algorisme. La cerca pel nom també permet arribar-hi."){: data-figure-width-web="40rem" data-figure-width-pdf="90%"}

![Diàleg Viewshed amb les coordenades i les altures de T]({{ site.baseurl }}/assets/captures/visibilitat-costa-punt.png "El camp demana altura relativa: 131,37 m sobre l'MDT, no la cota absoluta de 152,31 m. L'altre extrem se situa a 1,7 m sobre el terreny. Després s'aplica la màscara del domini comú."){: data-figure-width-web="42rem" data-figure-width-pdf="90%"}

La Calculadora ràster aplica `"Domini@1" * "Conca T MDT@1"`. Això conserva la resposta 0/1 dins del domini i NoData fora. El resultat de referència, `resultats/torxa-mdt.tif`, conté **2.962.199 cel·les visibles**, el **84,87%** del domini comparable. És superfície territorial, no nombre de persones.

## Comparar MDT i MDS amb els mateixos extrems {#mdt-mds-controlat}

Canviar de superfície no ha de moure la torxa ni els ulls. T continua a cota 152,311996 m: sobre l'MDS necessita una altura relativa d'1 m, mentre que sobre l'MDT en necessita 131,369997.

::: table "Cotes i altures del punt T"
| Magnitud | Valor aproximat |
| --- | ---: |
| MDT a T | 20,941999 m |
| Pic MDS a T | 151,311996 m |
| Cota de T en el model | 152,311996 m |
| Altura sobre MDT | 131,369997 m |
| Altura equivalent sobre MDS | 1 m |
:::

Els receptors conserven la cota **MDT + 1,7 m**. El mode **DEM** de [GDAL Viewshed](https://gdal.org/en/stable/programs/gdal_viewshed.html), activat amb `-om DEM`, retorna la **cota absoluta mínima** necessària a cada destinació. Es calcula amb MDS, les coordenades de T i altura d'origen 1 m. L'altura de destinació queda ignorada en aquest mode; **GROUND** expressaria una altra magnitud, l'altura addicional sobre la superfície.

Amb el resultat **Cota mínima MDS**, la Calculadora ràster compara cotes i aplica el mateix domini:

```text
"Domini@1" * (("MDT@1" + 1.7) >= "Cota mínima MDS@1")
```

![Calculadora ràster amb la màscara i la comparació de cotes absolutes]({{ site.baseurl }}/assets/captures/visibilitat-costa-cota-minima.png "La comparació manté els ulls sobre l'MDT. Domini conserva els llocs no calculats com a NoData. El resultat és binari; la cota mínima intermèdia, en metres absoluts, es conserva en Float64."){: data-figure-width-web="44rem" data-figure-width-pdf="94%"}

La conca MDS de T conté **447.860 cel·les visibles**, el **12,83%** del domini. La reducció correspon a una superfície opaca i agregada pel màxim. No representa transparència de capçades, intensitat de la flama ni condicions atmosfèriques; els marges petits dels perfils requereixen una lectura especialment prudent.

## Visibilitat al llarg de la carretera Vila-seca–la Pineda {#mostreig-punt-linia-area}

### Representar un recorregut amb observadors

Ara canvia la pregunta: **quines posicions del territori es veuen al llarg d'una carretera?** El recorregut segueix els eixos de la **TV-3148** del [Referencial Topogràfic Territorial de l'ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial). Va de la sortida de Vila-seca a l'enllaç amb la TV-3146, a l'entrada de la Pineda, i fa **3.652,272633 m**. Se'n prepara una trajectòria cartogràfica única per evitar sumar dues vegades les dues calçades.

El recorregut es divideix en **37 intervals iguals de 98,710071 m**. A **Punts al llarg de la geometria**, `native:pointsalonglines`, s'introdueix aquest pas i un desplaçament inicial de **49,355036 m**. Cada punt C se situa al mig de la longitud que representa. La capa conserva les posicions originals i les coordenades de centre de cel·la utilitzades en el càlcul.

![Mostreig de la TV-3148 amb intervals regulars i mig interval inicial]({{ site.baseurl }}/assets/captures/visibilitat-costa-carretera.png "Cada mostra representa 98,71 m del recorregut. La separació es mesura al llarg de la línia; no és un radi de visió. La suma dels 37 pesos recupera els 3.652,27 m analitzats."){: data-figure-width-web="42rem" data-figure-width-pdf="90%"}

### Sumar les conques, no les superfícies totals

**Viewshed calcula una conca per punt i execució.** Per comprendre el procediment es poden repetir individualment C05, C11 i C13. Per obtenir les 37 conques, QGIS ofereix **execució per lots**: una taula amb una fila per observador. Quan s'executa el lot, QGIS repeteix automàticament l'algorisme amb els paràmetres de cada fila; el lot no suma les conques per si sol.

S'hi accedeix amb clic dret sobre **Viewshed → Execute as batch process…**, o des del botó equivalent del diàleg de l'algorisme. Les opcions d'emplenament automàtic permeten afegir les coordenades dels 37 punts a partir dels camps `x` i `y`, copiar els paràmetres comuns a tota la columna i generar una ruta de sortida diferent per fila. El [manual de QGIS descriu el funcionament dels lots](https://docs.qgis.org/3.44/en/docs/user_manual/processing/batch.html).

En aquest lot MDT, les altures d'origen i destinació són **1,7 m sobre el terreny**. També són comuns l'MDT, banda 1, abast 0, curvatura 0,85714 i codis de resposta. Canvien **les coordenades i el fitxer de sortida**. Cal comprovar 37 files i 37 noms diferents abans d'executar-lo; escollir la capa de punts no fa que un paràmetre de coordenada individual recorri tots els seus objectes automàticament.

Els 37 ràsters de referència, ja emmascarats amb Domini, són a `resultats/conques-carretera-mdt`. Si el lot produeix conques crues, es poden sumar primer i aplicar la màscara comuna al resultat: amb nom **Suma C bruta**, la fórmula és `"Domini@1" * "Suma C bruta@1"`. Dins del domini és equivalent a emmascarar cada conca abans de sumar-la.

**Estadístiques de cel·la**, `native:cellstatistics`, amb estadística **Suma**, combina els 37 ràsters. Es pren una de les entrades com a referència de graella i es desactiva **Ignora NoData**. El resultat compta des de quantes posicions de carretera es veu cada destinació del model.

![Conca acumulada de les trenta-set posicions de carretera amb MDT]({{ site.baseurl }}/assets/captures/visibilitat-costa-acumulada.png "Un valor 12 significa visió des de 12 dels 37 observadors, no 12 persones. El màxim observat és 33. El mar i les zones sense comparació queden fora del recompte; el gris dins del domini correspon a zero."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

>>> Amb pesos iguals, una cel·la amb 12 representa aproximadament $12\times98,710071=1.184,52$ m de recorregut amb visió: el **32,43%** dels 3.652,27 m analitzats. És una aproximació per mostreig, no una digitalització de tots els canvis de visió entre punts.

La pregunta inversa, **des de quina part de la carretera es veu T**, es resol mostrejant la conca de la torxa als punts C amb `native:rastersampling`. Amb MDT, 34 de les 37 mostres donen 1: representen uns **3.356,14 m**. Aquesta longitud d'itinerari no s'obté sumant les àrees visibles de les 37 conques.

>> El paquet inclou `reproduccio/lots_visibilitat.py` per executar tota la cadena des de QGIS: llegeix cada observador, crida `gdal:viewshed`, aplica les cotes i Domini i desa els recomptes i percentatges. És un guió d'automatització amb les mateixes operacions, no una introducció manual de punts. El guió de pràctica mostra tant l'emplenament del lot gràfic com la invocació d'aquesta cadena.

## Visibilitat del recinte petroquímic {#cas-petroquimica}

### Delimitar una coberta funcional

La tercera pregunta és **des de quines parts del territori es veu algun element del polígon**. S'utilitza el polígon **1459998** del [Mapa de cobertes del sòl de Catalunya de 2024](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya), classe 347, «Zones industrials, comercials i/o de serveis». L'ortofoto permet reconèixer l'àrea industrial seleccionada de **162,59 ha**.

La geometria original representa una coberta del sòl, amb **19 forats** i entrants que separen parts de la instal·lació. Per tractar el sector com una unitat es delimita un **recinte petroquímic d'estudi** més compacte, que inclou patis i alguns espais entre peces industrials. La coberta original es manté a `dades/coberta-original.gpkg`; el recinte derivat, a `dades/poligon.gpkg`. La generalització no modifica els usos classificats pel MCSC.

### Construir un recinte compacte amb dos buffers {#perimetre-estudi}

Un **buffer positiu de n metres seguit d'un buffer negatiu de n metres sobre el resultat anterior** és un **tancament morfològic**. El primer expandeix la geometria; el segon en retreu el contorn. Les parts separades per passos estrets poden quedar unides i alguns buits es tanquen. La segona operació no desfà necessàriament la primera: els espais que s'han tancat poden romandre incorporats al recinte.

La distància expressa l'escala dels espais que es volen incorporar. En un pas aproximadament paral·lel, una amplada inferior a **2n** pot arribar a tancar-se durant l'expansió; la forma i la connexió amb l'exterior també condicionen el resultat. Per això es comparen diversos valors sobre l'ortofoto abans d'escollir-ne un.

A QGIS, l'eina **Àrea d'influència / Buffer**, `native:buffer`, es pot obrir des de **Vectorial → Geoprocessing Tools → Àrea d'influència…**. La traducció del submenú es conserva en anglès a la versió capturada. També és a **Geometria vectorial** dins de la caixa de Processament.

![Menú Vectorial i submenú de geoprocessament oberts fins a Àrea d'influència]({{ site.baseurl }}/assets/captures/visibilitat-acces-menu-buffer.png "Els menús estan desplegats. Els requadres indiquen Vectorial i l'entrada Àrea d'influència, que correspon a native:buffer."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

![Àrea d'influència seleccionada dins de la caixa de Processament]({{ site.baseurl }}/assets/captures/visibilitat-acces-caixa-buffer.png "La caixa d'eines també dona accés a Àrea d'influència. Cal triar aquesta eina de geometria vectorial; altres algorismes amb buffer al nom tenen funcions diferents."){: data-figure-width-web="40rem" data-figure-width-pdf="90%"}

La primera execució utilitza **Coberta original MCSC**, distància **+150 m**, **32 segments per quadrant**, unions arrodonides i dissolució activada. La segona execució utilitza **aquest intermedi**, distància **−150 m** i els mateixos altres paràmetres. El resultat es desa com **Recinte petroquímic d'estudi**.

El paquet conserva l'intermedi a `dades/buffer-positiu.gpkg`.

![Buffer positiu de cent cinquanta metres sobre la coberta original]({{ site.baseurl }}/assets/captures/visibilitat-costa-buffer-positiu.png "Primer s'expandeix la coberta original 150 m i es dissol el resultat. Els 32 segments per quadrant aproximen els arcs de les unions arrodonides."){: data-figure-width-web="42rem" data-figure-width-pdf="94%"}

![Buffer negatiu de cent cinquanta metres sobre el buffer intermedi]({{ site.baseurl }}/assets/captures/visibilitat-costa-perimetre.png "El segon buffer s'aplica a Buffer intermedi +150 m. El signe negatiu retreu aquest resultat 150 m; no s'aplica de nou a la coberta original."){: data-figure-width-web="42rem" data-figure-width-pdf="94%"}

::: table "Comparació de geometries per al mateix sector"
| Mètode | Àrea, ha | Forats | Àrea afegida fora del contorn original, ha |
| --- | ---: | ---: | ---: |
| Coberta original | 162,59 | 19 | 0 |
| Tancament +50/−50 m | 181,33 | 5 | 4,85 |
| Tancament +100/−100 m | 199,97 | 2 | 15,52 |
| Tancament +150/−150 m | 222,94 | 0 | 38,50 |
| Tancament +250/−250 m | 224,49 | 0 | 40,04 |
:::

![Coberta original i quatre distàncies de tancament comparades a la mateixa escala]({{ site.baseurl }}/assets/quarto/figures/visibilitat-perimetre.qmd "Amb 50 i 100 m encara queden buits. El tancament de 150 m produeix el recinte compacte utilitzat en l'exercici; passar a 250 m incorpora poca superfície addicional. La línia discontínua conserva el contorn exterior original."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="Font: MCSC ICGC 2024; buffers natius de QGIS, amb 32 segments per quadrant."}

S'adopta **150 m**, després de contrastar les formes amb l'ortofoto. El recinte té **222,94 ha** i incorpora **38,50 ha fora del contorn exterior original**. És una delimitació generalitzada d'estudi, no el límit oficial de tot el Polígon Sud. La discretització dels arcs retira també uns 3,77 m² de la font en punts de vora; el resultat no s'ha de tractar com una operació cadastral exacta. Les alternatives es conserven per poder revisar la decisió.

### Mostrejar l'interior i conservar els elements destacats

Una graella rectangular de **250 × 250 m** es retalla amb el **recinte petroquímic d'estudi** mitjançant `native:clip`. **Punt sobre la superfície**, `native:pointonsurface`, situa una mostra A dins de cada fragment. En resulten **57 fragments**.

La suma dels pesos és **2.229.408,741960 m²**. La malla representa també els espais incorporats al recinte; els fragments de vora tenen menys pes que els quadrats complets.

![Graella de dos-cents cinquanta metres per preparar el mostreig d'àrea]({{ site.baseurl }}/assets/captures/visibilitat-costa-area.png "La graella es retalla amb el recinte abans d'obtenir punts i pesos. Una mostra interior representa el seu fragment; no cal situar totes les mostres al perímetre."){: data-figure-width-web="42rem" data-figure-width-pdf="90%"}

Les mostres A se situen **1 m sobre l'MDS local**. La cota absoluta resultant es manté també al càlcul MDT: cada fila té les seves altures `h_mdt_m` i `h_mds_m`. Així es mostreja una superfície amb altures diferents, no s'assigna una mateixa torre hipotètica a tot el recinte.

![Mapa amb T, trenta-set punts de carretera i cinquanta-set mostres dins del recinte petroquímic]({{ site.baseurl }}/assets/quarto/figures/visibilitat-mostreig.qmd "La torxa és un objectiu singular, C mostreja posicions d'observació i A representa fragments del recinte. Les tres geometries responen preguntes diferents. Les cotes provenen dels models d'elevació i dels desplaçaments verticals definits a l'exercici."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICGC, RTT i MCSC 2024; col·laboradors d'OpenStreetMap."}

També aquí es repeteix el càlcul per lots: **57 execucions per superfície**, una per A. Amb MDT, l'altura d'origen varia segons `h_mdt_m`; amb MDS és 1 m i s'utilitza la cota mínima per mantenir els receptors a MDT + 1,7 m. El guió d'automatització del paquet encadena aquestes operacions, aplica Domini i acumula els pesos de cada fragment. Un lot de Viewshed, tot sol, només produeix les sortides individuals.

Una graella regular pot passar per alt una estructura estreta i alta. Per això **T es conserva com a objectiu addicional**. El mapa d'alguna part visible combina «es veu almenys una de les 57 mostres A» **o** «es veu T». No s'atribueixen a la torxa els metres quadrats de tot un fragment.

```text
("Nombre A@1" > 0) OR ("Torxa T@1" = 1)
```

![Mapa del territori amb visió d'alguna mostra industrial, inclosa la torxa]({{ site.baseurl }}/assets/captures/visibilitat-costa-poligon.png "El verd identifica visió d'algun dels 57 objectius d'àrea o de T, amb MDS. La conca de T queda inclosa en aquest resultat. Veure almenys una part no significa veure tot el polígon ni conèixer-ne l'impacte paisatgístic."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

Amb MDS, el resultat conté **470.444 cel·les visibles**, el **13,48%** del domini comparable. Amb MDT en conté **2.977.704**, el **85,31%**. Són estimacions condicionades pels punts seleccionats, la superfície, les altures i la resolució; les estructures que no s'han mostrejat poden modificar-les.

## Llegir conjuntament els resultats {#resultats-visibilitat-nord}

La comparació controlada de carretera requereix una comprovació addicional. En **9 de les 37 posicions**, els ulls a MDT + 1,7 m quedarien sota la superfície opaca de l'MDS. Es conserven aquestes files com a no calculades per a aquest contrast, i es comparen els dos models amb les mateixes **28 posicions**. Representen **2.763,88 m**, el 75,68% del recorregut. El càlcul inicial MDT amb les 37 mostres continua disponible.

![Comparació de la torxa, les posicions comunes de carretera i algun objectiu del polígon amb MDT i MDS]({{ site.baseurl }}/assets/quarto/figures/visibilitat-mdt-mds.qmd "T i G són mapes binaris. C representa la fracció de les 28 posicions comparables amb visió, no les 37 del primer exercici MDT. Els requadres expressen percentatge del territori calculable. El blanc conserva les zones no calculades."){: data-figure-width-web="48rem" data-figure-width-pdf="100%" data-caption-source="Fonts: elevacions ICGC 2021–2023, RTT i MCSC 2024, col·laboradors d'OpenStreetMap. Càlcul a 5 m; representació gràfica cada 25 m."}

La fracció ponderada d'àrea és una altra sortida. Suma els metres quadrats dels fragments representats per mostres visibles i divideix pel pes total dels **57 fragments**. La torxa addicional intervé en la resposta «alguna part», però no s'hi afegeix un pes superficial inventat.

::: table "Magnituds que no s'han de confondre"
| Sortida | Valor | Què respon |
| --- | --- | --- |
| Conca de T | 0/1 | Es veu la torxa des d'aquesta posició? |
| Carretera MDT, 37 conques | 0–37 | Quantes posicions de carretera veuen la destinació? |
| Alguna part del polígon | 0/1 | Es veu T o almenys una mostra A? |
| Àrea ponderada A | 0–100% | Quina fracció dels fragments representats té mostra visible? |
:::

`native:rastersampling` consulta cadascun dels mapes als receptors. R1–R4 corresponen a C05, C11, C13 i C37; R5, a **(352100;4552000) m**, queda fora del retall. La taula preparada és `resultats/receptors-resultats.gpkg`.

![Matriu de la torxa, algun element del polígon i fracció d'àrea als cinc receptors]({{ site.baseurl }}/assets/quarto/figures/visibilitat-matriu-real.qmd "T i G es llegeixen com 0/1; A és un percentatge ponderat de les 57 mostres interiors. Amb MDS, R1 veu la torxa i, per tant, algun element industrial, encara que cap mostra A sigui visible. R5 conserva un guió, no zero."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

>>> **Llegir R1.** T = 1, G = 1 i A = 0% amb MDS és una combinació coherent. La torxa identificada es veu, però la graella interior no l'havia mostrejada. Aquesta diferència explica per què la representació geomètrica necessita coneixement del lloc, i per què «cap mostra visible» no sempre equival a «cap element visible».

## Comparar alternatives i revisar el disseny

La comparació ha de mantenir receptors, criteris i paràmetres comuns, llevat que el canvi d'un d'aquests elements sigui precisament l'escenari estudiat. Es poden contrastar localització, extensió o altura de la proposta. Cal separar el que canvia per geometria del que canvia perquè s'ha alterat el conjunt de receptors.

Un indicador agregat pot resumir percentatge de receptors visibles o longitud d'itinerari exposada, però ha d'acompanyar-se del mapa i dels casos crítics. Dues alternatives amb el mateix total poden afectar receptors diferents. El geodisseny necessita conèixer aquesta distribució, especialment quan els efectes es concentren en llocs amb valor o ús específics.

La recomanació pot ser reduir una peça, modificar un límit o investigar una pantalla. Qualsevol mesura correctora també té efectes i manteniment: una plantació no és una barrera instantània ni immutable. La síntesi ha d'expressar quina millora s'espera, sota quines condicions i com es comprovaria.

## Activitats {#activitats-visibilitat}

### Tres lectures d'una mateixa matriu

Amb la [matriu fictícia](#exemple-intervisibilitat), cal calcular el nombre de punts de proposta visibles per receptor i el nombre de receptors calculats que veuen cada punt. Després s'ha d'explicar per què sumar tots els valors 1 dona tres relacions visibles, però no tres persones ni tres receptors diferents. La comprovació és identificar R2 com a receptor de dues relacions.

>> R1, R2 i R3 tenen, respectivament, 1, 2 i 0 punts visibles; R4 no té resultat. P1, P2 i P3 són visibles des de 2, 1 i 0 receptors calculats. Conservar aquestes dues lectures evita confondre extensió de la proposta observada amb nombre de llocs d'observació.

### Perfil resolt i conca visual

Cal seleccionar un receptor i un punt verificat de la proposta, construir-ne el perfil i explicar el resultat amb altures absolutes. Després s'ha de comparar amb la conca calculada. El document conservarà superfície, altures i obstacle determinant, amb una explicació de qualsevol discrepància.

### MDT i MDS amb extrems controlats

Amb el paquet local, calcula T sobre MDT i compara'l amb MDS mantenint T a cota 152,311996 m i els receptors a MDT + 1,7 m. T és a (346892,5;4552507,5) m; les altures relatives són 131,369997 m sobre MDT i 1 m sobre MDS. Conserva els dos ràsters binaris, la cota mínima absoluta i la màscara Domini.

Comprova aproximadament 2.962.199 cel·les visibles amb MDT i 447.860 amb MDS, dins de les 3.490.455 cel·les comparables de 5 m. Explica l'efecte de l'agregació màxima i per què 130,4 m estimats d'estructura no són una mesura de la flama.

### Acumulació i longitud de carretera

Suma les 37 conques MDT i conserva un ràster de nombre d'observadors i un de percentatge. Cada mostra representa 98,710071 m d'un total de 3.652,272633 m. Interpreta una cel·la amb valor 12: calcula longitud representada i fracció del recorregut. Comprova que no has sumat hectàrees dels mapes individuals.

Per a la visió de T amb MDS, cada mostra de la taula representa els mateixos **98,710071 m** de recorregut:

::: table "Dades per interpretar la cobertura de carretera"
| Estat en el contrast MDS | Nombre de mostres | Valor de T |
| --- | ---: | --- |
| Visible | 7 | 1 |
| Ocult | 21 | 0 |
| No calculat | 9 | Nul |
:::

Calcula 7/28 i explica per què expressa la fracció de les posicions comparables, no de tota la carretera. Si les nou desconegudes fossin ocultes o visibles, respectivament, quins límits donarien 7/37 i 16/37? Conserva les tres proporcions amb denominadors i interpretacions.

### Mostreig d'àrea i objectius singulars

Parteix de la coberta de 162,59 ha i prepara el recinte amb buffers +150 m i −150 m. Compara'n les 222,94 ha amb els resultats de 100 i 250 m. Explica per què la segona operació no recupera necessàriament la geometria original i justifica quins espais s'incorporen al recinte.

Prepara els 57 fragments d'àrea i comprova que els pesos sumen 2.229.408,741960 m². Compara el nombre de mostres visibles amb el percentatge ponderat: un fragment de vora no representa el mateix que un quadrat complet de 62.500 m².

Construeix «alguna part visible» com la unió de les mostres A i la torxa T. Amb MDS, comprova 470.444 cel·les visibles i que totes les 447.860 cel·les de la conca de T hi queden incloses. Interpreta R1, a (344977,5;4552147,5) m, amb T = 1, G = 1 i A = 0%. Explica què es perdria si s'utilitzés només la graella d'àrea.

### Exposició i valoració paisatgística

Cal redactar dues conclusions sobre el mateix resultat: una estrictament geomètrica i una valorativa, amb els criteris addicionals necessaris. La segona ha d'utilitzar una referència paisatgística documentada i identificar quines perspectives no han estat consultades. La distinció és el principal resultat de l'activitat.
