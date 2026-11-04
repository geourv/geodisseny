---
title: "Guia docent: accessibilitat — xarxa vectorial"
author: Benito Zaragozí
lang: ca
date: "Edició: 30 d'octubre de 2026"
content_status: review
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
2. Adjunta `accessibilitat-xarxa-vectorial.zip` a **Fitxers addicionals**.
3. Obre **`ENUNCIAT-MOODLE.md`**, lliurat al costat d'aquest PDF, i copia'n el text editable a **Descripció**. Comunica a classe i a Moodle els apartats seleccionats i el codi real de la pràctica. El marcador `prN` dels patrons de nom no assigna cap número.
4. Revisa la vista d'estudiant. El ZIP docent conté aquesta lectura i els projectes/resultats per preparar la sessió.

# Resolució i controls

El paquet docent conté `LLEGIU-ME.pdf` a l'arrel i els recursos a `data/`. Conserva `data/projectes/00-inici.qgz` i `02-xarxa.qgz`, amb dependències relatives. `data/accessibilitat-vilaseca.gpkg` conté els vectors inicials; `data/resultats.gpkg`, els resultats vectorials de referència. Els ràsters són GeoTIFF a `data/rasters/`. Els projectes seleccionen les capes pertinents al bloc i el dibuix segueix l'ordre del panell Capes.

| Magnitud | Control |
| --- | --- |
| O /D | (344407;4553668,36) /(344473,01;4554030,72) m |
| Recta vectorial | 368,32 m |
| Ruta oberta | 454,10 m |
| Temps a 5 km/h | 5,45 min |
| Eix retirat | rtt_id1354754 |
| Ruta tancada | Sense ruta; longitud/temps nuls |

Table: Controls del cas vectorial amb els mateixos O/D.

`native:shortestline` contrasta la recta amb Pitàgores. `native:shortestpathpointtopoint` utilitza criteri de longitud, direcció per defecte ambdós sentits, tolerància topològica0m i punt–xarxa0,1m. La ruta ràpida usa `v_kmh` i5km/h per defecte; el cost és en hores.

![La ruta oberta i la connexió retirada permeten interpretar la resposta de la xarxa.](captures/xarxa.png){width=100% height=350pt}

El tancament conserva `"rtt_id" <> 1354754`, amb `native:extractbyexpression`. Retirar tots els eixos que toquen el corredor ràster eliminaria també accessos que es volen mantenir. La xarxa preparada té7.945parts i no nodifica cada creuament visual.

Revisa justificació de toleràncies, punts fixos, unitats i connexions. La manca de ruta és un resultat del graf preparat, no una certificació de totes les alternatives físiques. En una altra zona, els controls impresos deixen de ser resultats esperats.

# Organització i lliurament portable

Mostra la separació entre `data/`, que es conserva com a referència, `sandbox/`, amb la còpia del QGZ i les proves, i `dist/`, amb els lliurables seleccionats. Els grups de capes no mouen fitxers. Les vistes del paquet docent permeten reprendre fases de classe; no converteixen totes les capes de referència en lliurables obligatoris.

La guia demana un GeoPackage **nou** a `dist/`, un QGZ **extern** relatiu i l'informe PDF, amb el patró codi–tema–cognoms. Els vectors i recursos necessaris s'exporten/copien a la selecció final; el projecte deixa de dependre de `data/` o `sandbox/`. Les proves descartades romanen fora del lliurament.

Obre una còpia traslladada o un ZIP acabat d'extreure, sense xarxa. Comprova les fonts de dades de la còpia, les capes, els estils, les etiquetes i l'ordre de dibuix. Si es conserva el WMS, també cal el seu XML i un context local per a la revisió offline. Un projecte que només funciona perquè troba les dades a l'ordinador original no acredita portabilitat.

# Posada en comú i fonts

Demana què afegeix la xarxa respecte de la recta i què caldria per passar d'una ruta del model a una diagnosi d'accés. Les captures documenten configuració i representació; la interpretació necessita controls i coneixement de les entrades.

Fonts: [ICGC RTT2024](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial), límit20/1/2026, ortofoto2025, [condicions ICGC](https://www.icgc.cat/condicions) i [QGIS3.44](https://docs.qgis.org/3.44/en/docs/user_manual/).
