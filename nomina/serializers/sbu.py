from rest_framework import serializers
from nomina.models.sbu import SBU


class SBUSerializer(serializers.ModelSerializer):

    class Meta:
        model  = SBU
        fields = ['id', 'anio', 'valor', 'fecha_vigencia']
        read_only_fields = ['id']

    def validate_anio(self, value):
        if value < 2000:
            raise serializers.ValidationError('El año no puede ser menor a 2000.')
        return value

    def validate_valor(self, value):
        if value <= 0:
            raise serializers.ValidationError('El valor del SBU debe ser mayor a 0.')
        return value