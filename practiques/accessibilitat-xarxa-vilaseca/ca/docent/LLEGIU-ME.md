---
title: "Guia docent: accessibilitat per xarxa vectorial"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
---

# Abast i durada orientativa

Bloc vectorial: recta, connexions, ruta curta/ràpida i tancament de P2. Les superfícies de cost i els temps amb relleu tenen lectures separades.

| Component | Estimació |
| --- | --- |
| Aula | 90–120 min |
| Treball autònom i informe | 60–90 min |
| Preparació docent | 30–45 min |

Table: Durada orientativa del bloc vectorial.

Estimació pendent de contrast amb una classe, amb QGIS preparat, dades locals i experiència bàsica amb capes i Processament. Instal·lar programari o descarregar una altra zona queda fora del còmput. La selecció del professor determina l'abast obligatori del70%; formular una pregunta pròpia pot ampliar el treball autònom.

# Preparar Moodle

1. Crea una **Tasca** amb el nom **Accessibilitat: xarxa vectorial**.
2. Adjunta `accessibilitat-xarxa-vilaseca-2026-10-18-ca.zip` a **Fitxers addicionals**.
3. Copia el bloc següent a **Descripció**, fins al final de «Qualificació». Comunica a classe i a Moodle els apartats seleccionats.
4. Revisa la vista d'estudiant. El ZIP docent conté aquesta lectura i els projectes/resultats per preparar la sessió.

## Enunciat per copiar a la descripció

**Dades.** Descarregueu `accessibilitat-xarxa-vilaseca-2026-10-18-ca.zip`. Obriu el projecte inici de `accessibilitat-vilaseca.gpkg` amb QGIS3.44 i seguiu `LLEGIU-ME.pdf`. Els eixos de xarxa i el context cartogràfic són de l'ICGC; trams admesos i velocitats són supòsits docents.

**Treball de classe.** El professor indicarà els apartats obligatoris dins del70%: distància recta, connexions, ruta curta/ràpida, tancament de P2 i interpretació. La guia completa no és una llista de passos automàticament obligatoris. Manteniu O/D i distingiu «sense ruta» de distància zero.

**Ampliacions per aspirar a l'excel·lent.** Compareu destins, velocitats o una altra zona, amb una referència i controls. Quin accés és més vulnerable? Quines dades permetrien contrastar la ruta? Proposeu una aplicació geogràfica proporcionada als resultats.

**Informe i lliurament.** Entregueu vectors en un GeoPackage, projecte relatiu i PDF amb pregunta, dades, decisions, controls, mapes/taula i conclusions. Podeu enregistrar la pantalla i extreure'n captures llegibles, numerades i comentades; el vídeo només es lliura si el professor ho indica. Comproveu l'obertura en una altra carpeta.

**Qualificació.** 70% apartats obligatoris indicats a classe;20% ampliacions;10% informe, captures, mapes i organització. Una ampliació necessita pregunta, controls i interpretació; no substitueix els obligatoris ni garanteix una nota.

# Resolució i controls

El paquet docent conserva `docent/projectes/00-inici.qgz` i `02-xarxa.qgz`, amb dependències relatives. El GeoPackage inicial és el del cas comú; `docent/resultats.gpkg` conté els resultats vectorials de referència. Els projectes seleccionen les capes pertinents al bloc.

| Magnitud | Control |
| --- | --- |
| O /D | (344407;4553668,36) /(344473,01;4554030,72) m |
| Recta vectorial | 368,323349 m |
| Ruta oberta | 454,104650 m |
| Temps a5km/h | 5,449256 min |
| Eix retirat | rtt_id1354754 |
| Ruta tancada | Sense ruta; longitud/temps nuls |

Table: Controls del cas vectorial amb els mateixos O/D.

`native:shortestline` contrasta la recta amb Pitàgores. `native:shortestpathpointtopoint` utilitza criteri de longitud, direcció per defecte ambdós sentits, tolerància topològica0m i punt–xarxa0,1m. La ruta ràpida usa `v_kmh` i5km/h per defecte; el cost és en hores.

![La ruta oberta i la connexió retirada permeten interpretar la resposta de la xarxa.](captures/xarxa.png){width=100% height=350pt}

El tancament conserva `"rtt_id" <> 1354754`, amb `native:extractbyexpression`. Retirar tots els eixos que toquen el corredor ràster eliminaria també accessos que es volen mantenir. La xarxa preparada té7.945parts i no nodifica cada creuament visual.

Revisa justificació de toleràncies, punts fixos, unitats i connexions. La manca de ruta és un resultat del graf preparat, no una certificació de totes les alternatives físiques. En una altra zona, els controls impresos deixen de ser resultats esperats.

# Posada en comú i fonts

Demana què afegeix la xarxa respecte de la recta i què caldria per passar d'una ruta del model a una diagnosi d'accés. Les captures documenten configuració i representació; la interpretació necessita controls i coneixement de les entrades.

Fonts: [ICGC RTT2024](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial), límit20/1/2026, ortofoto2025, [condicions ICGC](https://www.icgc.cat/condicions) i [QGIS3.44](https://docs.qgis.org/3.44/en/docs/user_manual/).
