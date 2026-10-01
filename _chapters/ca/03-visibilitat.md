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

Primer es comprova una línia entre dos punts. A continuació es repeteix el càlcul cap a moltes posicions per construir una conca visual, i des de diversos llocs per comparar vistes. Els exemples d'una carretera i d'un sector de la refineria ajuden a passar del perfil del terreny als mapes i a les eines de QGIS.

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

### Donar significat a la freqüència acumulada

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

## Calcular una conca i consultar-la als receptors amb QGIS {#procediment-visibilitat}

El treball amb QGIS combina dues operacions: **Conca visual / Viewshed** calcula un mapa des d'un punt, i **Mostreja els valors ràster** consulta aquell mapa a les posicions dels receptors. Repetir el primer càlcul per a cada punt P i el segon sobre els mateixos receptors R permet construir les columnes d'una matriu com l'anterior.

Els polígons de sol·licituds de parcs solars permeten estudiar alternatives amb extensió explícita, però cal llegir-ne `ESTAT` i la documentació. Una superfície autoritzada o en tramitació no és una prova que els panells ja estiguin construïts. Per estudiar una proposta es conserva aquesta condició; per estudiar una instal·lació existent cal contrastar construcció, data, altura i disposició.

### Preparar extrems i paràmetres

Cal crear una capa de receptors amb identificador, funció i altura relativa, i una capa de punts de la proposta amb el criteri de mostreig. Si una geometria prové d'una comprovació de l'inventari ICAEN, s'ha de conservar la relació amb el registre sense substituir la coordenada original. Les altures s'han de documentar com a mesurades, derivades o assumides.

Una fitxa de paràmetres ha d'incloure resolució, superfície, altures, abast, correcció de curvatura/refracció i codis de sortida. La primera execució hauria de correspondre a un parell d'extrems amb un perfil conegut. Això permet detectar una altura referida a la superfície incorrecta o una interpretació inversa de la sortida.

::: table "Del concepte al paràmetre d'una conca visual"
| Decisió | Entrada que cal revisar | Comprovació observable |
| --- | --- | --- |
| Què pot ocultar la visió? | MDT o MDS, banda i nuls | L'obstacle del perfil és present a la superfície |
| Des d'on es mira? | Coordenades de l'observador i CRS | El punt coincideix amb el receptor previst |
| A quina altura? | Altura d'observador i d'objectiu | No s'ha duplicat la cota del sòl |
| Fins on es calcula? | Abast màxim i extensió | Fora de l'abast es conserva «no calculat» |
| Què vol dir cada valor? | Codis visible, ocult i nul | La llegenda coincideix amb la sortida real |
:::

### Calcular i contrastar

QGIS incorpora `gdal:viewshed`; GRASS ofereix `r.viewshed` quan està disponible. Cal consultar l'ajuda de la versió utilitzada i conservar les convencions dels paràmetres {% cite qgisUserGuide %}. El càlcul per lots permet repetir el mateix model per diversos punts, però exigeix revisar la correspondència entre identificadors, altures i noms de sortida.

En l'exemple de QGIS es pren un retall del MDT de l'entorn de la refineria nord. El punt central de la instal·lació se situa a (350.900,88;4.560.059,92) m. S'hi assumeix una altura de 30 m, mentre que a les cel·les del territori s'avaluen receptors a 1,7 m. L'«observador» de la interfície és aquí el punt de la instal·lació: la línia de visió es comprova en sentit invers per respondre des d'on es podria veure.

