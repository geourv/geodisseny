# John Snow i Abraham Wald: fonts, imatges i ús docent

Ampliació demanada per l'autor el4d'octubre de2026, en la sessió local de
revisió del manual. Reserva ampliada a la incidència5:
https://github.com/geourv/geodisseny/issues/5#issuecomment-5974026161.
Es preserven la branca i els esborranys anteriors. C1 i C4 passen a draft;
la bibliografia ja era draft. Sense aprovació de commit o publicació.

## Revisió posterior del mateix dia

L'autor ha demanat encerclar les bombes del mapa en blau. La figura activa
és ara `assets/quarto/figures/john-snow-pous.qmd`, que genera un SVG amb
la imatge JPEG original incrustada i13cercles editables. Les posicions són
a `context/inputs/snow-pous.json`, en píxels de l'original3045×2840.
Els13símbols PUMP s'han revisat individualment; els cercles són identificadors
gràfics, no buffers. L'original conserva el seu SHA i el domini públic permet
afegir-hi anotacions. El peu acredita original i intervenció separadament.
La comprovació del SVG construït recupera el JPEG incrustat i confirma el hash.

La reorganització de C4 situa Snow com a primer cas després de la introducció.
Els crèdits i els enllaços de drets de totes dues imatges es concentren a
`data-caption-source`; s'han eliminat els paràgrafs administratius del cos.
Els bytes originals i les referències es conserven. El lliurament actual és el PDF233p,
amb la preparació QGIS documentada a `context/dades/punts-tarragones.md`.
Les xifres i reviews de225p que segueixen corresponen a la integració inicial.

## Ubicació i funció en la integració inicial

- C4, després de les preguntes sobre distribucions puntuals i abans del
  registre ICAEN: John Snow, unitat de les marques, ponderació de defuncions,
  població exposada, accés a l'aigua, investigació i cobertura del registre.
  Nou ancoratge john-snow i activitat de lectura del mapa.
- C1, després de població/mostra/registre: biaix de supervivència com a cas
  de selecció. Distinció entre els avions que tornaven i el conjunt d'interès;
  transferència a inventaris de comerços actius. Nou ancoratge
  biaix-supervivencia i activitat amb un inventari fictici de comerços.
- C4 enllaça amb C1 per recuperar la pregunta sobre els casos absents.
  No s'equipara tota dada absent amb biaix de supervivència.

## John Snow: font primària

Snow, John(1855), On the Mode of Communication of Cholera, segona edició,
John Churchill, Londres. Exemplar Wellcome a Internet Archive:
https://archive.org/details/b28985266.
Metadades verificades a https://archive.org/metadata/b28985266 i text OCR a
https://archive.org/download/b28985266/b28985266_djvu.txt.
La taula de mapes i les pàgines38–52 s'han consultat, no només la fitxa de Commons.

- La taula de mapes descriu una barra negra per defunció, situada a la casa
  del cas mortal, i les bombes accessibles al públic; període19agost–30setembre1854.
- Pàgines39–40: visites, registres i entrevistes sobre l'aigua consumida;
  entrevista del7de setembre i retirada de la maneta l'endemà.
- Pàgina42: aigua pròpia del workhouse de Poland Street i absència de consum
  de la bomba entre els treballadors de la cerveseria. El text evita atribuir
  protecció causal a la cervesa per si mateixa.
- Pàgines44–45: aigua transportada a una resident lluny de Broad Street.
- Pàgina45: casos no cartografiables per adreces absents després de trasllats.
- Pàgines46–47: bombes, camins indirectes cap a Rupert Street i diferències
  de població. La línia discontínua descriu l'àmbit de subdistrictes; no es
  presenta com una tessel·lació de Voronoi.
- Pàgines51–52: els nous atacs ja havien disminuït abans del8de setembre.
  Pròleg: primera edició d'agost1849. No es presenta el mapa com una descoberta
  sobtada ni la retirada de la maneta com una prova causal aïllada.

La fitxa Commons indica1854, l'any del brot. Al manual es distingeix de la
publicació de la segona edició i del mapa1 el1855. Referència snow1855cholera.

## Abraham Wald: font acadèmica i límits

Mangel, Marc, i Francisco J. Samaniego(1984), «Abraham Wald's Work on Aircraft
Survivability», Journal of the American Statistical Association79(386):259–267.
DOI https://doi.org/10.1080/01621459.1984.10478038.
Metadades contrastades amb Crossref, la pàgina de l'editor i la coberta del PDF.
La llista de publicacions de l'autor dona259–271; s'utilitza259–267, coincident
entre editor, Crossref i el PDF.1984 és l'any de publicació;2012 és l'alta digital.

La pàgina259 identifica el treball de Wald al Statistical Research Group,
els memoràndums de guerra, els avions retornats i el problema dels perduts no
observables. Còpia pública de consulta enllaçada des de la pàgina de l'autor:
https://people.ucsc.edu/~msmangel/Wald.pdf. PDF de10pàgines, amb coberta i
9pàgines de l'article, retingut només a /tmp/opencode per a consulta; no es
redistribueix al repositori ni al lloc. SHA
`7e8d614c5015f355dc1ff54b84131d8fa6cb4aab52df68aa56f3909a739ae042`.

