from django.contrib import admin
from nomina.models import Empleado, Nomina, DetalleNomina, Descuento
from nomina.models.sbu import SBU
from nomina.models.impuesto_renta import ImpuestoRenta


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'cedula', 'apellidos', 'nombres', 'area', 'salario', 'estado']
    search_fields = ['cedula', 'nombres', 'apellidos', 'area']
    list_filter   = ['area', 'estado', 'forma_pago']
    list_editable = ['estado']


class DetalleNominaInline(admin.TabularInline):
    model  = DetalleNomina
    extra  = 0
    fields = ['empleado', 'dias_laborados', 'subtotal_imponible', 'valor_a_recibir']
    readonly_fields = ['subtotal_imponible', 'valor_a_recibir']


@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'anio', 'mes', 'tipo', 'estado', 'fecha_generacion']
    search_fields = ['anio', 'mes']
    list_filter   = ['estado', 'tipo', 'anio']
    inlines       = [DetalleNominaInline]


class DescuentoInline(admin.TabularInline):
    model  = Descuento
    extra  = 0
    fields = [
        'prestamo_hipotecario', 'prestamo_quirografario',
        'prestamo_empresa', 'anticipos', 'multas_atraso',
        'dias_no_laborados', 'otros_descuentos', 'total_descuentos',
    ]
    readonly_fields = ['total_descuentos']


@admin.register(DetalleNomina)
class DetalleNominaAdmin(admin.ModelAdmin):
    list_display  = [
        'id', 'empleado', 'nomina', 'dias_laborados',
        'subtotal_imponible', 'aporte_personal_iess', 'valor_a_recibir',
    ]
    search_fields = [
        'empleado__cedula', 'empleado__nombres', 'empleado__apellidos'
    ]
    list_filter   = ['nomina__anio', 'nomina__mes']
    readonly_fields = [
        'sueldo_dias_trabajados', 'subtotal_imponible',
        'decimo_tercero', 'decimo_cuarto', 'fondos_reserva',
        'aporte_personal_iess', 'impuesto_renta',
        'total_ingresos', 'valor_a_recibir',
    ]
    inlines = [DescuentoInline]


@admin.register(Descuento)
class DescuentoAdmin(admin.ModelAdmin):
    list_display  = [
        'id', 'detalle_nomina', 'prestamo_hipotecario',
        'prestamo_quirografario', 'anticipos', 'total_descuentos',
    ]
    search_fields = [
        'detalle_nomina__empleado__cedula',
        'detalle_nomina__empleado__apellidos',
    ]
    readonly_fields = ['total_descuentos']


@admin.register(SBU)
class SBUAdmin(admin.ModelAdmin):
    list_display  = ['id', 'anio', 'valor', 'fecha_vigencia']
    search_fields = ['anio']
    ordering      = ['-anio']


@admin.register(ImpuestoRenta)
class ImpuestoRentaAdmin(admin.ModelAdmin):
    list_display  = [
        'id', 'anio', 'fraccion_basica', 'exceso_hasta',
        'impuesto_fraccion', 'porcentaje_excedente',
    ]
    list_filter   = ['anio']
    ordering      = ['anio', 'fraccion_basica']