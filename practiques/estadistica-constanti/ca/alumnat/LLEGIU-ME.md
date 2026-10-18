---
title: "Pràctica: punts, centres i dispersió a Constantí"
author: Benito Zaragozí
lang: ca
date: "Edició: 18 d'octubre de 2026"
content_status: approved
---

# Què expliquen els punts de Constantí?

Una concentració de punts no és necessàriament una concentració de potència. Compararem el nombre de registres, la seua localització i els pesos abans de dibuixar resums de dispersió i superfícies de densitat. Tot el recorregut utilitza el mateix conjunt municipal.

Els punts de l'ICAEN representen consumidors associats a instal·lacions d'autoconsum, no la petjada dels panells. Hi ha **124 registres**, dels quals **98 tenen una potència publicada** i 26 només un interval. Les coincidències de coordenades es conserven. La suma coneguda és **2.770 kW**; una dada absent no es converteix en zero.

**El professor indicarà a classe quins apartats i exercicis són obligatoris dins del 70% de la qualificació**, i ho recollirà a la tasca de Moodle. Aquesta guia ofereix un recorregut complet; la selecció de classe determina què s'ha de lliurar. Les ampliacions permeten aprofundir i aspirar a l'excel·lent, amb una pregunta i resultats justificats, sense substituir els obligatoris.

## Obrir el paquet

1. Descomprimeix el ZIP complet en una carpeta pròpia. Llegeix aquest PDF i conserva l'estructura de carpetes.
2. Utilitza **QGIS 3.44 LTR**. Les operacions d'aquesta pràctica són de Processament de QGIS; el mapa de calor no necessita Hotspot Analysis.
3. Al panell **Explorador**, crea una connexió GeoPackage a `payload/data/estadistica-constanti.gpkg` i desplega-la. Obre el projecte **inici** guardat dins del GeoPackage.
4. Comprova **EPSG:25831** i el·lipsoide **Cap / NONE**. Les longituds planes són en metres.
5. Crea `treball/` al costat de `payload/`. Desa-hi les teues sortides i una còpia del projecte; conserva el GeoPackage d'inici.

| Entrada | Contingut | Funció |
| --- | --- | --- |
| `punts` | 124 registres municipals | Comptar localitzacions i descriure la dispersió |
| `coneguda` | 98 potències publicades | Sumar kW sense imputar valors absents |
| `pesos` | 124 registres, amb `w_mid` i `imputat` | Comparar el centre dels registres amb un escenari de pesos |
| `malla` | 90 quadrats d'1 km de costat | Agregar recompte i potència coneguda |
| `limit` | Límit de Constantí | Situar l'àmbit municipal |
| `ortofoto` | Retall local de l'ICGC 2025 | Reconèixer els llocs i interpretar el mapa |

Table: Entrades preparades i funció en la pràctica.

La font local DejaVu Sans de `payload/data/fonts/` forma part dels recursos del projecte. Conserva-la amb el paquet. L'ortofoto és un retall del servei WMS ICGC de 2025; no cal connectar-se al servei per treballar.

![Punts de Constantí, límit municipal i ortofoto que permeten situar el cas.](captures/c4-constanti-dades.png){width=100% height=380pt}

# Recompte i potència per quadrats

Obre **Procés → Caixa d'eines**, o utilitza **Ctrl+Alt+T**. Cerca **Compta els punts al polígon**, `native:countpointsinpolygon`.

1. Polígons: `malla`. Punts: `punts`. Deixa buits pes i classe.
2. Camp de recompte: `n_punts`. Desa una capa `recompte` en un GeoPackage nou de `treball/`.
3. Comprova **90 files** i suma **124**. Representa `n_punts` amb intervals i conserva els punts damunt de la malla.
4. Repeteix sobre la capa de recompte amb els punts de `coneguda`, pes `POT_KW` i camp `kw_pub`.
5. Comprova que la suma de `kw_pub` és **2.770 kW**. Els 26 registres sense xifra no aporten un pes inventat.

