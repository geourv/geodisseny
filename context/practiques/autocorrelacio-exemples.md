---
title: "Autocorrelació de renda, edificació i potències puntuals"
subtitle: "Guia de treball amb QGIS"
author: Benito Zaragozí
lang: ca
date: "Preparació: 5 d'octubre de 2026"
content_status: draft
---

# Preguntes i dades

Les unitats veïnes tenen valors semblants? Canvia el resultat si es compara renda, edat o potència? Es pot estudiar la mateixa pregunta amb punts? La pràctica relaciona valor propi, veïnatge i resultat estadístic, abans d'interpretar els colors dels mapes locals.

## Contingut del paquet

- `01-renda.qgz`: renda per seccions i capes de resultats.
- `02-constanti.qgz`: 98 registres amb potència publicada, veïnatge d'A i Moran local sobre ortofoto.
- `autocorrelacio.gpkg`: seccions, atributs preparats i resultats de les execucions conservades.
- `renda.shp`, `.shx`, `.dbf`, `.prj`, `.cpg`: exportació completa per construir Queen al complement. El `.qml` conserva la simbologia.
- `ortofoto.tif` i `.qml`: context ICGC 2025, retall WMS a 8 m/píxel.
- `originals/`, `downloads.json`: taules de l'INE i metodologia conservades, amb URL i SHA-256.
- `analysis.json`, `qgis-controls.json`, `verification.json`: càlculs de referència, execucions Processing i comprovacions.
- `captures/`, `reproduccio/`: captures i fonts. Els preparadors necessiten el repositori i els originals indicats; els projectes i exercicis es poden obrir directament des del paquet.

La renda és de **2023**, referida a la població de l'1/1/2024; les seccions són d'aquesta mateixa data. Els edificis cadastrals provenen del feed del 21/8/2026. L'ICAEN es va extreure el 28/9/2026, sense haver establert la data efectiva del conjunt. Les coordenades ICAEN representen consumidors associats, no necessàriament les petjades dels panells.

# Preparar la sessió

1. Descomprimeix el paquet complet. Crea `treball/` per desar els teus projectes, exportacions i resultats.
2. Utilitza QGIS amb Processament i **Hotspot Analysis 4.0.0**. El catàleg de complements manté «v3» al nom: comprova la versió.
3. Comprova `libpysal` i `esda` des de **Complements → Consola de Python**. Les versions de referència són 4.13.0 i 2.7.1, amb Python 3.11 o posterior. Les vies d'instal·lació segons el paquet de QGIS són a C0 i a l'apartat «Preparació de QGIS i PySAL» de C5.
4. Obre `01-renda.qgz` i desa una còpia a `treball/`. El CRS és **EPSG:25831**. Per mesurar àrees planes, utilitza el·lipsoide **Cap/Planimètric** o l'expressió `area($geometry)`.
5. A l'Explorador, crea una connexió GeoPackage a `autocorrelacio.gpkg` i desplega-la. La connexió pertany al perfil de QGIS i es crea de nou en un altre ordinador.

```python
import sys
print(sys.version.split()[0], sys.prefix)
import libpysal, esda
print(libpysal.__version__, esda.__version__)
```

Una comprovació numèrica recupera quatre valors ficticis en cadena:

```python
from libpysal.weights import lat2W
from esda import Moran
print(Moran([1, 1, 4, 4], lat2W(1, 4), permutations=0).I)
```

El resultat és **0.5**. Aquí es comprova l'estadístic, no la significació.

# Renda: variable i veïnatge

## Capa i controls

Carrega `renda.shp` si encara no és al projecte. La taula ha de contenir **151 codis `cusec` diferents**, renda numèrica entre **7.261 i 27.703 €/persona**, i cap valor nul de `renda`. Són indicadors de secció: la mitjana simple, 15.220,36, no és la renda mitjana ponderada dels habitants de la comarca.

