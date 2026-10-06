---
title: "Constantí: descriure els punts i contrastar les potències"
subtitle: "Guia integrada dels capítols 4 i 5"
author: Benito Zaragozí
lang: ca
content_status: draft
---

# Dades i ordre de treball

La pràctica conserva el mateix territori per entendre què aporta cada operació: **recompte → centres → dispersió → densitat → semblança de potències veïnes**. Els punts ICAEN representen consumidors associats, no petjades de panells. L'extracció és del 28/9/2026, sense haver establert la data efectiva del conjunt. Ortofoto ICGC 2025, límits 20/1/2026; sistema EPSG:25831.

Descomprimeix el paquet complet i crea `treball/`. Conserva les fonts; desa-hi les teves capes i una còpia de cada projecte que modifiquis.

| Projecte | Pregunta |
| --- | --- |
| `01-recompte.qgz` | Quants registres hi ha en cada quadrat? |
| `02-centres.qgz` | On s'equilibren el nombre i els pesos? |
| `03-dispersio.qgz` | Quant s'escampen els punts i en quina direcció? |
| `04-kernel.qgz` | On es concentren les localitzacions segons el radi? |
| `05-moran.qgz` | Les potències de punts pròxims s'assemblen? |

`constanti.gpkg` conté dades i resultats. `renda.gpkg` i `renda.shp` permeten transferir el procediment a polígons. Els projectes tenen camins relatius: copia el paquet complet, no només el QGZ.

## Connexions i controls

1. Obre el projecte corresponent. A l'Explorador, crea connexió GeoPackage a `constanti.gpkg` i desplega'n les capes.
2. `punts`: **124 registres**. `coneguda`: **98**, amb suma **2.770 kW**; els altres 26 tenen interval però no potència numèrica.
3. Els registres coincidents es conserven. En els 98 casos coneguts hi ha 94 posicions diferents.
4. Mantén **EPSG:25831** i el·lipsoide **Cap/Planimètric**. Utilitza els noms de capa indicats a cada procediment.

# Recompte per quadrats

La capa `malla` té 90 quadrats d'1 km de costat, cadascun d'1 km². Obre **Procés → Caixa d'eines → Anàlisi vectorial → Compta els punts al polígon**.

1. Polígons: `malla`. Punts: `punts`. Pes i classe buits.
2. Camp: `n_punts`. Sortida: GeoPackage de treball, capa `recompte`.
3. Comprova 90 files i suma 124. El color de cada quadrat es pot contrastar amb els punts que hi cauen.
4. Repeteix amb `coneguda`, pes `POT_KW` i camp `kw_pub`. La suma és 2.770 kW.

\clearpage

![Eina de recompte i mapa dels mateixos punts de Constantí.](captures/c4-recompte-caixa.png){width=95%}

El quadrat del nucli amb més registres en conté 48 i suma 268 kW publicats. El quadrat de més potència coneguda conté 17 registres i 891 kW. **Més punts i més potència no són la mateixa propietat.** Localitza'ls per les coordenades mínimes del quadrat: 349500/4557000 i 345500/4558000 m.

**Resultat:** capa amb les dues variables, sumes i una lectura dels dos quadrats. Els 26 valors absents no s'han imputat en aquella suma.

# Centres dels registres i dels pesos

`pesos` conserva els 124 punts i `POT_KW`. El camp decimal `w_mid` afegeix una estimació només quan falta la xifra: 2,5; 15; 62,5 kW segons intervals fins a 5, més de 5 fins a 25 i més de 25 fins a 100. Suma 2.970 kW: 2.770 publicats i 200 assignats.

1. Obre **Coordenades mitjanes** a **Vectorial → Analysis Tools**, o a Anàlisi vectorial de la Caixa d'eines.
2. Entrada: `pesos`. Pes i ID únic buits. Desa `centre_registres`.
3. Repeteix amb `w_mid` com a pes, ID buit. Desa `centre_ponderat`.
4. Cada sortida té un punt. Superposa-les amb pesos proporcionals i ortofoto.

\clearpage

![Centres dels registres i ponderat, amb els valors publicats i assignats diferenciats.](captures/c4-centres-resultat.png){width=95%}

El canvi és 1.832 m cap a l'oest i una mica al nord. El registre de 450 kW aporta 15,2% del pes central; els cinc pesos més grans, 37,4%. El centre resumeix un equilibri, no recomana una ubicació.

**Resultat:** dos centres, un mapa amb noms i una explicació del desplaçament, distingint observació i estimació.

# Cercle i el·lipse de dispersió

Obre `03-dispersio.qgz`. Mantén 124 punts, el centre dels registres, cercle, el·lipse, límit i ortofoto. El radi del cercle és 2.000,66 m. Els semieixos de l'el·lipse són 1.934,44 i 510,47 m; les longituds completes són el doble.

Per practicar el dibuix, utilitza `dispersio` com a entrada de **Geometria segons l'expressió**, sortida Polígon. Executa aquestes expressions **separadament**:

```text
make_circle($geometry, "D_m", 72)
make_ellipse($geometry, "a_m", "b_m", "azimut", 72)
```

\clearpage

![Cercle i el·lipse visibles a QGIS sobre els 124 punts i el centre comú.](captures/c4-cercle-ellipse.png){width=95%}

**Resultat:** identifica un punt exterior i un espai interior amb pocs registres. Explica el radi i l'allargament sense donar-los significat de cobertura, percentatge fix o confiança.

# Mapa de calor

