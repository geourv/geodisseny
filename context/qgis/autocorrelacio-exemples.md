# Petició de captures: renda i potències de Constantí

## Revisió pedagògica vigent

La seqüència del capítol5 comença amb les98potències publicades de Constantí, sense logaritmes. La recepta arrenca una sessió neta amb només punts, límit, ortofoto i veïns, de manera que la llegenda de Moran local es vegi completa. Els registres de450i3kW es recuperen pels seus valors, no per lletres. Es mostra accés, configuració i resultat; després es transfereix el mètode a renda, identificant municipi/secció i etiquetant les rendes veïnes.

Les dades són a `constanti-pedagogia-20261005/`; els resultats de renda provenen de l'execució anterior i les còpies noves només canvien etiquetes i estils. Cap valor estadístic s'ha recalculat per aconseguir altres colors. Els paràgrafs següents descriuen el pla anterior, conservat com a historial; les captures de log_kw i Gi* ja no formen part de la recepta activa.

Preparar una seqüència en català per a estudiants que comencen amb l'autocorrelació. Fer servir les 151 seccions censals de 2024 amb renda neta per persona de 2023 i els 98 registres de Constantí amb potència publicada. Els resultats són els calculats amb Hotspot Analysis 4.0.0 pel preparador del consumidor, conservats al GeoPackage nou. No executar o modificar dades dels paquets anteriors.

Mostrar la Caixa d'eines oberta amb el grup LISA desplegat, que conté Local Moran's I; després, la variable renda i Queen al diàleg. El mapa local ha de tenir una llegenda amb HH/LL/HL/LH i casos no destacats, i identificar A, B i C. Apropar la secció A i els seus tres veïns, etiquetats A/1/2/3, perquè el lector pugui contrastar el càlcul del retard amb la taula del capítol.

Per a Constantí, mostrar punts de potència publicada sobre ortofoto, sense barrejar-hi valors imputats. Ensenyar la configuració log_kw, kNN8, pesos per files i el resultat nominal. Conservar A sobre el registre de 450 kW i les connexions amb els seus vuit veïns. Mostrar finalment la configuració i el mapa Gi* de la renda, amb pesos binaris, sense normalització i pseudo-p bilateral.

L'Explorador ha de mostrar `autocorrelacio.gpkg` desplegat a dalt a l'esquerra. Anotacions escasses amb selectors de controls, sense tapar text ni dibuixar rectangles de l'extensió de les capes sobre els mapes. Les captures de diàleg acrediten configuració; els controls del preparador acrediten execució. No afirmar que s'ha fet el procés manual clic a clic.

La inspecció inicial va motivar una comprovació visual específica de `Row standardization`. La recepta final espera 800 ms després d'obrir el diàleg i assenyala directament el `QCheckBox`: s'ha de veure marcat als dos Moran i desmarcat a Gi*. El resultat s'ha de verificar sobre el PNG; el manifest sense avisos no acredita per si sol l'estat de totes les caselles. L'intent `set_checkbox` va retornar «unknown step action ignored» i s'ha eliminat. Les captures no simulen clics executats ni atribueixen a la GUI la llavor explícita del càlcul de referència.

Fonts, paràmetres, dades seleccionades, resultats i limitacions: `context/dades/autocorrelacio-exemples.md` i `context/dades/preparar_autocorrelacio_exemples.py`.
