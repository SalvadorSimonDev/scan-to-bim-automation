Genera el scaffold completo de un script Python para pyRevit (Revit API) listo para producción.

Descripción del script: $ARGUMENTS

El scaffold debe incluir obligatoriamente:
1. Imports estándar de Revit API (`Autodesk.Revit.DB`, MEP namespaces relevantes).
2. Referencias a `doc` y `uidoc` desde `__revit__`.
3. `FilteredElementCollector` tipado (ajustado a los elementos descritos).
4. Bloque `Transaction` con nombre descriptivo, `t.Start()`, `t.Commit()` en try y `t.RollBack()` en except.
5. Output de resultados con `output.print_md()` de pyRevit (tabla markdown con columnas: ID, Nombre, Estado).
6. Bloque `if __name__ == '__main__':` para ejecución standalone si aplica.

Entrega solo el código. Sin explicaciones largas. Agrega comentario de una línea solo donde el WHY no sea obvio.
