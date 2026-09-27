---
layout: manual-chapter
title: Xarxes, rutes i accessibilitat
description: Grafs i topologia, impedància, camí més curt, àrees de servei i comparació amb la ruta ràster.
lang: ca
ref: xarxes-rutes-accessibilitat
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/xarxes-accessibilitat/
weight: 20
part: Continguts
manual_references: true
---

Després del projecte, el primer moviment que modelem és el discret: aquí el moviment només existeix on la xarxa el permet. La fricció és jerarquia, sentit i connectivitat, i les barreres s'expressen excloent vies. Al capítol següent, la fricció es tornarà contínua sobre el ràster.

>>>>> En acabar el capítol, cal poder calcular i explicar una ruta en xarxa.
>>>>>
>>>>> - Verificar la topologia d'una xarxa abans de calcular-hi res.
>>>>> - Triar la impedància (longitud, temps) segons el mode de desplaçament.
>>>>> - Comparar recta, ruta ràster i ruta en xarxa amb criteris, no a ull.

## Grafs, topologia i impedància

Una xarxa és un graf: nodes on es decideix i arcs on es circula. La **topologia** declara les regles del joc (connectivitat, absència de duplicats, sentits coherents): sense topologia garantida no hi ha ruta que valgui. La **impedància** declara què minimitza el càlcul (aquí, longitud per a vianants; temps amb velocitats per a vehicles) i canviar-la canvia la resposta. El camí més curt és un algorisme clàssic de grafs aplicat a cada parell origen-destí. {% cite longley2015gis %}

## Aplicació: la xarxa de vianants

La xarxa de treball exclou les autovies: un vianant no hi pot entrar, de manera que la barrera del capítol anterior aquí és una absència. El cas compara el mateix parell origen-destí en els tres models; si ruta ràster i ruta en xarxa divergeixen, la divergència s'explica pels supòsits de cada model. L'àrea de servei estén la pregunta de punt a zona: fins on s'arriba en X minuts o metres.

## Procediment a QGIS

Comprovació amb el verificador de topologia, correcció de geometries i snap d'origen i destí a la xarxa. Camí més curt de punt a punt i àrea de servei des del punt amb les eines natives d'anàlisi de xarxa (`shortestpathpointtopoint`, `serviceareafrompoint`), mesura de la polilínia i detecció d'illes desconnectades.

## Activitats

### Ruta en xarxa i taula comparativa

Calculeu la ruta entre Vila-seca i Tarragona i prepareu la taula de distàncies (recta i xarxa; la ruta ràster s'hi afegeix amb el capítol següent), amb la lectura de quan coincideixen els models i quan no.

### Àrea de servei

Com a extensió no avaluada: calculeu l'àrea de servei des de l'origen i compareu-la amb les bandes del ràster.
