---
layout: manual-chapter
title: Estadística espacial descriptiva
description: Centres, ponderació, dispersió, orientació i densitat per descriure distribucions geogràfiques i interpretar-ne els límits.
lang: ca
ref: distribucions-punts-densitat
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/punts-densitat/
weight: 40
part: Continguts
manual_references: true
---

Un mapa amb molts establiments petits i pocs de grans pot mostrar una concentració de punts diferent de la concentració d'activitat. La mateixa distinció apareix entre equipaments i capacitat de servei, arbres i biomassa o instal·lacions i potència. Per estudiar-la cal interpretar què representa cada registre, què significa la seva coordenada i quines observacions poden entrar en una ponderació.

El recorregut comença amb una pregunta senzilla: on quedaria el punt d'equilibri de totes les localitzacions? Després s'estudia quant se separen els punts d'aquest centre, en quina direcció s'estenen i on es concentren. Les mateixes observacions d'autoconsum de l'ICAEN permeten comparar aquestes lectures i reproduir-les amb QGIS.

>>>>> En acabar el capítol, cal poder descriure una distribució puntual i justificar-ne la ponderació.
>>>>>
>>>>> - Auditar unitat, cobertura, localització i variable de ponderació d'un inventari.
>>>>> - Comparar centroide territorial, centre mitjà i centre ponderat.
>>>>> - Interpretar distància estàndard, covariància i el·lipse direccional.
>>>>> - Distingir concentració de registres, intensitat ponderada i inferència espacial.
>>>>> - Comprovar la sensibilitat a valors absents, extrems i localització.

## Del mapa de punts a una pregunta estadística {#preguntes-punts}

Un mapa de biblioteques pot respondre on són els equipaments, però no necessàriament on es concentra la capacitat de servei. Una biblioteca de 40 places i una de 400 poden aparèixer amb el mateix símbol. Si cada punt compta una vegada, s'estudia la distribució d'equipaments; si la seva contribució és proporcional a les places, s'estudia una distribució ponderada de capacitat. La mateixa distinció serveix per a arbres i biomassa o instal·lacions i potència.

Centre
: Punt que resumeix una posició d'equilibri del conjunt. El seu significat depèn de què es compta o pondera.

Dispersió
: Separació dels elements respecte del centre. Permet distingir distribucions compactes i extenses.

Orientació
: Direcció al llarg de la qual el conjunt s'estén més. Només és informativa si hi ha un allargament apreciable.

Densitat o intensitat espacial
: Quantitat per unitat de superfície sota una definició i un mètode explícits. Permet estudiar variacions locals que un únic centre no mostra.

La lectura pot començar amb quatre preguntes: on s'equilibra el conjunt?, quant s'estén?, s'allarga en alguna direcció?, i on hi ha concentracions locals? No cal escollir un únic estadístic per respondre-les totes. Centre, el·lipse i densitat són resums complementaris que s'han de contrastar amb els punts originals {% cite longley2015gis lefever1926ellipse %}.

>>> Quatre serveis se situen als vèrtexs d'un quadrat. El centre mitjà queda al mig, encara que no hi hagi cap servei allí. El centre descriu l'equilibri de les coordenades; no identifica el servei central ni recomana automàticament on construir-ne un de nou. Per a aquesta última pregunta caldrien demanda, accessos i alternatives.

## Cas d'aplicació: el registre ICAEN {#inventari-icaen}

