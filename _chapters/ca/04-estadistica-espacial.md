---
layout: manual-chapter
title: Estadística espacial descriptiva
description: "Comptar, localitzar centres i descriure dispersió i densitat amb els punts de Constantí i QGIS."
lang: ca
ref: distribucions-punts-densitat
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/punts-densitat/
weight: 40
part: Continguts
manual_references: true
---

Les biblioteques d'una ciutat, els arbres d'un parc o els casos d'una malaltia es poden representar amb punts. El mapa permet localitzar-los i reconèixer agrupacions, zones poc ocupades o alineacions. Però, com es compara una distribució amb una altra? Dos municipis amb el mateix nombre d'equipaments poden tenir-los concentrats en un nucli o repartits entre diversos barris.

L'**estadística espacial descriptiva** resumeix aquesta disposició amb mesures que tenen en compte on són els elements. Un recompte diu quants n'hi ha dins d'una àrea; un centre resumeix la posició del conjunt; una mesura de dispersió descriu quant s'estén. Cada resultat conserva una part de la informació del mapa i en deixa fora una altra. Per interpretar-lo es torna als punts i al territori.

>>>>> En acabar el capítol, cal poder llegir i reproduir resums d'una distribució puntual.
>>>>>
>>>>> - Distingir el nombre de registres de la quantitat que representa un atribut.
>>>>> - Comptar punts dins de polígons i explicar el denominador d'una densitat.
>>>>> - Interpretar un centre mitjà i el canvi que introdueix la ponderació.
>>>>> - Llegir el cercle i l'el·lipse de dispersió sobre els punts originals.
>>>>> - Explicar què canvia en ampliar el radi d'un mapa de calor.

## John Snow: un mapa que orienta una pregunta {#john-snow}

El metge **John Snow** va investigar el brot de còlera de **1854** a l'entorn de Broad Street, al Soho de Londres. El mapa que va publicar el **1855** situa defuncions, cases, carrers i bombes públiques d'aigua. La concentració de morts suggeria una pregunta: havien consumit aigua de la mateixa font? El mapa ajudava a localitzar el problema; entrevistes i altres observacions permetien contrastar aquella explicació {% cite snow1855cholera %}.

