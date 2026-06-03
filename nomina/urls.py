from rest_framework.routers import DefaultRouter
from nomina.views import (EmpleadoViewSet, NominaViewSet, DetalleNominaViewSet, DescuentoViewSet, SBUViewSet, ImpuestoRentaViewSet,)
from nomina.views.user import UserViewSet

router = DefaultRouter()
router.register('empleados', EmpleadoViewSet,       basename='empleado')
router.register('nominas', NominaViewSet,         basename='nomina')
router.register('detalles', DetalleNominaViewSet,  basename='detalle-nomina')
router.register('descuentos', DescuentoViewSet,      basename='descuento')
router.register('sbu', SBUViewSet,            basename='sbu')
router.register('impuesto-renta', ImpuestoRentaViewSet,  basename='impuesto-renta')
router.register('usuarios', UserViewSet,           basename='usuario')

urlpatterns = router.urls