from datetime import datetime

class Transaccion:
    def __init__(self, id, producto_id, monto_pagado, vuelto):
        self.id = id
        self.producto_id = producto_id
        self.monto_pagado = monto_pagado
        self.vuelto = vuelto
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "producto_id": self.producto_id,
            "monto_pagado": self.monto_pagado,
            "vuelto": self.vuelto,
            "fecha": self.fecha
        }