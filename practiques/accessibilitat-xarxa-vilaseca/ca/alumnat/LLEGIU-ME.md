---
title: "Pràctica: accessibilitat per xarxa vectorial a Vila-seca"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
---

# Distància recta i itinerari per vials

Dos punts propers poden quedar separats per l'AP-7. Al Camí del Mas de la Plana compararem la recta entre O i D amb un itinerari sobre eixos connectats. Després retirarem la connexió de P2, mantenint els punts, per estudiar què representa una resposta «sense ruta».

**El professor indicarà a classe quins apartats i exercicis són obligatoris dins del 70% de la qualificació**, i els recollirà a Moodle. La guia ofereix el recorregut del bloc vectorial. Les ampliacions permeten aspirar a l'excel·lent, amb una pregunta, controls i interpretació.

# Dades i projecte d'inici

El ZIP conté `accessibilitat-vilaseca.gpkg` i `LLEGIU-ME.pdf`. El GeoPackage conserva el nom comú del cas i el projecte **inici**. Hi ha també entrades per als altres blocs; aquí s'utilitzen O/D, xarxa, passos, límit i ortofoto.

1. Utilitza **QGIS 3.44**. Descomprimeix el paquet en una carpeta pròpia i treballa sobre una còpia del GeoPackage.
2. A **Explorador → GeoPackage → Connexió nova**, selecciona el fitxer i desplega'l. Obre **inici**, o utilitza **Projecte → Obre des de → GeoPackage**.
3. Comprova **EPSG:25831** i el·lipsoide **Cap / NONE**. Les coordenades i longituds planes són en metres.
4. Desa un projecte de treball al costat de les dades. Conserva els resultats amb noms de capa nous.

![Connexió al GeoPackage del cas amb el projecte i les capes desplegats.](captures/inici.png){width=80% height=350pt}

La xarxa procedeix dels **eixos RTT2024 de l'ICGC**, amb escala òptima de treball d'1:5.000. Té 7.945 parts i conserva `rtt_id`, atributs cartogràfics i nodes preparats. Els contactes extrem–interior s'han dividit entre eixos de terreny genèric; no s'han creat cruïlles a cada creuament visual.

La selecció de trams i la velocitat uniforme són supòsits docents. Un eix cartogràfic no certifica accés a peu. Els passos a diferent nivell s'han de contrastar sobre cartografia i ortofoto.

Mantén les coordenades d'O/D durant tota la comparació:

```text
O: 344407.000000,4553668.360000 [EPSG:25831]
D: 344473.010000,4554030.720000 [EPSG:25831]
```

# Distància euclidiana

1. A **Procés → Caixa d'eines**, cerca **Línia més curta entre objectes**, `native:shortestline`.
2. Font **Origen O**, destinació **Destí D**, distància al punt més proper, **1** veí i distància màxima buida.
3. Desa **euclidiana_vector**. Mesura'n la longitud i compara-la amb les diferències de coordenades: 66,01 m en X i 362,36 m en Y.

![Configuració de la línia més curta entre els dos punts.](captures/distancies-vector-parametres.png){width=80% height=350pt}

$$d=\sqrt{66,01^2+362,36^2}\simeq368,32\ \mathrm{m}.$$

La recta no considera barreres, connexions ni permisos. Explica per què no és encara un itinerari. Tancar P2 no canvia aquesta separació.

# Ruta oberta i temps uniforme

1. Cerca **Camí més curt — punt a punt**, `native:shortestpathpointtopoint`.
2. Entrada **xarxa**, criteri **més curt**, mateixos O/D i direcció per defecte **ambdós sentits**.
3. Tolerància topològica **0 m** i punt–xarxa **0,1 m**. Desa **ruta_obert**: aproximadament **454,10 m**.
4. Repeteix amb **més ràpid**, camp `v_kmh` i velocitat per defecte **5 km/h**. Multiplica el cost en hores per 60: aproximadament **5,45 min**.

La velocitat és uniforme; no incorpora pendent ni penalització per coberta. Els sentits dels vehicles no es traslladen automàticament a un model a peu.

# Tancament de P2

1. Localitza **rtt_id = 1354754** a xarxa. Contrasta l'eix amb **pas_id = 2** de passos i l'ortofoto.
2. A **Extreu per expressió**, `native:extractbyexpression`, conserva `"rtt_id" <> 1354754`. Desa **xarxa_tancada**, sense modificar la inicial.
3. Repeteix la ruta amb els mateixos punts. La xarxa preparada retorna **sense ruta**. Conserva el missatge i representa la connexió retirada.

![La ruta oberta utilitza P2; retirar-ne l'eix deixa O i D desconnectats en la xarxa preparada.](captures/xarxa.png){width=100% height=350pt}

Una distància nul·la no és zero. La manca de ruta depèn dels eixos, exclusions i connexions del model; no demostra la manca de tota alternativa física. Inspecciona el component d'O abans d'ampliar la xarxa. Augmentar una tolerància per forçar una connexió necessita justificació.

# Ampliacions i preguntes obertes

- Compara un segon destí o diversos orígens. Quin és més vulnerable al tancament? Distància recta i ruta ordenen els destins igual?
- Prova velocitats diferenciades, justificades com a escenaris. Coincideixen la ruta curta i la ràpida?
- Aplica el mètode a una altra barrera o equipament, d'acord amb el professor. Revisa la cobertura externa al límit municipal i calcula controls propis.
- Proposa una aplicació geogràfica: diagnosi d'accessos a serveis o identificació de connexions vulnerables. Quines dades sobre accés autoritzat, obstacles o temps observats caldrien?

Les àrees de servei, la marxa amb MDT i les isòcrones tenen una lectura pròpia al bloc de **temps d'accés**. El bloc ràster permet contrastar aquest itinerari amb moviment entre cel·les.

# Informe i lliurament

Presenta pregunta i àmbit, fonts i decisions, procediment amb controls, mapes comparables i taula de resultats, i una conclusió amb límits. Explica les connexions, les toleràncies, el tancament i les unitats; no cal descriure cada clic.

Pots enregistrar fragments de pantalla amb un enregistrador com OBS Studio. Fes una prova de llegibilitat, anota els moments útils i desa fotogrames des d'un reproductor. Numera les captures i explica què demostren. Exporta els mapes finals amb llegenda, escala i unitats. El vídeo és una ajuda; només es lliura si el professor ho indica.

Lliura `accessibilitat-xarxa-vilaseca-cognom.gpkg`, amb les capes generades; un projecte `.qgz` amb rutes relatives; i un informe `.pdf`. Conserva les dades referenciades i comprova l'obertura després de moure la carpeta completa.

La qualificació distribueix **70% als apartats obligatoris indicats a classe**, **20% a les ampliacions** i **10% a l'informe, captures, mapes i organització**. Les ampliacions no substitueixen els obligatoris ni garanteixen una nota per haver-les intentat.

# Fonts

ICGC: [RTT i descàrregues](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial), edició2024; límit municipal del20/1/2026; ortofoto2025 de context a2m/píxel. [Condicions d'ús](https://www.icgc.cat/condicions), [descàrrega RTT per àrea](https://visors.icgc.cat/appdownloads/?c=fmetopoterritorial) i [QGIS3.44](https://docs.qgis.org/3.44/en/docs/user_manual/).
