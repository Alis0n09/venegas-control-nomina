from datetime import date
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from nomina.models import Empleado, Nomina, DetalleNomina, Descuento
from nomina.models.sbu import SBU
from nomina.models.impuesto_renta import ImpuestoRenta


def create_user(username='usuario', email=None, password='Pass1234!', **kwargs):
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, **kwargs
    )

def create_staff(username='admin', email=None, password='Admin1234!'):
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, is_staff=True
    )

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)

def auth_client(user):
    client = APIClient()
    access, _ = get_tokens(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return client


# ── Modelos de nomina ──

def create_empleado(
    cedula='1234567890',
    nombres='Gabriela',
    apellidos='Calderon',
    area='Sistemas',
    salario=800,
    estado=True,
    **kwargs,
):
    return Empleado.objects.create(
        cedula=cedula,
        nombres=nombres,
        apellidos=apellidos,
        area=area,
        salario=salario,
        forma_pago='transferencia',
        fecha_ingreso=date(2023, 1, 1),
        estado=estado,
        **kwargs,
    )

def create_nomina(anio=2025, mes=1, tipo='mensual', estado='generada'):
    return Nomina.objects.create(anio=anio, mes=mes, tipo=tipo, estado=estado)

def create_detalle(nomina=None, empleado=None, dias_laborados=30, **kwargs):
    if nomina is None:
        nomina = create_nomina()
    if empleado is None:
        empleado = create_empleado()
    return DetalleNomina.objects.create(
        nomina=nomina,
        empleado=empleado,
        dias_laborados=dias_laborados,
        **kwargs,
    )

def create_descuento(detalle=None, **kwargs):
    if detalle is None:
        detalle = create_detalle()
    return Descuento.objects.create(detalle_nomina=detalle, **kwargs)

def create_sbu(anio=2025, valor=460):
    return SBU.objects.create(anio=anio, valor=valor, fecha_vigencia=date(anio, 1, 1))

def create_tabla_ir(anio=2025):
    ImpuestoRenta.objects.create(
        anio=anio, fraccion_basica=0, exceso_hasta=11902,
        impuesto_fraccion=0, porcentaje_excedente=0,
    )
    ImpuestoRenta.objects.create(
        anio=anio, fraccion_basica=11902, exceso_hasta=15159,
        impuesto_fraccion=0, porcentaje_excedente=5,
    )