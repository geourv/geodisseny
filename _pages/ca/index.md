---
layout: manual-home
title: "Anàlisi Espacial i Geodisseny"
description: Manual de teoria aplicada, pràctiques i criteris d'anàlisi espacial i geodisseny amb QGIS.
lang: "ca"
ref: home
profiles: [unaltremanual]
content_status: draft
permalink: "/ca/"
nav: false
show_chapter_index: true
figure_captions: true
manual_references: false
---

Aquest manual forma part de l'assignatura **Anàlisi Espacial i Geodisseny** (codi `21234116`), de tercer curs del Grau en Geografia, Anàlisi Territorial i Sostenibilitat de la Universitat Rovira i Virgili. L'assignatura és obligatòria i combina sessions de teoria i pràctica a l'aula SIG. Professorat: Benito Zaragozí i Yolanda Pérez Albert.

L'objectiu del curs **no és memoritzar una col·lecció d'eines**. Es tracta d'entendre com es representa un problema territorial mitjançant dades, com condiciona el resultat cada tècnica d'anàlisi espacial i com es defensa una decisió amb mapa i números. [QGIS](https://qgis.org/) és l'eina principal de les pràctiques. El curs continua on acaba Tecnologies de la Informació Geogràfica: el model ràster i la calculadora de camps hi són el punt de partida, no el destí.

>>>>> En acabar el curs, cal poder dissenyar i defensar una anàlisi espacial completa orientada a una decisió territorial.
>>>>>
>>>>> - Preparar un projecte QGIS reproduïble amb fonts oficials (ICGC, Cadastre, OSM).
>>>>> - Aplicar distàncies, visibilitat, patrons de punts, autocorrelació i interpolació sobre un mateix territori.
>>>>> - Construir una avaluació multicriteri amb pesos justificats i anàlisi de sensibilitat.
>>>>> - Comunicar el resultat en un pòster científic i defensar-lo oralment.

El manual desenvolupa més exemples i activitats que els exigits per superar l'assignatura. Les demostracions de classe es fan sobre el **Tarragonès**; el treball de síntesi s'aplica per grups a **comarques diferents**. Donat que l'estudiant ja ha superat TIG i TIGIT, les activitats se centren en les parts noves: en algunes rebreu dades preparades per no repetir neteges apreses i anar directes a l'anàlisi.

Els lliuraments del curs segueixen un format únic: GeoPackage amb el projecte incrustat, còpia externa del projecte en `.qgz` i apunts breus en PDF amb captures. Les activitats lliurables estaran identificades de manera explícita; Moodle publicarà l'enunciat vigent, el termini i les condicions concretes de cada lliurament.

::: table "Dades identificatives de l'assignatura"
| Camp | Valor |
| --- | --- |
| Assignatura | Anàlisi Espacial i Geodisseny |
| Codi | `21234116` |
| Ensenyament | Grau en Geografia, Anàlisi Territorial i Sostenibilitat |
| Caràcter | Obligatòria |
| Professorat | Benito Zaragozí i Yolanda Pérez Albert |
:::

## Manual, Moodle i guia docent

::: table "On es troba cada tipus d'informació"
| Espai | Funció |
| --- | --- |
| Manual | Teoria, exemples, procediments, activitats i criteris per comprovar els resultats |
| Moodle | Calendari del curs, avisos, enunciats vigents, fitxers, lliuraments i qualificacions |
| Guia docent | Resultats d'aprenentatge, continguts, metodologies i condicions oficials de l'assignatura |
:::

**La guia docent és la referència normativa.** El manual acompanya l'assignatura però no és l'assignatura: explica el com, no fixa dates ni percentatges. El calendari sessió per sessió i els terminis viuen a Moodle i no es versionen aquí.

## Avaluació

L'avaluació combina pràctiques individuals continuades amb un treball de síntesi que es lliura com a document i es defensa oralment, amb preguntes de comprovació d'autoria i de comprensió de les eines. Cal un nivell mínim suficient en cada part per fer mitjana; una part no superada suspèn l'assignatura encara que la mitjana global arribi a l'aprovat.

Els lliuraments han de permetre verificar l'autoria i reconstruir el procés: projecte reproduïble, fonts declarades i captures que demostrin configuracions i comprovacions. No s'accepten lliuraments fora de termini i la còpia implica un 0. En cas d'usar eines d'intel·ligència artificial, cal un ús ètic i responsable: cal declarar-ne l'ús i ser capaç d'explicar-ne qualsevol resultat a l'exposició.

## Activitats

### Reconèixer els espais del curs

El resultat conservat serà una fitxa breu amb l'enllaç a la guia docent vigent, l'espai Moodle i el fòrum de dubtes. Per a cadascun, una informació que només correspongui a aquell espai i per què no convé buscar-la als altres dos.

### Preparar una consulta reproduïble

El resultat conservat serà una consulta breu sobre una incidència real o hipotètica de QGIS: objectiu, dades, passos, resultat esperat i obtingut. Si depèn d'un CRS, un camp, una ruta o un paràmetre, hi apareixerà explícitament.

### Anticipar el treball de síntesi

Un cop assignada la comarca, el diari conservarà una pregunta d'anàlisi espacial que s'hi pugui estudiar: dades necessàries, organisme que les proporciona i resultat observable que permetria respondre-la. No resol l'anàlisi ni dona per verificada cap font.
