---
layout: manual-chapter
title: Autocorrelació espacial
description: Matrius de pesos, associació global i local, inferència i sensibilitat per estudiar atributs d'unitats territorials.
lang: ca
ref: dependencia-espacial
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/dependencia-espacial/
weight: 50
part: Continguts
manual_references: true
---

Els barris veïns tenen valors semblants? Els valors alts d'una variable es concentren en determinats sectors o apareixen barrejats amb valors baixos? L'autocorrelació espacial ajuda a respondre aquestes preguntes comparant cada valor amb els del seu entorn. Cal començar amb una variable per unitat i una regla que indiqui quines unitats són veïnes.

Dos mapes poden contenir els mateixos valors i presentar disposicions molt diferents: en un, els valors alts poden estar junts; en l'altre, poden alternar-se amb els baixos. La mitjana de la variable no distingeix aquestes situacions. Per descriure-les s'han de conservar les relacions entre les unitats i comparar els valors de cada lloc amb els dels seus veïns.

>>>>> En acabar el capítol, cal poder interpretar associació espacial amb unitats, veïnatge i inferència explícits.
>>>>>
>>>>> - Definir una unitat territorial i una variable amb suport coherent.
>>>>> - Justificar una matriu de pesos i comprovar-ne les connexions.
>>>>> - Relacionar Moran global, Moran local i Getis–Ord amb preguntes diferents.
>>>>> - Interpretar permutacions, comparacions múltiples i sensibilitat.
>>>>> - Explicar per què no s'interpolen àrees parcel·làries com temperatures puntuals.

## Reconèixer semblances entre veïns {#intuicio-autocorrelacio}

En la correlació ordinària es comparen dues variables observades en els mateixos casos, com altitud i temperatura. En l'**autocorrelació espacial** es compara una variable amb els valors d'aquesta mateixa variable en llocs relacionats. El prefix «auto» remet a aquesta repetició de la variable; «espacial» indica que la relació entre casos depèn d'un veïnatge {% cite moran1950notes %}.

Pensem en quatre peces consecutives al llarg d'un camí. Si les àrees són 1, 1, 4 i 4 ha, les dues peces petites estan juntes i les dues grans també. Si són 1, 4, 1 i 4 ha, els extrems s'alternen. Els dos conjunts tenen la mateixa mitjana, 2,5 ha, i la mateixa dispersió. La diferència només es pot reconèixer després d'introduir l'ordre espacial i qui és veí de qui.

Autocorrelació positiva
: Predomini de relacions entre valors semblants, respecte de la variable i el veïnatge definits.

Autocorrelació negativa
: Predomini de contrastos entre veïns, com l'alternança de valors alts i baixos.

Associació global
: Resum únic per al conjunt de l'àmbit. Pot amagar diferències entre sectors.

Associació local
: Relació d'una unitat amb el seu entorn. Permet investigar on apareixen agrupacions o contrastos.

![Dos mapes esquemàtics amb quatre polígons en cadena doblegada: agrupació 1,1,4,4 i alternança 1,4,1,4]({{ site.baseurl }}/assets/quarto/figures/moran-patrons.qmd "Amb contactes A–B–C–D i pesos normalitzats per files, l'agrupació dona I = 0,5 i l'alternança I = −1. Les dues mitjanes són 2,5 ha. Geometria esquemàtica sense escala, no proporcional a les àrees fictícies atribuïdes; el signe encara no estableix significació."){: data-figure-width-web="41rem" data-figure-width-pdf="94%"}

La figura presenta un patró extremament petit per poder reconstruir el càlcul. En un mapa real poden coexistir zones agrupades, transicions i casos aïllats. El resum global serà útil per començar, però la lectura territorial necessitarà tornar a les unitats i als seus veïns. Tampoc s'ha d'equiparar agrupació d'atributs amb concentració de punts: aquí cada peça té un valor i una posició fixada.

## Construir el veïnatge {#matriu-pesos}

La **matriu de pesos** $W$ és una taula de relacions: una fila per unitat i una columna per unitat. El valor $w_{ij}$ indica quant contribueix la unitat $j$ a l'entorn de la unitat $i$. Un zero significa que aquella relació no entra al càlcul. Els pesos poden representar contacte, distància o altres connexions justificades {% cite moran1950notes anselin1995lisa %}.

