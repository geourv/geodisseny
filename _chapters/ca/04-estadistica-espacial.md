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

Les biblioteques d'una ciutat, els arbres d'un parc o els casos d'una malaltia es poden representar amb punts. El mapa permet localitzar-los i començar a reconèixer agrupacions, zones poc ocupades o alineacions. Però, com es compara una distribució amb una altra? Dos municipis amb el mateix nombre d'equipaments poden tenir-los concentrats en un nucli o repartits entre diversos barris.

L'**estadística espacial descriptiva** expressa aquesta disposició amb mesures que tenen en compte la localització dels elements. Comptar les biblioteques informa de quantes n'hi ha; mesurar les separacions entre elles ajuda a descriure com es reparteixen pel municipi. Aquestes mesures complementen el mapa i faciliten comparar distribucions. Explicar per què les biblioteques es concentren en un barri requereix, a més, informació sobre la població, els accessos i l'organització del servei.

>>>>> En acabar el capítol, cal poder descriure una distribució puntual i justificar-ne la ponderació.
>>>>>
>>>>> - Auditar unitat, cobertura, localització i variable de ponderació d'un inventari.
>>>>> - Comparar centroide territorial, centre mitjà i centre ponderat.
>>>>> - Interpretar distància estàndard, covariància i el·lipse direccional.
>>>>> - Distingir concentració de registres, intensitat ponderada i inferència espacial.
>>>>> - Comprovar la sensibilitat a valors absents, extrems i localització.

## John Snow i el brot de còlera de 1854 {#john-snow}

El metge **John Snow** va investigar el brot de còlera de **1854** a l'entorn de **Broad Street**, al Soho de Londres. Una peça coneguda d'aquella investigació és el mapa publicat a la segona edició d'*On the Mode of Communication of Cholera*, de **1855**. Hi situa les defuncions en relació amb les cases, els carrers i les bombes públiques d'aigua {% cite snow1855cholera %}. La importància del cas rau en la relació entre aquestes observacions: situar els morts permetia preguntar-se si compartien una font d'aigua, i investigar el consum permetia contrastar aquella explicació.