![Mapa històric amb les bombes d'aigua encerclades en blau]({{ site.baseurl }}/assets/quarto/figures/john-snow-pous.qmd "Cada barra negra representa una defunció associada a una casa. Els cercles blaus assenyalen les tretze bombes d'aigua, sense representar radis d'influència. La concentració entorn de Broad Street orienta una pregunta sobre el consum d'aigua; el dibuix, tot sol, no la respon."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="John Snow, mapa 1 de l'edició de 1855; litografia de C. F. Cheffins. [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Snow-cholera-map-1.jpg), [domini públic](https://creativecommons.org/publicdomain/mark/1.0/). Cercles afegits d'elaboració pròpia."}

<span id="unitats-dobservació-i-concentracions"></span>

Les barres no són tots els contagis ni tota la població. Si una casa amb quatre defuncions es representa amb un únic punt, comptar aquell punt una vegada descriu **cases afectades**; donar-li una contribució de quatre descriu **defuncions**. La posició pot ser la mateixa, però la quantitat estudiada canvia.

<span id="del-patró-espacial-a-la-hipòtesi"></span>

Snow també va estudiar excepcions: una institució pròxima tenia aigua pròpia, una cerveseria no depenia de la bomba de Broad Street i algunes persones que vivien lluny en rebien aigua. Proximitat i consum no eren equivalents. La maneta es va retirar el 8 de setembre de 1854, quan els nous atacs ja havien començat a disminuir; no s'ha de presentar aquella intervenció com una prova causal aïllada.

El cas mostra el valor d'una descripció espacial: **fer visible una disposició, precisar una pregunta i orientar comprovacions**. Explicar-ne les causes necessita altres dades. Aquesta distinció també guiarà la lectura d'una densitat o d'un centre espacial.

## Què representa cada punt? {#preguntes-punts}

Una distribució puntual reuneix les posicions d'un conjunt d'observacions. Abans de resumir-la s'identifica què és una observació: un arbre, una biblioteca, una defunció o un registre administratiu. El símbol no sempre representa una quantitat equivalent. Una biblioteca de 40 places i una de 400 poden dibuixar-se amb el mateix cercle.

Si cada biblioteca compta una vegada, es descriuen equipaments. Si cadascuna contribueix segons les seves places, es descriu capacitat: la segona biblioteca contribueix deu vegades més. Aquesta contribució és el **pes**. Ponderar no mou els punts; canvia la importància que tenen en el resum {% cite longley2015gis %}.

::: table "Preguntes i informació que conserva cada resum"
| Pregunta | Operació | Què s'obté? |
| --- | --- | --- |
| Quants elements hi ha a cada lloc? | Comptar dins de polígons | Nombre per àrea de treball |
| On s'equilibra el conjunt? | Coordenades mitjanes | Un punt central |
| Quant s'estén i en quina direcció? | Cercle i el·lipse de dispersió | Distàncies i allargament |
| On hi ha concentracions locals? | Densitat o mapa de calor | Variació de la concentració sobre el mapa |
:::

## Els registres d'autoconsum de Constantí {#preparacio-punts-qgis}

<span id="inventari-icaen"></span><span id="descàrrega-i-preparació-de-les-demostracions"></span><span id="camps-observats-i-controls"></span>

A Constantí, el mapa dels **124 registres** d'autoconsum permet reconèixer un grup dens al nucli i un altre conjunt sobre el polígon industrial occidental. Es pot preguntar si el grup amb més registres també és el que aporta més potència. Aquesta pregunta distingeix dues propietats: nombre de punts i quantitat associada a cadascun.

La font és l'[Observatori d'autoconsum de l'ICAEN](https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/). La coordenada correspon al **consumidor elèctric associat**, no necessàriament a la petjada dels panells. Els kW expressen potència, no energia produïda en kWh. L'extracció és del 28/09/2026; la data efectiva del conjunt no s'ha pogut establir {% cite icaenLocalitzacio %}.

El paquet docent **Constantí: estadística i autocorrelació** conté `constanti.gpkg`, ortofoto local i projectes per consultar els passos. Per començar, obre `01-recompte.qgz` i desa'n una còpia al teu directori de treball. També es pot preparar la vista des d'un projecte buit:

1. Estableix **EPSG:25831**, amb coordenades en metres. Desa el projecte i les sortides pròpies a `treball/`.
2. A **Explorador → GeoPackage → Connexió nova**, tria `constanti.gpkg` i desplega'l.
3. Afegeix `punts`, `limit` i `ortofoto.tif`. Anomena la capa de punts **Constantí · 124 punts** i apropa't a l'ortofoto.
4. Obre la taula i comprova **124 files**. Dos registres amb la mateixa coordenada continuen sent dues observacions; al mapa poden superposar-se.

![Registres d'autoconsum sobre el municipi de Constantí]({{ site.baseurl }}/assets/captures/c4-constanti-dades.png "Els punts indiquen consumidors associats de l'inventari. El grup oriental coincideix amb el nucli; a l'oest es distingeixen els recintes industrials. El registre de 450 kW està etiquetat per poder-lo recuperar en els càlculs següents."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="ICAEN, extracció 28/09/2026; límits ICGC 20/01/2026; [ortofoto ICGC 2025](https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms), retall WMS a 8 m/píxel. [Condicions ICGC](https://www.icgc.cat/condicions)."}

<span id="controls-demo"></span>

Tots els 124 registres tenen posició, però només **98 publiquen una potència numèrica**. Els altres 26 conserven un interval, com «més de 5 i fins a 25 kW». Poden intervenir en un recompte o en un resum de les posicions. Per sumar potències o ponderar-les es necessita una xifra, o una estimació declarada.

::: table "Controls del conjunt de Constantí"
| Dada | Valor | Ús immediat |
| --- | ---: | --- |
| Registres localitzats | 124 | Recompte i dispersió de les posicions |
| Potències publicades | 98 | Suma coneguda i comparació d'atributs |
| Només interval de potència | 26 | Posició coneguda; xifra no observada |
| Suma de potències publicades | 2.770 kW | Capacitat coneguda al registre |
:::

La cobertura cartogràfica que anuncia l'ICAEN —aproximadament el 93% del conjunt català— és una qüestió diferent del nombre de valors de potència disponibles. Tampoc s'ha de tractar aquesta selecció municipal com un cens físic complet de plaques solars. La font es conserva separada de les capes de treball.

## Comptar punts dins d'àrees {#comptar-constanti}

<span id="graella-i-recompte-amb-qgis"></span>

Comptar dins d'un polígon és una manera directa de passar del mapa a una taula. Si un quadrat conté 48 registres, la seva fila rep **48**. Canviar-ne el contorn pot canviar quins punts hi entren. Per això es comença amb quadrats de superfície igual: facilita comparar sense confondre nombre i mida de l'àrea.

La capa `malla` del paquet té **90 quadrats d'1 km de costat**, sobre una extensió que cobreix tots els punts de Constantí. Cada quadrat té 1 km². Es pot reproduir amb **Crea una malla**, tipus Rectangle (Polígon), espaiats horitzontal i vertical de 1.000 m i superposicions 0. L'extensió en EPSG:25831 és:

```text
343500,353500,4554000,4563000
```

Els dos primers nombres són el mínim i màxim est; els altres dos, el mínim i màxim nord. Aquí es mantenen els quadrats sencers, també quan travessen el límit municipal. Retallar-los canviaria les superfícies i, per tant, el denominador de la densitat.

### Recompte amb QGIS

Obre **Procés → Caixa d'eines → Anàlisi vectorial → Compta els punts al polígon**. L'eina també es pot cercar pel seu nom.

![Eina de recompte visible a la Caixa d'eines sobre el mapa de Constantí]({{ site.baseurl }}/assets/captures/c4-recompte-caixa.png "Compta els punts al polígon relaciona una capa de polígons amb una capa de punts. El mapa de fons conserva el mateix cas municipal, abans de calcular el resultat."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}

1. Tria **Quadrats d'1 km²** com a polígons i **Constantí · 124 punts** com a punts.
2. Deixa buits pes i classe. Anomena el camp **n_punts**.
3. Desa la sortida al GeoPackage de treball, amb nom `recompte`.
4. Comprova **90 files** i suma **124** al camp `n_punts`: cada registre ha entrat una vegada.

![Diàleg de recompte amb malla i punts de Constantí]({{ site.baseurl }}/assets/captures/c4-recompte-parametres.png "Els polígons defineixen les àrees on es compta. La capa de punts aporta les observacions. Sense pes, cada registre contribueix una unitat, també si la seva potència és absent."){: data-figure-width-web="38rem" data-figure-width-pdf="86%"}

![Quadrats acolorits segons el nombre de registres, amb els punts superposats]({{ site.baseurl }}/assets/captures/c4-recompte-resultat.png "El color resumeix quants registres hi ha dins de cada quadrat; els punts permeten comprovar-ho visualment. Un quadrat sense registres queda sense emplenament. La suma de tots els quadrats és 124."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="ICAEN; ortofoto i límits ICGC. Recompte amb QGIS."}

### Nombre i potència no són equivalents

El quadrat amb més registres conté **48**, amb **268 kW publicats**. Un altre quadrat, del sector occidental, conté **17 registres** però suma **891 kW publicats**. Hi ha menys observacions i més capacitat coneguda. Els dos recomptes fan tangible la pregunta inicial.

Per sumar potències, repeteix l'eina sobre la mateixa malla amb la capa **coneguda**, de 98 punts, i **POT_KW** com a pes. El camp nou `kw_pub` ha de sumar **2.770 kW**. Els 26 valors absents no s'han convertit en zero ni s'han inclòs com a xifres observades.

La **densitat** divideix la quantitat per la superfície. En un quadrat d'1 km², 48 registres equivalen a 48 registres/km². Si la mateixa quantitat fos dins de 0,25 km², serien $48/0{,}25=192$ registres/km². Una densitat de registres no és un percentatge d'adopció: per a aquest percentatge es necessitaria un denominador com el nombre de consumidors susceptibles de tenir autoconsum.

## Centre dels registres i centre ponderat {#centres}

<span id="escollir-el-resum-de-posició"></span>

El recompte mostra diferències dins de cada quadrat. Un **centre mitjà** resumeix, en canvi, la posició del conjunt sencer. Es fa la mitjana de les coordenades est i la de les coordenades nord: cada punt compta una vegada. Si es concentra més contribució a l'oest, un centre ponderat es desplaça en aquella direcció. El centre és una posició d'equilibri, no una instal·lació.

Un **centroide municipal** respon a una altra pregunta: resumeix la geometria del límit, com si tota la superfície contribuís igualment. No depèn dels registres. Un centre de punts i un centroide territorial poden diferir sense que cap dels dos estigui mal calculat.

### Estimar els pesos dels 26 intervals {#imputacio-intervals}

Per comparar centres sobre els **mateixos 124 punts**, s'utilitza un escenari de potència. Es conserva cada xifra publicada; als camps buits s'assigna el punt mitjà de l'interval. Si només se sap «més de 5 i fins a 25 kW», l'escenari utilitza **15 kW**. És una **imputació**, és a dir, una estimació per poder fer l'operació. No passa a ser una nova observació del productor.

::: table "Assignació central només quan falta POT_KW"
| Interval publicat | Valor assignat | Casos de Constantí |
| --- | ---: | ---: |
| Fins a 5 kW | 2,5 kW | 19 |
| Més de 5 i fins a 25 kW | 15 kW | 6 |
| Més de 25 i fins a 100 kW | 62,5 kW | 1 |
:::

<span id="camps-descenari-a-qgis"></span>

La capa `pesos` conserva `POT_KW` i afegeix **w_mid**, de tipus decimal. Per reproduir-la, crea una còpia de `punts` i aplica aquesta expressió a un camp nou amb aquell nom:

```sql
CASE
  WHEN "POT_KW" IS NOT NULL THEN "POT_KW"
  WHEN "INTERVAL" = 'Pot <= 5kW' THEN 2.5
  WHEN "INTERVAL" = '5 < Pot <= 25 kW' THEN 15
  WHEN "INTERVAL" = '25 < Pot <= 100 kW' THEN 62.5
  ELSE NULL
END
```

El resultat suma **2.970 kW d'escenari**: 2.770 publicats i 200 assignats. El registre de 450 kW es conserva sense canvis. Una classe oberta «més de 100 kW» sense xifra no tindria punt mitjà definit; aquest problema no afecta els 26 intervals de Constantí.

### Coordenades mitjanes a QGIS {#procediment-estadistica}

L'eina **Coordenades mitjanes** és a **Vectorial → Analysis Tools** i a **Anàlisi vectorial** dins de la Caixa d'eines. Les dues captures mostren aquesta mateixa distribució municipal {% cite qgisUserGuide %}.

::: subfigures a/b "Dos accessos a Coordenades mitjanes, amb Constantí com a context."
![Menú Vectorial desplegat fins a Coordenades mitjanes]({{ site.baseurl }}/assets/captures/c4-centres-menu.png "El menú obre l'eina des del grup d'anàlisi.")
![Coordenades mitjanes seleccionat a la Caixa d'eines]({{ site.baseurl }}/assets/captures/c4-centres-caixa.png "La mateixa eina és accessible a Anàlisi vectorial."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}
:::

1. Tria **Pesos de Constantí** i deixa buits **Pes del camp** i **Camp ID únic**. Així tots els 124 punts contribueixen igualment.
2. Desa aquesta sortida com a `centre_registres`.
3. Repeteix amb **w_mid** com a pes, també amb ID buit. Desa `centre_ponderat`.
4. Cada sortida ha de contenir **un punt**. Superposa'ls a les posicions originals i al mapa de pesos.

![Diàleg de coordenades mitjanes amb w_mid]({{ site.baseurl }}/assets/captures/c4-centre-parametres.png "w_mid és la contribució de cada registre. Deixar l'ID buit produeix un centre de tot el conjunt de Constantí, sense dividir-lo en grups."){: data-figure-width-web="38rem" data-figure-width-pdf="86%"}

![Centres dels registres i dels pesos sobre l'ortofoto]({{ site.baseurl }}/assets/captures/c4-centres-resultat.png "El rombe resumeix la posició dels registres; l'estrella, la dels pesos de potència. Els cercles grans aporten més pes. La separació entre els centres mostra que el nombre de registres i la capacitat d'escenari s'equilibren en llocs diferents."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="ICAEN i ICGC. Pesos publicats o assignats identificats a la capa; càlcul amb QGIS."}

### Interpretar el desplaçament {#interpretacio-constanti}

El centre dels registres és **(349.051,53; 4.557.573,88) m**. El ponderat és **(347.321,21; 4.558.177,04) m**: uns **1.832 m cap a l'oest i una mica al nord**. El grup del nucli té moltes observacions petites; al polígon industrial hi ha pesos elevats que fan una contribució important. Els decimals permeten comprovar el càlcul, sense atribuir precisió centimètrica al registre.

![Els mateixos punts amb contribució igual i amb símbols proporcionals al pes]({{ site.baseurl }}/assets/quarto/figures/constanti-pesos.qmd "A l'esquerra, tots els registres compten igual. A la dreta, l'àrea dels cercles és proporcional als pesos: blaus per als valors publicats i taronges per als assignats. El registre de 450 kW és al sector occidental. Els centres es poden identificar pel nom, sense confondre'ls amb punts observats."){: data-figure-width-web="46rem" data-figure-width-pdf="100%" data-caption-source="ICAEN i ortofoto ICGC 2025. Elaboració pròpia."}

Els 450 kW representen un **15,2%** del pes de l'escenari. Els cinc pesos més grans n'aporten el **37,4%**, mentre que les 26 assignacions només n'aporten el **6,7%**. La ponderació descriu aquest repartiment; no demostra per què existeix ni recomana construir una instal·lació al centre resultant.

<span id="exemple-controlat"></span>

>>> Amb dos punts ficticis, un de 10 kW a 0 km i un de 30 kW a 4 km sobre el mateix eix, el centre sense pes és a 2 km. Ponderant, els productes sumen $10\times0+30\times4=120$ kW·km; dividir per 40 kW dona **3 km**. El punt de més potència desplaça el centre cap a ell. A Constantí es fa aquesta mateixa operació en dues coordenades i amb 124 contribucions.

La forma general utilitza les coordenades $x_i$, $y_i$ i els pesos no negatius $p_i$. La suma dels pesos, $P$, ha de ser positiva:

$$
\begin{aligned}
\bar{x}_p&=\frac{\sum_i p_i x_i}{P},\\
\bar{y}_p&=\frac{\sum_i p_i y_i}{P},\\
P&=\sum_i p_i.
\end{aligned}
\label{eq:centre-x}
$$

<span id="sensibilitat-imputacio"></span>

Per comprovar la influència de l'estimació, les capes preparades conserven també un escenari baix i un d'alt. A Constantí, els centres extrems se separen **194 m**, força menys que el canvi de 1.832 m respecte del centre dels registres. Les tres regles provades mantenen el desplaçament cap al sector occidental. No són un interval de confiança ni cobreixen totes les combinacions possibles dels pesos absents.

## Extensió i orientació del conjunt {#dispersio-ellipse}

Un punt central no mostra quant s'escampen les observacions. Per descriure-ho es mesuren les separacions respecte del centre. El **cercle de dispersió** resumeix una distància en totes les direccions. L'**el·lipse** distingeix la direcció més allargada de la perpendicular. Les dues formes es llegeixen sobre els punts, no com una nova àrea d'instal·lacions {% cite lefever1926ellipse %}.

<span id="cercle-i-ellipse-de-linventari-icaen"></span><span id="extrems-i-agrupacions"></span>

![Cercle i el·lipse visibles sobre els 124 registres de Constantí]({{ site.baseurl }}/assets/captures/c4-cercle-ellipse.png "El cercle taronja i l'el·lipse blava comparteixen el centre dels registres. El cercle resumeix una separació típica; l'el·lipse segueix l'allargament entre el polígon industrial i el nucli. Hi ha punts fora dels contorns i espais amb pocs registres a dins: no són límits de cobertura."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="ICAEN; ortofoto i límits ICGC. Mateixos 124 punts, sense ponderar; representació amb QGIS."}

### Cercle de dispersió

La **distància estàndard** es calcula elevant al quadrat la distància de cada punt al centre, fent-ne la mitjana i obtenint l'arrel. El resultat de Constantí és **2.000,66 m**. En dibuixar un cercle d'aquest radi es conserva una mesura resumida de separació, sense exigir que tots els punts siguin a dins.

Amb distàncies de 1, 2 i 3 km, un exemple construït dona $\sqrt{(1^2+2^2+3^2)/3}=2{,}16$ km. No és el màxim de 3 km ni la mitjana ordinària de 2 km: el quadrat fa que les separacions grans contribueixin més. Per a $n$ punts amb distàncies $d_i$, sense pes:

$$
D=\sqrt{\frac{\sum_i d_i^2}{n}}.
\label{eq:distancia-estandard}
$$

### El·lipse i lectura de les direccions

L'el·lipse de Constantí té **1.934,44 m de semieix llarg** i **510,47 m de semieix curt**. Un semieix és la distància del centre fins a un extrem de l'eix: la longitud completa és el doble. El llarg és gairebé quatre vegades el curt, coherent amb l'allargament visible entre els dos grups. Un cercle no expressa aquesta diferència.

<span id="convenció-de-lellipse"></span><span id="entendre-la-forma-abans-dinterpretar-langle"></span>

L'eix és una orientació, sense sentit de circulació. No indica que les instal·lacions avancin d'un grup a l'altre. La convenció utilitzada dona als semieixos una desviació de les coordenades sobre cada direcció principal; no s'hi atribueix un percentatge fix de punts ni confiança en la posició del centre.

Per practicar la representació a QGIS, la capa `dispersio` conserva un centre amb aquests camps calculats:

::: table "Magnituds que es dibuixen a Constantí"
| Camp | Valor arrodonit | Lectura |
| --- | ---: | --- |
| D_m | 2.000,66 m | Radi del cercle |
| a_m | 1.934,44 m | Del centre a l'extrem de l'eix llarg |
| b_m | 510,47 m | Del centre a l'extrem de l'eix curt |
| azimut | 110,22° | Eix mesurat en sentit horari des del nord |
:::

Cerca **Geometria segons l'expressió** a la Caixa d'eines, tria `dispersio` com a entrada i Polígon com a sortida. Executa per separat les dues expressions i desa `cercle` i `ellipse`. El 72 controla el detall del contorn, no el nombre d'observacions.

```text
make_circle($geometry, "D_m", 72)
make_ellipse($geometry, "a_m", "b_m", "azimut", 72)
```

L'eina dibuixa a partir dels atributs; no estima la dispersió a partir d'un centre sol. El preparador calcula abans variàncies i covariància de les coordenades, que s'han introduït als [fonaments](../fonaments-geodisseny/). Per comprendre el resultat aquí, interessa reconèixer quines separacions resumeixen les dues formes i què amaguen del conjunt.

## Comparar distribucions municipals {#comparacio-municipis}

El Morell, el Catllar i Constantí il·lustren distribucions diferents. El Morell és compacte; el Catllar té grups més separats; Constantí presenta un allargament marcat. Es conserven tots els registres de cada municipi, sense ponderar.

![Distribucions municipals amb zoom adaptat i barres d'escala]({{ site.baseurl }}/assets/quarto/figures/punts-municipis.qmd "Cada panell s'apropa al seu conjunt perquè es puguin veure els punts, el cercle i l'el·lipse, també al Morell. Les escales són diferents: compara les barres d'escala i els radis numèrics, no la mida aparent dels contorns. Els límits municipals visibles donen context."){: data-figure-width-web="49rem" data-figure-width-pdf="100%" data-caption-source="ICAEN i límits ICGC. Resums sense ponderar; elaboració pròpia."}

Els radis són **323 m al Morell**, **2.278 m al Catllar** i **2.001 m a Constantí**. La comparació quantifica separacions que ja es poden reconèixer al mapa. Ponderar pels escenaris centrals només desplaça els centres del Morell i del Catllar uns 22 i 56 m: tenir més dispersió i tenir els pesos concentrats a un costat són propietats diferents.

<span id="el-resum-comarcal-com-a-referència"></span>

Un resum de tota la comarca barreja distribucions locals d'aquesta mena. Té sentit quan la pregunta és comarcal; no substitueix la lectura dels municipis. En traslladar el procediment es revisen selecció, pes, límits i escala, en lloc d'assumir que un centre regional explica tots els grups.

## Concentracions locals i mapa de calor {#densitat}

<span id="densitat-kernel-i-escala-de-suavització"></span>

La malla imposa vores: dos punts molt pròxims poden quedar en quadrats diferents. Una **densitat kernel**, també anomenada mapa de calor, reparteix la contribució de cada punt al seu voltant. A prop del punt la contribució és gran; disminueix en allunyar-se. El mapa suma aquestes contribucions a cada cel·la.

El **radi** fixa fins on arriba aquesta influència. Amb 500 m es distingeixen grups locals; amb 1.500 m es fusionen més contribucions. La **mida de píxel**, de 100 m en aquest exemple, és el detall de la graella que desa la superfície: no és el radi d'influència. Ampliar el radi no afegeix registres ni descobreix una causa de l'agrupació.

### Accés i paràmetres de QGIS {#mapa-de-calor-amb-qgis}

Obre la Caixa d'eines i cerca **Mapa de calor**. En la versió de referència és dins d'**Interpolació**, amb el nom **Mapa de calor (KDE, estimació de densitat de nuclis)**.

![Mapa de calor seleccionat a la Caixa d'eines]({{ site.baseurl }}/assets/captures/c4-kernel-caixa.png "La fila ressaltada localitza l'eina que crea el ràster. El mapa continua mostrant els punts de Constantí; es pot relacionar la configuració següent amb aquest conjunt concret."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}

1. Entrada: **Constantí · 124 punts**. Radi: **500 m**. Píxel X i Y: **100 m**.
2. A **Advanced Parameters**, tria kernel **Quartic**, sortida **Raw**, i deixa buit el pes. Cada registre aporta una contribució.
3. Desa `kernel-500-raw.tif`. Repeteix amb radi **1.500 m**, mateix píxel i una sortida diferent.

![Mapa de calor configurat amb radi 500 m i píxel 100 m]({{ site.baseurl }}/assets/captures/c4-kernel-parametres.png "El radi decideix quins punts poden contribuir a una cel·la. Els píxels X i Y controlen el detall del ràster. El tipus de kernel i el pes es revisen als paràmetres avançats."){: data-figure-width-web="38rem" data-figure-width-pdf="86%"}

### Comparar els dos radis amb les mateixes unitats

La sortida **Raw** de QGIS és una suma crua de contribucions. No s'ha d'etiquetar automàticament com registres/km². En el kernel Quartic, la conversió utilitzada multiplica aquella suma per $3\times10^6/(\pi h^2)$, amb el radi $h$ en metres. Es pot reproduir a **Ràster → Calculadora ràster**:

```text
"kernel-500-raw@1" * 3 * 1000000 / (3.141592653589793 * 500^2)
```

Per al ràster de 1.500 m es canvien el nom de banda i el radi de la fórmula. Mantén extensió, files, columnes i NoData de cada entrada. Les capes `densitat-500.tif` i `densitat-1500.tif` del paquet ja incorporen aquesta conversió i una llegenda comuna. La suma de densitats multiplicada per 0,01 km² —àrea d'un píxel— és aproximadament **124**, com el recompte original.

![Kernel de Constantí normalitzat amb els punts visibles]({{ site.baseurl }}/assets/captures/c4-kernel-resultat.png "El color representa registres/km² després de normalitzar. Cada valor pot rebre contribucions de punts pròxims, encara que no siguin dins del mateix píxel. Els punts sobre la superfície ajuden a distingir una concentració observada del seu resum suavitzat."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="ICAEN, ortofoto i límits ICGC; kernel Quartic de QGIS i normalització explícita."}

![Malla i kernels sobre els mateixos 124 punts de Constantí]({{ site.baseurl }}/assets/quarto/figures/constanti-recomptes.qmd "A l'esquerra, cada quadrat rep els punts que conté. Al centre i a la dreta, els punts contribueixen dins de radis de 500 i 1.500 m. Mateix territori, mateixes observacions i escala de color comuna: canvia la manera de resumir les concentracions."){: data-figure-width-web="49rem" data-figure-width-pdf="100%" data-caption-source="ICAEN i ortofoto ICGC 2025. Càlcul amb QGIS; elaboració pròpia."}

El kernel de 500 m conserva pics locals; el de 1.500 m els reparteix sobre àrees més àmplies. És una **descripció a una escala triada**. Una zona vermella no és per aquest fet significativa estadísticament, i una cel·la sense valor no demostra absència d'instal·lacions. El [capítol següent](../dependencia-espacial/#intuicio-autocorrelacio) conserva Constantí per estudiar una altra pregunta: si les **potències** dels punts veïns s'assemblen més del que s'obtindria en barrejar-les.

## Agregació territorial i altres variables {#potencia-antiguitat}

<span id="un-indicador-comparable-entre-seccions"></span><span id="suma-i-cobertura-per-secció-amb-qgis"></span>

Compta els punts al polígon també serveix amb seccions censals, sense una quadrícula regular. Aleshores les superfícies són diferents. Un nombre gran de registres pot reflectir una secció extensa o més consumidors: comparar exigeix triar un denominador pertinent.

<span id="afegir-lantiguitat-de-ledificació"></span><span id="llegir-una-associació-observada"></span>

El nombre d'edificis cadastrals, la seva edat o la renda poden aportar altres descripcions del territori. No són necessaris per calcular els centres i densitats puntuals explicats aquí. En agregar punts a seccions s'ha canviat la unitat d'observació; una correlació entre atributs de secció no és una relació observada dins de cada edifici o família. La [comparació de preguntes del capítol següent](../dependencia-espacial/#associacio-bivariant) desenvolupa aquesta distinció.

<span id="inventaris-complementaris-i-estats-de-projecte"></span>

Els inventaris de parcs en servei i de sol·licituds amb diferents estats tampoc amplien automàticament aquest univers d'autoconsum. Abans de reunir fonts, se'n comproven definicions, dates i identificadors. Descriure bé una distribució comença per saber què s'ha comptat.

## Activitats

### Lectura del mapa de Snow {#lectura-del-mapa-de-john-snow}

Prepara tres columnes: què es veu, quina pregunta suggereix i quina dada addicional caldria consultar. Inclou una concentració de barres, una bomba i una zona amb poques marques. Distingeix cases, defuncions i població exposada.

### Comptar i sumar sobre la mateixa malla {#recompte-i-potència-sobre-la-mateixa-graella}

Conserva una capa de 90 quadrats amb `n_punts` i `kw_pub`. Comprova les sumes **124 registres i 2.770 kW publicats**. Localitza els quadrats de 48 registres/268 kW i 17 registres/891 kW i explica per què «més punts» i «més potència» no són equivalents.

<span id="auditoria-de-lextracció"></span>

### Predir el desplaçament del centre {#predir-el-canvi-abans-de-recalcular}

En l'exemple construït de dos punts a 0 i 4 km, amb pesos 10 i 30 kW, el centre ponderat és a 3 km. Duplica tots dos pesos i després duplica només el de 30. Conserva productes, sumes i una predicció abans del càlcul. Els controls són **3 km** i **3,43 km**, respectivament.

### Centres i intervals de Constantí {#tres-centres-i-un-límit-territorial}

Reprodueix els centres amb els mateixos 124 punts, sense pes i amb `w_mid`. Desa un mapa amb nom dels centres, pesos publicats i assignats. Comprova un canvi d'uns **1.832 m**. Explica quina informació addicional seria necessària per interpretar aquell centre com una ubicació recomanada.

<span id="imputació-i-classe-oberta"></span>

### Cercle i el·lipse sobre els punts {#eix-i-sensibilitat}

Obre `03-dispersio.qgz`. Identifica el centre, una zona amb pocs punts dins dels contorns i algun punt exterior. Conserva una captura amb tot el context i explica què expressen els **2.001 m de radi** i els **1.934/510 m de semieix**, sense donar-los significat de cobertura o confiança.

### Comparació municipal {#distribucions-municipals}

Compara els radis de **323, 2.278 i 2.001 m**. Consulta les barres d'escala abans de comparar la figura del Morell, el Catllar i Constantí. El resultat serà una taula de magnituds i una lectura de la forma; la mida aparent dels panells no és el criteri de comparació.

### Radi del mapa de calor {#radi-i-ponderació-del-kernel}

Conserva els kernels de 500 i 1.500 m amb la mateixa escala de color. Comprova que utilitzen els mateixos 124 registres. Identifica una concentració que es distingeixi millor amb el radi petit i explica què aporta el gran, sense anomenar significació estadística el color més intens.
