from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from nomina.tests.helpers import create_user, create_staff, auth_client, create_nomina


class NominaPermisosTests(TestCase):
    def setUp(self):
        self.user  = create_user()
        self.admin = create_staff()

    def test_autenticado_puede_listar(self):
        resp = auth_client(self.user).get('/nomina/nominas/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_no_autenticado_retorna_401(self):
        resp = APIClient().get('/nomina/nominas/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_normal_no_puede_crear(self):
        resp = auth_client(self.user).post('/nomina/nominas/', {
            'anio': 2025, 'mes': 1, 'tipo': 'mensual'
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_puede_crear(self):
        resp = auth_client(self.admin).post('/nomina/nominas/', {
            'anio': 2025, 'mes': 1, 'tipo': 'mensual'
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['estado'], 'generada')


class NominaFlujoTests(TestCase):
    def setUp(self):
        self.admin  = create_staff()
        self.client = auth_client(self.admin)

    def test_aprobar_nomina_generada(self):
        nom = create_nomina(estado='generada')
        resp = self.client.post(f'/nomina/nominas/{nom.id}/aprobar/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['estado'], 'aprobada')

    def test_aprobar_nomina_ya_aprobada_retorna_400(self):
        nom = create_nomina(estado='aprobada')
        resp = self.client.post(f'/nomina/nominas/{nom.id}/aprobar/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pagar_nomina_aprobada(self):
        nom = create_nomina(estado='aprobada')
        resp = self.client.post(f'/nomina/nominas/{nom.id}/pagar/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['estado'], 'pagada')

    def test_pagar_nomina_no_aprobada_retorna_400(self):
        nom = create_nomina(estado='generada')
        resp = self.client.post(f'/nomina/nominas/{nom.id}/pagar/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_flujo_completo(self):
        nom = create_nomina(estado='generada')
        self.client.post(f'/nomina/nominas/{nom.id}/aprobar/')
        resp = self.client.post(f'/nomina/nominas/{nom.id}/pagar/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['estado'], 'pagada')

    def test_nomina_unica_por_anio_mes_tipo(self):
        create_nomina(anio=2025, mes=1, tipo='mensual')
        resp = self.client.post('/nomina/nominas/', {
            'anio': 2025, 'mes': 1, 'tipo': 'mensual'
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class NominaFiltrosTests(TestCase):
    def setUp(self):
        self.client = auth_client(create_user())
        create_nomina(anio=2025, mes=1, estado='generada')
        create_nomina(anio=2025, mes=2, estado='aprobada')
        create_nomina(anio=2025, mes=3, estado='pagada')

    def test_stats(self):
        resp = self.client.get('/nomina/nominas/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total', 'generadas', 'aprobadas', 'pagadas']:
            self.assertIn(field, resp.data)
        self.assertEqual(resp.data['total'], 3)
        self.assertEqual(resp.data['pagadas'], 1)