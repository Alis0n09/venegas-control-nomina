from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .helpers import create_user, create_staff, get_tokens


class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user   = create_user('ana', password='Pass1234!')

    def test_login_devuelve_tokens(self):
        resp = self.client.post('/auth/login/', {
            'username': 'ana', 'password': 'Pass1234!'
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access',   resp.data)
        self.assertIn('refresh',  resp.data)
        self.assertIn('username', resp.data)
        self.assertIn('is_staff', resp.data)

    def test_login_credenciales_incorrectas(self):
        resp = self.client.post('/auth/login/', {
            'username': 'ana', 'password': 'wrongpass'
        })
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_staff_devuelve_is_staff_true(self):
        create_staff('jefe', password='Admin1234!')
        resp = self.client.post('/auth/login/', {
            'username': 'jefe', 'password': 'Admin1234!'
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['is_staff'])


class RefreshLogoutTests(TestCase):
    def setUp(self):
        self.client  = APIClient()
        self.user    = create_user('bob')
        self.access, self.refresh = get_tokens(self.user)

    def test_refresh_devuelve_nuevo_access(self):
        resp = self.client.post('/auth/refresh/', {'refresh': self.refresh})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)

    def test_logout_invalida_refresh(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        resp = self.client.post('/auth/logout/', {'refresh': self.refresh})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # intentar usar el refresh ya inválido
        resp2 = self.client.post('/auth/refresh/', {'refresh': self.refresh})
        self.assertEqual(resp2.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_sin_refresh_retorna_400(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')
        resp = self.client.post('/auth/logout/', {})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_sin_autenticacion_retorna_401(self):
        resp = self.client.post('/auth/logout/', {'refresh': self.refresh})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)