---
layout: manual-chapter
title: Geoestadística i interpolació
description: Observacions XEMA, IDW, semivariograma i kriging amb QGIS, validació i ampliació amb covariables.
lang: ca
ref: superficies-continues
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/superficies-continues/
weight: 60
part: Continguts
manual_references: true
---

La temperatura, la precipitació o determinades propietats del sòl s'observen parcialment, mentre que moltes preguntes territorials necessiten informació entre els llocs mostrejats. La interpolació estima valors sota un model de relació espacial; la geoestadística n'estudia la dependència i la incertesa. La pregunta, el suport i la validació determinen si aquesta estimació és adequada.

El capítol parteix de les temperatures màximes observades a Catalunya el 15 d'agost de 2025. Primer s'estima entre estacions amb una regla de distància, IDW; després s'estudia com varien les diferències entre estacions segons la separació i s'introdueix el kriging. QGIS permet seguir aquests passos sobre les mateixes dades. La regressió amb altitud i el kriging dels residus s'incorporen més endavant, quan ja es pot entendre què afegeixen al model.

>>>>> En acabar el capítol, cal poder construir i validar una predicció espacial amb suport explícit.
>>>>>
>>>>> - Definir variable, suport espacial i temporal i domini de predicció.
>>>>> - Calcular una estimació IDW i interpretar un semivariograma.
>>>>> - Configurar IDW i kriging a QGIS i explicar el paper posterior de les covariables.
>>>>> - Interpretar variància condicional, errors de validació i extrapolació.
>>>>> - Justificar si la covariable millora el model i com entra en la decisió territorial.

## D'una observació a un valor estimat {#idea-interpolacio}

Una estació mesura 20 °C i una altra 26 °C. Quina temperatura s'assignaria a un lloc situat entre totes dues? Fer la mitjana, 23 °C, és una primera regla possible, però ignora si el lloc és molt més pròxim a la primera i si té una altitud diferent. Interpolar consisteix a explicitar una regla que relacioni observacions i posició per produir una estimació {% cite burrough1998principles %}.

Interpolació
: Estimació en posicions no observades a partir de dades i d'un model. L'estimació no es converteix en una nova observació independent.

Covariable
: Informació auxiliar disponible als punts observats i als llocs on es vol predir, com l'altitud derivada d'un MDT.

Tendència
: Part de la variació que es representa mitjançant posició o covariables. En una regressió amb altitud és el valor ajustat per aquella relació.

Residu
: Diferència entre observació i tendència als punts d'ajust. Pot conservar variació espacial que la tendència no explica.

### Una primera regla: ponderar per distància

La ponderació per l'invers de la distància, **IDW**, dona més contribució als punts pròxims. Amb distàncies positives $d_i$ i exponent $p>0$, els pesos normalitzats són:

$$
\lambda_i=\frac{d_i^{-p}}{\sum_j d_j^{-p}}.
\label{eq:idw-pesos}
$$

La predicció és $\widehat{T}=\sum_i\lambda_iT_i$. La suma dels pesos és 1. Si una posició coincideix amb una observació, la regla ha de tractar aquest cas expressament per evitar dividir per zero. També cal fixar quins punts entren en el veïnatge de predicció.

>>> En un exemple fictici, el lloc és a 1 km de l'estació de 20 °C i a 2 km de la de 26 °C. Amb $p=2$, els pesos sense normalitzar són 1 i 1/4; dividits per 1,25 esdevenen 0,8 i 0,2. La predicció és $0,8\times20+0,2\times26=21,2$ °C. No són 23 °C perquè la primera observació pesa quatre vegades més.

Amb $p=1$, els pesos serien 2/3 i 1/3 i la predicció, 22 °C. Augmentar l'exponent fa més local la influència dels punts propers. Aquesta és una decisió de model que es pot contrastar, no un paràmetre que es tria perquè produeix una imatge agradable. IDW tampoc introdueix altitud automàticament: dos llocs amb les mateixes distàncies als punts rebrien el mateix resultat encara que el seu relleu fos diferent.

IDW ofereix una primera superfície que es pot comparar amb altres mètodes. El kriging també combina observacions, però calcula els pesos a partir d'un model de diferències espacials. Abans d'explicar aquest model convé preparar una variable que signifiqui el mateix a totes les estacions.

## Cas d'aplicació: definir l'indicador tèrmic {#variable-temporal}

La màxima diària és el valor més alt observat durant un dia segons la definició temporal del productor. La **mitjana de màximes d'agost** resumeix aquestes màximes durant un agost concret o un període d'anys explícit. No equival a la màxima absoluta d'agost ni a la temperatura d'un episodi de calor simultani a totes les estacions.

