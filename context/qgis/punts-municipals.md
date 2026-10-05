# Escenaris de potència i interpretació a Constantí

Mostra una pràctica municipal de QGIS en català. La base són els 124 registres de Constantí, amb la mateixa geometria en tots els escenaris. Mantén les dades originals de potència i afegeix camps decimals per als límits i el punt mitjà dels intervals. El valor numèric publicat preval; els camps calculats no són observacions noves.

La sessió connecta `punts-municipals-20261004/municipis.gpkg` a l'Explorador superior esquerre, amb les capes desplegades. Utilitza l'ortofoto ICGC 2025 local, servida a 8 m/píxel, com a context. La vista inicial mostra registres amb contribució igual. La vista final utilitza àrees proporcionals a `w_mid`, blau per a valors publicats i taronja per als assignats, més els centres dels registres i de l'escenari central.

Captures: dades i connexió; Calculadora de camps amb `w_mid` decimal; Coordenades mitjanes amb `w_mid` i ID buit; resultat interpretat sobre la mateixa extensió; Geometria segons l'expressió per a l'el·lipse dels 124 punts. Emmarca camps i controls sense tapar-ne el text, amb marge zero i sense ombra. Les fórmules completes són al text; el diàleg no prova haver fet clic a Executa. Els resultats es comproven separadament amb QGIS i NumPy.
