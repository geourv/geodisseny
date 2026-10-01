---
layout: manual-chapter
title: Avaluació multicriteri i geodisseny
description: Objectius, restriccions, funcions de valor, pesos i sensibilitat per comparar alternatives territorials i revisar-ne el disseny.
lang: ca
ref: avaluacio-multicriteri
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/avaluacio-multicriteri/
weight: 70
part: Continguts
manual_references: true
---

Una localització pot tenir poc pendent, exposició tèrmica moderada i una peça territorial contínua, però afectar un espai incompatible amb l'actuació. Una altra pot ser admissible i obtenir puntuacions diferents segons la importància assignada a cada objectiu. L'avaluació multicriteri fa explícita aquesta estructura: què exclou, què gradua i com es comparen preferències.

El capítol integra el recorregut en un model docent de tres grups de restriccions i tres factors. La simplicitat permet reconstruir cada decisió i comprovar-ne la sensibilitat. El mapa resultant és una preselecció sota criteris declarats; el geodisseny continua amb alternatives concretes, efectes, actors i revisió de la proposta.

>>>>> En acabar el capítol, cal poder defensar una recomanació territorial condicionada.
>>>>>
>>>>> - Distingir norma aplicable, restricció docent i factor de preferència.
>>>>> - Transformar magnituds a funcions de valor i justificar-ne els pesos.
>>>>> - Implementar una combinació coherent i conservar exclusions i desconeguts.
>>>>> - Comparar sensibilitat de puntuacions, superfícies i alternatives.
>>>>> - Relacionar el resultat amb canvi, impacte i decisió en el marc de Steinitz.

## Objectius, criteris i alternatives {#decisio-espacial}

L'**objectiu** expressa una finalitat; el **criteri** permet valorar una alternativa; l'**indicador** concreta una mesura. Minimitzar moviments de terra és una finalitat; el pendent és un indicador parcial que pot ajudar a valorar-la. La relació entre tots dos necessita justificació: un pendent mitjà baix no garanteix per si sol poca excavació.

La dificultat multicriteri apareix quan una alternativa és millor en un aspecte i pitjor en un altre. Per localitzar un equipament, un lloc pot ser més accessible i un altre oferir més espai. Per restaurar un corredor fluvial, una opció pot reconnectar més hàbitat i requerir més sòl. Si totes les dimensions es reduïssin directament a una mateixa magnitud, la comparació seria més simple; sovint cal discutir com valorar conseqüències diferents.

Objectiu
: Finalitat que es vol assolir, com millorar l'accés o reduir una afectació.

Indicador
: Mesura amb unitats i suport, com minuts de recorregut, hectàrees afectades o proporció de receptors amb visió.

Funció de valor
: Regla que tradueix una mesura en una puntuació de preferència per a l'objectiu.

Pes
: Contribució relativa d'un factor dins de la regla de combinació, un cop definides les seves funcions de valor.

>>> Dues candidates fictícies tenen pendents de 4% i 8%. Són mesures del terreny. Preferir la primera perquè es vol facilitar la implantació és un judici vinculat a un objectiu. Excloure qualsevol pendent superior a un llindar seria una tercera decisió: caldria justificar el llindar i explicar si és tècnic, normatiu o assumit per a l'exercici.

Una **restricció** determina admissibilitat dins del model. Un **factor** gradua preferència entre opcions. Les exclusions no s'han de compensar amb bons valors en altres factors. Les dades desconegudes tampoc no s'han de convertir automàticament en absència de restricció.

Les alternatives poden ser localitzacions, polígons de projecte o combinacions d'actuacions. Una cel·la ben puntuada només és un element del cribratge. Per comparar propostes cal definir extensió, servei aportat, accessos, connexions i horitzó. Dues superfícies de mides diferents no són funcionalment equivalents pel fet de tenir la mateixa puntuació mitjana.

Malczewski desenvolupa la relació entre SIG i decisió multicriteri, mentre que Uyan aplica SIG i AHP a la selecció de parcs solars a Karapinar, Turquia {% cite malczewski1999gis uyan2013solar %}. Aquests treballs mostren com estructurar criteris i comparacions. Els seus pesos i llindars depenen del context i no constitueixen valors universals per al Camp de Tarragona.

## Marc català i traducció cartogràfica {#marc-normatiu}

El Decret llei 24/2021 modifica el marc d'implantació renovable i introdueix qüestions de participació i compatibilitat agrària. Per estudiar les condicions operatives cal consultar el Decret llei 16/2019 amb les seves modificacions, el planejament i les disposicions sectorials aplicables {% cite decretLlei242021 decretLlei162019 %}. Una norma modificativa històrica no resumeix necessàriament tot el règim vigent.

