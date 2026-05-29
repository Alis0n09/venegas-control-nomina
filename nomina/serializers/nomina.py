from django.db.models import Sum
from rest_framework import serializers
from nomina.models import Nomina
from nomina.serializers.detalle_nomina import DetalleNominaSerializer


class NominaSummarySerializer(serializers.ModelSerializer):
    periodo = serializers.SerializerMethodField()

    class Meta:
        model  = Nomina
        fields = ['id', 'anio', 'mes', 'periodo', 'tipo', 'estado', 'fecha_generacion']

    def get_periodo(self, obj):
        return f'{obj.mes:02d}/{obj.anio}'


class NominaSerializer(serializers.ModelSerializer):
    periodo          = serializers.SerializerMethodField()
    total_empleados  = serializers.SerializerMethodField()
    total_ingresos   = serializers.SerializerMethodField()
    total_a_pagar    = serializers.SerializerMethodField()
    detalles         = DetalleNominaSerializer(many=True, read_only=True)

    class Meta:
        model  = Nomina
        fields = [
            'id', 'anio', 'mes', 'periodo', 'tipo', 'estado', 'fecha_generacion',
            'total_empleados', 'total_ingresos', 'total_a_pagar',
            'detalles',
        ]
        read_only_fields = ['id', 'fecha_generacion']

    def get_periodo(self, obj):
        return f'{obj.mes:02d}/{obj.anio}'

    def get_total_empleados(self, obj):
        return obj.detalles.count()

    def get_total_ingresos(self, obj):
        total = obj.detalles.aggregate(total=Sum('total_ingresos'))['total']
        return total or 0

    def get_total_a_pagar(self, obj):
        total = obj.detalles.aggregate(total=Sum('valor_a_recibir'))['total']
        return total or 0

    def validate_mes(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError('El mes debe estar entre 1 y 12.')
        return value

    def validate_anio(self, value):
        if value < 2000:
            raise serializers.ValidationError('El anio no puede ser menor a 2000.')
        return value
