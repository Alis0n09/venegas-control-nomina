import django_filters

from nomina.models import Descuento, DetalleNomina, Empleado, Nomina


class EmpleadoFilter(django_filters.FilterSet):
    cedula = django_filters.CharFilter(lookup_expr='icontains')
    nombres = django_filters.CharFilter(lookup_expr='icontains')
    apellidos = django_filters.CharFilter(lookup_expr='icontains')
    area = django_filters.CharFilter(lookup_expr='icontains')
    banco = django_filters.CharFilter(lookup_expr='icontains')
    salario_min = django_filters.NumberFilter(field_name='salario', lookup_expr='gte')
    salario_max = django_filters.NumberFilter(field_name='salario', lookup_expr='lte')
    fecha_ingreso_desde = django_filters.DateFilter(field_name='fecha_ingreso', lookup_expr='gte')
    fecha_ingreso_hasta = django_filters.DateFilter(field_name='fecha_ingreso', lookup_expr='lte')
    cargas_min = django_filters.NumberFilter(field_name='cargas_familiares', lookup_expr='gte')
    cargas_max = django_filters.NumberFilter(field_name='cargas_familiares', lookup_expr='lte')
    tiene_cuenta = django_filters.BooleanFilter(method='filter_tiene_cuenta')

    class Meta:
        model = Empleado
        fields = [
            'cedula', 'nombres', 'apellidos', 'area', 'estado',
            'forma_pago', 'banco', 'tipo_cuenta', 'salario_min', 'salario_max',
            'fecha_ingreso_desde', 'fecha_ingreso_hasta',
            'cargas_min', 'cargas_max', 'tiene_cuenta',
        ]

    def filter_tiene_cuenta(self, queryset, name, value):
        if value:
            return queryset.exclude(numero_cuenta__isnull=True).exclude(numero_cuenta='')
        return queryset.filter(numero_cuenta__isnull=True) | queryset.filter(numero_cuenta='')


class NominaFilter(django_filters.FilterSet):
    fecha_generacion_desde = django_filters.DateFilter(field_name='fecha_generacion', lookup_expr='gte')
    fecha_generacion_hasta = django_filters.DateFilter(field_name='fecha_generacion', lookup_expr='lte')

    class Meta:
        model = Nomina
        fields = [
            'anio', 'mes', 'tipo', 'estado',
            'fecha_generacion_desde', 'fecha_generacion_hasta',
        ]


class DetalleNominaFilter(django_filters.FilterSet):
    nomina = django_filters.NumberFilter(field_name='nomina_id')
    empleado = django_filters.NumberFilter(field_name='empleado_id')
    nomina_anio = django_filters.NumberFilter(field_name='nomina__anio')
    nomina_mes = django_filters.NumberFilter(field_name='nomina__mes')
    empleado_cedula = django_filters.CharFilter(field_name='empleado__cedula', lookup_expr='icontains')
    dias_min = django_filters.NumberFilter(field_name='dias_laborados', lookup_expr='gte')
    dias_max = django_filters.NumberFilter(field_name='dias_laborados', lookup_expr='lte')
    total_ingresos_min = django_filters.NumberFilter(field_name='total_ingresos', lookup_expr='gte')
    total_ingresos_max = django_filters.NumberFilter(field_name='total_ingresos', lookup_expr='lte')
    valor_a_recibir_min = django_filters.NumberFilter(field_name='valor_a_recibir', lookup_expr='gte')
    valor_a_recibir_max = django_filters.NumberFilter(field_name='valor_a_recibir', lookup_expr='lte')

    class Meta:
        model = DetalleNomina
        fields = [
            'nomina', 'empleado', 'nomina_anio', 'nomina_mes', 'empleado_cedula',
            'dias_min', 'dias_max', 'total_ingresos_min', 'total_ingresos_max',
            'valor_a_recibir_min', 'valor_a_recibir_max',
        ]


class DescuentoFilter(django_filters.FilterSet):
    detalle_nomina = django_filters.NumberFilter(field_name='detalle_nomina_id')
    nomina = django_filters.NumberFilter(field_name='detalle_nomina__nomina_id')
    empleado = django_filters.NumberFilter(field_name='detalle_nomina__empleado_id')
    nomina_anio = django_filters.NumberFilter(field_name='detalle_nomina__nomina__anio')
    nomina_mes = django_filters.NumberFilter(field_name='detalle_nomina__nomina__mes')
    empleado_cedula = django_filters.CharFilter(
        field_name='detalle_nomina__empleado__cedula',
        lookup_expr='icontains',
    )
    total_descuentos_min = django_filters.NumberFilter(field_name='total_descuentos', lookup_expr='gte')
    total_descuentos_max = django_filters.NumberFilter(field_name='total_descuentos', lookup_expr='lte')
    anticipos_min = django_filters.NumberFilter(field_name='anticipos', lookup_expr='gte')
    anticipos_max = django_filters.NumberFilter(field_name='anticipos', lookup_expr='lte')

    class Meta:
        model = Descuento
        fields = [
            'detalle_nomina', 'nomina', 'empleado', 'nomina_anio', 'nomina_mes',
            'empleado_cedula', 'total_descuentos_min', 'total_descuentos_max',
            'anticipos_min', 'anticipos_max',
        ]