La consolidació del BOE de 30 d'octubre de 2025, consultada per al manual, inclou excepcions en l'article 9, tractament específic dels regadius i criteris de capacitat agrològica. El mateix servei adverteix d'actualització en procés. El cas docent ha d'identificar la versió utilitzada i comprovar les publicacions oficials posteriors abans d'atribuir una conseqüència jurídica concreta.

### Natura 2000, PEIN i capacitat agrològica

Natura 2000 i PEIN són delimitacions amb marcs que no s'han de considerar idèntics. Una unió de totes dues pot servir de **màscara docent conservadora**, si així es defineix, però no prova que cada actuació tingui el mateix règim en tot el conjunt. El tipus de projecte, les condicions i les excepcions importen.

La informació de capacitat agrològica de l'ICGC permet identificar classes, però la cobertura i l'escala s'han de comprovar. Una zona sense cartografia no és una zona de baixa capacitat. Les classes I–II no s'han de presentar com una prohibició universal independent d'autoconsum, usos, condicions experimentals o altres supòsits de la norma.

Les classes III–IV i els regadius tampoc no desapareixen del problema perquè un esquema docent només representi les classes I–II. El model 3+3 redueix dimensions per fer-les traçables; la fitxa de límits ha d'explicar quines condicions no s'hi han incorporat. La simplicitat del càlcul no pot convertir-se en una afirmació de compliment normatiu complet.

### Aigua i litoral

El **domini públic hidràulic** es relaciona amb aigües continentals i lleres; el **domini públic marítim-terrestre** i les servituds litorals tenen un altre règim. La inundabilitat representa escenaris i processos que tampoc no equivalen a aquelles delimitacions. Cal conservar capes i raons d'exclusió diferenciades.

La franja general de protecció de la Llei de costes es refereix al límit interior de la ribera del mar i conviu amb règims específics i transitoris {% cite lleiCostes1988 %}. Un buffer de 100 m al voltant d'una línia de costa cartogràfica no reprodueix automàticament aquesta delimitació. Si s'utilitza per practicar una operació, s'ha d'identificar com a aproximació geomètrica docent i contrastar-la amb la cartografia i el règim aplicables.

### El PLATER com a referència de planificació

El PLATER relaciona capacitat d'acollida, objectius territorials i desplegament d'energies renovables. La pàgina de l'ICAEN descriu una metodologia amb moltes més capes i dimensions que el model docent {% cite icaenPlater %}. La informació consultada remet a tramitació d'un projecte de decret i a fases d'informació pública: el visor, per si sol, no acredita aprovació definitiva.

La capa de capacitat d'acollida pot servir per comparar enfocaments i discutir diferències. No s'ha d'utilitzar alhora com a factor principal i com a «veritat» independent que valida el mateix model, perquè això introduiria circularitat. Cal conservar-ne versió, estat de tramitació i metodologia, i distingir-la de parcs existents o sol·licituds.

Les capes preparades per a la demostració permeten observar aquesta distinció amb dades reals. `ENERGIA_SOLAR_PROTECESPECIE` diferencia `No apta` i `Ponderació`: convertir totes dues categories en exclusió perdria el significat de la metodologia.

El ràster `ENERGIA_SOLAR_CAPACITACOLLI` ja és una sortida composta de capacitat 0–1; no és irradiància, pendent ni un factor independent de les seves entrades {% cite hipermapaEnergia %}.

En preparar el ràster provincial s'ha conservat la graella de 10 m, el zero i el valor `NoData`, sense recalcular la capacitat. Les metadades declaren una escala 1:40.000: la mida de cel·la no acredita exactitud parcel·lària de 10 m. Les diferències amb el model 3+3 s'han d'interpretar segons criteris, suport i estat de cada producte, no com una prova automàtica que un mapa sigui correcte i l'altre erroni.

## Model docent 3+3 {#model-3-3}

El model parteix d'una pregunta acotada: preseleccionar espais per estudiar alternatives fotovoltaiques sobre sòl, preservant les condicions definides i comparant tres preferències. No representa tot l'autoconsum en coberta ni tot el procés d'autorització. Les observacions ICAEN aporten context i aprenentatge analític, però no són directament les candidates del model.

