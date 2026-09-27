---
layout: manual-chapter
title: Dependència espacial
description: Hipòtesi d'independència, matrius de pesos, Moran, Geary, LISA, Gi* i la unitat areal modificable.
lang: ca
ref: dependencia-espacial
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/dependencia-espacial/
weight: 60
part: Continguts
manual_references: true
---

El que passa en un lloc s'assembla al que passa al costat? Aquest capítol formula la primera llei de la geografia com a hipòtesi contrastable i n'extreu clústers amb criteri estadístic. És el fil teòric que connecta amb la interpolació (el semivariograma n'és la versió contínua) i amb la validació del treball final. {% cite tobler1970movie %}

>>>>> En acabar el capítol, cal poder detectar clústers amb criteri estadístic.
>>>>>
>>>>> - Triar una matriu de pesos espacials i justificar-la amb el fenomen.
>>>>> - Calcular Moran I global, Geary C, indicadors locals LISA i Getis-Ord Gi*, amb lectura de p-valors.
>>>>> - Cartografiar clústers, hotspots, coldspots i atípics espacials.

## Independència, veïnatge i contrastos

La hipòtesi nul·la és la independència espacial: el valor d'una unitat no depèn dels veïns. La **matriu de pesos** declara qui és veí de qui (contigüitat Queen o Rook per a polígons, distància fixa o k veïns per a punts) i tot en depèn. Moran I {% cite moran1950notes %} resumeix la covariació amb el retard espacial; la C de Geary {% cite geary1954contiguity %} pondera diferències locals. Valors significatius rebutgen l'atzar, no expliquen la causa.

## Escala global i escala local

El global diu si hi ha estructura; el local diu on. Els indicadors locals d'Anselin {% cite anselin1995lisa %} classifiquen cada unitat (HH, LL, HL, LH: clústers i atípics) i la Gi* de Getis i Ord {% cite getis1992analysis ord1995local %} gradua hotspots i coldspots. Amb moltes unitats, la significació es corregeix per comparacions múltiples; sense correcció, el mapa menteix per excés.

## La unitat areal modificable

L'agregació triada condiciona el resultat: un mateix fenomen dóna clústers diferents per parcel·la, secció censal o graella. Tot clúster es llegeix amb la unitat declarada, i la comparació entre agregacions forma part de la interpretació, no d'un annex.

## Eines: estadística espacial a QGIS

El nucli de QGIS descriu (capítol anterior) i classifica (`kmeansclustering`, `dbscanclustering`); els contrastos inferencials d'aquest capítol es calculen amb les eines d'estadística espacial de la caixa de processament (proveïdors i complements disponibles a l'aula, amb recepta proporcionada) sobre les mateixes capes, i els resultats tornen al projecte com a capes per al mapa. Els residus d'una interpolació o d'una EMC també hi passen: autocorrelació residual alta invalida el model.

## Aplicació: clústers del cas

POIs i variables socioeconòmiques de l'INE al Tarragonès, amb la mateixa matriu de pesos per a globals, locals i Gi*, llindar declarat i mapa de significació i tipus.

## Activitats

### Clústers amb criteri

Mapa de clústers i hotspots amb significació, taula d'estadístics globals i interpretació amb unitat declarada.

### Segona matriu, segona lectura

Com a extensió no avaluada: repetiu amb una altra matriu de pesos i discutiu què canvia i què roman.
