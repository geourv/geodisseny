---
title: "Autocorrelació: controls i interpretació"
subtitle: "Notes docents del paquet de 5 d'octubre de 2026"
author: Benito Zaragozí
lang: ca
content_status: draft
---

# Controls del conjunt

- **151 seccions** de 2024; renda neta mitjana per persona de 2023 disponible a totes. Població mínima publicada: 158.
- Unió exacta per `cusec`; els codis 4314809005 i 4314809006 només tenen files buides el 2023 a la taula temporal i no són al seccionat utilitzat.
- **38.689 edificis funcionals**, 13.566.378,2127 m² de petjada; 135 travessen alguna vora de secció. S'assignen sencers pel punt interior, com en el recompte.
- Original cadastral: 40.180 objectes; quatre no s'assignen. Un identificador es reutilitza en dos objectes municipals diferents, no superposats; es conserven qualificats per font.
- Edat: **150 seccions**, exclosa 4314807015 perquè només té set edificis amb any únic.
- Potència: **150 seccions**, exclosa 4314806003 perquè només té registres amb potència absent.
- Comparació entre variables: **126 casos**, amb almenys deu edificis d'any únic i una potència publicada de categoria Edifici.
- Constantí: **98 potències publicades**, 94 posicions; conjunt complet de 124 amb 26 absències. Geometria puntual simple, EPSG:25831.

# Resultats globals

Normalització per files, diagonal zero. Els contrastos globals es defineixen cap a associació positiva abans del càlcul, amb 9.999 permutacions i llavor 20261005.

| Variable | n | Queen | Rook | kNN4 | kNN8 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Renda, €/persona | 151 | 0,571917 | 0,579014 | 0,569406 | 0,484782 |
| Mediana d'edat | 150 | 0,354646 | 0,383910 | 0,472597 | 0,354423 |
| ln(1 + kW/100 edificis) | 150 | 0,144047 | 0,130133 | 0,148766 | 0,100359 |
| ln(1 + kW/1.000 m²) | 150 | 0,220149 | 0,207798 | 0,220833 | 0,186916 |
| Petjada mitjana per edifici | 151 | 0,267143 | 0,268148 | 0,257863 | 0,189308 |

Pseudo-p queen: renda i edat 0,0001; potència per nombre 0,0028; potència per superfície 0,0001; petjada mitjana 0,0002. No interpretar I com a percentatge ni comparar indicadors sense revisar unitats i mostra.

La I queen s'ha contrastat amb la fórmula matricial directa. El Shapefile de renda conserva exactament els veïns de les geometries completes originals. No s'ha inferit Queen de les geometries simplificades destinades a figures.

# Lectures locals de renda

| Cas | Valor propi | Mitjana de veïns | Quadrant | Pseudo-p de referència | BH a 0,05 |
| --- | ---: | ---: | --- | ---: | --- |
| A · 4314807013 | 23.239 | 21.496,67 | HH | 0,0049 | Destacat |
| B · 4314808012 | 7.379 | 10.228,25 | LL | 0,0010 | Destacat |
| C · 4304701002 | 7.744 | 13.453,50 | LL | 0,2527 | No destacat |

La mitjana simple dels indicadors de les 151 seccions és 15.220,36. A rep pes 1/3 de cadascuna de les seccions 4314807007, 4314807016 i 4304301002. C mostra que un valor propi molt baix no implica una associació local extrema.

La referència amb llavor explícita destaca nominalment 29 HH, 23 LL i 6 LH. Benjamini–Hochberg deixa 23 HH, 18 LL i 3 LH, amb tall 0,0136. És una sensibilitat exploratòria; no s'afirma control universal sota dependència arbitrària.

**Execució QGIS conservada:** 27 HH, 23 LL, 6 LH i 95 casos no destacats. Els quadrants coincideixen amb la referència independent; els pseudo-p varien per la seqüència aleatòria del complement, que no exposa llavor al diàleg. No exigir recompte idèntic en una nova execució; conservar la seva taula. `q_value` és un quadrant, no un ajust FDR.