L'exemple explica la selecció condicionada al retorn. La distribució dels
impactes entre supervivents no és la distribució de tots els avions;
s'expliciten els supòsits d'exposició i probabilitat de retorn. No es reprodueix
una anècdota de confrontació amb comandaments ni s'inventa un registre d'impactes.
Referència mangel1984wald.

## Imatges i drets

Fonts executables i procedència:
`context/dades/preparar_imatges_historiques.py` i
`context/inputs/imatges-historiques.json`. El primer --download comprova la
mida i el SHA-1 publicat abans de retenir el fitxer; després la comprovació
és offline. S'hi registra SHA-256, URL d'arxiu, versió, autoria i drets.
Les imatges es copien byte a byte; no s'han retocat ni reconstruït.

| Fitxer | Drets i atribució | Versió i mida |
| --- | --- | --- |
| assets/img/historia/john-snow-1855.jpg | Domini públic, PD-Art/PD-old-100-expired; John Snow, litografia C. F. Cheffins | Commons22juny2007,3045×2840px,1.183.741bytes |
| assets/img/historia/biaix-supervivencia.svg | CC BY-SA4.0; Martin Grandjean(vector), McGeddon(imatge), US Air Force(concepte del diagrama) | Commons21març2021,107.968bytes |

- Snow: https://commons.wikimedia.org/w/index.php?title=File:Snow-cholera-map-1.jpg&oldid=1188845148.
  S'utilitza el fitxer arxivat de2007 d'1,18MB, anterior a la substitució de
  més de20.000píxels i18,38MB. PDM és una marca de domini públic, no CC BY-SA
  ni la llicència del text de la pàgina. SHA-256
  `0ff06d6af2045f20f730b5cf00c134173807c4cba9380823e26a66fa3e62ef1c`.
- Avions: https://commons.wikimedia.org/w/index.php?title=File:Survivorship-bias.svg&oldid=1176240698.
  És un dibuix modern amb impactes hipotètics; el peu ho diu expressament.
  Es conserven els autors, l'enllaç de procedència i el de CC BY-SA4.0,
  diferenciant els drets de la il·lustració dels del text del manual. SHA-256
  `6f49564ea8e32f9d3f20860a2ee109fe3cb9cebf1d2d89b118a4566066e0b543`.

Les dues noves entrades bibliogràfiques declaren manual=true i
manual_selected=false perquè també apareguin a la bibliografia general web.

## Revisió i estat del lliurament local

- Imatges comprovades offline contra la versió declarada i el seu manifest;
  les còpies d'_site són idèntiques byte a byte. Crèdits, enllaços a Commons
  i enllaços de drets visibles al web i al PDF.54referències, sense duplicats.
- C1 té16imatges i C4 en té13. Revisats els dos capítols i la bibliografia
  a1440/390px:29imatges dels capítols carregades, cap error MathJax, citació
  crua, ancoratge perdut ni overflow. Enllaç de Snow al cas dels avions comprovat.
- La primera comprovació del navegador es va avançar a la càrrega dels
  recursos. S'ha ajustat l'espera del guió de QA a document complet i imatges
  descodificades; la passada completa posterior és correcta.
- Prosa i qualitat de fonts correctes; C1 conserva l'avís mecànic conegut
  «I i» a «Errors de tipus I i II», nombre romà i conjunció, no duplicació.
  Site-check executat abans del build. L'importador és codi del consumidor;
  no s'ha llegit ni modificat codi intern dels proveïdors.
- PDF225p. Figures1.2 i4.1, textos, activitats, crèdits i bibliografia
  inspeccionats. Corregit el pas de Coordenades mitjanes perquè el token
  native:meancoordinates no sobresortís després del canvi de paginació;
  límits finals correctes, sense alterar paràmetres o resultats de la pràctica.
- PDF SHA `62d9cc42e35920dbabbe834bad49d3f2fe689e4562e0133ae195041d86d8b2ef`;
  còpia servida idèntica, fresh/artifacts_valid. Rebut preview SHA
  `78d3cff16f1ee55f920ad1005183849c3ec2e5c5a5111d8bdddd1e204c5f095b`.
- Review C1 `wald-supervivencia-evidencia-20261004`, revisió28, digest
  `bd2f7b604683b5417bd0ebd8bb20eb1e5b52efcb451dfefc65ca2331ef4b98d2`.
- Review C4 `snow-punts-evidencia-20261004`, revisió29, digest
  `3e0476f5d07c15ca1d0d49f9ef0aa12a57ca9fdfb501261e256908e3845ed2d2`.
- Review bibliografia `bibliografia-snow-wald-copia-20261004`, revisió30,
  digest `86bbbafb3f64d084e2f5f4897f9e6666a754e95647ccf8ef39f3a2dee4e20826`.
  Cap troballa nova;27reviews/23stale. Les passades no aproven contingut.

Evidències temporals: /tmp/opencode/geodisseny-snow-wald-review.json,
geodisseny-seven-browser.json, geodisseny-snow-wald-p*.png i les vistes web
geodisseny-area-{1,4}-{1440,390}.png. Serve local32768 obert. C1, C3, C4 i
bibliografia en draft; sense commit ni publicació. El main públic continua
amb la versió199p autoritzada anteriorment. _data/metrics.yml i pins sense diff.