![Diàleg de conca visual amb model d'elevacions, origen i altures assenyalats]({{ site.baseurl }}/assets/captures/visibilitat-parametres.png "Viewshed, de GDAL: superfície, posició, altures i abast. El primer càlcul produeix el mapa visible/ocult del punt central."){: data-figure-width-web="43rem" data-figure-width-pdf="100%"}

Després es carrega la capa de caps de municipi. L'eina `native:rastersampling`, **Mostreja els valors ràster**, rep la capa de punts i la conca visual. El prefix identifica de quin punt de la instal·lació prové la nova columna.

![Mostreig d'una conca visual als punts dels receptors]({{ site.baseurl }}/assets/captures/intervisibilitat-mostreig.png "Mostreja els valors ràster afegeix la resposta del mapa a la taula de punts. La banda 1 i el prefix centre_ produeixen el camp centre_1."){: data-figure-width-web="43rem" data-figure-width-pdf="100%"}

Amb codis de sortida 1 per a visible i 0 per a ocult, el mostreig dona 1 al punt de Perafort i 0 al de Constantí. La nova columna es pot anomenar `centre_1`. No s'està classificant tot el municipi: és la resposta en el punt representatiu carregat. Per afegir una altra columna es calcula la conca d'un altre punt de la instal·lació i es repeteix el mostreig sobre la mateixa capa de receptors.

>> A l'eina de GDAL, distància màxima 0 significa calcular sobre tota l'extensió del ràster, no una visió de radi zero. La llegenda també ha de correspondre als codis escollits: en aquesta execució es configura visible=1, ocult=0 i no calculat=255.

La primera sortida s'inspecciona com a valors, no només com a colors. Amb l'eina d'identificació de QGIS es consulta un lloc que el perfil prediu com a visible, un d'ocult i un de fora d'abast. Després es configura una simbologia categòrica amb etiquetes explícites. Una rampa contínua entre 0 i 1 podria suggerir una gradació que el resultat binari no conté.

Les conques es combinen només quan comparteixen graella i domini vàlid. Un remostreig de visibilitat binària ha de respectar el significat categòric: la interpolació bilineal de 0 i 1 no produeix una probabilitat de visió. Si cal canviar resolució, convé recalcular o definir explícitament una proporció de cel·les, que és una magnitud diferent.

La intersecció amb receptors es pot resoldre mostrejant el ràster als punts, amb identificadors estables. Cal registrar no visible, visible i no calculat. Per a trams o superfícies, el resum ha d'explicar si es basa en punts, longitud o àrea. El perfil entre un receptor i una part de la proposta ajuda a interpretar els resultats i a localitzar l'obstacle determinant.

### Controls mínims de lectura

El mapa ha d'identificar proposta, receptors, domini i font d'elevacions. La llegenda no hauria de dir «impacte nul» on el model només diu «no visible». Cal inspeccionar almenys un cas visible, un d'ocult i un de pròxim al límit de visió, perquè aquest últim és més sensible a errors d'altura o resolució.

Una comprovació sobre ortofoto o terreny pot confirmar obstacles que el model omet. La discrepància s'ha d'utilitzar per revisar el model, no per ajustar els paràmetres fins que coincideixin amb una resposta desitjada. Si manca informació, es conserva com a incertesa del resultat.

## Representar un sector petroquímic amb un punt o amb moltes mostres {#cas-petroquimica}

Un centre és una primera simplificació d'una instal·lació extensa. Però una part situada uns centenars de metres més enllà pot aparèixer per darrere d'un turó que n'ocultava el centre. Per observar aquest efecte es comparen un punt central i un conjunt de mostres, sobre **Tarragonès i Baix Camp**.

Les elevacions provenen dels [models territorials de l'ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions/Elevacions-territorial/Models-delevacions): MDT LiDAR de 5 m i MDS LiDAR d'1 m, període 2021–2023. El paquet conté versions regionals reduïdes a 25 m, alineades en EPSG:25831. Aquesta reducció facilita l'experiment comarcal, però pot suavitzar edificis, vegetació i estructures estretes. No s'ha d'interpretar el MDS de 25 m com un inventari d'altures de torres.

### Representar la instal·lació i les altures

S'utilitza la parcel·la `1406801CF5610C`, de 171,63 ha, a la Pobla de Mafumet. Representa un sector de la refineria nord. El seu centre geomètric es compara amb **28 punts** d'una malla de 250 m que queden dins del polígon. Són posicions de mostreig; no s'han identificat com a torres.

L'escenari base assumeix objectius a 30 m sobre el terreny i receptors a 1,7 m. Per calcular el mapa s'aprofita la reciprocitat geomètrica de la línia de visió: es llança la conca des del punt de la instal·lació, a 30 m, cap a possibles receptors a 1,7 m. Les altures es mantenen associades als extrems físics quan s'inverteix la pregunta. El resultat és numèric i depèn del mètode discret emprat; no és una comprovació visual de camp.

El càlcul incorpora el coeficient de curvatura i refracció **0,85714** de [GDAL](https://gdal.org/en/stable/programs/gdal_viewshed.html). A diferència del perfil curt inicial, aquí les distàncies comarcals fan rellevant considerar la forma de la Terra.

### Cobertura abans de comptar visibilitat

Quan falta una elevació, no se sap si aquell lloc tapa una línia de visió. Les posicions afectades queden fora de la comparació i s'utilitza la mateixa zona calculable en tots els escenaris. El mar es representa com una superfície plana a 0 m. Així es pot comparar la proporció visible sense canviar inadvertidament què es compta.

>>>> «Ocult» significa que s'ha calculat una línia i hi ha un obstacle. «No calculat» significa que falta una condició per decidir-ho. Convertir totes dues situacions en zero faria semblar menys visible un lloc simplement perquè hi ha menys informació.

![Dos mapes disposats verticalment comparen la conca del centre i l'acumulació de vint-i-vuit mostres]({{ site.baseurl }}/assets/quarto/figures/visibilitat-petroquimica.qmd "A: visibilitat d'un únic centre. B: nombre de punts visibles entre les 28 mostres del sector. La gradació permet distingir veure'n una petita part de veure'n moltes posicions. Objectius a 30 m i receptors a 1,7 m sobre el terreny, amb el mateix àmbit calculable."){: data-figure-width-web="38.5rem" data-figure-width-pdf="91%" data-caption-source="Fonts: elevacions i límits ICGC; parcel·la de la Dirección General del Catastro. Càlcul a 25 m, representació a 100 m."}

::: table "Què canvia en ampliar les mostres o modificar l'altura?"
| Representació | Altura d'objectiu | Altura de receptor | Proporció visible de l'àmbit calculable |
| --- | ---: | ---: | ---: |
| Centre | 30 m | 1,7 m | 15,8% |
| Almenys una de 28 mostres | 30 m | 1,7 m | 19,8% |
| Centre més alt | 60 m | 1,7 m | 23,6% |
| Centre, receptors elevats | 30 m | 15 m | 31,7% |
:::

Augmentar l'altura de l'objectiu o la del receptor amplia la superfície potencialment visible en aquests escenaris. Això no quantifica població exposada ni afirma que existeixin torres de 60 m o receptors a 15 m en totes les cel·les. Per estudiar edificis concrets caldria situar receptors, obtenir altures i diferenciar carrer, finestres i coberta. Tampoc no es pot traduir l'àrea visible directament en magnitud d'impacte paisatgístic.

### Com ampliar la prova amb el MDS

Els controls anteriors corresponen al **MDT**. El MDS regional s'inclou com a entrada de contrast. Per comparar obstacles cal mantenir les altures absolutes dels extrems: un receptor a 1,7 m sobre el terreny no passa automàticament a estar a 1,7 m sobre una teulada. Si l'eina només admet una altura relativa constant sobre el ràster d'entrada, cal modificar el plantejament o seleccionar receptors amb correccions individuals; reutilitzar els mateixos dos nombres no garanteix una comparació controlada.

Tornar al perfil ajuda a interpretar els canvis: es pot triar un lloc visible, un d'ocult i un de proper al límit, i comprovar quin obstacle és determinant. Aquesta lectura connecta els colors del mapa amb el raonament de la primera figura.

## Comparar alternatives i revisar el disseny

La comparació ha de mantenir receptors, criteris i paràmetres comuns, llevat que el canvi d'un d'aquests elements sigui precisament l'escenari estudiat. Es poden contrastar localització, extensió o altura de la proposta. Cal separar el que canvia per geometria del que canvia perquè s'ha alterat el conjunt de receptors.

Un indicador agregat pot resumir percentatge de receptors visibles o longitud d'itinerari exposada, però ha d'acompanyar-se del mapa i dels casos crítics. Dues alternatives amb el mateix total poden afectar receptors diferents. El geodisseny necessita conèixer aquesta distribució, especialment quan els efectes es concentren en llocs amb valor o ús específics.

La recomanació pot ser reduir una peça, modificar un límit o investigar una pantalla. Qualsevol mesura correctora també té efectes i manteniment: una plantació no és una barrera instantània ni immutable. La síntesi ha d'expressar quina millora s'espera, sota quines condicions i com es comprovaria.

## Activitats

### Tres lectures d'una mateixa matriu

Amb la [matriu fictícia](#exemple-intervisibilitat), cal calcular el nombre de punts de proposta visibles per receptor i el nombre de receptors calculats que veuen cada punt. Després s'ha d'explicar per què sumar tots els valors 1 dona tres relacions visibles, però no tres persones ni tres receptors diferents. La comprovació és identificar R2 com a receptor de dues relacions.

>> R1, R2 i R3 tenen, respectivament, 1, 2 i 0 punts visibles; R4 no té resultat. P1, P2 i P3 són visibles des de 2, 1 i 0 receptors calculats. Conservar aquestes dues lectures evita confondre extensió de la proposta observada amb nombre de llocs d'observació.

### Perfil resolt i conca visual

Cal seleccionar un receptor i un punt verificat de la proposta, construir-ne el perfil i explicar el resultat amb altures absolutes. Després s'ha de comparar amb la conca calculada. El document conservarà superfície, altures i obstacle determinant, amb una explicació de qualsevol discrepància.

### MDT i MDS amb extrems controlats

Cal comparar una representació de sòl i una de superfície, mantenint justificades les posicions absolutes dels extrems. El resultat ha de distingir l'efecte dels obstacles del que produiria situar l'observador damunt d'una coberta. No s'accepta una conclusió basada només en el recompte de cel·les visibles.

### Mostreig de la instal·lació

Cal comparar un únic punt amb un conjunt justificat de punts de la proposta. La matriu receptor–punt ha de mostrar quines parts generen visibilitat addicional. El resultat serà una proposta de modificació geomètrica i la seva nova estimació d'exposició.

### Exposició i valoració paisatgística

Cal redactar dues conclusions sobre el mateix resultat: una estrictament geomètrica i una valorativa, amb els criteris addicionals necessaris. La segona ha d'utilitzar una referència paisatgística documentada i identificar quines perspectives no han estat consultades. La distinció és el principal resultat de l'activitat.