![Mapa històric de John Snow amb les tretze bombes d'aigua encerclades en blau]({{ site.baseurl }}/assets/quarto/figures/john-snow-pous.qmd "Mapa del brot de còlera de 1854, publicat el 1855. Cada petita barra negra representa una defunció associada a una casa. Els cercles blaus afegits assenyalen les tretze bombes d'aigua marcades PUMP: serveixen per localitzar-les, no representen radis d'influència. La concentració de barres al voltant de Broad Street es pot comparar amb la d'altres parts del mapa."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="John Snow, mapa 1 de l'edició de 1855; litografia de C. F. Cheffins. [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Snow-cholera-map-1.jpg), [domini públic](https://creativecommons.org/publicdomain/mark/1.0/). Cercles blaus d'elaboració pròpia sobre la imatge original."}

### Unitats d'observació i concentracions

Les barres representen **defuncions**, no tots els contagis ni tota la població. Snow les associa a la casa on es va produir la mort o el cas mortal; la posició no és una observació directa del lloc on es va ingerir l'aigua. El mateix mapa combina, doncs, esdeveniments, localitzacions d'edificis, xarxa de carrers i punts d'abastament. Aquestes unitats no es poden comptar com si fossin equivalents.

>>> Si una casa tingués quatre barres i es digitalitzés com un únic punt, el camp de defuncions hauria de conservar el valor **4**. Comptar aquell punt una vegada descriuria cases afectades; ponderar-lo per quatre descriuria defuncions. Són dues preguntes diferents sobre la mateixa localització.

La concentració de barres al voltant de Broad Street era rellevant per investigar l'aigua de la bomba. Però un nombre alt de morts també s'ha de relacionar amb quantes persones vivien o treballaven a cada lloc. Un mapa de recomptes no proporciona, per si sol, una taxa de mortalitat ni el risc individual. Aquesta distinció entre numerador i població exposada serà igualment necessària en interpretar una densitat kernel o comparar inventaris territorials.

### La hipòtesi de transmissió per l'aigua {#del-patró-espacial-a-la-hipòtesi}

Snow va combinar registres de defuncions, visites i preguntes sobre **quina aigua consumien les persones**. Les excepcions aparents ajudaven a contrastar l'explicació: la institució d'acollida de Poland Street disposava de subministrament propi, i els treballadors d'una cerveseria pròxima no obtenien l'aigua de la bomba de Broad Street. També va documentar persones que vivien lluny però rebien aigua d'aquella bomba. Viure a prop i consumir-ne l'aigua no eren la mateixa dada {% cite snow1855cholera %}.

La proximitat tampoc no era només una distància recta. Snow assenyala que alguns carrers aparentment propers a la bomba de Rupert Street requerien un recorregut indirecte per arribar-hi. Això connecta el mapa de punts amb la **distància per xarxa**: un punt d'abastament pot semblar proper al mapa i ser menys accessible pels carrers.

La maneta de la bomba de Broad Street es va retirar el **8 de setembre de 1854**. El mateix Snow explica que els nous atacs ja havien disminuït abans d'aquella intervenció. Per tant, la retirada i el descens posterior no s'han d'explicar com una prova aïllada que el mapa descobrís de cop la causa i acabés immediatament amb el brot. Snow ja havia exposat la hipòtesi de transmissió el 1849; el mapa formava part d'una investigació més àmplia.

El cas també mostra els límits del registre. Snow reconeix que no va poder situar totes les persones traslladades a hospitals o fora del barri, perquè en alguns casos faltava l'adreça. La lectura crítica d'un mapa inclou preguntar **quins casos s'han pogut localitzar, quins falten i què representa una zona sense marques**. Aquesta revisió de la cobertura enllaça amb la selecció de les observacions introduïda amb el [cas dels avions als fonaments](../fonaments-geodisseny/#biaix-supervivencia).

## Distribucions puntuals: localització i atributs {#preguntes-punts}

Una **distribució puntual** reuneix les posicions d'un conjunt d'observacions dins d'un àmbit i un període definits. Pot representar esdeveniments, com defuncions, o objectes que es resumeixen amb una coordenada, com biblioteques. La coordenada permet estudiar on són; els atributs permeten precisar què es compta en cada lloc. Aquesta distinció és necessària abans de calcular un resum.

Un mapa de biblioteques pot respondre on són els equipaments, però no necessàriament on es concentra la capacitat de servei. Una biblioteca de 40 places i una de 400 poden aparèixer amb el mateix símbol. Si cada punt compta una vegada, s'estudia la distribució d'equipaments; si la seva contribució és proporcional a les places, s'estudia una distribució **ponderada** de capacitat. El **pes** és aquesta contribució: la segona biblioteca pesa deu vegades més, encara que totes dues siguin un sol equipament.

Les preguntes sobre la distribució orienten el resum que es calcula {% cite longley2015gis lefever1926ellipse %}:

::: table "Preguntes i resums d'una distribució puntual"
| Pregunta | Resum | Què permet comparar? |
| --- | --- | --- |
| On s'equilibra el conjunt? | Centre mitjà o ponderat | Posició de conjunts amb contribucions iguals o diferents |
| Quant s'estén respecte del centre? | Distància estàndard | Distribucions compactes o extenses |
| S'estén més en alguna direcció? | El·lipse direccional | Allargament i orientació del conjunt |
| On hi ha concentracions locals? | Recompte per superfície o kernel | Variacions que un únic centre no representa |
:::

>>> Quatre serveis se situen als vèrtexs d'un quadrat. El centre mitjà queda al mig, encara que no hi hagi cap servei allí. Si es dupliquen les separacions mantenint-ne el centre, augmenta la dispersió. Cap dels dos resums identifica el millor lloc per construir un equipament nou: per a això caldrien demanda, accessos i alternatives.

Una densitat relaciona una quantitat amb una superfície definida. Si s'estudien biblioteques, la quantitat pot ser el nombre d'equipaments; si s'estudia capacitat, pot ser el nombre de places. La unitat del resultat ha de conservar aquesta diferència. Centre, el·lipse i densitat són lectures complementàries i es contrasten amb els punts originals.

## Centres espacials {#centres}

El **centre mitjà** dels punts és la mitjana de les coordenades: cada registre contribueix igualment. El **centre ponderat** dona més contribució als registres amb més pes. En un inventari d'equipaments, el pes podria ser el nombre de places; en un inventari energètic, la potència coneguda. El resultat és una posició d'equilibri de la quantitat escollida.

El **centroide geomètric d'un territori** resumeix un objecte diferent: és el centre de massa del polígon assumint densitat uniforme de superfície. Depèn del límit territorial, no de les instal·lacions. Pot quedar fora d'un polígon còncau o multipartit. Un punt garantit a l'interior és útil per etiquetar, però no s'ha de presentar com a centroide.

### Centre mitjà i ponderat de quatre instal·lacions fictícies {#exemple-controlat}

En un sistema pla docent, quatre instal·lacions se situen a (0,0), (4,0), (0,4) i (4,4) km, amb potències 10, 10, 20 i 60 kW. Les coordenades i les potències són fictícies. Sense pes, les dues coordenades del centre són $(0+4+0+4)/4=2$ km: cada punt aporta una quarta part al resultat. Per ponderar, es multiplica cada coordenada per la potència corresponent.

::: table "Productes necessaris per calcular el centre ponderat fictici"
| Punt | Est, km | Nord, km | Potència, kW | Potència × est | Potència × nord |
| --- | ---: | ---: | ---: | ---: | ---: |
| P1 | 0 | 0 | 10 | 0 | 0 |
| P2 | 4 | 0 | 10 | 40 | 0 |
| P3 | 0 | 4 | 20 | 0 | 80 |
| P4 | 4 | 4 | 60 | 240 | 240 |
| Suma | 8 | 8 | 100 | 280 | 320 |
:::

Es divideixen les dues últimes sumes per 100 kW: $280/100=2,8$ km i $320/100=3,2$ km. El centre ponderat és (2,8;3,2) km. P4 el desplaça cap al quadrant superior dret perquè aporta el 60% de la potència, no perquè contingui més registres. Les unitats kW·km del numerador es divideixen pels kW del denominador i tornen a donar quilòmetres.

El càlcul es pot escriure per a qualsevol nombre de punts. Si $x_i$ i $y_i$ són les coordenades del punt $i$, $p_i$ el seu pes no negatiu i $P>0$ la suma dels pesos:

$$
\bar{x}_p=\frac{\sum_i p_i x_i}{P},\qquad P=\sum_i p_i.
\label{eq:centre-x}
$$

$$
\bar{y}_p=\frac{\sum_i p_i y_i}{P}.
\label{eq:centre-y}
$$

![Comparació dels mateixos quatre punts amb pes igual i ponderats per potència: canvien centre i el·lipse, no les localitzacions]({{ site.baseurl }}/assets/quarto/figures/centres-potencia.qmd "A l'esquerra, cada registre pesa igual; a la dreta, les àrees dels símbols són proporcionals als kW ficticis. Centre i el·lipse es calculen amb els pesos de cada panell, amb semieixos d'una desviació. La creu grisa és el centroide del mateix polígon de fons i no canvia en ponderar."){: data-figure-width-web="43rem" data-figure-width-pdf="100%"}

Ponderar per kW descriu el centre de la **capacitat registrada coneguda**. No és el centre de l'energia generada: per a això caldrien kWh d'un mateix període. Una instal·lació pot tenir molta potència i producció anual condicionada per irradiància, orientació, disponibilitat o limitacions operatives.

>> Si totes quatre potències es dupliquen, el total passa de 100 a 200 kW, però el centre ponderat no es mou: numerador i denominador es multipliquen pel mateix factor. Si només augmenta la de P4, sí que es desplaça cap a aquell punt. Aquesta és una comprovació senzilla del càlcul.

### Resums de posició i distància {#escollir-el-resum-de-posició}

No totes les eines que produeixen un punt central calculen el mateix. La mitjana respon a un equilibri de coordenades; altres centres responen a preguntes sobre distàncies.

::: table "Resums de posició i significat del punt resultant"
| Resum | Què sintetitza? | Pot coincidir amb una observació? |
| --- | --- | --- |
| Centroide d'un polígon | Distribució uniforme de la superfície | No ho exigeix |
| Centre mitjà | Mitjana de les coordenades dels punts | No ho exigeix |
| Centre mitjà ponderat | Mitjana amb contribucions desiguals | No ho exigeix |
| Mediana espacial geomètrica | Posició que minimitza la suma de distàncies euclidianes | No ho exigeix |
| Element central o medoide | Observació amb menor suma de distàncies a les altres | Sí, es tria entre les observacions |
:::

La mediana espacial geomètrica tampoc no és, en general, el punt obtingut fent per separat la mediana de $x$ i la de $y$. En aquest capítol s'utilitzen els centres mitjans, comprovables amb sumes. Comparar-los amb el centroide comarcal no estableix una distribució ideal: costa, població, activitats i disponibilitat de cobertes poden explicar posicions molt desiguals. El centroide no és per si mateix una referència de rendiment o equitat.

## Inventari ICAEN: dades i preparació {#inventari-icaen}

La pàgina de [localització d'instal·lacions](https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/) integra el visor Hipermapa. La capa d'autoconsum s'anomena `ENERGIA_INSTALAUTOCONFV`. L'ICAEN indica que el mapa representa aproximadament el **93% de les instal·lacions d'autoconsum fotovoltaic de Catalunya**: aquelles de les quals disposa de georeferenciació vàlida i coherent. És una dada de cobertura cartogràfica del conjunt català; no un percentatge de potències publicades ni una taxa d'absència específica del Tarragonès {% cite icaenLocalitzacio %}.

La coordenada correspon al consumidor elèctric associat. En autoconsum col·lectiu és la d'un dels consumidors. Per tant, el centre espacial descriu inicialment les localitzacions que publica el registre, no necessàriament el centre de les petjades físiques dels panells. Aquesta limitació pot ser assumible a escala regional i determinant en una anàlisi parcel·lària o visual.

Cal separar **registre**, **consumidor**, **instal·lació física** i **agrupació administrativa**. Les coincidències de coordenades no demostren duplicació: diversos registres poden compartir una adreça o una posició de referència. Tampoc no s'ha de suposar que un identificador cartogràfic es manté entre edicions. La deduplicació necessita una regla basada en la documentació i en els identificadors disponibles.

### Fonts i selecció territorial {#descàrrega-i-preparació-de-les-demostracions}

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

### Registres localitzats i potència publicada {#controls-demo}

En el fitxer de treball, **tots els 5.102 registres del Tarragonès tenen una posició al mapa**. Una qüestió diferent és si el camp `POT_KW` conté una xifra de potència. La taula distingeix els registres localitzats dels que publiquen aquest valor numèric.

::: table "Recomptes de control de la demostració amb l'extracció del 28 de setembre de 2026"
| Selecció per atribut | Registres amb punt | POT_KW positiu | POT_KW buit | Edifici / Terra |
| --- | ---: | ---: | ---: | --- |
| Província de Tarragona | 20.447 | 15.331 | 5.116 | 20.415 / 32 |
| Tarragonès | 5.102 | 3.762 | 1.340 | 5.096 / 6 |
:::

Els **1.340** corresponen a camps de potència buits en registres que **sí que són al mapa**. A més, tots conserven una classe a `INTERVAL`: 1.074 són de fins a 5 kW, 257 de més de 5 i fins a 25 kW, 8 de més de 25 i fins a 100 kW, i un de més de 100 kW. Es coneix, doncs, una franja de potència. Aquests registres poden intervenir en qualsevol descripció que només necessiti la posició; per ponderar per kW caldria una xifra o una regla explícita d'estimació a partir de l'interval.

>> La capa disponible és l'**univers de treball**. En la pràctica municipal es conserven tots els punts i es distingeixen la potència publicada i els pesos assignats per als escenaris. Les geometries no canvien quan es canvia la regla de ponderació.

Seleccionar només els registres amb potència numèrica i assignar pesos als que tenen un interval són decisions diferents. La primera canvia el conjunt analitzat; la segona conserva les observacions i introdueix un supòsit sobre l'atribut. Aquí es practica la segona opció mitjançant camps nous, de manera que sempre es pugui recuperar la dada publicada.

L'extracció també presenta coordenades coincidents. Al Tarragonès hi ha 528 registres addicionals respecte del nombre de posicions diferents. Aquest recompte no justifica eliminar-los: és una qüestió de qualitat que s'ha d'interpretar amb el model del registre. Es conserven tant el recompte de registres com el de localitzacions diferents.

## Anàlisi municipal: els punts de Constantí {#preparacio-punts-qgis}

A Constantí, els **124 registres** permeten observar un agrupament dens al sector oriental i un altre conjunt a l'oest, sobre grans recintes edificats. L'ortofoto ajuda a relacionar-los amb el territori. La pregunta és concreta: **el grup amb més punts també concentra més potència?** Un centre sense pesos i un centre ponderat ofereixen dues respostes comparables si es mantenen les mateixes localitzacions.

El material **Punts municipals** conté `municipis.gpkg`, amb els registres del Morell, el Catllar i Constantí, els límits i els resultats de contrast; `ortofoto.tif` i `constanti.qgz` permeten recuperar la vista. La capa `punts_base` conserva **672 registres** dels tres municipis. `punts_escenaris` afegeix els camps calculats, sense substituir `POT_KW`.

1. Obre un projecte amb **EPSG:25831**, unitats mètriques i el·lipsoide **Cap/Planimètric**. Desa les sortides pròpies en un GeoPackage de treball.
2. A **Explorador → GeoPackage → Connexió nova**, connecta `municipis.gpkg` i desplega'n les capes. Afegeix `punts_base` i filtra **CODI_MUN** pel valor **430477**. Han de quedar **124 punts**; anomena aquesta capa **Constantí**.
3. Afegeix `limits`, filtrada pel codi **430477** del camp **CODIMUNI**, i l'ortofoto. També es pot obtenir la mateixa selecció a partir de `registre_icaen` del paquet comarcal, conservant tots els registres del municipi.
4. Obre la taula: **98** registres tenen `POT_KW` i **26** només un interval. Mantén tots els punts per comparar els escenaris. L'Explorador mostra fonts; el panell Capes mostra les que s'utilitzen al projecte.

El filtre de la capa de punts utilitza el codi emmagatzemat com a enter:

```sql
"CODI_MUN" = 430477
```

El del límit municipal utilitza el codi emmagatzemat com a text:

```sql
"CODIMUNI" = '430477'
```

![Punts de Constantí sobre ortofoto amb la connexió GeoPackage desplegada]({{ site.baseurl }}/assets/captures/municipals-dades.png "Els 124 registres es relacionen amb el nucli i amb altres sectors del municipi. La mateixa vista es conserva en comparar pesos; cada punt continua representant un consumidor associat."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICAEN, límits ICGC 20/01/2026 i ortofoto ICGC 2025 obtinguda per WMS a 8 m/píxel. Preparació i captura pròpies."}

### Valors representatius dels intervals {#imputacio-intervals}

Si només se sap que una potència és de més de 5 i fins a 25 kW, es pot assignar **15 kW**, el punt mitjà, per fer un càlcul docent. És una **imputació**: una regla que completa un atribut per a l'anàlisi. El punt mitjà no és una mitjana observada ni una nova dada del productor. Una altra regla seria utilitzar la mitjana de casos coneguts de la mateixa classe, però caldria justificar que representen els casos sense valor.

Es defineixen tres escenaris. Quan `POT_KW` existeix, es conserva en tots tres; només s'assigna un pes quan aquell camp és buit.

::: table "Pesos assignats als registres sense POT_KW, en kW"
| Interval publicat | Inferior: w_inf | Central: w_mid | Superior: w_sup |
| --- | ---: | ---: | ---: |
| Potència fins a 5 | 0 | 2,5 | 5 |
| Més de 5 i fins a 25 | 5 | 15 | 25 |
| Més de 25 i fins a 100 | 25 | 62,5 | 100 |
| Més de 100 | Tractament separat | Sense punt mitjà definit | Sense límit superior definit |
:::

Els valors inferiors són **llindars de sensibilitat**: el 5 d'un interval obert a 5 és un valor límit, i el zero de la primera classe no descriu una instal·lació observada de potència nul·la. Un punt amb pes zero es conserva a la capa però no contribueix al centre ponderat d'aquell escenari. Les sumes dels pesos han de ser positives.

L'interval «més de 100 kW» no permet deduir un punt mitjà o un màxim. Si també manca `POT_KW`, s'ha d'obtenir una altra dada o declarar un supòsit addicional. L'únic cas així de l'extracció és a **Torredembarra**; no afecta el Morell, el Catllar ni Constantí. En canvi, una potència publicada de 450 kW es conserva encara que pertanyi a aquesta classe.

### Camps d'escenari a QGIS

Crea una còpia de **Constantí** al fitxer de treball. A **Calculadora de camps**, crea `w_mid` com a **Decimal (double)**, amb dues xifres decimals, i aplica:

```sql
CASE
  WHEN "POT_KW" IS NOT NULL THEN "POT_KW"
  WHEN "INTERVAL" = 'Pot <= 5kW' THEN 2.5
  WHEN "INTERVAL" = '5 < Pot <= 25 kW' THEN 15
  WHEN "INTERVAL" = '25 < Pot <= 100 kW' THEN 62.5
  ELSE NULL
END
```

Repeteix-ho per a `w_inf` i `w_sup`, canviant només els tres valors assignats segons la taula. Crea també `imputat` amb `"POT_KW" IS NULL`, per distingir visualment els pesos assignats. A Constantí han de sortir **26** casos marcats i cap pes central buit: 19 de la primera classe, 6 de la segona i un de la tercera. Els 98 valors publicats es mantenen idèntics.

![Calculadora de camps amb w_mid de tipus decimal]({{ site.baseurl }}/assets/captures/municipals-camp.png "El camp decimal conserva 2,5 i 62,5. La fórmula prioritza la potència publicada i completa només els camps buits; POT_KW continua disponible per al contrast."){: data-figure-width-web="44rem" data-figure-width-pdf="95%"}

La suma central és **2.970 kW**: 2.770 publicats més 200 assignats. La inferior és 2.825 i la superior, 3.115 kW. Aquestes són quantitats d'escenari, que permeten estudiar si la interpretació canvia amb la regla.

### Coordenades mitjanes a QGIS {#procediment-estadistica}

Els centres es calculen sobre els **mateixos 124 punts de Constantí**. El primer dona una contribució igual a cada registre; el segon utilitza `w_mid`. Els altres dos camps permeten repetir la comparació sense canviar de selecció.

L'eina **Coordenades mitjanes** és a **Vectorial → Analysis Tools** —el grup d'eines d'anàlisi— i a **Anàlisi vectorial** dins de la Caixa d'eines. El seu identificador és `native:meancoordinates`. La interfície pot conservar alguns noms anglesos, encara que la sessió sigui en català {% cite qgisUserGuide %}.

::: subfigures a/b "Dos accessos a Coordenades mitjanes: el menú Vectorial i la caixa de Processament."
![Menú Vectorial desplegat fins a Coordenades mitjanes]({{ site.baseurl }}/assets/captures/punts-centres-menu.png "El menú obre l'eina des del grup Analysis Tools.")
![Caixa de Processament amb Coordenades mitjanes visible dins d'Anàlisi vectorial]({{ site.baseurl }}/assets/captures/punts-centres-caixa.png "La caixa permet localitzar la mateixa eina sense recórrer els menús."){: data-figure-width-web="40rem" data-figure-width-pdf="82%"}
:::

1. Tria la capa de **Constantí** amb els camps d'escenari. Deixa buits **Pes del camp** i **Camp ID únic**. Desa `centre_registres`.
2. Repeteix amb **w_mid** com a pes i ID buit. Desa `centre_central`.
3. Repeteix amb **w_inf** i **w_sup**, en sortides diferenciades. Cada resultat ha de contenir **un punt**.
4. Per obtenir els tres municipis alhora, utilitza la capa completa de 672 punts i **CODI_MUN** com a ID únic: en aquest cas s'obté un centre per municipi, no un centre comú.

::: subfigures a/b "Centre dels registres i centre de l'escenari central de Constantí."
![Diàleg de coordenades mitjanes amb w_mid com a pes i ID buit]({{ site.baseurl }}/assets/captures/municipals-centre.png "w_mid combina valors publicats i assignats; els 124 punts són els mateixos.")
![Punts proporcionals als pesos i centres sobre l'ortofoto de Constantí]({{ site.baseurl }}/assets/captures/municipals-resultat.png "Rombe: centre dels registres; estrella: centre central ponderat. Blau: potència publicada; taronja: pes assignat."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}
:::

El centre dels registres és **(349.051,53; 4.557.573,88) m** i el central ponderat, **(347.321,21; 4.558.177,04) m**. El canvi és d'uns **1.832 m cap a l'oest i lleugerament al nord**. Els decimals permeten contrastar càlculs, sense atribuir precisió centimètrica a les localitzacions.

### Interpretació dels punts i de la ponderació {#interpretacio-constanti}

Per entendre el desplaçament es representa la mateixa distribució dues vegades. A l'esquerra, tots els símbols tenen la mateixa mida. A la dreta, la seva **àrea és proporcional al pes central**. Les localitzacions no canvien: canvia la contribució de cada registre.

![Mateixos punts de Constantí amb contribució igual i amb àrees proporcionals al pes central sobre ortofoto]({{ site.baseurl }}/assets/quarto/figures/constanti-pesos.qmd "R resumeix el nombre de registres; P resumeix els pesos de l'escenari central. Els punts de més pes del sector occidental desplacen P cap a aquell grup. El registre A té 450 kW publicats. Els pesos assignats són taronges; els publicats, blaus. El centre R pot quedar entre grups sense coincidir amb una instal·lació."){: data-figure-width-web="46rem" data-figure-width-pdf="100%" data-caption-source="ICAEN, extracció del 28/09/2026; ortofoto ICGC 2025, WMS a 8 m/píxel. Cartografia pròpia; la imatge dona context als consumidors associats."}

El grup oriental conté molts registres petits; al sector occidental, diversos pesos publicats elevats tenen més influència. El registre A aporta **450 dels 2.970 kW de l'escenari**, un 15,2%; els cinc pesos més grans representen el **37,4%**. Els 200 kW assignats només en representen el 6,7%. Això explica per què el centre de capacitat no coincideix amb el del recompte. No cal interpretar el punt central com una ubicació recomanada: és un resum del repartiment de contribucions.

### Sensibilitat a la regla d'imputació {#sensibilitat-imputacio}

Els tres escenaris responen si el desplaçament observat depèn molt de triar el punt mitjà. A Constantí, les distàncies al centre sense pes són **1.934 m**, **1.832 m** i **1.740 m**. Els centres inferior i superior se separen **194 m**, força menys que el desplaçament respecte del recompte. En aquestes tres proves es manté la lectura de més contribució al sector occidental.

![Comparació de les sumes de potència i dels desplaçaments dels centres en els tres escenaris]({{ site.baseurl }}/assets/quarto/figures/punts-escenaris.qmd "La suma pot variar sense moure gaire el centre, com al Morell i al Catllar. A Constantí es manté un desplaçament important en els tres escenaris. Inferior i superior es refereixen als pesos assignats: no són els extrems possibles de la posició ni un interval de confiança."){: data-figure-width-web="46rem" data-figure-width-pdf="100%" data-caption-source="ICAEN; valors publicats conservats i imputació explícita dels intervals. Elaboració pròpia."}

Assignar alhora tots els límits baixos o tots els alts és una prova de sensibilitat, no una exploració de totes les combinacions possibles. El centre és un quocient de sumes ponderades: una suma superior no obliga que cada coordenada del centre també sigui superior. La conclusió ha de conservar què és estable en els escenaris provats i què canvia.

## Dispersió i orientació {#dispersio-ellipse}

Dos conjunts poden tenir el mateix centre i extensions molt diferents. Per descriure aquesta separació es mesuren les distàncies dels punts al centre. En l'exemple sense pesos, els quatre punts són a $\sqrt{2^2+2^2}=\sqrt{8}\simeq2,83$ km. Un cercle de radi 2,83 km les resumeix perquè, en aquest cas simètric, totes són iguals.

La **distància estàndard** generalitza el càlcul: fa la mitjana dels quadrats de les distàncies i n'obté l'arrel. Si cada punt té una contribució diferent, aquesta mitjana es pondera. Amb $d_i$ com a distància plana al centre ponderat, els pesos $p_i$ i la suma $P$:

$$
D_p=\sqrt{\frac{\sum_i p_i d_i^2}{P}}.
\label{eq:distancia-estandard}
$$

El resultat conserva unitats de longitud. Un cercle amb aquest radi resumeix la separació respecte del centre de la mateixa manera en totes les direccions: és un resum **isòtrop**. Si els punts formen una banda, convé representar també quant s'estenen al llarg de la banda i perpendicularment. L'el·lipse direccional utilitza per fer-ho la variància de les coordenades i la covariància entre elles {% cite lefever1926ellipse %}.

Amb els pesos de les quatre instal·lacions, el centre canvia i cada distància contribueix en proporció a la potència: el resultat és $\sqrt{5,92}\simeq2,43$ km. No s'han desplaçat les instal·lacions; s'ha canviat quina distribució es resumeix. Sense ponderació, tots els pesos valen 1 i $P$ és el nombre de punts.

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

### Covariància, eixos i orientació {#entendre-la-forma-abans-dinterpretar-langle}

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

### Cercle i el·lipse de Constantí {#cercle-i-ellipse-de-linventari-icaen}

Amb contribució igual dels **124 punts de Constantí**, la distància estàndard és **2.000,66 m**. L'el·lipse amb $k=1$ té semieixos de **1.934,44 i 510,47 m**. L'eix llarg és gairebé quatre vegades el curt: resumeix l'allargament entre els grups de punts del sector occidental i del nucli oriental. El cercle i l'el·lipse comparteixen centre, però el cercle no expressa aquesta diferència entre direccions.

Per dibuixar-los a QGIS, es parteix del punt de coordenades mitjanes. La seva taula pot incorporar el radi `D_m`, els semieixos `a_m` i `b_m` i l'orientació `azimut`. El radi és l'arrel de $S_{xx}+S_{yy}$. Si es defineix $\Delta=\sqrt{(S_{xx}-S_{yy})^2+4S_{xy}^2}$, els semieixos són les arrels de $(S_{xx}+S_{yy}+\Delta)/2$ i $(S_{xx}+S_{yy}-\Delta)/2$. Així es poden repetir les operacions amb la Calculadora de camps o un full de càlcul.

La capa `dispersio` de `municipis.gpkg` permet comprovar els atributs. Per obtenir-los, es copia `centre_registres` al fitxer de treball i es creen camps decimals. La capa **Constantí** ha de conservar el filtre municipal i els 124 punts. Per exemple, `Sxx` utilitza la mitjana de les desviacions est–oest al quadrat:

```text
with_variable('cx', x($geometry),
  aggregate('Constantí', 'mean',
    (x($geometry) - @cx)^2))
```

`cx` conserva la coordenada del centre; dins d'`aggregate`, la geometria correspon a cada punt de **Constantí**. Per a `Syy` es fa l'operació equivalent amb la coordenada nord. `Sxy` utilitza la mitjana dels productes de les dues desviacions. El nom de capa és part de l'expressió: llegir una capa comarcal sense filtrar produiria un altre càlcul.

::: table "Paràmetres de dispersió dels 124 punts de Constantí, sense ponderar"
| Camp | Valor | Significat |
| --- | ---: | --- |
| `Sxx` | 3326162,490825 | Variància est–oest, en m² |
| `Syy` | 676463,642354 | Variància nord–sud, en m² |
| `Sxy` | −1129131,018222 | Covariància, en m² |
| `D_m` | 2000,656426 | Radi del cercle en metres |
| `a_m` | 1934,437738 | Semieix llarg en metres |
| `b_m` | 510,467208 | Semieix curt en metres |
| `azimut` | 110,220000 | Orientació axial horària des del nord, expressada entre 0° i 180° |
:::

**Geometria segons l'expressió**, identificada com `native:geometrybyexpression`, crea els polígons a partir del centre i dels seus atributs:

1. Tria **Centre i dispersió de Constantí** com a entrada i **Polígon** com a tipus de sortida. Deixa desactivades les dimensions Z i M.
2. Aplica `make_circle($geometry, "D_m", 72)` i desa la capa `cercle` a `treball.gpkg`.
3. Repeteix amb `make_ellipse($geometry, "a_m", "b_m", "azimut", 72)` i desa `ellipse`.
4. Superposa les dues capes als 124 punts, sense emplenament: cercle discontinu i el·lipse contínua. Comprova que comparteixin el centre dels registres i que l'eix llarg segueixi la direcció indicada.

El darrer nombre de les expressions controla el detall de les corbes. Les magnituds ja s'han calculat a partir dels punts: l'eina no pot estimar la dispersió d'un inventari si només rep un centre sense aquests atributs.

Les expressions fan explícit **quin resum s'està dibuixant**: radi igual a la distància estàndard i semieixos iguals a les arrels dels autovalors. Un cercle mínim que envoltés tots els punts respondria una altra pregunta. Escriure l'expressió facilita comprovar aquesta convenció i repetir-la en un altre conjunt; la interpretació depèn després de comparar el contorn amb els punts i amb el territori.

![Geometria per expressió amb els semieixos i l'azimut de Constantí]({{ site.baseurl }}/assets/captures/municipals-ellipse.png "L'expressió dibuixa l'el·lipse a partir dels atributs calculats sobre Constantí. El resultat es compara amb els punts i amb els altres municipis."){: data-figure-width-web="44rem" data-figure-width-pdf="95%"}

>> Un resum direccional facilita comparar conjunts. Per explicar per què els punts s'alineen caldrien dades sobre consumidors, activitats, cobertes i altres processos. L'angle, per si sol, no identifica la causa.

### Comparació entre municipis {#comparacio-municipis}

Un únic resum comarcal combina nuclis i grups de punts molt separats. La comparació municipal permet veure diferències que aquell resum superposa. La figura agrupa els registres pel **codi municipal publicat per l'ICAEN** i utilitza tots els punts de cada grup, amb contribució igual: no s'hi aplica el filtre de potència. Els tres panells comparteixen escala, de manera que els radis es poden comparar directament.

![Distribucions del Morell, el Catllar i Constantí amb els centres, cercles i el·lipses a la mateixa escala]({{ site.baseurl }}/assets/quarto/figures/punts-municipis.qmd "Al Morell els punts formen un conjunt compacte; al Catllar estan repartits en grups més separats. Constantí presenta un allargament que el cercle, tot sol, no descriu. D és la distància estàndard, en km. Cada panell està centrat en el seu conjunt i manté la mateixa escala; els límits municipals donen context."){: data-figure-width-web="54rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICAEN, extracció del 28/09/2026, i límits ICGC del 20/01/2026. Resums sense ponderar, semieixos k=1; elaboració pròpia."}

La distància estàndard és **323 m al Morell**, **2.278 m al Catllar** i **2.001 m a Constantí**. Aquests valors quantifiquen l'extensió dels registres respecte del seu centre. No són percentatges d'adopció de l'autoconsum: per comparar aquesta qüestió caldrien denominadors com el nombre de consumidors o d'edificis pertinents. El contorn municipal ajuda també a veure que els conjunts ocupen territoris de forma i mida diferents.

Una segona comparació examina els pesos centrals dins de cada municipi. Es conserven **totes les observacions** i s'aplica la mateixa regla d'imputació als camps buits. La distància entre el centre sense pes i el central ponderat resumeix el canvi de posició d'equilibri.

::: table "Comparació municipal amb la mateixa regla central d'imputació"
| Municipi | Registres | Suma de l'escenari, kW | Distància entre centres, m |
| --- | ---: | ---: | ---: |
| El Morell | 111 | 771 | 22 |
| El Catllar | 437 | 2.338,5 | 56 |
| Constantí | 124 | 2.970 | 1.832 |
:::

Al Morell i al Catllar, els dos centres són pròxims malgrat la diferència de dispersió entre els municipis. A Constantí, la distribució de pesos s'equilibra en una posició força diferent del recompte. Són dues propietats que no s'han de confondre: **estar més escampat** i **tenir els pesos més grans desplaçats respecte del conjunt**.

A QGIS, **Coordenades mitjanes** amb `punts_escenaris` com a entrada i **CODI_MUN** com a **Camp ID únic** produeix tres centres. Es deixa buit el pes per al recompte i es tria **w_mid** per a l'escenari central. Amb el registre comarcal complet s'obtindrien 22 grups, però la imputació exigiria resoldre abans el cas obert de Torredembarra. Per a cercle i el·lipse, cada agregació ha de llegir la capa municipal filtrada.

### El resum comarcal com a referència

El centre comarcal condensa distribucions municipals diferents i serveix com a referència de conjunt. Amb la selecció dels 3.762 registres que publiquen potència, el centre sense pes és (357.387,97; 4.556.891,17) m i el ponderat per `POT_KW`, (354.528,52; 4.556.391,87) m: es desplaça uns 2.903 m cap a l'oest. Canviar primer dels 5.102 punts al subconjunt conegut desplaça el centre 244 m. No és el mateix efecte que ponderar.

En aquella selecció, Constantí aporta el 2,60% dels registres i el 7,56% dels kW; el Catllar, el 8,67% i el 4,81%. Aquestes contribucions ajuden a interpretar el resum regional després d'haver llegit els casos locals. El cercle comarcal té radi 8.698,20 m i l'el·lipse semieixos de 8.152,14 i 3.033,37 m. Les capes del paquet comarcal conserven aquests controls, amb una selecció diferent de la pràctica municipal imputada.

## Recomptes, densitat i patrons puntuals {#densitat}

El centre resumeix tot l'inventari amb un punt. Per veure diferències locals, una primera opció és comptar registres en àrees comparables. Una quadrícula d'1 km de costat conté quadrats d'1 km²: si un quadrat inclou 8 registres, el recompte és 8 i la densitat, 8 registres/km². En un quadrat de 500 m de costat, els mateixos 8 registres equivaldrien a $8/0,25=32$ registres/km². El nombre i la densitat només coincideixen numèricament quan l'àrea és una unitat.

### Graella i recompte amb QGIS

Per estudiar **concentracions locals dins d'un àmbit ampli**, aquesta ampliació recupera el paquet comarcal **Punts del Tarragonès**. Utilitza la capa **ICAEN coneguda**, els 3.762 registres amb `POT_KW` numèric, per comparar recompte i potència sobre la mateixa selecció. La graella i el kernel mantenen la variació local que un únic centre comarcal resumiria en un punt.

1. Cerca **Crea una malla**, l'eina `native:creategrid`, a la Caixa d'eines. Tria **Rectangle (Polígon)**, espaiats horitzontal i vertical de **1.000 m**, superposicions **0** i CRS **EPSG:25831**.
2. Fixa l'extensió `340000,374000,4546000,4566000`: mínim i màxim est, seguits del mínim i màxim nord. Desa `graella` a `treball.gpkg`. Han de sortir **680 quadrats**; l'àrea plana de cadascun és 1.000.000 m².
3. Obre **Compta els punts al polígon**, l'eina `native:countpointsinpolygon`. Tria la graella com a polígons i **ICAEN coneguda** com a punts. Deixa buits pes i classe; anomena `n_punts` el camp i desa `recompte`.
4. Comprova que la suma de `n_punts` sigui **3.762**. Repeteix sobre la mateixa graella amb **POT_KW** com a pes i `kw_coneguts` com a camp: ara la suma ha de ser **36.633 kW**.

::: subfigures a/b "La graella fixa les unitats d'agregació; el recompte assigna una contribució a cada punt."
![Crea una malla amb espaiats horitzontal i vertical de mil metres]({{ site.baseurl }}/assets/captures/punts-graella-parametres.png "Espaiats iguals i superposició nul·la produeixen quadrats d'un quilòmetre quadrat.")
![Diàleg de recompte amb la graella, els punts coneguts i el pes buit]({{ site.baseurl }}/assets/captures/punts-recompte-parametres.png "Amb el pes buit, n_punts compta registres; amb POT_KW, la sortida suma potències."){: data-figure-width-web="44rem" data-figure-width-pdf="95%"}
:::

La suma comprova que cada registre ha quedat assignat una vegada. Si es retallen els quadrats per la costa, les àrees deixen de ser iguals: cal dividir pel nou valor d'àrea per expressar densitat per superfície terrestre. Un zero significa que no hi ha registres de la selecció dins del quadrat; no demostra absència de qualsevol instal·lació solar.

![Mapa graduat del recompte de registres sobre la graella]({{ site.baseurl }}/assets/captures/punts-recompte-resultat.png "Cada quadrat conserva la mateixa superfície. El color representa registres de la selecció per km²; les cel·les s'estenen més enllà del límit comarcal per cobrir tots els punts."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICAEN i ICGC; agregació i captura pròpies."}

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

L'eina **Mapa de calor (KDE, estimació de densitat de nuclis)** reparteix la contribució dels punts entre cel·les veïnes. El seu identificador a Processament és:

```text
qgis:heatmapkerneldensityestimation
```

El procediment es fa des de la Caixa d'eines de **QGIS**. Radi, píxel, kernel i pes es trien al diàleg; la normalització es completa amb la Calculadora ràster.

1. Tria **ICAEN coneguda**, radi **1.500 m** i mida de píxel X i Y de **100 m**.
2. Desplega **Advanced Parameters**. Tria kernel **Quartic** i sortida **Raw**; deixa buits els camps de radi variable i de pes. Desa `kernel-punts-1500-raw.tif`.
3. Repeteix amb radi **500 m** i el mateix píxel. Conserva una sortida diferent per no perdre la comparació.
4. Normalitza cada resultat amb el factor que li correspon abans d'aplicar una escala de colors comuna. Una segona parella, amb **POT_KW** com a pes, permet estudiar capacitat coneguda; les unitats seran diferents.

![Diàleg de mapa de calor amb radi 1500 m i píxel 100 m]({{ site.baseurl }}/assets/captures/punts-kernel-parametres.png "El radi determina l'entorn d'influència; la mida de píxel fixa la graella de sortida. El grup Advanced Parameters dona accés al kernel, al pes i al tipus de valor."){: data-figure-width-web="44rem" data-figure-width-pdf="95%"}

En aquest kernel, la contribució crua a distància $d<h$ és $(1-(d/h)^2)^2$ i fora del radi és zero. El volum sota cada contribució és $\pi h^2/3$. Per obtenir punts/km², la Calculadora ràster multiplica la sortida crua per $3\times10^6/(\pi h^2)$, amb $h$ en metres. Amb 1.500 m, el factor és aproximadament 0,424413; amb 500 m, 3,819719. Aquesta conversió fa comparables les unitats dels dos radis.

A **Ràster → Calculadora ràster**, selecciona la banda de la sortida crua i aplica el factor. Per al radi de 1.500 m:

```text
"kernel-punts-1500-raw@1" * 3 * 1000000 / (3.141592653589793 * 1500^2)
```

Conserva el mateix CRS, extensió i nombre de files i columnes que la capa d'entrada. La multiplicació manté els NoData: el ràster cru pot deixar sense valor cel·les que no ha visitat cap kernel. Aquest tractament no informa sobre la cobertura de l'inventari. Com a control de normalització, la suma de densitats multiplicada per **0,01 km²**, l'àrea de cada píxel, ha d'aproximar la contribució total: 3.762 registres o 36.633 kW, segons el pes.

![Densitat normalitzada representada a QGIS amb el límit comarcal]({{ site.baseurl }}/assets/captures/punts-kernel-resultat.png "Kernel de radi 1.500 m normalitzat a registres/km². La llegenda conserva l'escala comuna dels dos radis; un valor local prové de la suma de contribucions veïnes."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICAEN i ICGC; càlcul i captura propis."}

![Recompte en graella i dos mapes kernel amb radis de 500 i 1500 m]({{ site.baseurl }}/assets/quarto/figures/icaen-densitat.qmd "A: cada quadrat resumeix els punts que conté. B i C: densitat quartic normalitzada a punts/km², amb radi diferent i escala de color comuna. Els tres panells utilitzen els mateixos 3.762 registres; cap color representa significació estadística."){: data-figure-width-web="49rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICAEN i ICGC. Càlcul QGIS i normalització analítica del kernel."}

La graella mostra concentracions dins d'unitats fixes; el radi de 500 m conserva pics locals, i el de 1.500 m els uneix en àrees més àmplies. La contribució s'estén també fora del límit comarcal perquè el kernel no coneix aquella frontera. Retallar el mapa no corregeix l'absència de punts externs ni converteix la superfície en una probabilitat.

## Agregació per seccions censals: potència i antiguitat {#potencia-antiguitat}

Després dels quadrats regulars, es pot resumir l'inventari en una partició administrativa: les **seccions censals**. Cada fila de la nova taula descriu una secció sencera. La primera pregunta és quina potència coneguda s'hi concentra; una segona pregunta, opcional, compara aquest indicador amb l'antiguitat de l'edificació. Agregar vol dir reunir les contribucions dels objectes que pertanyen a cada àrea.

La demostració combina les [seccions censals de l'ICGC i l'Idescat](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Seccions-censals), edició 1 de gener de 2024, amb l'inventari ICAEN ja descrit i els [edificis INSPIRE del Cadastre](https://www.catastro.hacienda.gob.es/INSPIRE/Buildings/43/ES.SDGC.BU.atom_43.xml), feed de 21 d'agost de 2026 {% cite icgc2024seccions cadastre2026buildings %}. Per centrar l'exercici en l'agregació de punts, `seccions` ja incorpora el nombre d'edificis funcionals i els resums d'antiguitat de la preparació cadastral. La procedència i els codis municipals verificats es conserven al paquet; els codis del servei cadastral no s'han de confondre amb els de l'INE.

### Un indicador comparable entre seccions

Els punts ICAEN s'assignen per posició als polígons de secció. Aquesta ampliació conserva **POT_KW publicat**, sense incorporar els pesos imputats del cas municipal. S'utilitzen els registres de categoria `Edifici`: 5.096 consumidors, 3.757 amb potència positiva coneguda, que sumen 36.058 kW. No s'està atribuint cada consumidor a un edifici cadastral concret. Les sis observacions sobre terra queden fora d'aquest indicador.

Per reduir l'efecte del nombre d'edificis de cada secció, es defineix:

$$
q_s=100\,\frac{\sum_{i\in s,\,p_i\text{ coneguda}}p_i}{B_s}.
\label{eq:potencia-seccio}
$$

$p_i$ és la potència registrada coneguda, en kW, i $B_s$ el nombre d'objectes cadastrals `Building` en estat funcional assignats a la secció $s$. L'assignació d'aquests polígons utilitza un punt interior, amb control de casos sense correspondència. S'obtenen 38.689 objectes funcionals al conjunt. **Un edifici cadastral no és un habitatge**: aquest denominador no mesura llars ni persones i pot combinar usos diferents. Tampoc corregeix l'absència de potència en part de l'inventari; $q_s$ és una suma coneguda normalitzada, no la capacitat total real.

>>> Una secció fictícia amb 800 kW coneguts i 200 edificis té $100\times800/200=400$ kW per 100 edificis. Una altra amb 800 kW i 400 edificis té 200 kW per 100 edificis. La suma de potència és igual, però la relació amb el nombre d'edificis és diferent. «Per 100» és una escala de presentació, no una selecció de cent edificis.

### Suma i cobertura per secció amb QGIS

1. Afegeix `seccions`, amb **151 polígons**, i una còpia de `registre_icaen`. Filtra aquesta última amb `"UBICACIO" = 'Edifici'`: han de quedar **5.096** punts.
2. Amb **Compta els punts al polígon**, compta'ls per secció, sense pes, al camp `n_reg`.
3. Afegeix `AND "POT_KW" > 0` al filtre. Han de quedar **3.757** punts. Repeteix el recompte al camp `n_coneguts`, utilitzant com a polígons la sortida anterior per conservar els camps.
4. Repeteix sobre aquella sortida, ara amb **POT_KW** com a pes i `kw_coneguts` com a camp. La suma ha de ser **36.058 kW**.
5. A la Calculadora de camps, crea `kw_100ed` com a decimal i aplica l'expressió següent. `functional_n` és el nombre d'edificis funcionals ja incorporat a cada secció.

```sql
CASE
  WHEN "functional_n" > 0
    AND ("n_reg" = 0 OR "n_coneguts" > 0)
  THEN 100.0 * "kw_coneguts" / "functional_n"
END
```

La condició diferencia dues situacions: cap registre dona suma coneguda zero; registres amb totes les potències absents donen **NULL**, perquè no es coneix cap contribució. L'indicador tampoc es calcula sense un denominador positiu. En aquesta selecció, **una secció queda sense indicador**. Representar-la com zero canviaria el significat de les dades.

::: subfigures a/b "Agregació de potència i indicador per secció censal."
![Diàleg de suma de potència dels punts Edifici sobre les seccions]({{ site.baseurl }}/assets/captures/punts-seccions-parametres.png "POT_KW transforma el recompte en suma de capacitat coneguda.")
![Indicador de potència per cent edificis a les seccions del Tarragonès]({{ site.baseurl }}/assets/captures/punts-seccions-resultat.png "La divisió pel nombre d'edificis produeix kW coneguts per 100 edificis funcionals; l'absència d'indicador té una classe pròpia."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}
:::

### Afegir l'antiguitat de l'edificació

L'antiguitat és una segona variable, no un requisit per estudiar espacialment la primera. Aquí es calcula respecte de 2026 i es resumeix amb la mediana. El Cadastre pot donar un any inicial i un de final, corresponents a les unitats constructives més antiga i més moderna. Per obtenir una edat única es retenen els 31.302 objectes funcionals amb tots dos anys iguals. Els 7.368 amb anys diferents i els 19 sense data vàlida no entren en aquesta mediana; els dos anys no formen un interval de confiança.

![Mapes de potència registrada per cent edificis funcionals i d'antiguitat mediana a les seccions del Tarragonès]({{ site.baseurl }}/assets/quarto/figures/seccions-tarragones.qmd "Dos atributs agregats sobre les 151 seccions de 2024. A: kW coneguts de categoria Edifici per 100 objectes cadastrals funcionals; una secció només amb potències absents queda sense indicador. B: mediana d'antiguitat dels objectes amb any inicial igual al final; es requereixen almenys deu casos. Les fonts tenen dates diferents."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Fonts: ICGC/Idescat, Cadastre i ICAEN. Agregació i cartografia pròpies; EPSG:25831. Contorns simplificats només per dibuixar."}

### Llegir una associació observada

La correlació utilitza les 126 seccions amb almenys deu edificis d'any únic i almenys una potència coneguda. Es relaciona l'antiguitat mediana amb $y_s=\log(1+q_s)$, on el logaritme és natural i $q_s$ s'expressa numèricament en les unitats definides. La transformació comprimeix els valors més elevats; afegir 1 permet representar zero, però l'escala i la constant formen part de la definició. Aquesta anàlisi respon a una pregunta transformada, no a una relació lineal directa en kW.

En aquesta mostra, $r=-0,401$ i $R^2=0,161$. La recta és aproximadament $\hat y=5,194-0,02093a$, amb $a$ en anys. Les seccions més antigues tendeixen a tenir menys potència coneguda per edifici, però hi ha molta variació que aquesta recta no resumeix. Si es correlaciona l'edat amb el logaritme de la suma de kW sense normalitzar per edificis, $r$ és −0,278: canviar el denominador modifica la pregunta i el resultat.

![Núvol d'antiguitat i potència normalitzada amb regressió, i gràfic dels residus]({{ site.baseurl }}/assets/quarto/figures/potencia-antiguitat.qmd "Associació descriptiva entre 126 seccions. La recta resumeix una tendència negativa; els residus són les diferències entre observat i ajustat. Cada punt és una secció, no un edifici."){: data-figure-width-web="49rem" data-figure-width-pdf="100%"}

La interpretació ha de considerar usos industrials i residencials, tipus d'edificació, nombre d'habitatges, renda, règim de tinença i cobertura del registre. No s'han controlat aquestes variables. Les potències absents i l'exclusió dels edificis amb anys diferents també poden alterar el patró. El [capítol d'autocorrelació](../dependencia-espacial/#cas-seccions) estudia la dependència espacial del mateix indicador; la regressió aquí no demostra que l'antiguitat causi menys autoconsum.

### Inventaris complementaris i estats de projecte

Les altres capes energètiques no amplien automàticament el mateix univers d'autoconsum. Les metadades de `ENERGIA_SOLAR_PARCS` descriuen plantes sobre terreny, connectades a xarxa i de més de 100 kW en servei abans del Decret llei 16/2019. `ENERGIA_PARCSSOLARS_MULTIPOLI`, en canvi, recull sol·licituds que han arribat a informació pública, amb un camp `ESTAT` que diferencia situacions {% cite hipermapaEnergia %}.

La selecció d'entitats que intersecten la província de Tarragona conté 13 punts del primer producte i 165 entitats del segon. Entre aquestes últimes, l'extracció examinada informa de 17 en servei, 76 autoritzades, 49 en tramitació, 17 no autoritzades, 5 desistides i una sense estat. Són recomptes de registres del paquet original, no un cens independent de plantes actuals ni conjunts que es puguin sumar sense reconciliació.

Les geometries completes dels projectes seleccionats es conserven encara que alguna part superi el límit provincial. Així no es modifica silenciosament el suport dels atributs de superfície. La relació entre fonts requereix estudiar expedients, noms, dates i geometries; un mateix projecte podria aparèixer en productes diferents. Les bateries es mantenen com una ampliació separada, perquè emmagatzematge i generació fotovoltaica no són la mateixa tecnologia.

## Activitats

### Lectura del mapa de John Snow

Observa el [mapa de Broad Street](#john-snow) i prepara una taula breu amb tres columnes: què es veu, quina hipòtesi suggereix i quina informació addicional caldria consultar. Inclou una concentració de barres, una zona amb poques marques i una bomba d'aigua. Distingeix defuncions, cases i població exposada.

Explica què canviaria si una casa amb diverses barres es representés com un sol punt sense conservar-ne el recompte. Relaciona després els casos de la institució amb aigua pròpia i de la persona que rebia aigua lluny de la bomba amb la diferència entre proximitat i consum. La conclusió ha d'identificar una observació que prové del mapa i una altra que requereix informació de la investigació.

### Pesos i desplaçament del centre {#predir-el-canvi-abans-de-recalcular}

Utilitza els punts ficticis P1=(0,0), P2=(4,0), P3=(0,4) i P4=(4,4) km, amb potències 10, 10, 20 i 60 kW. Anticipa què passarà en duplicar totes les potències, en duplicar només P4 i en eliminar P4. Recalcula els centres i compara la predicció amb el resultat. Explica el mecanisme del desplaçament, a més de donar coordenades.

>> Duplicar totes les potències conserva (2,8;3,2). Si només P4 passa de 60 a 120 kW, el total és 160 kW i el centre passa a (3,25;3,50). Si es retira P4, queden 40 kW i el centre ponderat és (1;2). Retirar una observació vàlida només per canviar el resultat no seria una decisió de neteja legítima; aquí és una prova explícita de sensibilitat.

### Auditoria de l'extracció

Cal reproduir els recomptes de la demostració o explicar les diferències d'edició. La taula conservarà cobertura, potències absents, geometries coincidents i categories. El resultat ha d'identificar almenys una decisió d'anàlisi que canviï a causa d'aquests controls.

### Centres municipals i pesos {#tres-centres-i-un-límit-territorial}

Reprodueix el centre dels 124 registres de Constantí i els tres centres ponderats per `w_inf`, `w_mid` i `w_sup`. Conserva un mapa de punts amb àrees proporcionals als pesos i indica quins són publicats i quins, assignats. Explica per què el centre es desplaça i què permet afirmar la comparació dels tres escenaris.

### Eix i sensibilitat

Reprodueix el cercle i l'el·lipse dels 124 punts de Constantí, sense pes. Relaciona l'allargament amb els grups visibles, i identifica un espai dins del contorn amb pocs punts. Si repeteixes el càlcul amb `w_mid`, utilitza també el centre ponderat i divideix les sumes ponderades per la suma dels pesos.

### Distribucions municipals

Compara el Morell i el Catllar amb tots els punts disponibles i sense pesos. Conserva la mateixa escala als mapes i comprova les distàncies estàndard de 323 i 2.278 m. Repeteix els centres amb `w_mid`: els desplaçaments han de ser d'uns 22 i 56 m. Explica com dos municipis amb dispersions molt diferents poden tenir un canvi petit en ponderar.

### Imputació i classe oberta

En un registre sense `POT_KW`, interpreta l'interval «més de 100 kW». Explica per què no se'n pot calcular el punt mitjà. Proposa una font addicional o tres valors hipotètics superiors a 100 per estudiar sensibilitat, identificant-los com a supòsits. No presentis el valor més alt assajat com un màxim real.

### Recompte i potència sobre la mateixa graella

Compara `n_punts` i `kw_coneguts` sobre els mateixos 680 quadrats. Localitza un quadrat amb molts registres i un altre amb molta potència; comprova a la taula si coincideixen. Conserva un mapa de cada variable, les dues sumes de control i una explicació de la diferència entre recompte i capacitat.

### Radi i ponderació del kernel

Compara un KDE de registres i un de potència coneguda, amb radis de 500 i 1.500 m i píxel de 100 m. Normalitza les quatre sortides i conserva una escala de colors comuna per a cada unitat. Descriu les concentracions que s'uneixen en ampliar el radi i l'efecte dels valors absents. Cap de les superfícies és un mapa directe d'idoneïtat.
