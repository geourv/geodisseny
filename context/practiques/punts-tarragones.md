---
title: "Distribucions puntuals del Tarragonès"
subtitle: "Centres, dispersió, recomptes i densitat amb QGIS"
author: Benito Zaragozí
lang: ca
date: "Preparació: 4 d'octubre de 2026"
content_status: draft
---

# Preguntes i dades de treball

On s'equilibren els registres d'autoconsum? Què canvia si cadascun contribueix segons la seva potència? Com es distingeixen una distribució extensa, una banda i diverses concentracions locals? Els exercicis comparteixen dades perquè es pugui interpretar què canvia en cada resum.

Els punts de l'ICAEN representen **consumidors elèctrics associats**, no necessàriament la petjada física dels panells. La potència en kW és capacitat registrada; no és energia produïda en kWh. L'extracció és del 28 de setembre de 2026, però la revisió de les metadades és de 30 de juny de 2024: la data efectiva del conjunt no s'ha pogut verificar.

## Organització del paquet

- `dades.gpkg`: registre complet del Tarragonès, selecció amb potència coneguda, límit comarcal i seccions censals.
- `resultats.gpkg`: centres, paràmetres de dispersió, cercle, el·lipse, graella, recomptes i agregació per seccions.
- `kernel-…-raw.tif`: sortides crues; `densitat-….tif`: conversió a registres/km² o kW coneguts/km². Els QML fixen la simbologia.
- `projectes/`: sis projectes amb camins relatius; obre el que correspon a la fase que vulguis consultar.
- `fonts/`: còpies de les entrades conservades. Les dades cadastrals de les seccions ja estan agregades; aquest paquet no refà la preparació dels edificis originals.
- `captures/`, `controls/` i `reproduccio/`: figures, resultats de contrast i fonts de la preparació.

| Projecte | Vista |
| --- | --- |
| `01-inventari.qgz` | Inventari complet i límit |
| `02-centres.qgz` | Tres centres estadístics i centroide |
| `03-dispersio.qgz` | Cercle i el·lipse sobre els punts |
| `04-recompte.qgz` | Graella d'1 km² |
| `05-kernel.qgz` | Densitat de radi 1.500 m |
| `06-seccions.qgz` | Potència coneguda per 100 edificis |

## Sessió i connexions

1. Descomprimeix tot el paquet i crea una carpeta `treball`. Utilitza QGIS 3.44 amb Processament. La versió exacta dels controls és als registres del paquet.
2. Crea un projecte nou amb **EPSG:25831** i el·lipsoide **Cap/Planimètric**. Desa'l a `treball/practica.qgz`, amb camins relatius.
3. Al panell Explorador, fes clic dret a **GeoPackage → Connexió nova**. Selecciona `dades.gpkg`; repeteix-ho amb `resultats.gpkg`.
4. Desplega els fitxers per comprovar-ne les capes. Refresca l'Explorador si no apareix una capa acabada de desar. La connexió pertany al perfil de QGIS; en un altre ordinador cal crear-la de nou.
5. Afegeix `tarragones` i `registre_icaen`. Conserva les sortides pròpies a `treball/treball.gpkg`, no sobre les dades de referència.

![L'Explorador mostra el fitxer i les capes; el panell Capes mostra les que s'han carregat al projecte.](captures/punts-dades.png){width=90%}

# Cobertura, absències i selecció

Obre la taula de `registre_icaen` i comprova aquests controls. Un valor absent de potència no s'ha de substituir per zero. Les coordenades coincidents tampoc justifiquen eliminar registres sense estudiar-ne els identificadors.

| Control del Tarragonès | Valor |
| --- | ---: |
| Registres | 5.102 |
| Potència coneguda positiva | 3.762 |
| Potència absent | 1.340 |
| Suma de potències conegudes | 36.633 kW |
| Categoria Edifici / Terra | 5.096 / 6 |
| Registres addicionals respecte de posicions diferents | 528 |

1. Fes clic dret a la capa i obre **Filtre**. Escriu `"POT_KW" > 0`.
2. Comprova els 3.762 registres i exporta la capa filtrada al fitxer de treball, amb nom `icaen_coneguda`.
3. Anomena-la **ICAEN coneguda** al panell Capes. Les expressions de la guia utilitzen exactament aquest nom.
4. Conserva una capa del conjunt complet sense filtre, amb un altre nom. Un filtre de capa i una selecció d'objectes són mecanismes diferents: els diàlegs següents no utilitzen «Només objectes seleccionats».

