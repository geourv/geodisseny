---
layout: manual-chapter
title: Avaluació multicriteri
description: Objectiu i criteris, AHP i consistència, regles de combinació, sensibilitat i lectura sobre parcel·les.
lang: ca
ref: avaluacio-multicriteri
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/avaluacio-multicriteri/
weight: 80
part: Continguts
manual_references: true
---

On ubicar una instal·lació d'energies renovables? Aquest capítol integra tot el curs en una decisió territorial amb criteris, pesos i sensibilitat. L'avaluació multicriteri assisteix la decisió; no hi ha òptim objectiu, hi ha la millor alternativa segons preferències declarades. El marc clàssic és Saaty {% cite saaty1980ahp saaty2008decision %} i la referència SIG és Malczewski {% cite malczewski1999gis %}.

>>>>> En acabar el capítol, cal poder defensar una decisió territorial amb mapa i números.
>>>>>
>>>>> - Separar objectiu, factors i limitants, i ponderar amb AHP i consistència.
>>>>> - Combinar capes, analitzar la sensibilitat i llegir el resultat sobre parcel·les.
>>>>> - Comunicar-ho en un pòster i defensar-lo oralment.

## Objectiu, criteris i alternatives

Tot comença amb l'objectiu en una frase i les **alternatives** (aquí, cada cel·la o parcel·la candidata). Els **factors** graduen (pendent, distància a xarxa, visibilitat, usos, riscos, accessibilitat); els **limitants** exclouen en binari (proteccions, urbano, extrems). Barrejar-los és l'error fundacional: un limitant no pondera, veta.

## Pesos AHP i consistència

La matriu de comparació per parells converteix judicis ("la pendent importa el doble que la distància") en pesos, i la ràtio de consistència (CR < 0,1) rebutja matrius incoherents. Cada judici queda documentat al full de càlcul: un pes sense justificació no és un criteri. El càlcul es fa al full SAATY i els pesos entren al SIG per join, sense complements.

## Regles de combinació

Totes les entrades, vinguin de vector o de ràster, es rasteritzen a la graella comuna del projecte abans de combinar: l'AMC d'aquest curs és íntegrament ràster. Factors normalitzats a la mateixa escala i agregats: suma ponderada per defecte, amb els extrems AND (tot ha de complir-se, risc mínim) i OR (n'hi ha prou amb un, risc màxim) com a referència. El mapa d'idoneïtat es classifica en nivells llegibles i cada nivell té conseqüència territorial.

## Sensibilitat i robustesa

Cap decisió sobreviu a un sol joc de pesos sense anàlisi de sensibilitat: variar cada pes ±10% en execucions repetides (modelador per lots), mapa d'incertesa i canvi de classe per parcel·la. El que no canvia és robust; el que canvia depèn d'un judici i s'ha de dir.

## Aplicació: de la idoneïtat a la parcel·la

Encreuament amb parcel·les del Cadastre (servei WFS o Atom) i estadístiques zonals: òptimes, subòptimes i no aptes. La parcel·la és la unitat que decideix, no la cel·la: el mapa continu es llegeix en unitats de gestió.

## Pòster i defensa del treball de síntesi

El pòster A0 comunica la decisió: títol, autoria, introducció, metodologia amb flux, resultats amb els mapes clau, discussió, conclusions i codi de dades. L'esborrany es defensa amb preguntes d'autoria; el document final incorpora les millores.

## Activitats

### Idoneïtat amb sensibilitat

Jerarquia, pesos amb consistència, mapa d'idoneïtat, mapa d'incertesa i qualificació de parcel·les sobre la comarca de treball.

### Pòster

Com a tancament del curs: maquetació A0, defensa oral i document final corregit.
