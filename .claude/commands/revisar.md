Audita el siguiente código contra las reglas del proyecto BIM Scan-to-BIM:

```
$ARGUMENTS
```

Evalúa estos puntos en orden y responde con una tabla markdown:

| # | Regla | Estado | Problema encontrado |
|---|---|---|---|
| 1 | Transaction con RollBack en except | ✅/❌ | ... |
| 2 | FilteredElementCollector con OfCategory+OfClass | ✅/❌ | ... |
| 3 | Sin iteración doble sobre colecciones grandes | ✅/❌ | ... |
| 4 | LookupParameter con check None antes de escribir | ✅/❌ | ... |
| 5 | Sin TaskDialog/UI bloqueante en flujo principal | ✅/❌ | ... |
| 6 | Lotes de máx 500 elementos por Transaction | ✅/❌ | ... |
| 7 | Output de resultados (no print nativo) | ✅/❌ | ... |

Tras la tabla: lista solo los problemas con ❌ y el fix exacto (código corregido, no descripción).
