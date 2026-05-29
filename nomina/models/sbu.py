from django.db import models

class SBU(models.Model):
    anio            = models.IntegerField(unique=True)
    valor           = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vigencia  = models.DateField()

    class Meta:
        db_table = 'sbu'

    def __str__(self):
        return f'SBU {self.anio} — ${self.valor}'