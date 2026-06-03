from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from nomina.models.impuesto_renta import ImpuestoRenta
from nomina.serializers.impuesto_renta import ImpuestoRentaSerializer
from nomina.permissions import IsStaffOrReadOnly
from nomina.pagination import StandardPagination


class ImpuestoRentaViewSet(viewsets.ModelViewSet):
    queryset           = ImpuestoRenta.objects.all()
    serializer_class   = ImpuestoRentaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_fields   = ['anio']
    ordering_fields    = ['anio', 'fraccion_basica']
    ordering           = ['-anio', 'fraccion_basica']

    @action(detail=False, methods=['get'], url_path='por-anio/(?P<anio>[0-9]{4})')
    def por_anio(self, request, anio=None):
        """Devuelve todos los tramos de un año específico."""
        tramos = ImpuestoRenta.objects.filter(anio=anio).order_by('fraccion_basica')
        if not tramos.exists():
            return Response({'error': f'No hay tabla de IR para el año {anio}.'}, status=404)
        return Response(ImpuestoRentaSerializer(tramos, many=True).data)