La contigüitat **rook** exigeix compartir una vora; **queen** també admet contacte en un vèrtex. Una distància fixa relaciona centroides dins d'un radi; els $k$ veïns més propers garanteixen un nombre de relacions sortints, però poden connectar peces molt allunyades en zones disperses. L'elecció altera la pregunta i s'ha de comparar amb la geometria real.

![Dues definicions de veïnatge al voltant de la mateixa unitat sintètica]({{ site.baseurl }}/assets/quarto/figures/veinatges.qmd "La mateixa unitat té quatre veïns si s'exigeix contacte per vora i vuit si també s'admet contacte per vèrtex. Esquema sintètic per interpretar W; no és un mapa de significació."){: data-figure-width-web="38rem" data-figure-width-pdf="85%"}

### Diagonal, normalització i asimetria

En molts càlculs de Moran es fixa $w_{ii}=0$ per evitar que una unitat sigui veïna d'ella mateixa. La Gi* incorpora la pròpia unitat segons la seva definició. Reutilitzar sense revisar una matriu amb la diagonal equivocada pot canviar l'estadístic que es creu estar calculant.

La normalització per files divideix cada pes per la suma de la seva fila. El **retard espacial** passa a ser una mitjana ponderada dels veïns quan la fila té suma positiva. Una matriu binària de contacte pot ser simètrica i deixar de ser-ho numèricament després de normalitzar si les unitats tenen nombres de veïns diferents.

### Matriu de pesos d'una cadena de quatre àrees {#exemple-matriu}

En la cadena A–B–C–D, A només té B com a veí i D només té C. B té A i C; C té B i D. Amb pesos binaris, cada relació valdria 1. En normalitzar per files, els dos veïns d'una peça interior reben 1/2 cadascun, mentre que el veí únic d'un extrem rep 1. La taula representa exactament aquesta regla.

::: table "Matriu W de la cadena fictícia, normalitzada per files"
| Unitat de la fila | A | B | C | D | Suma |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 0 | 1 | 0 | 0 | 1 |
| B | 0,5 | 0 | 0,5 | 0 | 1 |
| C | 0 | 0,5 | 0 | 0,5 | 1 |
| D | 0 | 0 | 1 | 0 | 1 |
:::

Llegir la fila B vol dir «la meitat del valor d'A més la meitat del de C». Si els valors són 1, 1, 4 i 4 ha, el retard espacial de B és $0,5\times1+0,5\times4=2,5$ ha. El d'A és 1 ha perquè el seu únic veí és B. «Retard» és el terme estadístic: aquí no significa cap retard temporal, sinó un resum dels valors a les unitats relacionades.

>> La fila indica **de qui rep informació** cada unitat. Comprovar que les files sumin 1 ajuda a verificar aquesta normalització, però no demostra que els veïns siguin territorialment adequats. Una matriu pot estar ben calculada i representar una relació poc pertinent.

Els $k$ veïns també poden generar relacions asimètriques: que A tingui B entre els seus més propers no implica la relació inversa. Cal decidir si es conserva aquesta direcció o se simetritza amb una regla explícita. La simetrització modifica el nombre de relacions i no és una operació neutra.

### Illes i qualitat geomètrica

Una unitat sense veïns pot reflectir una illa real, un polígon separat o un error de geometria. No s'ha d'eliminar ni connectar automàticament per fer desaparèixer un avís. Cal documentar el seu tractament i saber com l'eina l'incorpora als denominadors i a la inferència.

La matriu ha de tenir una clau estable que relacioni files amb observacions. Si s'ordena la taula o se'n retira un registre sense reconstruir la correspondència, els pesos poden acabar relacionant valors equivocats. Comprovacions útils són nombres de veïns, distàncies màximes, components connectats, diagonal i una inspecció de casos coneguts.

## Autocorrelació global {#moran-global}

La I de Moran relaciona desviacions respecte de la mitjana amb les dels veïns. Si $z_i=x_i-\bar{x}$ i $S_0=\sum_i\sum_jw_{ij}$:

