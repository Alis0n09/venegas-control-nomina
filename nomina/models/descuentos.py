from django.db import models

from nomina.models.detalle_nomina import DetalleNomina

class Descuento(models.Model):
    detalle_nomina          = models.OneToOneField(DetalleNomina, on_delete=models.CASCADE, related_name='descuento')

    # Préstamos IESS
    prestamo_hipotecario    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prestamo_quirografario  = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Otros descuentos
    prestamo_empresa        = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    anticipos               = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    multas_atraso           = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dias_no_laborados       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    otros_descuentos        = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Total
    total_descuentos        = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'descuento'

    def __str__(self):
        return f'Descuentos — {self.detalle_nomina}'