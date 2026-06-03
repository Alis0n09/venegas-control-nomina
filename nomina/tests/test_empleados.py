from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from nomina.tests.helpers import create_user, create_staff, auth_client, create_empleado


class EmpleadoPermisosTests(TestCase):
    def setUp(self):
        self.user     = create_user()
        self.admin    = create_staff()
        self.empleado = create_empleado()

    def test_autenticado_puede_listar(self):
        resp = auth_client(self.user).get('/api/empleados/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_no_autenticado_retorna_401(self):
        resp = APIClient().get('/api/empleados/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_normal_no_puede_crear(self):
        resp = auth_client(self.user).post('/api/empleados/', {
            'cedula': '9999999999', 'nombres': 'X', 'apellidos': 'Y',
            'area': 'Z', 'salario': '800', 'forma_pago': 'efectivo',
            'fecha_ingreso': '2024-01-01',
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_puede_crear(self):
        resp = auth_client(self.admin).post('/api/empleados/', {
            'cedula': '0987654321', 'nombres': 'Pedro', 'apellidos': 'Torres',
            'area': 'Contabilidad', 'salario': '800.00',
            'forma_pago': 'efectivo', 'fecha_ingreso': '2024-01-01',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_admin_puede_eliminar(self):
        resp = auth_client(self.admin).delete(f'/api/empleados/{self.empleado.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


class EmpleadoFiltrosTests(TestCase):
    def setUp(self):
        self.client = auth_client(create_user())
        create_empleado(cedula='1111111111', area='Sistemas',     estado=True)
        create_empleado(cedula='2222222222', area='Contabilidad', estado=False)

    def test_filtrar_activos(self):
        resp = self.client.get('/api/empleados/?estado=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for emp in resp.data['results']:
            self.assertTrue(emp['estado'])

    def test_buscar_por_area(self):
        resp = self.client.get('/api/empleados/?search=Sistemas')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    def test_endpoint_activos(self):
        resp = self.client.get('/api/empleados/activos/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for emp in resp.data['results']:
            self.assertTrue(emp['estado'])

    def test_stats(self):
        resp = self.client.get('/api/empleados/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total_empleados', 'total_activos', 'total_inactivos', 'por_area']:
            self.assertIn(field, resp.data)


class EmpleadoAccionesTests(TestCase):
    def setUp(self):
        self.admin  = create_staff()
        self.client = auth_client(self.admin)

    def test_desactivar_empleado(self):
        emp = create_empleado()
        resp = self.client.post(f'/api/empleados/{emp.id}/desactivar/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(resp.data['estado'])

    def test_desactivar_empleado_ya_inactivo(self):
        emp = create_empleado(estado=False)
        resp = self.client.post(f'/api/empleados/{emp.id}/desactivar/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reactivar_empleado(self):
        emp = create_empleado(estado=False)
        resp = self.client.post(f'/api/empleados/{emp.id}/reactivar/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['estado'])

    def test_reactivar_empleado_ya_activo(self):
        emp = create_empleado(estado=True)
        resp = self.client.post(f'/api/empleados/{emp.id}/reactivar/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_cedula_duplicada(self):
        create_empleado(cedula='1111111111')
        resp = self.client.post('/api/empleados/', {
            'cedula': '1111111111', 'nombres': 'Luis', 'apellidos': 'Gomez',
            'area': 'Ventas', 'salario': '800', 'forma_pago': 'efectivo',
            'fecha_ingreso': '2024-01-01',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)