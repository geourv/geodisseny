---
title: "Pràctica: temps d'accés, marxa i isòcrones"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
---

# Abast per xarxa i per superfície

Què es pot assolir en 3, 6 o 12 minuts? Compararem branques accessibles de la xarxa amb temps de marxa sobre una superfície amb relleu. L'anada i la tornada poden diferir; tancar P2 modifica els accessos mantenint els mateixos O/D.

**El professor indicarà a classe els apartats obligatoris del70%** i els recollirà a Moodle. Aquest bloc pot servir com a ampliació del recorregut anterior o com a tasca pròpia. La guia no converteix tots els procediments en obligatoris.

# Entrades preparades

El ZIP conté `accessibilitat-vilaseca.gpkg`, **friccio_obert.tif**, **friccio_tancat.tif** i aquest PDF. Les friccions són entrades inicials d'aquest bloc, preparades amb cobertes, vials i passos. No contenen els temps ni les isòcrones que calcularàs. Si disposes de les teves friccions del bloc ràster, utilitza-les després de validar-les i declara les diferències respecte de la referència.

1. Utilitza QGIS 3.44 amb GDAL i GRASS. Crea una connexió GeoPackage i obre **inici**; carrega les dues friccions des de la carpeta local.
2. Comprova EPSG:25831/NONE, extensió X343000–346000/Y4552000–4555200, cel·la5m i600×640cel·les.
3. Crea una carpeta d'intermedis. Selecciona capes concretes als diàlegs GRASS; desa el projecte amb rutes relatives i mantén tots els fitxers referenciats.

O=(344407;4553668,36)m;D=(344473,01;4554030,72)m. La fricció oberta té pes1als vials i passos; P2tancat és NoData i els alternatius continuen amb1. El model admet moviment entre cel·les i no certifica permisos de pas.

# Àrees de servei de xarxa

1. Obre **Àrea de servei — des d'un punt**, `native:serviceareafrompoint`.
2. Xarxa oberta, origen O, criteri **més ràpid**, camp `v_kmh`, velocitat5km/h, ambdós sentits i tolerància0.
3. **Travel cost** és en hores:0.05/0.10/0.20per als límits3/6/12min. Desa sortides en línies i noms diferenciats.
4. Extreu `"rtt_id" <> 1354754` per retirar P2i repeteix amb els mateixos límits.

Les longituds de branques accessibles no són un trajecte únic. Un polígon que les embolcalli no acredita accés a tota la superfície interior. D entra en 6 min amb P2 obert; el component d'O queda aïllat en el model tancat.

# Altitud i penalització temporal

1. Carrega **mdt** del GeoPackage. Retalla'l a ambit_calcul amb `gdal:cliprasterbyextent`, conservant resolució nativa5m i alineació. Desa **mdt_ambit.tif**.
2. Converteix la fricció en penalització addicional en segons per metre:

```text
("friccio_obert@1" - 1) * 0.125
```

3. Conserva NoData i la graella. Repeteix per al tancat. Els pesos1/2/4/6passen a0/0,125/0,375/0,625s/m.

No multipliquis aquesta penalització per5: r.walk incorpora la distància. Zero significa sense penalització addicional, no temps de marxa zero.

# Anada, tornada i control pla

1. A **r.walk.points**, elevació **mdt_ambit**, fricció **friccio_temporal_obert** i inici **Origen O**.
2. Coeficients **0.72,6.0,1.9998,-1.9998**, lambda1i slope factor **−0,2125m/m**. Sense moviment de cavall, nuls conservats i cost dels nuls buit; regió comuna5m.
3. Desa segons i direccions. Divideix els segons per60per representar minuts. Mostreja D i reconstrueix des de D amb r.path, formatdegree.
4. Repeteix r.walk des de **D**, amb les mateixes entrades; reconstrueix des d'O. Invertir la línia no recalcula el temps.

![r.walk utilitza altitud i penalització temporal com a entrades diferents.](captures/marxa-parametres.png){width=80% height=350pt}

![Anada i tornada amb càlculs independents sobre el mateix MDT.](captures/marxa.png){width=100% height=350pt}

El control és 401,80 s = 6,70 min d'anada i 394,47 s = 6,57 min de tornada. Per al control pla, crea elevació constant amb `"mdt_ambit@1" * 0`, sense canviar fricció: 340,72 s en els dos sentits. El MDT de 5 m pot simplificar el perfil d'un pas inferior; els temps no estan calibrats amb caminades observades.

# Isòcrones i franges de temps

1. Parteix de la marxa **des d'O en minuts**, no del cost ponderat ni de segons.
2. A **r.contour**, nivells3,6,12, sense increment regular, mínim3punts per línia, regió comuna5m.
3. Crea franges a Calculadora ràster:

```text
if("minuts@1" <= 3, 1,
   if("minuts@1" <= 6, 2,
      if("minuts@1" <= 12, 3, 4)))
```

4. Blau0–3min, verd>3–6, taronja>6–12i gris>12. Conserva NoData com a barrera, no com temps superior a12.
5. Repeteix r.walk des d'O amb P2tancat i mateix MDT/paràmetres. D requereix **25,92min**. Utilitza els mateixos nivells, colors i enquadrament.

![D queda entre 6 i 12 min amb P2 obert.](captures/isocrones-obert.png){width=100% height=350pt}

![Amb P2 tancat, D queda fora de 12 min; altres cel·les continuen accessibles.](captures/isocrones-tancat.png){width=100% height=350pt}

Compta les classes amb **Informe de valors únics del ràster**. Cada cel·la fa 25 m². Per obtenir hectàrees acumulades, suma fins al límit i multiplica per 25/10.000. Si una franja toca el límit de càlcul, amplia la regió abans d'interpretar-ne l'àrea.

# Ampliacions, informe i fonts

Compara altres orígens, límits de temps, pesos o una zona amb més pendent. Canvia un paràmetre cada vegada i mantén una referència. Quin lloc és més vulnerable? Quina part de la diferència explica el relleu? Com canvia la conclusió si la cobertura o el domini són incomplets?

Proposa una aplicació geogràfica: accés a equipaments, itineraris o connexions vulnerables. Quines observacions i restriccions d'accés caldria contrastar? Diferencia abast lineal de xarxa, superfície accessible i temps estimat del model.

L'informe ha de presentar pregunta, dades i decisions, controls, mapes/taules comparables i interpretació amb límits. Pots enregistrar fragments de pantalla i extreure fotogrames llegibles i comentats. El vídeo només es lliura si el professor ho indica; els mapes finals han de tenir llegenda, escala i unitats.

Lliura vectors en GeoPackage, projecte relatiu, TIFF requerits i PDF, amb el prefix **accessibilitat-temps-vilaseca-cognom**. Comprova la carpeta després de moure-la.

Qualificació: 70% apartats obligatoris indicats a classe; 20% ampliacions; 10% informe, captures, mapes i organització. Les ampliacions no substitueixen els obligatoris ni garanteixen una nota.

Fonts: [ICGC elevacions LiDAR2021–2023](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Elevacions), MDT5m, MCSC/RTT2024iortofoto2025; [condicions ICGC](https://www.icgc.cat/condicions), [QGIS3.44](https://docs.qgis.org/3.44/en/docs/user_manual/), [r.walk](https://grass.osgeo.org/grass84/manuals/r.walk.html), [r.contour](https://grass.osgeo.org/grass84/manuals/r.contour.html).
