from django.db.models import Avg, Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from nomina.models import DetalleNomina
from nomina.serializers.detalle_nomina import (
    DetalleNominaSerializer,
    DetalleNominaSummarySerializer,
)
from nomina.permissions import IsStaffOrReadOnly
from nomina.pagination import StandardPagination
from nomina.filters import DetalleNominaFilter


class DetalleNominaViewSet(viewsets.ModelViewSet):
    queryset           = DetalleNomina.objects.select_related('nomina', 'empleado').all()
    serializer_class   = DetalleNominaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = DetalleNominaFilter
    search_fields      = ['empleado__cedula', 'empleado__nombres', 'empleado__apellidos']
    ordering_fields    = [
        'dias_laborados', 'total_ingresos', 'valor_a_recibir',
        'nomina__anio', 'nomina__mes', 'empleado__apellidos',
    ]
    ordering           = ['nomina__anio', 'nomina__mes', 'empleado__apellidos']

    @action(
        detail=False,
        methods=['get'],
        url_path='por-nomina/(?P<nomina_id>[^/.]+)',
    )
    def por_nomina(self, request, nomina_id=None):
        qs = self.filter_queryset(
            self.get_queryset().filter(nomina_id=nomina_id)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                DetalleNominaSummarySerializer(page, many=True).data
            )
        return Response(DetalleNominaSummarySerializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='por-empleado/(?P<empleado_id>[^/.]+)',
    )
    def por_empleado(self, request, empleado_id=None):
        qs = self.filter_queryset(
            self.get_queryset().filter(empleado_id=empleado_id)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                DetalleNominaSummarySerializer(page, many=True).data
            )
        return Response(DetalleNominaSummarySerializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        qs = DetalleNomina.objects.all()
        data = {
            'total_detalles': qs.count(),
            'total_ingresos': qs.aggregate(total=Sum('total_ingresos'))['total'] or 0,
            'total_a_pagar': qs.aggregate(total=Sum('valor_a_recibir'))['total'] or 0,
            'promedio_a_recibir': round(float(qs.aggregate(Avg('valor_a_recibir'))['valor_a_recibir__avg'] or 0), 2),
        }
        return Response(data)