$$
I=\frac{n}{S_0}\,\frac{\sum_i\sum_jw_{ij}z_i z_j}{\sum_i z_i^2}.
\label{eq:moran}
$$

Els productes són positius quan valors alts estan relacionats amb alts o baixos amb baixos, i negatius quan es relacionen desviacions de signe contrari. L'estadístic requereix variació en la variable i una matriu vàlida. Els seus límits depenen de $W$; no convé interpretar-lo com una correlació ordinària sempre acotada exactament entre −1 i 1.

Sota una referència habitual de permutació amb diagonal nul·la, l'esperança és $-1/(n-1)$, no exactament zero. El contrast compara el valor observat amb una distribució de referència adequada. Un resultat significatiu no identifica la causa de l'estructura, i un resultat global poc marcat no descarta configuracions locals diferents que es compensin.

### Exemple del paper de W

Quatre peces en cadena tenen valors 1, 1, 4 i 4. Si cada peça es relaciona amb les adjacents de la cadena i els pesos es normalitzen per files, la I és 0,5. Si totes es relacionen igualment amb totes les altres, la I és −1/3. En aquest últim cas la relació completa imposa un valor degenerat que no distingeix la configuració espacial: no és un contrast útil del patró.

El primer resultat es pot reconstruir sense programari estadístic. La mitjana és 2,5, de manera que els valors centrats $z$ són −1,5, −1,5, +1,5 i +1,5. Aplicar la matriu als valors centrats dona −1,5, 0, 0 i +1,5. Es multiplica després el valor centrat de cada unitat pel seu retard centrat.

::: table "Reconstrucció de Moran global en la cadena 1, 1, 4, 4"
| Unitat | Valor x, ha | Valor centrat z | Retard de z | Producte z × retard | z² |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 1 | −1,5 | −1,5 | 2,25 | 2,25 |
| B | 1 | −1,5 | 0 | 0 | 2,25 |
| C | 4 | 1,5 | 0 | 0 | 2,25 |
| D | 4 | 1,5 | 1,5 | 2,25 | 2,25 |
| Suma | 10 | 0 | 0 | 4,5 | 9 |
:::

Hi ha $n=4$ unitats i $S_0=4$ perquè cadascuna de les quatre files suma 1. Per tant, $I=(4/4)\times(4,5/9)=0,5$. En l'alternança, cada valor centrat té un retard de signe contrari i de la mateixa magnitud: els productes sumen −9 i $I=-1$. Les unitats d'àrea al quadrat es cancel·len entre numerador i denominador; I és adimensional.

L'exemple mostra que no s'ha modificat cap superfície, sinó la definició de relació. La sensibilitat a $W$ no és un error a ocultar, sinó part de la interpretació. Cal justificar quina matriu representa millor la pregunta i què aporta una de contrast.

La C de Geary utilitza diferències quadràtiques entre valors relacionats, amb una sensibilitat distinta a configuracions locals {% cite geary1954contiguity %}. Comparar estadístics pot enriquir la diagnosi, però no s'han de seleccionar només els que donin la resposta esperada.

## Indicadors locals i significació {#indicadors-locals}

Els indicadors locals estudien la relació d'una observació amb el seu entorn. **LISA** designa una família de mesures d'associació espacial local; la I de Moran local n'és un cas. La combinació entre signe del valor centrat, signe del retard espacial i resultat inferencial permet distingir clústers i atípics {% cite anselin1995lisa %}.

::: table "Lectura de les configuracions locals de Moran"
| Configuració | Valor de la unitat i entorn | Interpretació condicionada al contrast |
| --- | --- | --- |
| HH | Alt amb veïns relativament alts | Nucli d'associació local de valors elevats |
| LL | Baix amb veïns relativament baixos | Nucli d'associació local de valors baixos |
| HL | Alt amb entorn relativament baix | Atípic espacial alt |
| LH | Baix amb entorn relativament alt | Atípic espacial baix |
:::

Alt i baix es defineixen respecte de la mitjana del conjunt, no respecte d'un llindar territorial universal. HH combina dues desviacions positives; LL, dues de negatives. Una unitat HH no queda qualificada com a apta per a cap actuació. El mapa conserva també els casos no destacats i els no calculables.

