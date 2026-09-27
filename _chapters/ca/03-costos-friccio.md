---
layout: manual-chapter
title: Superfícies de cost i fricció
description: Distància euclidiana contra cost acumulat, fricció amb barreres, anisotropia i ruta de cost mínim en ràster.
lang: ca
ref: superficies-cost-friccio
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/superficies-cost/
weight: 30
part: Continguts
manual_references: true
---

La distància euclidiana poques vegades descriu com es mou ningú: el territori oposa resistència i conté barreres. Aquest capítol construeix superfícies de cost que ho incorporen i n'extreu rutes òptimes.

>>>>> En acabar el capítol, cal poder distingir proximitat euclidiana de cost acumulat.
>>>>>
>>>>> - Explicar què representa una superfície de fricció, una de cost acumulat i una barrera.
>>>>> - Dissenyar barreres (i el seu punt de pas) amb criteri de mobilitat.
>>>>> - Llegir per què una ruta evita un eix excepte per un punt concret.

## Tres distàncies, tres preguntes

La **proximitat euclidiana** mesura separació geomètrica (buffers i distància a la font més propera). La **fricció** assigna a cada cel·la el cost de travessar-la: jerarquia viària, usos del sòl o pendent, segons el mode de desplaçament. El **cost acumulat** suma la fricció des d'un origen i respon quant costa arribar a cada lloc. Són tres magnituds diferents i no es comparen sense declarar unitats. {% cite burrough1998principles longley2015gis %}

## Barreres i punts de pas

Una barrera multiplica el cost fins a fer un pas inviable excepte pels punts declarats: una autovia per a un vianant, una zona protegida per a una infraestructura. Dissenyar la barrera és dissenyar el punt de pas (un pont, un corredor): sense forat explícit, la ruta òptima no existeix o dona la volta a l'àmbit. Aquest gest és el cor de l'aplicació del curs.

## Anisotropia: pujar no és baixar

El càlcul bàsic és isòtrop (costa igual en totes direccions). A peu o en bicicleta, la pendent trenca la simetria: la funció de Tobler quantifica com cau la velocitat amb la inclinació. {% cite tobler1970movie %} S'estudia a teoria i el càlcul anisotròpic queda com a extensió; a la pràctica, la fricció es modela amb jerarquia viària i barreres.

## Aplicació: travessar sense entrar a l'autovia

El cas del curs combina jerarquia viària amb una barrera d'autovia entre Vila-seca i Tarragona: entrar-hi a peu costa molt i la ruta hi ha de passar per un pont declarat. El resultat es llegeix sol al mapa (el cost baixa resseguint eixos i puja lluny d'ells).

## Procediment a QGIS

Proximitat a la selecció viària, rasterització amb valors de fricció, reclassificació i calculadora per a la superfície final, tot en EPSG:25831 amb graella de 25 m alineada. Després cost acumulat des de l'origen amb el mòdul de cost del proveïdor GRASS (`r.cost`, superfícies de cost i direccions), extracció de la ruta amb `r.drain` des del destí i vectorització a polilínia. Comproveu alineació, cel·les sense dada i unitats abans d'interpretar res.

## Activitats

### Tres distàncies entre dos punts

Entre Vila-seca i Tarragona, completeu la comparació amb la ruta òptima en ràster: els dos mapes (ràster i xarxa) i la taula amb les 3 distàncies i la seva lectura.

### Segon destí o isòcrones

Com a extensió no avaluada: repetiu amb un segon destí, deriveu isòcrones o calculeu estadístiques zonals per municipi.