La pàgina de [localització d'instal·lacions](https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/) integra el visor Hipermapa. La capa d'autoconsum s'anomena `ENERGIA_INSTALAUTOCONFV`. L'ICAEN declara que només s'hi representen registres amb georeferenciació vàlida i coherent. El conjunt és d'autoconsum fotovoltaic, no un cens de tota la producció solar ni una capa exclusiva de parcs sobre sòl {% cite icaenLocalitzacio %}.

La coordenada correspon al consumidor elèctric associat. En autoconsum col·lectiu és la d'un dels consumidors. Per tant, el centre espacial descriu inicialment les localitzacions que publica el registre, no necessàriament el centre de les petjades físiques dels panells. Aquesta limitació pot ser assumible a escala regional i determinant en una anàlisi parcel·lària o visual.

Cal separar **registre**, **consumidor**, **instal·lació física** i **agrupació administrativa**. Les coincidències de coordenades no demostren duplicació: diversos registres poden compartir una adreça o una posició de referència. Tampoc no s'ha de suposar que un identificador cartogràfic es manté entre edicions. La deduplicació necessita una regla basada en la documentació i en els identificadors disponibles.

### Descàrrega i preparació de les demostracions

L'activació de diverses capes al visor no implica que una descàrrega contingui totes les capes visibles. Cal revisar el contingut del paquet rebut, el nom de capa i el format real. L'exportació examinada per a la demostració es va lliurar com a GML, XML de metadades i SLD d'estil; després es va convertir a GeoPackage sense corregir les coordenades originals.

Els paquets preparats es distribueixen a Moodle. La província de Tarragona és el conjunt de partida i el Tarragonès és una selecció de treball. Un subconjunt d'entorn es pot utilitzar per estudiar sensibilitat de vora. Són seleccions solapades del mateix inventari: ajuntar-les com si fossin fonts independents duplicaria registres.

Cada paquet necessita data d'extracció, empremta, filtres i recompte. La data de descàrrega no és la data efectiva de tots els registres. En l'exportació examinada el 28 de setembre de 2026, l'XML conserva una revisió de 30 de juny de 2024 i una data de metadades de 3 de desembre de 2024. Aquesta discrepància s'ha de conservar, en lloc de presentar automàticament les dades com un cens actualitzat a setembre de 2026.

### Camps observats i controls

La inspecció de l'exportació identifica els camps següents. Aquesta taula descriu el paquet examinat; una nova edició exigeix comprovar-ne l'esquema abans de repetir el procés.

::: table "Camps de l'exportació ICAEN utilitzada en la demostració"
| Camps | Funció | Control |
| --- | --- | --- |
| `gml_id`, `OBJECTID` | Identificació dins de l'exportació | Unicitat i estabilitat dins del procés, sense pressupostar estabilitat entre edicions |
| `CODI_MUN`, `MUNICIPI`, `COMARCA`, `PROVINCIA` | Referència administrativa | Codi com a identificador i contrast amb límits de la mateixa preparació |
| `POT_KW` | Potència registrada, exportada com a enter | Valors absents, positius i extrems; no confondre amb energia |
| `UBICACIO` | Categoria publicada, com Edifici o Terra | Dominis i significat; no inferir geometria exacta |
| `INTERVAL` | Classe de potència | Coherència amb el valor quan existeix; no imputar silenciosament un punt mitjà |
| `X`, `Y` i geometria | Coordenades i objecte espacial | CRS, correspondència i ús de la geometria vigent després de transformar |
:::

El GML conté geometries MultiPoint, amb un únic punt per registre en l'extracció inspeccionada, i CRS `EPSG:25831`. Una conversió a punts simples és possible si es comprova que no altera el recompte ni duplica identificadors. Si una futura edició contingués diversos punts per registre, separar-los sense decidir com repartir la potència multiplicaria artificialment la capacitat.

### Inventaris complementaris i estats de projecte

Les altres capes de la demostració no amplien automàticament el mateix univers d'autoconsum. Les metadades de `ENERGIA_SOLAR_PARCS` descriuen plantes sobre terreny, connectades a xarxa i de més de 100 kW en servei abans del Decret llei 16/2019. `ENERGIA_PARCSSOLARS_MULTIPOLI`, en canvi, recull sol·licituds que han arribat a informació pública, amb un camp `ESTAT` que diferencia situacions {% cite hipermapaEnergia %}.

La selecció d'entitats que intersecten la província de Tarragona conté 13 punts del primer producte i 165 entitats del segon. Entre aquestes últimes, l'extracció examinada informa de 17 en servei, 76 autoritzades, 49 en tramitació, 17 no autoritzades, 5 desistides i una sense estat. Són recomptes de registres del paquet, no un cens independent de plantes actuals ni conjunts que es puguin sumar sense reconciliació.

Les geometries completes dels projectes seleccionats es conserven encara que alguna part superi el límit provincial. Així no es modifica silenciosament el suport dels atributs de superfície. La relació entre fonts requereix estudiar expedients, noms, dates i geometries; un mateix projecte podria aparèixer en productes diferents. Les bateries es mantenen com una ampliació separada, perquè emmagatzematge i generació fotovoltaica no són la mateixa tecnologia.

## Primer resultat: cobertura i valors absents {#controls-demo}

La primera demostració és una auditoria, no un mapa de clústers. Els recomptes de control de l'extracció permeten comprovar que el fitxer o el filtre utilitzat és el mateix. Els valors següents corresponen exclusivament al paquet examinat, no a un indicador de l'autoconsum vigent en qualsevol data.

::: table "Recomptes de control de la demostració amb l'extracció del 28 de setembre de 2026"
| Selecció per atribut | Registres | Potència coneguda positiva | Potència absent | Edifici / Terra |
| --- | ---: | ---: | ---: | --- |
| Província de Tarragona | 20.447 | 15.331 | 5.116 | 20.415 / 32 |
| Tarragonès | 5.102 | 3.762 | 1.340 | 5.096 / 6 |
:::

Els 1.340 valors absents del Tarragonès impedeixen calcular un centre ponderat que representi directament tots els 5.102 registres. Es pot calcular el centre dels 3.762 valors coneguts, identificant la població analitzada. El centre no ponderat de comparació ha d'utilitzar també aquests mateixos registres si es vol aïllar l'efecte de ponderar.

Convé conservar tres resultats: centre no ponderat del conjunt complet, centre no ponderat del subconjunt amb potència i centre ponderat del mateix subconjunt. La primera diferència informa de la selecció per disponibilitat; la segona, de la ponderació. Si les observacions sense potència es concentren en una zona, la mancança no és espacialment neutra.

L'extracció també presenta coordenades coincidents. Al Tarragonès hi ha 528 registres addicionals respecte del nombre de posicions diferents. Aquest recompte no justifica eliminar-los: és una qüestió de qualitat que s'ha d'interpretar amb el model del registre. Es conserven tant el recompte de registres com el de localitzacions diferents.

## Centres espacials {#centres}

El **centroide geomètric comarcal** és el centre de massa del polígon assumint densitat uniforme de superfície. Depèn del límit territorial, no de les instal·lacions. Pot quedar fora d'un polígon còncau o multipartit. Un punt garantit a l'interior és útil per etiquetar, però és un objecte diferent i no s'ha de presentar com a centroide.

El **centre mitjà** dels punts és la mitjana de les coordenades. Cada registre contribueix igualment. El **centre ponderat** dona més contribució als registres amb més pes: aquí, més potència. Si $x_i$ i $y_i$ són les coordenades del punt $i$, $p_i$ la seva potència positiva i $P$ la suma de potències:

$$
\bar{x}_p=\frac{\sum_i p_i x_i}{P},\qquad P=\sum_i p_i.
\label{eq:centre-x}
$$

$$
\bar{y}_p=\frac{\sum_i p_i y_i}{P}.
\label{eq:centre-y}
$$

Ponderar per kW descriu el centre de la **capacitat registrada coneguda**. No és el centre de l'energia generada: per a això caldrien kWh d'un mateix període. Una instal·lació pot tenir molta potència i producció anual condicionada per irradiància, orientació, disponibilitat o limitacions operatives.

### Exemple controlat

En un sistema pla docent, quatre instal·lacions se situen a (0,0), (4,0), (0,4) i (4,4) km, amb potències 10, 10, 20 i 60 kW. El centre mitjà és (2,2) km; el ponderat és (2,8;3,2) km. La instal·lació del quadrant superior dret desplaça el centre perquè aporta el 60% de la potència del conjunt, no perquè contingui més registres.

Les quatre instal·lacions i les seves coordenades són fictícies. Es calculen primer les coordenades sense pes: $(0+4+0+4)/4=2$ km per a l'est i $(0+0+4+4)/4=2$ km per al nord. Cada punt aporta una quarta part al resultat. La taula permet repetir després el càlcul amb pesos sense amagar cap pas.

::: table "Productes necessaris per calcular el centre ponderat fictici"
| Punt | Est, km | Nord, km | Potència, kW | Potència × est | Potència × nord |
| --- | ---: | ---: | ---: | ---: | ---: |
| P1 | 0 | 0 | 10 | 0 | 0 |
| P2 | 4 | 0 | 10 | 40 | 0 |
| P3 | 0 | 4 | 20 | 0 | 80 |
| P4 | 4 | 4 | 60 | 240 | 240 |
| Suma | 8 | 8 | 100 | 280 | 320 |
:::

Es divideixen les dues últimes sumes per 100 kW: $280/100=2,8$ km i $320/100=3,2$ km. Les unitats kW·km del numerador es divideixen pels kW del denominador i tornen a donar quilòmetres. Els pesos normalitzats són 0,1, 0,1, 0,2 i 0,6: sumen 1 i fan visible la contribució de cada punt.

![Comparació dels mateixos quatre punts amb pes igual i ponderats per potència: canvien centre i el·lipse, no les localitzacions]({{ site.baseurl }}/assets/quarto/figures/centres-potencia.qmd "A l'esquerra, cada registre pesa igual; a la dreta, les àrees dels símbols són proporcionals als kW ficticis. Centre i el·lipse es calculen amb els pesos de cada panell, amb semieixos d'una desviació. La creu grisa és el centroide del mateix polígon de fons i no canvia en ponderar."){: data-figure-width-web="43rem" data-figure-width-pdf="100%"}

La comparació amb un centroide territorial respon si l'inventari s'equilibra en una posició diferent del polígon. No estableix que existeixi una distribució ideal centrada en la comarca. Costa, població, activitats i disponibilitat de cobertes poden generar distribucions molt desiguals sense que el centre comarcal sigui una referència de rendiment o equitat.

>> Si totes quatre potències es dupliquen, la capacitat total passa de 100 a 200 kW, però el centre ponderat no es mou: numerador i denominador es multipliquen pel mateix factor. Si només augmenta la de P4, sí que es desplaça cap a aquell punt. Aquesta és una comprovació senzilla de la implementació.

### Escollir el resum de posició

No totes les eines que produeixen un punt central calculen el mateix. La mitjana respon a un equilibri de coordenades; altres centres responen a preguntes sobre distàncies. La taula ajuda a identificar la pregunta abans de cercar una eina.

::: table "Resums de posició i significat del punt resultant"
| Resum | Què sintetitza? | Pot coincidir amb una observació? |
| --- | --- | --- |
| Centroide d'un polígon | Distribució uniforme de la superfície | No ho exigeix |
| Centre mitjà | Mitjana de les coordenades dels punts | No ho exigeix |
| Centre mitjà ponderat | Mitjana amb contribucions desiguals | No ho exigeix |
| Mediana espacial geomètrica | Posició que minimitza la suma de distàncies euclidianes | No ho exigeix |
| Element central o medoide | Observació amb menor suma de distàncies a les altres | Sí, es tria entre les observacions |
:::

La mediana espacial geomètrica tampoc no és, en general, el punt obtingut fent per separat la mediana de $x$ i la de $y$. És important consultar la definició de cada implementació. En aquest exemple s'utilitzen els centres mitjans, que es poden comprovar amb les sumes de la taula anterior.

### Coordenades mitjanes a QGIS {#procediment-estadistica}

Amb la capa del Tarragonès en EPSG:25831, el filtre `"POT_KW" > 0` conserva 3.762 registres. **Multipart a parts simples** (`native:multiparttosingleparts`) els converteix en punts simples; en aquest paquet cada registre conté un sol punt i el recompte es manté. La capa s'anomena `ICAEN punts`.

Des de **Vectorial → Eines d'anàlisi → Coordenades mitjanes**, o cercant `native:meancoordinates` a la Caixa d'eines, es calcula primer un centre amb el pes buit. Després es repeteix amb `POT_KW` com a pes. El camp ID únic es deixa buit en tots dos casos: si s'hi triés municipi, QGIS calcularia un centre per municipi; si s'hi triés un identificador diferent per registre, no resumiria el conjunt {% cite qgisUserGuide %}.

::: subfigures a/b "Coordenades mitjanes amb QGIS 3.44.11. Els dos centres estadístics comparteixen els 3.762 registres amb potència coneguda; només canvia la contribució de cada punt."
![Diàleg de coordenades mitjanes amb POT_KW com a pes i agrupació buida]({{ site.baseurl }}/assets/captures/icaen-parametres.png "POT_KW pondera; el camp ID buit manté un únic grup.")
![Centres sense pes i ponderat i centroide comarcal sobre el mapa del Tarragonès]({{ site.baseurl }}/assets/captures/icaen-resultat.annotations.svg "Rombe blau: centre mitjà; triangle taronja: ponderat; creu fosca: centroide comarcal."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}
:::

Els punts seleccionats sumen 36.633 kW. El centre sense pes és (357.387,97; 4.556.891,17) m i el ponderat (354.528,52; 4.556.391,87) m. La ponderació el desplaça uns 2.903 m cap a l'oest i lleugerament al sud. Els decimals permeten comparar càlculs; no impliquen que les localitzacions publicades tinguin precisió centimètrica.

El **centroide comarcal** s'obté amb **Centroides** sobre el polígon del Tarragonès, no sobre els punts ICAEN. Si el límit prové de diversos municipis, primer es dissolen per formar la comarca. Fer la mitjana dels centroides municipals sense considerar les àrees donaria un altre resum.

## Dispersió i orientació {#dispersio-ellipse}

La **distància estàndard** combina la dispersió de les dues coordenades. Si $d_i$ és la distància plana de cada punt al centre ponderat, una convenció descriptiva és:

$$
D_p=\sqrt{\frac{\sum_i p_i d_i^2}{P}}.
\label{eq:distancia-estandard}
$$

El resultat conserva unitats de longitud. Un cercle amb aquest radi resumeix la separació respecte del centre de la mateixa manera en totes les direccions: és un resum **isòtrop**. Si els punts formen una banda, convé representar també quant s'estenen al llarg de la banda i perpendicularment. L'el·lipse direccional utilitza per fer-ho la variància de les coordenades i la covariància entre elles {% cite lefever1926ellipse %}.

En l'exemple sense pesos, els quatre punts disten $\sqrt{2^2+2^2}=\sqrt{8}\simeq2,83$ km del centre. Per tant, la distància estàndard també és 2,83 km. Amb pesos, el centre canvia i cada distància contribueix en proporció a la potència: el resultat és $\sqrt{5,92}\simeq2,43$ km. No s'han desplaçat les instal·lacions; s'ha canviat quina distribució es resumeix.

Per construir la matriu es resta el centre a cada coordenada. Les desviacions est–oest s'anomenen $u_i$ i les nord–sud, $v_i$. Cada quadrat o producte es pondera per la potència i es divideix per la suma dels pesos, P. Així s'obtenen les dues variàncies i la covariància:

$$
\begin{aligned}
S_{xx}&=\frac{\sum_i p_i u_i^2}{P},\\
S_{yy}&=\frac{\sum_i p_i v_i^2}{P},\\
S_{xy}&=\frac{\sum_i p_i u_i v_i}{P}.
\end{aligned}
\label{eq:covariancia-espacial}
$$

Aquestes tres quantitats permeten trobar els eixos que segueixen millor l'allargament del conjunt. El nom matemàtic de les direccions és **autovectors**; les variàncies al llarg d'aquelles direccions són els **autovalors**.

### Entendre la forma abans d'interpretar l'angle

La matriu conté tres peces d'informació. $S_{xx}$ mesura dispersió est–oest; $S_{yy}$, nord–sud; $S_{xy}$ indica si avançar cap a l'est sol anar acompanyat d'avançar cap al nord o cap al sud. En el conjunt ponderat valen 3,36, 2,56 i 0,64 km². La suma de les dues primeres és 5,92 km², exactament el quadrat de la distància estàndard. Aquesta identitat ofereix una comprovació independent.

Quan els punts formen una banda obliqua, descriure-la amb eixos est–oest i nord–sud no segueix el seu allargament. Els autovectors fan el paper d'uns eixos girats que segueixen la direcció de màxima dispersió i la perpendicular. Els autovalors indiquen quanta variància hi ha al llarg de cadascun. No són coordenades d'instal·lacions ni pesos nous.

Per a l'exemple, els autovalors són aproximadament 3,715 i 2,205 km². Les seves arrels són 1,93 i 1,49 km: aquests són els semieixos de la convenció $k=1$ utilitzada a la figura. L'eix principal forma uns 29° en sentit antihorari des de l'est. Com que l'allargament és moderat, la figura no mostra una banda estreta ni prova l'existència d'un corredor funcional.

>>>> Un eix no té sentit de circulació. Una el·lipse orientada del sud-oest al nord-est no diu que el fenomen es desplaci cap al nord-est. Per parlar de canvi temporal caldria comparar dates i conservar inventaris amb cobertures compatibles.

### Convenció de l'el·lipse

En aquest capítol es defineixen semieixos $k\sqrt{\lambda_1}$ i $k\sqrt{\lambda_2}$, amb $k$ declarat. Per a la figura docent s'utilitza $k=1$. Altres implementacions d'el·lipse direccional introdueixen factors d'escala diferents; cal comparar paràmetres, no només el nom de l'eina.

Una el·lipse amb $k=1$ no conté necessàriament el 68% dels punts. Fins i tot sota normalitat bivariant ideal, l'el·lipse de distància de Mahalanobis unitària conté aproximadament el 39,3%. Fora d'aquell model no s'ha d'atribuir un percentatge teòric sense contrast. Tampoc no és un interval de confiança del centre ni una frontera dels llocs on hi ha instal·lacions.

L'orientació és axial: 20° i 200° descriuen el mateix eix. Cal declarar si l'angle es mesura des de l'est o des del nord i en quin sentit. Un eix allargat no indica flux d'energia, direcció de creixement temporal ni causalitat d'una infraestructura. Si els autovalors són semblants, l'orientació pot ser inestable i poc informativa.

### Extrems i agrupacions

Un registre de potència elevada pot desplaçar el centre i girar l'el·lipse. Cal comprovar unitats, tipus d'instal·lació i qualitat abans d'interpretar-lo. La sensibilitat pot repetir el càlcul excloent temporalment el registre més influent, però el resultat principal ha de conservar les observacions vàlides i justificar qualsevol exclusió.

Una distribució amb dos grups separats pot tenir el centre en una zona amb pocs punts. L'el·lipse pot cobrir un espai intermedi sense activitat. Per això el mapa de punts és inseparable dels estadístics. Els resums són útils per comparar conjunts sota una convenció comuna, no per substituir l'estructura observada.

### Cercle i el·lipse de l'inventari ICAEN

Amb contribució igual dels 3.762 punts, la distància estàndard és 8.698,20 m. L'el·lipse amb $k=1$ té semieixos de 8.152,14 i 3.033,37 m, i l'eix llarg forma 12,33° en sentit antihorari des de l'est. Per tant, el conjunt s'estén més d'oest a est que de nord a sud. El cercle i l'el·lipse comparteixen centre, però destaquen propietats diferents.

![Punts ICAEN, centre mitjà, cercle de distància estàndard i el·lipse direccional]({{ site.baseurl }}/assets/quarto/figures/icaen-dispersio.qmd "El cercle resumeix la distància al centre amb un únic radi; l'el·lipse distingeix dues direccions de dispersió. Mateixos 3.762 punts i contribucions iguals. Els contorns no delimiten cobertura ni percentatges fixos d'observacions."){: data-figure-width-web="45rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICAEN i límit comarcal ICGC. EPSG:25831; elaboració pròpia."}

Per dibuixar-los a QGIS, es parteix del punt de coordenades mitjanes. La seva taula pot incorporar el radi `D_m`, els semieixos `a_m` i `b_m` i l'orientació `azimut`. El radi és l'arrel de $S_{xx}+S_{yy}$. Si es defineix $\Delta=\sqrt{(S_{xx}-S_{yy})^2+4S_{xy}^2}$, els semieixos són les arrels de $(S_{xx}+S_{yy}+\Delta)/2$ i $(S_{xx}+S_{yy}-\Delta)/2$. Així es poden repetir les operacions amb la Calculadora de camps o un full de càlcul.

::: table "Paràmetres del centre de dispersió, sense ponderar, de la selecció ICAEN"
| Camp | Valor | Significat |
| --- | ---: | --- |
| `D_m` | 8698,204203 | Radi del cercle en metres |
| `a_m` | 8152,141105 | Semieix llarg en metres |
| `b_m` | 3033,373000 | Semieix curt en metres |
| `azimut` | 77,672737 | Angle horari des del nord, igual a 90° menys l'angle des de l'est |
:::

**Geometria segons l'expressió** (`native:geometrybyexpression`) crea els polígons a partir d'aquest centre. Amb tipus de sortida polígon, `make_circle($geometry, "D_m", 72)` dibuixa el cercle i `make_ellipse($geometry, "a_m", "b_m", "azimut", 72)` l'el·lipse. El darrer nombre controla el detall amb què s'aproxima la corba. Les dues expressions fan servir magnituds prèviament calculades; no estimen la dispersió a partir d'un centre aïllat.

::: subfigures a/b "De les magnituds de dispersió als polígons de resum amb QGIS."
![Geometria per expressió amb els semieixos i l'azimut de la taula]({{ site.baseurl }}/assets/captures/dispersio-parametres.png "L'expressió llegeix els semieixos i l'azimut dels atributs del centre.")
![Cercle i el·lipse superposats als punts ICAEN en QGIS]({{ site.baseurl }}/assets/captures/dispersio-resultat.png "Cercle discontinu i el·lipse blava sobre els punts originals."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}
:::

>> Un resum direccional facilita comparar conjunts. Per explicar per què els punts s'alineen caldrien dades sobre consumidors, activitats, cobertes i altres processos. L'angle, per si sol, no identifica la causa.

## Recomptes, densitat i patrons puntuals {#densitat}

El centre resumeix tot l'inventari amb un punt. Per veure diferències locals, una primera opció és comptar registres en àrees comparables. A QGIS, **Crea una graella** (`native:creategrid`) amb tipus rectangle, separació horitzontal i vertical de 1.000 m i CRS EPSG:25831 produeix quadrats d'1 km². L'extensió ha de cobrir tots els punts.

**Compta els punts al polígon** (`native:countpointsinpolygon`) rep la graella com a capa de polígons i `ICAEN punts` com a capa puntual. Es deixen buits pes i classe i s'anomena `n_punts` el camp de resultat. La suma d'aquest camp és 3.762: cada registre ha quedat assignat una vegada. Un quadrat amb 8 registres té 8 punts/km²; si es retalla un quadrat per la costa, cal dividir pel nou valor d'àrea si es vol una densitat per superfície terrestre.

![Diàleg de recompte de punts dins de la graella de polígons]({{ site.baseurl }}/assets/captures/graella-recompte.png "La graella defineix les unitats; n_punts conserva el recompte. Amb el pes buit, cada registre contribueix una vegada."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

La graella imposa vores: dos punts pròxims poden caure en quadrats diferents. Desplaçar-ne l'origen és una prova útil de sensibilitat. Si es vol una superfície sense salts entre quadrats, es pot repartir la contribució de cada punt en el seu entorn.

### Densitat kernel i escala de suavització

Una estimació kernel reparteix contribucions dels punts sobre l'espai. Sense pesos, descriu intensitat de registres sota la normalització adequada; amb pesos en kW, pot descriure concentració de capacitat coneguda. En tots dos casos, l'amplada de banda determina l'escala de suavització. Cal provar-ne més d'una i mantenir-les comparables entre subconjunts.

La idea es pot imaginar com un petit relleu suau centrat en cada punt. Molt a prop, la contribució és alta; a mesura que augmenta la distància, disminueix. A cada posició se sumen les contribucions de tots els punts. L'**amplada de banda**, sovint indicada amb $h$, controla fins a quin entorn es reparteix cadascuna. No és la mida de la cel·la: la cel·la fixa el detall amb què es representa la superfície ja estimada.

![Dos mapes kernel dels mateixos vuit punts ficticis, amb amplades de banda petita i gran i una llegenda comuna]({{ site.baseurl }}/assets/quarto/figures/densitat-radi.qmd "Els mateixos vuit punts produeixen concentracions locals més marcades amb h = 0,4 km i una superfície més suau amb h = 1,2 km. Kernel gaussià normalitzat, amb una contribució total unitària per punt sobre el pla complet. Llegenda comuna en punts/km²; no són valors crus del mapa de calor de QGIS."){: data-figure-width-web="35.5rem" data-figure-width-pdf="85%"}

En la figura, ampliar $h$ fa menys alts els pics i reparteix la mateixa contribució en una zona més ampla. No s'han perdut punts; ha canviat l'escala de la pregunta. Una amplada petita és sensible a grups molt locals i a errors de localització. Una de gran ajuda a veure tendències àmplies, però pot fusionar concentracions diferents. Cap de les dues és correcta només perquè produeix un mapa més suau.

>>> Si s'aplica una quadrícula de recompte i una cel·la d'1 km² conté 8 punts, la densitat és 8 punts/km². Si conté una suma de 80 kW coneguts, són 80 kW/km². En un kernel, en canvi, una cel·la pot rebre contribucions de punts exteriors: el seu valor no es llegeix com el recompte de punts que físicament cauen dins.

El valor cru d'un mapa de calor de QGIS no s'ha d'etiquetar automàticament com a instal·lacions o kW per hectàrea. Cal comprovar el tipus de kernel, la normalització, el radi, les unitats i el significat de la sortida. Una cel·la amb valor alt no conté necessàriament una instal·lació ni acredita aptitud per a una de nova.

Les vores i les zones on el fenomen pot existir importen. Un model homogeni sobre tota la comarca pot tractar com a possibles localitzacions el mar o espais sense consumidors. La funció K de Ripley permet estudiar relacions entre punts a diverses distàncies, però necessita una finestra d'observació i un model nul adequats {% cite ripley1976second %}. Rebutjar homogeneïtat en un territori urbà i rural no demostra per si sol interacció entre instal·lacions.

Les agrupacions de DBSCAN i k-means són exploratòries. No proporcionen significació estadística pel fet de dibuixar grups. El capítol següent estudiarà autocorrelació d'atributs en unitats territorials; aquest és un altre problema, que no valida automàticament els grups puntuals d'aquest inventari.

### Mapa de calor amb QGIS

**Mapa de calor — KDE** (`qgis:heatmapkerneldensityestimation`) rep `ICAEN punts`, radi 1.500 m i píxel de 100 m. A les opcions avançades es tria kernel **Quartic**, sense camp de pes i amb sortida **Raw**. Es repeteix amb radi 500 m, mantenint la mateixa mida de píxel. El radi canvia l'entorn d'influència; el píxel només canvia on s'avalua la superfície.

![Diàleg de mapa de calor amb radi 1500 m i píxel 100 m]({{ site.baseurl }}/assets/captures/kernel-parametres.png "Radi i mida de píxel tenen funcions diferents. El camp de pes buit conserva una contribució igual per punt."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

En aquest kernel, la contribució crua a distància $d<h$ és $(1-(d/h)^2)^2$ i fora del radi és zero. El volum sota cada contribució és $\pi h^2/3$. Per obtenir punts/km², la Calculadora ràster multiplica la sortida crua per $3\times10^6/(\pi h^2)$, amb $h$ en metres. Amb 1.500 m, el factor és aproximadament 0,424413; amb 500 m, 3,819719. Aquesta conversió fa comparables les unitats dels dos radis.

![Recompte en graella i dos mapes kernel amb radis de 500 i 1500 m]({{ site.baseurl }}/assets/quarto/figures/icaen-densitat.qmd "A: cada quadrat resumeix els punts que conté. B i C: densitat quartic normalitzada a punts/km², amb radi diferent i escala de color comuna. Els tres panells utilitzen els mateixos 3.762 registres; cap color representa significació estadística."){: data-figure-width-web="49rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICAEN i ICGC. Càlcul QGIS i normalització analítica del kernel."}

La graella mostra concentracions dins d'unitats fixes; el radi de 500 m conserva pics locals, i el de 1.500 m els uneix en àrees més àmplies. La contribució s'estén també fora del límit comarcal perquè el kernel no coneix aquella frontera. Retallar el mapa no corregeix l'absència de punts externs ni converteix la superfície en una probabilitat.

## De punts a seccions: potència i antiguitat {#potencia-antiguitat}

Després dels quadrats regulars, es pot resumir l'inventari en una partició administrativa: les **seccions censals**. Cada fila de la nova taula descriu una secció sencera. La primera pregunta és quina potència coneguda s'hi concentra; una segona pregunta, opcional, compara aquest indicador amb l'antiguitat de l'edificació. Agregar vol dir reunir les contribucions dels objectes que pertanyen a cada àrea.

La demostració combina les [seccions censals de l'ICGC i l'Idescat](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Seccions-censals), edició 1 de gener de 2024, amb l'inventari ICAEN ja descrit i els [edificis INSPIRE del Cadastre](https://www.catastro.hacienda.gob.es/INSPIRE/Buildings/43/ES.SDGC.BU.atom_43.xml), feed de 21 d'agost de 2026 {% cite icgc2024seccions cadastre2026buildings %}. El paquet de pràctica conserva les fonts, els codis municipals verificats i els resultats agregats. Els codis del servei cadastral no s'han de confondre amb els de l'INE.

### Un indicador comparable entre seccions

Els punts ICAEN s'assignen per posició als polígons de secció. En aquest cas s'utilitzen els registres de categoria `Edifici`: 5.096 consumidors, 3.757 amb potència positiva coneguda, que sumen 36.058 kW. No s'està atribuint cada consumidor a un edifici cadastral concret. Les sis observacions sobre terra queden fora d'aquest indicador, encara que apareguessin en el càlcul anterior dels centres.

Per reduir l'efecte del nombre d'edificis de cada secció, es defineix:

$$
q_s=100\,\frac{\sum_{i\in s,\,p_i\text{ coneguda}}p_i}{B_s}.
\label{eq:potencia-seccio}
$$

$p_i$ és la potència registrada coneguda, en kW, i $B_s$ el nombre d'objectes cadastrals `Building` en estat funcional assignats a la secció $s$. L'assignació d'aquests polígons utilitza un punt interior, amb control de casos sense correspondència. S'obtenen 38.689 objectes funcionals al conjunt. **Un edifici cadastral no és un habitatge**: aquest denominador no mesura llars ni persones i pot combinar usos diferents. Tampoc corregeix l'absència de potència en part de l'inventari; $q_s$ és una suma coneguda normalitzada, no la capacitat total real.

>>> Una secció fictícia amb 800 kW coneguts i 200 edificis té $100\times800/200=400$ kW per 100 edificis. Una altra amb 800 kW i 400 edificis té 200 kW per 100 edificis. La suma de potència és igual, però la relació amb el nombre d'edificis és diferent. «Per 100» és una escala de presentació, no una selecció de cent edificis.

A QGIS es poden assignar punts ICAEN i punts interiors dels edificis a les seccions amb **Uneix atributs per localització**. Després s'agrupa pel codi de secció: suma de potències conegudes, nombre d'edificis funcionals i cobertura del registre. La Calculadora de camps aplica la fórmula quan el denominador és positiu. Una secció amb registres però totes les potències absents es conserva sense indicador.

### Afegir l'antiguitat de l'edificació

L'antiguitat és una segona variable, no un requisit per estudiar espacialment la primera. Aquí es calcula respecte de 2026 i es resumeix amb la mediana. El Cadastre pot donar un any inicial i un de final, corresponents a les unitats constructives més antiga i més moderna. Per obtenir una edat única es retenen els 31.302 objectes funcionals amb tots dos anys iguals. Els 7.368 amb anys diferents i els 19 sense data vàlida no entren en aquesta mediana; els dos anys no formen un interval de confiança.

![Mapes de potència registrada per cent edificis funcionals i d'antiguitat mediana a les seccions del Tarragonès]({{ site.baseurl }}/assets/quarto/figures/seccions-tarragones.qmd "Dos atributs agregats sobre les 151 seccions de 2024. A: kW coneguts de categoria Edifici per 100 objectes cadastrals funcionals; una secció només amb potències absents queda sense indicador. B: mediana d'antiguitat dels objectes amb any inicial igual al final; es requereixen almenys deu casos. Les fonts tenen dates diferents."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICGC/Idescat, Cadastre i ICAEN. Agregació i cartografia pròpies; EPSG:25831. Contorns simplificats només per dibuixar."}

### Llegir una associació observada

La correlació utilitza les 126 seccions amb almenys deu edificis d'any únic i almenys una potència coneguda. Es relaciona l'antiguitat mediana amb $y_s=\log(1+q_s)$, on el logaritme és natural i $q_s$ s'expressa numèricament en les unitats definides. La transformació comprimeix els valors més elevats; afegir 1 permet representar zero, però l'escala i la constant formen part de la definició. Aquesta anàlisi respon a una pregunta transformada, no a una relació lineal directa en kW.

En aquesta mostra, $r=-0,401$ i $R^2=0,161$. La recta és aproximadament $\hat y=5,194-0,02093a$, amb $a$ en anys. Les seccions més antigues tendeixen a tenir menys potència coneguda per edifici, però hi ha molta variació que aquesta recta no resumeix. Si es correlaciona l'edat amb el logaritme de la suma de kW sense normalitzar per edificis, $r$ és −0,278: canviar el denominador modifica la pregunta i el resultat.

![Núvol d'antiguitat i potència normalitzada amb regressió, i gràfic dels residus]({{ site.baseurl }}/assets/quarto/figures/potencia-antiguitat.qmd "Associació descriptiva entre 126 seccions. La recta resumeix una tendència negativa; els residus són les diferències entre observat i ajustat. Cada punt és una secció, no un edifici."){: data-figure-width-web="49rem" data-figure-width-pdf="100%"}

La interpretació ha de considerar usos industrials i residencials, tipus d'edificació, nombre d'habitatges, renda, règim de tinença i cobertura del registre. No s'han controlat aquestes variables. Les potències absents i l'exclusió dels edificis amb anys diferents també poden alterar el patró. El [capítol d'autocorrelació](../dependencia-espacial/#cas-seccions) estudia la dependència espacial del mateix indicador; la regressió aquí no demostra que l'antiguitat causi menys autoconsum.

## Activitats

### Predir el canvi abans de recalcular

Amb els quatre punts ficticis, cal anticipar què passarà en duplicar totes les potències, en duplicar només P4 i en eliminar P4. Després es recalculen els centres i es compara la predicció amb el resultat. El lliurament ha d'explicar el mecanisme del desplaçament, no només donar coordenades.

>> Duplicar totes les potències conserva (2,8;3,2). Si només P4 passa de 60 a 120 kW, el total és 160 kW i el centre passa a (3,25;3,50). Si es retira P4, queden 40 kW i el centre ponderat és (1;2). Retirar una observació vàlida només per canviar el resultat no seria una decisió de neteja legítima; aquí és una prova explícita de sensibilitat.

### Auditoria de l'extracció

Cal reproduir els recomptes de la demostració o explicar les diferències d'edició. La taula conservarà cobertura, potències absents, geometries coincidents i categories. El resultat ha d'identificar almenys una decisió d'anàlisi que canviï a causa d'aquests controls.

### Tres centres i un límit territorial

Cal comparar el centroide comarcal amb els tres centres descrits: conjunt complet, subconjunt conegut sense pes i subconjunt conegut ponderat. La interpretació ha de separar efecte de selecció i de ponderació. El mapa i la taula de coordenades han d'indicar CRS i denominadors.

### Eix i sensibilitat

Cal reproduir el cercle i l'el·lipse sense pes i comparar-los amb la distribució ponderada per potència. Es conservaran centre, radi, semieixos i orientació. La interpretació ha d'explicar què canvia en la contribució dels punts i què es manté en les seves localitzacions.

### Recompte i potència sobre la mateixa graella

Cal comparar un KDE de registres i un de potència coneguda, amb dos radis. El resultat serà una lectura de les concentracions que apareixen i desapareixen i de l'efecte dels valors absents. No s'ha d'utilitzar cap de les dues superfícies com a mapa directe d'idoneïtat.
