from rest_framework import serializers
from nomina.models import DetalleNomina
from nomina.serializers.empleado import EmpleadoSummarySerializer


class DetalleNominaSummarySerializer(serializers.ModelSerializer):
    empleado = EmpleadoSummarySerializer(read_only=True)

    class Meta:
        model  = DetalleNomina
        fields = ['id', 'empleado', 'dias_laborados', 'total_ingresos', 'valor_a_recibir']

class DetalleNominaSerializer(serializers.ModelSerializer):
    empleado_detalle = EmpleadoSummarySerializer(source='empleado', read_only=True)

    class Meta:
        model  = DetalleNomina
        fields = [
            'id', 'nomina', 'empleado', 'empleado_detalle',
            'dias_laborados', 'horas_extras', 'sueldo_dias_trabajados',
            'bonos', 'ingreso_adicional',
            'subtotal_imponible',
            'decimo_tercero', 'decimo_cuarto', 'fondos_reserva',
            'aporte_personal_iess', 'impuesto_renta',
            'total_ingresos', 'valor_a_recibir',
        ]
        read_only_fields = ['id', 'subtotal_imponible', 'decimo_tercero', 'decimo_cuarto',
                             'fondos_reserva', 'aporte_personal_iess', 'impuesto_renta', 
                             'total_ingresos', 'valor_a_recibir']

    def validate_dias_laborados(self, value):
        if value < 0:
            raise serializers.ValidationError('Los dias laborados no pueden ser negativos.')
        if value > 31:
            raise serializers.ValidationError('Los dias laborados no pueden ser mayores a 31.')
        return value

    def validate(self, attrs):
        campos_monetarios = [
            'horas_extras', 'sueldo_dias_trabajados', 'bonos', 'ingreso_adicional',
        ]

        for campo in campos_monetarios:
            if campo in attrs and attrs[campo] < 0:
                raise serializers.ValidationError({campo: 'El valor no puede ser negativo.'})

        return attrs
