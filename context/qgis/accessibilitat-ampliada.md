# Marxa anisòtropa, girs i isòcrones

Captures en català amb QGIS 3.44.11. Utilitzar les dades i els resultats locals
comprovats de distancies-vilaseca-20261001-ampliada. Mostrar O, D i P2 amb
etiquetes visibles. A r.walk.points, distingir MDT en metres, fricció addicional
en segons/metre i inici O. Els segons de sortida es converteixen a minuts.

Mostrar el mapa de temps, les rutes d'anada/tornada i les franges 0–3, >3–6,
>6–12 minuts, amb els mateixos colors que els mapes SVG del manual. Comparar
el pas obert i tancat amb el mateix enquadrament. Mostrar r.contour amb entrada
en minuts, nivells 3,6,12 i mínim 3 punts per evitar contorns degenerats.

La captura nativa de ruta identifica la xarxa i el criteri temporal. La manca
de suport d'una taula de girs està comprovada amb l'esquema públic de l'eina;
no fingir un control de girs a la interfície. L'esquema SVG separat explica
la maniobra condicionada pel tram d'arribada.

Utilitzar PNG anotat, SVG i manifest del proveïdor. No tapar valors de controls,
O/D ni els passos amb les etiquetes. Els càlculs precedeixen les captures.
