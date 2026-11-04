# Accessibilitat: model ràster de cost

**Dades.** Descarregueu `accessibilitat-raster.zip` i conserveu l'estructura completa. Llegiu `LLEGIU-ME.pdf`, a l'arrel, i obriu `data/inici.qgz` amb QGIS 3.44, GDAL i GRASS. Els vectors són al GeoPackage de `data/`; els ràsters són GeoTIFF separats a `data/rasters/`. El cas d'aplicació és Vila-seca. Manteniu O/D, EPSG:25831/NONE i graella de 5 m. El grup Ortofoto ICGC conté el retall local i el WMS de context per consultar més detall amb connexió.

**Organització.** Preserveu `data/` i deseu la còpia del projecte, proves i intermedis a `sandbox/`. Prepareu `dist/` com a selecció final. Organitzar grups al panell Capes no mou ni copia les dades entre carpetes.

**Treball de classe.** El professor indicarà els apartats obligatoris del 70%: proximitat, reclassificació de cobertes, vials de pes 1, barreres/passos, r.cost/r.path i comparació de longitud/cost. La guia completa no obliga a lliurar tots els passos. Comproveu alineació i la prioritat pas → barrera → vial → coberta.

**Ampliacions per aspirar a l'excel·lent.** Compareu el model només de cobertes amb el que integra vials, o canvieu pesos/resolució o zona amb una referència i controls. Què passa quan la coberta generalitza un camí dins d'un conreu? Desenvolupeu una aplicació geogràfica i identifiqueu les dades que faltaria contrastar.

**Informe i lliurament.** Prepareu a `dist/` un GeoPackage nou amb els vectors seleccionats, un QGZ extern relatiu, els TIFF necessaris a `rasters/` i el PDF amb pregunta, fonts, decisions, controls, mapes/taula i conclusions. Incloeu els recursos que utilitza el projecte, no les alternatives descartades ni els intermedis sense ús final. El patró de carpeta/ZIP i fitxers principals és `prN-accessibilitat-raster-cognoms`, amb les extensions corresponents; `prN` representa el codi real d'aquesta tasca. Podeu enregistrar la pantalla i extreure captures llegibles i comentades; el vídeo només es lliura si el professor ho indica.

**Portabilitat.** Obriu una còpia traslladada o el ZIP extret en una carpeta nova, sense xarxa. Les fonts de dades han de ser dins de la còpia, sense dependències del `sandbox/` original. Reviseu dades, graella, NoData, estils, etiquetes, fonts tipogràfiques i ordre de dibuix.

**Qualificació.** 70% apartats indicats a classe; 20% ampliacions; 10% informe, captures, mapes i organització. Es valoren pregunta, controls i interpretació, no el nombre d'operacions.