![Accés a l'eina de recompte i mapa de Constantí.](captures/c4-recompte-caixa.png){width=95% height=380pt}

El quadrat del nucli amb més registres conté **48 punts i 268 kW publicats**. El quadrat amb més potència coneguda té **17 registres i 891 kW**. Identifica'ls per les coordenades mínimes **349500/4557000** i **345500/4558000 m**.

**Conserva:** la capa amb les dues variables, les sumes i una explicació de per què els dos màxims no coincideixen. Cada quadrat té 1 km²: el valor de recompte també es pot llegir com registres/km² en aquest suport concret.

# Centre dels registres i centre ponderat

La capa `pesos` preserva `POT_KW`. Només quan falta la xifra, `w_mid` assigna el punt mitjà de l'interval: **2,5, 15 o 62,5 kW**. L'escenari suma **2.970 kW**: 2.770 publicats i 200 assignats. És una estimació de treball, no una nova observació.

1. Cerca **Coordenades mitjanes**, `native:meancoordinates`, a Anàlisi vectorial. També és accessible des de **Vectorial → Analysis Tools**.
2. Entrada: `pesos`. Deixa pes i ID únic buits. Desa `centre_registres`.
3. Repeteix amb `w_mid` com a pes, ID buit, i desa `centre_ponderat`.
4. Cada resultat és un punt. Superposa'ls amb el límit, els punts i la vista de pesos proporcionals.

![Centre dels registres i centre ponderat sobre el mateix territori.](captures/c4-centres-resultat.png){width=95% height=380pt}

El desplaçament és d'uns **1.832 m cap a l'oest i una mica al nord**. El registre de 450 kW representa el 15,2% del pes central; els cinc pesos més grans, el 37,4%. El centre resumeix un equilibri i pot caure en un lloc sense registres: no recomana on instal·lar una activitat.

**Conserva:** els dos centres, un mapa amb noms i una interpretació que distingisca nombre de registres, potència publicada i pes assignat.

# Cercle i el·lipse de dispersió

El cercle resumeix una distància quadràtica al centre; l'el·lipse descriu l'allargament segons dues direccions. Per practicar-ne el dibuix utilitzarem els paràmetres de referència del mateix conjunt de 124 punts.

| Paràmetre | Valor de referència |
| --- | ---: |
| Radi del cercle | 2.000,6564 m |
| Semieix major de l'el·lipse | 1.934,4377 m |
| Semieix menor | 510,4672 m |
| Azimut del semieix major | 110,22° |

Table: Paràmetres de dispersió per dibuixar els resums sobre el centre dels registres.

1. Pren **el teu `centre_registres`**, no el centre ponderat, com a entrada de **Geometria segons l'expressió**, `native:geometrybyexpression`.
2. Tria sortida Polígon i executa aquesta expressió per al cercle:

```text
make_circle($geometry, 2000.6564, 72)
```

3. En una segona execució, sobre el mateix centre, dibuixa l'el·lipse:

```text
make_ellipse($geometry, 1934.4377, 510.4672, 110.22, 72)
```

4. Desa les dues capes a `treball/`, amb farciment transparent i contorns diferents. Mantén visibles els 124 punts, el centre, el límit i l'ortofoto.

![Cercle i el·lipse de referència sobre els punts de Constantí.](captures/c4-cercle-ellipse.png){width=95% height=380pt}

Les xifres impreses estan arrodonides; la referència docent conserva els paràmetres complets. Els semieixos són la meitat de les longituds completes. Aquests contorns **no indiquen un percentatge fix de punts, una cobertura de servei ni un interval de confiança**.

**Conserva:** les dues geometries, un punt exterior i un espai interior amb pocs registres identificats al mapa. Explica què mostra el radi i què afegeix l'allargament de l'el·lipse.

# Mapa de calor i radi de contribució

Cerca **Mapa de calor**, `qgis:heatmapkerneldensityestimation`, dins d'Interpolació.

1. Entrada: `punts`, **sense pes**. Radi **500 m** i mida de píxel X/Y **100 m**.
2. A paràmetres avançats: kernel **Quartic** i valors de sortida **Raw**. Desa `kernel-500-raw.tif`.
3. Repeteix amb radi **1.500 m**, mateix píxel i sense pes.
4. Per convertir el primer ràster en registres/km², utilitza Calculadora ràster:

```text
"kernel-500-raw@1" * 3 * 1000000 / (3.141592653589793 * 500^2)
```

5. Adapta nom i radi a 1.500 m. Conserva NoData i aplica **la mateixa escala de color** a les dues densitats.

![Eina de mapa de calor localitzada sobre el cas de Constantí.](captures/c4-kernel-caixa.png){width=95% height=380pt}

El radi decideix fins on contribueix cada punt; el píxel decideix amb quin detall es desa la superfície. Raw no equival directament a registres/km². La suma de les densitats multiplicada per l'àrea de píxel, **0,01 km²**, s'aproxima a 124 registres. Un pic de color no és un contrast estadístic.

**Conserva:** els dos ràsters raw, els dos normalitzats, unitats, paràmetres i una comparació sobre els punts. Identifica una diferència que desaparega quan augmenta el radi.

# Ampliacions, preguntes obertes i aplicacions

Escull una pregunta que no quedi resolta només reproduint les captures. Mantén una referència, registra què canvies i explica si la conclusió és estable. No cal fer totes les propostes:

- **Suport del recompte.** Repeteix l'agregació amb una altra mida de quadrat o amb l'origen de la malla desplaçat. El lloc amb més registres continua sent el mateix? Separa el canvi d'unitat espacial del canvi en les dades.
- **Pesos i valors absents.** Compara el centre dels registres, el de les potències publicades i escenaris separats per als intervals sense xifra. Quant varia el centre? Conserva `POT_KW` i identifica els valors assignats; una estimació no és una observació nova.
- **Radis i discretització.** Prova un radi intermedi i altres mides de píxel, canviant un paràmetre cada vegada. Quines concentracions persisteixen? Mantén unitats i escala de color comparables i revisa la integral de la densitat.
- **Un altre municipi.** Amb dades adequades i d'acord amb el professor, compara Constantí amb un municipi proper. Recalcula els centres i els paràmetres de dispersió: les constants del cercle i l'el·lipse de Constantí no serveixen per a un altre conjunt.

Una aplicació geogràfica pot ser descriure com es distribueix l'autoconsum dins d'un municipi o comparar l'estructura de diversos registres territorials. Quines dades sobre edificis, habitants o activitats ajudarien a interpretar una concentració? Com distingiries una diferència territorial d'una diferència de cobertura del registre? Formula què podria aportar el mapa a una diagnosi i què encara no permet explicar.

Els resums descriptius no demostren causes ni significació estadística. Una concentració de punts o kW tampoc determina per si sola un lloc adequat per a una nova instal·lació.

# Preparar l'informe

Organitza el PDF com una resposta a una pregunta:

1. **Pregunta i selecció de classe.** Situa Constantí i identifica els apartats obligatoris anunciats pel professor i l'ampliació escollida, si n'hi ha.
2. **Dades i decisions.** Explica què representa cada punt, les dates, els valors absents i els pesos. Identifica el suport espacial, el CRS i els paràmetres utilitzats.
3. **Procediment i controls.** Presenta els passos que condicionen el resultat. Per als apartats seleccionats, conserva sumes, centres, paràmetres de dispersió o controls de densitat, amb unitats.
4. **Resultats i comparació.** Inclou una taula de controls i els mapes necessaris. Mantén escales comparables i diferencia recompte, potència publicada i escenari de pesos.
5. **Interpretació i límits.** Explica què resumeix cada resultat, quina pregunta respon i què no es pot deduir del registre.
6. **Ampliació i aplicació.** Si has fet repeticions o canviat de zona, compara-les amb la referència i proposa una aplicació geogràfica o una comprovació posterior.

## Enregistrar la pantalla i extreure captures

Pots enregistrar fragments de la sessió amb un enregistrador de pantalla, com OBS Studio. Fes primer una prova breu amb QGIS i comprova que són llegibles els camps, els pesos i els paràmetres. Anota els moments dels passos que vols explicar.

En un reproductor de vídeo, pausa el fotograma útil i desa'l amb la funció de captura de fotograma. Retalla el que no aporta informació, sense eliminar el nom de l'eina ni els paràmetres necessaris. Numera cada imatge i escriu un peu que expliqui la decisió o el control. Exporta els mapes finals amb llegenda, escala i unitats, en lloc de limitar-los a una captura de pantalla.

No cal lliurar el vídeo tret que el professor ho indiqui. L'informe ha de seleccionar evidències i interpretar-les, no reproduir tota la gravació ni descriure cada clic.

# Lliurament i fonts

Lliura `estadistica-constanti-cognom.gpkg`, amb els vectors generats; `estadistica-constanti-cognom.qgz`, amb rutes relatives; els TIFF referenciats; i `estadistica-constanti-cognom.pdf`, amb l'informe. El treball ha de permetre comprovar les operacions i interpretacions seleccionades a classe. Mantén tots els fitxers referenciats al costat del projecte i comprova que s'obre després de moure la carpeta completa, amb la xarxa desconnectada.

El **70%** correspon als apartats obligatoris que indicarà el professor. Les ampliacions permeten aspirar a l'excel·lent segons els criteris comunicats a classe i recollits a Moodle; no substitueixen els obligatoris ni garanteixen una nota per haver-les intentat. En una zona alternativa, identifica el cas al nom dels fitxers i conserva les fonts i els controls propis.

- ICAEN: [localització d'instal·lacions d'autoconsum](https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/), extracció del 28/9/2026; data efectiva del conjunt no establerta.
- ICGC: límit municipal del 20/1/2026 i ortofoto 2025. [Condicions d'ús](https://www.icgc.cat/condicions).
- [Manual QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/): eines i significat dels paràmetres.

Les dades representen un registre disponible, amb dates, geometries i atributs de precisió limitada. La conclusió ha d'explicar què resumeix cada operació, sense convertir els resultats en causes o recomanacions de localització.
