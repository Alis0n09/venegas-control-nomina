from django.db import models

class ImpuestoRenta(models.Model):
    anio                    = models.IntegerField()
    fraccion_basica         = models.DecimalField(max_digits=12, decimal_places=2)
    exceso_hasta            = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    impuesto_fraccion       = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_excedente    = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'impuesto_renta'
        ordering = ['anio', 'fraccion_basica']

    def __str__(self):
        return f'IR {self.anio} — desde ${self.fraccion_basica}'