from django.db import models

class Nomina(models.Model):
    TIPO_CHOICES = [
        ('mensual', 'Mensual'),
        ('quincenal', 'Quincenal'),
    ]
    ESTADO_CHOICES = [
        ('generada', 'Generada'),
        ('aprobada', 'Aprobada'),
        ('pagada', 'Pagada'),
    ]

    anio                = models.IntegerField()
    mes                 = models.IntegerField()
    tipo                = models.CharField(max_length=30, choices=TIPO_CHOICES)
    estado              = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='generada')
    fecha_generacion    = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'nomina'
        unique_together = ('anio', 'mes', 'tipo')

    def __str__(self):
        return f'Nómina {self.mes}/{self.anio} - {self.tipo}'