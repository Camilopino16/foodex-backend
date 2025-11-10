from decimal import Decimal, ROUND_HALF_UP

def escalar_ingredientes(receta, porciones_objetivo: int):
    factor = Decimal(porciones_objetivo) / Decimal(receta.porciones_base or 1)
    out = []
    for ing in receta.ingredientes.all():
        cant = (ing.cantidad_base * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        out.append({
            "id": ing.id,
            "nombre_ing": ing.nombre_ing,
            "unidad": ing.unidad,
            "cantidad": float(cant),
        })
    return {"porciones": porciones_objetivo, "ingredientes": out, "factor": float(factor)}

def reconciliar_con_inventario(receta, porciones_objetivo: int):
    scaled = escalar_ingredientes(receta, porciones_objetivo)
    faltantes = []
    for ing in receta.ingredientes.all():
        req = Decimal(next(i["cantidad"] for i in scaled["ingredientes"] if i["id"] == ing.id))
        disp = sum(Decimal(c.cantidad_disponible) for c in ing.stock_items.all())
        if disp < req:
            faltantes.append({
                "ingrediente_id": ing.id,
                "nombre_ing": ing.nombre_ing,
                "requerido": float(req),
                "disponible": float(disp),
                "unidad": ing.unidad,
            })
    max_porciones = porciones_objetivo
    for ing in receta.ingredientes.all():
        total_disp = sum(Decimal(c.cantidad_disponible) for c in ing.stock_items.all())
        if ing.cantidad_base > 0:
            posibles = (total_disp / Decimal(ing.cantidad_base) * Decimal(receta.porciones_base)).quantize(Decimal("0"), rounding=ROUND_HALF_UP)
            max_porciones = min(max_porciones, int(posibles))
    return {"scaled": scaled, "faltantes": faltantes, "max_porciones_posibles": max_porciones}
