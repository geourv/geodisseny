# Torxa, carretera i polígon industrial

Mostra una progressió per a alumnat inicial: identifica la torxa de la Canonja
en l'ortofoto, comprova la intervisibilitat amb punts de la TV-3148, calcula
una conca puntual, suma 37 conques al llarg del recorregut i acaba amb la
visibilitat de l'àrea industrial seleccionada al MCSC2024. El recompte
d'alguna part del polígon incorpora les 57 mostres d'àrea i la torxa T.

Les dades provenen del preparador `context/dades/preparar_visibilitat_costa.py`.
Treballa amb els fitxers locals de `visibilitat-costa-20261002-r3`, EPSG:25831,
QGIS3.44.11 i el runtime fixat. Les cotes absolutes es mantenen en comparar
MDT i MDS; el domini comú exclou mar, elevacions desconegudes i els raigs
que les travessen. Les fonts no són un inventari d'altures de flames.

Dotze captures: ortofoto i MDS amb el mateix enquadrament inicial, torxa,
Viewshed puntual, intervisibilitat, calculadora de cota mínima, mostreig de
carretera, mapa acumulat MDT, buffers +150 m i −150 m, graella d'àrea i
mapa de visibilitat d'algun objectiu industrial. Els diàlegs mostren els
paràmetres preparats; els mapes carreguen resultats calculats i contrastats
amb QGIS natiu. No presentis els diàlegs com a prova d'execució per clics.

Utilitza etiquetes llegibles, QGIS visible i una anotació curta per idea.
El nom de la capa i de l'anotació és «Recinte petroquímic d'estudi»; el mètode
geomètric es documenta als passos. El segon buffer usa l'intermedi del primer.
L'MDS inicial ha de mostrar llegenda de cotes en metres. Emmarca controls i
botons amb requadres, sense tapar-ne el text.
Els resultats i paquets es distribueixen per Moodle i queden fora de Git.
