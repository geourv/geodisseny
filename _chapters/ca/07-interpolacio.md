---
layout: manual-chapter
title: Superfícies contínues
description: Estacionarietat, semivariograma i models, IDW contra kriging, validació i mapes d'error.
lang: ca
ref: superficies-continues
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/superficies-continues/
weight: 70
part: Continguts
manual_references: true
---

Temperatura, precipitació o elevació existeixen a tot arreu però es mesuren en punts: aquest capítol estima valors on no hi ha observacions i quantifica l'error de cada predicció. Sense semivariograma, interpolar és una caixa negra. La geoestadística neix amb Matheron {% cite matheron1963principles %} i la referència de fons és Cressie {% cite cressie1993statistics %}.

>>>>> En acabar el capítol, cal poder interpolar amb criteri i quantificar l'error.
>>>>>
>>>>> - Construir el semivariograma experimental i ajustar-hi un model amb anisotropia.
>>>>> - Aplicar IDW i kriging ordinari, comparar-los i triar amb validació creuada.
>>>>> - Lliurar la superfície amb el seu mapa d'error, no només la predicció.

## Estacionarietat: el peatge d'entrada

Interpolar amb kriging exigeix estacionarietat: mitjana constant i covariació que només depèn de la distància (i la direcció). Si hi ha tendència regional, primer es modela (kriging universal) o el variograma menteix. Comprovar-la és el primer pas, no un refinament.

## Variograma experimental i models

El semivariograma experimental mesura com creix la dissimilaritat amb la distància, per classes i per direccions (0°, 45°, 90°, 135°) per detectar anisotropia. El model teòric (esfèric, exponencial o gaussià) el resumeix en **nugget** (error de mesura i microvariació), **sill** (variància total) i **range** (abast de la dependència). Un nugget proper al sill avisa que no hi ha estructura aprofitable.

## IDW contra kriging

L'IDW pondera per distància inversa sense model: simple, sempre disponible (interpolació IDW nativa i de GDAL), cec a l'estructura. El kriging ordinari pondera amb el model i retorna variància de predicció a cada cel·la. La validació creuada (deixar-ne una fora) decideix amb RMSE, MAE i correlació observat-predicció, més Moran I dels residus com a control.

## Eines: interpolació a QGIS

L'IDW es calcula amb la interpolació nativa; el variograma experimental, l'ajust del model i el kriging, amb les eines geoestadístiques de la caixa de processament (proveïdors de l'aula), i els ràsters tornen al projecte per al mapa i els zonals. Una coberta categòrica no s'interpola amb mitjanes.

## Aplicació: superfície amb el seu error

Temperatura o precipitació d'estacions sobre el Tarragonès: variograma ajustat, kriging amb contrast IDW, taula de validació i mapes de predicció i d'error, un al costat de l'altre.

## Activitats

### Superfície amb el seu error

Variograma, kriging, validació i doble mapa com a lliurable complet.

### Amb tendència o covariable

Com a extensió no avaluada: kriging universal o una covariable auxiliar i discussió de què millora.
