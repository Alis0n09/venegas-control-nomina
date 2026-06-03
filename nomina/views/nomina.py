from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from nomina.models import Nomina
from nomina.serializers.nomina import NominaSerializer, NominaSummarySerializer
from nomina.permissions import IsStaffOrReadOnly
from nomina.pagination import StandardPagination
from nomina.filters import NominaFilter


class NominaViewSet(viewsets.ModelViewSet):
    queryset           = Nomina.objects.all()
    serializer_class   = NominaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = NominaFilter
    search_fields      = ['tipo', 'estado']
    ordering_fields    = ['anio', 'mes', 'estado']
    ordering           = ['-anio', '-mes']

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='aprobar',
    )
    def aprobar(self, request, pk=None):
        nomina = self.get_object()
        if nomina.estado != 'generada':
            return Response(
                {'error': 'Solo se pueden aprobar nominas en estado generada.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        nomina.estado = 'aprobada'
        nomina.save(update_fields=['estado'])
        return Response(NominaSummarySerializer(nomina).data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='pagar',
    )
    def pagar(self, request, pk=None):
        nomina = self.get_object()
        if nomina.estado != 'aprobada':
            return Response(
                {'error': 'Solo se pueden pagar nóminas en estado aprobada.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        nomina.estado = 'pagada'
        nomina.save(update_fields=['estado'])
        return Response(NominaSummarySerializer(nomina).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        qs = Nomina.objects.all()
        data = {
            'total':    qs.count(),
            'generadas': qs.filter(estado='generada').count(),
            'aprobadas': qs.filter(estado='aprobada').count(),
            'pagadas':   qs.filter(estado='pagada').count(),
        }
        return Response(data)
