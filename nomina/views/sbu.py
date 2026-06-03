from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from nomina.models.sbu import SBU
from nomina.serializers.sbu import SBUSerializer
from nomina.permissions import IsStaffOrReadOnly
from nomina.pagination import StandardPagination


class SBUViewSet(viewsets.ModelViewSet):
    queryset           = SBU.objects.all()
    serializer_class   = SBUSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [OrderingFilter]
    ordering_fields    = ['anio', 'valor']
    ordering           = ['-anio']

    @action(detail=False, methods=['get'], url_path='vigente')
    def vigente(self, request):
        """Devuelve el SBU del año actual."""
        from datetime import date
        sbu = SBU.objects.filter(anio=date.today().year).first()
        if not sbu:
            return Response({'error': 'No hay SBU registrado para el año actual.'}, status=404)
        return Response(SBUSerializer(sbu).data)