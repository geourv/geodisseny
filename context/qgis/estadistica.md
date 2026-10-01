# Centres, dispersió i densitat a QGIS

Mostrar les eines sobre la mateixa selecció de 3.762 consumidors ICAEN amb
potència coneguda: diàleg de coordenades mitjanes amb POT_KW com a pes,
el·lipse per geometria d'expressió i resultat sobre els punts, recompte en
quadrats d'1 km i mapa de calor de radi 1.500 m i píxel 100 m.

La capa de paràmetres de dispersió conté els semieixos de la covariància
poblacional i l'azimut calculats a preparar_estadistica.py; no són límits de
confiança. La densitat del mapa final aplica a la sortida quartic crua el
factor 3e6/(pi*1500^2), per expressar punts/km². Conservar separades la
captura del diàleg i aquesta normalització. Una fletxa per idea; no tapar
els controls. Fonts: ICAEN i límit comarcal ICGC.
