---
title: "Pràctica: anàlisi d'intervisibilitat"
author: Benito Zaragozí
lang: ca
date: "Edició: 30 d'octubre de 2026"
content_status: review
---

# Intervisibilitat entre punts, recorreguts i àrees

Començarem amb una torxa industrial de la Canonja: **es veu des d'un punt de la carretera?** Després estudiarem el recorregut de la TV-3148 entre Vila-seca i l'enllaç de la Pineda: **quines posicions es veuen al llarg de la via?** Finalment ampliarem els objectius: **des d'on es veu alguna part del recinte petroquímic?**

El punt dona una resposta 0/1; la carretera suma observadors; el recinte resumeix objectius industrials. Les elevacions, altures i cobertura són comunes, però els nombres no representen la mateixa magnitud. Cap resultat mesura directament persones exposades ni impacte paisatgístic.

**El professor indicarà a classe quins apartats i exercicis són obligatoris dins del 70% de la qualificació**, i ho recollirà a la tasca de Moodle. Aquesta guia ofereix la progressió completa de punt, línia i àrea; la selecció de classe determina què s'ha de lliurar. Les ampliacions permeten aprofundir i aspirar a l'excel·lent, amb una pregunta i resultats justificats, sense substituir els obligatoris.

## Obrir el paquet

1. Descomprimeix el ZIP complet. `LLEGIU-ME.pdf` és a l'arrel i els recursos a `data/`. Utilitza **QGIS 3.44 LTR**, amb Processament i GDAL.
2. Obre **`data/inici.qgz`**. A **Explorador → GeoPackage → Connexió nova**, connecta també `data/visibilitat-costa.gpkg` per consultar els vectors. Els ràsters són GeoTIFF separats a `data/rasters/`.
3. Comprova **EPSG:25831**, unitats mètriques i el·lipsoide **Cap / NONE**.
4. Conserva `data/` com a referència i crea `sandbox/` al seu costat. Desa-hi una còpia del projecte com a **`intervisibilitat.qgz`**, amb rutes relatives, i utilitza un GeoPackage nou per als vectors de treball. Les expressions dels lots utilitzaran `sandbox/` amb `@project_folder`; desa el projecte abans d'emplenar les sortides.

Les proves, les conques individuals i els intermedis es conserven a `sandbox/`. Al final prepararàs `dist/` només amb els resultats i recursos seleccionats per lliurar. L'ordre de dibuix segueix el panell **Capes**; els grups poden reflectir aquestes fases, però no mouen fitxers. Les captures mostren una sessió de referència: les rutes absolutes depenen de la ubicació on treballes.

| Entrada | Què representa |
| --- | --- |
| `mdt` / `mds` | Terreny i superfície opaca, graella de 5 m |
| `domini` | Cobertura comparable: 1 o NoData |
| `torxa` | T, estructura identificada i cotes de model |
| `carretera` / `mostres_carretera` | Recorregut i 37 posicions de treball |
| `coberta_original` | Polígon MCSC 2024 abans de generalitzar |
| `receptors` | R1–R5 per consultar respostes |
| `ambit` / `ortofoto` | Extensió comuna i context local |

Table: Dades preparades per al recorregut de punt, línia i àrea.

La capa de mostres de carretera s'anomena `mostres_carretera` al GeoPackage. La font local DejaVu Sans de `data/fonts/` és un recurs del projecte i s'ha de conservar amb el paquet.