**Gi* QGIS:** 26 concentracions altes, 21 baixes i 104 no destacades. Renda, Queen binari, sense normalització de files, estrella amb la pròpia unitat, 9.999 permutacions i pseudo-p bilateral. Els Z s'han contrastat amb la fórmula directa de suma local; error màxim absolut inferior a 1e-10. No hi ha correcció múltiple.

# Petjada i relacions entre variables

D, secció 4314806006: 194 edificis, 600.362,8442 m², 1.944 kW. Resultats: **1.002,0619 kW/100 edificis** i **3,2380 kW/1.000 m²**. Petjada mitjana: 3.094,6538 m². No convertir aquesta superfície en coberta solar disponible.

| X propi | Y propi | Pearson | Moran bivariant X–retard de Y |
| --- | --- | ---: | ---: |
| Edat | log_pot | −0,400954 | −0,075342 |
| Edat | log_area | −0,281850 | −0,000187 |
| Renda | log_pot | 0,285617 | 0,005458 |
| Renda | log_area | 0,326332 | 0,112904 |
| Petjada mitjana | log_pot | 0,518408 | 0,135643 |
| Petjada mitjana | log_area | −0,075764 | −0,089810 |

Mateixos 126 casos; Queen refet per al subconjunt. Aquestes xifres són descriptives. Ni renda ni edat s'han unit individualment a famílies o a petjades de panells. La I dels residus edat–log_pot és 0,163861, pseudo-p 0,0029.

El mapa anterior de potència per nombre, amb llavor 20260929, destacava un HH després de BH; la llavor 20261005 no en destaca cap. La I global no canvia. És un exemple de variació de Montecarlo prop d'un tall molt restrictiu, no una contradicció entre geometries.

# Constantí

| Prova | n | I |
| --- | ---: | ---: |
| log_kw, kNN4 | 98 | 0,655668 |
| log_kw, kNN8 | 98 | 0,632489 |
| log_kw, kNN12 | 98 | 0,589300 |
| Vuit veïns i tots els empatats al tall | 98 | 0,620203 |
| Ordre dels registres invertit, kNN8 | 98 | 0,632474 |
| kW sense transformar, kNN8 | 98 | 0,191856 |
| Escenari inferior transformat, kNN8 | 124 | 0,591282 |
| Escenari central transformat, kNN8 | 124 | 0,621062 |
| Escenari superior transformat, kNN8 | 124 | 0,571434 |

Amb kNN8 hi ha 14 files amb empats a la distància de tall. La regla inclusiva arriba a nou veïns en algunes files. L'aresta més llarga és de 2.565,71 m. Radi de 500 m: sis illes, deu components; radi de 1.000 m: tres illes, set components. Aquelles dues proves es documenten sense índex inferencial.

A, de 450 kW: `ln(451) = 6,111467`. Veïns de 100, 100, 60, 30, 100, 20, 60 i 50 kW: mitjana dels logaritmes **4,059681**, superior a la mitjana general **2,488461**. HH; pseudo-p de referència 0,0001. Sortida QGIS nominal: 34 HH, 41 LL, 1 HL, 2 LH i 20 no destacats.

Conservar les 26 absències al conjunt complet; els escenaris no són valors observats. El mapa principal de 98 casos no conté cap imputació. La potència transforma l'atribut que es compara, no un pes del punt en el sentit del centre ponderat de C4: aquí els pesos espacials descriuen el veïnatge.

# Evidència i abast

Les sortides locals s'han executat amb l'API pública de Processing del mateix QGIS que es captura. La fórmula global i els Z de Gi* disposen de controls independents. Les captures mostren accés, diàlegs configurats i capes calculades; **no acrediten un recorregut manual clic a clic**.

El paquet conserva dades i camins relatius. La prova de portabilitat obre els projectes en una ruta diferent, sense xarxa i amb els inputs en lectura. Les instruccions d'instal·lació de Windows/macOS provenen de documentació; la prova funcional executada correspon al runtime Linux fixat, no a instal·lacions realitzades en aquells dos sistemes.
