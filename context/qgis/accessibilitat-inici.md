# Captures de la pràctica d'accessibilitat: dades d'inici

Preparar captures QGIS en català per a una guia que es pugui seguir a casa.
La xarxa de l'activitat es deriva físicament dels eixos RTT2024 de l'ICGC,
amb identificadors rtt_id i una selecció/nodificació documentades. Fer servir
el GeoPackage d'inici i els resultats del run ICGC nou, inclosa la resposta
sense ruta després de retirar l'eix1354754 de P2. Les captures de xarxa han
de mostrar la font ICGC, la ruta oberta i la connexió que es tanca; no dibuixar
una volta OSM com a resultat de la xarxa ICGC.
Completar la guia amb el diàleg de rasterització de cobertes —camp classe,
resolució5m, extensió comuna—, el dels vials RTT —valor fix1, sense camp,
mateixa graella— i el de passos —camp pas_id, fons0 vàlid—.
Fer visible que vials i passos tenen fricció1/cost per cel·la5; els eixos viaris
no reobren la plataforma de l'AP-7 fora dels passos ni P2 en l'escenari tancat.
Mostrar que els passos amb fricció1 es conserven al cost per cel·la amb valor5.
Regenerar els diàlegs i les vistes amb les entrades, coordenades, resultats i
camps del run ICGC. Conservar les captures anteriors com a reconstrucció.
La primera vista ha de mostrar la connexió al GeoPackage desplegada a
l'Explorador, el projecte incrustat i les capes origen, destí, xarxa, cobertes,
passos i MDT. Assenyalar la selecció d'una capa concreta, no de tot el fitxer.

Les captures següents han de relacionar distància GRASS i fonsNULL, rutes i
passos alternatius, cobertes reclassificades amb polígons de pas, cost acumulat,
marxa amb relleu i isòcrones obertes/tancades. Conservar QGIS i els seus panells,
unitats i llegendes. Fer servir els projectes docents com a moments de control.
Els dos camins de cost i marxa poden ser sortides cartogràfiques retallades al
canvas, amb unitats i interpretació al peu; connexió, diàlegs i isòcrones han
de conservar la interfície QGIS i la llegenda de la capa pertinent.

Fonts versionades de l'activitat a `practiques/accessibilitat-vilaseca/`.
Les preparacions noves són a `sandbox/practiques/accessibilitat-vilaseca/<run>/`;
el preparador materialitza una configuració/recepta confinada a aquell run.
Les referències de les captures històriques a tmp/dades-docents identifiquen
snapshots segellats. Sortides privades completes PNG/SVG/manifest a captures/.
Cap preparació del campus; cap reutilització d'un resultat antic com si fos
el resultat de la xarxa i les cobertes noves.
