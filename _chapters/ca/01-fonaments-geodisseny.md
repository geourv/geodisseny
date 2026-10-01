---
layout: manual-chapter
title: Fonaments d'anàlisi espacial i geodisseny
description: Models geogràfics, estadística, escala i incertesa per interpretar patrons i argumentar decisions territorials.
lang: ca
ref: fonaments-analisi-espacial-geodisseny
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/fonaments-geodisseny/
weight: 10
part: Continguts
manual_references: true
---

Un centre de salut pot ser a prop d'un barri i, tot i així, tenir un accés difícil. La ruta depèn dels carrers i dels passos disponibles, a més de la distància. L'anàlisi espacial estudia aquestes relacions entre localització, connexions i característiques del territori.

El treball amb dades i eines SIG de [TIG](https://geourv.github.io/tig/ca/) és el punt de partida. L'estadística ajuda a resumir les dades i a comparar llocs. Els models són representacions simplificades que permeten respondre preguntes, com estimar el temps d'un trajecte o la temperatura en un lloc sense termòmetre. El geodisseny utilitza aquest coneixement per formular propostes i estudiar-ne les conseqüències.

>>>>> Comprendre què representa una anàlisi espacial i com interpretar-ne els resultats.
>>>>>
>>>>> - Explicar què representa cada fila i cada columna d'una taula geogràfica.
>>>>> - Calcular una mitjana i descriure si els valors són semblants o molt diferents.
>>>>> - Llegir la relació entre dues variables i entendre què canvia en agrupar les dades.
>>>>> - Interpretar un marge d'estimació i una prova estadística a partir d'un exemple de camp.
>>>>> - Seguir les sis preguntes de Steinitz per comparar propostes territorials.

## Què és l'anàlisi espacial {#analisi-espacial}

Un ajuntament que vol millorar l'accés a un centre de salut pot disposar d'un mapa de barris, del nombre d'habitants i de les distàncies al centre. Amb aquestes dades es poden fer preguntes diferents: quina és la distància mitjana dels barris?, quina correspon als habitants?, quin recorregut haurien de fer a peu? Cada pregunta dona un paper diferent a la població, les distàncies i les connexions.

L'**anàlisi espacial** estudia on es localitzen els fenòmens geogràfics, com es distribueixen i com es relacionen. La posició i les relacions espacials intervenen en el càlcul. La mitjana d'una variable municipal es pot obtenir sense consultar el mapa; comprovar si els valors elevats són veïns, en canvi, exigeix definir una relació de distància, contacte o connexió {% cite longley2015gis burrough1998principles %}.

Una manera de reconèixer el paper de l'espai és repartir els mateixos valors entre localitzacions diferents. Aquesta reorganització s'anomena **permutació**. La mitjana de la taula no canviaria, però sí que podrien canviar les zones on s'ajunten els valors alts. Comparar aquestes disposicions permet veure què depèn de la localització.

>>> Quatre àrees fictícies contenen 10, 10, 30 i 30 comerços. Hi ha 80 comerços en total: la mitjana és $80/4=20$ comerços per àrea. Aquest nombre és el mateix tant si les dues àrees amb 30 comerços estan juntes com si estan separades. El mapa, en canvi, permet veure la diferència.

![Recompte de comerços en quatre àrees fictícies, amb els valors alts junts o separats]({{ site.baseurl }}/assets/quarto/figures/patrons-espacials.qmd "Els nombres indiquen comerços per àrea. Els dos mapes tenen 80 comerços i una mitjana de 20 per àrea. A l'esquerra, les àrees amb 30 comerços són veïnes; a la dreta, estan separades. La mitjana no mostra aquesta diferència espacial. Exemple fictici."){: data-figure-width-web="33rem" data-figure-width-pdf="78%"}

En la figura només s'ha canviat l'assignació dels valors a les quatre àrees. Es mantenen la forma, el recompte i els nombres utilitzats. La diferència entre els mapes prové, doncs, de la disposició espacial dels valors.

La cartografia fa visibles observacions i resultats. Un mapa pot suggerir una concentració, però per interpretar-la cal saber què s'ha inventariat, sobre quin domini i amb quina cobertura. Una superfície acolorida contínua pot ser una estimació o una simple suavització gràfica. La seva aparença no acredita que s'hagi mesurat el fenomen a cada cel·la ni que el model s'hagi validat.

El geoprocessament proporciona operacions com retallar, intersectar, transformar o calcular distàncies. Escollir-les depèn del problema. Un retall municipal pot servir per resumir la població del municipi, però deixar fora serveis i vies necessaris per estudiar-ne l'accessibilitat. La mateixa operació pot ser adequada per a una pregunta i fer perdre informació important per a una altra.

### Descripció, explicació, predicció i proposta

La **descripció** estableix què s'observa: on hi ha elements, com es distribueixen o quin valor adopten. L'**explicació** investiga els mecanismes que poden generar el patró. La **predicció** estima valors no observats, dins d'un domini o un horitzó especificats. La **proposta** introdueix canvis desitjats i necessita criteris per valorar-los. Les quatre funcions es poden relacionar, però no són intercanviables.

Una concentració de comerços al voltant d'una estació descriu un patró. Afirmar que l'estació l'ha causat requereix estudiar alternatives explicatives, dates i processos. Estimar activitat en una futura estació introdueix condicions de transferència. Decidir on s'ha de construir una nova estació afegeix objectius i preferències que les observacions no determinen per si soles.

::: table "Una mateixa qüestió territorial pot generar preguntes analítiques diferents"
| Funció | Exemple | Evidència necessària |
| --- | --- | --- |
| Descriure | On es concentra la capacitat d'autoconsum registrada? | Inventari delimitat, potències comparables i localitzacions interpretades |
| Explicar | Quins processos contribueixen al patró? | Hipòtesis, variables i disseny que permetin contrastar explicacions |
| Predir | Quines màximes tèrmiques s'esperen entre estacions? | Observacions comparables, model i validació |
| Proposar | Quines alternatives territorials convé estudiar? | Objectius, restriccions, conseqüències i preferències explícites |
:::

Descriure una concentració de punts en un eix no basta per recomanar-hi noves instal·lacions. Per estudiar una ubicació també cal conèixer les alternatives, les condicions del lloc i els efectes de la proposta.

## Observacions, variables i suport {#observacions-suport}

Abans de calcular res, convé llegir la taula com una descripció del món. Si cada fila correspon a una estació meteorològica, l'estació és la **unitat d'observació**. Les columnes poden contenir-ne l'altitud, la temperatura o el tipus d'entorn: són les **variables**. Cada cel·la conté un valor d'una d'aquestes variables.

Observació
: Un cas del qual es recull informació. En una taula d'estacions meteorològiques, una fila pot correspondre a una estació en un dia determinat.

Variable
: La característica que es mesura o classifica en cada observació: temperatura màxima, altitud o tipus d'entorn.

Valor
: El resultat concret d'aquella mesura o classificació, com 31,2 °C, 120 m o entorn urbà.

Suport
: L'espai i el temps als quals es refereix el valor. «31,2 °C en aquesta estació durant aquest dia» és més precís que «31,2 °C en aquest municipi».

Llegir una taula comença, doncs, per poder completar la frase «cada fila representa...». Si una estació apareix durant trenta dies, hi ha trenta registres però només un emplaçament. Si una taula resumeix trenta estacions en un mateix dia, hi ha trenta emplaçaments i un únic període. El recompte de files coincideix, però la informació espacial i temporal és diferent. Aquesta lectura de casos i variables és també el punt de partida de l'estadística introductòria {% cite diez2019openintro %}.

El **suport** precisa a quin espai i a quin període correspon la dada. Una temperatura mesurada en una estació durant un dia no és la temperatura de tot el municipi durant tot l'any. De la mateixa manera, dibuixar l'àrea d'una parcel·la al seu punt central no fa que aquell valor descrigui cada punt del terreny. En un cas es mesura una temperatura en un lloc; en l'altre, la superfície d'una peça de sòl completa.

>> Per llegir una dada, completa tres frases: «cada fila representa...», «aquesta columna mesura...» i «el valor es refereix a aquest lloc i període...». Això evita començar un càlcul amb unitats que no són comparables.

### Escales de mesura i operacions admissibles

Una variable **nominal** distingeix categories sense ordre, com bosc, conreu i sòl urbà. Una variable **ordinal** permet ordenar categories, com prioritat baixa, mitjana i alta, però no afirma que cada salt sigui igual. Una escala **d'interval** permet comparar diferències: passar de 10 a 15 °C i de 20 a 25 °C són augments de cinc graus. En una escala **de raó**, el zero indica absència de la magnitud: 0 m és cap longitud i 200 m són el doble de 100 m. El nom de l'escala resumeix, doncs, quines comparacions tenen sentit.

Una temperatura de 40 °C no és «el doble de temperatura» que 20 °C en el mateix sentit que 40 kW és el doble de potència que 20 kW. Fer la mitjana dels codis d'una coberta tampoc no crea una categoria intermèdia vàlida. Els nombres emmagatzemats no garanteixen una magnitud quantitativa: un codi municipal pot ser una etiqueta, encara que només contingui dígits.

::: table "Escales de mesura: què es pot interpretar a partir del valor"
| Variable d'exemple | Escala | Operació amb sentit | Interpretació que no se'n deriva |
| --- | --- | --- | --- |
| Coberta: bosc, conreu, urbà | Nominal | Comptar àrees de cada categoria | Fer la mitjana dels codis de les categories |
| Prioritat: baixa, mitjana, alta | Ordinal | Ordenar casos | Suposar que dos salts tenen la mateixa magnitud |
| Temperatura en °C | Interval | Calcular una diferència de 5 °C | Dir que 30 °C és el doble de 15 °C |
| Distància en metres | Raó | Comparar 200 m amb 100 m | Confondre distància recta i recorregut possible |
:::

>> Un codi numèric pot continuar sent una etiqueta. Els codis 1 = bosc i 2 = conreu permeten seleccionar registres, però el valor mitjà 1,5 no defineix una coberta. Abans d'aplicar una funció estadística a un camp, cal interpretar-lo, no només comprovar que el programa el classifica com a numèric.

Un recompte és **discret**: hi pot haver dues o tres instal·lacions, però no dues i mitja. Una longitud o una temperatura són magnituds **contínues**: entre 20 i 21 °C hi ha valors intermedis, encara que el termòmetre només en mostri alguns decimals. Aquesta distinció ajuda a triar el resum i el gràfic adequats; no diu, tota sola, quin model geogràfic s'ha d'aplicar.

### Població, mostra i registre

Si es vol conèixer el temps que triguen tots els estudiants a arribar al campus, el conjunt d'estudiants és la **població**. Si només es pregunta a cinquanta, aquestes cinquanta persones formen una **mostra**. Les seves respostes es poden descriure directament; per estendre la conclusió a tot el campus importa com s'han escollit. Preguntar només a qui arriba en bicicleta deixaria fora altres experiències.

En estadística, «població» també pot referir-se a parcel·les, instal·lacions o mesures possibles, no només a persones. Un registre administratiu pot cobrir només una part del fenomen: per exemple, les instal·lacions inscrites i amb coordenades conegudes. «Tots els registres descarregats» no significa necessàriament «tots els elements existents».

El mostreig també pot ser desigual en l'espai. Una xarxa d'estacions meteorològiques respon a criteris d'emplaçament i manteniment; els seus punts no són una mostra aleatòria uniforme. La concentració d'estacions en determinades altituds o entorns condiciona la capacitat de predir en els altres. Afegir més punts molt pròxims entre si no sempre aporta tanta informació com observar un entorn poc representat.

Els valors absents s'han de distingir dels zeros. Una potència desconeguda no és una instal·lació de 0 kW; una cel·la no coberta per una cartografia no és una zona lliure de restriccions. El recompte de valors coneguts permet saber quants registres han entrat en una operació. En una mitjana, per exemple, aquesta selecció determina per quin nombre es divideix la suma.

>>> Tres registres tenen potències 10 kW, 20 kW i una potència desconeguda. La mitjana dels **dos valors coneguts** és 15 kW. Substituir el desconegut per zero donaria 10 kW, però afegiria una observació que no existeix. Tampoc es poden atribuir 15 kW al tercer registre sense un model d'imputació. La conclusió correcta conserva «2 de 3 registres amb potència coneguda».

## Centre, distribució i dispersió {#estadistica-descriptiva}

Quan es disposa de moltes dades, una taula completa pot ser difícil de llegir. L'**estadística descriptiva** (*descriptive statistics*) en facilita el resum. Es poden fer tres preguntes: quin valor representa el centre del conjunt?, quant s'allunyen els valors d'aquest centre?, hi ha valors molt més grans o petits que la resta? La manera com es reparteixen els valors és la seva **distribució**.

Els càlculs següents utilitzen **cinc instal·lacions fictícies**, amb potències de 5, 5, 10, 20 i 60 kW, per poder seguir les operacions a mà. La potència expressa capacitat de generació instantània, mentre que l'energia acumulada durant un període s'expressaria, per exemple, en kWh. Les mateixes operacions servirien per a superfícies o distàncies, amb les unitats corresponents.

### Mitjana, mediana i quantils

Per calcular la **mitjana aritmètica** (*arithmetic mean*), se sumen les cinc potències i es divideix per cinc: $(5+5+10+20+60)/5=20$ kW. Si es repartissin els 100 kW totals a parts iguals, correspondrien 20 kW a cada instal·lació. La fórmula escriu aquesta mateixa operació de manera abreujada:

$$
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i.
\label{eq:mitjana}
$$

>> **Com es llegeix la fórmula?** $n$ és el nombre de dades: aquí, cinc. $x_i$ és cadascuna de les potències. El signe $\sum$ vol dir «suma-les totes» i la barra de $\bar{x}$ identifica la mitjana. La fórmula no afegeix cap operació al càlcul que s'acaba de fer.

Una altra manera de trobar el centre és ordenar els nombres i escollir el del mig. És la **mediana** (*median*). En la sèrie 5, 5, 10, 20 i 60, el valor central és 10 kW: hi ha dos nombres a cada costat. Si el nombre de dades fos parell, es faria habitualment la mitjana dels dos centrals.

La mitjana de 20 kW i la mediana de 10 kW responen, doncs, preguntes diferents. La primera relaciona el total amb el nombre d'instal·lacions. La segona identifica una posició central sense que el valor de 60 kW l'arrossegui cap amunt {% cite diez2019openintro %}. Els **quantils** (*quantiles*) amplien aquesta idea de posició: separen altres proporcions de les dades ordenades, com un quart o tres quarts.

El **diagrama de caixa**, o *boxplot*, permet comparar aquestes posicions. La caixa va del primer quartil, $Q_1$, al tercer, $Q_3$; una ratlla interior marca la mediana. El primer quartil deixa aproximadament un 25% dels valors per sota; el tercer, un 75%. La caixa resumeix així la part central de la distribució.

En A, amb la convenció de quantils emprada aquí, $Q_1$, mediana i $Q_3$ són 5, 10 i 20 kW. L'amplada de la caixa és el **rang interquartílic**, $Q_3-Q_1=15$ kW, sovint abreujat **IQR** per *interquartile range*. Resumeix la separació entre els quartils, mentre que el rang total, $60-5=55$ kW, depèn dels dos extrems.

>> Aquí els quantils es calculen per interpolació lineal entre els valors ordenats. La posició corresponent a una proporció $p$ és $1+(n-1)p$. Amb cinc valors, el primer quartil ocupa la posició $1+4\times0,25=2$ i el tercer, $1+4\times0,75=4$: corresponen als valors 5 i 20 kW. Si la posició no fos entera, s'interpolaria entre els dos valors adjacents.

Els segments anomenats **bigotis** arriben fins als valors observats més extrems que resten dins d'unes tanques convencionals. La regla habitual situa les tanques a $Q_1-1,5\,\mathrm{IQR}$ i $Q_3+1,5\,\mathrm{IQR}$. En A són −17,5 i 42,5 kW: els bigotis arriben a 5 i 20, i el valor 60 apareix separat. La tanca és una regla gràfica per destacar observacions, no un límit físic ni un contrast estadístic.

![Punts i caixes de dues sèries de cinc potències, amb els valors centrals i la mitjana assenyalats]({{ site.baseurl }}/assets/quarto/figures/distribucions.qmd "Cinc instal·lacions poden tenir una mitjana de 20 kW i ser molt diferents entre si, com a dalt, o tenir totes 20 kW, com a baix. Els punts són les potències; la caixa en resumeix la part central. La ratlla verda assenyala la mediana. Dades fictícies."){: data-figure-width-web="42rem" data-figure-width-pdf="95%"}

La figura permet fer una comprovació visual abans de calcular la dispersió: A ocupa diverses posicions de l'eix horitzontal i B es concentra en una sola. Els punts que tenen la mateixa potència s'apilen per poder comptar-los; la seva altura gràfica no representa cap segona variable. En B, quartils i mediana coincideixen a 20 kW i la caixa es redueix a una ratlla. En una mostra tan petita convé conservar els punts originals al costat del resum.

>>> Si els 60 kW del conjunt A es canvien per 160 kW, la suma passa a 200 kW i la mitjana a 40 kW. La mediana continua sent 10 kW perquè el tercer valor ordenat no ha canviat. Això explica què significa que la mitjana sigui sensible als extrems: una sola observació pot moure el resum de tot el conjunt.

Amb moltes observacions, es pot utilitzar un **histograma**: per exemple, comptar quantes instal·lacions tenen entre 0 i 10 kW, entre 10 i 20 kW, i així successivament. Les barres mostren aquests recomptes. Canviar l'amplada dels intervals modifica l'aspecte del gràfic, encara que les dades continuïn sent les mateixes.

### Variància, desviació estàndard i rang interquartílic

Per entendre la dispersió es calcula primer quant se separa cada valor de la mitjana. En A, les diferències respecte dels 20 kW són −15, −15, −10, 0 i 40 kW. Sumar-les no serveix per mesurar dispersió: els signes es compensen i la suma és zero. Elevar-les al quadrat evita aquesta compensació i dona més influència a les separacions grans.

::: table "Càlcul de la dispersió de les cinc potències fictícies"
| Registre | Potència, kW | Diferència respecte de 20 kW | Diferència al quadrat, kW² |
| --- | ---: | ---: | ---: |
| A1 | 5 | −15 | 225 |
| A2 | 5 | −15 | 225 |
| A3 | 10 | −10 | 100 |
| A4 | 20 | 0 | 0 |
| A5 | 60 | 40 | 1.600 |
| Suma | 100 | 0 | 2.150 |
:::

La **variància descriptiva** (*variance*) és la mitjana d'aquests quadrats: $2150/5=430$ kW². La **desviació estàndard** (*standard deviation*) n'és l'arrel quadrada, aproximadament 20,74 kW. La variància conserva la unitat elevada al quadrat; extreure'n l'arrel permet tornar a comparar la dispersió amb les potències originals. En B totes les diferències són zero i, per tant, també ho són variància i desviació.

![Tres passos per mesurar quant se separen cinc potències de la seva mitjana]({{ site.baseurl }}/assets/quarto/figures/variancia-desviacio.qmd "Quant s'allunyen les cinc potències de la mitjana de 20 kW? A mostra les diferències; B les eleva al quadrat perquè els signes no es compensin; C torna als kW mitjançant l'arrel quadrada. La dispersió resumida així és de 20,74 kW. Dades fictícies."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

>> **Segueix una sola instal·lació.** A5 té 60 kW, és a dir, 40 kW més que la mitjana. Al panell següent aporta $40\times40=1600$ kW². Aquesta barra gran explica per què un sol valor molt allunyat pot fer créixer tant la variància.

Si aquests cinc casos fossin només una mostra amb què es vol estimar la dispersió d'un conjunt més gran, el càlcul habitual dividiria per $n-1$, aquí quatre. Aquesta correcció té en compte que la mitjana també s'ha estimat amb la mostra. S'utilitza amb condicions com el mostreig aleatori i la independència de les observacions {% cite diez2019openintro %}:

$$
s^2=\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2.
\label{eq:variancia}
$$

Amb aquest divisor, l'exemple dona $2150/4=537,5$ kW². Per descriure els cinc nombres com a conjunt complet s'ha utilitzat el divisor $n$. L'estimació mostral amb $n-1$ té una altra finalitat i depèn dels supòsits sobre la mostra. Si les observacions estan relacionades espacialment, el supòsit d'independència pot no ser adequat.

El rang interquartílic del boxplot és menys sensible a un valor molt extrem que la desviació estàndard. Si es canvien els 60 kW per 160 kW, $Q_1$, la mediana i $Q_3$ es mantenen, però la variància augmenta. Per això comparar caixa, punts i desviació ajuda a distingir la dispersió de la part central i la influència de les cues de la distribució.

>> La mitjana respon «al voltant de quin valor se situa el conjunt?». La dispersió respon «quant se separen els valors entre si?». Convé formular totes dues preguntes abans de comparar dos municipis o dos inventaris.

Un valor atípic pot ser una observació vàlida molt influent, un error d'unitats o un registre duplicat. Cal investigar-lo abans d'eliminar-lo. Comparar els resums amb i sense aquell registre és una anàlisi de sensibilitat, no una justificació automàtica per descartar-lo. En potències, la conversió incorrecta entre MW i kW pot alterar tota la distribució.

### Ponderar és canviar la pregunta

Hi ha situacions en què cada fila no hauria de comptar igual. Un barri de 1.000 habitants representa més persones que un de 200. Una **mitjana ponderada** (*weighted mean*) permet donar a cada barri un pes proporcional a la seva població:

$$
\bar{x}_p=\frac{\sum_i p_i x_i}{\sum_i p_i}.
\label{eq:mitjana-ponderada}
$$

Aquí $x_i$ és la distància i $p_i$ és el pes, en aquest cas el nombre d'habitants. Primer es multiplica cada distància pels habitants del barri; després se sumen els productes i es divideix per la població total. Els pesos han de ser no negatius i sumar més de zero.

>>> Dos barris ficticis són a 2 km i a 8 km del centre de salut. Si cada barri compta igual, la distància mitjana és $(2+8)/2=5$ km. Però el primer té 1.000 habitants i el segon 200. La mitjana ponderada és $(1000\times2+200\times8)/1200=3$ km: el barri més proper representa cinc vegades més persones. El numerador suma habitants·km i el denominador habitants; el resultat torna a expressar-se en km.

Els dos resultats són correctes per a les seves preguntes. Els 5 km descriuen la mitjana de dues unitats administratives; els 3 km aproximen la distància assignada a un habitant triat entre els 1.200. Encara no són la distància real de cada persona: s'ha suposat que tot el barri es pot representar per una única distància. Ponderar millora la correspondència amb la pregunta demogràfica, però no elimina la simplificació espacial.

>> **Ponderar** vol dir que no totes les observacions contribueixen igual. Aquí el pes era el nombre d'habitants. Al capítol de centres espacials serà la potència associada a cada punt; al d'avaluació multicriteri serà la importància assignada a un criteri. Abans de multiplicar per un pes, cal poder explicar què representa.

## Relacions entre variables i regressió {#covariancia-regressio}

Viure més lluny del centre implica trigar més a arribar-hi? Per estudiar-ho fan falta **dues dades de cada trajecte**: distància i temps. Un **diagrama de dispersió** (*scatterplot*) les representa com un punt: es busca la distància a l'eix horitzontal i el temps al vertical. Un punt situat a 5 km i 50 minuts correspon a un trajecte amb aquestes dues característiques {% cite diez2019openintro %}.

### Quan dues variables canvien juntes

La taula conté trajectes en autobús en dos territoris ficticis. En A, les distàncies grans acostumen a anar acompanyades de temps llargs. En B passa el contrari. Això podria motivar preguntes sobre freqüències, transbordaments o connexions directes, però aquestes dades inventades només serveixen per aprendre a llegir les dues formes de relació.

::: table "Cinc trajectes de bus en cadascun de dos territoris ficticis"
| Distància al centre, km | Temps en A, min | Temps en B, min |
| ---: | ---: | ---: |
| 1 | 10 | 50 |
| 2 | 20 | 40 |
| 3 | 40 | 20 |
| 4 | 30 | 30 |
| 5 | 50 | 10 |
:::

En tots dos territoris, la distància mitjana és 3 km i el temps mitjà, 30 minuts. Les línies discontínues de la figura marquen aquests valors i divideixen cada gràfic en quatre parts. Un punt a dalt i a la dreta supera totes dues mitjanes; un punt a baix i a la dreta supera la distància mitjana, però té un temps inferior al mitjà.

![Distància al centre i temps en autobús en dos territoris ficticis, amb les mitjanes marcades]({{ site.baseurl }}/assets/quarto/figures/covariancia.qmd "Cada punt és un trajecte en bus. En A, els trajectes més llunyans tendeixen a durar més; en B, tendeixen a durar menys. Les línies marquen 3 km i 30 minuts, les mitjanes dels dos territoris. El rectangle destacat ajuda a calcular si distància i temps s'allunyen de la mitjana en el mateix sentit o en sentits contraris."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

La **covariància** (*covariance*) resumeix aquest canvi conjunt. Per calcular-la, primer es resta a cada valor la seva mitjana i després es multipliquen les dues diferències. En el trajecte de 5 km i 50 minuts, són +2 km i +20 minuts: el producte és +40 km·min. En el de 5 km i 10 minuts, són +2 km i −20 minuts: el producte és −40 km·min.

>> **Com es llegeix el signe?** Dos valors per sobre de les seves mitjanes donen un producte positiu; dos per sota, també. Si un és per sobre i l'altre per sota, el producte és negatiu. Això és el que resumeixen els colors dels quatre sectors del gràfic.

En A, els cinc productes són 40, 10, 0, 0 i 40: sumen 90 km·min. Amb el divisor mostral $n-1=4$, la covariància és 22,5 km·min. En B, els signes s'inverteixen i s'obté −22,5 km·min. La fórmula reuneix aquests passos, amb $x$ per a la distància i $y$ per al temps:

$$
s_{xy}=\frac{1}{n-1}\sum_i(x_i-\bar{x})(y_i-\bar{y}).
\label{eq:covariancia}
$$

### Una escala comuna per a la relació: la correlació

La covariància depèn de les unitats. Si les distàncies es passessin de quilòmetres a metres, el seu nombre es multiplicaria per mil, encara que els trajectes fossin els mateixos. La **correlació de Pearson** (*Pearson correlation*), representada amb la lletra $r$, permet descriure la relació en una escala sense unitats, entre −1 i +1.

Un valor proper a +1 indica que els punts segueixen una recta creixent: quan una variable augmenta, l'altra tendeix a augmentar. Un valor proper a −1 indica una recta decreixent. Un valor proper a zero indica que una recta descriu poc la relació; encara podria haver-hi una corba o grups amb comportaments diferents.

La correlació divideix la covariància per les desviacions estàndard de totes dues variables, $s_x$ i $s_y$:

$$
r=\frac{s_{xy}}{s_xs_y}.
\label{eq:pearson}
$$

En els trajectes anteriors, el producte de les desviacions estàndard és 25 km·min. Per això $r=22,5/25=0,9$ en A i $r=-0,9$ en B. Són relacions lineals marcades en aquests conjunts petits. La correlació descriu els punts, però no demostra per què el transport funciona així.

### De descriure una relació a fer una estimació

Ara podem preguntar-nos si la temperatura d'una estació es pot estimar a partir de la seva altitud. La **regressió lineal** (*linear regression*) busca una recta que resumeixi aquesta relació. Cada altitud introdueix un valor a la recta i n'obté una temperatura estimada. Abans d'aplicar-la, es dibuixen els punts per comprovar si una recta té sentit {% cite diez2019openintro %}.

Una recta s'escriu $\widehat y=a+bx$. Aquí $x$ és la dada coneguda i $\widehat y$, el valor que s'estima. El nombre $a$ situa la recta; $b$ indica quant canvia l'estimació quan $x$ augmenta una unitat. En l'exemple següent, les unitats de $b$ seran graus Celsius per metre d'altitud.

### Ajust, predicció i residu

Per a cada valor de x, la recta ofereix un valor estimat de y. El circumflex de $\widehat y_i$ recorda que és una estimació, mentre que $y_i$ és l'observació. Restar-los permet veure què no ha reproduït la recta:

$$
\widehat{y}_i=a+b x_i,\qquad e_i=y_i-\widehat{y}_i.
\label{eq:regressio-residu}
$$

El mètode de **mínims quadrats** (*least squares*) compara possibles rectes i tria la que fa més petita la suma dels residus al quadrat. És semblant al càlcul de dispersió: elevar les diferències al quadrat impedeix que errors positius i negatius es cancel·lin. La recta triada pot ser útil dins dels valors estudiats sense continuar sent adequada molt més enllà.

El **residu** (*residual*) és la diferència entre observació i valor ajustat als punts utilitzats. Un **error de predicció de validació** es calcula sobre una observació que no ha intervingut en l'ajust. Confondre'ls afavoreix una avaluació massa optimista: un model flexible pot reproduir molt bé les dades conegudes i predir malament en llocs nous.

### Llegir una recta i un residu amb dades completes {#exemple-regressio}

La taula següent conté altituds i temperatures fictícies d'un mateix indicador temporal. Les quatre primeres estacions s'utilitzen per ajustar; la cinquena es reserva per comprovar una predicció. Les altituds s'expressen en metres i les temperatures en °C. La separació es decideix abans de calcular la recta.

::: table "Observacions fictícies per seguir una regressió i una comprovació independent"
| Estació | Altitud, m | Temperatura, °C | Ús |
| --- | ---: | ---: | --- |
| E1 | 0 | 30 | Ajust |
| E2 | 100 | 30 | Ajust |
| E3 | 200 | 29 | Ajust |
| E4 | 300 | 27 | Ajust |
| V | 150 | 30 | Validació: no entra en l'ajust |
:::

La recta de mínims quadrats de E1–E4 és $\widehat{T}=30,5-0,01z$, on $z$ és l'altitud. El pendent indica una disminució estimada d'1 °C per cada 100 m, **només en aquest conjunt fictici**. A 200 m, el model prediu $30,5-0,01\times200=28,5$ °C. E3 observa 29 °C, de manera que el residu és $29-28,5=+0,5$ °C: és mig grau més càlida que el valor ajustat.

La figura situa les mateixes estacions sobre un perfil de relleu i en un gràfic de temperatura. L'altitud ocupa l'eix vertical dels dos dibuixos: E3 queda a 200 m en tots dos. En el gràfic de la dreta, el punt és la temperatura observada i la recta, l'estimada.

![Les mateixes estacions en un perfil de relleu i en un gràfic de temperatura, unides per les seves altituds]({{ site.baseurl }}/assets/quarto/figures/regressio-residus.qmd "Les estacions E1–E4 serveixen per calcular la recta. A E3, la temperatura observada és 0,5 °C superior a l'estimada: aquesta diferència és el residu. V es reserva per comprovar la recta amb una dada que no l'ha ajudat a calcular; allà la diferència és d'1 °C. Relleu i temperatures ficticis."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

L'altitud s'ha dibuixat verticalment per poder seguir cada estació del relleu al gràfic. El model continua estimant **temperatura a partir d'altitud**; el canvi de disposició només fa horitzontals les diferències de temperatura. El perfil dona un context espacial als punts, però les distàncies al llarg del perfil no entren en aquesta regressió.

>> **Llegeix el residu d'E3.** Busca els 200 m d'altitud. El punt és a 29 °C i la recta a 28,5 °C. La separació horitzontal és mig grau: $29-28,5=+0,5$ °C. Un residu positiu vol dir que l'observació és més alta que l'estimació.

Per a V, la mateixa recta dona 29 °C a 150 m. La diferència $30-29=+1$ °C és ara un error de validació perquè aquesta observació no ha contribuït als coeficients. La figura fa visible la diferència entre ajustar i comprovar: els punts d'ajust construeixen la recta; el punt reservat n'examina una predicció.

>>>> El pendent −0,01 °C/m s'ha calculat amb nombres ficticis. No és una constant atmosfèrica ni una recepta per corregir temperatures reals. En una aplicació caldria estimar-lo amb observacions comparables, explorar altres explicacions i validar amb més casos.

El coeficient $R^2$ compara l'ajust de la recta amb una referència molt senzilla: predir sempre la mitjana. Si és proper a 1, la recta redueix molt les diferències respecte d'aquella referència; si és proper a 0, n'aporta poca millora. Parla de les dades utilitzades per ajustar, no de la qualitat garantida en llocs nous.

En aquest exemple, $R^2\simeq0,833$: la recta redueix en un 83,3% la suma dels errors al quadrat respecte d'estimar sempre 29 °C, la mitjana de les quatre estacions. Això explica què aporta la recta als punts coneguts. La comprovació amb V examina una altra qüestió: com funciona en una observació reservada.

#### Com s'obtenen els dos nombres de la recta

Per refer el càlcul, el pendent es pot obtenir dividint la covariància entre altitud i temperatura per la variància de l'altitud. Després es calcula el punt de partida amb les mitjanes:

$$
b=\frac{s_{xy}}{s_x^2},\qquad a=\bar{y}-b\bar{x}.
\label{eq:coeficients-regressio}
$$

Amb E1–E4, les mitjanes són 150 m i 29 °C. Els productes de desviacions sumen −500 m·°C i els quadrats de les desviacions d'altitud, 50.000 m². Com que els divisors mostrals es cancel·len, $b=-500/50000=-0,01$ °C/m. Finalment, $a=29-(-0,01)\times150=30,5$ °C. S'obté $r\simeq-0,913$; en una regressió amb una variable i terme independent, $R^2=r^2$.

### Temperatura i altura: el gradient adiabàtic {#gradient-adiabatic}

La disminució de temperatura amb l'altura té una explicació física important, però cal identificar **què es mou i què es compara**. Una parcel·la d'aire que ascendeix troba menys pressió, s'expandeix i es refreda. Si no intercanvia calor amb l'entorn i continua no saturada, es pot aproximar el canvi amb el **gradient adiabàtic sec** (*dry adiabatic lapse rate*), d'uns 9,8 °C per quilòmetre d'ascens {% cite noaa2023parcel %}.

>> Aquí **parcel·la d'aire** vol dir una porció d'aire que seguim durant el moviment. **Gradient** indica quant canvia una magnitud amb la distància o l'altura. **Adiabàtic** significa que no hi ha intercanvi de calor amb l'entorn; el refredament es produeix en expandir-se l'aire.

En un exemple conceptual, una parcel·la comença a 20 °C a l'altura de referència. Si puja 500 m sota aquests supòsits, perd aproximadament 4,9 °C i arriba a 15,1 °C. Si puja 1.000 m, arriba a 10,2 °C. La relació és:

$$
T(z)=T(z_0)-\Gamma_d(z-z_0).
\label{eq:adiabatic}
$$

Aquí z i la referència $z_0$ s'expressen en quilòmetres i $\Gamma_d=9,8$ °C/km és la magnitud positiva del refredament. El signe menys indica que la temperatura baixa en ascendir. Si s'utilitzen metres, el coeficient ha de passar a 0,0098 °C/m. La resta de temperatures té la mateixa magnitud en graus Celsius i kelvins.

![Una porció d'aire que puja i es refreda, comparada amb temperatures de quatre estacions situades a altituds diferents]({{ site.baseurl }}/assets/quarto/figures/gradient-adiabatic.qmd "A dalt se segueix la mateixa porció d'aire: en pujar 1.000 m, passa de 20 a 10,2 °C sota el model adiabàtic sec. A baix es comparen quatre llocs diferents. Cada fila comparteix l'escala d'altura entre el dibuix del relleu i el gràfic tèrmic. Són dos problemes diferents, encara que tots dos relacionin temperatura i altura."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

En la primera fila es pot resseguir la línia dels 500 m: la parcel·la i el punt del gràfic corresponen als mateixos 15,1 °C. En la segona, E3 queda a 200 m als dos panells i aporta una observació de 29 °C. Les escales verticals coincideixen dins de cada parell; el rang de la primera fila és més gran perquè s'hi representa un ascens de 1.000 m.

Quan la parcel·la assoleix saturació, la condensació allibera calor i el refredament és més lent i variable; no es prolonga automàticament el pendent sec. El **gradient ambiental** descriu el perfil de l'aire que envolta la parcel·la i pot incloure inversions. Finalment, una regressió entre estacions de superfície compara llocs diferents, influïts per costa, orientació, urbanització i situació meteorològica. Aquestes tres relacions ajuden a interpretar temperatura i altitud, però no són intercanviables. El capítol d'interpolació comença amb distàncies entre estacions i després explica com incorporar l'altitud i validar-ne l'aportació.

### La mateixa estadística en dues coordenades

També es poden resumir les posicions d'un mapa. La mitjana de les coordenades est–oest i la de les coordenades nord–sud situen un punt central. Si els punts segueixen una vall allargada, una el·lipse pot mostrar en quina direcció s'estenen més. S'apliquen així les idees de centre i dispersió a dues coordenades {% cite cressie1993statistics %}.

L'el·lipse és un resum de les posicions: no delimita una frontera administrativa ni garanteix que tots els punts siguin a dins. El capítol d'estadística espacial en desenvolupa el càlcul amb mapes. Aquí és suficient retenir la pregunta: on se situa el conjunt i en quina direcció s'estén?

## Veïnatge, dependència i escala {#relacions-models}

Un **model espacial** selecciona les parts del territori que ajuden a respondre la pregunta. Per estudiar accés a serveis, pot representar carrers i connexions com una xarxa. Per estudiar temperatura, pot representar un valor a cada posició: és un camp continu. Per estudiar usos del sòl, pot representar parcel·les o altres objectes delimitats. Aquesta elecció depèn d'allò que es vol conèixer, no només del format dels fitxers.

El **veïnatge** especifica quins llocs es comparen amb cada lloc. Poden ser els municipis que comparteixen límit o les estacions situades a menys de deu quilòmetres. Aquesta llista de relacions es pot escriure en una taula, anomenada **matriu de pesos W**: cada fila representa un lloc i cada columna un possible veí. El valor $w_{ij}$ indica quant contribueix el lloc j a l'entorn del lloc i. Al capítol d'autocorrelació se'n construirà una amb quatre unitats.

La proximitat sovint va acompanyada de semblances, com resumeix la formulació de Tobler {% cite tobler1970movie %}. Aquesta **dependència espacial** s'ha de comprovar en cada problema: barreres, alternances o connexions llunyanes poden donar altres patrons. La **heterogeneïtat** indica que les propietats o les relacions varien entre llocs. Per exemple, dos entorns poden tenir mitjanes diferents i, alhora, mostrar semblances entre veïns dins de cadascun.

### Extensió, resolució i agregació

L'extensió és el domini observat; la resolució, el detall de la representació; el suport, la unitat sobre la qual es defineix la mesura. Una graella fina no crea observacions noves. Rasteritzar valors municipals a 5 m manté informació municipal, encara que produeixi moltes cel·les. Tractar-les com observacions independents multiplica artificialment la mida de mostra.

>>> Un municipi té una renda mitjana publicada de 20.000 euros. Copiar aquest nombre a cadascuna de 10.000 cel·les crea 10.000 representacions del mateix resum, no 10.000 rendes observades. Si una cel·la coincideix amb una casa, tampoc se'n pot deduir la renda dels habitants. El detall del dibuix i el detall del coneixement són coses diferents.

L'àmbit de càlcul pot superar el de comunicació. Una xarxa ha de conservar recorreguts que surten i tornen a entrar; una conca visual necessita els obstacles intermedis; la interpolació es beneficia d'observacions exteriors ben distribuïdes. Retallar al final no és una regla mecànica, però sovint evita efectes de vora introduïts per un límit administratiu sense relació amb el procés.

### Unitats modificables: l'efecte de l'agregació {#maup}

Agrupar observacions en àrees ajuda a resumir-les, però també modifica el patró que es pot estudiar. El **problema de la unitat espacial modificable**, conegut com **MAUP** (*modifiable areal unit problem*), apareix quan taxes, correlacions o altres resultats depenen de la mida i de la delimitació de les agregacions. Es distingeixen l'**efecte d'escala**, en passar a unitats més grans o més petites, i l'**efecte de zonificació**, en canviar els límits tot mantenint un nombre comparable d'unitats {% cite longley2015gis %}.

Imaginem setze cel·les urbanes amb **100 habitants cadascuna**. En cada cel·la es coneixen el percentatge de persones de 65 anys o més i el nombre de viatges diaris en autobús per cada 100 habitants. Les dades són fictícies. Una inscripció «10/40» significa un 10% de persones de 65 anys o més i 40 viatges diaris per 100 habitants; no vol dir necessàriament quaranta viatgers diferents.

Primer es representen les setze cel·les per separat. Després s'agrupen en quatre zones horitzontals i es calculen els dos indicadors de cada zona. Finalment, es torna a fer el resum amb quatre zones verticals. No s'ha mogut cap habitant ni canviat cap viatge; només s'ha canviat la manera d'agrupar-los.

![Tres maneres de resumir els mateixos habitants i viatges de bus: cel·les, zones horitzontals i zones verticals]({{ site.baseurl }}/assets/quarto/figures/maup.qmd "Cada cel·la té 100 habitants. Els nombres mostren el percentatge de població de 65 anys o més i els viatges diaris en bus per 100 habitants. En agrupar per files, les zones més envellides tenen més viatges; en agrupar per columnes, en tenen menys. Les dades són les mateixes: ha canviat la divisió del mapa. Exemple fictici."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

La primera zona horitzontal reuneix 400 habitants. El percentatge de persones de 65 anys o més és $(10+14+18+22)/4=16\%$. Hi ha $(40+36+32+28)/4=34$ viatges diaris per 100 habitants. Es poden fer mitjanes simples perquè les quatre cel·les tenen la mateixa població. En conjunt continuen havent-hi un 22% de persones de 65 anys o més i 40 viatges per 100 habitants.

>> **Mira què representa cada punt de baix.** A l'esquerra és una cel·la; al mig i a la dreta, una zona de quatre cel·les. La línia puja al gràfic central i baixa al de la dreta. El canvi no prové d'un comportament nou de la població, sinó del resum territorial escollit.

El pas de setze cel·les a quatre zones il·lustra el canvi d'escala; la comparació entre les dues particions de quatre zones aïlla la zonificació. Els valors s'han construït per fer visible un canvi extrem de signe. En una aplicació, repetir l'anàlisi amb delimitacions justificades permet saber fins a quin punt la conclusió depèn de la divisió escollida. La unitat ha de respondre el procés i la pregunta, no seleccionar-se perquè produeix la correlació desitjada.

### Relacions entre àrees i entre individus {#fal-lacia-ecologica}

La **fal·làcia ecològica** (*ecological fallacy*) és un error d'interpretació: traslladar a individus una relació observada entre àrees o grups. Una correlació municipal descriu municipis; no identifica automàticament què passa entre les persones o instal·lacions que contenen. La distinció entre correlacions agregades i individuals és el problema clàssic exposat per Robinson {% cite robinson1950ecological %}.

Considerem divuit habitatges ficticis repartits en tres zones, amb sis habitatges a cadascuna. Es comparen superfície en m² i consum elèctric anual en MWh; 1 MWh equival a 1.000 kWh. Les superfícies mitjanes de les zones A, B i C són 60, 100 i 140 m², i els consums mitjans, 6, 10 i 14 MWh. Les zones amb habitatges més grans tenen, doncs, més consum mitjà.

![Superfície i consum dels habitatges de tres zones, comparats amb les mitjanes de cada zona]({{ site.baseurl }}/assets/quarto/figures/fal-lacia-ecologica.qmd "A l'esquerra, cada punt és un habitatge: dins de cada color, els més grans consumeixen menys energia a l'any. A la dreta, cada punt és la mitjana d'una zona i la relació sembla la contrària. El resum de les zones no explica com es relacionen els habitatges dins de cadascuna. Superfície en m², consum en MWh i dades fictícies."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

>> **Compara primer punts del mateix color.** En cada zona, anar cap a la dreta —més superfície— porta cap avall —menys consum—. Després compara les tres mitjanes de la dreta: ara la línia puja. La unitat que es compara ha canviat d'habitatge a zona.

Per exemple, a la zona A l'habitatge de 50 m² consumeix 7 MWh i el de 70 m², 5 MWh. Aquest patró no es podria recuperar a partir de la mitjana de 60 m² i 6 MWh. En dades observades, composició de les llars, ocupació o sistemes de climatització podrien ajudar a explicar diferències; aquí no s'ha mesurat cap d'aquests factors. La figura demostra una possibilitat matemàtica, no una llei del consum residencial.

MAUP i fal·làcia ecològica plantegen dues comprovacions diferents. El primer pregunta què canvia quan es modifiquen les unitats agregades. La segona pregunta si la conclusió es refereix a la mateixa unitat que les dades. Conèixer totes les mitjanes municipals no substitueix disposar d'observacions individuals per estudiar una relació entre individus.

## Inferència, validació i incertesa {#escala-incertesa}

Fer un càlcul amb les dades disponibles és una cosa; treure'n una conclusió sobre més casos és una altra. La mitjana de cinquanta temps de trajecte descriu aquelles cinquanta respostes. Per estimar el temps mitjà de tot el campus, també importa com s'ha triat la mostra i quant podria variar el resultat si es preguntés a altres persones. Aquest pas de les dades a una conclusió més general és la **inferència estadística** (*statistical inference*) {% cite diez2019openintro %}.

### Un cas de camp: comprovar una cinta mètrica {#cas-cinta}

En una pràctica es vol comprovar una cinta mètrica abans d'utilitzar-la. Es disposa d'un tram de **20 m de llargada coneguda** i es mesura setze vegades. Cada vegada es torna a col·locar i llegir la cinta. La pregunta és si tendeix a donar lectures massa grans o massa petites. És una situació de treball de camp; els valors següents són ficticis per poder seguir el raonament.

L'**error de cada lectura** és la distància llegida menys els 20 m coneguts. Una lectura de 20,03 m dona un error de **+3 cm**; una de 19,98 m, de **−2 cm**. El signe indica el sentit de la diferència. No significa necessàriament que algú hagi treballat malament: col·locació, tensió i lectura poden introduir petites variacions.

::: table "Errors de setze lectures d'una cinta sobre un tram de 20 m; dades fictícies"
| Lectures | Errors, en centímetres |
| --- | --- |
| 1–4 | −4, −2, −1, 0 |
| 5–8 | 0, +1, +1, +2 |
| 9–12 | +3, +3, +4, +4 |
| 13–16 | +5, +6, +8, +10 |
:::

Els errors sumen 40 cm. La seva mitjana és $40/16=2,5$ cm: en aquest grup s'ha llegit, de mitjana, 2,5 cm de més. Aquest és un resultat descriptiu. Per concloure que la cinta **tendeix** a donar lectures massa grans, cal preguntar-se si una diferència així podria aparèixer sovint només per la variació entre lectures.

>> **Una lectura i una tendència no són el mateix.** Una cinta ben ajustada pot donar algun error positiu i algun de negatiu. El que es vol detectar és un desajust persistent de la mitjana, anomenat **biaix**. Les seccions següents continuen aquest mateix cas, sempre amb errors expressats en centímetres.

### La distribució normal i la variació de les mitjanes {#normal-mitjanes}

Si es repetissin moltes lectures amb una cinta ben ajustada, s'esperarien moltes diferències petites al voltant de zero i menys diferències molt grans. Una manera de representar aquesta distribució és una campana simètrica: la **distribució normal** (*normal distribution*). El centre indica al voltant de quin error s'agrupen les lectures; l'amplada indica quant varien.

Per fer els càlculs de l'exemple, suposem que es coneix la dispersió habitual de la cinta: una desviació estàndard de **4 cm**. També suposem que els errors segueixen una normal i que cada repetició és independent de les anteriors. Són les condicions d'aquest model docent, no propietats garantides de qualsevol mesura de camp.

En la normal, aproximadament 68 de cada 100 lectures queden a menys d'una desviació estàndard del centre; 95 de cada 100, a menys d'1,96 desviacions. Si el centre és zero i la desviació és 4 cm, aquests marges són ±4 cm i aproximadament ±7,84 cm.

Ara es poden agrupar les lectures de setze en setze i calcular una mitjana per grup. Les mitjanes solen quedar més a prop del centre perquè part dels errors positius i negatius es compensen. La dispersió de les **mitjanes dels grups** s'anomena **error estàndard** (*standard error*, SE). Amb les condicions de l'exemple es calcula així:

$$
\mathrm{SE}=\frac{\sigma}{\sqrt{n}}.
\label{eq:error-estandard}
$$

El nombre $n$ és el de lectures de cada grup i la lletra grega $\sigma$ representa la desviació estàndard, aquí 4 cm. Per a setze lectures, $4/\sqrt{16}=1$ cm. Per tant, la dispersió d'una lectura és 4 cm i la de la mitjana de setze lectures és 1 cm. Són dues mesures de variabilitat diferents.

![Errors d'una lectura de la cinta i errors mitjans de grups de setze lectures, expressats en centímetres]({{ site.baseurl }}/assets/quarto/figures/normal-mitjanes.qmd "Mesurar el tram de 20 m una sola vegada dona resultats més variables que fer la mitjana de setze lectures. Per això la campana de baix és més estreta. El zero indica una lectura sense diferència respecte dels 20 m. Les zones pintades mostren on s'espera trobar aproximadament el 68% i el 95% dels resultats si la cinta està ben ajustada."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

>> **Com es llegeix la campana?** L'eix horitzontal indica centímetres de més o de menys. Els resultats s'acumulen sobretot on la campana és alta. Per saber quina proporció cau entre dos valors, es mira l'àrea sota la corba entre aquells valors, no només l'altura en un punt. Tota l'àrea representa el 100% dels resultats possibles.

La forma que adopten les possibles mitjanes és una **distribució mostral** (*sampling distribution*). No totes les dades originals tenen forma de campana: les rendes o les potències poden ser molt asimètriques. El teorema central del límit explica per què moltes mitjanes es poden aproximar amb una normal en augmentar la mostra, sota condicions com independència, distribució comuna i variància finita. Aquí no cal recórrer a aquesta aproximació: s'ha suposat que els errors individuals ja són normals.

### Què expressa un interval de confiança {#intervals-confianca}

La mitjana del nostre grup és +2,5 cm, però un altre grup de setze lectures donaria probablement una mitjana una mica diferent. Un **interval de confiança** (*confidence interval*, CI) acompanya l'estimació amb un marge que reflecteix aquesta variació. Amb el model de l'exemple, el marge del 95% és 1,96 vegades l'error estàndard. Com que aquest error estàndard és 1 cm, es resten i se sumen 1,96 cm als 2,5 cm observats:

$$
\bar{x}\ \pm\ 1,96\,\frac{\sigma}{\sqrt n}.
\label{eq:ic-mitjana}
$$

El signe $\pm$ indica «restar i sumar». L'extrem inferior és $2,5-1,96=0,54$ cm i el superior, $2,5+1,96=4,46$ cm. Així, el desajust mitjà estimat de la cinta queda entre **+0,54 i +4,46 cm**, amb el procediment del 95%. L'interval queda tot per sobre de zero; més endavant es relacionarà aquest resultat amb la prova per detectar un biaix.

Per entendre el 95%, imaginem que repetim moltes vegades la prova, sempre amb setze lectures noves. Cada grup dona una mitjana i un interval. Amb les condicions del model, aproximadament 95 de cada 100 intervals inclouran el desajust mitjà real de la cinta. Els altres no l'inclouran, encara que el càlcul estigui ben fet.

![Quaranta marges calculats a partir de grups de setze lectures d'una cinta ben ajustada, amb el zero assenyalat]({{ site.baseurl }}/assets/quarto/figures/intervals-confianca.qmd "Cada ratlla és l'interval obtingut amb un grup diferent de setze lectures. En aquesta simulació la cinta està ben ajustada: el desajust real és 0 cm, marcat per la línia vertical. Trenta-set intervals passen pel zero i tres no. Amb quaranta proves no s'ha d'obtenir exactament un 95% d'encerts."){: data-figure-width-web="42rem" data-figure-width-pdf="95%"}

>> **Què estima aquest marge?** El desajust mitjà de la cinta, no l'error de cadascuna de les lectures. El «95%» descriu quantes vegades acostuma a encertar el procediment en repetir-lo. Un interval ja calculat conté el valor real o no el conté; no s'atribueix un 95% de probabilitat a un valor real que és fix.

El factor 1,96 és adequat aquí perquè s'ha fixat un model normal amb dispersió coneguda. Si la dispersió també s'hagués d'estimar amb les setze lectures, s'utilitzaria habitualment la distribució **t de Student**. El marge canviaria: hi hauria una incertesa addicional. Per això una fórmula d'interval sempre va acompanyada de les condicions en què s'aplica.

### Contrast d'hipòtesis i p-valor {#contrast-hipotesis}

Una **prova o contrast d'hipòtesis** (*hypothesis test*) formalitza la pregunta: «el resultat s'allunya prou del que esperaríem amb una cinta ben ajustada?». La situació de partida és que la cinta no tingui un desajust mitjà: uns errors positius es compensarien amb altres de negatius. Aquesta situació s'anomena **hipòtesi nul·la** (*null hypothesis*). L'alternativa és que la cinta tendeixi a donar lectures de més o de menys.

Abans de fer la prova, es fixa una regla. En aquest exemple s'accepta que, fins i tot amb una cinta ben ajustada, la regla doni una falsa alarma aproximadament **5 vegades de cada 100**. Amb grups de setze lectures i el model normal descrit, això situa els límits de la regla a −1,96 i +1,96 cm d'error mitjà. Si la mitjana del grup queda fora, es considera prou estranya per posar en dubte l'ajust de la cinta.

La mitjana observada de **+2,5 cm** supera el límit positiu. La figura posa la regla i el resultat junts per poder veure aquesta comparació directament. També marca −2,5 cm: una diferència igual de gran en sentit contrari seria igualment important. Per això es diu que la prova és **bilateral** (*two-sided test*).

![Una sola campana amb els límits de la regla a menys i més 1,96 cm i el resultat observat de més 2,5 cm]({{ site.baseurl }}/assets/quarto/figures/contrast-hipotesi.qmd "Comprovació d'una cinta sobre un tram de 20 m. Les línies taronges marquen els límits fixats abans de la prova; la línia blava contínua marca els +2,5 cm d'error mitjà obtinguts. El resultat queda fora del límit. Les dues petites zones blaves sumen la probabilitat de resultats almenys tan allunyats del zero: aproximadament l'1,24%, si la cinta estigués ben ajustada."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

>> **Llegeix la figura en aquest ordre.** Primer localitza el zero: és l'absència de desajust mitjà. Després mira els límits taronges, que defineixen la regla. Finalment situa els +2,5 cm observats. Les zones blaves van encara més enllà, a banda i banda, i responen una altra pregunta: com de poc habitual seria un resultat tan allunyat del zero?

La resposta a aquesta darrera pregunta és el **p-valor** (*p-value*). Aquí val aproximadament **0,0124**, és a dir, **1,24%**. Si la cinta estigués ben ajustada i repetíssim la prova sota les mateixes condicions, només aquesta proporció de proves donaria una mitjana tan allunyada de zero com la nostra, o encara més. Com que l'1,24% és inferior al 5% escollit per a la regla, el contrast posa en dubte la situació de partida: es **rebutja la hipòtesi nul·la**.

>>>> El p-valor no diu que hi hagi una probabilitat de l'1,24% que la cinta estigui ben ajustada. Parteix de suposar que ho està i pregunta com de poc freqüent seria el resultat. Tampoc identifica la causa del desajust: caldria comprovar la cinta, la col·locació i el procediment {% cite wasserstein2016pvalues %}.

#### Els noms i símbols que apareixen als resultats estadístics

La nul·la s'abreuja $H_0$ i l'alternativa, $H_1$. La mitjana real dels errors s'escriu $\mu$; per tant, «sense desajust mitjà» s'escriu $H_0:\mu=0$. El 5% fixat abans de mirar les dades és el **nivell de significació**, $\alpha=0,05$. El p-valor, en canvi, es calcula després amb les dades obtingudes.

Un **estadístic** és un nombre calculat amb les dades. Per a aquesta prova es pot expressar l'error mitjà com a nombre d'errors estàndard que el separen del zero:

$$
z_{\mathrm{obs}}=\frac{\bar{x}-\mu_0}{\sigma/\sqrt n}.
\label{eq:contrast-normal}
$$

En la fórmula, $\mu_0$ és el valor proposat per la nul·la, zero. L'operació és $(2,5-0)/1=2,5$. El resultat ja no té unitats: indica que la mitjana observada és a 2,5 errors estàndard del zero. Aquest canvi d'escala permet consultar una normal estàndard, centrada a zero i amb desviació 1. A la figura s'han conservat els centímetres perquè es vegi què significa per a la cinta.

L'interval obtingut abans, de +0,54 a +4,46 cm, tampoc inclou zero. En aquest model, l'interval del 95% i el contrast bilateral amb un nivell del 5% són dues maneres coherents de presentar la mateixa comparació.

### Errors de tipus I i II, i potència {#errors-contrast}

La prova decideix a partir de només setze lectures i es pot equivocar. Imaginem dues cintes: una està ben ajustada; l'altra fa llegir, de mitjana, **3 cm de més** en el tram de 20 m. S'aplica a totes dues la mateixa regla dels límits ±1,96 cm. Poden passar dues equivocacions diferents.

Un **error de tipus I** (*type I error*) és una **falsa alarma**: la cinta està ben ajustada, però el grup de lectures cau fora dels límits. Un **error de tipus II** (*type II error*) és un **problema no detectat**: la cinta té un desajust, però la mitjana del grup queda dins dels límits. La taula permet seguir les quatre possibilitats sense utilitzar símbols.

::: table "Què conclou la prova i com està realment la cinta"
| Resultat de la prova | Cinta ben ajustada | Cinta amb desajust |
| --- | --- | --- |
| No es detecta un desajust | Encert | Problema no detectat: tipus II |
| Es detecta un desajust | Falsa alarma: tipus I | Encert |
:::

Amb la cinta ben ajustada, el model preveu unes **5 falses alarmes per cada 100 proves**, perquè així s'ha fixat la regla. Amb la cinta que fa llegir 3 cm de més, el mateix model preveu que aproximadament **15 de cada 100 proves no detectin el problema**. Les altres 85 sí que el detectarien. Una prova és sempre un grup de setze lectures, no una lectura aïllada.

![Dues graelles de cent proves: cinc falses alarmes amb una cinta ben ajustada i uns quinze problemes no detectats amb una cinta que fa llegir tres centímetres de més]({{ site.baseurl }}/assets/quarto/figures/errors-contrast.qmd "Cada quadrat representa una prova de setze lectures sobre el tram de 20 m. A l'esquerra, una cinta ben ajustada provocaria unes 5 falses alarmes de cada 100 proves. A la dreta, amb un desajust mitjà de +3 cm, unes 15 proves no el detectarien. Són freqüències esperades aproximades del model, no cent proves fetes al camp."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

>> **Pots obtenir un «no es detecta» amb una cinta desajustada.** Per això aquesta resposta no prova que la cinta sigui perfecta. Significa que aquell grup de lectures no ha activat la regla. El segon dibuix mostra aquest problema amb els quadrats taronges.

La capacitat de detectar un desajust concret s'anomena **potència estadística** (*statistical power*). Aquí és aproximadament del 85% per a un desajust de +3 cm. Seria diferent per a un desajust de +0,3 cm, molt més difícil de detectar amb les mateixes setze lectures. Als textos estadístics, la probabilitat de no detectar-lo s'escriu $\beta$ i la potència, $1-\beta$.

Es poden reduir les falses alarmes allunyant els límits de la regla, però llavors també es deixen passar més desajustos. Fer més lectures independents permet estimar la mitjana amb més precisió. Finalment, detectar 3 cm de diferència i decidir si són importants són qüestions diferents: depèn de si la cinta s'utilitza per situar una parcel·la de mostreig aproximada o per a una mesura que exigeix molta precisió.

### Què canvia amb dades espacials

En el cas de la cinta s'ha suposat que cada lectura aporta informació independent. En un mapa això sovint no passa: deu termòmetres al mateix pati poden explicar menys sobre la temperatura d'una comarca que deu estacions repartides per entorns diferents. Les observacions properes poden compartir condicions i errors. Utilitzar-les com si fossin independents pot produir intervals massa estrets i una confiança excessiva.

Per comprovar si valors semblants tendeixen a estar junts, es pot comparar el mapa observat amb mapes on s'han barrejat els mateixos valors entre llocs. És el procediment de **permutació** introduït al començament. Es pregunta si el patró observat és habitual entre aquells mapes de comparació. Aquesta prova té les seves condicions: barrejar llocs amb climes o funcions molt diferents pot no ser una referència adequada.

El capítol d'autocorrelació reprendrà aquest raonament amb Moran i contrastos locals. Amb molts contrastos augmenten les oportunitats de falsos positius, de manera que també s'ha de considerar el conjunt de proves. En qualsevol cas, un resultat significatiu s'interpreta juntament amb la magnitud, les unitats, el suport i els supòsits; no es converteix automàticament en una explicació causal ni en una prioritat territorial.

### Verificar, validar i reproduir

La **verificació** comprova que el càlcul s'ha fet com es volia: les dades són les previstes, els metres no s'han confós amb quilòmetres i la fórmula és correcta. La **validació** pregunta si el model serveix per a l'ús previst, comparant-lo amb observacions que permetin comprovar-lo. La **reproduïbilitat** permet que una altra persona refaci els passos i obtingui el mateix resultat. Repetir un càlcul no demostra, tot sol, que sigui un bon model del territori.

Recordem que un error de validació és **observació menys predicció** en un cas que no ha servit per calcular el model. Si quatre temperatures predites donen errors de −2, −1, +1 i +2 °C, la mitjana dels errors és zero. Però cap de les quatre prediccions ha encertat exactament. Per això interessa resumir també la mida dels errors sense que els signes es cancel·lin.

L'error absolut mitjà, **MAE** (*mean absolute error*), fa la mitjana de les distàncies a zero: $(2+1+1+2)/4=1,5$ °C. L'arrel de l'error quadràtic mitjà, **RMSE** (*root mean square error*), eleva primer els errors al quadrat i dona més pes als grans. En aquest cas és $\sqrt{(4+1+1+4)/4}\simeq1,58$ °C. Les fórmules escriuen aquestes dues operacions per a qualsevol nombre de casos:

$$
\mathrm{MAE}=\frac{1}{n}\sum_i |e_i|.
\label{eq:mae}
$$

$$
\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum_i e_i^2}.
\label{eq:rmse}
$$

Un biaix proper a zero pot ocultar errors positius i negatius grans. MAE i RMSE s'han d'interpretar en la unitat de la resposta i en relació amb l'ús. Si una diferència tèrmica entre candidates és menor que l'error de validació, establir un ordre precís amb decimals és poc informatiu.

>> **Una comprovació senzilla.** Si totes les prediccions fossin exactes, tots els errors serien zero i tant MAE com RMSE valdrien zero. En canvi, una mitjana d'errors igual a zero pot amagar diferències grans de signes oposats.

La diferència entre MAE i RMSE es pot comprovar canviant un error de +2 a +8 °C: tots dos resums augmenten, però el quadrat fa que el segon respongui més al valor gran. Escollir una mètrica depèn de l'ús: un error molt gran pot ser especialment problemàtic en una decisió amb un llindar crític. Cap resum únic substitueix revisar on es produeixen els errors.

Una **partició** és la separació entre dades per ajustar i dades per comprovar. Ha d'assemblar-se a la situació on s'utilitzarà la predicció. Retirar una estació que té moltes veïnes a prop és una prova menys exigent que retirar totes les d'una vall. Roberts i col·laboradors expliquen per què aquesta separació importa amb dades espacials {% cite roberts2017validation %}. Les observacions reservades han de quedar fora de tots els passos de l'ajust.

### Sensibilitat i robustesa

La sensibilitat pregunta què canvia quan es modifiquen dades, paràmetres o preferències. Desplaçar punts dins d'un marge plausible estudia incertesa de localització; canviar el veïnatge estudia una decisió de model; modificar pesos multicriteri estudia preferències. Aquestes proves tenen significats diferents i s'han de presentar separadament.

Un resultat és **robust** davant d'aquestes proves si canvia poc. Per exemple, si dues ubicacions continuen sent les preferides amb pesos una mica diferents, la tria depèn menys d'aquell pes concret. Això no elimina altres problemes: si totes les proves utilitzen un mapa incomplet, totes poden compartir el mateix error.

## Precedents del geodisseny {#mcharg}

Estudiar el lloc abans de transformar-lo relaciona el geodisseny amb la planificació regional, la planificació ecològica i la modelització cartogràfica. Aquests corrents aporten maneres de descriure el territori, interpretar-ne els processos i comparar intervencions. Els SIG faciliten una part de les operacions; les preguntes sobre què convé canviar i amb quins efectes tenen una història més llarga.

### Conèixer la regió i planificar amb els processos naturals

Patrick Geddes, a *Cities in Evolution* (1915), situa l'estudi de les ciutats en relació amb la regió, les activitats i la seva evolució. El reconeixement del lloc i la diagnosi regional són precedents importants d'una planificació que parteix del coneixement geogràfic. Una ciutat es pot estudiar juntament amb els espais que l'abasteixen, els desplaçaments i les transformacions del paisatge, més enllà del seu límit administratiu {% cite geddes1915cities %}.

Ian L. McHarg va publicar *Design with Nature* el 1969. Va proposar estudiar el relleu, l'aigua, els sòls, la vegetació i les activitats abans de decidir els usos del sòl. La superposició de mapes permet comparar aquestes condicions i valorar quins usos s'hi adequen. Aquesta és una de les seves aportacions a la planificació ecològica {% cite mcharg1969nature %}.

Per exemple, proposar una nova zona residencial només a partir de la distància al centre urbà podria ignorar inundabilitat, sòls o continuïtat d'hàbitats. La lectura conjunta pot suggerir una ubicació diferent o una altra forma d'ocupació. El valor de la superposició no és que moltes capes produeixin automàticament una resposta correcta: cal interpretar els processos, la qualitat de les dades i els criteris amb què es qualifiquen els llocs.

### De la superposició al model cartogràfic

La modelització cartogràfica desenvolupa maneres de combinar aquestes representacions de forma explícita. C. Dana Tomlin sistematitza l'**àlgebra de mapes** (*map algebra*) a *Geographic Information Systems and Cartographic Modeling* (1990). Les operacions poden relacionar valors en una mateixa posició, resumir un veïnatge o calcular propietats dins d'una zona. Aquesta distinció ajuda a expressar models com una seqüència d'operacions i a revisar què significa cada resultat {% cite tomlin1990cartographic %}.

Per exemple, combinar pendent, cobertes i distància a camins pot produir un mapa per estudiar possibles emplaçaments. Encara s'ha de decidir què es considera adequat, quines condicions exclouen una ubicació i quines diferències es poden compensar. L'avaluació multicriteri formalitza una part d'aquestes preferències i permet comparar-ne l'efecte {% cite malczewski1999gis %}. Una operació numèrica pot ser reproduïble sense que el judici que incorpora sigui compartit per tothom.

Michael F. Goodchild, en la seva discussió de 2010 sobre **geodisseny** (*geodesign*), recupera la relació dels SIG amb el disseny i amb la cartografia. Assenyala la necessitat de donar suport tant a l'esbós de propostes com als models científics sobre el funcionament del món. Dibuixar un canvi i estimar-ne les conseqüències han de poder relacionar-se: un polígon proposat pot modificar drenatge, accessos o visibilitat, no només l'aparença del mapa {% cite goodchild2010geodesign %}.

Geddes ajuda a situar la diagnosi regional; McHarg, la lectura ecològica del lloc; Tomlin, la formulació d'operacions cartogràfiques; i Goodchild, la connexió entre informació, models i disseny. El marc de Carl Steinitz organitza aquestes relacions mitjançant preguntes que van de la representació del territori a la decisió sobre alternatives, amb participació i retorns durant el procés {% cite steinitz2012framework %}.

## El geodisseny i les sis preguntes de Steinitz {#sis-preguntes-steinitz}

El **geodisseny** relaciona comprensió geogràfica, formulació de propostes, avaluació d'efectes i decisió sobre canvis territorials. Steinitz el planteja com una col·laboració entre ciències geogràfiques, professions del disseny i la planificació, especialistes tecnològics i persones del lloc. Les dades aporten evidència, però els objectius, els valors i les responsabilitats no es dedueixen d'una capa {% cite steinitz2012framework %}.

El marc organitza el treball mitjançant sis tipus de models i **tres iteracions**, amb funcions i sentits de lectura diferents. Primer es recorre de representació a decisió per comprendre el lloc i el problema. Després es treballa en sentit invers: a partir de la decisió que cal sostenir es dedueixen impactes, alternatives, criteris, processos i dades necessaris. La tercera iteració executa l'estudi de representació a decisió i incorpora retorns quan els resultats o la participació ho exigeixen {% cite steinitz2012framework psu2020steinitz %}.

![Les sis preguntes de Steinitz i els tres recorreguts per comprendre el lloc, preparar l'estudi i dur-lo a terme]({{ site.baseurl }}/assets/img/steinitz-marc.svg "Les sis preguntes es repassen tres vegades. Primer es coneixen el lloc i el problema, de dalt a baix. Després es parteix de la decisió que cal prendre per esbrinar quines dades i mètodes faran falta, de baix a dalt. Finalment es fa l'estudi, amb retorns si cal revisar-lo."){: data-figure-width-web="44rem" data-figure-width-pdf="100%" data-caption-source="Adaptació de Steinitz (2012) i del recurs GEODZ 511 de Penn State."}

>> **Una pregunta per començar.** Si s'ha de decidir entre dues ubicacions, quins efectes s'han de comparar? I quines dades permetran estimar-los? Aquest raonament cap enrere correspon a la fletxa que puja; ajuda a recollir informació que sigui útil per a la decisió.

Les sis preguntes s'aborden més d'una vegada. La primera iteració permet entendre el problema; la segona defineix com s'estudiarà; i la tercera aplica els mètodes triats. Durant el treball es poden revisar dades, mètodes, alternatives o escala. Els tres primers models descriuen el lloc, n'expliquen el funcionament i el valoren; els tres darrers estudien els canvis proposats.

### Representació: com s'ha de descriure el lloc?

El model de representació selecciona allò que s'ha de conèixer: objectes, variables, dates, relacions i qualitat. En una proposta de restauració fluvial, pot incloure lleres, usos, edificacions i cotes; en una proposta energètica, també elements de consum, generació i connexió. La selecció ha de respondre la pregunta, no acumular totes les capes disponibles.

Una parcel·la cadastral, una explotació agrària i una coberta observada són representacions diferents. Si s'equiparen al començament, les fases següents poden convertir una simplificació en una falsa afirmació sobre propietat o funció. El resultat d'aquesta pregunta és una base interpretada i un registre de mancances, no només un mapa amb moltes capes.

### Procés: com funciona el territori?

El model de procés representa relacions que expliquen o simulen funcionament: circulació, temperatura, drenatge o visió. Una distància recta pot aproximar una relació, però no conté connectivitat, horaris ni barreres. Cal explicar què conserva la simplificació i què omet.

Una correlació pot revelar una relació útil per predir, sense identificar un mecanisme causal complet. En canvi, una relació física també necessita dades i paràmetres adequats. La utilitat d'un model es valora segons la pregunta, el domini i la validació, no només segons la seva complexitat.

### Avaluació: el funcionament és satisfactori?

Una mesura es converteix en valoració quan es relaciona amb un criteri. Quinze minuts fins a un servei poden considerar-se acceptables en un context i insuficients en un altre. La mateixa exposició visual pot rebre valoracions diferents segons receptor, paisatge i objectiu. Els criteris han d'indicar qui els estableix i amb quina justificació.

Cal separar normes aplicables, coneixement expert i preferències. Un llindar normatiu necessita una font i un àmbit; un llindar docent necessita identificar-se com a convenció; una preferència necessita atribució. Presentar-los tots com a propietats objectives del terreny oculta decisions substantives.

### Canvi: quines alternatives es poden formular?

Les alternatives especifiquen què canvia, on, amb quina extensió i en quin horitzó. Poden modificar un traçat, conservar un corredor, distribuir una ocupació o combinar actuacions. La proposta inclou els elements associats: una instal·lació amb accessos i línies produeix més transformacions que el seu polígon principal.

La comparació necessita una funció comuna o diferències de servei explícites. Una alternativa més petita pot ocupar menys sòl perquè aporta menys servei. Cal incloure una referència, que pot ser un escenari sense l'actuació però amb altres canvis previstos. «No fer aquest projecte» no significa que el territori romangui immòbil.

### Impacte: què canviaria respecte de la referència?

El model d'impacte compara conseqüències sota condicions coherents. Un nou accés pot modificar temps de recorregut; una ocupació pot fragmentar una explotació; un conjunt d'actuacions pot generar exposició acumulada. L'impacte no és simplement el valor absolut d'un indicador.

Per exemple, si en un tram hi passen 10 camions per hora sense el projecte i se'n preveuen 14 amb el projecte, el canvi estimat és $14-10=+4$ camions per hora. Es comparen el mateix lloc i el mateix horitzó temporal. Aquesta resta es pot escriure així:

$$
\Delta I=I_1-I_0.
\label{eq:impacte-referencia}
$$

Aquí $I_1$ és el valor amb projecte, $I_0$ és el de referència i $\Delta I$ vol dir «canvi en l'indicador». El signe positiu només indica un augment: més camions poden ser desfavorables per al soroll i més energia produïda pot ser favorable per a un altre objectiu. La interpretació depèn d'allò que es mesura i de qui en rep els efectes.

### Decisió: quin canvi resulta preferible?

La decisió relaciona efectes, restriccions i preferències. Pot concloure seleccionant, modificant, combinant o descartant alternatives; també pot justificar una dada addicional abans d'escollir. L'avaluació multicriteri aporta un llenguatge per ordenar aquests arguments, però no substitueix la deliberació ni les competències de decisió {% cite malczewski1999gis %}.

Una puntuació alta no anul·la una restricció. Tampoc no acredita disponibilitat del sòl o acceptació social. La recomanació ha d'explicar quines condicions la sostenen i quins canvis la farien variar. Si totes les alternatives són inadequades, el retorn pot afectar l'objectiu o el disseny, no només els pesos.

### Un hort solar en una plana agrària {#steinitz-hort-solar}

Imaginem un **territori fictici** amb conreus de secà, dos nuclis habitats, una riera estacional, camins agrícoles i un polígon industrial. S'hi estudia un hort solar. Els conreus continuen en explotació, els camins donen accés a les finques i la riera concentra l'escorrentia durant episodis de pluja. Aquestes funcions formen part de la situació de partida: una superfície sense edificacions no és un espai sense ús ni relacions.

El model de **representació** reuneix relleu, cobertes, recintes cultivats, cursos d'aigua, habitatges, camins i infraestructures elèctriques, amb les dates i els límits de cada font. També necessita informació sobre usos i accessos que pot requerir observació de camp i consulta a les persones del lloc. Una línia elèctrica dibuixada al mapa no acredita que admeti una nova connexió; aquesta dada s'ha d'obtenir de la font competent.

Els models de **procés** expliquen com hi circula l'aigua, quins recorreguts mantenen les explotacions i des d'on es veuria la instal·lació. L'estimació de generació relacionaria irradiació, temperatura i característiques del sistema. L'**avaluació** pregunta si el funcionament actual i les condicions del lloc són adequats per als objectius plantejats: per exemple, preservar la continuïtat agrària i evitar incrementar problemes de drenatge. Els criteris, les restriccions aplicables i les preferències dels actors es documenten separadament.

El model de **canvi** concreta dues propostes: una ocupació compacta al costat d'un accés existent i una distribució en recintes que conserva un pas agrícola i una franja de drenatge. Cada alternativa inclou accessos, tancaments i connexió, a més dels panells. La comparació fixa un mateix horitzó i una generació anual estimada equivalent; si això no es pot aconseguir, s'ha d'explicar la diferència de servei. La referència sense projecte conserva els usos previstos per a aquell horitzó, no una superfície buida.

El model d'**impacte** estima les diferències respecte d'aquesta referència: sòl ocupat, recorreguts agrícoles, drenatge, exposició visual i energia produïda, amb les seves incerteses. Suposem, només per il·lustrar la lectura de les magnituds, que les petjades completes de les alternatives fossin 12 i 9 ha. La segona ocuparia 3 ha menys que la primera; respecte de la referència sense nova ocupació solar, els increments serien +12 i +9 ha. Cap dels dos nombres, tot sol, informa de la fragmentació de les explotacions.

La **decisió** compara el conjunt d'efectes amb les preferències i les responsabilitats corresponents. Si la proposta de 9 ha obliga a fer una volta llarga per accedir a un recinte cultivat, es pot tornar al model de canvi i ajustar el pas. Si la dada de connexió no és suficient, el retorn afecta la representació i la viabilitat de les alternatives. Les aportacions d'agricultors, veïnat, promotors i administracions poden modificar tant el disseny com els criteris de comparació.

![Sis vinyetes d'una plana agrària: lloc, circulació d'aigua i accessos, elements a conservar, dues disposicions solars, ocupació de sòl i revisió amb les persones implicades]({{ site.baseurl }}/assets/quarto/figures/steinitz-solar-exemple.qmd "Un hort solar en un lloc fictici. Els quatre primers mapes mostren el mateix territori: N1 i N2 són nuclis habitats. A ocupa un recinte de 12 ha; B, dos recintes que sumen 9 ha i deixen el pas central lliure. Les barres comparen la nova ocupació. La darrera vinyeta recorda que també s'han de valorar els accessos, la connexió i les perspectives locals."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

>> **Segueix el camí agrícola.** Existeix abans del projecte, serveix per arribar als camps i es vol conservar. La forma de l'alternativa afecta aquest camí. Per això escollir només la barra més baixa —menys hectàrees ocupades— no resol tota la decisió.

Aquest mateix exemple permet llegir la **segona iteració en sentit invers**. Si la decisió ha de valorar la continuïtat agrària, cal estimar-ne els impactes; això exigeix alternatives amb accessos definits, un model de recorreguts i dades sobre el funcionament de les explotacions. La necessitat de dades es dedueix del problema que s'ha de resoldre. La tercera iteració aplica els mètodes seleccionats i revisa la proposta quan les conseqüències no són satisfactòries. El capítol d'avaluació multicriteri reprèn aquest cas amb més detall.

### Un abocador en una conca amb nuclis habitats {#steinitz-abocador}

Considerem ara una **conca fictícia** amb dos nuclis, camps, una carretera principal i pous d'abastament. Es vol estudiar on gestionar una quantitat prevista de residus no perillosos que han de destinar-se a dipòsit controlat. Hi ha dues possibles ubicacions: una propera a la carretera i una altra amb un accés més llarg. La situació de referència és continuar amb el sistema de gestió previst sense el nou projecte; inclou els transports i instal·lacions corresponents.

La **representació** incorpora el relleu, la xarxa de drenatge, la geologia i hidrogeologia, els pous, els habitatges, els usos i les rutes de transport. En aquest cas, una incertesa sobre el subsòl pot ser més decisiva que una petita diferència en la distància a la carretera. Les dades cartogràfiques inicials poden orientar on investigar, però no substitueixen l'estudi del terreny necessari per valorar una ubicació.

Els models de **procés** estudien escorrentia, infiltració, circulació subterrània i recorreguts de camions. Per examinar un possible transport de contaminants s'han de formular les vies de circulació i les condicions de funcionament o fallada que es volen analitzar. La distància recta a un pou no representa per si sola aquesta connexió. L'**avaluació** confronta el funcionament i la vulnerabilitat del lloc amb els objectius de protecció, els usos existents i la normativa aplicable, que en un cas real s'hauria de verificar.

El model de **canvi** defineix cada emplaçament amb la seva capacitat, fases, cel·les de dipòsit, accessos i sistemes de gestió d'aigües i lixiviats. Els lixiviats són els líquids que han estat en contacte amb els residus i n'han incorporat substàncies. Es comparen alternatives que gestionen una mateixa quantitat i tipus de residus durant un horitzó comú. El model d'**impacte** estima els canvis en trànsit, soroll, ocupació, paisatge i condicions de l'aigua respecte de la referència. Inclou el període de funcionament i les conseqüències després del tancament, així com la distribució dels efectes entre nuclis i receptors.

La **decisió** no es redueix a triar la parcel·la més allunyada de les cases o la ruta més curta. Una ubicació pot escurçar transports i, alhora, plantejar més incertesa hidrogeològica. Una restricció que la faci inviable no es compensa donant més pes a l'accessibilitat. Es pot descartar una alternativa, reformular-ne els accessos o obtenir informació addicional abans de decidir. Si canvia la previsió de residus per mesures de prevenció i tractament, també es revisen la capacitat necessària i el problema inicial.

En la iteració de disseny dels mètodes, la necessitat de justificar la protecció dels pous condueix cap enrere: des de la decisió fins als impactes sobre l'aigua, els escenaris de canvi, els processos hidrogeològics i les dades necessàries. Residents, responsables de l'abastament, gestors de residus i administracions poden identificar receptors, recorreguts i preocupacions que un inventari inicial no recollia. La participació acompanya la formulació de les alternatives, no només la presentació d'una ubicació ja escollida {% cite steinitz2012framework %}.

![Sis vinyetes d'una conca: nuclis i pou, circulació, receptors a protegir, dos emplaçaments, possible via de lixiviats i retorn a l'estudi del subsòl]({{ site.baseurl }}/assets/quarto/figures/steinitz-abocador-exemple.qmd "Dos possibles emplaçaments d'un abocador en una conca fictícia. A té un accés més curt que B, però també s'ha d'estudiar què podria passar amb l'aigua i el pou P. El tall del subsòl dibuixa una possible via de lixiviats en cas de fallada: és una hipòtesi per investigar. La decisió pot ser obtenir aquesta informació abans de triar."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

>> **Segueix el pou P.** Primer se'n coneix la posició. Després es pregunta d'on li arriba l'aigua i si el projecte hi podria introduir un canvi. La distància a la carretera no respon aquesta pregunta: cal estudiar el subsòl i la circulació de l'aigua.

Els dos exemples comparteixen les sis preguntes, però demanen models i dades diferents. En l'hort solar, conservar un accés agrícola pot conduir a redistribuir els recintes; en l'abocador, una incertesa sobre circulació subterrània pot exigir una investigació abans de comparar puntuacions. El marc ajuda a explicar aquests retorns i a relacionar coneixement del lloc, propostes i decisió.

## L'àrea de treball i les dades {#cas-fotovoltaic}

Com a TIG, el manual utilitza sobretot un territori proper per explicar els mètodes: el Camp de Tarragona, amb molts exemples al Tarragonès. La familiaritat amb els llocs ajuda a interpretar els mapes i a contrastar-los amb el terreny. Un camí conegut, per exemple, permet entendre millor per què un càlcul de ruta passa per un lloc o en descarta un altre.

Els exemples inclouen accessos, visibilitat, autoconsum o temperatures. Les pràctiques poden canviar de problema i d'àrea. Els conceptes de distància, dispersió, veïnatge o incertesa continuen sent útils per estudiar altres territoris i treballar amb fonts diferents.

Canviar de font exigeix tornar a mirar què representa cada dada. Un punt d'un inventari pot situar un consumidor associat a una instal·lació; una estació meteorològica correspon a un lloc de mesura; una parcel·la representa una superfície delimitada. Conèixer-ne el significat, la data i l'escala permet decidir si el mètode és adequat i quines adaptacions necessita.

La bibliografia ofereix aplicacions en altres contextos. Geurs i van Wee estudien l'accessibilitat en relació amb transport i usos del sòl; Bishop, la percepció visual de turbines; Hengl i col·laboradors, la combinació de regressió i kriging. Se'n poden comparar els plantejaments i els mètodes, revisant els supòsits abans d'aplicar-los a un altre lloc {% cite geurs2004accessibility bishop2002visual hengl2007regression %}.

## Activitats {#activitats-fonaments}

### Comprovació de conceptes

Quatre barris tenen valors 10, 10, 30 i 30. En un mapa, els dos barris de valor 30 són veïns; en un altre, estan separats pels de valor 10. Calcula la mitjana en els dos casos i explica què conserva el nombre i què canvia al mapa. Respon també: una potència desconeguda s'ha de substituir per zero? Si una predicció dona 29 °C i s'observen 30 °C, quin és l'error «observació menys predicció»?

>> Comprovació: la mitjana és 20 en tots dos mapes; el valor desconegut es conserva com a absent; i l'error és $30-29=+1$ °C. Acompanya els nombres amb una explicació, no només amb el resultat.

### Dues distribucions amb la mateixa mitjana

Compara les cinc potències **fictícies** 5, 5, 10, 20 i 60 kW amb cinc valors de 20 kW. Fes una taula amb total, mitjana, mediana, mínim, màxim i desviació descriptiva amb divisor $n$, i representa els dos conjunts en un gràfic. Tots dos han de sumar 100 kW i tenir mitjana 20 kW; només el segon té dispersió zero.

Dibuixa també els boxplots amb $Q_1=5$, mediana 10 i $Q_3=20$ en el primer conjunt. Comprova les tanques −17,5 i 42,5 kW i explica per què 60 es representa separat. Explica per què «la instal·lació mitjana té 20 kW» no descriu igualment els dos conjunts. Quina mesura ajuda a identificar una observació central? Quina relaciona el recompte amb la capacitat total?

### Observació, suport i representació

Considera tres dades: una instal·lació amb 10 kW de potència registrada, una parcel·la de 2 ha i una estació que mesura una màxima de 31 °C en un dia. Fes una taula amb què s'observa, què es mesura, en quines unitats i a quin espai o període correspon. Quina informació temporal falta en els dos primers casos? Explica per què posar les tres dades en punts sobre un mapa no les fa equivalents.

### Relació, residu i validació

Fes servir les dades fictícies d'aquesta taula. La recta calculada només amb E1–E4 és $\widehat T=30,5-0,01z$, on $z$ és l'altitud en metres i la temperatura estimada s'expressa en °C.

::: table "Dades per a l'activitat de temperatura, residu i validació"
| Estació | Altitud, m | Temperatura observada, °C | Paper |
| --- | ---: | ---: | --- |
| E1 | 0 | 30 | Calcular la recta |
| E2 | 100 | 30 | Calcular la recta |
| E3 | 200 | 29 | Calcular la recta |
| E4 | 300 | 27 | Calcular la recta |
| V | 150 | 30 | Comprovar-la després |
:::

Calcula les cinc temperatures estimades i resta-les de les observades. Per exemple, a E1 s'estimen 30,5 °C i l'error és $30-30,5=-0,5$ °C. Conserva una taula amb observació, estimació i diferència. Per a E1–E4 s'han d'obtenir −0,5, +0,5, +0,5 i −0,5 °C; per a V, +1 °C.

Dibuixa els punts i la recta, i marca V amb un símbol diferent. Explica per què l'error de V és una comprovació més independent que els altres. Finalment, situa una possible estació a 1.500 m: queda dins del rang amb què s'ha calculat la recta? Què caldria comprovar abans de confiar en la seva predicció?

### Llegir una afirmació estadística

Revisa tres afirmacions: «p < 0,05 demostra la causa», «una correlació nul·la demostra absència de relació» i «mil cel·les remostrejades són mil observacions noves». Escriu una versió corregida de cadascuna i explica quin supòsit faltava i com es podria comprovar.

### Canviar les zones mantenint les dades

Cada casella de la taula representa una cel·la amb 100 habitants. El primer nombre és el percentatge de població de 65 anys o més; el segon, els viatges diaris en bus per 100 habitants. Són les dades fictícies de l'exemple d'agregació, reproduïdes aquí per fer els càlculs.

::: table "Població de 65 anys o més (%) / viatges diaris en bus per 100 habitants"
| Posició | Columna 1 | Columna 2 | Columna 3 | Columna 4 |
| --- | ---: | ---: | ---: | ---: |
| Fila 1 | 10 / 40 | 14 / 36 | 18 / 32 | 22 / 28 |
| Fila 2 | 14 / 44 | 18 / 40 | 22 / 36 | 26 / 32 |
| Fila 3 | 18 / 48 | 22 / 44 | 26 / 40 | 30 / 36 |
| Fila 4 | 22 / 52 | 26 / 48 | 30 / 44 | 34 / 40 |
:::

Calcula les mitjanes de cada fila: la primera ha de donar 16% i 34 viatges per 100 habitants. Repeteix-ho per columnes: la primera dona 16% i 46 viatges. Dibuixa els quatre punts de cada agrupació, amb el percentatge a l'eix horitzontal i els viatges al vertical. Explica per què una sèrie puja i l'altra baixa sense que cap dada original hagi canviat. Conserva les dues taules de mitjanes i els gràfics.

### Què es pot afirmar sobre un habitatge?

Les zones següents contenen sis habitatges ficticis cadascuna. Només se'n coneixen inicialment les mitjanes.

::: table "Mitjanes de tres zones per a l'activitat sobre dades agregades"
| Zona | Superfície mitjana, m² | Consum mitjà anual, MWh |
| --- | ---: | ---: |
| A | 60 | 6 |
| B | 100 | 10 |
| C | 140 | 14 |
:::

Escriu una conclusió sobre les **zones**. Es pot afirmar amb aquesta taula que un habitatge més gran que un altre de la mateixa zona consumeix més? Ara s'afegeixen dues dades de la zona A: un habitatge de 50 m² consumeix 7 MWh l'any i un de 70 m² en consumeix 5. Explica què permeten comprovar aquestes dues observacions i conserva una conclusió corregida.

### Un interval i una decisió

Una cinta mesura setze vegades un tram conegut de 20 m. Els errors següents són en centímetres: un valor positiu significa que s'ha llegit de més. Es manté el model de l'exemple: errors normals independents amb desviació coneguda de 4 cm.

::: table "Errors de les setze lectures per a l'activitat de la cinta mètrica"
| Lectures | Errors, cm |
| --- | --- |
| 1–4 | −4, −2, −1, 0 |
| 5–8 | 0, +1, +1, +2 |
| 9–12 | +3, +3, +4, +4 |
| 13–16 | +5, +6, +8, +10 |
:::

1. Suma els errors i calcula la mitjana. Comprova que són 40 cm i +2,5 cm, respectivament. Quina lectura en metres correspon a un error de +3 cm?
2. Calcula l'error estàndard amb $4/\sqrt{16}$ i el marge del 95% multiplicant el resultat per 1,96. Resta i suma el marge a la mitjana: els extrems són +0,54 i +4,46 cm. Què significa que el zero quedi fora?
3. La regla fixada abans de la prova assenyala un possible desajust si l'error mitjà queda fora de −1,96 a +1,96 cm. Dibuixa aquests límits en una recta graduada i situa-hi els +2,5 cm observats. Quina decisió dona la regla?
4. El p-valor calculat amb aquest model és 1,24%. Explica'l començant amb «si la cinta estigués ben ajustada...». Descriu també una falsa alarma i un desajust no detectat.

Conserva els càlculs, la recta graduada i les explicacions. Com a ampliació, calcula el marge si cada prova tingués 64 lectures independents: s'ha d'obtenir 0,98 cm. Explica per què un marge més petit ajuda a estimar el desajust mitjà, però no repara una cinta que mesuri malament.

### Formular les sis preguntes

Planteja un canvi en un lloc que coneguis i respon les sis preguntes de Steinitz. Compara dues alternatives amb una mateixa referència i explica en quin moment caldria revisar una decisió anterior. Distingeix dades, supòsits i judicis. Quines persones podrien tenir preferències diferents sobre les alternatives?

Tanca la proposta indicant quina informació et faria modificar-la i per què.
