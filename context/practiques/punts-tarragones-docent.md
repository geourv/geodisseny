---
title: "Punts del Tarragonès: controls docents"
author: Benito Zaragozí
lang: ca
date: "Preparació: 4 d'octubre de 2026"
content_status: draft
---

# Criteris d'interpretació

Les coordenades ICAEN corresponen a consumidors associats. Els resultats no mesuren petjades de panells, energia produïda, idoneïtat ni significació de clústers. Són resums descriptius de l'extracció conservada. La selecció per potència coneguda s'ha de mantenir en comparar pesos.

# Controls de dades i centres

| Control | Resultat |
| --- | --- |
| Inventari / coneguts / absents | 5102 / 3762 / 1340 |
| Suma coneguda | 36633 kW |
| Centre complet | (357272,517729;4556675,776714) m |
| Centre conegut sense pes | (357387,967435;4556891,170892) m |
| Centre ponderat | (354528,518116;4556391,868968) m |
| Desplaçament per ponderació | 2902,714732 m |
| Distància estàndard sense pes | 8698,204203 m |
| Semieixos, k=1 | 8152,141105 / 3033,373000 m |
| Angle des de l'est / azimut nord | 12,327263° / 77,672737° |

El centre ponderat es desplaça sobretot a l'oest. El canvi entre conjunt complet i conegut respon a disponibilitat de potència. El centroide depèn del límit, no dels registres. Una el·lipse d'una desviació no té cobertura universal del 68%.

En l'exemple fictici de quatre punts, el centre mitjà és (2;2) i el ponderat (2,8;3,2) km. Duplicar tots els pesos no mou el centre; duplicar només P4 dona (3,25;3,50); retirar P4 dona (1;2). La distància estàndard passa de 2,828427 km sense pes a 2,433105 km amb els pesos originals.

# Graella i kernels

La graella té 680 polígons, extensió X340000–374000/Y4546000–4566000 i quadrats d'1 km². S'han contrastat els recomptes i sumes de **cada cel·la** amb una assignació independent de coordenades: totals 3.762 registres i 36.633 kW. No són només controls del total general.

| Kernel quartic, píxel100m | Integral discreta |
| --- | ---: |
| Registres, h500m | 3762,002337 |
| Registres, h1500m | 3761,999764 |
| kW, h500m | 36633,587271 |
| kW, h1500m | 36633,014610 |

La integral és la suma de densitats vàlides × 0,01 km². Es calcula sobre la sortida completa, abans de retallar. Els factors de normalització són 3,8197186342 i 0,4244131816 respectivament. No interpretar valors crus com densitats, NoData com inventari absent, ni un píxel menor com dades més precises.

# Seccions censals

- 151 polígons, clau `cusec`, geometries completes de 2024.
- Categoria Edifici: 5.096 registres, 3.757 potències conegudes, 36.058 kW.
- Denominador agregat: 38.689 objectes Building funcionals, no habitatges.
- Una secció sense indicador: **4314806003**. Conserva registres però no potència coneguda; no és zero.
- L'indicador es comprova secció per secció amb els agregats conservats, amb tractament explícit de nuls.
- L'ampliació edat–potència utilitza 126 seccions. Pearson r=−0,400954 amb log(1+q), R²=0,160764; descriptiu i ecològic, sense atribució causal.

# Comprovació del procediment

Els càlculs s'han executat amb Processing en el runtime registrat. Centres: contrast NumPy; cercle: distància dels vèrtexs; el·lipse: covariància de la corba; graella: assignació independent; kernels: integral discreta; seccions: correspondència per codi amb una preparació independent. Els sis projectes s'han reobert en una ruta diferent, readonly i sense xarxa.

Els diàlegs mostren paràmetres i els mapes, fitxers calculats. Això no equival a haver recorregut tot el guió per clics. Les captures desen sortides temporals als diàlegs; l'alumne conserva les seves a `treball.gpkg` o TIFF. Comprovar entrada, filtre i camp de pes és més important que reproduir els colors.
