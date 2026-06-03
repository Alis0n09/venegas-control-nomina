from decimal import Decimal, ROUND_HALF_UP
from nomina.models.impuesto_renta import ImpuestoRenta
from nomina.models.sbu import SBU


def _redondear(valor):
    return Decimal(valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def calcular_detalle_nomina(detalle):

    salario     = Decimal(detalle.empleado.salario)
    anio        = detalle.nomina.anio
    dias        = Decimal(detalle.dias_laborados)
    horas_50    = Decimal(detalle.horas_extras)

    sueldo_dias = _redondear(salario / 30 * dias)
    valor_hora  = _redondear(salario / 240)
    valor_horas_50 = _redondear(valor_hora * Decimal('1.5') * horas_50)

    detalle.sueldo_dias_trabajados = sueldo_dias

    subtotal = _redondear(
        sueldo_dias
        + valor_horas_50
        + Decimal(detalle.bonos)
        + Decimal(detalle.ingreso_adicional)
    )
    detalle.subtotal_imponible = subtotal


    detalle.decimo_tercero = _redondear(subtotal / 12)
    detalle.fondos_reserva = _redondear(subtotal / 12)

    sbu = SBU.objects.filter(anio=anio).first()
    sbu_valor = Decimal(sbu.valor) if sbu else Decimal('460.00')
    detalle.decimo_cuarto = _redondear(sbu_valor / 12)


    aporte_iess = _redondear(subtotal * Decimal('0.0945'))
    detalle.aporte_personal_iess = aporte_iess

    ingreso_anual = subtotal * 12
    detalle.impuesto_renta = _calcular_impuesto_renta(ingreso_anual, anio)


    detalle.total_ingresos  = subtotal
    detalle.valor_a_recibir = _redondear(
        subtotal - aporte_iess - detalle.impuesto_renta
    )

    return detalle


def _calcular_impuesto_renta(ingreso_anual, anio):

    ingreso_anual = Decimal(ingreso_anual)

    tabla = ImpuestoRenta.objects.filter(
        anio=anio,
        fraccion_basica__lte=ingreso_anual,
    ).order_by('-fraccion_basica').first()

    if not tabla:
        return Decimal('0.00')

    excedente = ingreso_anual - Decimal(tabla.fraccion_basica)
    impuesto_anual = (
        Decimal(tabla.impuesto_fraccion)
        + excedente * (Decimal(tabla.porcentaje_excedente) / 100)
    )

    return _redondear(impuesto_anual / 12)


def calcular_total_descuentos(descuento):

    total = (
        Decimal(descuento.prestamo_hipotecario)
        + Decimal(descuento.prestamo_quirografario)
        + Decimal(descuento.prestamo_empresa)
        + Decimal(descuento.anticipos)
        + Decimal(descuento.multas_atraso)
        + Decimal(descuento.dias_no_laborados)
        + Decimal(descuento.otros_descuentos)
    )
    descuento.total_descuentos = _redondear(total)
    return descuento