Cerca **Mapa de calor** a la Caixa d'eines; és dins d'Interpolació. Entrada: `punts`, radi 500 m, píxel X i Y de 100 m. A Advanced Parameters: Quartic, Raw, pes buit. Desa `kernel-500-raw.tif`. Repeteix amb 1.500 m.

\clearpage

![Mapa de calor localitzat a la Caixa d'eines, sobre el mateix territori.](captures/c4-kernel-caixa.png){width=95%}

El radi decideix fins on contribueixen els punts; el píxel només desa la superfície amb el detall triat. Raw no és directament registres/km². A la Calculadora ràster, la normalització per 500 m és:

```text
"kernel-500-raw@1" * 3 * 1000000 / (3.141592653589793 * 500^2)
```

Canvia banda i radi per 1.500 m. Les capes `densitat-500` i `densitat-1500` del paquet ja estan normalitzades. Aplica la mateixa escala de color; conserva els punts per interpretar les concentracions.

**Resultat:** compara els dos radis amb unitats i selecció declarades. La suma de densitats per 0,01 km² d'àrea de píxel s'aproxima a 124 registres. Un pic de color no és un contrast estadístic.

# Potències veïnes

Obre `05-moran.qgz`. Ara s'utilitzen els 98 punts de `coneguda`, sense cap imputació. Cada observació es relaciona amb els vuit més propers.

- Punt de 450 kW: veïns 100, 100, 60, 30, 100, 20, 60 i 50 kW; suma 520 i mitjana 65 kW.
- Punt de 3 kW del nucli: veïns 4, 4, 3, 10, 3, 3, 3 i 3 kW; suma 33 i mitjana 4,125 kW.
- Mitjana dels 98 valors: 28,2653 kW. Al primer cas, propi i entorn són alts; al segon, baixos.

\clearpage

![450 kW i les vuit potències veïnes. Les línies fan explícita la regla de comparació.](captures/c5-punts-veins.png){width=95%}

**Resultat:** conserva xifres, suma, mitjana i signes respecte de 28,27. No confonguis aquests pesos espacials d'1/8 amb els pesos de potència del centre ponderat.

# Moran i permutacions

La I global en kW és 0,191856. La prova de referència conserva posicions i veïns i barreja les 98 potències 9.999 vegades. Només 3 barreges arriben a aquell valor o el superen; amb correcció d'una unitat, pseudo-p 0,0004. No és una prova sobre aleatorietat de localitzacions ni sobre la causa del patró.

Per al mapa local, prepara Hotspot Analysis 4.0.0 i comprova les importacions al Python de QGIS, seguint el capítol 5. Obre **Hotspot Analysis → LISA → Local Moran's I**.

| Paràmetre | Valor |
| --- | --- |
| Input / Analysis field | `coneguda` / `POT_KW` |
| Weights / K | KNN /8 |
| Distance metric | Euclidean |
| Row standardization | Activat |
| Optimize threshold automatically | Desactivat |
| Random permutations |9999 |
| Two-tailed p-value | Desactivat |
| Output | GeoPackage de treball, capa nova |

`q_value` és el quadrant: 1=HH, 2=LH, 3=LL, 4=HL. No és un ajust FDR. Separa els casos amb `p_value >= 0.05` abans de classificar els quadrants.

\clearpage

![Mapa local amb llegenda completa i registres de 450 i 3 kW identificats.](captures/c5-punts-resultat.png){width=95%}

L'execució conservada té 8 HH, 45 LL, 1 HL, 3 LH i 41 no destacats. El complement no exposa llavor al diàleg, i una nova execució pot canviar casos propers al tall. Guarda els teus camps retornats. Per als dos registres de lectura, el pseudo-p de referència és 0,0244 i 0,0027.

**Resultat:** mapa amb variable, veïnatge, contrast i llegenda, més una conclusió que diferenciï evidència d'associació i explicació causal.

# Transferència a renda i a altres variables

Carrega `renda.shp` sense filtre, mantenint tots els components del fitxer. Té 151 seccions de 2024 i renda neta per persona de 2023. Local Moran's I utilitza `renda`, Queen, pesos binaris, normalització per files i 9.999 permutacions, sense bilateral. La geometria completa decideix els contactes.

La secció 07013 de Tarragona té 23.239 €/persona i veïnes de 24.068, 23.235 i 17.187: mitjana 21.496,67. El cas 08012 té 7.379 i mitjana veïna 10.228,25; Constantí 01002 té 7.744 i 13.453,50. Els seus dos veïns, de 13.262 i 13.645 €/persona, permeten reconstruir aquesta última mitjana.

**Resultat:** valor propi, veïns i lectura del contrast, identificant municipi i codi. Per relacionar renda, edificis i autoconsum es pot reunir informació per secció, però no es disposa d'una unió individual família–edifici–instal·lació. Dates i denominadors continuen condicionant la interpretació.

# Fonts i conservació

ICAEN: [localització d'autoconsum](https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/); ICGC: [condicions d'ús](https://www.icgc.cat/condicions); INE: [renda, taula 31223](https://www.ine.es/jaxiT3/Tabla.htm?t=31223&L=0). La renda usa les seccions ICGC/Idescat de 2024 i la metodologia ADRH de l'INE.

Les captures mostren accés, configuració i resultats calculats amb Processing, sense acreditar un recorregut manual clic a clic. Scripts, controls i manifests conserven la reproducció tècnica. Les dades i els paquets docents no formen part de les descàrregues del web públic.
