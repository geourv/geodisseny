---
layout: manual-chapter
title: Visibilitat del territori
description: Conca visual, altures i curvatura, MDT contra MDS, intervisibilitat i lectura de l'impacte visual.
lang: ca
ref: visibilitat-territori
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/visibilitat/
weight: 40
part: Continguts
manual_references: true
---

Des d'on es veurà una instal·lació proposada? Aquesta pregunta típica de geodisseny es respon amb conques visuals calculades sobre el relleu, encreuades amb els punts que importa protegir de l'impacte.

>>>>> En acabar el capítol, cal poder calcular i interpretar una conca visual.
>>>>>
>>>>> - Parametritzar un viewshed amb criteri (altures, curvatura, abast).
>>>>> - Encreuar la conca amb punts sensibles i llegir perfils longitudinals.
>>>>> - Defensar un mapa d'impacte amb criteris explícits.

## Què veu un observador

Una conca visual binària declara cada cel·la com a visible o no des d'un punt amb una altura donada. Tres paràmetres decideixen el resultat: **altura d'observador** (una torre no és un hort solar), **altura d'objectiu** (què compta com a vist) i **abast** amb correcció de curvatura terrestre. Sense declarar-los, dues conques no són comparables.

## MDT contra MDS

Es treballa amb MDT, és a dir, sòl nu: un model de superfície amb edificis i vegetació donaria conques menors. La diferència s'ha de declarar a la interpretació, no amagar-la: l'impacte calculat és una cota superior. {% cite burrough1998principles %}

## Intervisibilitat i conca acumulada

La intervisibilitat pregunta si dos punts es veuen mútuament (matriu entre sensibles); la conca acumulada suma conques des de diversos observadors i gradua l'exposició del territori. Ambdues estenen el cas bàsic sense canviar d'eina.

## Aplicació: un hort solar vist des dels punts sensibles

El cas del curs situa un observador a la instal·lació proposada i pregunta quins nuclis i trams de via la veuen. El perfil longitudinal fins al sensible més proper explica el resultat millor que cap estadística.

## Procediment a QGIS

Conca amb l'eina de viewshed de GDAL (`gdal:viewshed`) o el mòdul GRASS (`r.viewshed`), encreuament amb la capa de sensibles i perfils longitudinals. Comproveu graella, cel·les sense dada i que l'abast cobreix tots els sensibles abans d'interpretar res.

## Activitats

### Mapa d'impacte visual

Conca binària, taula de sensibles (veu o no veu), perfil clau i mapa d'impacte amb instal·lació, conca i sensibles.

### Conca acumulada

Com a extensió no avaluada: acumuleu conques des de tres punts o construïu la matriu d'intervisibilitat entre sensibles.