![Torxa, carretera i sector industrial sobre l'ortofoto.](captures/visibilitat-costa-dades.png){width=100% height=380pt}

La graella comuna té **2.000 × 2.000 cel·les de 5 m**: X 342000–352000, Y 4549000–4559000. MDT i MDS provenen del LiDAR ICGC **2021–2023**. L'MDT és natiu de 5 m; l'MDS d'1 m s'ha agregat pel màxim a 5 m. El màxim pot eixamplar obstacles estrets i les capçades es tracten com a opaques.

El grup **Ortofoto ICGC** conté el retall local i la capa **WMS**, que necessita internet. El retall de 2025 és de 10 m/píxel i permet treballar sense connexió; la capa d'origen del servei és de 25 cm. Per veure detalls, activa el WMS i desactiva la còpia local; per continuar sense internet, torna a la local. Aquesta elecció només canvia el context visual, no l'MDT, l'MDS ni la graella d'anàlisi.

Conserva `data/ortofoto-wms.xml` amb les dades: és la configuració de la capa en línia.

![Ortofoto local activada i WMS desactivat dins del mateix grup de context. La casella del WMS s'activa només quan hi ha connexió.](captures/visibilitat-ortofoto-context.png){width=70% height=400pt}

![MDS amb el mateix enquadrament i llegenda de cotes en metres.](captures/visibilitat-costa-mds.png){width=100% height=380pt}

El domini comparable té **3.490.455 cel·les**. Els buits del mar cartografiat s'han tractat a 0 m; els altres buits i les línies afectades per elevacions desconegudes queden fora del domini. **NoData no és ocultació.**

Utilitza **`data/rasters/mdt.tif`**, **`mds.tif`** i **`domini.tif`**, ja carregats com **MDT**, **MDS** i **Domini**. No cal exportar-los abans de calcular. En desar intermedis, conserva CRS, resolució, alineació i NoData. Els vectors continuen al GeoPackage.

# A. Torxa i parelles de visió

## Cota de T

T correspon al node OSM **7682543312**, classificat com a torxa industrial i contrastat amb l'ortofoto. El punt original és aproximadament (346894,82; 4552508,35) m. El càlcul utilitza el centre de cel·la **(346892,5; 4552507,5) m**, amb un desplaçament de 2,48 m.

| Magnitud | Metres |
| --- | ---: |
| MDT a T | 20,94 |
| Pic MDS | 151,31 |
| Diferència pic–terreny | 130,37 |
| Cota T del model, pic +1 m | 152,31 |
| Altura relativa sobre MDT | 131,37 |
| Altura relativa sobre MDS | 1 |

Table: Cotes i altures utilitzades per a T.

Els aproximadament 130,4 m són una estimació d'estructura a partir del LiDAR. Les cotes de la taula estan arrodonides per facilitar-ne la lectura; això no acredita una exactitud centimètrica del model. El metre addicional separa el punt de model de la superfície digital: **no mesura la flama**. Els atributs de `torxa` conserven les cotes de procedència.

![Torxa identificada al detall de l'ortofoto.](captures/visibilitat-costa-torxa.png){width=100% height=380pt}

## Conca sobre MDT

Obre **Procés → Caixa d'eines** o **Ctrl+Alt+T**. Cerca **Viewshed** i comprova el proveïdor GDAL.

1. Eina `gdal:viewshed`, entrada `MDT`, banda 1.
2. Observador: `346892.5,4552507.5 [EPSG:25831]`.
3. Altura d'observador **131,37 m**; altura de destinació **1,7 m**; distància màxima **0**, tota la finestra.
4. Prem el triangle de **Advanced Parameters / Paràmetres avançats**, sota la distància màxima, per desplegar els camps que estan ocults.
5. Localitza **Additional command-line parameters / Paràmetres addicionals de la línia d'ordres**, identificat com a `EXTRA` a l'ajuda. El formulari principal de Viewshed no té una casella pròpia per a NoData: s'introdueix en aquest quadre de text. Escriu-hi la línia completa següent:

```text
-vv 1 -iv 0 -ov 255 -a_nodata 255 -cc 0.85714
```

No afegeixis cometes ni posis cada opció en una fila diferent. Utilitza el guionet normal `-`, conserva el guió baix de `-a_nodata` i el punt decimal de `0.85714`.

| Opció i valor | Funció |
| --- | --- |
| `-vv 1` | Escriu 1 als llocs visibles; el valor per defecte de GDAL és 255 |
| `-iv 0` | Escriu 0 als llocs ocults: és una observació vàlida, no NoData |
| `-ov 255` | Codi dels llocs fora de l'abast màxim, si s'ha limitat |
| `-a_nodata 255` | Declara 255 com a NoData de la sortida |
| `-cc 0.85714` | Coeficient de curvatura/refracció del model |

Table: Opcions escrites en un únic camp avançat de GDAL Viewshed.

**No posis NoData a 0**: eliminaries els llocs ocults. Tampoc no deixis visibles=255 i NoData=255 alhora. `-ov` assigna un codi als píxels fora d'abast; `-a_nodata` declara el codi de NoData: són funcions diferents. Aquesta declaració no reconstrueix elevacions desconegudes de l'entrada; utilitza les dades preparades i la màscara Domini.

6. Desa la conca crua a `sandbox/` i carrega-la com **Conca T MDT**.
7. Amb Calculadora ràster, `native:rastercalc`, aplica:

```text
"Domini@1" * "Conca T MDT@1"
```

8. Mantén extensió, 5 m i EPSG:25831; desa `T-mdt.tif`. A **Registre / Log**, comprova que l'ordre generada conté `-vv 1` i `-a_nodata 255`. A **Propietats de la capa → Informació**, comprova banda Byte i NoData 255 a la conca crua; els valors vàlids són 0 i 1. La calculadora pot assignar un altre codi de NoData a la sortida emmascarada.

![Camp de paràmetres addicionals desplegat amb les opcions de GDAL Viewshed. La línia assigna 1 als visibles, 0 als ocults i 255 al NoData; s'escriu sencera en un únic camp.](captures/visibilitat-extra-obert.png)

El càlcul de referència conservat té **2.962.199 cel·les visibles**, **84,87%** del domini. Si Calculadora ràster canvia el codi de NoData, consulta la banda; no l'interpretes com zero.

## Comparar amb MDS i consultar receptors

1. Repeteix Viewshed amb MDS, mateix T i altura d'observador **1 m**. Altura de destinació 0, distància màxima 0.
2. Desplega els paràmetres avançats i substitueix el contingut del mateix camp d'opcions addicionals per `-om DEM -cc 0.85714 -a_nodata -9999`. Desa la sortida Float64 com **Cota mínima MDS**.
3. El mode DEM retorna cota absoluta mínima i ignora l'altura de destinació. Mantén els receptors a **MDT +1,7 m**:

```text
"Domini@1" * (("MDT@1" + 1.7) >= "Cota mínima MDS@1")
```

4. Desa `T-mds.tif`. Control: **447.860 cel·les**, **12,83%** del domini.
5. Executa **Mostreja els valors ràster**, `native:rastersampling`, sobre `receptors`, amb prefixos diferents per a MDT i MDS.

| Receptor | Mostra de carretera | MDT | MDS |
| --- | --- | ---: | ---: |
| R1 | C05 | 1 | 1 |
| R2 | C11 | 0 | 0 |
| R3 | C13 | 1 | 0 |
| R4 | C37 | 1 | 0 |
| R5 | Fora del retall | Nul | Nul |

Table: Parelles de contrast sense moure els extrems entre superfícies.

![Parelles visibles i ocultes amb el mateix origen T.](captures/visibilitat-costa-intervisibilitat.png){width=100% height=380pt}

**Conserva:** els dos mapes, la cota mínima, el domini i la taula de parelles. Distingeix relleu, obstacle superficial i lloc no calculat.

# B. Conca acumulada de carretera

El recorregut fa aproximadament **3.652,27 m** i segueix una trajectòria única de la TV-3148 fins a l'enllaç amb la TV-3146. No suma les dues calçades com si foren una línia única de longitud doble ni modela sentits de circulació.

1. Amb **Punts al llarg de la geometria**, `native:pointsalonglines`, sobre `carretera`, usa distància **98,71 m**, inici **49,36 m** i final 0. Desa aquesta prova amb un nom nou.
2. Comprova 37 punts a la prova creada. Per al lot guiat següent utilitza **`mostres_carretera` del paquet**, no aquella sortida nova. Ja conté identificadors C01–C37, `x` i `y` als centres de cel·la, `pk_m`, `pes` i els camps del contrast MDT/MDS; la suma de pesos recupera la longitud.
3. Fes una execució individual de control per a **C05**, amb ulls d'origen/destinació **1,7 m**, abast 0 i les mateixes opcions. El lot següent repetirà la configuració per a cinc punts de prova i després per a les 37 posicions.

![Configuració de Punts al llarg de la geometria: interval de 98,71 m i desplaçament inicial de 49,36 m sobre la TV-3148.](captures/visibilitat-carretera-parametres.png){width=95% height=420pt}

### Camps de coordenades abans d'autoemplenar

```{=latex}
\begin{manualcallout}{ManualCalloutWarning}{Alerta}
```

**Punts nous i mostres preparades.** Punts al llarg de la geometria hereta atributs i afegeix distància i angle, però **no crea automàticament els camps `x` i `y`** que utilitzen les expressions d'aquesta guia. Comprova'ls a la taula abans d'obrir el lot. Canviar el nom d'una capa nova a C no hi afegeix aquests camps ni els identificadors C01–C37.

```{=latex}
\end{manualcallout}
```

Si has de preparar punts nous, les coordenades es poden afegir **a tots els registres d'una vegada**, sense escriure-les punt per punt:

1. Cerca **Afegeix camps X/Y a la capa / Add X/Y fields to layer**, `native:addxyfields`, a la Caixa de Processament.
2. Entrada: els punts nous. Fixa **EPSG:25831** com a sistema de coordenades; no deixis el valor inicial EPSG:4326 si necessites coordenades UTM en metres. Deixa el prefix dels camps buit i desa una capa nova.
3. Comprova que la taula conté camps numèrics **`x` i `y`**, sense nuls. Són les coordenades de la geometria. També es poden calcular amb Calculadora de camps, amb `x($geometry)` i `y($geometry)`, respectivament; el càlcul s'aplica a tota la capa.

Les mostres preparades ajusten les coordenades al centre de les cel·les de 5 m. Afegir X/Y a uns punts nous no fa aquest ajust ni crea els camps de pes, altura o cobertura. Per reproduir les xifres de referència i les expressions filtrades de cinc punts, continua amb **`mostres_carretera` del paquet**. En un altre cas, prepara també identificadors únics i un ordre estable: un ID heretat de la carretera no identifica necessàriament cada observador.

## Primera execució per lots

Al menú contextual de moltes eines de la Caixa de Processament apareix **Executar com a procés per lots…**. Potser ja has vist aquesta opció en altres eines sense utilitzar-la. Ara la farem servir per repetir Viewshed sense haver d'obrir el diàleg per a cada observador.

**Un lot és una taula: cada fila de càlcul és una execució i cada columna és un paràmetre o una sortida.** Viewshed continua calculant un observador cada vegada. Aquí canvien les coordenades i el TIFF de sortida; es mantenen MDT, banda, altures, abast i opcions. El lot no emmascara ni suma les conques.

### Autocompletar un primer lot de cinc punts

A la Caixa de Processament, cerca **Viewshed** del proveïdor GDAL, fes clic dret sobre l'eina i tria **Executar com a procés per lots…**. També pots obrir Viewshed normalment i prémer el botó amb aquest nom a la part inferior del diàleg.

![Taula de Viewshed després d'emplenar el lot de prova: cinc observadors i cinc noms de sortida diferents. Les capçaleres visibles estan ressaltades; les altres columnes es configuren amb les constants indicades més avall. Els botons de carpeta i disc, ressaltats en verd, recuperen i desen el fitxer .batch.](captures/visibilitat-batch-taula.png)

El menú de cada columna ofereix aquestes tres operacions. Els noms catalans de la captura poden diferir lleugerament dels d'una altra instal·lació:

| Opció del menú | Què fa | Ús en aquesta pràctica |
| --- | --- | --- |
| **Omple cap avall / Fill Down** | Copia el primer valor a totes les files existents | MDT, banda, altures constants i opcions |
| **Calcula segons una expressió… / Calculate by Expression…** | Calcula un valor per a cada fila existent | Un nom de sortida per observador; `@row_number` comença en 0 |
| **Selecciona valors segons una expressió… / Add Values by Expression…** | Afegeix files amb els elements d'una llista | Les cinc coordenades, o les 37 del conjunt complet |

Table: Tres opcions d'autoemplenat amb funcions diferents.

![Menú real d'Emplenament automàtic de la columna Observer location. L'opció ressaltada, Selecciona valors segons una expressió, afegeix una fila per element de l'array; no recalcula les files que ja hi havia.](captures/visibilitat-batch-autofill.png)

| Mostra | Observer location | Sortida a la carpeta de prova |
| --- | --- | --- |
| C05 | `344977.5,4552147.5 [EPSG:25831]` | `conca-C05-mdt.tif` |
| C11 | `345422.5,4551812.5 [EPSG:25831]` | `conca-C11-mdt.tif` |
| C13 | `345587.5,4551707.5 [EPSG:25831]` | `conca-C13-mdt.tif` |
| C25 | `346417.5,4550937.5 [EPSG:25831]` | `conca-C25-mdt.tif` |
| C37 | `347257.5,4550157.5 [EPSG:25831]` | `conca-C37-mdt.tif` |

Table: Cinc mostres de carretera per comprovar l'autocompletat, en EPSG:25831.

Són cinc observadors de la carretera, **no els receptors R1–R5**: R5 és fora del retall i serveix per interpretar un resultat no calculat. Canvia el nom de la capa `mostres_carretera` a **C** al panell Capes; no cal reanomenar la taula del GeoPackage. El projecte ha d'estar en EPSG:25831.

1. Comença en una taula de lot nova. La fila **Autofill… / Emplenament automàtic** és la capçalera de menús; la fila de sota és una execució inicial encara buida.
2. A **Observer location**, obre el menú **Emplenament automàtic… → Selecciona valors segons una expressió… / Autofill… → Add Values by Expression…**. És el menú d'aquesta columna, no el de l'altura. Enganxa l'expressió següent:

```text
aggregate(
  layer := 'C', aggregate := 'array_agg',
  expression := to_string("x") || ',' || to_string("y")
                || ' [EPSG:25831]',
  filter := "id" IN ('C05','C11','C13','C25','C37'),
  order_by := "id"
)
```

![Editor d'Add Values by Expression amb el filtre dels cinc observadors. La previsualització retorna un array de coordenades dels camps x i y de C; comprova els camps i els identificadors abans d'acceptar.](captures/visibilitat-batch-expressio.png)

3. La previsualització ha de mostrar una llista de **cinc textos de coordenades**. Prem **D'acord / OK** i comprova les cel·les de la taula: han de correspondre als cinc punts de la taula anterior. Seleccionar cinc objectes al mapa no substitueix el filtre explícit de l'expressió.
4. **Compta les files després de tancar l'expressió.** En QGIS 3.44.11, Add Values conserva la fila inicial buida i afegeix les cinc noves: queden sis files d'execució. Selecciona el número de la fila inicial buida a l'esquerra i prem **− / Remove row(s)**. Han de quedar **cinc execucions amb coordenades**, més la capçalera Autofill. No executis una fila buida ni una coordenada `0,0`.
5. A la barra superior del lot, prem **Toggle advanced mode / Mostra els paràmetres avançats**. En el lot, aquest botó mostra columnes amagades; no és el triangle del diàleg individual. Desplaça't horitzontalment fins a **Additional command-line parameters**.
6. Emplena la primera fila amb els valors comuns de la taula següent i, **en cada columna comuna**, fes **Autofill… → Fill Down**. No ho facis a Observer location ni a la sortida.

![Després d'acceptar l'array hi ha sis execucions: la primera continua buida i les altres cinc tenen coordenades. El requadre identifica la fila que s'ha de retirar; la capçalera d'autoemplenat no és una execució.](captures/visibilitat-batch-fila-buida.png)

![Omple cap avall o Fill Down al menú dels paràmetres addicionals. Copia les opcions de la primera fila a les altres; aquesta acció serveix per a constants, no per als noms de sortida.](captures/visibilitat-batch-fill-down.png)

| Columna comuna | Valor per a les cinc execucions MDT |
| --- | --- |
| Entrada i banda | MDT i 1 |
| Observer height / Target height | 1,7 m i 1,7 m |
| Maximum distance | 0, tota la finestra |
| Additional command-line parameters | `-vv 1 -iv 0 -ov 255 -a_nodata 255 -cc 0.85714` |

Table: Constants del lot: s'emplenen a la primera fila i es copien cap avall.

![Menú de la columna Sortida amb Calcula segons una expressió ressaltat. Es calcularà un nom per fila existent; copiar un únic nom amb Omple cap avall faria coincidir les destinacions.](captures/visibilitat-batch-calcula.png)

7. Comprova que el projecte obert és **`sandbox/intervisibilitat.qgz`** i crea **`sandbox/conques-mdt-prova/`**. A l'editor d'expressions, previsualitza primer `@project_folder`: ha de donar la carpeta `sandbox`, sense el prefix `geopackage:`. A **Sortida / Output**, utilitza **Autofill… → Calculate by Expression… / Calcula mitjançant una expressió…** amb:

```text
@project_folder || '/conques-mdt-prova/conca-' ||
array_get(
  aggregate(
    layer := 'C', aggregate := 'array_agg', expression := "id",
    filter := "id" IN ('C05','C11','C13','C25','C37'),
    order_by := "id"
  ),
  @row_number
) || '-mdt.tif'
```

Aquí es calcula **un nom per a cada fila existent**. `@row_number` comença en **0**, encara que el número visible de la taula inclogui la fila Autofill. `@project_folder` és la carpeta del projecte `.qgz` desat. Revisa les cinc rutes completes i diferents, de C05 a C37, en el mateix ordre que les coordenades. Cada sortida ha de ser una ruta ordinària de fitxer `.tif`, dins de la carpeta creada.

![Editor de Calcula segons una expressió per a la sortida. La previsualització correspon a la primera fila; després d'acceptar, comprova a la taula els cinc noms calculats amb el mateix ordre d'observadors.](captures/visibilitat-batch-sortides.png)

```{=latex}
\begin{manualcallout}{ManualCalloutWarning}{Alerta}
```

**Rutes a Windows.** Revisa una ruta completa abans d'executar el lot. El projecte pot aportar una carpeta com `C:\Users\Nom\Documents\practica\sandbox`, mentre que una concatenació afegeix `/conques-mdt-prova/`. Per obtenir separadors uniformes `\` a Windows, l'expressió següent normalitza **tota la ruta final**. En una cadena de l'editor d'expressions, `'\\'` representa una barra invertida. Desa primer el projecte i crea la carpeta de sortida.

```{=latex}
\end{manualcallout}
```

```text
replace(
  @project_folder || '/conques-mdt-prova/conca-' ||
  array_get(
    aggregate(
      layer := 'C', aggregate := 'array_agg', expression := "id",
      filter := "id" IN ('C05','C11','C13','C25','C37'),
      order_by := "id"
    ),
    @row_number
  ) || '-mdt.tif',
  '/', '\\'
)
```

Aplica la mateixa normalització quan canviïs la carpeta per als altres lots. Torna a revisar les cel·les ja emplenades: editar l'expressió o desar el projecte no corregeix automàticament les rutes anteriors.

8. Prem **Executa**. A **Registre / Log**, comprova que GDAL acaba amb codi0 i que s'han creat cinc TIFF vàlids. Un missatge d'error o un codi no zero requereix corregir l'execució encara que el resum de Processament digui que ha acabat. La casella **Carrega les capes en acabar** afegeix els resultats al projecte, però no els suma.

### Si la sortida comença per geopackage:

Un projecte incrustat dins d'un GeoPackage pot donar a `@project_folder` un valor com `geopackage:/ruta/data`. Afegir-hi `/conca.tif` no el converteix en una ruta GeoTIFF vàlida. A la distribució actual, el projecte és un `.qgz` extern; si es recupera un projecte incrustat d'una edició anterior, desa'n primer una còpia a `sandbox/intervisibilitat.qgz`.

Després de desar, **torna a calcular les cel·les de sortida del lot**: QGIS no reescriu automàticament les rutes que ja hi havia. Comprova que la carpeta existeix i que cap sortida comença per `geopackage:`. Una referència d'entrada `GPKG:/ruta/fitxer.gpkg:mdt` pot identificar un ràster vàlid; el prefix `geopackage:` davant del nom de sortida `.tif` és un problema diferent. Exportar l'entrada a GeoTIFF no corregeix aquella ruta de sortida.

### Si la previsualització és correcta però la taula queda a zero

**Add Values by Expression** espera una llista i n'afegeix un element a cada fila nova. **Calculate by Expression** espera el valor d'una sola cel·la i recalcula les files existents. Si poses l'array sencer de coordenades en aquesta segona opció, el control de punt pot convertir-lo en `0,0`, tot i que l'array sembli correcte en previsualització.

Per recuperar una taula que ja té exactament cinc files, tria **Calculate by Expression** a Observer location i introdueix **un element de la llista per fila**:

```text
array_get(
  aggregate(
    layer := 'C', aggregate := 'array_agg',
    expression := to_string("x") || ',' || to_string("y")
                  || ' [EPSG:25831]',
    filter := "id" IN ('C05','C11','C13','C25','C37'),
    order_by := "id"
  ),
  @row_number
)
```

Torna a comprovar les coordenades **fora** del diàleg d'expressions. Per a 37 files, utilitza la mateixa expressió **sense la línia `filter`**. Si la capa no es diu C o no té els camps `x`, `y` i `id`, corregeix-ne la referència; una previsualització nul·la o una fila a zero no són un resultat acceptable.

El menú de **Capa d'entrada** té també opcions per seleccionar capes obertes o fitxers. Serveixen per afegir entrades a les execucions, per exemple els TIFF d'un lot de Calculadora ràster. No converteixen una selecció d'objectes de C en coordenades d'Observer location.

![Menú d'autoemplenat de l'entrada ràster: les tres opcions generals i les de selecció de fitxers, carpetes o capes obertes. L'etiqueta diferencia aquesta selecció d'entrades de l'array de coordenades dels observadors.](captures/visibilitat-batch-seleccio.png)

### Afegir les 37 coordenades amb una expressió

Prepara una **taula nova** per al lot complet. No afegeixis les 37 posicions al darrere de les cinc de prova: duplicaries aquells observadors. Mantén C com a nom de `mostres_carretera`.

A la columna **Observer location**, tria **Autofill… → Add Values by Expression…**. Aquesta opció afegeix files a partir d'una llista. **Calculate by Expression…** és diferent: només modifica les files que ja hi ha. Introdueix:

```text
aggregate(
  layer := 'C', aggregate := 'array_agg',
  expression := to_string("x") || ',' || to_string("y")
                || ' [EPSG:25831]',
  order_by := "id"
)
```

Després de D'acord, retira la fila inicial buida si ha quedat abans de les noves coordenades: en la versió comprovada apareixen **38 execucions abans de retirar-la**. Comprova **37 files de càlcul**, de C01 a C37, sense comptar Autofill. La primera coordenada és `344677.5,4552382.5 [EPSG:25831]`; l'última, `347257.5,4550157.5 [EPSG:25831]`. Revisa també C05, C11 i C13 a les seves files.

Mostra les columnes avançades i copia amb **Fill Down** només les constants del lot de cinc. Crea **`sandbox/conques-mdt/`**. A **Sortida → Calculate by Expression**, utilitza:

```text
@project_folder || '/conques-mdt/conca-' ||
array_get(
  aggregate(
    layer := 'C', aggregate := 'array_agg', expression := "id",
    order_by := "id"
  ),
  @row_number
) || '-mdt.tif'
```

Revisa 37 noms únics, `conca-C01-mdt.tif` a `conca-C37-mdt.tif`. També es pot triar el primer TIFF amb **… → Select File/Folder… → Fill with numbers**, però cal conservar la correspondència entre número i observador. **Fill Down amb un únic nom de sortida sobreescriuria els resultats.**

Desa el lot complet abans d'executar-lo. Executa i comprova les 37 finalitzacions al registre abans de continuar.

### Desar, recuperar i editar el fitxer del lot

1. Amb la taula plena i comprovada, prem el **botó de disc / Desa el lot** i desa, per exemple, `conques-mdt.batch` dins de `sandbox/`. Conserva també la prova de cinc punts amb un nom diferent.
2. Per recuperar-la, obre **Viewshed com a procés per lots** i prem el **botó de carpeta / Obre el lot**. Selecciona el `.batch` i revisa el nombre de files, entrades, coordenades, altures, opcions i sortides abans de prémer Executa.
3. Si una execució s'ha interromput, comprova quins TIFF s'han creat correctament. Prepara una còpia de la configuració només amb les files pendents; carregar el `.batch` no identifica automàticament les execucions acabades.

El `.batch` és **un fitxer de text JSON**, que es pot obrir amb un editor de text. En la versió de referència, la marca de format és `batch_3.40`; `rows` conté les execucions i cada fila separa `PARAMETERS` de `OUTPUTS`. El fitxer desa els valors de la taula, no les dades, els TIFF ni l'historial de les expressions d'autoemplenat. Cal obrir-lo a l'eina corresponent i conservar les entrades.

Es poden preparar ràpidament identificadors, coordenades, altures i noms en un **full de càlcul** o un **editor de text**. Per editar directament el `.batch`, parteix d'un fitxer desat per la teva versió de QGIS i conserva l'estructura JSON, les claus, cometes i tipus de valor. Un CSV no es pot reanomenar a `.batch` i esperar que sigui equivalent. A JSON, una barra invertida d'una ruta Windows s'escriu `\\`; el desament de QGIS ja en fa l'escapament. Reobre sempre la còpia editada i comprova'n les files abans d'executar-la.

Quan hagis utilitzat lots, conserva el **`.batch`, les expressions i una captura de la taula plena** com a evidència del procediment, útil també per a la revisió amb Unaltramesa. Afegeix el registre i els controls dels resultats per acreditar què s'ha calculat: la configuració sola no demostra una execució correcta.

### Recuperar un lot després de traslladar el treball

Les rutes relatives del QGZ **no converteixen automàticament les del `.batch`**: aquest pot conservar les adreces absolutes escrites a la taula. Tampoc s'hi desa `@project_folder` com una fórmula que es recalcula en carregar-lo.

1. Conserva la configuració original i treballa sobre una còpia. Obre el projecte traslladat, desa'l a `sandbox/intervisibilitat.qgz` i comprova les capes d'entrada i la nova carpeta del projecte.
2. Carrega la còpia del `.batch`. Reassigna les entrades als fitxers de la ubicació nova, crea les carpetes de sortida i **torna a calcular totes les cel·les de sortida** amb les expressions corresponents. Mantén el mateix filtre i ordre d'observadors; no afegeixis files si només estàs corregint rutes.
3. Revisa la taula completa i desa la còpia amb un nom diferent. Una prova de recuperació no necessita executar el lot complet. Si cal tornar a calcular, utilitza una carpeta de sortides nova, sense sobreescriure resultats comprovats.

Per al lliurament, la configuració original documenta l'execució feta. Si només s'han seleccionat alguns resultats o intermedis, explica la correspondència entre aquelles rutes i els fitxers lliurats. No presentis el `.batch` com una execució portable sense haver-ne comprovat també les entrades i les sortides des de la ubicació nova.

### Suma posterior de les conques

El lot ha produït fitxers individuals. Per acumular-los, **una sola execució d'Estadístiques de cel·la pot sumar tots els TIFF**; no cal escriure una expressió de 37 termes ni encadenar sumes de dos en dos.

1. Cerca **Estadístiques de cel·la / Cell statistics**, `native:cellstatistics`, a la Caixa de Processament. Obre l'eina **normalment**, no com un altre lot: ara les entrades es combinen en una sortida.
2. A **Capes d'entrada / Input layers**, prem **…**. Selecciona totes les conques de la carpeta corresponent amb **Afegeix fitxers / Add files** o marca-les entre les capes carregades. Per a la prova, selecciona només els cinc TIFF de `conques-mdt-prova`; per al resultat complet, només els 37 de `conques-mdt`. Comprova el recompte abans de tancar el selector.
3. Tria **Suma / Sum**. **Count / Recompte** comptaria valors vàlids, també els zeros, i no respondria quants observadors veuen el lloc.
4. Desmarca **Ignora els valors NoData / Ignore NoData values**. Pren una conca del mateix conjunt com a **Capa de referència / Reference layer**: C05 per a la prova o C01 per al conjunt de 37.

![Estadístiques de cel·la amb cinc conques seleccionades, Suma i Ignora NoData desactivat. La referència és Conca C05; els requadres assenyalen les entrades i l'operació que les combina. Els paràmetres avançats encara estan col·lapsats.](captures/visibilitat-lots-suma.png){width=75% height=420pt}

5. A **Paràmetres avançats**, fixa **Output NoData value = 255**. Desa `suma-prova-crua.tif` o `suma-C-crua.tif`, fora de la carpeta d'entrades, i executa una vegada. Comprova extensió, EPSG:25831 i píxel de 5 m; les entrades han de compartir també l'origen de graella.
6. Aplica Domini **una sola vegada**, amb Calculadora ràster, i desa `suma-C-mdt.tif`:

```text
"Domini@1" * "Suma C crua@1"
```

Carrega la suma crua amb el nom **Suma C crua** abans d'utilitzar l'expressió. No incloguis al selector l'MDT, l'MDS, Domini, sumes anteriors o els cinc TIFF de prova juntament amb els 37 definitius. **Fusionar / Merge** construeix un mosaic; no és la suma cel·la a cel·la de les conques superposades.

| Comprovació amb les mateixes dades i paràmetres | Cinc punts de prova | 37 posicions |
| --- | ---: | ---: |
| Màxim teòric de la suma | 5 | 37 |
| Màxim observat de referència | 4 | 33 |
| Cel·les amb alguna visió, dins de Domini | 1.307.684 | 1.461.016 |

Table: Controls de l'acumulació; els cinc punts són C05, C11, C13, C25 i C37.

Per al percentatge complet, utilitza una única expressió `100 * "Suma C MDT@1" / 37`, amb el nom de capa **Suma C MDT**. Per a la prova, el denominador seria 5. El denominador sempre identifica el conjunt que has sumat.

![Suma de posicions amb visió: màxim possible 37 i observat 33.](captures/visibilitat-costa-acumulada.png){width=100% height=380pt}

El control té **1.461.016 cel·les** amb alguna visió i màxim **33**. Un valor 12 representa **1.184,52 m** i **32,43%** del recorregut mostrejat. No sumes les hectàrees de les 37 conques.

## Carretera des d'on es veu T

Mostreja la conca T als punts C. Amb MDT, 34/37 són visibles: **3.356,14 m**, el **91,89%**. Amb MDS, 9 posicions queden sota la superfície opaca i es conserven com no calculades.

Per MDS, després del mostreig amb prefix `T_mds_`, crea un camp amb:

```text
CASE WHEN "calculable" = 1 THEN "T_mds_1" ELSE NULL END
```

Les 28 posicions compatibles representen **2.763,88 m**, el **75,68%** de cobertura. Entre elles, 7 són visibles i 21 ocultes: **690,97 m**, el **25% del subconjunt**, no el 25% de tota la carretera. Per al contrast MDT/MDS usa les mateixes 28 posicions; la suma MDT de 37 és un altre resultat.

### Lot MDS dels 28 observadors compatibles

Per acumular conques de carretera sobre MDS, els ulls han de continuar a la mateixa cota absoluta **MDT +1,7 m**. El camp `h_mds_m` de C ja conserva aquesta altura relativa; **no copiïs 1,7 a tota aquesta columna**. Exclou les nou posicions amb `calculable=0`: C01, C06, C07, C09, C16, C19, C29, C33 i C34.

1. Obre un lot nou de Viewshed. A **Observer location → Add Values by Expression**, introdueix:

```text
aggregate(
  layer := 'C', aggregate := 'array_agg',
  expression := to_string("x") || ',' || to_string("y")
                || ' [EPSG:25831]',
  filter := "calculable" = 1,
  order_by := "id"
)
```

2. Retira la fila inicial buida, si s'ha conservat, i comprova **28 execucions**. A **Observer height → Calculate by Expression**, calcula un escalar per fila amb el mateix filtre i ordre:

```text
array_get(
  aggregate(
    layer := 'C', aggregate := 'array_agg',
    expression := "h_mds_m", filter := "calculable" = 1,
    order_by := "id"
  ),
  @row_number
)
```

3. Copia cap avall només les constants: entrada **MDS**, banda 1, altura de destinació 0, abast 0. A la columna avançada, **substitueix** les opcions binàries per `-om DEM -cc 0.85714 -a_nodata -9999`. Aquest mode produeix cota mínima absoluta, en Float64, amb NoData −9999; encara no és una resposta 0/1.
4. Crea `sandbox/cotes-minimes-carretera-mds/`. A **Sortida → Calculate by Expression**, utilitza:

```text
@project_folder || '/cotes-minimes-carretera-mds/' ||
array_get(
  aggregate(
    layer := 'C', aggregate := 'array_agg', expression := "id",
    filter := "calculable" = 1, order_by := "id"
  ),
  @row_number
) || '-min-mds.tif'
```

5. Comprova la correspondència coordenada–altura–nom a la primera i última fila i en una d'intermèdia. Executa el lot i conserva els 28 TIFF de cota mínima.
6. Per convertir-los en binaris sense obrir 28 calculadores individuals, obre **Calculadora ràster de GDAL**, `gdal:rastercalculator`, **com a lot**. A **Input layer C**, utilitza **Autofill → Add Files by Pattern…** amb `*.tif` i la carpeta anterior. Comprova 28 execucions sense fila buida.
7. Emplena la primera fila i copia les constants: **Input A = MDT**, **Input B = Domini**, bandes A/B/C =1, fórmula **`B * ((A + 1.7) >= C)`**, **Set output NoData value =255** i **Output raster type = Byte**. Aquí A/B/C són les entrades de la calculadora, no els noms dels grups de mostres. El NoData de les entrades es conserva com a NoData a la sortida.
8. Crea una carpeta de binaris nova. Tria el primer nom de sortida amb **… → Select File/Folder… → Fill with numbers** per obtenir 28 noms diferents. Conserva el fitxer `.batch` per relacionar cada binari amb el seu TIFF de cota mínima. Executa.
9. Obre **Estadístiques de cel·la** normalment i suma aquests **28 binaris** d'una vegada: Suma, Ignora NoData desactivat, referència del mateix conjunt i NoData de sortida 255. Divideix la suma per **28**, no per 37, per obtenir el percentatge del subconjunt comparable.

Per comparar amb MDT, acumula també només els **28 TIFF MDT amb aquests mateixos identificadors**, retirant les nou posicions excloses. Mantén aquest resultat separat de la suma completa de 37. No hi afegeixis els TIFF de cota mínima: metres d'altitud i respostes binàries no es poden sumar com si fossin la mateixa magnitud.

**Conserva:** mostres, suma, percentatge i taula de cobertura. Distingisca territori visible des de la carretera i carretera des d'on es veu T.

# C. Alguna part del recinte petroquímic

La font és el polígon MCSC 2024 **1459998**, categoria **347**, de **162,59 ha**, amb 19 forats. El sector pertany al Polígon Sud, a la Canonja; no representa tot el complex petroquímic de Tarragona ni la refineria del Polígon Nord.

1. Sobre `coberta_original`, executa `native:buffer`: **+150 m**, 32 segments per quadrant, unions arrodonides i dissolució.
2. Sobre l'intermedi anterior, executa un segon buffer **−150 m**, amb els mateixos altres paràmetres.
3. Comprova geometria vàlida, **222,94 ha** i cap forat. Dona-li el nom **Recinte petroquímic d'estudi** i contrasta'l amb l'ortofoto.

![Primer buffer positiu sobre la coberta original.](captures/visibilitat-costa-buffer-positiu.png){width=95% height=380pt}

![Buffer negatiu sobre l'intermedi positiu, no sobre l'original.](captures/visibilitat-costa-perimetre.png){width=95% height=380pt}

| Distància +n/−n | Àrea | Forats | Afegit exterior |
| --- | ---: | ---: | ---: |
| 50 m | 181,33 ha | 5 | 4,85 ha |
| 100 m | 199,97 ha | 2 | 15,52 ha |
| 150 m | 222,94 ha | 0 | 38,50 ha |
| 250 m | 224,49 ha | 0 | 40,04 ha |

Table: Alternatives de tancament amb els mateixos paràmetres d'arcs.

Les dues operacions no es cancel·len necessàriament: els entrants estrets poden desaparèixer. El recinte de 150 m incorpora 38,50 ha fora del contorn original; la discretització retira també uns 3,77 m² de vora. És una delimitació d'estudi, no un límit oficial nou.

## Mostrejar i comparar cotes

1. Crea una graella rectangular de **250 ×250 m**: X 345250–350000, Y 4551750–4552750, EPSG:25831.
2. Retalla-la amb el recinte i calcula `$area` amb NONE en un camp decimal **`area_m2`**. Després obtín **un punt per fragment** amb `native:pointonsurface`, conservant aquest camp d'àrea.
3. Comprova **57 fragments** i una suma aproximada de **2.229.408,74 m²**. Els pesos corresponen als fragments, no a quadrats complets.
4. A la capa de punts, executa **Afegeix un camp autoincremental**, `native:addautoincrementalfield`: nom `n_lot`, inici 1 i ordenació per l'identificador de la graella. Desa el resultat i anomena'l **A**. Amb Calculadora de camps, crea `id_lot` de text amb `'A' || lpad(to_string("n_lot"), 2, '0')`: A01–A57. Conserva en un camp decimal `pes` l'àrea del fragment del qual prové el punt; si el camp heretat es diu `area_m2`, utilitza `"area_m2"`. No calculis l'àrea de la geometria de punt, que seria zero.
5. Crea camps decimals `x` i `y` per a les coordenades de càlcul als centres de cel·la. Utilitza, respectivament, les expressions següents:

```text
342000 + (floor((x($geometry) - 342000) / 5) + 0.5) * 5
4559000 - (floor((4559000 - y($geometry)) / 5) + 0.5) * 5
```

6. Amb **Mostreja els valors ràster**, mostreja MDT i MDS als punts, amb prefixos `MDT_` i `MDS_`. A la capa final A, crea `h_mdt_m` amb `"MDS_1" + 1 - "MDT_1"` i `h_mds_m` amb 1. La mostra se situa **1 m sobre l'MDS local**; els dos camps mantenen la mateixa cota absoluta en canviar de superfície. Comprova que no hi ha elevacions nul·les als 57 punts i conserva `id_lot`, `x`, `y` i `pes` en les sortides successives. Reserva el nom **A** per a aquesta capa final; reanomena els intermedis per evitar noms duplicats.

![Configuració d'una graella de 250 × 250 m abans de retallar-la amb el recinte petroquímic d'estudi.](captures/visibilitat-costa-area.png){width=95% height=380pt}

### Autocompletar les 57 conques MDT de l'àrea

Obre un lot nou de Viewshed. La pauta és la mateixa de la carretera, però ara **varien les altures** i cada mostra té un pes d'àrea.

1. A **Observer location → Add Values by Expression**, introdueix:

```text
aggregate(
  layer := 'A', aggregate := 'array_agg',
  expression := to_string("x") || ',' || to_string("y")
                || ' [EPSG:25831]',
  order_by := "id_lot"
)
```

2. Retira la fila inicial buida si ha quedat i comprova **57 execucions**. A **Observer height → Calculate by Expression**, utilitza:

```text
array_get(
  aggregate(
    layer := 'A', aggregate := 'array_agg',
    expression := "h_mdt_m", order_by := "id_lot"
  ),
  @row_number
)
```

3. Copia les constants amb Fill Down: MDT/banda 1, destinació 1,7 m, abast 0 i opcions `-vv 1 -iv 0 -ov 255 -a_nodata 255 -cc 0.85714`. No copiïs cap avall la columna d'altura variable.
4. Crea `sandbox/conques-area-mdt/`. A **Sortida → Calculate by Expression**, introdueix:

```text
@project_folder || '/conques-area-mdt/conca-' ||
array_get(
  aggregate(
    layer := 'A', aggregate := 'array_agg',
    expression := "id_lot", order_by := "id_lot"
  ),
  @row_number
) || '-mdt.tif'
```

5. Comprova **el mateix ordre `id_lot` a coordenades, altures i sortides**. Executa i suma els 57 TIFF amb una sola execució d'Estadístiques de cel·la: Suma, Ignora NoData desactivat, referència del conjunt i NoData 255. Aplica Domini una vegada; anomena el resultat **Nombre A**. Compta mostres visibles, no metres quadrats.

Per a **MDS**, prepara un altre lot de 57 punts amb les mateixes coordenades. Ara l'altura d'origen és 1 m, la destinació 0 i les opcions són `-om DEM -cc 0.85714 -a_nodata -9999`. Canvia també la carpeta i el sufix de les sortides perquè siguin cotes mínimes MDS. Converteix-les a 57 binaris amb el lot de Calculadora ràster de GDAL explicat per a la carretera: A=MDT, B=Domini, C=cota mínima, fórmula `B * ((A + 1.7) >= C)`, Byte i NoData 255. Suma **els binaris**, no les cotes mínimes, per obtenir Nombre A sobre MDS.

### Ponderar les conques sense sumar 57 termes a mà

Nombre A dona el mateix valor a un fragment petit i a un de gran. Per acumular la superfície representada cal multiplicar cada conca pel **seu propi `pes`**, abans de sumar-les. Farem la multiplicació amb un lot i la suma amb una sola operació.

1. Obre **Calculadora ràster de GDAL** com a lot. A **Input layer A → Add Files by Pattern**, afegeix els 57 TIFF binaris de `conques-area-mdt/`. Comprova 57 execucions sense fila buida. Per fixar-ne l'ordre, a **Input layer A → Calculate by Expression** utilitza la mateixa expressió de rutes del lot anterior, la que construeix `conques-area-mdt/conca-A01-mdt.tif` a `conca-A57-mdt.tif`.
2. Bandes A/B=1 i entrada B=Domini. A la columna **Formula → Calculate by Expression**, introdueix:

```text
'A * B * ' || to_string(
  array_get(
    aggregate(
      layer := 'A', aggregate := 'array_agg',
      expression := "pes", order_by := "id_lot"
    ),
    @row_number
  )
)
```

La fórmula de cada fila quedarà com `A * B * valor_del_pes`. No hi enganxis l'array sencer ni escriguis la mateixa àrea per a tots els punts. Utilitza els pesos de les dades, sense arrodonir-los abans d'acumular; les taules de lectura sí que poden mostrar-los arrodonits.

3. Copia les constants: **Output raster type = Float32** i **Set output NoData value = −9999**. No utilitzis Byte: els pesos d'àrea poden superar 255. Crea `sandbox/pesos-area-mdt/` i calcula les sortides amb:

```text
@project_folder || '/pesos-area-mdt/pes-' ||
array_get(
  aggregate(
    layer := 'A', aggregate := 'array_agg',
    expression := "id_lot", order_by := "id_lot"
  ),
  @row_number
) || '-mdt.tif'
```

4. Revisa la correspondència **fitxer–pes–sortida** i executa. Cada ràster conté 0 si la mostra és oculta o el seu pes en m² si és visible, amb NoData separat.
5. Obre **Estadístiques de cel·la** normalment. Selecciona només els 57 TIFF de `pesos-area-mdt/`, tria Suma, Ignora NoData desactivat, referència del conjunt i **NoData de sortida −9999**. Desa la capa **Àrea A visible**: és superfície representada, no un recompte de punts.
6. Per al percentatge, obtén la suma exacta de `pes` amb el panell Estadístiques o l'expressió `aggregate('A','sum',"pes")`; és aproximadament 2.229.408,74 m² en el cas de referència. A Calculadora ràster, calcula `100 * "Àrea A visible@1" / suma_exacta_de_pesos`, substituint el denominador per la xifra obtinguda. No divideixis per 57 ni sumis les hectàrees dels mapes individuals.

Per a MDS, repeteix el lot de ponderació amb **els binaris MDS**, les rutes de les seves entrades i carpetes de sortida diferents. Conserva el mateix ordre `id_lot`, els mateixos pesos, Float32 i NoData −9999. Les cotes mínimes són intermedis d'altitud: no són les entrades d'aquesta ponderació.

## Afegir T i interpretar els pesos

La suma de les 57 respostes A compta mostres visibles. Per preguntar si es veu **alguna part**, afegeix la torxa singular T, que una graella pot passar per alt:

```text
("Nombre A@1" > 0) OR ("Torxa T@1" = 1)
```

Control MDS: **470.444 cel·les**, **13,48%** del domini. MDT: **2.977.704**, **85,31%**. Conserva NoData.

![Mapa que inclou alguna mostra d'àrea o la torxa T.](captures/visibilitat-costa-poligon.png){width=100% height=380pt}

La fracció d'àrea és $100\sum_i w_iV_i/\sum_iw_i$, amb pesos en m². **T no rep un pes superficial inventat**. Als receptors, R1 dona T=1, alguna part=1 i A=0% amb MDS: es veu la torxa però cap de les 57 mostres d'àrea.

**Conserva:** fragments, mostres, pesos, recompte, mapa d'alguna part i percentatge ponderat. La conclusió ha d'identificar què es veu, des d'on, altures, superfície i cobertura de dades.

# Ampliacions, preguntes obertes i aplicacions

Escull una pregunta que vagi més enllà de repetir el recorregut seleccionat. Mantén una referència, registra els paràmetres i explica què canvia. No cal fer totes les propostes:

- **Altures i receptors.** Compara altres altures de model o receptors adequats. En quin cas canvia la resposta visible/ocult? Declara la cota absoluta de cada extrem per no confondre un canvi de superfície amb un canvi de receptor.
- **Densitat del mostreig.** Repeteix un recorregut amb més o menys posicions, o desplaça la graella de l'àrea. Es mantenen els llocs destacats? Compara pesos i cobertura, no només el nombre de mostres visibles.
- **Delimitació i objectius.** Prova altres distàncies de tancament +n/−n o compara objectius singulars i d'àrea. Quina superfície s'afegeix? Pot una graella ometre una estructura alta com T?
- **Un altre lloc.** D'acord amb el professor, aplica el mètode a un mirador, un itinerari o un altre objectiu amb elevacions adequades. Recalcula altures, domini i controls; els percentatges del cas de la Canonja no són valors esperats per al nou lloc.

Una aplicació geogràfica pot ser comparar visió geomètrica des d'un itinerari o ajudar a seleccionar punts per a una observació de paisatge. Què caldria observar al camp? Quines dades permetrien relacionar la visió amb usos, freqüentació o percepció? Explica què aporta el càlcul i què falta per estudiar exposició o impacte, sense atribuir-los directament a la conca visual.

Les repeticions han de respondre una pregunta de sensibilitat. Canvia un paràmetre cada vegada, mantén la resta i conserva també resultats que no confirmin la primera idea.

# Preparar l'informe

Organitza el PDF perquè cada resultat respongui una pregunta:

1. **Pregunta i selecció de classe.** Situa l'objectiu, els receptors i els apartats obligatoris anunciats pel professor. Identifica l'ampliació, si en fas una.
2. **Dades i decisions.** Explica MDT/MDS, dates, resolució, altures absolutes i relatives, domini i mostreig. Justifica la delimitació d'estudi quan sigui pertinent.
3. **Procediment i controls.** Mostra els paràmetres que condicionen les conques, el lot, la màscara i l'acumulació dels apartats seleccionats. Distingueix una execució individual del conjunt de repeticions.
4. **Resultats comparables.** Inclou mapes amb llegenda i el mateix enquadrament, i una taula amb unitats, cobertura i denominadors. Separa visible, ocult i no calculat.
5. **Interpretació i límits.** Explica què es veu i des d'on, i diferencia resposta binària, recompte i fracció ponderada. Identifica què no informa sobre persones o impacte paisatgístic.
6. **Ampliació i aplicació.** Compara les repeticions amb la referència i proposa una aplicació geogràfica o una observació que permeti contrastar-la.

## Enregistrar la pantalla i extreure captures

Pots enregistrar fragments de la sessió amb un enregistrador de pantalla, com OBS Studio. Fes una prova breu amb la finestra de QGIS i comprova que es llegeixen altures, coordenades i opcions. Documenta una configuració individual, la preparació del lot i els controls que corresponguin a la selecció de classe; anota els moments útils del vídeo.

Després, pausa'l en un reproductor i desa els fotogrames amb la funció de captura de fotograma. Retalla només les zones irrellevants, conserva el context dels paràmetres i afegeix número i peu explicatiu. Exporta els mapes finals amb llegenda, escala i unitats. Una captura d'un diàleg mostra la configuració; una de mapa mostra la representació. Relaciona-les amb controls numèrics del resultat.

No cal lliurar el vídeo tret que el professor ho indiqui. Selecciona les evidències que ajudin a seguir el raonament; l'informe no necessita tots els fotogrames ni una explicació de cada clic.

# Lliurament, fonts i portabilitat

Prepara `dist/` només amb els apartats seleccionats a classe:

1. Crea-hi un **GeoPackage nou** amb els vectors lliurats: punts, receptors, mostres, recinte o fragments necessaris per als resultats i les comprovacions. Utilitza **Exporta → Desa els objectes com a…** i noms de capa diferents dins del mateix fitxer, sense sobreescriure'l complet. Conserva identificadors, cotes, altures i pesos que expliquen els càlculs.
2. Copia a `dist/rasters/` els GeoTIFF necessaris per representar i revisar la selecció: conques emmascarades, sumes, percentatges o cotes mínimes quan els controls demanats les necessitin. Afegeix el domini i el context local utilitzats. Els lots de prova, les alternatives descartades i els fitxers no utilitzats es queden a `sandbox/`; no s'adjunten automàticament totes les conques individuals.
3. Desa el projecte final com a `.qgz` **extern al GeoPackage** dins de `dist/`, amb rutes relatives. Carrega les capes dels fitxers finals i retira del projecte les referències a `data/` i `sandbox/`. Comprova estils, etiquetes i ordre de dibuix. Conserva `fonts/` si cal la font tipogràfica i instal·la la còpia inclosa si QGIS no la troba. Si mantens el WMS opcional, copia també el seu XML; el context local ha de permetre la revisió offline.
4. Desa l'informe PDF. Si has utilitzat lots, incorpora les configuracions `.batch`, les expressions i els registres a `evidencies/`, amb una nota que relacioni les rutes de l'execució i els resultats lliurats. Conserva l'original com a traça; una còpia preparada per reexecutar ha d'estar identificada i tenir les rutes revisades.
5. Identifica carpeta/ZIP i fitxers principals amb codi, tema i cognoms. En aquest patró, **`prN` es reemplaça pel codi real de la tasca de Moodle**:

```filetree
prN-intervisibilitat-cognoms.gpkg
prN-intervisibilitat-cognoms.qgz
prN-intervisibilitat-cognoms.pdf
rasters/
evidencies/
```

Reanomena la carpeta final amb el mateix prefix i/o comprimeix-la. Obre la còpia traslladada o el ZIP extret en una carpeta nova, sense connexió. Comprova capes vàlides, dades, estils, etiquetes, fonts tipogràfiques i ordre; totes les dependències del QGZ han de ser dins de la còpia. Revisa separadament les rutes del `.batch`: una configuració d'execució no es repara movent el projecte ni canviant-lo de nom.

El **70%** correspon als apartats obligatoris que indicarà el professor. Les ampliacions permeten aspirar a l'excel·lent segons els criteris comunicats a classe i recollits a Moodle; no substitueixen els obligatoris ni garanteixen una nota per haver-les intentat. En una zona alternativa, identifica el cas al nom dels fitxers i conserva les fonts i els controls propis.

- [ICGC, elevacions](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions): LiDAR 2021–2023, MDT 5 m i MDS 1 m agregat pel màxim.
- [Mapa de cobertes ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Mapes/Mapa-de-cobertes-del-sol-de-Catalunya), edició 2024, i [RTT](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial), edició 2024.
- Ortofoto ICGC 2025 i [condicions d'ús](https://www.icgc.cat/condicions).
- [OpenStreetMap](https://www.openstreetmap.org/copyright): node de torxa 7682543312, versió 1.
- [QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/), [processament per lots](https://docs.qgis.org/3.44/en/docs/user_manual/processing/batch.html) i [GDAL Viewshed](https://gdal.org/en/stable/programs/gdal_viewshed.html).
- Farnós Marsal, J. (2025). [La indústria petroquímica de Tarragona](https://publicacions.iec.cat/repository/pdf/00000528/00000061.pdf): polígons Nord/Sud, port i conduccions.

El GeoPackage inicial prepara entrades locals; les sortides de l'activitat s'han de calcular. La selecció de `dist/` ha de ser autònoma respecte de les proves conservades a `sandbox/`. Una visió calculada no substitueix observacions de camp ni un estudi de percepció o impacte.
