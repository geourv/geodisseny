---
layout: manual-chapter
title: Autocorrelació espacial
description: "Potències veïnes a Constantí: comparació d'atributs, I de Moran, permutacions i aplicació a seccions censals."
lang: ca
ref: dependencia-espacial
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/dependencia-espacial/
weight: 50
part: Continguts
manual_references: true
---

Un mapa de punts pot mostrar dues concentracions i, alhora, dues distribucions molt diferents de l'atribut que representa. Un grup pot reunir moltes instal·lacions petites; un altre, menys instal·lacions però amb més potència. Comptar i descriure la dispersió no respon encara si els punts pròxims tenen valors semblants.

Per estudiar aquesta semblança es compara el valor de cada observació amb els dels seus veïns. Després es pregunta si la disposició és més marcada que la que s'obtindria en repartir els mateixos valors d'una altra manera. Aquest contrast aporta evidència sobre l'associació espacial definida, sense explicar per si sol les causes del fenomen.

>>>>> En acabar el capítol, cal poder interpretar i contrastar la semblança entre valors veïns.
>>>>>
>>>>> - Distingir concentració de localitzacions i semblança dels atributs.
>>>>> - Calcular una mitjana dels veïns amb una regla de proximitat explícita.
>>>>> - Explicar què resumeix la I de Moran i què afegeixen les permutacions.
>>>>> - Llegir els valors propis, els veïns i el resultat d'un contrast local a QGIS.
>>>>> - Traslladar el procediment de punts a polígons sense confondre les unitats.

## Les potències properes a Constantí {#intuicio-autocorrelacio}

<span id="moran-punts-constanti"></span>