### Màximes del 15 d'agost de 2025

La [Xarxa d'Estacions Meteorològiques Automàtiques, XEMA](https://www.meteo.cat/wpweb/serveis/dades-obertes/), del Servei Meteorològic de Catalunya, publica observacions i metadades d'estacions {% cite meteocatDadesObertes %}. Al portal de dades obertes es poden filtrar les [observacions](https://analisi.transparenciacatalunya.cat/d/nzvn-apee) pel codi de variable **40, Temperatura màxima**, i pel dia **2025-08-15**. La variable i la unitat, °C, es contrasten amb les [metadades de variables](https://analisi.transparenciacatalunya.cat/d/4fb2-n3yi).

Cada registre utilitzat resumeix mitja hora. Les metadades indiquen que `data_lectura` és l'inici de l'interval i que l'hora s'expressa en **Temps Universal, TU**. Es trien els intervals des de les 00:00 fins a les 23:30 del mateix dia, amb estat `V` —vàlid— i base temporal `SH` —semihorària—. La màxima diària de l'exemple és el màxim dels 48 valors, no la seva mitjana.

Les coordenades i l'altitud s'obtenen de les [metadades d'estacions](https://analisi.transparenciacatalunya.cat/d/yqwd-vj5e), unides pel codi. Es requereixen 48 intervals diferents, un valor vàlid en cadascun i metadades compatibles amb la data. De les 183 estacions amb observacions descarregades, una no tenia correspondència a la taula de metadades; el conjunt final té **182 estacions**, amb màximes entre **17,6 i 42,6 °C**.

::: table "Camps de la capa de temperatures utilitzada a QGIS"
| Camp | Significat | Unitat o control |
| --- | --- | --- |
| `codi`, `nom` | Estació de la XEMA | Codi únic per unir observacions i metadades |
| `tx_c` | Màxim de les 48 màximes semihoràries vàlides | °C |
| `dia_tu` | Dia comú de l'indicador | 2025-08-15, en TU |
| `n` | Intervals admesos | 48 a cada estació |
| `alt_m` | Altitud publicada | Metres; disponible per a una ampliació amb relleu |
:::

A QGIS, la taula de coordenades geogràfiques s'incorpora amb EPSG:4326 i s'exporta a **ETRS89 / UTM 31N, EPSG:25831**, perquè les distàncies del model es calculin en metres. El paquet docent de Moodle conserva la capa preparada i les observacions de partida. Les metadades són una instantània del catàleg; un estudi climàtic de diversos anys hauria de considerar també la història de les estacions i possibles relocalitzacions. L'ús de les dades segueix l'[avís legal de Meteocat](https://www.meteo.cat/wpweb/avis-legal/).

### Canviar de dia a període

Per a una estació $i$ i un conjunt de dies vàlids $D$, la mitjana de màximes és:

$$
\overline{T_{\max}}(s_i)=\frac{1}{|D|}\sum_{d\in D}T_{\max}(s_i,d).
\label{eq:tmax-agost}
$$

Si cada estació utilitza dies diferents, es poden comparar suports temporals diferents. Una estació que perdi precisament els dies més càlids pot semblar més fresca. Cal conservar calendari, nombre de dies vàlids, regles de qualitat i criteri de comparabilitat. La data d'obtenció del fitxer no identifica aquest període.

>>> Cinc dies ficticis tenen màximes 30, 32, 34, absent i 30 °C. La mitjana dels quatre dies coneguts és $126/4=31,5$ °C; la màxima observada és 34 °C. Si l'absent es tractés com zero, s'obtindrien 25,2 °C, un resultat incorrecte. Tampoc es pot garantir que 34 °C sigui la màxima de tot el període, perquè falta un dia.

L'exemple cartogràfic d'aquest capítol conserva un sol dia. Per estudiar un mes s'hauria de preparar un altre indicador, amb calendari i cobertura comparables. Barrejar el màxim històric de cada estació, produït en dies i anys diferents, no descriu un episodi meteorològic coherent.

::: table "Indicadors tèrmics que no s'han d'equiparar"
| Indicador | Pregunta que respon | Límit |
| --- | --- | --- |
| Mitjana de màximes d'un agost | Quin nivell diürn alt és habitual en aquell mes? | Pot suavitzar episodis excepcionals |
| Màxima absoluta del període | Quin valor extrem s'hi ha observat? | Sensible a longitud de sèrie, qualitat i dies absents |
| Percentil de màximes | Quin llindar supera una fracció dels dies? | Necessita una mostra temporal suficient i una convenció |
| Màxima d'un dia d'episodi | Com es distribueix l'extrem en una data comuna? | Descriu aquell episodi, no una climatologia general |
:::

Un ràster és una forma de representar l'estimació espacial d'aquesta variable. La paraula superfície descriu el suport de sortida; no canvia el fet que s'estiguin interpolant temperatures. La seva resolució ha de ser coherent amb el model i les observacions, no amb el detall màxim disponible del MDT.

## Estacions, relleu i domini d'estudi {#dades-climatiques}

La XEMA proporciona observacions i metadades d'estacions, accessibles a través dels serveis de Meteocat {% cite meteocatDadesObertes %}. La preparació necessita identificador, coordenades, altitud, variable, unitat, període, estat de validació i valors absents. La dada diària s'ha de construir o obtenir d'acord amb la definició del productor, inclòs el tractament de l'hora i el dia. Cal utilitzar una mateixa convenció per a totes les estacions.

Aquí s'utilitzen les estacions admeses del conjunt de Catalunya. La diversitat entre costa, depressions i muntanya ajuda a veure que un model basat només en distàncies pot deixar variació sense explicar. El límit administratiu serveix per presentar el mapa, però no és una frontera física de la temperatura: a les vores falta informació d'estacions externes. Per a un estudi local s'hauria de revisar expressament el domini i l'entorn d'observacions.

### Cobertura altitudinal i distribució espacial

Per estimar una relació amb l'altitud cal que les estacions en representin un rang suficient. Un conjunt concentrat en una plana pot no permetre identificar un pendent estable. La presència de poques estacions molt elevades tampoc no garanteix una relació transferible a tota l'àrea.

Cal comparar l'altitud publicada de l'estació amb la que s'extreu del MDT, revisant definició i exactitud. Una discrepància pot provenir de resolució, localització o referència vertical. La covariable utilitzada per ajustar i la utilitzada per predir han de ser compatibles. No convé barrejar altituds de fonts diferents sense aquesta comprovació.

Una graella molt fina del MDT no fa fina la informació climàtica. La resolució de sortida s'ha de justificar segons densitat d'estacions, variació representada i ús. El mapa pot tenir molts píxels, però el nombre d'observacions i la seva distribució continuen limitant-ne la interpretació.

## IDW de les temperatures amb QGIS {#procediment-clima}

A la Caixa d'eines es cerca **Interpolació IDW** (`qgis:idwinterpolation`). Es trien les estacions i l'atribut `tx_c`, i es prem **+** per incorporar la combinació a la taula d'entrada com a punts. El desplegable pot mostrar un altre camp després d'afegir-lo: el que entra al càlcul és la fila conservada a la taula.

L'exponent és 2. S'estableixen EPSG:25831 i l'extensió est 260.000–530.000 m, nord 4.486.000–4.752.000 m, amb píxel de 2.000 m. En aquesta eina no es restringeix el càlcul a un nombre fix de veïns: la ponderació utilitza els punts d'entrada i en redueix la contribució amb la distància. La resolució de 2 km representa una superfície regional, no diferències entre cobertes d'edificis.

![Diàleg IDW amb tx_c a la taula d'entrada, exponent 2 i píxel de 2000 m]({{ site.baseurl }}/assets/captures/idw-parametres.png "La fila tx_c de la taula identifica la variable interpolada. L'exponent controla la disminució del pes amb la distància; la mida de píxel defineix la graella de sortida."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

Després del càlcul es comproven el CRS, l'extensió i la mida de cel·la a la informació del ràster. El retall amb el límit de Catalunya facilita la presentació; no recalcula el model. Per comparar-lo amb kriging es conserva la mateixa graella i la mateixa escala de colors.

## Del parell d'estacions al semivariograma {#kriging-residus}

La geoestadística estudia com canvien les diferències entre observacions quan augmenta la separació. Matheron en va formalitzar fonaments i Cressie desenvolupa el tractament estadístic dels camps {% cite matheron1963principles cressie1993statistics %}. El **semivariograma experimental** resumeix la meitat de les diferències quadràtiques entre parells d'observacions d'una classe de distància:

$$
\widehat{\gamma}(h)=\frac{1}{2N_h}\sum_{(i,j)\in P_h}(T_i-T_j)^2.
\label{eq:semivariograma}
$$

Aquí $T_i$ és la temperatura a l'estació $i$, $P_h$ el conjunt de parells de la classe de separació $h$ i $N_h$ el nombre de parells. Un valor petit indica temperatures semblants a aquella separació; un valor gran, diferències més marcades. Com que s'eleven diferències al quadrat, la semivariància té unitats de °C². No és una temperatura estimada.

### Calcular un punt del semivariograma {#exemple-semivariograma}

La fórmula té tres passos: seleccionar parells amb separació semblant, elevar al quadrat les diferències i fer-ne la mitjana dividida per dos. En un exemple fictici, cinc estacions en línia ocupen les posicions 0, 1, 2, 3 i 4 km i mesuren 31, 30,5, 29,5, 29 i 30 °C.

Els quatre parells separats exactament 1 km tenen diferències 0,5, 1, 0,5 i −1 °C. Els quadrats sumen 2,5 °C². La semivariància és $2,5/(2\times4)=0,3125$ °C². Es pot repetir el procés per a cada separació disponible.

::: table "Semivariograma experimental de cinc temperatures fictícies alineades"
| Separació, km | Nombre de parells | Suma de diferències quadràtiques, °C² | Semivariància, °C² |
| --- | ---: | ---: | ---: |
| 1 | 4 | 2,50 | 0,3125 |
| 2 | 3 | 4,75 | 0,7917 |
| 3 | 2 | 4,25 | 1,0625 |
| 4 | 1 | 1,00 | 0,5000 |
:::

El darrer valor disminueix i només es basa en un parell. No s'ha de forçar una història territorial a partir d'aquest únic punt: les cinc estacions serveixen per entendre el càlcul, però són molt poques per ajustar amb confiança una estructura espacial. En un conjunt gran, les distàncies se solen agrupar en intervals i cal estudiar quants parells contribueixen a cada interval.

L'**efecte llavor** descriu una discontinuïtat a l'origen associable a microvariació i error; el **llindar** i l'**abast** resumeixen la variació i l'escala de dependència en models adequats. En models exponencials o gaussians, l'abast pràctic necessita una convenció perquè l'aproximació al llindar és asimptòtica. No s'ha de confondre l'abast del variograma amb una distància jurídica o una frontera física exacta.

![Model esfèric de semivariograma amb efecte llavor, llindar i abast identificats]({{ site.baseurl }}/assets/quarto/figures/semivariograma.qmd "Model teòric esfèric: efecte llavor de 0,2 °C², llindar total de 2 °C² i abast de 4 km. Els paràmetres són il·lustratius; la corba no és un ajust a les cinc estacions de la taula ni a dades meteorològiques reals."){: data-figure-width-web="33rem" data-figure-width-pdf="78%"}

La lectura de la corba comença a l'esquerra: parells molt pròxims tendeixen a diferir menys que parells separats, sota aquest model. La discontinuïtat entre zero i distàncies positives molt petites és la llavor. El llindar és el nivell que la corba assoleix; l'abast esfèric és la distància a partir de la qual es manté en aquell nivell. Un model teòric no ha de passar per cada punt experimental: sintetitza una estructura admissible que després s'ha de contrastar {% cite cressie1993statistics %}.

### Ajustar un model admissible

El model teòric ha de ser matemàticament admissible i tenir paràmetres interpretables. Per exemple, una llavor negativa no representa una variància vàlida. Un ajust visual atractiu tampoc basta si els paràmetres són inestables. Cal conservar el nombre de parells de cada classe; si s'estudien direccions diferents —**anisotropia**—, també s'ha de comprovar que disposin de parells i distàncies comparables.

### Semivariograma de les estacions XEMA a QGIS

El proveïdor [**Processing SAGA NextGen**](https://github.com/baswein/qgis-processing-saga-nextgen), versió 1.3.0, connecta QGIS amb SAGA 9.8.0 en aquest exemple. Necessita SAGA instal·lat i accessible, a més del complement. A la Caixa d'eines, **Variogram** (`sagang:variogram`) rep les estacions, `tx_c`, 12 classes inicials, distància màxima 150.000 m i salt 1, que conserva tots els punts.

![Diàleg SAGA Variogram amb dotze classes i distància màxima de 150 km]({{ site.baseurl }}/assets/captures/variograma-parametres.png "El semivariograma agrupa parells d'estacions. El nombre de classes i la distància màxima defineixen com es resumeixen les diferències; no són la resolució del ràster."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

La taula de sortida permet representar semivariància i distància i consultar quants parells entren en cada classe. El gràfic de les 182 estacions augmenta amb la separació i no mostra un replà clar fins als 150 km. Per això l'exemple utilitza un model **lineal amb llavor**, en lloc d'atribuir-li un abast que el gràfic no sosté. La forma també convida a investigar diferències regionals i relació amb el relleu.

## Kriging ordinari amb les mateixes observacions {#kriging-ordinari}

El **kriging** combina observacions amb pesos calculats a partir del model de dependència i del veïnatge de predicció. Pot generar pesos negatius sense que això sigui, per si sol, un error. La distribució dels punts, el model i els paràmetres determinen el resultat; afegir cel·les al mapa no afegeix observacions.

La diferència amb IDW és que el kriging considera també com es relacionen les observacions **entre elles**. Tres estacions molt juntes poden aportar informació redundant, mentre que una quarta situada en una altra direcció pot ampliar la cobertura. Els pesos s'obtenen resolent un sistema que utilitza el model espacial i les condicions d'estimació; no s'assignen només segons qui és el punt més pròxim.

En kriging ordinari, els pesos sumen 1 per conservar una mitjana constant desconeguda. En el cas particular de dues observacions equidistants d'un punt mitjà, amb el mateix model isòtrop, la simetria dona pesos 0,5 i 0,5. Amb temperatures 20 i 26 °C s'estimarien 23 °C. En una geometria més complexa, aquesta mitjana simple no es pot donar per vàlida.

La formulació exigeix hipòtesis sobre la mitjana i sobre com es comporten les diferències espacials dins del domini. Una tendència regional marcada pot qüestionar un model únic. Per això es comparen mapes i errors i es considera més endavant si una covariable, com l'altitud, ajuda a representar aquella tendència.

### Configuració i lectura del resultat

**Ordinary Kriging** (`sagang:ordinarykriging`) rep les mateixes estacions i `tx_c`. L'extensió i la mida de cel·la són les d'IDW, amb **Fit: cells**. Es mantenen 12 classes, màxim 150 km i salt 1. El camp **Model** conté `a + b*x/100000`: $x$ és distància en metres, i dividir per 100.000 facilita l'escala numèrica de l'ajust sense canviar que el model sigui lineal.

L'ajust d'aquest conjunt dona aproximadament $a=2,79123$ i $b=19,5643$. A distàncies positives, la corba és $2,79123+19,5643h/100000$, en °C², amb $h$ en metres. La llavor i el pendent són positius. Aquest model no té replà ni abast finit: el límit de 150 km correspon al resum experimental utilitzat per ajustar-lo.

![Diàleg de kriging ordinari SAGA amb graella i model lineal]({{ site.baseurl }}/assets/captures/kriging-parametres.png "Kriging ordinari amb cel·les de 2000 m, 12 classes de separació i model a + b*x/100000. La sortida Prediction estima temperatures; Prediction Error, amb Variance, expressa variància en °C²."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

Es tria cerca global amb tots els punts, sense transformació logarítmica ni kriging de blocs. La predicció i la variància es guarden en fitxers diferents. El càlcul dels mapes conserva totes les observacions; l'opció de validació interna està desactivada. Això produeix les superfícies, però encara no compara la capacitat predictiva fora de la mostra.

![Estacions XEMA, semivariograma i mapes IDW i kriging de les màximes del dia]({{ site.baseurl }}/assets/quarto/figures/temperatures-catalunya.qmd "Màximes del 15 d'agost de 2025, dia TU. A: 182 observacions. B: parells agrupats en 12 classes i model lineal de SAGA. C i D: IDW i kriging ordinari en la mateixa graella de 2 km i escala 15–45 °C. La suavitat dels mapes no és una mesura de precisió."){: data-figure-width-web="48rem" data-figure-width-pdf="100%" data-caption-source="Observacions i metadades: Servei Meteorològic de Catalunya. Límit: ICGC. Càlcul QGIS/SAGA; elaboració pròpia."}

IDW conserva canvis locals més marcats al voltant d'algunes estacions; el kriging representa una transició més contínua sota el model ajustat. Cap dels dos incorpora l'altitud com a predictor en aquests mapes. Per decidir quin és més útil cal retirar observacions, predir-les i comparar errors, no escollir la superfície més agradable visualment.

## Ampliació amb altitud i residus {#regressio-altitud}

L'altitud és una **covariable**: informació auxiliar disponible als punts observats i sobre tot el domini mitjançant un MDT. Una regressió empírica pot representar part de la variació tèrmica:

$$
\widehat{m}(s)=a+bz(s).
\label{eq:tendencia-altitud}
$$

Aquí $z(s)$ és altitud en metres i $b$ el pendent, en °C per metre. Els coeficients s'estimen amb les observacions. No es fixen automàticament a partir del gradient adiabàtic, que descriu una massa d'aire desplaçada verticalment, no la relació entre màximes de superfície d'estacions diferents. Costa, inversions, circulació i urbanització poden introduir altres diferències.

El **residu** $e(s_i)=T(s_i)-\widehat m(s_i)$ és allò que queda després de restar la tendència. A la [taula de regressió dels fonaments]({{ site.baseurl }}/ca/chapters/fonaments-geodisseny/#exemple-regressio), una observació de 29 °C i una tendència de 28,5 °C deixen +0,5 °C. Si estacions properes conserven residus semblants, es pot investigar si aquesta estructura aporta informació per predir.

### Reconstruir temperatura amb regressió-kriging {#regressio-kriging}

Es calcula ara el semivariograma dels **residus**, substituint $T_i$ per $e_i$ a la fórmula. No s'ha de reutilitzar sense justificació el semivariograma de les temperatures originals. Després del kriging residual, la predicció final combina tendència i residu estimat:

$$
\widehat{T}(s)=\widehat{m}(s)+\widehat{e}(s).
\label{eq:regressio-kriging}
$$

>>> Si la regressió prediu 30 °C en un lloc i el kriging hi estima un residu de +0,5 °C, la reconstrucció és 30,5 °C. Si el residu fos −0,5 °C, seria 29,5 °C. Les dues parts estan en °C i es poden sumar. La variància de kriging, expressada en °C², és una sortida distinta i no s'afegeix a la temperatura.

Hengl, Heuvelink i Rossiter presenten aquesta relació i la discuteixen en casos de predicció espacial {% cite hengl2007regression %}. La idea es transfereix a variables de sòl o ambientals quan hi ha covariables exhaustives i observacions adequades. La utilitat de la covariable depèn de la relació i de la validació, no del simple fet que existeixi un mapa auxiliar.

![Separació de tendència i residus i reconstrucció de la temperatura]({{ site.baseurl }}/assets/diagrams/regressio-kriging.mmd "La regressió aporta una tendència sobre el MDT; el kriging estima l'estructura residual. La validació ha de reajustar tota la cadena dins de cada partició per evitar que les observacions de contrast influeixin en el model."){: data-figure-width-web="39.5rem" data-figure-width-pdf="85%"}

Si els residus no mostren estructura aprofitable, afegir kriging pot no millorar la regressió. Si l'altitud aporta poc, un altre model simple pot ser suficient. La comparació docent inclou com a mínim una referència senzilla, una regressió i la combinació; IDW pot servir de contrast determinista, amb potència i veïnatge declarats.

### Comparar models sobre un camp que es coneix {#interpolacio-sintetica}

Per observar què aporta cada pas, la figura parteix d'un camp tèrmic creat matemàticament. La temperatura combina una disminució amb altitud i una variació espacial suau addicional. Només nou posicions es fan servir com a observacions. La superfície completa es conserva com a referència de l'experiment; no és una capa de temperatura observada del territori.

![Camp sintètic conegut i tres estimacions amb les mateixes nou observacions: regressió amb altitud, IDW i regressió-kriging]({{ site.baseurl }}/assets/quarto/figures/interpolacio-comparada.qmd "Comparació controlada amb nou observacions fictícies, la mateixa extensió i una escala de temperatura comuna. La regressió usa altitud; IDW usa distàncies amb p = 2; regressió-kriging hi afegeix residus amb un model esfèric prescrit per a l'exemple. No són resultats de validació sobre estacions reals."){: data-figure-width-web="35.5rem" data-figure-width-pdf="85%"}

La regressió recupera una tendència ampla perquè disposa d'altitud a tot el domini, però no representa tota la variació que s'ha introduït en el camp. IDW respon a les observacions properes sense conèixer l'altitud com a variable. La combinació parteix de la tendència i estima una correcció espacial. Comparar els panells amb la mateixa llegenda evita confondre canvis d'escala de color amb diferències del model.

L'experiment fixa expressament el semivariograma residual per poder reproduir el càlcul: no pretén demostrar que nou punts bastin per estimar-ne amb precisió els paràmetres. En una aplicació, el model de dependència s'hauria d'ajustar o justificar i contrastar amb dades no utilitzades. Conèixer aquí la superfície generadora permet preguntar on falla cada aproximació; al territori real no es disposa d'aquesta resposta completa.

Per portar aquesta ampliació a QGIS, es mostreja el MDT als punts, s'ajusta la regressió i es conserven els residus vinculats pel codi d'estació. El camp residual passa a ser l'atribut del variograma i del kriging. La Calculadora ràster aplica $a+bz$ al MDT i hi suma la predicció residual sobre una graella alineada. Les dues parts estan en °C; la variància en °C² es conserva separada.

## Validar amb observacions retirades {#validacio-clima}

Validar vol dir comprovar prediccions en observacions que no han participat en el seu ajust. Per comparar IDW i kriging, es reserva el mateix conjunt d'estacions i s'utilitzen només les altres per construir cada model. El variograma també s'ha d'ajustar sense les estacions reservades. Després es mostregen les prediccions a les posicions retirades i es calculen diferències respecte dels valors observats.

En cada partició es retiren les observacions de contrast i es tornen a ajustar regressió, residus i variograma només amb les d'entrenament. Reutilitzar els residus o el variograma calculats amb totes les estacions faria participar les observacions retirades en la seva pròpia predicció.

La separació espacial s'ha d'adaptar a l'ús. Deixar una estació fora pot ser útil per estudiar predicció dins d'una xarxa densa; blocs o separacions més grans posen a prova transferència a espais menys observats. Cal mantenir les mateixes particions per comparar models i informar d'errors per entorns i altituds, a més dels resums globals {% cite roberts2017validation %}.

### Llegir una comparació de prediccions

Una taula de validació conserva, per a cada observació retirada, el valor observat i el predit per cadascun dels models. No cal interpretar primer un índex global: es poden calcular i mapar les discrepàncies abans de resumir-les.

::: table "Exemple fictici de quatre prediccions independents de l'ajust"
| Cas | Observació, °C | Model A, °C | Error A | Model B, °C | Error B |
| --- | ---: | ---: | ---: | ---: | ---: |
| V1 | 30 | 32 | −2 | 31 | −1 |
| V2 | 31 | 32 | −1 | 31,5 | −0,5 |
| V3 | 28 | 27 | +1 | 27,5 | +0,5 |
| V4 | 29 | 27 | +2 | 28 | +1 |
:::

Els dos models tenen biaix zero. A té MAE d'1,5 °C i RMSE d'1,58 °C; B, MAE de 0,75 °C i RMSE de 0,79 °C. B és millor en aquestes quatre prediccions segons totes dues mesures, però la taula no demostra que el seu comportament sigui igual en una altitud o regió no representada. Són prediccions construïdes per explicar les mètriques, no una comparació executada de Meteocat.

>> Una partició de validació és una pregunta sobre transferència. Separar una estació d'un grup dens pregunta una cosa diferent de retirar totes les estacions d'una vall. La partició ha d'assemblar-se a la situació on es voldrà utilitzar el mapa.

## Incertesa i ús territorial {#incertesa-termica}

La variància de kriging és una mesura condicionada al model, als paràmetres i a les localitzacions observades. No és l'error que s'ha mesurat comparant predicció i observació. En regressió-kriging, la variància residual tampoc no inclou automàticament tota la incertesa de la regressió ni possibles covariàncies; cal anomenar-la **variància condicional del kriging residual**, no error total de temperatura.

La desviació estàndard és l'arrel de la variància i recupera graus Celsius. L'error real només es pot calcular on hi ha observacions independents de contrast. Cal mostrar tant la predicció com els diagnòstics de validació i les zones de suport feble. Retallar al Tarragonès no elimina extrapolacions ni mancances del domini d'ajust.

Per incorporar temperatura a una avaluació multicriteri es pot definir una funció de preferència tèrmica acotada, però s'ha d'explicar què representa. Una penalització basada en màximes d'aire és un indicador d'exposició, no una simulació completa de rendiment. Cal evitar que petites diferències inferiors a la incertesa produeixin categories territorials aparentment precises.

La comparació entre un agost mitjà i un episodi extrem pot donar ordres diferents de candidates. Aquesta diferència és informativa: permet distingir una condició habitual d'una prova d'estrès. La decisió final ha de conservar escenari, covariables i incertesa, en lloc d'escollir el mapa que afavoreixi una alternativa predeterminada.

## Calor i resposta fotovoltaica {#temperatura-modul}

Un mapa de màximes de l'aire pot ajudar a discutir exposició tèrmica, però no calcula directament producció fotovoltaica. La potència del mòdul depèn, entre altres factors, de la irradiància i de la temperatura de les cèl·lules. En tecnologies habituals de silici, més temperatura pot reduir la potència a igual irradiància {% cite skoplaki2009temperature %}.

Una aproximació local compara potència a igual irradiància amb un coeficient tèrmic $\gamma_P$:

$$
\frac{P(T_c)}{P(T_{\mathrm{ref}})}\simeq1+\gamma_P(T_c-T_{\mathrm{ref}}).
\label{eq:potencia-temperatura}
$$

$T_c$ és temperatura de cèl·lula, i $T_{\mathrm{ref}}$ la de referència. Amb un coeficient fictici de −0,004 K⁻¹, passar de 25 a 55 °C de cèl·lula implica una reducció relativa aproximada del 12% a la mateixa irradiància. No és una pèrdua anual de kWh ni un percentatge universal.

### Aire, mòdul i cèl·lula

La XEMA mesura temperatura de l'aire. El mòdul rep radiació i intercanvia calor amb el seu entorn; el vent i el muntatge en condicionen la temperatura. El model de Faiman representa aquesta relació amb temperatura ambient, irradiància al pla i coeficients de pèrdues tèrmiques {% cite faiman2008temperature %}:

$$
T_m=T_a+\frac{G}{U_0+U_1v}.
\label{eq:faiman}
$$

$T_m$ és temperatura del mòdul i $T_a$, de l'aire; $G$ és irradiància al pla en W/m² i $v$, velocitat del vent en m/s segons la definició del model. $U_0$ té unitats W/(m²·K) i $U_1$ unitats W·s/(m³·K). Els coeficients depenen de calibració i muntatge. La documentació de [pvlib](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.temperature.faiman.html) explica l'origen dels valors per defecte.

![Resposta tèrmica sintètica amb irradiància i vent fixats i canvi relatiu de potència]({{ site.baseurl }}/assets/quarto/figures/temperatura-rendiment.qmd "La temperatura del mòdul pot superar la de l'aire i varia amb la ventilació. Simulació amb G = 800 W/m², U0 = 25, U1 = 6,84 i coeficient de potència −0,004 K⁻¹. No estima producció anual ni condicions mesurades d'una instal·lació."){: data-figure-width-web="42rem" data-figure-width-pdf="95%"}

>>>> Les màximes diàries d'aire, irradiància i vent no tenen per què coincidir en el temps. Combinar-ne extrems independents crea un escenari, no una observació simultània. Igualment, temperatura de mòdul i de cèl·lula necessiten la correspondència del model utilitzat abans d'aplicar un coeficient de potència.

## Activitats

### Del pes a l'estimació

Cal reconstruir les prediccions IDW de 21,2 °C i 22 °C del primer exemple i repetir el càlcul quan totes dues distàncies són 1 km. La comprovació és obtenir llavors 23 °C amb tots dos exponents. S'ha d'explicar quina informació fa servir IDW i quina dada addicional incorporaria una regressió amb altitud.

### Reconstruir el semivariograma petit

Amb les cinc temperatures de l'[exemple](#exemple-semivariograma), cal enumerar parells, distàncies i diferències quadràtiques. La taula final ha de reproduir les quatre semivariàncies. Després es resten 30 °C a totes les temperatures i es comprova que les diferències i el semivariograma es mantenen. Aquesta operació resta una constant, no una tendència que variï amb el lloc.

### Definir i auditar l'indicador

Cal reproduir la selecció de 182 estacions i les màximes del dia indicat, conservant estats de qualitat i els 48 intervals. Després es proposa una regla per ampliar l'indicador a una mitjana mensual, amb dies vàlids i tractament de mancances. La interpretació explicarà per què els dos indicadors no responen la mateixa pregunta.

### Comparar IDW i kriging

Cal conservar les dues prediccions en una graella comuna i reservar el mateix conjunt d'estacions per al contrast. La taula de validació inclourà codi, observació, prediccions i errors. El resultat compararà MAE i RMSE i descriurà la distribució espacial dels casos retirats, sense deduir precisió del nombre de píxels ni de la suavitat del mapa.

### Altitud com a covariable

Cal comparar una referència simple, regressió i regressió-kriging amb les mateixes particions de validació. El resultat ha d'indicar rang altitudinal, coeficients, errors i casos d'extrapolació. La conclusió justificarà si el MDT aporta una millora, sense imposar un gradient adiabàtic.

### Predicció i incertesa

Cal conservar ràsters de tendència, residu, temperatura reconstruïda i variància condicional disponible. El mapa d'incertesa ha d'identificar unitats i components no representats. S'ha de comparar una zona ben mostrejada amb una de suport feble.

### Interpretar una pèrdua tèrmica

Amb condicions docents d'irradiància, vent i coeficient tèrmic, cal calcular una diferència de potència a igual irradiància. El resultat ha de distingir aire, mòdul i cèl·lula, i explicar per què no es pot convertir directament en pèrdua anual de kWh. La discussió final relacionarà aquesta limitació amb la penalització tèrmica de l'EMC.
