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
        for campo in [
            'prestamo_hipotecario', 'prestamo_quirografario',
            'prestamo_empresa', 'anticipos', 'multas_atraso',
            'dias_no_laborados', 'otros_descuentos',
        ]:
            if campo in attrs and attrs[campo] < 0:
                raise serializers.ValidationError({campo: 'El descuento no puede ser negativo.'})
        return attrs
 
    def create(self, validated_data):
        from nomina.services import calcular_total_descuentos
        descuento = Descuento(**validated_data)
        descuento = calcular_total_descuentos(descuento)
        descuento.save()
        return descuento
 
    def update(self, instance, validated_data):
        from nomina.services import calcular_total_descuentos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance = calcular_total_descuentos(instance)
        instance.save()
        return instance