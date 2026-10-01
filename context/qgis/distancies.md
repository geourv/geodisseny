# Distàncies, xarxa i costos a Vila-seca

Preparar captures de QGIS 3.44 en català per a una pràctica inicial de Geografia.
Les dades i els càlculs són al paquet privat distancies-vilaseca-20261001, amb
projectes QGIS de rutes relatives. Els projectes carreguen resultats calculats
amb les eines indicades i conserven els punts O i D com a capes etiquetades.

Mostrar l'entorn del Camí del Mas de la Plana i el pas P2 sota l'AP-7, la línia
recta, el ràster de distància, la ruta sobre xarxa i les franges accessibles en
3, 6 i 12 minuts. En el model de xarxa, tancar P2 desconnecta O: «sense ruta» no
és una longitud zero. La velocitat uniforme de 5 km/h és un supòsit docent.

Mostrar després la fricció: camins 1, resta 4, edificis i autopista NoData,
excepte els passos admesos. r.cost rep cost per cel·la: la fricció multiplicada
pels 5 m de resolució. r.path parteix de D i segueix les direccions de retorn
cap a O. El cost acumulat són metres ponderats, no minuts ni altituds.

Tancar amb dues captures de la Pineda que mostrin el ràster 1/20 i el cost
acumulat, amb els extrems i els camins visibles. L'MDT és una dada diferenciada;
no participa en aquests costos de resistència.

Captures de finestra QGIS amb llegenda de capes, origen, destí i resultat
identificables. Als diàlegs, enquadrar camps reals amb selectors del proveïdor.
Utilitzar algunes anotacions amb requadre i etiqueta curta, sense tapar valors.
Als mapes, les etiquetes d'O i D provenen de les dades de QGIS; els requadres
del pas i de les superfícies poden ser anotacions cartogràfiques explícites.
Conservar PNG, SVG anotat i manifest. No reconstruir finestres o traduccions.
