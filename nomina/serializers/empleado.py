from rest_framework import serializers
from nomina.models import Empleado


class EmpleadoSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model  = Empleado
        fields = ['id', 'cedula', 'nombres', 'apellidos', 'area', 'estado']


class EmpleadoSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    tiene_cuenta    = serializers.SerializerMethodField()

    class Meta:
        model  = Empleado
        fields = [
            'id', 'cedula', 'nombres', 'apellidos', 'nombre_completo',
            'correo', 'direccion', 'area',
            'forma_pago', 'banco', 'tipo_cuenta', 'numero_cuenta', 'tiene_cuenta',
            'salario', 'numero_iess', 'cargas_familiares',
            'fecha_ingreso', 'estado',
        ]
        read_only_fields = ['id']

    def get_nombre_completo(self, obj):
        return f'{obj.apellidos} {obj.nombres}'

    def get_tiene_cuenta(self, obj):
        return obj.numero_cuenta is not None

    def validate_cedula(self, value):
        if len(value) != 10:
            raise serializers.ValidationError('La cédula debe tener exactamente 10 dígitos.')
        if not value.isdigit():
            raise serializers.ValidationError('La cédula solo debe contener números.')
        return value

    def validate_salario(self, value):
        if value < 460:
            raise serializers.ValidationError('El salario no puede ser menor al SBU ($460).')
        return value

    def validate_cargas_familiares(self, value):
        if value < 0:
            raise serializers.ValidationError('Las cargas familiares no pueden ser negativas.')
        return value