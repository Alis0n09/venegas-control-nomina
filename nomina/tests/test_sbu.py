from datetime import date
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from nomina.tests.helpers import create_user, create_staff, auth_client, create_sbu


class SBUPermisosTests(TestCase):
    def setUp(self):
        self.user  = create_user()
        self.admin = create_staff()
        create_sbu(anio=2024, valor=450)
        create_sbu(anio=2025, valor=460)

    def test_autenticado_puede_listar(self):
        resp = auth_client(self.user).get('/nomina/sbu/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_no_autenticado_retorna_401(self):
        resp = APIClient().get('/nomina/sbu/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_normal_no_puede_crear(self):
        resp = auth_client(self.user).post('/nomina/sbu/', {
            'anio': 2026, 'valor': '470.00', 'fecha_vigencia': '2026-01-01'
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_puede_crear(self):
        resp = auth_client(self.admin).post('/nomina/sbu/', {
            'anio': 2026, 'valor': '470.00', 'fecha_vigencia': '2026-01-01'
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


class SBUValidacionesTests(TestCase):
    def setUp(self):
        self.admin  = create_staff()
        self.client = auth_client(self.admin)

    def test_valor_negativo_retorna_400(self):
        resp = self.client.post('/nomina/sbu/', {
            'anio': 2025, 'valor': '-100', 'fecha_vigencia': '2025-01-01'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valor_cero_retorna_400(self):
        resp = self.client.post('/nomina/sbu/', {
            'anio': 2025, 'valor': '0', 'fecha_vigencia': '2025-01-01'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anio_duplicado_retorna_400(self):
        create_sbu(anio=2025, valor=460)
        resp = self.client.post('/nomina/sbu/', {
            'anio': 2025, 'valor': '465', 'fecha_vigencia': '2025-01-01'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class SBUVigenteTests(TestCase):
    def setUp(self):
        self.client = auth_client(create_user())

    def test_vigente_devuelve_sbu_anio_actual(self):
        create_sbu(anio=date.today().year, valor=460)
        resp = self.client.get('/nomina/sbu/vigente/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['anio'], date.today().year)
        self.assertIn('valor', resp.data)

    def test_vigente_sin_datos_retorna_404(self):
        resp = self.client.get('/nomina/sbu/vigente/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)