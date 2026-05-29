from django.db import models
from nomina.models.empleado import Empleado
from nomina.models.nomina import Nomina

class DetalleNomina(models.Model):
    nomina              = models.ForeignKey(Nomina, on_delete=models.CASCADE, related_name='detalles')
    empleado            = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name='detalles')

    # Ingresos
    dias_laborados          = models.IntegerField()
    horas_extras            = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sueldo_dias_trabajados  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonos                   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ingreso_adicional       = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Subtotales
    subtotal_imponible      = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Beneficios legales
    decimo_tercero          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    decimo_cuarto           = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fondos_reserva          = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Deducciones legales
    aporte_personal_iess    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto_renta          = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Totales
    total_ingresos          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_a_recibir         = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'detalle_nomina'
        unique_together = ('nomina', 'empleado')

    def __str__(self):
        return f'Detalle — {self.empleado} | {self.nomina}'