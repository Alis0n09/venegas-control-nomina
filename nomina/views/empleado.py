from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg

from nomina.models                  import Empleado
from nomina.serializers.empleado    import EmpleadoSerializer, EmpleadoSummarySerializer
from nomina.permissions             import IsStaffOrReadOnly
from nomina.pagination              import StandardPagination
from nomina.filters                 import EmpleadoFilter


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset           = Empleado.objects.all()
    serializer_class   = EmpleadoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = EmpleadoFilter
    search_fields      = ['cedula', 'nombres', 'apellidos', 'area']
    ordering_fields    = ['apellidos', 'nombres', 'area', 'salario', 'fecha_ingreso']
    ordering           = ['apellidos']

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='activos',
    )
    def activos(self, request):
        qs   = self.filter_queryset(
            self.get_queryset().filter(estado=True)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                EmpleadoSummarySerializer(page, many=True).data
            )
        return Response(EmpleadoSummarySerializer(qs, many=True).data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='desactivar',
    )
    def desactivar(self, request, pk=None):
        empleado = self.get_object()
        if not empleado.estado:
            return Response(
                {'error': 'El empleado ya está desactivado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        empleado.estado = False
        empleado.save(update_fields=['estado'])
        return Response({
            'id':     empleado.id,
            'nombre': str(empleado),
            'estado': empleado.estado,
        })

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        qs = Empleado.objects.all()
        data = {
            'total_empleados':  qs.count(),
            'total_activos':    qs.filter(estado=True).count(),
            'total_inactivos':  qs.filter(estado=False).count(),
            'promedio_salario': round(float(qs.aggregate(Avg('salario'))['salario__avg'] or 0), 2),
            'por_area':         list(qs.values('area').annotate(total=Count('id')).order_by('area')),
        }
        return Response(data)
