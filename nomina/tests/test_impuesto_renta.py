from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from nomina.tests.helpers import create_user, create_staff, auth_client, create_tabla_ir


class ImpuestoRentaPermisosTests(TestCase):
    def setUp(self):
        self.user  = create_user()
        self.admin = create_staff()
        create_tabla_ir(anio=2025)

    def test_autenticado_puede_listar(self):
        resp = auth_client(self.user).get('/nomina/impuesto-renta/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_no_autenticado_retorna_401(self):
        resp = APIClient().get('/nomina/impuesto-renta/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_normal_no_puede_crear(self):
        resp = auth_client(self.user).post('/nomina/impuesto-renta/', {
            'anio': 2026, 'fraccion_basica': '0',
            'exceso_hasta': '12000', 'impuesto_fraccion': '0',
            'porcentaje_excedente': '0',
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_puede_crear(self):
        resp = auth_client(self.admin).post('/nomina/impuesto-renta/', {
            'anio': 2026, 'fraccion_basica': '0',
            'exceso_hasta': '12000', 'impuesto_fraccion': '0',
            'porcentaje_excedente': '0',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


class ImpuestoRentaValidacionesTests(TestCase):
    def setUp(self):
        self.admin  = create_staff()
        self.client = auth_client(self.admin)

    def test_exceso_hasta_menor_que_fraccion_retorna_400(self):
        resp = self.client.post('/nomina/impuesto-renta/', {
            'anio': 2025, 'fraccion_basica': '5000',
            'exceso_hasta': '3000',
            'impuesto_fraccion': '0', 'porcentaje_excedente': '5',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_porcentaje_mayor_100_retorna_400(self):
        resp = self.client.post('/nomina/impuesto-renta/', {
            'anio': 2025, 'fraccion_basica': '0',
            'exceso_hasta': '5000',
            'impuesto_fraccion': '0', 'porcentaje_excedente': '150',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_porcentaje_negativo_retorna_400(self):
        resp = self.client.post('/nomina/impuesto-renta/', {
            'anio': 2025, 'fraccion_basica': '0',
            'exceso_hasta': '5000',
            'impuesto_fraccion': '0', 'porcentaje_excedente': '-5',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class ImpuestoRentaPorAnioTests(TestCase):
    def setUp(self):
        self.client = auth_client(create_user())
        create_tabla_ir(anio=2024)
        create_tabla_ir(anio=2025)

    def test_por_anio_devuelve_tramos_correctos(self):
        resp = self.client.get('/nomina/impuesto-renta/por-anio/2025/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for tramo in resp.data:
            self.assertEqual(tramo['anio'], 2025)

    def test_por_anio_sin_datos_retorna_404(self):
        resp = self.client.get('/nomina/impuesto-renta/por-anio/2000/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_filtrar_por_anio(self):
        resp = self.client.get('/nomina/impuesto-renta/?anio=2024')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for tramo in resp.data['results']:
            self.assertEqual(tramo['anio'], 2024)