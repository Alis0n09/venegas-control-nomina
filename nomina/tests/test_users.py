from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from nomina.tests.helpers import create_user, create_staff, auth_client


class ProfileTests(TestCase):
    def setUp(self):
        self.user   = create_user('carlos')
        self.client = auth_client(self.user)

    def test_ver_perfil_propio(self):
        resp = self.client.get('/nomina/usuarios/profile/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['username'], 'carlos')

    def test_editar_perfil_propio(self):
        resp = self.client.patch('/nomina/usuarios/profile/', {'first_name': 'Carlos'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['first_name'], 'Carlos')

    def test_cambiar_password_correcto(self):
        resp = self.client.post('/nomina/usuarios/change-password/', {
            'current_password': 'Pass1234!',
            'new_password':     'Nueva5678!',
            'new_password2':    'Nueva5678!',
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_cambiar_password_actual_incorrecta(self):
        resp = self.client.post('/nomina/usuarios/change-password/', {
            'current_password': 'Incorrecta!',
            'new_password':     'Nueva5678!',
            'new_password2':    'Nueva5678!',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cambiar_password_no_coinciden(self):
        resp = self.client.post('/nomina/usuarios/change-password/', {
            'current_password': 'Pass1234!',
            'new_password':     'Nueva5678!',
            'new_password2':    'Diferente!',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class UsuariosStaffTests(TestCase):
    def setUp(self):
        self.admin  = create_staff()
        self.user   = create_user('diana')
        self.client = auth_client(self.admin)

    def test_admin_puede_listar_usuarios(self):
        resp = self.client.get('/nomina/usuarios/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('results', resp.data)

    def test_usuario_normal_no_puede_listar(self):
        resp = auth_client(self.user).get('/nomina/usuarios/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_autenticado_retorna_401(self):
        resp = APIClient().get('/nomina/usuarios/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crear_usuario(self):
        resp = self.client.post('/nomina/usuarios/', {
            'username':  'nuevo',
            'email':     'nuevo@test.com',
            'password':  'Pass1234!',
            'password2': 'Pass1234!',
            'is_staff':  False,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['username'], 'nuevo')
        self.assertFalse(resp.data['is_staff'])

    def test_crear_usuario_username_duplicado(self):
        create_user('juan')
        resp = self.client.post('/nomina/usuarios/', {
            'username':  'juan',
            'email':     'otro@test.com',
            'password':  'Pass1234!',
            'password2': 'Pass1234!',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_usuario_passwords_no_coinciden(self):
        resp = self.client.post('/nomina/usuarios/', {
            'username':  'nuevo',
            'email':     'nuevo@test.com',
            'password':  'Pass1234!',
            'password2': 'Diferente!',
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_toggle_active_desactiva(self):
        resp = self.client.post(f'/nomina/usuarios/{self.user.id}/toggle-active/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(resp.data['is_active'])

    def test_toggle_active_reactiva(self):
        self.user.is_active = False
        self.user.save()
        resp = self.client.post(f'/nomina/usuarios/{self.user.id}/toggle-active/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['is_active'])

    def test_stats(self):
        resp = self.client.get('/nomina/usuarios/stats/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for field in ['total', 'activos', 'inactivos', 'staff']:
            self.assertIn(field, resp.data)

    def test_filtrar_por_is_staff(self):
        resp = self.client.get('/nomina/usuarios/?is_staff=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for u in resp.data['results']:
            self.assertTrue(u['is_staff'])

    def test_buscar_por_username(self):
        resp = self.client.get('/nomina/usuarios/?search=diana')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)
        self.assertEqual(resp.data['results'][0]['username'], 'diana')