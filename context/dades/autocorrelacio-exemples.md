# C5: renda, edificació i atributs puntuals

## Revisió pedagògica posterior

La primera ampliació documentada a continuació ha estat revisada per
l'autor. El material vigent dels capítols4i5 es registra a
`context/dades/constanti-pedagogia.md`: fil municipal continu, kW originals
abans de transformacions, operacions visibles i prova amb permutacions.
Les correlacions exploratòries d'aquest document es conserven com a
recerca i controls, sense una regressió feble com a conclusió docent.
El ZIP r2 interromput es conserva complet després de recuperació, amb
rebut històric propi; no substitueix el paquet nou de Constantí.

Tasca [#7](https://github.com/geourv/geodisseny/issues/7), branca `content/7-autocorrelacio-exemples`. Preparació del 5/10/2026 per a revisió humana. C0, C5 i bibliografia tornen a `draft`; cap aprovació ni publicació de la revisió nova.

## Fonts i seleccions

- **INE, ADRH 2023**, publicat el 21/10/2025. [Taula 31223](https://www.ine.es/jaxiT3/Tabla.htm?t=31223&L=0), indicador «Renta neta media por persona»; [CSV complet](https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/31223.csv), 5.714.767 bytes, SHA-256 `894f8d0bd143347b7b0ad677db31d7a04c56ce26e231a85379db00304938bbf2`.
- [Condicions de reutilització INE](https://www.ine.es/dyngs/AYU/index.htm?cid=125): informació estadística CC BY 4.0, llevat d'indicació contrària; atribució, elaboració pròpia i darrera actualització identificades. La metodologia i les fonts són de l'INE, no s'atribueix patrocini o validació del manual a l'organisme.
- [Taula 31231, població](https://www.ine.es/jaxiT3/Tabla.htm?t=31231&L=0), CSV 6.478.308 bytes, SHA `c9aaa295b835447422468a35ab316623cc917516d79b6bfe50557b23592bef38`.
- [Metodologia ADRH, octubre 2025](https://www.ine.es/metodologia/metodologia_adrh.pdf), còpia de 379.382 bytes, SHA `96d2cfcddc73c3d76c232e23a1dc37ddf46fbc100de03f426043c04771ed291d`. Pàgines 4, 6–9: renda de l'any natural, població d'1 de gener següent; registres administratius, població trobada, mínims i acotació d'extrems. No és simplement una variable recollida en un qüestionari censal.
- **151 seccions ICGC/Idescat d'1/1/2024**, geometries completes de `tmp/dades-docents/seccions/originals/seccions-20240101.zip`. La unió per `cusec` és completa: deu dígits INE, no `MUNDISSEC`. Dos codis de la sèrie temporal —4314809005 i 4314809006— tenen files buides el 2023 i no entren en les geometries; no s'han imputat. Cap renda absent; població mínima158. Llicència de les seccions: CC BY 4.0.
- **Cadastre Buildings**, feed de Tarragona21/8/2026 i mapping INE–DGC de `preparar_seccions.py`. Revisats hashes de tots els originals. Es conserven40.180 objectes d'entrada, quatre sense assignació i un identificador reutilitzat en objectes municipals diferents. Els38.689 funcionals assignats coincideixen secció per secció amb el recompte anterior.
- **Petjada**, àrea plana EPSG:25831 de la geometria Building, no superfície de plantes ni coberta útil. Assignació de l'edifici sencer pel punt interior, coherent amb el nombre d'edificis:135 petjades travessen una vora. Total13.566.378,212727593m². Cap unió individual consumidor→edifici.
- **ICAEN**, mateix original immutable de28/9/2026: `tmp/dades-docents/moodle/autoconsum-tarragona-20260928.gpkg`, SHA `1c8b4bda31ac5bfa35fd8ac4b1fbf36990d01065590c673b579e0670291ac9c8`. La data efectiva no s'ha verificat. Constantí:124registres;98amb potència publicada, suma2770kW,94posicions. Cas principal sense imputacions.
- Atributs anteriors de seccions: `tmp/dades-docents/seccions/seccions-analisi.gpkg`, SHA `84d7a33bfa8dab8089bb852e447947c92a95da3bf733161663e24a2be98523af`. **Els pesos nous es construeixen amb les geometries completes del ZIP original**, no amb la còpia simplificada de figures.

Els originals nous, la metodologia i els manifests viuen a `tmp/dades-docents/qgis/autocorrelacio-20261005/`. La figura utilitza un input petit agregat per secció a `context/inputs/autocorrelacio-exemples.json`; els registres ICAEN individuals i els projectes queden al paquet privat.

## Disseny i resultats de les proves

`preparar_autocorrelacio_exemples.py --analyse` conserva **31 proves de variable/veïnatge** i sis comparacions entre variables. Les dues bandes de distància amb illes es documenten sense índex inferencial. No s'ha seleccionat una distància mitjançant l'optimitzador de significació.

- Cinc variables de seccions: renda, mediana d'edat, log1p(kW/100edificis), log1p(kW/1000m²), petjada mitjana. Queen, rook, kNN4 i kNN8 per a cadascuna.
- Mostres: renda151; edat150, exclosa4314807015 (<10dates exactes); potència150, exclosa4314806003 (totes les potències absents). La mostra comuna de correlacions és126.
- Constantí: kNN4/8/12 sobre98potències publicades transformades; bandes500/1000m; tres escenaris heretats sobre124registres; tots els empatats al tall del vuitè, ordre invers i kW crus.
- Diagonalzero i normalització per files; kNN dirigit, sense simetritzar. Veïns externs al Tarragonès o al conjunt municipal no incorporats. IDs ordenats abans del càlcul.
- Contrastos globals: associació **positiva**, cua superior fixada a priori, `(1 + count(sim >= I))/(B + 1)`. 9999permutacions, llavor20261005; es conserva també `esda.p_sim` per comparació.
- Locals de referència: `Moran_Local(..., seed=20261005, n_jobs=1)`, convenció `p_sim` d'esda. BHα0,05 com a sensibilitat exploratòria, sense garantia universal sota dependència.

| Variable | n | I queen | Pseudo-p positiu |
| --- | ---: | ---: | ---: |
| Renda |151|0,571916933|0,0001|
| Edat |150|0,354645577|0,0001|
| Potència per nombre, log1p |150|0,144046770|0,0028|
| Potència per petjada, log1p |150|0,220148634|0,0001|
| Petjada mitjana |151|0,267142788|0,0002|

Constantí: kNN8 log1p I0,632489490; kNN4/12 0,655668178/0,589300479. Incloure tots els empatats dona0,620202609 (8–9veïns). Ordre invers0,632473587. kW crus0,191856301. Escenaris inferior/central/superior0,591282401/0,621062230/0,571433856. Radi500:6illes/10components; radi1000:3illes/7components. Longitud màxima kNN8:2565,713m;14files amb empats al tall.

### Casos de lectura

- A, renda `4314807013`:23239€/persona; tres veïns24068/23235/17187; retard21496,6667; HH, p_ref0,0049, BHsí.
- B, `4314808012`:7379; quatre veïns9879/9934/13523/7577; retard10228,25; LL, p_ref0,001, BHsí.
- C, `4304701002`:7744; veïns13262/13645; retard13453,5; LL però p_ref0,2527, no destacat. Mitjana simple del conjunt15220,3576.
- D, `4314806006`:194edificis,600362,8442m²,1944kW;1002,061856kW/100edificis i3,238042kW/1000m².
- Punt A de Constantí:450kW; veïns100/100/60/30/100/20/60/50. log propi6,111467; retard4,059681; mitjana dels98logaritmes2,488461.

Pearson edat–log_count−0,400954 versus Moran bivariant−0,075342; renda–log_count0,285617 versus0,005458. Renda–log_area Pearson0,326332; edat–log_area−0,281850. Petjada mitjana–log_count0,518408 i petjada mitjana–log_area−0,075764. Relacions ecològiques descriptives, sense prova causal.

La referència antiga de potència per nombre (llavor20260929) té el mateix I, p_global0,0024 i un HH després de BH. La nova llavor no en destaca cap. Es conserva la figura antiga amb la seva llavor explícita i es desenvolupa la variació de Montecarlo prop del tall; no se substitueix silenciosament el resultat anterior.

## QGIS, dependències i controls

Runtime fixat `sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc`: QGIS3.44.11, Python3.13.7, NumPy2.2.4, SciPy1.15.3, libpysal4.13.0, esda2.7.1; metadades de paquet comprovades, Numba0.67.0. esda2.7.1 exigeix Python>=3.11.

Plugin4.0.0, commit `f00561970149787664fc2cabe26a110cc2d4226a` del6/5/2026. S'han consultat README, documentació de distribució, metadades i implementació pública del **connector estadístic** per verificar convencions; no el codi intern dels renderers/capturadors del proveïdor.

- `hotspotanalysis:moranlocal`, renda151:Queen, ROW_STANDARDIZEtrue,9999, TWO_TAILEDfalse. Sortida conservada27HH/23LL/6LH/95NS.
- Mateix algorisme sobre punts98:log_kw,kNN8,Euclidean,ROWtrue,9999,TWO_TAILEDfalse.34HH/41LL/1HL/2LH/20NS.
- `hotspotanalysis:getisordgistar`, renda151:Queen,binari,ROWfalse,9999,TWO_TAILEDtrue.26altes/21baixes/104NS. Fórmula analítica directa de Z contrastada: error màxim `5.329070518200751e-15`.
- Quadrants de QGIS iguals als de referència. Els pseudo-p no són idèntics: el diàleg no exposa llavor i `np.random.seed` no equival a donar `seed` al randomitzador local d'esda. Es conserva cada execució sense atribuir-li la llavor20261005 de la referència.
- El registre Processing només ofereix Moran local i local bivariant, no global. El bloc de consola del capítol reprodueix el global de renda amb el Shapefile: I0,571916933 i p0,0001. La prova de dependències de quatre valors retorna0,5.
- Queen del connector requereix Shapefile i força Queen sobre polígons. No es presenta el selector de kNN com una via vàlida per contrastar pesos dels polígons en aquesta versió.

Instal·lació: fonts del mantenidor i de QGIS per a OSGeo4W/macOS/Flatpak; documentació PySAL per pip/conda. Ubuntu24.04 té libpysal però no esda al catàleg consultat. Conda-forge confirma qgis3.44 en linux-64,linux-aarch64,osx-64,osx-arm64,win-64; libpysal4.13.0 i esda2.7.1 són noarch. **Consulta de catàleg no equival a resolució o instal·lació executada**: només s'ha fet la prova funcional en el runtime Linux fixat. El manual demana comprovar l'entorn efectiu dins de QGIS i no repetir una instal·lació en un Python diferent.

### Preparació executable

Al host, `--fetch` descarrega només les quatre URLs declarades. CSV i PDF metodològic estan fixats a SHA; si canvien al productor, la preparació s'atura. Els originals previs es munten readonly. A dins del runtime fixat, executar `--analyse --qgis --finalise` amb només la destinació nova writable. Al host, `--record` publica l'input agregat de figures i `--docs` utilitza la imatge Pandoc/XeLaTeX fixada.

Les altres fases són `--verify RUTA --report FITXER`, amb el paquet reubicat readonly i sense xarxa, i `--package`, que exigeix controls de portabilitat i PDF, crea un ZIP nou i el segella. Un directori amb `sealed.json` no es regenera. Recomputar els locals del connector crea una altra seqüència de permutació: no sobrescriure un paquet segellat per forçar els mateixos colors.

## Figures i captures

Quatre QMD: `renda-moran`, `autocorrelacio-edat`, `autocorrelacio-denominadors`, `autocorrelacio-relacions`. Renderització pel worker Python immutable d'unaltraweb. Geometries simplificades només per dibuixar; forats preservats amb paths compostos. Etiquetes A/B/C amb punts interiors reals; mapa i diagrama relacionats.

Nou bundles `c5-…` a la recepta `context/qgis/autocorrelacio-exemples.yml`:eines,renda-parametres,renda-resultat,renda-veins,constanti-dades,constanti-parametres,constanti-resultat,gi-parametres,gi-resultat. QGIS català,x11,DPR1,ExploradorGeoPackage desplegat; PNG/SVG/manifests del proveïdor, sense retocs manuals.

La primera selecció per «Local Moran's I» ressaltava la bivariant per coincidència parcial. La recepta final desplega i ressalta el grup LISA; el peu identifica inequívocament l'eina univariant. Per als paràmetres s'espera el diàleg i es verifica directament la casella: Moran marcada, Gi* desmarcada. Els controls inferencials fora de la part visible del diàleg es donen a la taula i al procediment, sense afirmar que siguin visibles a la captura.

Les captures acrediten estats de GUI i resultats calculats; `manual_click_by_click=false`. Els renderers i runtimes compartits no s'han modificat.

## Revisió

Diagnosi editorial inicial `c5-exemples-estructura-20261005`, revisió57: diversitat de suport/indicador, requisits i accés QGIS, lectura local concreta. Findings resolts explícitament a revisions58–60; cinc reviews renderitzades a61–65. Estat final65:50reviews,45stale; les cinc noves són actuals. Les fonts es mantenen en draft per a l'autor.

### Resultat de les comprovacions

- `prose-check`: C0/C5/bibliografia sense findings pendents. `manual-source-quality-check`: sense errors; les figures noves tenen text proporcionat, amb avisos resolts ajustant només les amplades web. Es conserva l'avís anterior de punts-municipis(C4).
- `manual-computation-check`:54/54actuals. `site-check` correcte abans dels builds. Tres blocs Python exactes del capítol executats al runtime QGIS, amb resultats d'importació,0,5 i0,5719/0,0001.
- Web1440/390px:6vistes de C0/C5/bibliografia,17imatges de C5, sense errors MathJax, recursos absents ni desbordament de pàgina.25encapçalaments/ancoratges de la versió anterior conservats; tres referències noves presents.
- PDF local253p,40.710.571bytes, SHA `0890bb1405da1b298a388fc4481024b7aa00ac9e8b7496fa910b96fc25887ef2`. Inspecció de pàgines28,189–190,192,194,196–199,201,203,206–208 i límits de totes les paraules. La taula de sensibilitat de Constantí s'ha abreujat per mantenir-la íntegra en una pàgina. Fons, peus, fórmules i fonts revisats.
- PDF servit al preview idèntic al generat. Rebut `.cache/unaltraweb/manual-pdf-preview.json`, operació `manual-pdf-preview`; fonts modificades en draft. La identificació de previsualització local es manté al lliurament i al rebut; no es pressuposa un bàner HTML que aquest perfil no mostra.
- Cinc rutes privades comprovades amb404: inputJSON,GeoPackage,ZIP,QMD i configuració del capturador. Dades massives fora de Git i de `_site`.
- Portabilitat: `01-renda.qgz`(4capes) i `02-constanti.qgz`(5), muntats a `/dades-classe`, sense xarxa i readonly, sense accés al checkout. Totes les fonts relatives resoltes, SQLite íntegre, recomptes/pseudo-p vàlids i hashes sense canvis.
- GUIA10p i SOLUCIONS3p, inspecció visual i cap desbordament. SHA dels PDF al rebut privat `verificacio-pdf.json`.

### Paquet conservat

`tmp/dades-docents/practica-autocorrelacio-20261005.zip`:61fitxers,27.939.328bytes, SHA `86f6bcbb5443bbd9586b5a62ca27dff94b27150365e9c345c4c6176c5f4098f3`. CRC i hashes de tots els membres comprovats. `sealed.json` declara `private-author-review` i `human_approved:false`. No s'ha pujat a Moodle.

El paquet conserva la còpia del preparador amb què es va generar. Després de segellar s'ha afegit al CLI del repositori una guarda comuna que rebutja també `--fetch` i `--finalise` sobre una destinació segellada; no modifica l'algorisme ni els resultats. La prova negativa de `--finalise` s'ha executat i tots els fitxers del paquet mantenen el seu hash. No s'ha alterat la còpia històrica dins del ZIP.

Rebuts de treball a `/tmp/opencode/autocorrelacio-{portabilitat,main-pdf,web-integrity,editorial-final}.json` i `geodisseny-seven-browser.json`; el registre durable és aquest document i els manifests de figures/captures. No hi ha commit, push ni publicació de la revisió nova.
