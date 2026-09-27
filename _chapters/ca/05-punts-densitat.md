---
layout: manual-chapter
title: Distribucions de punts i densitat
description: Intensitat contra observació, centres i dispersió, KDE, quadrícules, aleatorietat i funció K.
lang: ca
ref: distribucions-punts-densitat
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/punts-densitat/
weight: 50
part: Continguts
manual_references: true
---

On són les coses i formen patrons? Aquest capítol descriu distribucions de punts (comerç, serveis, equipaments) amb estadístics i mapes, per tipologia, perquè cada activitat té una lògica espacial pròpia.

>>>>> En acabar el capítol, cal poder descriure un patró de punts amb estadístics i mapes.
>>>>>
>>>>> - Calcular centre mitjà, distància estàndard i distribució direccional per tipologia.
>>>>> - Estimar densitat kernel amb amplada de banda justificada i detectar agregació amb recomptes i funció K.
>>>>> - Distingir un hotspot visual d'un clúster significatiu (aquest es confirma al capítol següent).

## Punts observats contra intensitat estimada

Un mapa de punts mostra observacions; un mapa de densitat estima **intensitat per unitat d'àrea** allà on no hi ha punts. Confondre'ls és l'error clàssic: una cel·la densa no conté aquella gent o botigues, estima quanta activitat hi ha per hectàrea. Tota densitat porta un model a dins.

## Centres, dispersió i forma

El centre mitjà situa, la distància estàndard dispersa i l'el·lipse direccional orienta: tres números que resumeixen una tipologia abans de cap mapa. A QGIS es calculen amb coordenada mitjana i les eines d'estadística de la caixa (`meancoordinates`), per lots quan hi ha diverses tipologies.

## KDE: nucli, amplada i vores

La densitat kernel reparteix cada punt amb una funció de nucli fins a una amplada de banda: la banda decideix el que es veu (banda petita, soroll; banda gran, tot pla) i cal justificar-la i provar-ne una de contrast. Les vores de l'àmbit subestimen la densitat si no es corregeixen. L'eina és el mapa de calor per estimació kernel (`heatmapkerneldensityestimation`).

## Aleatorietat, quadrícules i funció K

L'aleatorietat completa espacial és la referència: els recomptes per quadrícula (millor hexagonal, amb punts comptats per polígon) diuen si hi ha més cel·les plenes o buides de l'esperat, i la funció K de Ripley {% cite ripley1976second %} contrasta agregació, regularitat o atzar a cada distància. El grup d'eines de clustering per densitat (`dbscanclustering`) i de partició (`kmeansclustering`) classifica els punts en grups com a pas exploratori previ al contrast del capítol següent.

## Aplicació: tipologies d'activitat al Tarragonès

Comerç, serveis i equipaments d'OSM i de l'IDEC: mateixos estadístics, tres lògiques espacials. La comparació entre tipologies amb els mateixos números és sovint més informativa que superposar densitats.

## Activitats

### Retrat d'una tipologia

Estadístics, mapa KDE i lectura de la funció K per a una tipologia, amb interpretació territorial.

### Comparació entre tipologies

Com a extensió no avaluada: compareu dues tipologies amb els mateixos estadístics i discutiu si comparteixen lògica espacial.