>>> Si la mitjana del conjunt és 5 ha, una peça de 8 ha té valor centrat positiu. Amb veïns de 7, 8 i 9 ha, el retard també és positiu i la configuració és alta–alta. Amb veïns d'1, 2 i 3 ha seria alta–baixa. Encara falta el contrast per decidir si es destaca com a associació local; els quadrants no són, per si mateixos, una prova de significació.

Un mapa local es llegeix en tres passos. Primer es consulta el valor de la unitat. Després es revisa el resum dels veïns que determina el quadrant. Finalment es consulta si el resultat passa el criteri inferencial adoptat. Saltar directament al color HH o LL fa perdre el significat de la classificació i pot ocultar que un mateix resultat depèn molt del radi de veïnatge.

La Gi* de Getis–Ord estudia concentracions de valors alts o baixos en un entorn que inclou la unitat segons la convenció del mètode {% cite getis1992analysis ord1995local %}. No classifica de la mateixa manera els atípics HL i LH. Dos mapes poden diferir perquè responen preguntes diferents, encara que utilitzin una definició de proximitat semblant.

### Permutacions i comparacions múltiples

La inferència per permutacions genera una distribució de referència. En una implementació local condicional es fixa el valor de la unitat i es reorganitzen els altres valors segons el procediment. Cal conservar nombre de permutacions, llavor, sentit del contrast i tractament de pesos. Els p-valors de motors diferents no són comparables si canvia aquesta convenció.

Amb $B$ permutacions, una forma habitual de pseudo-p utilitza una correcció d'una unitat, de manera que la resolució mínima és $1/(B+1)$. Si hi ha molts contrastos, aquesta resolució pot ser insuficient per a una correcció exigent. No obtenir observacions significatives pot reflectir el disseny de la prova, no només el patró.

### Un contrast que es pot enumerar sencer

Amb dos valors 1 i dos valors 4 només hi ha sis ordres diferents sobre la cadena. Es pot calcular la I de tots mantenint fixa W. La referència d'aquest exemple considera aquests sis ordres igualment probables i pregunta, en un contrast unilateral, per valors de I tan grans com l'observat o més.

::: table "Totes les disposicions diferents del petit exemple de permutació"
| Valors en l'ordre A–B–C–D | I de Moran |
| --- | ---: |
| 1, 1, 4, 4 | 0,5 |
| 1, 4, 1, 4 | −1 |
| 1, 4, 4, 1 | −0,5 |
| 4, 1, 1, 4 | −0,5 |
| 4, 1, 4, 1 | −1 |
| 4, 4, 1, 1 | 0,5 |
:::

Dos dels sis ordres tenen I igual a 0,5 i cap la supera. La probabilitat exacta d'obtenir un valor almenys tan gran sota aquesta referència és $2/6=1/3$. Tot i la semblança visual de la primera cadena, aquest exemple no dona evidència contra la referència al nivell 0,05. Amb només quatre unitats, la distribució possible és molt grollera. Aquí s'han enumerat tots els ordres; la correcció de Montecarlo descrita abans correspon al cas en què només se'n mostreja un nombre finit.

>>>> Un p-valor petit no és la mida de l'agrupació ni la seva importància territorial. Un mapa local necessita magnituds, veïnatge i criteri de contrast; decidir on actuar exigeix, a més, objectius i coneixement del procés {% cite wasserstein2016pvalues %}.

Quan es fan molts contrastos locals, el problema canvia d'escala. Amb 100 contrastos vàlids sota hipòtesis nul·les certes i nivell 0,05, el nombre esperat de rebuigs falsos és aproximadament 5; no significa que cada mapa contingui exactament cinc errors. Les proves locals poden ser dependents. Una correcció de comparacions múltiples tracta aquest problema conjunt i s'ha d'escollir i documentar segons el procediment.

El quadern de GeoDa d'Anselin aplica Moran local a donacions per habitant dels departaments francesos del conjunt Guerry. Mostra com canvien les localitzacions destacades en variar el llindar, les permutacions i els criteris de comparacions múltiples {% cite anselin2020workbook %}. La lliçó transferible és comparar configuracions, no cercar el llindar que produeixi més colors.

