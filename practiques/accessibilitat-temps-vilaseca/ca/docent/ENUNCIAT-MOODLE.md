# Accessibilitat: temps d'accés

**Dades.** Descarregueu `accessibilitat-temps-acces.zip` i conserveu l'estructura completa. Llegiu `LLEGIU-ME.pdf`, a l'arrel, i obriu `data/inici.qgz` amb QGIS 3.44, GDAL i GRASS. Els vectors són al GeoPackage de `data/`; l'MDT i les friccions oberta/tancada són GeoTIFF a `data/rasters/`. El cas d'aplicació és Vila-seca. Són entrades del bloc; haureu de calcular temps i isòcrones. El grup Ortofoto ICGC permet alternar el context local amb el WMS quan hi ha connexió.

**Organització.** Conserveu `data/` com a referència i utilitzeu `sandbox/` per al projecte de treball, proves i intermedis. A `dist/` prepareu la selecció final. Els grups de capes no mouen els fitxers entre carpetes.

**Treball de classe.** El professor indicarà els apartats obligatoris del 70%: àrees de servei, marxa d'anada/tornada, control pla, isòcrones/franges i interpretació. La guia completa no converteix tots els procediments en obligatoris. Manteniu O/D, graella i paràmetres en cada comparació.

**Ampliacions per aspirar a l'excel·lent.** Compareu orígens, llindars, pesos o una zona amb més pendent. Quina connexió o superfície es perd? Quina observació permetria contrastar els temps? Desenvolupeu una aplicació geogràfica amb una referència, controls i límits explícits.

**Informe i lliurament.** Prepareu a `dist/` un GeoPackage nou amb els vectors seleccionats, un QGZ extern relatiu, els TIFF necessaris a `rasters/`, els recursos utilitzats i el PDF amb pregunta, fonts, decisions, mapes/taules i conclusions. No hi afegiu experiments descartats ni fitxers no utilitzats. Identifiqueu carpeta/ZIP i fitxers principals amb `prN-temps-acces-cognoms`, amb les extensions corresponents; substituïu `prN` pel codi real d'aquesta tasca. Diferencieu branques de xarxa, superfícies, longitud, cost i temps. Podeu enregistrar la pantalla i extreure captures comentades; el vídeo només es lliura si el professor ho indica.

**Portabilitat.** Obriu una còpia traslladada o el ZIP extret en una carpeta nova, sense xarxa. El QGZ ha de llegir les dades de la còpia, sense dependències de `data/` o `sandbox/` originals. Comproveu valors i unitats, capes, estils, etiquetes, fonts tipogràfiques i ordre.

**Qualificació.** 70% apartats indicats a classe; 20% ampliacions; 10% informe, captures, mapes i organització. Una ampliació necessita pregunta, controls i interpretació i no substitueix els obligatoris.