**Resultat conservable:** taula de controls, capa filtrada i nota sobre què representen la coordenada i la potència.

# Centres de la distribució

Quatre punts ficticis a (0,0), (4,0), (0,4) i (4,4) km tenen potències 10, 10, 20 i 60 kW. El centre sense pes és (2,2) km. Els productes potència×coordenada sumen 280 i 320 kW·km; dividir per 100 kW dona el centre ponderat (2,8;3,2) km. És una posició d'equilibri, no una instal·lació ni una ubicació recomanada.

## Accés i paràmetres

Obre **Vectorial → Analysis Tools → Coordenades mitjanes**. També es troba a la Caixa d'eines, dins d'**Anàlisi vectorial**; l'identificador és `native:meancoordinates`.

![Accés a Coordenades mitjanes des del menú Vectorial.](captures/punts-centres-menu.png){width=95%}

![La caixa oberta mostra la mateixa eina dins d'Anàlisi vectorial.](captures/punts-centres-caixa.png){width=78%}

1. Entrada: **ICAEN coneguda**. Deixa buits el pes i el camp ID únic. Executa i desa `centre_mitja` al GeoPackage de treball.
2. Repeteix amb **POT_KW** com a pes i ID buit. Desa `centre_ponderat`.
3. Sobre el conjunt complet sense filtre, calcula un tercer centre sense pes i desa `centre_total`.
4. Executa **Centroides** (`native:centroids`) sobre el polígon `tarragones` i desa `centroide`. No utilitzis els punts ICAEN com a entrada d'aquesta operació.

![El pes canvia la contribució; l'ID buit conserva un únic grup.](captures/punts-centres-parametres.png){width=90%}

Comprova que cada sortida contingui un punt. Un camp municipal com a ID donaria un centre per municipi; un ID únic per registre impediria resumir el conjunt.

## Coordenades i interpretació

| Resum | Est, m | Nord, m |
| --- | ---: | ---: |
| Conjunt complet, sense pes | 357272,52 | 4556675,78 |
| Selecció coneguda, sense pes | 357387,97 | 4556891,17 |
| Selecció coneguda, ponderada | 354528,52 | 4556391,87 |

![Centres i centroide comarcal: les posicions responen a preguntes diferents.](captures/punts-centres-resultat.png){width=100%}

La ponderació desplaça el centre uns **2.903 m** cap a l'oest i lleugerament al sud. La diferència entre els dos centres sense pes, en canvi, prové de la selecció per disponibilitat de potència. Els decimals serveixen per contrastar càlculs, no acrediten precisió centimètrica de les dades.

**Resultat conservable:** mapa amb llegenda, taula de coordenades i explicació separada dels efectes de selecció i ponderació.

# Dispersió i orientació

La distància estàndard resumeix la separació respecte del centre amb un radi. L'el·lipse distingeix l'eix de màxima dispersió i el perpendicular. S'utilitza la convenció descriptiva amb divisor n i semieixos d'una desviació; el contorn no garanteix contenir el 68% dels punts.

## Camps del centre

Copia `centre_mitja` com a `centre_dispersio`. Obre'n la taula i crea camps decimals amb la Calculadora de camps, en l'ordre següent. Mantén **ICAEN coneguda** carregada i amb els mateixos 3.762 punts.

Camp `Sxx`:

```text
with_variable('cx', x($geometry),
  aggregate('ICAEN coneguda', 'mean',
    (x($geometry)-@cx)^2))
```

Camp `Syy`:

```text
with_variable('cy', y($geometry),
  aggregate('ICAEN coneguda', 'mean',
    (y($geometry)-@cy)^2))
```

Camp `Sxy`:

```text
with_variable('cx', x($geometry),
  with_variable('cy', y($geometry),
    aggregate('ICAEN coneguda', 'mean',
      (x($geometry)-@cx)*(y($geometry)-@cy))))
```

Els camps de dispersió següents es calculen a partir d'aquestes tres quantitats. Les primeres tenen unitats m²; radi i semieixos tornen a tenir unitats m.

| Camp | Expressió |
| --- | --- |
| `D_m` | `sqrt("Sxx" + "Syy")` |
| `delta` | `sqrt(("Sxx" - "Syy")^2 + 4 * "Sxy"^2)` |
| `a_m` | `sqrt(("Sxx" + "Syy" + "delta") / 2)` |
| `b_m` | `sqrt(("Sxx" + "Syy" - "delta") / 2)` |
| `azimut` | `90 - degrees(atan2(2 * "Sxy", "Sxx" - "Syy")) / 2` |

Controls: `Sxx`=63847660,549470; `Syy`=11811095,805279; `Sxy`=11942063,437619; `D_m`=8698,204203; `a_m`=8152,141105; `b_m`=3033,373000; `azimut`=77,672737° horaris des del nord.

## Polígons de resum

1. Cerca **Geometria segons l'expressió** (`native:geometrybyexpression`). Entrada: el centre amb els camps; sortida: **Polígon**; Z i M desactivades.
2. Per al cercle, aplica `make_circle($geometry, "D_m", 72)`.
3. Per a l'el·lipse, aplica `make_ellipse($geometry, "a_m", "b_m", "azimut", 72)`.
4. Desa les dues sortides i dibuixa-les sense emplenament sobre els punts. Contrasta-les amb les capes homònimes de `resultats.gpkg`.

![L'expressió utilitza els atributs del centre per dibuixar una el·lipse.](captures/punts-dispersio-parametres.png){width=90%}

![Cercle i el·lipse resumeixen propietats diferents de la mateixa selecció.](captures/punts-dispersio-resultat.png){width=100%}

Per ponderar la dispersió, parteix del centre ponderat i substitueix les mitjanes per sumes de `POT_KW` multiplicat per cada quadrat o producte, dividides per la suma de potències. No reutilitzis el centre sense pes amb una covariància ponderada.

**Resultat conservable:** taula de variàncies, radi, semieixos i angle; mapa que conservi els punts; explicació de per què l'eix no indica moviment ni creixement temporal.

# Graella, recompte i potència

Una cel·la d'1 km de costat té 1 km². El recompte de registres coincideix numèricament amb registres/km², però una suma de potències s'expressa en kW/km². Si es retalla la cel·la per la costa, cal tornar a calcular-ne la superfície.

1. Obre **Crea una malla** (`native:creategrid`), tipus **Rectangle (Polígon)**.
2. Extensió: `340000,374000,4546000,4566000`, en EPSG:25831. Espaiats: **1000 m** en tots dos eixos. Superposicions: **0**. Desa `graella`.
3. Comprova **680 polígons** i àrea plana d'1.000.000 m² per polígon.

![La malla fixa extensió, espaiats i CRS.](captures/punts-graella-parametres.png){width=90%}

4. Obre **Compta els punts al polígon** (`native:countpointsinpolygon`). Polígons: graella; punts: **ICAEN coneguda**; pes i classe: buits; camp: `n_punts`. Desa `recompte`.
5. Repeteix utilitzant la sortida anterior com a polígons per conservar el primer camp. Pes: **POT_KW**; camp: `kw_coneguts`. Desa una capa diferent, `recompte_potencia`.
6. Comprova sumes de **3.762** i **36.633**. Si no coincideixen, revisa entrada, filtre, extensió i possibles punts sobre vores compartides abans d'interpretar el mapa.

![El pes buit produeix un recompte; un camp de pes produeix la suma d'aquell atribut.](captures/punts-recompte-parametres.png){width=90%}

![La graella representa variació local sense moure els punts.](captures/punts-recompte-resultat.png){width=100%}

**Resultat conservable:** dos mapes sobre els mateixos polígons i una comparació de quadrats amb molts registres i amb molta potència. Un zero és absència de registres de la selecció, no absència de qualsevol fenomen energètic.

# Densitat kernel

Un kernel reparteix la contribució de cada punt dins d'un entorn. El radi controla la suavització; el píxel controla la discretització de la sortida. S'utilitza un kernel quartic, diferent del gaussià de l'exemple conceptual del manual.

## Sortides crues

1. Obre **Mapa de calor (KDE, estimació de densitat de nuclis)**, identificador `qgis:heatmapkerneldensityestimation`.
2. Entrada: **ICAEN coneguda**; radi: **1500 m**; píxel X i Y: **100 m**.
3. A **Advanced Parameters**, tria kernel **Quartic** i sortida **Raw**. Deixa buits radi variable i pes. Desa `kernel-punts-1500-raw.tif`.
4. Repeteix amb radi **500 m** i un altre fitxer.
5. Repeteix les dues operacions amb pes **POT_KW** i noms `kernel-kw-…-raw.tif`.

![Radi i píxel tenen funcions diferents; els paràmetres avançats permeten triar kernel i ponderació.](captures/punts-kernel-parametres.png){width=90%}

## Normalització i representació

La contribució quartic crua integra un volum de πh²/3. Per obtenir quantitat per km², multiplica per `3 * 1000000 / (pi * h^2)`. A la Calculadora ràster, per a 1500 m:

```text
"kernel-punts-1500-raw@1" * 3 * 1000000
  / (3.141592653589793 * 1500^2)
```

Utilitza l'extensió, el CRS i les dimensions de la capa crua corresponent, sense retallar-la encara. Desa `densitat-punts-1500.tif`. Repeteix amb radi 500 m i amb les dues sortides ponderades. Factors: **0,4244131816** per a 1500 m i **3,8197186342** per a 500 m. No apliquis el mateix factor als dos radis.

Conserva NoData; el motor pot deixar-hi les cel·les no visitades per cap kernel. La suma dels valors vàlids multiplicada per 0,01 km² aproxima el total de registres o kW. Les diferències petites provenen de discretització i precisió numèrica. Retallar per la comarca altera la integral i no és una correcció de vora.

![Kernel normalitzat amb llegenda en registres/km².](captures/punts-kernel-resultat.png){width=100%}

Compara radis amb la mateixa escala de colors per a la mateixa unitat. Els QML del paquet comparteixen els límits entre radis; registres/km² i kW/km² tenen escales separades. Un pic no indica significació estadística ni aptitud d'un emplaçament.

**Resultat conservable:** quatre ràsters normalitzats, control de contribució total i explicació dels canvis per radi i per pes.

# Potència coneguda per secció censal

La capa `seccions` conserva els polígons de 2024. `functional_n` és un recompte cadastral ja preparat d'objectes Building en estat funcional; no és nombre d'habitatges. `age_exact_n` i `age_median_exact` resumeixen només els objectes amb any inicial igual al final. Les fonts tenen dates diferents.

1. Carrega `seccions` i una còpia del registre complet. Filtra els punts amb `"UBICACIO" = 'Edifici'`; comprova **5096**.
2. Compta'ls per secció, sense pes, al camp `n_reg`.
3. Afegeix `AND "POT_KW" > 0` al filtre; comprova **3757**. Sobre la sortida de l'operació anterior, obtén `n_coneguts` sense pes.
4. Repeteix sobre aquesta sortida amb pes **POT_KW** i camp `kw_coneguts`. Comprova una suma de **36058 kW** i **151 seccions**.

![POT_KW s'acumula dins dels polígons de secció.](captures/punts-seccions-parametres.png){width=90%}

5. Crea el camp decimal `kw_100ed`:

```sql
CASE
  WHEN "functional_n" > 0
    AND ("n_reg" = 0 OR "n_coneguts" > 0)
  THEN 100.0 * "kw_coneguts" / "functional_n"
END
```

6. Comprova **una secció amb NULL**. Els registres amb totes les potències absents no produeixen un zero conegut. Representa els nuls amb una categoria pròpia.
7. Contrasta els camps amb `seccions_resum` de `resultats.gpkg`, utilitzant `cusec` com a clau, no l'ordre de les files.

![Indicador en kW coneguts per 100 edificis funcionals; els valors absents es distingeixen dels baixos.](captures/punts-seccions-resultat.png){width=100%}

Per a l'ampliació d'antiguitat, selecciona seccions amb `age_exact_n >= 10` i `n_coneguts > 0`: han de ser **126**. Cada observació és una secció, no un edifici. L'associació descriptiva del capítol no prova causalitat.

**Resultat conservable:** agregats per `cusec`, fórmula de l'indicador, mapa amb classe de nuls i nota sobre denominador, dates i cobertura.

# Fonts i reproducció

- [ICAEN: localització de l'autoconsum](https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/): font de l'inventari; extracció 28/09/2026, data efectiva no verificada.
- [ICGC: seccions censals](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Seccions-censals): geometries ICGC/Idescat de l'01/01/2024. [Condicions d'ús de l'ICGC](https://www.icgc.cat/condicions).
- [Cadastre INSPIRE](https://www.catastro.hacienda.gob.es/webinspire/index.html): edificis del feed de 21/08/2026, agregats prèviament; correspondències i controls a `reproduccio/seccions-resultats.json`.
- [Manual QGIS](https://docs.qgis.org/3.44/en/docs/user_manual/): eines, camps i interpretació dels paràmetres.

Els scripts de preparació conserven el procés i esperen l'estructura del repositori geodisseny. Els projectes i els exercicis d'aquesta guia funcionen amb els fitxers del paquet. Les captures mostren diàlegs configurats i resultats representats; els registres documenten per separat els càlculs Processing i els controls independents.