La font és la taula 31223 de l'[Atlas de distribució de renda de les llars de l'INE](https://www.ine.es/jaxiT3/Tabla.htm?t=31223&L=0). La descàrrega completa conté anys, municipis, districtes i seccions. Per refer la unió s'ha de filtrar any 2023, «Renta neta media por persona» i nivell secció; després es fa la unió pel codi de deu dígits. No unir una taula temporal sense filtrar-la.

## Reconstruir un retard

Activa `renda_veins` i apropa't a la capa. Identifica la secció A i els tres veïns, numerats 1, 2 i 3.

| Unitat | Codi | Renda, €/persona |
| --- | --- | ---: |
| A | 4314807013 | 23.239 |
| 1 | 4314807007 | 24.068 |
| 2 | 4314807016 | 23.235 |
| 3 | 4304301002 | 17.187 |

\clearpage

![A i els tres veïns queen. Cada veí rep pes 1/3; la secció A no entra al seu propi retard.](captures/c5-renda-veins.png){width=95%}

Calcula la mitjana dels tres veïns: **21.496,67 €/persona**. Compara valor propi i retard amb 15.220,36. Tots dos són superiors: és el quadrant **HH**, encara sense haver-ne fet el contrast local.

**Resultat conservable:** mapa del veïnatge i taula amb rendes, pesos i retard.

# Moran local de la renda

## Accés i configuració

Obre **Procés → Caixa d'eines → Hotspot Analysis → LISA → Local Moran's I**. No triïs l'eina bivariant.

\clearpage

![El grup LISA reuneix tres eines. Local Moran's I és l'opció univariant del final.](captures/c5-eines.png){width=95%}

Utilitza el **Shapefile complet**, sense filtres de capa. Aquesta versió del complement construeix Queen llegint el fitxer, no qualsevol selecció visible. Conserva junts tots els components del Shapefile.

| Paràmetre | Valor |
| --- | --- |
| Input layer / Analysis field | `renda.shp` / `renda` |
| Spatial weights type | Queen's Contiguity |
| Optimize threshold automatically | Desactivat |
| Binary weights | Activat |
| Row standardization | **Activat** |
| Random permutations | 9.999 |
| Two-tailed p-value | Desactivat |
| Output | `treball/treball.gpkg`, capa `renda_lisa` |

\clearpage

![Renda, Queen i normalització per files. Les permutacions i la sortida són més avall al diàleg.](captures/c5-renda-parametres.png){width=80%}

Executa i comprova 151 objectes, geometria conservada i camps `p_value`, `q_value`, `Z_score`. Els controls corresponen a una execució des de Processing; les captures de diàleg mostren configuració, no una seqüència manual clic a clic.

## Simbologia i interpretació

El camp `q_value` és el quadrant: **1=HH, 2=LH, 3=LL, 4=HL**. No és un ajust FDR. A **Propietats → Simbologia → Categoritzat**, utilitza l'expressió següent, classifica i assigna colors:

```sql
CASE
  WHEN "p_value" >= 0.05 THEN 'No destacat'
  WHEN "q_value" = 1 THEN 'Alt-alt (HH)'
  WHEN "q_value" = 2 THEN 'Baix-alt (LH)'
  WHEN "q_value" = 3 THEN 'Baix-baix (LL)'
  WHEN "q_value" = 4 THEN 'Alt-baix (HL)'
END
```

\clearpage

![Moran local: HH en vermell, LL en blau fosc, LH en blau clar; gris per als casos no destacats.](captures/c5-renda-resultat.png){width=95%}

Compara A amb B i C. B té 7.379 €/persona i veïnes de 9.879, 9.934, 13.523 i 7.577; el retard és 10.228,25. C té 7.744 i veïnes de 13.262 i 13.645; el retard és 13.453,50. Tot i tenir renda pròpia semblant, B queda destacada com a LL i C no.

El complement no ofereix una llavor al diàleg. Conserva la teva taula: casos propers a 0,05 poden canviar entre execucions. El mapa nominal no incorpora una correcció de comparacions múltiples. Els camps `p_ref`, `q_ref` i `fdr_ref` conserven separadament el càlcul de referència amb llavor 20261005.

**Resultat conservable:** capa calculada, mapa amb llegenda completa i tres fitxes de lectura A/B/C.

## Resum global

Selecciona la capa **`renda.shp`**, completa i sense filtre, i executa aquest bloc a l'editor de la consola de QGIS:

```python
import numpy as np
from libpysal.weights import Queen
from esda import Moran
capa = iface.activeLayer()
ruta = capa.source().split('|')[0]
assert ruta.lower().endswith('.shp')
y = np.array([f['renda'] for f in capa.getFeatures()], dtype=float)
w = Queen.from_shapefile(ruta)
assert len(y) == w.n == 151 and not w.islands
np.random.seed(20261005)
m = Moran(y, w, transformation='r', permutations=9999)
p = (1 + np.count_nonzero(m.sim >= m.I)) / 10000
print(round(m.I, 4), p)
```

Controls: **0.5719 i 0.0001**. La prova global és unilateral cap a associació positiva, fixada abans de veure el resultat. La I no és un percentatge de seccions semblants.

# Getis–Ord Gi*: una altra pregunta local

Torna al mateix Shapefile i obre **Getis–Ord Gi***. Tria `renda`, Queen i pesos binaris. Deixa **Row standardization desmarcat**, estableix 9.999 permutacions i activa **Two-tailed p-value**, a la part inferior. Desa la sortida al GeoPackage de treball.

\clearpage

![Configuració de Gi*: es manté la renda però es treballa amb pesos binaris sense normalitzar les files.](captures/c5-gi-parametres.png){width=80%}

Representa en vermell els casos amb `p_value < 0.05` i `Z_score > 0`; en blau, els que passen el mateix llindar i tenen signe negatiu; en gris, la resta. Gi* inclou la secció pròpia en la suma i no classifica atípics HH/LL/HL/LH com Moran.

\clearpage

![Concentracions locals de renda amb Gi*: altes en vermell, baixes en blau i no destacades en gris.](captures/c5-gi-resultat.png){width=95%}

**Resultat conservable:** comparació amb Moran local, declarant la diferència de pregunta, pesos i contrast. Aquest mapa tampoc no incorpora correcció múltiple.

# Antiguitat i denominadors

La capa `seccions` conté camps ja agregats. Les 38.689 petjades funcionals sumen 13.566.378,21 m². Cada edifici s'ha assignat sencer pel seu punt interior, també quan travessa una vora. La petjada no és superfície construïda de totes les plantes ni coberta disponible per a panells.

| Camp | Significat |
| --- | --- |
| `edat` | Mediana d'antiguitat respecte de 2026; almenys deu edificis amb any únic |
| `n_edif`, `n_exact` | Edificis funcionals i edificis amb any únic |
| `petjada` | Suma de petjades, m² |
| `kw_pub` | Suma de kW publicats de categoria Edifici |
| `kw100ed`, `kw1000m` | kW per 100 edificis i per 1.000 m² |
| `log_pot`, `log_area` | `ln(1 + indicador)` en les dues normalitzacions |
| `mostra` | 1 als 126 casos comuns per comparar relacions entre variables |

1. Per a edat, filtra `"edat" IS NOT NULL` i **exporta els 150 objectes** a un Shapefile nou. Treu el filtre de la capa original i analitza l'exportació, no un filtre sobre el fitxer de 151.
2. Per a potència, exporta els 150 objectes amb `"log_pot" IS NOT NULL`. La secció exclosa no és la mateixa que en edat.
3. Aplica Queen, normalització per files i 9.999 permutacions a `edat`, `log_pot` i `log_area`, sobre cada exportació pertinent.
4. Conserva els camps originals i les sortides de cada variable per separat. Un augment de I en canviar el denominador no converteix automàticament aquell indicador en millor.

Comprova el cas D: 1.944 kW, 194 edificis i 600.362,84 m² donen **1.002,06 kW/100 edificis** i **3,24 kW/1.000 m²**. El numerador es manté.

**Resultat conservable:** taula amb mostra, unitats, indicador, veïnatge i resultat, més una explicació del canvi de denominador.

# Punts de Constantí

## Observacions i veïns

Obre `02-constanti.qgz` i desa'n una còpia. `constanti` conté **98 registres amb potència publicada**, en 94 posicions diferents. No s'han imputat els 26 valors absents del conjunt de 124. No eliminis registres coincidents només perquè es dibuixin superposats.

\clearpage

![Potències publicades de Constantí i connexions del punt A amb els seus vuit veïns.](captures/c5-constanti-dades.png){width=95%}

El camp `log_kw` és `ln(1 + "pot_kw")`. A Local Moran's I, tria **kNN**, **8 veïns**, distància euclidiana, normalització per files, 9.999 permutacions i opció bilateral desactivada. Desa el resultat i aplica la mateixa expressió de quadrants que en renda.

\clearpage

![Cada punt rep informació de vuit veïns; amb normalització, cadascun contribueix 1/8.](captures/c5-constanti-parametres.png){width=80%}

\clearpage

![Moran local dels mateixos punts: grup occidental de valors alts i grup oriental de valors baixos.](captures/c5-constanti-resultat.png){width=95%}

## Lectura i sensibilitat

A té 450 kW. Els seus vuit veïns tenen 100, 100, 60, 30, 100, 20, 60 i 50 kW. Transforma cada valor i calcula després la mitjana: **4,060**. El valor transformat d'A és 6,111 i la mitjana dels 98 registres és 2,488. Per això A és HH.

Compara el mapa amb la taula de sensibilitat de C5: I passa de 0,656 amb quatre veïns a 0,632 amb vuit i 0,589 amb dotze. Amb kNN8, el vincle més llarg arriba a 2.566 m. Un radi de 500 m deixa sis illes; un de 1.000 m, tres. No interpretis una prova que les ignori sense declarar-ho.

**Resultat conservable:** veïnatge d'A, taula dels valors transformats i paràgraf que distingeixi semblança de potències de concentració de localitzacions.

# Relacions entre variables i conclusions

Sobre els 126 casos amb `mostra = 1`, compara la relació edat–potència i renda–potència. La potència pròpia i la mitjana de potència de les veïnes responen a preguntes diferents. Si es construeix Queen per a aquest subconjunt, primer s'exporta i es refan els contactes.

La conclusió ha d'identificar **unitat, variable, dates, selecció, denominador, matriu, contrast i límits**. Conserva una carpeta de treball amb capes, projecte, taules i mapes. No concloguis que una família concreta instal·la més potència a partir d'una relació observada entre seccions.

# Fonts

- [INE, taula 31223: renda mitjana i mediana](https://www.ine.es/jaxiT3/Tabla.htm?t=31223&L=0) i [metodologia ADRH, octubre 2025](https://www.ine.es/metodologia/metodologia_adrh.pdf).
- [ICGC/Idescat, seccions censals](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Seccions-censals), edició 1/1/2024, CC BY 4.0.
- [Dirección General del Catastro, INSPIRE Buildings](https://www.catastro.hacienda.gob.es/webinspire/index.html), feed de Tarragona 21/8/2026.
- [ICAEN, localització d'instal·lacions d'autoconsum](https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/).
- [Ortofoto ICGC i condicions d'ús](https://www.icgc.cat/condicions), WMS territorial 2025.
- [Hotspot Analysis](https://plugins.qgis.org/plugins/HotSpotAnalysis_v3/), versió 4.0.0; libpysal i esda.
