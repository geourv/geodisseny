---
layout: manual-chapter
title: Preparació d'un projecte SIG
description: Dada, font i capa; sistemes de referència; projecte reproduïble i mapa de localització amb referència.
lang: ca
ref: preparacio-projecte-sig
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/preparacio-projecte-sig/
weight: 10
part: Continguts
manual_references: true
---

Tot anàlisi comença abans del primer càlcul: triant fonts, fixant el sistema de referència i organitzant un projecte que una altra persona pugui obrir i entendre. Aquest capítol repassa aquests fonaments sobre el Tarragonès i tanca amb el mapa de localització del curs.

>>>>> En acabar el capítol, cal poder obrir un projecte reproduïble i compondre un mapa amb referència.
>>>>>
>>>>> - Distingir descàrrega, servei WMS o WFS i capa local en un projecte.
>>>>> - Filtrar, exportar i documentar capes amb criteri de traçabilitat.
>>>>> - Combinar ortofoto, límits, nuclis i viari en una composició amb mapa de referència.

## Repàs de TIG i prerequisits de TIGIT

Es repassen el model ràster, la calculadora de camps, la simbolització temàtica i la composició d'un mapa. Es dona per conegut el primer curs de [TIGIT](https://geourv.github.io/tigit/ca/): treball amb full de càlcul i indicadors, unions de taules amb capes a QGIS, principis de representació de la Terra i sistemes de referència, semiologia gràfica i llenguatge cartogràfic, i ús de fonts oficials. Qui necessiti refrescar aquests fonaments, els trobarà allà.

## De la dada a la capa: vocabulari mínim

Una **dada** és una observació; una **font** és qui la produeix i amb quines condicions (data, detall, llicència); un **producte** n'és la materialització (un full del MDT, una ortofoto anual); una **capa** és com la carreguem al projecte. La **via d'accés** decideix la traçabilitat: una descàrrega es versiona, un WMS es referencia (la imatge la compon el servidor) i un WFS lliura entitats. Confondre via i dada és l'error més comú: un WMS d'ortofoto no és una dada analitzable, és un fons visual. {% cite longley2015gis %}

## El sistema de referència abans de res

Cap mesura té sentit sense sistema de referència de coordenades (CRS) amb unitats adequades: distàncies i àrees es calculen en projectats (aquí, EPSG:25831), mai en graus. Si una capa arriba en un altre sistema, reprojecció explícita abans de res, i comprovació d'extensió i unitats després.

## Fonts oficials: descobrir, descarregar i servir

Una font es tria per pregunta, no per comoditat. L'**Hipermapa de la Generalitat** serveix per descobrir què hi ha; el **Vissir o el web de Descàrregues de l'ICGC** per obtenir divisions administratives municipals, Nomenclàtor de nuclis, xarxa viària BT-5M i corbes de nivell. L'ortofoto recent es consumeix com a **WMS de l'ICGC**. A QGIS, tot passa pel gestor de fonts: connexions WMS i WFS desades, descàrregues a carpeta de treball i cap ruta absoluta que trenqui el projecte en un altre ordinador.

## El projecte com a unitat reproduïble

Un projecte és un contracte: CRS únic, rutes relatives, capes amb origen declarat i cap resultat sense procedència. El gest mínim és filtrar municipis per comarca amb una expressió, exportar la selecció a un GeoPackage propi i treballar-hi des d'allà, mai sobre la descàrrega general. El recompte resultant es comprova sempre.

## Composició amb mapa de referència

Un mapa de localització respon on som abans de qualsevol anàlisi: ortofoto, límits, nuclis i viari en una composició A4 amb títol, llegenda, escala gràfica, fonts i data de l'ortofoto, més un **mapa de referència de Catalunya** amb la comarca destacada (un segon mapa dins la composició, enllaçat a una vista general). Si el WMS cau, la composició ha de continuar obrint-se.

## Activitats

### Mapa de localització del Tarragonès

Munteu des de zero el projecte del curs: descàrrega, filtre per comarca, exportació al GeoPackage propi i composició A4 amb referència, amb captures del procés i comprovació en un perfil net.

### Segona lectura del mateix mapa

Trieu una ampliació sense avaluar: corbes de nivell, polígon de mar retallat, noves simbologies o etiquetes. Serveix per practicar criteri visual abans que compti nota.
