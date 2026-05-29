from django.db import models

class Empleado(models.Model):
    FORMA_PAGO_CHOICES = [
        ('transferencia', 'Transferencia'),
        ('efectivo', 'Efectivo'),
    ]
    TIPO_CUENTA_CHOICES = [
        ('ahorros', 'Ahorros'),
        ('corriente', 'Corriente'),
    ]

    cedula              = models.CharField(max_length=10, unique=True)
    nombres             = models.CharField(max_length=100)
    apellidos           = models.CharField(max_length=100)
    correo              = models.EmailField(max_length=150, unique=True, null=True, blank=True)
    direccion           = models.CharField(max_length=255, null=True, blank=True)
    area                = models.CharField(max_length=100)
    forma_pago          = models.CharField(max_length=30, choices=FORMA_PAGO_CHOICES)
    banco               = models.CharField(max_length=80, null=True, blank=True)
    tipo_cuenta         = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES, null=True, blank=True)
    numero_cuenta       = models.CharField(max_length=30, null=True, blank=True)
    salario             = models.DecimalField(max_digits=10, decimal_places=2)
    numero_iess         = models.CharField(max_length=15, unique=True, null=True, blank=True)
    cargas_familiares   = models.IntegerField(default=0)
    fecha_ingreso       = models.DateField()
    estado              = models.BooleanField(default=True)

    class Meta:
        db_table = 'empleado'

    def __str__(self):
        return f'{self.apellidos} {self.nombres}'
