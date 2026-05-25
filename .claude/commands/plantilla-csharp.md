Genera el scaffold completo de un comando externo en C# para el Revit SDK listo para producción.

Descripción del comando: $ARGUMENTS

El scaffold debe incluir obligatoriamente:
1. Namespace y clase que implementa `IExternalCommand`.
2. Método `Execute(ExternalCommandData, ref string, ElementSet)` con firma correcta.
3. Referencias a `doc`, `uidoc`, `app` obtenidas desde `commandData`.
4. Bloque `using (Transaction t = new Transaction(doc, "NombreAccion"))` con `t.Start()`, `t.Commit()` y manejo de `OperationCanceledException`.
5. Retorno `Result.Succeeded`, `Result.Failed` y `Result.Cancelled` en los casos correspondientes.
6. Registro de errores con `failureMessage` (el parámetro ref string del método Execute).
7. `[Transaction(TransactionMode.Manual)]` attribute en la clase.

Entrega solo el código C#. Sin explicaciones. Comentario de una línea solo donde el WHY no sea obvio.
