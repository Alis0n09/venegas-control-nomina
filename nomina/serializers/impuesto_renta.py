from rest_framework import serializers
from nomina.models.impuesto_renta import ImpuestoRenta


class ImpuestoRentaSerializer(serializers.ModelSerializer):

    class Meta:
        model  = ImpuestoRenta
        fields = [
            'id', 'anio', 'fraccion_basica', 'exceso_hasta',
            'impuesto_fraccion', 'porcentaje_excedente',
        ]
        read_only_fields = ['id']

    def validate_anio(self, value):
        if value < 2000:
            raise serializers.ValidationError('El año no puede ser menor a 2000.')
        return value

    def validate_porcentaje_excedente(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('El porcentaje debe estar entre 0 y 100.')
        return value

    def validate(self, attrs):
        fraccion_basica = attrs.get('fraccion_basica', 0)
        exceso_hasta    = attrs.get('exceso_hasta')
        if exceso_hasta is not None and exceso_hasta <= fraccion_basica:
            raise serializers.ValidationError(
                {'exceso_hasta': 'Debe ser mayor que la fracción básica.'}
            )
        return attrs