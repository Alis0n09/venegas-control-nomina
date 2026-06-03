from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from nomina.tests.helpers import (create_user, create_staff, auth_client,create_empleado, create_nomina, create_detalle,create_sbu, create_tabla_ir,
)


class DetallePermisosTests(TestCase):
    def setUp(self):
        self.user    = create_user()
        self.admin   = create_staff()
        self.nomina  = create_nomina()
        self.emp     = create_empleado()

    def test_autenticado_puede_listar(self):
        resp = auth_client(self.user).get('/nomina/detalles/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_no_autenticado_retorna_401(self):
        resp = APIClient().get('/nomina/detalles/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_normal_no_puede_crear(self):
        resp = auth_client(self.user).post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id, 'dias_laborados': 30
        })
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_puede_crear(self):
        create_sbu()
        create_tabla_ir()
        resp = auth_client(self.admin).post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id, 'dias_laborados': 30
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)


class DetalleCalculosTests(TestCase):
    def setUp(self):
        self.admin   = create_staff()
        self.client  = auth_client(self.admin)
        create_sbu()
        create_tabla_ir()
        self.nomina  = create_nomina()
        self.emp     = create_empleado(salario=800)

    def test_calcula_subtotal_imponible(self):
        resp = self.client.post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id, 'dias_laborados': 30
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(resp.data['subtotal_imponible']), 800.00)

    def test_calcula_aporte_iess(self):
        resp = self.client.post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id, 'dias_laborados': 30
        })
        self.assertEqual(float(resp.data['aporte_personal_iess']), 75.60)

    def test_calcula_decimos_informativos(self):
        resp = self.client.post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id, 'dias_laborados': 30
        })
        self.assertGreater(float(resp.data['decimo_tercero']), 0)
        self.assertGreater(float(resp.data['decimo_cuarto']), 0)

    def test_valor_a_recibir_menor_que_subtotal(self):
        resp = self.client.post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id, 'dias_laborados': 30
        })
        subtotal = float(resp.data['subtotal_imponible'])
        a_recibir = float(resp.data['valor_a_recibir'])
        self.assertLess(a_recibir, subtotal)

    def test_campos_calculados_son_readonly(self):
        resp = self.client.post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id,
            'dias_laborados': 30, 'subtotal_imponible': '99999',
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(float(resp.data['subtotal_imponible']), 99999)


class DetalleValidacionesTests(TestCase):
    def setUp(self):
        self.admin   = create_staff()
        self.client  = auth_client(self.admin)
        self.nomina  = create_nomina()
        self.emp     = create_empleado()

    def test_dias_negativos_retorna_400(self):
        resp = self.client.post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id, 'dias_laborados': -1
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dias_mayores_31_retorna_400(self):
        resp = self.client.post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id, 'dias_laborados': 32
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empleado_duplicado_en_nomina_retorna_400(self):
        create_sbu()
        create_tabla_ir()
        create_detalle(nomina=self.nomina, empleado=self.emp)
        resp = self.client.post('/nomina/detalles/', {
            'nomina': self.nomina.id, 'empleado': self.emp.id, 'dias_laborados': 30
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class DetalleFiltrosTests(TestCase):
    def setUp(self):
        self.client  = auth_client(create_user())
        self.nomina  = create_nomina()
        self.emp     = create_empleado()
        create_detalle(nomina=self.nomina, empleado=self.emp)

    def test_por_nomina(self):
        resp = self.client.get(f'/nomina/detalles/por-nomina/{self.nomina.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for d in resp.data['results']:
            self.assertEqual(d['nomina'], self.nomina.id)

    def test_por_empleado(self):
        resp = self.client.get(f'/nomina/detalles/por-empleado/{self.emp.id}/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_stats(self):
        resp = self.client.get('/nomina/detalles/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total_detalles', 'total_ingresos', 'total_a_pagar', 'promedio_a_recibir']:
            self.assertIn(field, resp.data)