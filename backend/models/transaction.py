# Modelo de Transaccion
# Una transaccion registra cada compra realizada

from datetime import datetime

def crear_transaccion(id, producto_id, monto_pagado, vuelto):
    # Obtenemos la fecha y hora actual
    fecha_actual = datetime.now()
    fecha_texto = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")

    transaccion = {
        "id": id,
        "producto_id": producto_id,
        "monto_pagado": monto_pagado,
        "vuelto": vuelto,
        "fecha": fecha_texto
    }
    return transaccion

def transaccion_a_diccionario(transaccion):
    resultado = {
        "id": transaccion["id"],
        "producto_id": transaccion["producto_id"],
        "monto_pagado": transaccion["monto_pagado"],
        "vuelto": transaccion["vuelto"],
        "fecha": transaccion["fecha"]
    }
    return resultado