## Un exemple clàssic: els barris de Columbus {#columbus}

El conjunt clàssic [**Columbus**](https://pysal.org/libpysal/generated/libpysal.examples.available.html) conté 49 barris d'Ohio l'any 1980. La variable `CRIME` resumeix robatoris en domicilis i de vehicles per 1.000 llars. No és el nombre brut d'incidències: el denominador permet comparar barris amb nombres diferents de llars. Les metadades remeten a la taula 12.1, pàgina 189, d'Anselin {% cite anselin1988spatial %}.

La figura recorre quatre lectures de les mateixes dades. Primer es representa la variable; després es dibuixen els veïns queen d'un barri. El tercer panell compara el valor de cada barri amb la mitjana dels seus veïns. Perquè tots dos eixos siguin comparables, s'ha restat la mitjana i s'ha dividit per la desviació estàndard: són **valors estandarditzats**, sense les unitats originals.

![Quatre lectures dels barris de Columbus: incidències, veïns, diagrama de Moran i associació local]({{ site.baseurl }}/assets/quarto/figures/columbus-moran.qmd "A: incidències per 1.000 llars. B: un barri i els seus veïns queen. C: valor estandarditzat i mitjana dels veïns, amb I = 0,500. D: Moran local amb pseudo-p unilateral menor de 0,05, 9.999 permutacions i sense correcció múltiple. Gris: no destacat amb aquest criteri."){: data-figure-width-web="49rem" data-figure-width-pdf="100%" data-caption-source="Dades Columbus distribuïdes amb libpysal; Anselin (1988). Coordenades digititzades en unitats arbitràries, sense escala mètrica atribuïda."}

Un punt del quadrant superior dret té un valor superior a la mitjana i veïns que, de mitjana, també la superen. Al quadrant inferior esquerre passa el contrari. Els quadrants creuats indiquen contrast: un barri alt en un entorn baix o un barri baix en un entorn alt. En aquesta normalització, la recta que passa per l'origen té pendent igual a la I de Moran.

El resum global és $I=0,5002$, amb pseudo-p 0,0001 en 9.999 permutacions i llavor 20260930. El resultat indica associació positiva sota aquest veïnatge i aquesta referència. No significa que la meitat dels barris siguin iguals ni que la proximitat expliqui causalment les incidències. El mapa local diferencia agrupacions altes, agrupacions baixes i contrastos que el nombre global no situa.

>> La seqüència de lectura és **variable → veïns → relació → contrast**. La mateixa seqüència servirà a QGIS amb una altra variable i altres polígons. El color final no substitueix les tres lectures anteriors.

## Cas real: autoconsum per seccions censals {#cas-seccions}

Ara es reprèn l'[indicador d'autoconsum per secció]({{ site.baseurl }}/ca/chapters/punts-densitat/#potencia-antiguitat): potència coneguda de categoria Edifici per 100 edificis cadastrals funcionals, anomenada $q_s$. La pregunta és si una secció amb valor elevat tendeix a tenir veïnes amb valors elevats. **Només s'utilitza aquesta variable**; no cal introduir l'antiguitat per calcular-ne l'autocorrelació.

Els valors més elevats de $q_s$ se separen molt de la majoria. Per comprimir aquella escala s'utilitza $y_s=\log(1+q_s)$, amb logaritme natural. La Calculadora de camps de QGIS crea `log_pot` amb `ln(1 + "kw_per_100_buildings")`. Per exemple, $q_s=0$ es transforma en 0 i $q_s=99$ en aproximadament 4,605. La transformació conserva l'ordre dels valors però canvia les diferències entre ells.

De les 151 seccions de 2024, una només té potències absents i queda fora del càlcul. Les altres 150 es relacionen per contigüitat queen, sobre les geometries completes, amb diagonal zero i pesos normalitzats per files. No hi ha illes en aquest subconjunt. Les seccions sense cap registre ICAEN tenen zero potència **coneguda al registre**; no s'afirma que l'autoconsum real sigui nul. Els veïns externs a la comarca no formen part de W, una decisió que condiciona la lectura de les vores.

### Resultat global i contrast local

El càlcul de referència dona $I=0,144$, amb esperança de referència $-1/149\simeq-0,0067$. Amb 9.999 permutacions i llavor 20260929, el pseudo-p retornat pel motor és 0,0024. Hi ha associació positiva sota aquesta referència, sense que això impliqui que tot el territori formi un únic clúster. Com a contrast, quatre veïns més propers entre centroides donen $I=0,149$ i pseudo-p de 0,0026.

![Diagrama de Moran i mapa dels resultats locals amb correcció de comparacions múltiples]({{ site.baseurl }}/assets/quarto/figures/moran-tarragones.qmd "A: el pendent del retard espacial sobre la variable estandarditzada correspon a I amb aquesta normalització. B: Moran local, pseudo-p de permutació d'esda i procediment Benjamini–Hochberg a 0,05 sobre 150 contrastos; només una secció queda destacada com a HH. Gris clar no significa absència demostrada de patró."){: data-figure-width-web="52rem" data-figure-width-pdf="100%" data-caption-source="Fonts i agregació: mateix conjunt ICGC/Idescat–Cadastre–ICAEN del capítol d'estadística descriptiva."}

Per al mapa local es conserva la convenció unilateral de `Moran_Local.p_sim` del motor, amb les mateixes 9.999 permutacions. El procediment Benjamini–Hochberg ordena els 150 pseudo-p i els compara amb llindars de rang $0,05k/150$. El tall obtingut és 0,0003 i queda destacada una secció HH de Vila-seca, codi `4317101013`. És un resultat exploratori condicionat a variable, matriu, implementació i tractament de les comparacions múltiples; no s'atribueix una garantia universal de control d'errors sota qualsevol dependència espacial.

La secció destacada s'ha de llegir juntament amb els seus valors, usos i cobertura. El resultat no situa una instal·lació individual ni acredita idoneïtat per ampliar-la. Igualment, una secció no destacada pot tenir una potència elevada sense una associació local prou extrema sota el contrast. Aquesta distinció explica per què el mapa de la variable i el mapa local no es poden substituir entre si.

### Moran local a QGIS {#procediment-autocorrelacio}

El complement [**Hotspot Analysis v4**](https://github.com/geografiadascoisas/HotSpotAnalysis_Plugin), versió 4.0.0, afegeix a la Caixa d'eines **Local Moran's I** (`hotspotanalysis:moranlocal`) i **Getis–Ord Gi***. La versió importa: no s'ha de donar per equivalent una eina antiga amb un nom semblant. El complement necessita `libpysal` i `esda`; l'entorn d'aquest exemple utilitza 4.13.0 i 2.7.1, respectivament.

Per a Queen, aquesta implementació llegeix un **Shapefile**. S'exporten les 150 seccions admeses amb el codi estable `cusec` i `log_pot`, conservant junts els fitxers `.shp`, `.shx`, `.dbf`, `.prj` i `.cpg`. No s'han de simplificar les geometries abans de construir els contactes.

Al diàleg de Moran local es trien la capa, `log_pot` i **Queen's Contiguity**. Es marquen pesos binaris i normalització per files, es desactiva l'optimització de distància i s'estableixen 9.999 permutacions. L'opció bilateral es deixa desmarcada per conservar la convenció unilateral d'aquesta demostració. Els camps de distància i KNN no defineixen els contactes quan s'ha seleccionat Queen.

![Diàleg Moran local amb variable log_pot i veïnatge Queen]({{ site.baseurl }}/assets/captures/moran-parametres.png "Hotspot Analysis v4: cada polígon és una secció i log_pot és la variable analitzada. Queen inclou contactes per vora o vèrtex; les files es normalitzen."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

La sortida afegeix `p_value` i `q_value`. El segon camp codifica quadrants: 1=HH, 2=LH, 3=LL i 4=HL. Per construir una classe cartogràfica es consulta primer si `p_value < 0.05`; si no, la secció queda com a no destacada. Així no es confon pertànyer a un quadrant amb superar un contrast.

![Mapa QGIS de Moran local amb grups alts i baixos i atípics espacials]({{ site.baseurl }}/assets/captures/moran-resultat.png "Moran local amb llindar nominal de 0,05, sense correcció múltiple. Aquest mapa permet reconèixer HH, LL, HL i LH; no és el mapa més restrictiu amb Benjamini–Hochberg de la figura anterior."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}

La convenció de pseudo-p del complement i la seqüència aleatòria poden diferir de les d'un altre motor. Convé conservar els camps retornats i els paràmetres, no només la imatge. Per reproduir exactament un mapa publicat s'utilitza també la taula de resultats de l'execució corresponent.

### Hotspots estadístics amb Getis–Ord Gi*

Un **hotspot estadístic** és un entorn on la concentració de valors alts resulta destacada sota un contrast especificat. Una zona vermella del KDE del capítol anterior només indicava densitat elevada: no s'hi havia fet aquest contrast. Igualment, k-means divideix observacions en grups i DBSCAN identifica agrupacions segons distàncies i nombre de punts; cap dels dos produeix automàticament un p-valor de Gi*.

Gi* suma contribucions de la unitat i del seu veïnatge. En aquest exemple es reutilitzen `log_pot` i els contactes Queen, amb pesos binaris, **sense normalització per files**; el mètode estrella inclou la pròpia unitat. Es demanen 9.999 permutacions i s'activa el pseudo-p bilateral. Són decisions diferents de les del mapa de Moran local i han de constar en comparar-los {% cite getis1992analysis ord1995local %}.

![Paràmetres de Getis–Ord Gi estrella al complement de QGIS]({{ site.baseurl }}/assets/captures/hotspots-parametres.png "Gi* sobre la mateixa variable, amb contactes Queen i pesos binaris. L'opció bilateral i les 9.999 permutacions completen la configuració del contrast."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

La taula retornada conté `Z_score` i `p_value`. Amb p bilateral menor de 0,05, un signe positiu destaca una concentració alta i un de negatiu una concentració baixa. L'execució conservada destaca 7 seccions altes i 13 de baixes; les altres 130 no passen aquest llindar nominal. No s'hi ha aplicat correcció múltiple.

![Mapa QGIS de concentracions altes i baixes segons Gi estrella]({{ site.baseurl }}/assets/captures/hotspots-resultat.png "Getis–Ord Gi*: concentracions altes en vermell, baixes en blau i casos no destacats en gris. Llindar bilateral nominal de 0,05, sense correcció múltiple. No hi ha classes HL o LH."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}

Per interpretar una diferència amb Moran local es torna a la pregunta: Moran compara el valor propi amb els veïns i permet reconèixer atípics; Gi* destaca sumes locals altes o baixes. No cal que els colors coincideixin. Abans d'utilitzar el resultat per prioritzar una actuació, s'han de revisar cobertura, veïnatge i comparacions múltiples.

### Ampliació: els residus de la regressió

Si es reprèn la regressió antiguitat–potència del capítol anterior, cada residu és la diferència entre el valor observat i el que estimava la recta. Aquells residus també formen una variable per secció. Sobre les 126 seccions admeses, la matriu queen restringida a la mostra dona una I dels residus de 0,164 i pseudo-p de 0,0026. Restar la recta no elimina tota la dependència espacial. Caldria investigar variables omeses, processos compartits o patrons del registre; aquest contrast no decideix per si sol quina explicació és correcta.

Una reproducció conservarà el codi de secció, els recomptes que entren en cada indicador, W, versions i llavor. També compararà el resultat amb una altra definició defensable de veïnatge i amb criteris de cobertura més estrictes. Les diferències entre aquestes proves són part del resultat territorial, no soroll que s'hagi d'amagar.

## Transferència a parcel·les agràries {#suport-agrari}

La mateixa pregunta es pot formular sobre àrees parcel·làries: les peces grans tendeixen a tenir veïnes grans? Una parcel·la cadastral, un recinte d'ús agrari del SIGPAC i una explotació són unitats diferents. Primer es tria la unitat, després es calcula l'àrea en hectàrees i finalment es construeix el veïnatge. Per Queen es conserven els polígons; per distàncies es poden utilitzar centroides, mantenint la correspondència d'identificadors.

Una agrupació de parcel·les grans descriu geometria, no titularitat. Un mateix titular pot gestionar moltes peces petites; una peça gran pot tenir usos i condicions de tinença diversos. **Minifundi** i **latifundi** són conceptes agraris i socials, no etiquetes automàtiques dels colors HH i LL.

### Per què no s'interpolen les àrees dels centroides? {#no-interpolar-arees}

L'àrea descriu tot el polígon; no és una propietat física mesurada al seu centre. Si una parcel·la de 10 ha es divideix en dues de 5 ha sense canviar el terreny, una interpolació passaria d'una observació de 10 a dues de 5. La superfície estimada canviaria per una nova partició administrativa, no per un canvi del camp físic.

>>> Amb un termòmetre, moure's a un altre punt manté la pregunta «quina temperatura hi ha aquí?». Amb l'àrea parcel·lària, el valor pertany a una peça sencera. Travessar-ne una vora canvia d'unitat. Que el programa accepti els centroides no dona significat físic als valors interpolats.

Representar l'àrea a cada polígon conserva aquest suport. Rasteritzar-la també pot conservar-lo si cada cel·la rep l'atribut de la peça corresponent. Una altra cosa és interpolar entre centroides com si fossin temperatures. Existeixen mètodes d'interpolació areal amb supòsits propis; no són aquella operació puntual. Els [fonaments sobre observació i suport]({{ site.baseurl }}/ca/chapters/fonaments-geodisseny/#observacions-suport) permeten decidir quina pregunta s'està formulant.

## Aportació a les alternatives territorials

L'autocorrelació pot indicar sectors on es concentren determinades dimensions parcel·làries. Per estudiar candidates cal tornar als polígons: superfície admissible, forma, continuïtat, usos i restriccions. Un clúster estadístic pot contenir nuclis i veïns de dimensions diverses; no s'ha de convertir en una única finca disponible.

Si la puntuació final utilitza l'àrea de la parcel·la i també un indicador local derivat d'aquella àrea, es pot duplicar la influència de la mateixa informació. Cal justificar si el criteri representa mida individual o context espacial. El capítol multicriteri mantindrà aquesta distinció i evitarà anomenar «latifundi» un simple valor alt.

L'estabilitat entre matrius pot reforçar una diagnosi acotada. La inestabilitat revela dependència de l'escala de relació i suggereix què cal investigar. En tots dos casos, la conclusió ha de referir-se a la unitat estudiada i no a propietaris o explotacions que no s'han observat.

## Activitats

### Calcular abans d'interpretar colors

Cal reconstruir la matriu de la cadena i les dues I de la figura amb un full de càlcul. La sortida inclourà valors, mitjana, valors centrats, retards, productes i sumes. Després s'ha de repetir l'enumeració de sis ordres i explicar la diferència entre observar I positiva i obtenir un contrast significatiu.

>> Els controls són: files de W amb suma 1, diagonal zero, suma de valors centrats zero, suma de quadrats 9, I de 0,5 per agrupació i −1 per alternança. Si la mitjana canvia en permutar, no s'han conservat els mateixos valors.

### Demostrar el problema de suport

Cal comparar una partició docent abans i després de dividir una parcel·la sense modificar el terreny. Es representarà l'àrea per polígon i s'explicarà què canviaria en una interpolació dels centroides. El resultat és una demostració conceptual de per què aquesta interpolació no estima una propietat física contínua.

### Dues matrius, dues preguntes

Cal construir una matriu principal i una de contrast, conservar-ne els diagnòstics i representar els veïns de tres unitats. La justificació ha d'explicar quina relació territorial representa cada matriu i què significa una unitat aïllada.

### Associació global i local

Cal calcular un estadístic global i un de local amb variable, matriu i inferència declarades. S'han de conservar mapes de valors, significació i configuració, amb una taula de sensibilitat. Una localització destacada s'ha d'interpretar retornant a la geometria i als valors dels veïns.

### Geometria i decisió

Cal seleccionar un sector amb peces relativament grans i redactar una fitxa de candidata. La fitxa ha de separar allò que es coneix de superfície i continuïtat d'allò que faltaria sobre ús, propietat i disponibilitat. El resultat no pot qualificar el sector com a apte només perquè aparegui HH.
