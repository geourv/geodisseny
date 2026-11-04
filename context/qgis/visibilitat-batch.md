# Taula de lots i autoemplenat de Viewshed

Captures docents sobre les mostres reals C05/C11/C13/C25/C37 de la TV-3148.
Ús puntual del capturador publicat0.7.0 autoritzat per l'autor el27/10/2026;
controller45fd7b5e… i engine1003721d… ja preparats. Pantalla privada autenticada,
sense DISPLAY del host ni execució de Viewshed. La connexió MCP0.6.1 i el
helper seleccionat de Web no es reetiqueten com a actualitzats.

Mostrar la taula real, no només el botó d'accés. Explicar visualment:

- Fill Down copia una constant de la primera fila a les altres.
- Calculate by Expression calcula un valor per fila existent; @row_number
  comença en0 i les sortides han de ser úniques.
- Add Values by Expression afegeix les coordenades d'un array com a files noves.
- El menú de l'entrada també permet seleccionar capes obertes o fitxers;
  seleccionar objectes de C no equival a omplir Observer location.

Capturar l'editor real amb l'array de cinc punts, acceptar-lo i mostrar la fila
inicial buida. Retirar-la, copiar les constants amb el handler natiu Fill Down,
calcular els noms amb @project_folder i comprovar els cinc valors acceptats,
no només la previsualització. Ressaltar capçaleres/cel·les amb selectors natius
i etiquetes que expliquin la funció. Mostrar també EXTRA desplegat al diàleg
individual, amb els codis1/0/255 i -a_nodata255 llegibles.

La capa C preparada conté id/x/y; pointsalonglines no garanteix aquests camps.
La lectura ha d'explicar la preparació de coordenades i el CRS. La taula plena
ha de permetre identificar també els botons natius de desar i obrir el .batch.
El fitxer és configuració JSON recuperable; no conté les dades ni acredita el
resultat dels algorismes. Conservar fonts, PNG, SVG i manifests del productor.

Els primers renders són proves create-only a sandbox. Revisar llegibilitat,
menús oberts, camps, taula acceptada i aïllament abans del bundle final i dels
PDFs. No canviar les dades científiques ni tornar a executar les179conques.
