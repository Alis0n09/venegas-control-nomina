from django.db.models import Avg, Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from nomina.models import Descuento
from nomina.serializers.descuentos import DescuentoSerializer
from nomina.permissions import IsStaffOrReadOnly
from nomina.pagination import StandardPagination
from nomina.filters import DescuentoFilter


class DescuentoViewSet(viewsets.ModelViewSet):
    queryset           = Descuento.objects.select_related(
        'detalle_nomina',
        'detalle_nomina__nomina',
        'detalle_nomina__empleado',
    ).all()
    serializer_class   = DescuentoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = DescuentoFilter
    search_fields      = [
        'detalle_nomina__empleado__cedula',
        'detalle_nomina__empleado__nombres',
        'detalle_nomina__empleado__apellidos',
    ]
    ordering_fields    = [
        'total_descuentos', 'prestamo_hipotecario', 'prestamo_quirografario',
        'prestamo_empresa', 'anticipos', 'multas_atraso',
        'detalle_nomina__nomina__anio', 'detalle_nomina__nomina__mes',
        'detalle_nomina__empleado__apellidos',
    ]
    ordering           = [
        'detalle_nomina__nomina__anio',
        'detalle_nomina__nomina__mes',
        'detalle_nomina__empleado__apellidos',
    ]

    @action(
        detail=False,
        methods=['get'],
        url_path='por-nomina/(?P<nomina_id>[^/.]+)',
    )
    def por_nomina(self, request, nomina_id=None):
        qs = self.filter_queryset(
            self.get_queryset().filter(detalle_nomina__nomina_id=nomina_id)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                DescuentoSerializer(page, many=True).data
            )
        return Response(DescuentoSerializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='por-empleado/(?P<empleado_id>[^/.]+)',
    )
    def por_empleado(self, request, empleado_id=None):
        qs = self.filter_queryset(
            self.get_queryset().filter(detalle_nomina__empleado_id=empleado_id)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                DescuentoSerializer(page, many=True).data
            )
        return Response(DescuentoSerializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        qs = Descuento.objects.all()
        data = {
            'total_registros': qs.count(),
            'total_descuentos': qs.aggregate(total=Sum('total_descuentos'))['total'] or 0,
            'promedio_descuentos': round(float(qs.aggregate(Avg('total_descuentos'))['total_descuentos__avg'] or 0), 2),
            'total_prestamos_iess': (
                (qs.aggregate(total=Sum('prestamo_hipotecario'))['total'] or 0) +
                (qs.aggregate(total=Sum('prestamo_quirografario'))['total'] or 0)
            ),
            'total_anticipos': qs.aggregate(total=Sum('anticipos'))['total'] or 0,
            'total_multas_atraso': qs.aggregate(total=Sum('multas_atraso'))['total'] or 0,
        }
        return Response(data)