![Tres grups de restriccions i tres factors alimenten una preselecció territorial]({{ site.baseurl }}/assets/diagrams/emc-3-3.mmd "Model docent 3+3: les restriccions determinen el domini admissible i els factors en graduen la preferència. La cobertura desconeguda queda identificada; la puntuació no acredita autorització ni disponibilitat."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

::: table "Components i límits del model docent"
| Component | Representació inicial | Interpretació |
| --- | --- | --- |
| R1. Espais ambientals | Màscara de les delimitacions seleccionades | Exclusió docent conservadora amb motiu i font |
| R2. Condicions agràries | Classes i condicions seleccionades, amb cobertura | No substitueix totes les excepcions ni el règim de regadiu |
| R3. Aigua i litoral | Unió documentada de condicionants diferenciats | Conservar separats DPH, litoral i escenaris hídrics |
| F1. Pendent | Funció decreixent de preferència | Indicador parcial de dificultat d'implantació |
| F2. Exposició tèrmica | Funció de l'indicador de màximes triat | No és producció anual ni temperatura de cèl·lula |
| F3. Estructura parcel·lària | Superfície utilitzable i continuïtat definides | No equival a propietat ni a facilitat contractual |
:::

Els accessos i la visibilitat es conserven per a la comparació posterior de les candidates. Aquesta decisió manté el model bàsic llegible, però no els considera irrellevants. Un escenari ampliat pot incorporar-los com a factors addicionals, revisant pesos i possibles redundàncies. No s'han d'introduir ocultament dins d'un factor de nom genèric.

### Tres estats de coneixement

Una màscara booleana utilitza 1 per a admissible i 0 per a exclòs segons el criteri. Cal mantenir també una màscara de **cobertura coneguda**. Fora de cobertura, el resultat és desconegut, no admissible per defecte. Si els nuls es converteixen en zero o un sense justificació, una mancança de dades es transforma en una decisió territorial.

La intersecció de restriccions admissibles pot expressar-se com el producte de màscares 0/1 dins del domini conegut. Convé conservar cada màscara individual per explicar per què una zona queda exclosa. Una única sortida final no permet reconstruir coincidències entre causes ni verificar una futura actualització normativa.

::: table "Lectura de tres cel·les fictícies abans de combinar factors"
| Cel·la | Condició ambiental | Condició agrària | Condició hídrica | Conclusió |
| --- | --- | --- | --- | --- |
| X | Admissible | Admissible | Admissible | Es poden calcular preferències si hi ha factors coneguts |
| Y | Exclosa | Admissible | Admissible | Exclosa per un motiu conegut |
| Z | Admissible | Desconeguda | Admissible | No es pot afirmar que compleixi totes les condicions |
:::

En X la pregunta passa a ser «quina puntuació obté?». En Y, millorar pendent o temperatura no elimina l'exclusió. En Z, primer cal resoldre o tractar explícitament la manca d'informació. Si una cel·la tingués alhora una exclusió coneguda i una altra condició desconeguda, aquella exclusió ja seria suficient per descartar-la dins del model; la manca de cobertura continuaria registrada.

>>>> Un zero pot significar puntuació mínima, exclusió o, en una codificació deficient, dada absent. Cal conservar capes i etiquetes que permetin distingir aquests significats abans de multiplicar o sumar ràsters.

## Funcions de valor i normalització {#funcions-valor}

Una funció de valor tradueix una magnitud a una escala de preferència. Normalitzar no és simplement fer que els valors càpiguen entre 0 i 100. Cal indicar si més valor és favorable o desfavorable, quins punts de referència s'utilitzen i si la resposta és lineal, esglaonada o d'un altre tipus.

Per a un factor que es vol reduir, una funció lineal acotada pot donar 100 fins a $a$, disminuir entre $a$ i $b$ i donar 0 a partir de $b$. Per a un factor creixent s'inverteix el sentit. Els llindars han de provenir d'un criteri justificat o quedar identificats com a valors docents; no es poden deduir només dels extrems observats per comoditat.

### Transformar un pendent amb una regla visible {#exemple-funcio-valor}

Per practicar, es defineix una preferència fictícia que dona 100 punts fins al 2% de pendent i baixa linealment a zero al 10%. No és un llindar legal ni una especificació d'enginyeria. Entre aquests dos extrems, la puntuació és $100(10-p)/(10-2)$, on $p$ és pendent en percentatge. Amb 6%, el resultat és $100\times4/8=50$ punts.

::: table "De la mesura a la preferència en la funció fictícia de pendent"
| Pendent | 0% | 2% | 4% | 6% | 8% | 10% | 12% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Puntuació | 100 | 100 | 75 | 50 | 25 | 0 | 0 |
:::

Per sota de 2% la funció satura a 100: no dona 125 punts a una superfície plana. Per damunt de 10% queda a zero: no produeix puntuacions negatives. Zero és aquí **preferència mínima del factor**, no exclusió automàtica. Si es vol prohibir un rang, cal representar aquella decisió com a restricció.

![Funció decreixent de valor per al pendent i canvi de preferència entre A i B en variar el pes tèrmic]({{ site.baseurl }}/assets/quarto/figures/funcions-valor.qmd "A l'esquerra, una regla fictícia transforma pendent a preferència 0–100. A la dreta, les mateixes candidates canvien d'ordre quan augmenta el pes tèrmic, mantenint el parcel·lari a 0,30 i ajustant el de pendent. Cap corba representa una norma ni preferències recollides de persones reals."){: data-figure-width-web="43rem" data-figure-width-pdf="100%"}

El panell esquerre mostra una decisió que sovint queda amagada en una reclassificació. Canviar els punts de trencament modifica la valoració encara que les dades de pendent siguin idèntiques. El panell dret, que es desenvolupa a l'exemple d'alternatives, mostra una altra decisió: quant contribueix cada valoració al resultat global. Funció de valor i pes s'han de llegir conjuntament.

### Pendent i exposició tèrmica

El pendent necessita unitats: graus i percentatge no són equivalents. La relació és $p=100\tan\theta$ quan $\theta$ s'expressa correctament en el càlcul. Una reclassificació que confongui 10° amb 10% canvia substancialment el factor. També cal conservar el mètode de derivació del MDT i el tractament de vores.

El factor tèrmic utilitza l'indicador del capítol anterior, amb el seu període. Si el model tracta una mitjana de màximes d'agost, el resultat no es pot anomenar risc de màxima absoluta. Una funció molt abrupta pot amplificar diferències menors que la incertesa de predicció. Cal provar llindars i escenaris tèrmics plausibles.

### Superfície utilitzable i fragmentació

La preferència per una peça gran ha d'estar vinculada a la mida requerida per l'alternativa. Un cop hi ha superfície suficient, premiar indefinidament parcel·les més grans pot no tenir cap justificació. La forma i la continuïtat poden importar tant com l'àrea total: dues peces estretes o separades no equivalen a una superfície compacta utilitzable.

El factor pot calcular-se sobre superfície admissible de la parcel·la i saturar-se en un llindar docent explícit. Cal distingir aquesta superfície de l'àrea original i evitar comptar-hi parts excloses. Els clústers d'autocorrelació aporten context, però no s'han d'afegir com una bonificació automàtica d'una informació ja representada per l'àrea.

La fragmentació geomètrica no és fragmentació de propietat. Si l'objectiu real inclou reduir el nombre de contractes, caldria informació de titularitat o gestió. En absència d'aquesta, el model ha de conservar un nom de factor que descrigui allò que efectivament mesura.

## Pesos, AHP i compensació {#pesos-ahp}

Els pesos expressen importància relativa dins d'una regla de combinació. El seu significat depèn de les funcions de valor: canviar el rang o la forma d'un factor pot modificar-ne la influència encara que el pes numèric es mantingui. Per tant, pesos i normalització s'han de revisar conjuntament.

L'AHP construeix una matriu recíproca de comparacions per parells. Si un criteri es considera el doble d'important que un altre segons l'escala adoptada, la comparació inversa és la meitat. La diagonal val 1. D'aquesta matriu s'obtenen pesos amb el mètode declarat, i es revisa la coherència dels judicis {% cite saaty1980ahp saaty2008decision %}.

### Una matriu coherent que es pot resoldre a mà

Per entendre la reciprocitat, es consideren tres factors genèrics F1, F2 i F3. S'assumeix que F1 pesa el doble que F2, i F2 el triple que F3. Si aquests judicis són exactament coherents, F1 ha de pesar sis vegades més que F3. Són judicis inventats per a l'exemple, no els pesos del model territorial.

::: table "Comparacions per parells fictícies i exactament coherents"
| Factor de la fila respecte del de la columna | F1 | F2 | F3 |
| --- | ---: | ---: | ---: |
| F1 | 1 | 2 | 6 |
| F2 | 1/2 | 1 | 3 |
| F3 | 1/6 | 1/3 | 1 |
:::

Es pot assignar provisionalment 1 a F3, 3 a F2 i 6 a F1. La suma és 10; normalitzar dona pesos 0,1, 0,3 i 0,6, respectivament. Comprovar quocients recupera tots els judicis: $0,6/0,3=2$, $0,3/0,1=3$ i $0,6/0,1=6$. En aquest cas construït, els mètodes habituals d'extracció de pesos recuperen la mateixa proporció.

Si, mantenint les dues primeres comparacions, s'afirmés que F1 només pesa dues vegades més que F3, ja no existiria una proporció exacta que satisfés tots els judicis. AHP permet resumir-los i estudiar-ne la inconsistència. La revisió ha de tornar a les raons de les comparacions, no canviar nombres només fins a superar un llindar.

La ràtio de consistència compara un índex d'inconsistència amb una referència aleatòria de la mida corresponent. El llindar 0,10 és una convenció habitual, no una prova de veritat, equitat o acceptació social. Una matriu coherent pot representar preferències discutibles. El full de càlcul ha de conservar judicis, justificacions, pesos i referència utilitzada.

### Suma ponderada

Amb funcions de valor $f_k$ entre 0 i 100 i pesos no negatius que sumen 1, la puntuació dins del domini admissible és:

$$
S(s)=\sum_k w_k f_k(s).
\label{eq:emc-suma}
$$

La suma és **compensatòria**: una valoració baixa pot quedar compensada per altres d'altes. Això la fa inadequada per expressar una prohibició absoluta. Les regles booleanes AND i OR representen altres lògiques de compliment; no són mesures directes de risc territorial mínim o màxim.

La correlació entre factors també importa. Si dos representen gairebé el mateix condicionant, poden duplicar-ne la influència. La revisió conceptual ha de precedir una prova estadística: dos factors poc correlacionats poden continuar compartint part del mateix objectiu o de les mateixes dades.

## Exemple numèric d'alternatives {#exemple-emc}

L'exemple següent és sintètic. A i B es consideren comparables quant al servei aportat; C incompleix una restricció definida per al cas. Les puntuacions ja han estat transformades a preferència 0–100 i no representen dades observades del Tarragonès.

::: table "Alternatives docents amb tres factors i admissibilitat separada"
| Alternativa | Admissible | Pendent | Temperatura | Estructura parcel·lària |
| --- | --- | ---: | ---: | ---: |
| A | Sí | 80 | 40 | 60 |
| B | Sí | 60 | 90 | 50 |
| C | No | 100 | 100 | 100 |
:::

Amb pesos 0,50, 0,20 i 0,30, A obté 66 i B obté 63. Amb pesos 0,20, 0,50 i 0,30, A obté 54 i B obté 72. El canvi de preferència es produeix sense modificar les dades. C continua exclosa en tots dos escenaris: una puntuació potencial elevada no compensa l'incompliment.

El primer càlcul d'A es descompon en tres contribucions: $0,50\times80=40$ punts pel factor de pendent; $0,20\times40=8$ pel tèrmic; i $0,30\times60=18$ pel parcel·lari. La suma és 66. Per a B són 30, 18 i 15 punts, que sumen 63. Fer visibles aquestes contribucions permet explicar el resultat: A guanya perquè el primer escenari dona més influència a un factor on A supera B.

### Trobar on canvia l'ordre

Si es manté el pes parcel·lari a 0,30 i s'anomena $t$ el pes tèrmic, el pes de pendent és $0,70-t$. Així, els tres pesos sempre sumen 1 per a $0\leq t\leq0,70$. Substituint les puntuacions de la taula, A obté $74-40t$ i B obté $57+30t$.

Les dues puntuacions coincideixen quan $74-40t=57+30t$, és a dir, $t=17/70\simeq0,243$. Per sota d'aquest valor A supera B; per damunt, B supera A. El panell dret de la figura mostra aquesta intersecció. En lloc d'afirmar que «A és la millor», es pot formular una conclusió més útil: A és preferida mentre la importància del factor tèrmic no superi aproximadament 0,243 sota la resta de condicions fixades.

>> La sensibilitat no exigeix generar centenars de mapes sense llegir-los. Un llindar de canvi d'ordre ja identifica quina preferència és decisiva i sobre què caldria deliberar. Les restriccions s'apliquen abans: C no entra en aquesta competició.

La diferència petita entre A i B en el primer escenari s'ha de llegir amb la incertesa dels factors. Si una entrada pot variar prou per invertir el resultat, convé conservar un conjunt de candidates i indicar què caldria verificar. La precisió decimal de la calculadora no és precisió de la decisió.

## Implementació a QGIS {#procediment-emc}

El paquet docent de Moodle identifica les fonts i la seva edició. Abans de rasteritzar, cal revisar cobertura i règim de cada restricció i construir la taula de criteris. Les capes de parcs, sol·licituds i capacitat d'acollida no s'han de fusionar en una sola categoria d'«instal·lacions»: tenen funcions i estats diferents.

### Graella comuna i màscares

Totes les sortides combinades han de compartir CRS, extensió, origen i mida de cel·la. Coincidir en resolució no garanteix alineació. Cal inspeccionar la transformació dels límits, les cel·les de vora i el criteri de rasterització. Una decisió sobre cel·les parcialment afectades pot canviar superfície admissible, especialment amb elements estrets.

La màscara de cobertura precedeix la interpretació. Dins del domini conegut, les màscares individuals es combinen conservant motius d'exclusió. La simbologia final diferencia almenys desconegut, exclòs i admissible. Cap classe ha de quedar amagada sota la mateixa etiqueta de valor zero.

### Factors i calculadora

El pendent es deriva del model del terreny amb unitats comprovades. La temperatura prové del model i període seleccionats. La superfície parcel·lària utilitzable es calcula després de les exclusions pertinents i es transforma amb la funció definida. La rasterització d'aquest últim factor manté el suport parcel·lari; no interpola centroides.

Un exemple de combinació dels tres ràsters de preferència a la Calculadora ràster és:

::: listing "Suma docent de factors ja normalitzats i alineats"
```text
0.50 * "f_pendent@1"
+ 0.20 * "f_temperatura@1"
+ 0.30 * "f_parceles@1"
```
:::

La puntuació es restringeix després al domini admissible amb una operació de màscara que conservi els nuls. Si s'utilitza una multiplicació 0/1, el valor zero resultant d'exclusió s'ha de distingir d'una puntuació zero admissible mitjançant la màscara original. Tampoc no s'ha de suposar que multiplicar per zero resol qualsevol `NoData` de les entrades.

Cal comprovar manualment unes cel·les conegudes, el rang 0–100 i la correspondència entre nom de factor i pes. Un canvi de nom o d'ordre de bandes pot produir un mapa aparentment coherent amb una combinació equivocada. El modelador ajuda a repetir la cadena, però no substitueix aquests controls.

### Lectura per parcel·la i candidata

Les estadístiques zonals han d'acompanyar la mitjana amb superfície admissible, proporció exclosa, dispersió i continuïtat. Una mitjana alta sobre una fracció mínima de la parcel·la no garanteix una alternativa viable. Les candidates poden necessitar agrupacions de peces, però aquesta operació exigeix revisar el nou suport i els condicionants compartits.

El resultat s'ha de tornar a contrastar amb accessos i visibilitat. Aquest retorn pot descartar una peça ben puntuada o suggerir una alternativa amb menor extensió i menys efectes. El mapa continu ajuda a explorar; la decisió opera sobre propostes amb significat territorial.

## Sensibilitat i robustesa {#sensibilitat}

La prova més simple modifica pesos dins de valors plausibles, però també convé contrastar funcions de valor, resolució i escenaris tèrmics. Variar un pes un ±10% relatiu no és sumar o restar deu punts percentuals. Després del canvi cal renormalitzar tots els pesos perquè sumin 1.

![Escenaris de pesos i factors produeixen comparacions de puntuació, superfície i rànquing]({{ site.baseurl }}/assets/diagrams/emc-sensibilitat.mmd "La sensibilitat conserva el model base, modifica supòsits explícits i compara candidates sota criteris comuns. L'estabilitat dins dels escenaris assajats no és una probabilitat d'encert."){: data-figure-width-web="25.5rem" data-figure-width-pdf="61%"}

Les classes de puntuació han de mantenir llindars comparables entre escenaris. Si cada mapa es classifica per quantils nous, una proporció semblant de superfície apareixerà sempre a la classe alta encara que canviïn els valors. Per estudiar canvis d'àrea amb sentit cal fixar llindars o explicar per què es modifiquen.

La taula de sensibilitat ha de conservar superfície coneguda, admissible i seleccionada, a més de diferències de puntuació i canvis de rànquing. El denominador ha de ser el mateix o quedar justificat. La freqüència amb què una candidata resulta preferida és una descripció dels escenaris provats, no una probabilitat d'error sense un model addicional.

## Del mapa al procés de geodisseny {#retorn-geodisseny}

El marc de Steinitz exigeix més que seleccionar el màxim d'un ràster {% cite steinitz2012framework %}. Cal concretar alternatives, estimar efectes respecte de la referència i explicar com intervenen actors i criteris. La millor cel·la pot formar part d'una proposta pitjor si accessos, connexions o fragmentació augmenten els efectes totals.

### Sis models per a l'hort solar

El [marc dels fonaments]({{ site.baseurl }}/ca/chapters/fonaments-geodisseny/#sis-preguntes-steinitz) es pot recuperar sobre una mateixa proposta solar. Cada model respon una pregunta diferent. La representació descriu què hi ha; el procés explica com funciona; l'avaluació jutja aquell funcionament segons objectius. Els tres models següents introdueixen alternatives, n'estimen els efectes i permeten decidir si es prefereixen.

![Sis models de Steinitz amb exemples d'un hort solar i tres recorreguts d'iteració]({{ site.baseurl }}/assets/img/steinitz-hort-solar.svg "Steinitz aplicat a una comparació docent d'horts solars. Primera iteració: entendre el lloc, de representació a decisió. Segona: dissenyar el mètode en sentit invers. Tercera: executar l'estudi. La revisió pot modificar dades, models o implantacions; no és una tramitació administrativa completa."){: data-figure-width-web="50rem" data-figure-width-pdf="100%" data-caption-source="Adaptació docent del marc de Steinitz (2012); elaboració pròpia."}

En el **model de representació** s'organitzen MDT, usos, parcel·les, camins i receptors. Un polígon de candidata encara només situa una possibilitat. El **model de procés** calcula, per exemple, com s'hi arriba, per on circula l'aigua i des d'on es veuria una altura determinada. Les tècniques de xarxes, visibilitat i interpolació dels capítols anteriors aporten models parcials d'aquest funcionament.

El **model d'avaluació** pregunta si les condicions són satisfactòries segons els objectius acordats. Aquí es defineixen exclusions, preferències i llindars. El model 3+3 pertany principalment a aquesta part: ajuda a preseleccionar àrees, però no dibuixa la implantació concreta ni calcula tots els seus efectes.

El **model de canvi** defineix alternatives comparables: A i B poden oferir una funció semblant amb disposicions diferents, accessos diferents o una ocupació menor. També es conserva l'alternativa de no implantar. El **model d'impacte** compara cadascuna amb l'estat de referència: superfície agrària afectada, moviments de terra estimats, connexions noves o receptors amb visió. Canviar el perímetre obliga a recalcular aquests efectes.

El **model de decisió** confronta els efectes amb criteris i perspectives. Pot portar a preferir A, modificar B, descartar totes dues o obtenir una dada que falta. Si B redueix l'exposició visual però empitjora l'accés, la decisió necessita explicar aquella compensació; no desapareix sota una puntuació global.

### Tres iteracions, tres funcions

La **primera iteració**, de dalt a baix, ajuda a entendre el lloc i l'abast del problema. Per a l'hort solar es pregunta què es coneix del territori, quins processos importen, quins canvis són imaginables i qui hauria de valorar-los. El resultat és una formulació compartida del problema, amb mancances d'informació identificades.

La **segona iteració** recorre el marc en sentit invers per dissenyar els mètodes. Si la decisió ha de comparar pèrdua de sòl agrari i exposició des de nuclis, cal especificar quins indicadors d'impacte ho mesuraran. Això obliga a definir les alternatives, els criteris d'avaluació, els processos necessaris i, finalment, les dades amb què es representaran. Aquest retorn evita calcular totes les capes disponibles sense saber per a què serviran.

La **tercera iteració** executa l'estudi amb els mètodes triats: prepara les dades, calcula processos, avalua, dibuixa alternatives i compara efectes. Els resultats poden obligar a repetir-ne una part. Una implantació que ocupa una àrea ben puntuada però afecta un receptor especialment sensible pot reduir-se o desplaçar-se; es recalculen els efectes abans de tornar a decidir.

>>> Una alternativa fictícia obté 72 punts d'idoneïtat, però el seu accés travessa una franja que es vol preservar. Es pot provar una entrada diferent o una implantació menor. El retorn al model de canvi és una decisió de disseny: no consisteix a augmentar un pes fins que aquella afectació deixi de veure's a la puntuació.

La recomanació conserva què és estable entre escenaris, què depèn de preferències i què encara es desconeix. També explica qui rep beneficis i qui suporta efectes. Administració, propietaris, agricultors, residents i promotors poden aportar perspectives diferents; una simulació d'aquests papers a l'aula no equival a una consulta real. L'informe final connecta la proposta escollida amb dades, mètodes, efectes i raons de revisió.

## Transferir el model a altres decisions {#altres-localitzacions}

La mateixa seqüència es pot aplicar a equipaments i activitats molt diferents. El que es transfereix és la manera de formular la pregunta, comprovar les fonts i comparar alternatives; no els pesos del cas solar. Una distància pot ser avantatge per a un ús i inconvenient per a un altre. També pot canviar qui rep el benefici i qui suporta el cost {% cite malczewski1999gis geurs2004accessibility %}.

### Escoles: cobertura i trajectes quotidians

Una escola nova es pot estudiar a partir de la població en edat escolar, la capacitat dels centres existents, els trajectes a peu i les barreres de pas. La pregunta no és només «on hi ha més infants?», sinó «quines mancances de cobertura es redueixen amb cada alternativa?». Una isòcrona necessita una xarxa transitable a peu, passos segurs i temps amb unitats justificades; la distància euclidiana no representa aquests trajectes.

Les parcel·les candidates es contrastarien amb planejament, superfície, risc d'inundació i condicions ambientals. Després es compararien cobertura addicional, temps de desplaçament i distribució de beneficis entre barris. La població prevista i els horitzons demogràfics donarien escenaris de sensibilitat. El mapa d'idoneïtat seria una entrada per a la decisió educativa, no un substitut de les necessitats de capacitat i gestió.

### Abocadors: separar exclusió i comparació

En un abocador, la geologia, la hidrogeologia, el risc, els usos, l'accessibilitat de vehicles i la distància a receptors poden tenir funcions diferents. Alguns requisits poden excloure emplaçaments segons la normativa aplicable; altres comparen alternatives admissibles. Dibuixar un radi únic al voltant de tots els elements sense consultar el règim que correspon a cadascun produeix una falsa precisió jurídica.

El disseny inclouria l'àrea de servei, els residus previstos, la vida útil i els recorreguts dels vehicles. Les alternatives es valorarien també per la distribució territorial de càrregues i per efectes acumulats. Reduir el cost mitjà de transport podria augmentar l'exposició d'un nucli concret; les dues magnituds s'han de comunicar abans d'agregar-les.

### Centres penitenciaris: accessibilitat i inserció territorial

Una pràctica sobre un centre penitenciari pot comparar connexió amb serveis sanitaris i judicials, accés de personal i visites, transport públic, disponibilitat de sòl i compatibilitat urbanística. L'accessibilitat es defineix per a usuaris i modes diferents: allunyar l'equipament dels nuclis no és, per si mateix, un objectiu suficient.

El programa funcional i els requisits verificats precedirien qualsevol ponderació. La comparació hauria d'explicar com afecten les alternatives els trajectes de les famílies, els serveis i els municipis receptors. Els pesos d'una simulació d'actors a classe representen posicions assumides, no preferències atribuïdes a institucions o habitants reals. Aquesta proposta docent no identifica cap emplaçament concret com a candidat.

### Hotels rurals: edificació existent, recursos i capacitat del lloc

Per a un hotel rural es podria començar per reutilitzar edificació existent, en lloc de cercar sòl buit amb la puntuació més alta. Els factors inclourien accessibilitat, connexió amb itineraris, recursos paisatgístics i culturals, disponibilitat de serveis i estacionalitat. La protecció patrimonial, la regulació turística, el planejament i les condicions de subministrament formarien part de la comprovació de cada alternativa.

La proximitat a un espai valuós pot afavorir l'atractiu i, alhora, augmentar la pressió sobre aquell espai. Cal separar potencial de demanda, capacitat de gestió i sensibilitat ambiental. Un mapa de paisatge no calcula automàticament ocupació hotelera; aquesta estimació requeriria dades i un model addicionals.

## Lectures per comparar decisions metodològiques {#lectures-emc}

Les lectures següents permeten revisar models publicats sense copiar-ne mecànicament els pesos. En cadascuna convé reconstruir una taula amb objectiu, unitat candidata, exclusions, factors, normalització, pesos i comprovació del resultat.

- **Instal·lacions solars.** Uyan estudia localització de plantes solars amb SIG i AHP a Karapınar {% cite uyan2013solar %}. És una lectura per identificar com s'enllacen criteris espacials i comparacions per parells. La transferència al Camp de Tarragona exigeix reconstruir fonts, planejament i significat de cada criteri; els pesos d'aquell estudi no tenen validesa universal.
- **Abocadors.** Kontos, Komilis i Halvadakis presenten una metodologia SIG aplicada a Lesbos {% cite kontos2003landfills %}. La lectura permet preguntar quines operacions eliminen opcions i quines les ordenen. Les condicions insulars i el marc normatiu de l'estudi no es poden traslladar directament a una altra jurisdicció o data.
- **Escoles.** Başeğmez, Doğan i Aydın combinen SIG, aprenentatge automàtic, ordenació de variables i TOPSIS {% cite basegmez2025schools %}. El cas ajuda a distingir la importància estimada d'una variable d'una preferència pública sobre un criteri. Cal examinar què s'ha validat: predir una variable o reproduir una classificació no equival a demostrar la conveniència territorial de la decisió.

La síntesi de lectura pot comparar dues decisions concretes: per exemple, tractar l'accessibilitat com a factor compensable o com a requisit mínim. Després s'ha de formular com canviaria el model docent, quines dades noves necessitaria i quin resultat observable permetria contrastar la millora. Aquesta és una utilització de la literatura més útil que afegir una cita al peu d'un mapa sense revisar-ne els supòsits.

## Activitats

### Distingir mesura, valoració i exclusió

Cal calcular les puntuacions de pendent per a 1%, 5% i 11% amb la funció resolta i explicar si una puntuació zero implica prohibició. Després s'ha de comparar aquesta regla amb una restricció fictícia que exclogués pendents superiors al 10%. El resultat ha de conservar les dues interpretacions en columnes diferents.

>> Les puntuacions són 100, 62,5 i 0. Amb la funció de valor sola, 11% és preferència mínima i encara podria compensar-se amb altres factors. Amb la restricció addicional, quedaria exclòs. La distinció depèn de la regla adoptada, no del color vermell del mapa.

### Taula de criteris i justificació

Cal preparar el model 3+3 amb font, data, suport, funció i regla de cada component. S'ha de distingir norma, simplificació docent i preferència. La comprovació consisteix a identificar una excepció o manca de cobertura que una simple màscara no resoldria.

### Reconstruir l'exemple

Cal obtenir les puntuacions 66 i 63, i després 54 i 72, per a les alternatives A i B. C ha de continuar exclosa. El full de càlcul conservarà valors, pesos i fórmules, i explicarà per què admissibilitat i preferència es mantenen separades.

### Model ràster i lectura territorial

Cal generar màscares, factors i puntuació amb graella comprovada. La síntesi parcel·lària inclourà superfície admissible i continuïtat, i es contrastarà amb accessos i visibilitat. El resultat serà una fitxa de dues candidates comparables, no només un mapa classificat.

### Sensibilitat i decisió argumentada

Cal comparar un escenari base i almenys dos canvis justificats, mantenint classes i denominadors coherents. L'informe explicarà variacions de superfície i rànquing i formularà una recomanació amb condicions. Si la informació no permet decidir, s'ha d'identificar la comprovació concreta que faria avançar el procés.
