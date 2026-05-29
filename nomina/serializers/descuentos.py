from rest_framework import serializers
from nomina.models import Descuento
from nomina.serializers.detalle_nomina import DetalleNominaSerializer


class DescuentoSerializer(serializers.ModelSerializer):
    detalle = DetalleNominaSerializer(source='detalle_nomina', read_only=True)

    class Meta:
        model  = Descuento
        fields = [
            'id', 'detalle_nomina', 'detalle',
            'prestamo_hipotecario', 'prestamo_quirografario',
            'prestamo_empresa', 'anticipos', 'multas_atraso',
            'dias_no_laborados', 'otros_descuentos',
            'total_descuentos',
        ]
        read_only_fields = ['id', 'total_descuentos']

    def validate(self, attrs):
        campos_descuento = [
            'prestamo_hipotecario', 'prestamo_quirografario',
            'prestamo_empresa', 'anticipos', 'multas_atraso',
            'dias_no_laborados', 'otros_descuentos',
        ]

        for campo in campos_descuento:
            if campo in attrs and attrs[campo] < 0:
                raise serializers.ValidationError({campo: 'El descuento no puede ser negativo.'})

        return attrs