El [capítol anterior](../punts-densitat/#preparacio-punts-qgis) descrivia 124 registres de Constantí. Ara s'utilitzen els **98 que publiquen una xifra de potència**, entre 2 i 450 kW. Els 26 valors absents queden fora d'aquest càlcul; no s'hi utilitzen els pesos imputats. Cada observació continua sent un consumidor associat del registre ICAEN, no la petjada física dels panells.

El mapa dona una primera pista. Al nucli hi ha molts valors petits; al polígon industrial occidental, diverses potències grans. Es trien dos registres concrets, **450 kW** i **3 kW**, etiquetats a QGIS. No són noms d'instal·lacions: són els valors que permeten recuperar les dues observacions del càlcul.

![Potències publicades de Constantí amb els registres de 450 i 3 kW i les seves connexions]({{ site.baseurl }}/assets/captures/c5-punts-dades.png "Els colors distingeixen intervals de potència dels 98 registres. Les línies connecten els punts de 450 i 3 kW amb els vuit veïns utilitzats en el càlcul. La proximitat dels cercles i la semblança dels seus colors són dues informacions diferents."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="ICAEN, extracció 28/09/2026; [ortofoto ICGC 2025](https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms), retall WMS a 8 m/píxel; límit ICGC. [Condicions ICGC](https://www.icgc.cat/condicions)."}

L'**autocorrelació espacial** estudia si els valors d'una variable s'assemblen entre llocs relacionats. «Auto» indica que es compara la mateixa variable —aquí, potència—; «espacial», que les relacions depenen del veïnatge. Un kernel intens indicava molts registres pròxims. Aquí s'examina si les **potències** d'aquells registres s'assemblen, una qüestió diferent {% cite moran1950notes %}.

## Comparar un valor amb els dels veïns {#matriu-pesos}

Per començar s'ha de concretar «a prop». En aquest cas, cada registre es compara amb els **vuit punts més propers** en distància recta, sobre EPSG:25831. Aquesta regla s'anomena **kNN**, veïns més propers, amb $k=8$. La potència d'un punt no intervé a triar-los: es trien per distància i després se'n consulten els valors.

### El registre de 450 kW i el seu entorn

Els vuit veïns del registre de 450 kW tenen **100, 100, 60, 30, 100, 20, 60 i 50 kW**. Tots es poden veure a la captura ampliada. La seva suma és 520 kW i la mitjana és **65 kW**.

![Potència del registre de 450 kW i dels seus vuit veïns sobre l'ortofoto]({{ site.baseurl }}/assets/captures/c5-punts-veins.png "Les línies identifiquen quins punts entren en la comparació. Cada veí està etiquetat amb la seva potència: les vuit xifres sumen 520 kW. El valor de 450 kW no entra a la seva pròpia mitjana veïna. La ubicació és la publicada per al consumidor associat, sense atribuir exactitud de coberta a l'ortofoto."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="ICAEN i ICGC; mateix conjunt de 98 registres, ampliat només per llegir-ne els valors."}

Per al registre de **3 kW** del nucli, els veïns tenen **4, 4, 3, 10, 3, 3, 3 i 3 kW**. Sumen 33 kW: la mitjana és **4,125 kW**. El contrast entre els dos entorns ja es pot explicar amb xifres comprensibles, abans de calcular cap índex.

::: table "Dos registres concrets i les seves mitjanes veïnes"
| Registre visible al mapa | Potència pròpia | Suma dels vuit veïns | Mitjana dels veïns |
| --- | ---: | ---: | ---: |
| Polígon industrial · 450 kW | 450 kW | 520 kW | 65 kW |
| Nucli · 3 kW | 3 kW | 33 kW | 4,125 kW |
:::

La mitjana dels **98 valors del conjunt** és **28,27 kW**. El registre industrial i la seva mitjana veïna la superen. El registre del nucli i el seu entorn hi queden per sota. «Valors semblants» no significa idèntics: es comparen magnituds respecte d'una referència comuna.

### Pesos espacials i taula de relacions

<span id="exemple-matriu"></span><span id="diagonal-normalització-i-asimetria"></span>

Fer la mitjana dels vuit veïns equival a donar-ne a cadascun **1/8 de contribució**. Aquests són els **pesos espacials**. No són els pesos de potència del centre ponderat: aquí expressen quines observacions intervenen en la comparació i quant contribueix cadascuna.

Es pot conservar aquesta regla en una taula amb una fila i una columna per registre. Una relació no utilitzada rep 0; cadascun dels vuit veïns rep 1/8. La suma de cada fila és 1. Aquesta taula és la **matriu de pesos**, habitualment $W$. La diagonal és zero perquè no es compara un punt amb ell mateix.

El resum de valors veïns rep el nom tècnic de **retard espacial** (*spatial lag*). Aquí no és cap retard de temps: és exactament la mitjana veïna que s'ha calculat, 65 o 4,125 kW. El nom es fa servir després a la documentació dels programes, però el significat continua sent aquella operació.

<span id="illes-i-qualitat-geomètrica"></span><span id="distància-empats-i-valors-absents"></span><span id="exemple-del-paper-de-w"></span>

Vuit veïns no defineix un radi constant. Al nucli dens s'arriba aviat a vuit punts; en sectors dispersos, el vincle més llarg del conjunt arriba a **2.566 m**. La regla també pot ser asimètrica: que un punt triï un altre no obliga que el segon triï el primer. A més, hi ha 94 posicions diferents per als 98 registres: els coincidents es conserven i es comproven els empats, en lloc d'eliminar observacions.

## Què resumeix la I de Moran? {#moran-global}

El mateix càlcul es repeteix per a tots els punts. Un valor propi i una mitjana veïna superiors a 28,27 contribueixen a una associació de valors alts. Quan tots dos són inferiors, contribueixen a una associació de valors baixos. Quan un és alt i l'altre baix, aporten un contrast. La **I de Moran** reuneix aquestes contribucions en un únic nombre {% cite moran1950notes %}.

### Diferències respecte de la mitjana

Es resta la mateixa mitjana general al valor propi i a la mitjana dels veïns. Així, «per sobre» es representa amb signe positiu i «per sota», amb signe negatiu. Per al punt de 450 kW les diferències són aproximadament **+421,73** i **+36,73 kW**; per al de 3 kW, **−25,27** i **−24,14 kW**.

Multiplicar les dues diferències dona una contribució positiva en tots dos casos: positiu per positiu o negatiu per negatiu. Si les diferències tinguessin signes contraris, el producte seria negatiu. Aquest mecanisme explica els signes de l'índex, sense haver de pressuposar què significa la lletra $z$.

::: table "Lectura dels signes, amb una mateixa referència de 28,27 kW"
| Valor propi | Mitjana veïna | Producte de les diferències | Contribució |
| --- | --- | --- | --- |
| Per sobre | Per sobre | Positiu | Semblança de valors alts |
| Per sota | Per sota | Positiu | Semblança de valors baixos |
| Per sobre | Per sota | Negatiu | Contrast alt–baix |
| Per sota | Per sobre | Negatiu | Contrast baix–alt |
:::

### Resultat del conjunt i fórmula general

La I de les potències publicades és **0,192**, amb vuit veïns i mitjanes per fila. Hi predominen contribucions de semblança entre veïns. No significa que un 19,2% dels punts sigui igual ni és un percentatge explicat per la proximitat. Tampoc no identifica on es concentra l'associació: per això es conserva el mapa i es torna als casos locals.

La fórmula suma els productes de diferències i els divideix per una mesura de la variació del conjunt. Si $x_i$ és la potència d'un punt i $\bar{x}$ la mitjana, la diferència $z_i=x_i-\bar{x}$ és el seu **valor centrat**, en kW: és l'operació que ja s'ha calculat amb xifres. $w_{ij}$ és el pes del veí $j$ i $S_0$, la suma de tots els pesos:

$$
I=\frac{n}{S_0}
\frac{\sum_i\sum_j w_{ij}z_i z_j}{\sum_i z_i^2}.
\label{eq:moran}
$$

Aquí hi ha $n=98$ punts i $S_0=98$, perquè cadascuna de les 98 files suma 1. Les unitats kW² es cancel·len entre numerador i denominador: I no té unitats. Una I positiva resumeix semblances, i una de negativa, contrastos, sota la regla triada. Els límits exactes depenen dels pesos: no s'ha d'assumir que sempre sigui una correlació ordinària entre −1 i 1.

## Contrastar el patró amb potències barrejades {#permutacions}

<span id="permutacions-i-comparacions-múltiples"></span><span id="un-contrast-que-es-pot-enumerar-sencer"></span>

Veure potències semblants juntes és una observació. Per valorar si el patró destaca sota una referència concreta es manté **el mateix mapa de posicions i els mateixos veïns**, i es reparteixen les 98 potències a l'atzar entre aquelles posicions. No s'afegeixen punts ni es canvia cap valor: només on s'assigna cadascun en aquesta prova.

![Potències observades i una distribució construïda barrejant els mateixos valors]({{ site.baseurl }}/assets/quarto/figures/constanti-moran.qmd "A l'esquerra hi ha les potències publicades. A la dreta, els mateixos 98 valors s'han assignat a l'atzar a les mateixes posicions: és una prova construïda, no una altra edició del registre. La mitjana i la suma no canvien; la semblança espacial sí. La I passa de 0,192 a −0,016 en aquesta barreja."){: data-figure-width-web="49rem" data-figure-width-pdf="100%" data-caption-source="ICAEN i ortofoto ICGC 2025. Permutació docent amb llavor 20261005; càlcul amb libpysal/esda i representació pròpia."}

Una sola barreja no representa totes les disposicions possibles. Es repeteix **9.999 vegades** i es calcula una I en cadascuna. L'histograma mostra amb quina freqüència apareixen els diferents valors de I quan la potència no conserva la seva associació amb el lloc original.

![Histograma de les I de 9999 permutacions i línia de la I observada]({{ site.baseurl }}/assets/quarto/figures/constanti-permutacions.qmd "Cada barra reuneix barreges que donen una I dins del mateix interval. La línia vermella situa el valor observat, 0,192. Només tres de les 9.999 barreges arriben a aquest valor o el superen: el resultat observat és poc freqüent sota aquesta referència."){: data-figure-width-web="35.5rem" data-figure-width-pdf="95%" data-caption-source="Mateixos 98 registres de Constantí i kNN8. Potències en kW, sense transformar; 9.999 permutacions, llavor 20261005. Elaboració pròpia."}

El contrast pregunta per una associació **positiva** almenys tan marcada com l'observada. Amb la correcció habitual d'una unitat, el resultat és $(3+1)/(9999+1)=0{,}0004$. Aquest **pseudo-p de permutació** és una freqüència de referència del procediment. No és la probabilitat que una explicació industrial sigui certa ni la proporció de registres erronis.

El resultat aporta evidència contra aquella assignació aleatòria dels atributs: **les potències i les posicions estan relacionades sota el veïnatge triat**. No prova interacció física entre instal·lacions, ni que una d'elles causi la potència de la veïna. Tipus de consumidor, usos del territori i estructura del registre podrien ajudar a investigar per què es produeix el patró.

>> La prova conserva les posicions. Per tant, no contrasta si «hi ha massa punts junts» respecte d'una distribució de localitzacions. Contrasta la disposició de **l'atribut potència** en aquests punts. Aquesta és la diferència respecte del recompte i el kernel del capítol anterior.

## Semblances i contrastos locals {#indicadors-locals}

El nombre global no mostra si tots els sectors contribueixen igual. **Moran local** examina cada valor propi i el seu entorn. Recuperem els dos registres: el de 450 kW té una mitjana veïna de 65 kW, tots dos per sobre de la mitjana general; el de 3 kW té una mitjana veïna de 4,125 kW, tots dos per sota. Són configuracions **alta–alta** i **baixa–baixa** {% cite anselin1995lisa %}.

### Configuració no és encara significació

La documentació abrevia les quatre configuracions com **HH, LL, HL i LH**, per *high* i *low*. Les lletres són noms de categories, no identificadors de punts: HH significa valor alt amb veïns alts. Es distingeixen també els valors alts en entorns baixos i els baixos en entorns alts.

Per destacar una observació es necessita un contrast local. En la referència conservada, el pseudo-p del registre de 450 kW és **0,0244** i el del de 3 kW, **0,0027**. Tots dos passen el llindar nominal de 0,05. Un altre registre pot tenir potència elevada i no passar-lo, perquè també intervenen els veïns i la distribució de referència.

El contrast global i els locals no són intercanviables. Als locals condicionals es conserva el valor propi i es reorganitzen els altres valors segons el procediment. Si es fan molts contrastos, augmenta l'oportunitat de destacar casos per atzar; per això un mapa nominal es considera exploratori i es contrasta amb un tractament de comparacions múltiples.

### Calcular Moran local a QGIS {#procediment-autocorrelacio}

<span id="veïnatge-i-càlcul-a-qgis"></span>

La [preparació del complement i les biblioteques](#preparacio-pysal) permet executar l'eina des de la interfície. Obre **Procés → Caixa d'eines → Hotspot Analysis → LISA** i tria **Local Moran's I**, l'eina univariant. La bivariant que apareix al costat compara dos atributs diferents.

![Grup LISA desplegat sobre les potències de Constantí]({{ site.baseurl }}/assets/captures/c5-punts-eines.png "El grup reuneix tres eines. Local Moran's I analitza una variable: la potència publicada dels punts. El mapa de fons i l'Explorador corresponen al mateix conjunt municipal."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}

1. Obre `05-moran.qgz`, o carrega **coneguda** des de `constanti.gpkg`: ha de tenir 98 punts simples, amb **POT_KW** numèric.
2. A Local Moran's I, tria **POT_KW**, **K-Nearest Neighbors** i **K = 8**. Mantén distància euclidiana i pesos binaris.
3. Activa **Row standardization**: cadascun dels vuit veïns contribueix 1/8. Deixa desactivada l'optimització de distància.
4. Estableix **9.999 permutacions**. Deixa **Two-tailed p-value** desactivat per conservar la convenció del complement.
5. Desa la sortida en un GeoPackage de treball, amb nom `moran_potencia`. Comprova 98 objectes i els atributs originals conservats.

![Diàleg de Moran local amb POT_KW i vuit veïns]({{ site.baseurl }}/assets/captures/c5-punts-parametres.png "POT_KW indica què es compara; kNN8, amb qui. La normalització marcada expressa una mitjana dels veïns. Les permutacions i la sortida es revisen a la part inferior del diàleg."){: data-figure-width-web="38rem" data-figure-width-pdf="86%"}

La sortida conté **p_value** i **q_value**. `q_value` és el quadrant, no un ajust FDR: 1=HH, 2=LH, 3=LL, 4=HL. A **Propietats → Simbologia → Categoritzat**, aquesta expressió separa els casos no destacats abans de consultar-ne el quadrant:

```sql
CASE
  WHEN "p_value" >= 0.05 THEN 'No destacada'
  WHEN "q_value" = 1 THEN 'Alta amb veins alts'
  WHEN "q_value" = 2 THEN 'Baixa amb veins alts'
  WHEN "q_value" = 3 THEN 'Baixa amb veins baixos'
  WHEN "q_value" = 4 THEN 'Alta amb veins baixos'
END
```

<span id="llegir-el-resultat-local"></span><span id="resultat-global-i-contrast-local"></span>

![Moran local sobre potències en kW amb els dos registres etiquetats]({{ site.baseurl }}/assets/captures/c5-punts-resultat.png "Vermell: potència alta amb veïns alts; blau fosc: baixa amb veïns baixos. El registre de 450 kW i el de 3 kW es poden recuperar pel seu valor. Gris significa no destacat amb el contrast nominal de 0,05, no absència demostrada de relació. Mateixes potències en kW que als càlculs anteriors."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="ICAEN i ICGC. Local Moran's I, Hotspot Analysis 4.0.0; 9.999 permutacions, sense correcció múltiple al mapa nominal."}

L'execució QGIS conservada destaca **8 alta–alta, 45 baixa–baixa, 1 alta–baixa i 3 baixa–alta**; 41 no passen el llindar nominal. El diàleg no ofereix llavor: una altra execució pot canviar algun cas prop del tall. Es conserva la taula retornada, no només la imatge. El càlcul de referència amb llavor explícita confirma els quadrants i permet aplicar Benjamini–Hochberg a 0,05; els dos registres comentats es mantenen destacats.

## Comprovar les decisions de l'anàlisi {#sensibilitat}

### Què canvia amb el veïnatge o la variable?

Una regla diferent representa un altre entorn. Amb vuit veïns els punts dispersos es connecten a distàncies més grans que els del nucli. Un radi fix de 500 m deixa sis punts sense veïns, i un d'1.000 m, tres. No s'han eliminat silenciosament per obtenir un mapa més net. La regla inclusiva que manté tots els empatats al tall també es conserva com a prova de sensibilitat.

L'exemple principal ha utilitzat **kW sense transformar** perquè el valor propi i la mitjana dels veïns es puguin llegir directament. Les potències grans tenen molta influència. Si s'analitza $\ln(1+\mathrm{kW})$, les distàncies numèriques entre valors es comprimeixen i la I amb kNN8 passa a **0,632**. Aquest resultat correspon a una variable transformada; no és un índex «més correcte» ni una justificació per substituir els kW sense explicar-ho.

### Quina conclusió és defensable?

La conclusió ha d'identificar **98 potències publicades de Constantí**, veïnatge de vuit punts, I observada i contrast amb potències permutades. S'ha observat una associació positiva i una disposició poc freqüent sota aquella referència. Per atribuir-la a causes concretes es necessitaria comprovar tipus de consumidors, usos i altres dades.

No s'ha demostrat que una zona sigui adequada per a noves instal·lacions. Tampoc que les observacions sense potència segueixin el mateix patró. Reconèixer què aporta la prova i què encara queda per investigar és part del resultat {% cite wasserstein2016pvalues %}.

## Transferència a seccions censals: renda {#renda-seccions}

<span id="preparació-de-la-capa"></span>

La mateixa pregunta es pot formular amb polígons: **les seccions de renda alta tendeixen a tenir veïnes de renda alta?** Ara cada observació és una secció censal i la variable, renda neta mitjana anual per persona, en euros. El veïnatge pot definir-se pel contacte entre les seccions, en lloc dels vuit punts més propers.

L'[Atlas de distribució de renda de les llars de l'INE](https://www.ine.es/jaxiT3/Tabla.htm?t=31223&L=0) aporta l'any **2023**, publicat el 21/10/2025. La població de referència és d'**1/1/2024**, coherent amb les seccions ICGC/Idescat d'aquella data. La unió per codi INE de deu dígits produeix **151 seccions i 151 rendes numèriques** al Tarragonès. La renda no és salari ni una observació de cada família {% cite ine2025atlas ine2025metodologia icgc2024seccions %}.

### Contactes i mitjana veïna {#renda-retard}

S'utilitza **Queen**: dues seccions són veïnes si comparteixen una vora o un vèrtex. **Rook** exigiria una vora. En normalitzar cada fila es dona el mateix pes als veïns d'una secció: si en té tres, cadascun contribueix 1/3; si en té quatre, 1/4.

La secció **07013 de Tarragona**, codi complet `4314807013`, té **23.239 €/persona**. Les seves tres veïnes tenen **24.068, 23.235 i 17.187 €/persona**. El retard —la mitjana que ja s'ha après amb punts— és **21.496,67 €/persona**. Valor propi i entorn superen la mitjana simple dels 151 indicadors, **15.220,36 €/persona**.

![Secció 07013 de Tarragona i rendes de les tres veïnes]({{ site.baseurl }}/assets/captures/c5-renda-veins.png "La secció estudiada està destacada en blau fosc. Les tres seccions en blau clar comparteixen contacte Queen; cadascuna contribueix un terç a la mitjana veïna. Els valors etiquetats es corresponen amb el càlcul de 21.496,67 €/persona."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="INE, renda 2023; ICGC/Idescat, seccions 2024. Representació amb QGIS."}

### Resultat global i lectura del mapa

La I de renda és **0,572**, i el pseudo-p positiu, **0,0001**, amb 9.999 permutacions i llavor 20261005. El patró positiu es manté amb Rook, 0,579, i amb quatre centroides més propers, 0,569. Ampliar a vuit centroides dona 0,485: l'entorn que es resumeix ha canviat. Les unitats externes a la comarca no entren en aquestes matrius.

![Mapa de renda i relació de cada secció amb la mitjana de les veïnes]({{ site.baseurl }}/assets/quarto/figures/renda-moran.qmd "Cada punt del gràfic és una secció, no una persona. Els eixos conserven euros anuals per persona. Les línies de la mitjana separen rendes pròpies i veïnes altes o baixes; els casos estan identificats pel municipi i la secció. El resultat global resumeix una continuïtat de valors que no exigeix que totes les rendes siguin iguals."){: data-figure-width-web="49rem" data-figure-width-pdf="100%" data-caption-source="[INE, ADRH 2023](https://www.ine.es/jaxiT3/Tabla.htm?t=31223&L=0), CC BY 4.0; seccions ICGC/Idescat 2024, CC BY 4.0. Elaboració pròpia."}

La secció **08012 de Tarragona** té **7.379 €/persona** i mitjana veïna de **10.228,25**; és una associació baixa–baixa destacada. La secció **01002 de Constantí** té una renda pròpia semblant, **7.744**, però una mitjana veïna menys extrema, **13.453,50**, i no passa el contrast local. El valor propi baix no basta per obtenir el mateix resultat.

::: table "Casos de renda: valor propi, entorn i contrast de referència"
| Municipi i secció | Renda pròpia | Mitjana veïna | Lectura local |
| --- | ---: | ---: | --- |
| Tarragona 07013 | 23.239 | 21.496,67 | Alta amb veïnes altes; p = 0,0049 |
| Tarragona 08012 | 7.379 | 10.228,25 | Baixa amb veïnes baixes; p = 0,0010 |
| Constantí 01002 | 7.744 | 13.453,50 | No destacada; p = 0,2527 |
:::

Les xifres són €/persona. La mitjana utilitzada per Moran dona la mateixa contribució a cada secció; no estima la renda mitjana de tots els habitants, que necessitaria el denominador poblacional. Aquest canvi d'unitat és tan important com el canvi d'eina.

### Reproducció amb QGIS

Carrega **renda.shp** del paquet d'autocorrelació per seccions. Aquesta versió del complement llegeix Queen des d'un Shapefile; conserva junts `.shp`, `.shx`, `.dbf`, `.prj` i `.cpg`. Exporta el conjunt complet i mantén-lo sense filtres, perquè geometries i atributs han de tenir els mateixos casos.

Local Moran's I utilitza **renda**, **Queen's Contiguity**, pesos binaris, normalització per files i 9.999 permutacions. L'optimització de distància i l'opció bilateral queden desactivades. Els camps de radi i KNN no decideixen els contactes quan s'ha triat Queen. El complement força Queen amb polígons; no s'atribueixen a aquell diàleg els contrastos Rook o kNN calculats separadament.

![Mapa local de renda amb les seccions de lectura identificades]({{ site.baseurl }}/assets/captures/c5-renda-resultat.png "La renda alta i baixa es compara amb la de les veïnes. Tarragona 07013 i 08012 queden destacades; Constantí 01002 no. Aquest és el mapa nominal de QGIS, sense correcció múltiple: gris no significa que la renda sigui mitjana ni que no hi hagi cap relació."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="INE i ICGC/Idescat; Hotspot Analysis 4.0.0. La taula de referència amb llavor explícita es conserva separada de l'execució del complement."}

<span id="resum-global-i-sensibilitat-del-veïnatge"></span><span id="moran-global-qgis"></span>

El complement retorna indicadors locals, sense una eina separada de Moran global. Si es necessita reproduir aquest resum global de renda, selecciona el Shapefile complet i executa el bloc a l'editor de la consola de Python de QGIS:

```python
import numpy as np
from libpysal.weights import Queen
from esda import Moran
capa = iface.activeLayer()
ruta = capa.source().split('|')[0]
assert ruta.lower().endswith('.shp')
y = np.array([f['renda'] for f in capa.getFeatures()], dtype=float)
w = Queen.from_shapefile(ruta)
assert len(y) == w.n == 151 and not w.islands
np.random.seed(20261005)
m = Moran(y, w, transformation='r', permutations=9999)
p = (1 + np.count_nonzero(m.sim >= m.I)) / 10000
print(round(m.I, 4), p)
```

Els controls són **0.5719 i 0.0001**. És una comprovació addicional amb les biblioteques que també utilitza el complement, no una exigència de programar tots els passos de la pràctica.

## Relacionar renda, edificació i autoconsum {#associacio-bivariant}

<span id="cas-seccions"></span><span id="autocorrelacio-antiguitat"></span><span id="un-exemple-numèric-de-canvi-de-denominador"></span><span id="ampliació-els-residus-de-la-regressió"></span>

Les tres fonts es poden reunir **per secció**, després de comprovar codis, dates i geometries. Però fan observacions diferents. La renda és un indicador dels habitants; l'edat és un resum d'edificis cadastrals; la potència s'agrega des de consumidors associats. Compartir un polígon no estableix una correspondència individual entre una família, un edifici i una instal·lació.

La pregunta s'ha d'escriure abans de combinar camps. «Les rendes s'assemblen entre veïnes?» utilitza una sola variable i el veïnatge. «Les seccions de renda alta tenen més autoconsum?» compara dues variables **dins de la mateixa secció**. «Les seccions de renda alta estan envoltades de seccions amb més autoconsum?» compara renda pròpia i potència **veïna**: és associació espacial bivariant. Cap resultat d'una d'aquestes preguntes respon automàticament les altres.

Hi ha, a més, una decisió sobre què significa «més autoconsum». A la secció **02001 de Constantí** es coneixen **2.577 kW**, amb **939 edificis funcionals** i **964.262,85 m² de petjada**. Dividir pel nombre produeix **274,44 kW per 100 edificis**; dividir per petjada, **2,67 kW per 1.000 m²**. El numerador és el mateix, però les dues ràtios comparen quantitats diferents. La petjada no és coberta solar disponible ni superfície construïda de totes les plantes.

La renda és de 2023, les seccions de 2024 i el feed cadastral, del 21/08/2026; la data efectiva ICAEN no s'ha verificat. Les possibles relacions són exploratòries, amb aquestes limitacions. No s'ha establert una explicació individual o causal renda–instal·lació. Els resultats d'autocorrelació de punts i renda sí que responen preguntes delimitades i contrastades; no necessiten una regressió addicional per tenir sentit.

## Altres aplicacions i límits {#altres-aplicacions}

<span id="columbus"></span><span id="hotspots-estadístics-amb-getisord-gi"></span>

El conjunt **Columbus**, de 49 barris d'Ohio de 1980, és un exemple de llibre d'Anselin: `CRIME` expressa robatoris per 1.000 llars, no el nombre brut. La I Queen de referència és aproximadament 0,500. La lectura és la mateixa que amb renda: una variable per barri, veïns definits i contrast declarat. La font bibliogràfica permet practicar amb un altre fenomen sense inventar observacions {% cite anselin1988spatial %}.

**Getis–Ord Gi*** és una alternativa local que estudia sumes de valors en un entorn que inclou la pròpia unitat. Pot destacar concentracions altes o baixes, però no distingeix els atípics alt–baix i baix–alt de la mateixa manera que Moran. Abans de comparar colors es revisa què resumeix cada estadístic i quina prova s'ha fet; el color d'un kernel, per si sol, no és aquest contrast {% cite getis1992analysis ord1995local %}.

<span id="suport-agrari"></span><span id="no-interpolar-arees"></span><span id="aportació-a-les-alternatives-territorials"></span>

També es pot preguntar si parcel·les grans tendeixen a tenir parcel·les grans com a veïnes. L'àrea pertany al polígon, no és una mesura física presa al centroide. Dividir una peça de 10 ha en dues de 5 ha canvia l'atribut sense canviar el terreny: interpolar aquells centroides com temperatures estimaria un efecte de la partició. Un grup de peces grans tampoc demostra propietat comuna o disponibilitat per a una actuació.

## Preparar QGIS i les biblioteques {#preparacio-pysal}

**Hotspot Analysis 4.0.0** fa servir `libpysal` per construir pesos i `esda` per calcular estadístics. Són biblioteques del projecte **PySAL**. No totes les instal·lacions de QGIS les incorporen: han de funcionar al Python que executa QGIS, com ja s'anuncia a la [presentació](../../../ca/) {% cite cereda2026hotspot %}.

Al [catàleg de complements](https://plugins.qgis.org/plugins/HotSpotAnalysis_v3/) el nom conserva «v3»; comprova **la versió 4.0.0** des de **Complements → Gestiona i instal·la complements**. Cerca Hotspot Analysis, instal·la'l i activa'l. El mantenidor documenta també la [instal·lació des de ZIP](https://github.com/geografiadascoisas/HotSpotAnalysis_Plugin).

### Comprovar l'entorn de QGIS {#comprovar-les-biblioteques}

Obre **Complements → Consola de Python**, o prem **Ctrl+Alt+P**, i executa:

```python
import sys
print(sys.version.split()[0], sys.prefix)
import libpysal, esda
print(libpysal.__version__, esda.__version__)
print(libpysal.__file__)
print(esda.__file__)
```

Les rutes indiquen quines biblioteques està carregant QGIS. Les versions de referència són **libpysal 4.13.0 i esda 2.7.1**, amb Python **3.11 o posterior**. Un paquet instal·lat en un altre Python de l'ordinador pot no estar disponible aquí. `ModuleNotFoundError` indica una importació absent; errors de NumPy o Numba poden reflectir incompatibilitats de versions.

Una prova petita comprova també el càlcul. Les dades següents són construïdes: dos valors baixos junts i dos d'alts al llarg d'una fila. El control és **0.5**, sense contrast de permutació perquè aquí només es prova la importació i l'estadístic.

```python
from libpysal.weights import lat2W
from esda import Moran
w = lat2W(1, 4)
resultat = Moran([1, 1, 4, 4], w, permutations=0)
print(round(resultat.I, 3))
```

### Vies d'instal·lació {#vies-dinstallació}

La [guia de QGIS](https://qgis.org/resources/installation-guide/) distingeix distribucions amb entorns diferents. Tanca QGIS després d'instal·lar paquets, torna'l a obrir i repeteix la prova d'importació. No s'ha de pressuposar que el Python d'una terminal qualsevol sigui el de QGIS.

**Windows amb OSGeo4W.** Obre l'OSGeo4W Shell de la mateixa instal·lació i comprova l'entorn. Les ordres corresponen a aquella shell:

```bat
python -c "import sys; print(sys.version, sys.prefix)"
python -m pip install --user libpysal==4.13.0 esda==2.7.1
```

La via d'usuari pressuposa que aquella instal·lació de QGIS admet els paquets d'usuari. En equips d'aula gestionats, les dependències les prepara l'administració del mateix entorn.

**macOS amb QGIS.app.** El mantenidor proposa el Python del paquet. Comprova que la ruta correspon a l'aplicació instal·lada; el nom pot ser diferent:

```bash
QGIS_PY="/Applications/QGIS.app/Contents/MacOS/bin/python3"
"$QGIS_PY" -c "import sys; print(sys.version, sys.prefix)"
"$QGIS_PY" -m pip install --user \
  libpysal==4.13.0 esda==2.7.1
```

**Linux.** Amb paquets del sistema, comprova si la distribució ofereix totes dues biblioteques per al mateix Python. Ubuntu 24.04 ofereix `python3-libpysal`, però no `python3-esda` al catàleg consultat. `externally-managed-environment` indica un Python gestionat pel sistema; no s'ha de resoldre sobreescrivint-ne indiscriminadament els paquets.

Una via per preparar QGIS i les biblioteques conjuntament en un entorn separat és [Miniforge](https://github.com/conda-forge/miniforge), amb conda-forge:

```bash
conda create -n qgis-aeg -c conda-forge --strict-channel-priority \
  "qgis=3.44" "python>=3.11,<3.14" "libpysal=4.13" "esda=2.7"
conda activate qgis-aeg
qgis
```

Obre el QGIS de l'entorn activat i instal·la-hi el complement. Crear l'entorn no modifica el QGIS que s'obre des d'una altra icona. Amb Flatpak, la guia oficial descriu una instal·lació dins del seu propi entorn. Les guies de [libpysal](https://pysal.org/libpysal/stable/installation.html) i [esda](https://pysal.org/esda/stable/installation.html) documenten pip i conda-forge. Les versions concretes han de ser compatibles amb el Python disponible.

## Activitats

### Valor propi i vuit veïns {#calcular-abans-dinterpretar-colors}

Recupera el registre de 450 kW a `05-moran.qgz` i els vuit valors de 100, 100, 60, 30, 100, 20, 60 i 50 kW. Conserva una captura amb les connexions i les xifres, suma 520 i mitjana **65 kW**. Compara amb la mitjana general **28,27 kW** i explica els signes de les dues diferències.

<span id="atributs-puntuals-i-concentració-de-registres"></span>

### Què es conserva en una permutació? {#dues-matrius-dues-preguntes}

Compara els dos mapes de potències. Escriu què s'ha mantingut —98 punts, 98 valors, suma, mitjana i veïnatge— i què s'ha canviat. Interpreta després **3 de 9.999** i el pseudo-p **0,0004**. La conclusió no ha d'atribuir una causa al resultat.

### Llegir el mapa local {#associació-global-i-local}

Conserva el valor propi, la mitjana veïna, la categoria i el pseudo-p dels registres de 450 i 3 kW. Explica per què un quadrant i passar un contrast són dues decisions diferents. Consulta també un cas gris i comprova que no es pot deduir el seu valor de potència només d'aquell color.

### Una secció i els seus contactes {#reconstruir-un-retard-de-renda}

La secció 07013 de Tarragona té 23.239 €/persona i tres veïnes de 24.068, 23.235 i 17.187. Conserva els codis, un mapa de contactes i la mitjana **21.496,67 €/persona**. Compara amb **15.220,36** i amb el pseudo-p de referència **0,0049**: distingeix quadrant i contrast.

### Canviar el denominador {#comparar-denominadors-sense-canviar-casos}

La secció 02001 de Constantí té 2.577 kW publicats, 939 edificis funcionals i 964.262,85 m² de petjada. Calcula **274,44 kW per 100 edificis** i **2,67 kW per 1.000 m²**. Explica què pregunta cadascuna de les dues ràtios i per què no mesuren ocupació efectiva dels panells.

<span id="demostrar-el-problema-de-suport"></span><span id="geometria-i-decisió"></span>

### Valor de la prova i informació que falta

Redacta una conclusió de Constantí amb unitat, variable, veïnatge, índex observat i permutacions. Separa l'associació observada d'una explicació possible sobre usos industrials o residencials. Identifica les dades addicionals que permetrien comprovar aquella explicació.
