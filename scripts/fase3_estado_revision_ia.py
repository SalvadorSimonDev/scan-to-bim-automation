# -*- coding: utf-8 -*-
# [FASE 3] Auditoría de Conectividad MEP — Estado_Revision_IA
# Revit API / pyRevit (IronPython 2.7)
# Tecnología: pyRevit | Versión Revit target: 2023–2025

import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import (
    FilteredElementCollector,
    BuiltInCategory,
    BuiltInParameter,
    Transaction,
    ConnectorType,
)
from Autodesk.Revit.DB.Plumbing import Pipe
from Autodesk.Revit.DB.Mechanical import Duct

doc   = __revit__.ActiveUIDocument.Document
output = script.get_output()
output.close_others()

# ── Constantes ───────────────────────────────────────────────────────────────
PARAM_ESTADO    = "Estado_Revision_IA"
ESTADO_VALIDADO = "Validado Automático"
ESTADO_PENDIENTE = "Pendiente de Validar Humana"
FT_TO_MM        = 304.8
LOTE            = 500           # elementos por Transaction


# ── Helpers de geometría ──────────────────────────────────────────────────────
def _param_double(elem, bip):
    p = elem.get_Parameter(bip)
    return p.AsDouble() if p and p.HasValue else 0.0


def datos_tuberia(pipe):
    """Devuelve (diametro_mm, longitud_mm)."""
    d = _param_double(pipe, BuiltInParameter.RBS_PIPE_DIAMETER_PARAM) * FT_TO_MM
    l = _param_double(pipe, BuiltInParameter.CURVE_ELEM_LENGTH)       * FT_TO_MM
    return round(d, 1), round(l, 1)


def datos_conducto(duct):
    """Devuelve (dimension_mm, longitud_mm). Para rectangular usa el ancho mayor."""
    l = _param_double(duct, BuiltInParameter.CURVE_ELEM_LENGTH) * FT_TO_MM
    # Circular
    d = _param_double(duct, BuiltInParameter.RBS_CURVE_DIAMETER_PARAM)
    if d > 0:
        return round(d * FT_TO_MM, 1), round(l, 1)
    # Rectangular — devuelve ancho x alto como string, tamaño = max(w, h)
    w = _param_double(duct, BuiltInParameter.RBS_CURVE_WIDTH_PARAM)
    h = _param_double(duct, BuiltInParameter.RBS_CURVE_HEIGHT_PARAM)
    return round(max(w, h) * FT_TO_MM, 1), round(l, 1)


# ── Validación de topología ───────────────────────────────────────────────────
def ambos_extremos_conectados(elem):
    """
    True si todos los conectores físicos del elemento tienen contraparte.
    Excluye conectores lógicos (de sistema MEP), que no representan uniones físicas.
    """
    try:
        fisicos = [
            c for c in elem.ConnectorManager.Connectors
            if c.ConnectorType != ConnectorType.Logical
        ]
        # Un tramo válido tiene exactamente 2 extremos físicos, ambos conectados
        return len(fisicos) >= 2 and all(c.IsConnected for c in fisicos)
    except Exception:
        return False


# ── Collector ─────────────────────────────────────────────────────────────────
def recopilar_mep():
    pipes = list(
        FilteredElementCollector(doc)
        .OfCategory(BuiltInCategory.OST_PipeCurves)
        .OfClass(Pipe)
        .ToElements()
    )
    ducts = list(
        FilteredElementCollector(doc)
        .OfCategory(BuiltInCategory.OST_DuctCurves)
        .OfClass(Duct)
        .ToElements()
    )
    return pipes, ducts


# ── Procesamiento en lotes ────────────────────────────────────────────────────
def procesar_lote(lote_items):
    """
    lote_items: lista de (elem, fn_datos)
    Procesa en una única Transaction y devuelve lista de resultados para el reporte.
    """
    resultados = []
    t = Transaction(doc, "BIM_Estado_Revision_IA")
    try:
        t.Start()
        for elem, fn_datos in lote_items:
            dim_mm, long_mm = fn_datos(elem)
            estado = ESTADO_VALIDADO if ambos_extremos_conectados(elem) else ESTADO_PENDIENTE

            param = elem.LookupParameter(PARAM_ESTADO)
            escrito = False
            if param is not None and not param.IsReadOnly:
                param.Set(estado)
                escrito = True

            resultados.append({
                "id":       elem.Id.IntegerValue,
                "tipo":     elem.__class__.__name__,
                "dim_mm":   dim_mm,
                "long_mm":  long_mm,
                "estado":   estado,
                "escrito":  escrito,
            })
        t.Commit()
    except Exception as e:
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
        raise e

    return resultados


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# ── Reporte de salida ─────────────────────────────────────────────────────────
def imprimir_reporte(resultados, n_pipes, n_ducts):
    total     = len(resultados)
    validados = sum(1 for r in resultados if r["estado"] == ESTADO_VALIDADO)
    pendientes = total - validados
    sin_param  = sum(1 for r in resultados if not r["escrito"])

    output.print_md(f"""
## [FASE 3] Auditoría MEP — Estado_Revision_IA
| Métrica | Valor |
|---|---|
| Tuberías (Pipe) | {n_pipes} |
| Conductos (Duct) | {n_ducts} |
| **Total procesado** | **{total}** |
| ✅ Validado Automático | {validados} ({validados / total * 100:.1f}%) |
| ⚠️ Pendiente de Validar Humana | {pendientes} ({pendientes / total * 100:.1f}%) |
| ❌ Sin parámetro `Estado_Revision_IA` | {sin_param} |
""")

    if sin_param > 0:
        output.print_md(
            f"> **Acción requerida:** {sin_param} elemento(s) no tienen el parámetro compartido "
            f"`Estado_Revision_IA` en el proyecto. Crea el parámetro en el gestor de parámetros "
            f"compartidos antes de volver a ejecutar."
        )

    if resultados:
        muestra = resultados[:100]
        filas = []
        for r in muestra:
            icono = "✅" if r["estado"] == ESTADO_VALIDADO else "⚠️"
            escrito_icono = "✅" if r["escrito"] else "❌"
            filas.append(
                f"| {output.linkify(r['id'])} | {r['tipo']} "
                f"| {r['dim_mm']} | {r['long_mm']} "
                f"| {icono} {r['estado']} | {escrito_icono} |"
            )

        output.print_md(
            f"\n### Detalle ({'primeros 100' if len(resultados) > 100 else 'todos'})\n"
            "| ID | Tipo | Ø/Dim (mm) | Longitud (mm) | Estado | Param |\n"
            "|---|---|---|---|---|---|\n" +
            "\n".join(filas)
        )


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    pipes, ducts = recopilar_mep()
    todos = [(p, datos_tuberia) for p in pipes] + [(d, datos_conducto) for d in ducts]

    if not todos:
        output.print_md("**Sin tuberías ni conductos en el documento activo.**")
        return

    resultados = []
    for lote in chunks(todos, LOTE):
        resultados.extend(procesar_lote(lote))

    imprimir_reporte(resultados, len(pipes), len(ducts))


main()
