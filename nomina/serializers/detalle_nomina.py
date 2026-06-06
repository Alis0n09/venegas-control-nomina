from rest_framework import serializers
from nomina.models import DetalleNomina
from nomina.serializers.empleado import EmpleadoSummarySerializer

class DetalleNominaSummarySerializer(serializers.ModelSerializer):
    empleado = EmpleadoSummarySerializer(read_only=True)

    class Meta:
        model  = DetalleNomina
        fields = ['id', 'empleado', 'nomina', 'dias_laborados', 'total_ingresos', 'valor_a_recibir']


class DetalleNominaSerializer(serializers.ModelSerializer):
    empleado_detalle = EmpleadoSummarySerializer(source='empleado', read_only=True)
    nomina_display   = serializers.SerializerMethodField()

    def get_nomina_display(self, obj):
        return f"Nómina {obj.nomina.mes}/{obj.nomina.anio} - {obj.nomina.tipo}"

    class Meta:
        model  = DetalleNomina
        fields = [
            'id', 'nomina', 'empleado', 'empleado_detalle',
            'nomina_display',
            'dias_laborados', 'horas_extras', 'sueldo_dias_trabajados',
            'bonos', 'ingreso_adicional',
            'subtotal_imponible',
            'decimo_tercero', 'decimo_cuarto', 'fondos_reserva',
            'aporte_personal_iess', 'impuesto_renta',
            'total_ingresos', 'valor_a_recibir',
        ]
        read_only_fields = [
            'id', 'sueldo_dias_trabajados', 'subtotal_imponible',
            'decimo_tercero', 'decimo_cuarto', 'fondos_reserva',
            'aporte_personal_iess', 'impuesto_renta',
            'total_ingresos', 'valor_a_recibir',
        ]

    def validate_dias_laborados(self, value):
        if value < 0:
            raise serializers.ValidationError('Los dias laborados no pueden ser negativos.')
        if value > 31:
            raise serializers.ValidationError('Los dias laborados no pueden ser mayores a 31.')
        return value

    def validate(self, attrs):
        for campo in ['horas_extras', 'bonos', 'ingreso_adicional']:
            if campo in attrs and attrs[campo] < 0:
                raise serializers.ValidationError({campo: 'El valor no puede ser negativo.'})
        return attrs

    def create(self, validated_data):
        from nomina.services import calcular_detalle_nomina
        detalle = DetalleNomina(**validated_data)
        detalle = calcular_detalle_nomina(detalle)
        detalle.save()
        return detalle

    def update(self, instance, validated_data):
        from nomina.services import calcular_detalle_nomina
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance = calcular_detalle_nomina(instance)
        instance.save()
        return instance