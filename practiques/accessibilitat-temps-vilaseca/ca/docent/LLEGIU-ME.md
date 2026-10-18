---
title: "Guia docent: temps d'accés i ampliacions"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
---

# Abast, prerequisits i durada

Bloc d'àrees de servei, marxa amb MDT i isòcrones. Pot completar les dues subpràctiques anteriors o usar-se com a tasca amb les friccions inicials proporcionades. Aquestes incorporen els eixos RTT i els passos; els temps i contorns els calcula l'alumnat.

| Component | Estimació |
| --- | --- |
| Aula | 120–150min |
| Treball autònom i informe | 90–120min |
| Preparació docent | 30–45min |

Table: Durada orientativa amb friccions inicials disponibles.

Estimació pendent de prova d'aula, amb QGIS/GDAL/GRASS preparats i coneixement de graella, NoData, costos i reconstrucció de camins. Tornar a construir la fricció correspon al bloc ràster i s'afegeix al temps. La selecció anunciada del70% determina l'abast; una zona alternativa o més repeticions l'amplia.

# Preparar Moodle

1. Crea una **Tasca** amb el nom **Accessibilitat: temps d'accés i ampliacions**.
2. Adjunta `accessibilitat-temps-vilaseca-2026-10-18-ca.zip` a **Fitxers addicionals**.
3. Copia el bloc següent a **Descripció**, fins al final de «Qualificació», i recull la selecció de classe.
4. Revisa la vista d'estudiant i les dues friccions d'inici. El docent conserva aquesta lectura, els resultats i les vistes de servei, marxa i isòcrones.

## Enunciat per copiar a la descripció

**Dades.** Descarregueu `accessibilitat-temps-vilaseca-2026-10-18-ca.zip`. Obriu inici de `accessibilitat-vilaseca.gpkg` amb QGIS3.44, GDAL i GRASS, i carregueu les friccions oberta/tancada. Són entrades del bloc; haureu de calcular temps i isòcrones.

**Treball de classe.** El professor indicarà els apartats obligatoris del70%: àrees de servei, marxa d'anada/tornada, control pla, isòcrones/franges i interpretació. La guia completa no converteix tots els procediments en obligatoris. Manteniu O/D, graella i paràmetres en cada comparació.

**Ampliacions per aspirar a l'excel·lent.** Compareu orígens, llindars, pesos o una zona amb més pendent. Quina connexió o superfície es perd? Quina observació permetria contrastar els temps? Desenvolupeu una aplicació geogràfica amb una referència, controls i límits explícits.

**Informe i lliurament.** Entregueu vectors en GeoPackage, projecte relatiu, TIFF requerits i PDF amb pregunta, fonts, decisions, mapes/taules i conclusions. Diferencieu branques de xarxa, superfícies, longitud, cost i temps. Podeu enregistrar la pantalla i extreure captures comentades; el vídeo només es lliura si el professor ho indica. Comproveu l'obertura des d'una altra ubicació.

**Qualificació.** 70%apartats indicats a classe;20%ampliacions;10%informe, captures, mapes i organització. Una ampliació necessita pregunta, controls i interpretació i no substitueix els obligatoris.

# Xarxa i superfície temporal

O=(344407;4553668,36)m;D=(344473,01;4554030,72)m. EPSG:25831/NONE, graella5m i600×640cel·les; X343000–346000/Y4552000–4555200. P2és rtt_id1354754/pas_id2.

| Límit | Xarxa oberta, longitud única | Xarxa tancada, longitud única |
| --- | ---: | ---: |
| 3min | 448,384607m | 68,418647m |
| 6min | 1116,560723m | 68,418647m |
| 12min | 3606,611447m | 68,418647m |

Table: Branques accessibles; unió geomètrica per evitar duplicats.

`native:serviceareafrompoint` usa criteri ràpid, v_kmh/5 km/h, O i ambdós sentits. Travel cost és 0,05/0,10/0,20 hores. D entra en 6 min obert; en tancar P2, augmentar el límit no permet sortir del component d'O. No són longituds d'un itinerari únic.

# Marxa i control del relleu

La fricció temporal és `("friccio_obert@1" - 1) * 0.125`, en s/m, sense multiplicar per5. r.walk rep altituds, no un ràster de pendent. Coeficients0.72,6.0,1.9998,-1.9998;lambda1;slope factor−0,2125m/m; sense moviment de cavall i nuls exclosos.

| Model | O→D | D→O |
| --- | ---: | ---: |
| MDT, P2obert | 401,797517s =6,696625min | 394,465679s =6,574428min |
| Elevació constant | 340,724610s | 340,724610s |
| MDT, P2tancat | 1555,331669s =25,922194min | No requerit per aquest control |

Table: Temps dels models amb vials integrats a la fricció inicial.

![Les dues direccions provenen d'execucions diferents de r.walk.](captures/marxa.png){width=100% height=350pt}

La diferència d'anada/tornada és 7,33 s; el pla és simètric. Un zero de penalització addicional no elimina el temps de desplaçament. No invertir només la línia; cada sentit necessita les seves direccions i origen. El MDT de 5 m pot simplificar el pas inferior i els temps no són caminades observades.

# Isòcrones i superfície

Usa marxa des d'O **en minuts**. r.contour:nivells3/6/12, mínim3punts per línia i regió comuna5m. Les franges conserven NoData separat de>12min. Repeteix P2tancat amb el mateix MDT, paràmetres i colors.

| Límit | Obert, cel·les | Obert, ha | Tancat, cel·les | Tancat, ha |
| --- | ---: | ---: | ---: | ---: |
| Fins a3min | 2831 | 7,0775 | 2552 | 6,3800 |
| Fins a6min | 10924 | 27,3100 | 7677 | 19,1925 |
| Fins a12min | 35430 | 88,5750 | 22109 | 55,2725 |

Table: Recomptes i àrees acumulades;25m²per cel·la.

![Isòcrones obertes: D entre 6 i 12 min.](captures/isocrones-obert.png){width=100% height=350pt}

![Isòcrones tancades: D fora de 12 min.](captures/isocrones-tancat.png){width=100% height=350pt}

Les franges de referència no toquen el límit de càlcul. En altres zones, comprovar-ho abans de publicar-ne l'àrea. La xarxa arriba a D en5,45min; la marxa amb MDT i fricció en6,70min. En tancar P2, el ràster conserva un camí mentre que el graf no connecta O/D: les condicions de moviment difereixen.

# Projectes, posada en comú i fonts

Vistes docents00/03/04/08/09/10: inici, àrees de servei obertes/tancades, marxa i isòcrones. Conserven dependències relatives i els intermedis temporals per reprendre controls de classe.

Revisa la selecció anunciada, les unitats, els dos sentits, el control pla, la cobertura i la interpretació. En ampliacions, demana què canvia respecte de la referència i quines dades permetrien contrastar-ho. Una superfície temporal no mesura directament població servida ni permisos d'accés.

Fonts: [ICGC elevacions](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions), LiDAR2021–2023/MDT5m, MCSC/RTT2024/ortofoto2025; [condicions ICGC](https://www.icgc.cat/condicions), [r.walk](https://grass.osgeo.org/grass84/manuals/r.walk.html), [r.contour](https://grass.osgeo.org/grass84/manuals/r.contour.html).
