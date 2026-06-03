# Control de Nómina — API REST

Sistema de gestion de nomina desarrollado con Django REST Framework. Calcula automáticamente beneficios de ley (décimos, fondos de reserva), aportes al IESS y retención del Impuesto a la Renta según las tablas del SRI.

---

## Despliegue

Producción | https://venegas-nominas.uaeftt-ute.site
IP directa | http://20.150.222.163 
Admin Django | https://venegas-nominas.uaeftt-ute.site/admin/
---

## Requisitos previos

- Python 3.12+
- uv
- PostgreSQL 14+

---

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone <https://github.com/Alis0n09/venegas-control-nomina.git>
cd control-nomina
```

### 2. Instalar dependencias

```bash
uv sync
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DB_NAME=venegas_nominas
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

# Opcional — nombre de la BD para tests
TEST_DB_NAME=venegas_nominas_test_db
```

### 4. Crear la base de datos en PostgreSQL

```sql
CREATE DATABASE venegas_nominas;
```

### 5. Aplicar migraciones

```bash
uv run python manage.py migrate
```

### 6. Cargar datos iniciales (tablas SRI)

```bash
uv run python manage.py loaddata nomina/fixtures/impuesto_renta_2024.json
uv run python manage.py loaddata nomina/fixtures/impuesto_renta_2025.json
uv run python manage.py loaddata nomina/fixtures/impuesto_renta_2026.json
```

### 7. Crear superusuario (administrador)

```bash
uv run python manage.py createsuperuser
```

### 8. Ejecutar el servidor

```bash
uv run python manage.py runserver
```

## Autenticación

La API usa **JWT (JSON Web Tokens)**. Para acceder a los endpoints protegidos:

### Paso 1 — Obtener token

```http
POST /auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "tu_contraseña"
}
```

**Respuesta:**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "admin",
  "email": "admin@ejemplo.com",
  "is_staff": true
}
```

### Paso 2 — Usar el token en cada request

Agrega el header `Authorization` a todas tus peticiones:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Listado de Endpoints

### Autenticación

POST | `/auth/login/` | Obtener token JWT |
POST | `/auth/refresh/` | Refrescar access token  
POST | `/auth/logout/` | Cerrar sesión (invalida token) 

---

### Empleados — `/api/empleados/`

GET | `/api/empleados/` | Listar todos los empleados |
POST | `/api/empleados/` | Crear empleado 
GET | `/api/empleados/{id}/` | Ver empleado
GET | `/api/empleados/activos/` | Listar solo empleados activos | Público |
POST | `/api/empleados/{id}/desactivar/` | Desactivar empleado | Admin |
POST | `/api/empleados/{id}/reactivar/` | Reactivar empleado | Admin |
GET | `/api/empleados/stats/` | Estadísticas de empleados | Autenticado |


### Nóminas — `/api/nominas/`

GET | `/api/nominas/` | Listar nóminas 
POST | `/api/nominas/` | Crear nómina 
GET | `/api/nominas/{id}/` | Ver nómina con detalles
PUT | `/api/nominas/{id}/` | Actualizar nómina
PATCH | `/api/nominas/{id}/` | Actualizar nómina parcial  
POST | `/api/nominas/{id}/aprobar/` | Aprobar nómina (generada → aprobada) 
POST | `/api/nominas/{id}/pagar/` | Marcar como pagada 
GET | `/api/nominas/stats/` | Estadísticas de nóminas 


### Detalle de Nómina — `/api/detalles/`

GET | `/api/detalles/` | Listar detalles 
POST | `/api/detalles/` | Crear detalle (calcula automaticamente)
GET | `/api/detalles/{id}/` | Ver detalle 
PATCH | `/api/detalles/{id}/` | Actualizar detalle


### Descuentos — `/api/descuentos/`

GET | `/api/descuentos/` | Listar descuentos 
POST | `/api/descuentos/` | Crear descuento 
GET | `/api/descuentos/{id}/` | Ver descuento por nomina o empleado


### SBU — `/api/sbu/`

GET | `/api/sbu/` | Listar todos los SBU 
POST | `/api/sbu/` | Registrar SBU 
GET | `/api/sbu/vigente/` | SBU del año actual 


### Impuesto a la Renta — `/api/impuesto-renta/`

GET | `/api/impuesto-renta/` | Listar todo
GET | `/api/impuesto-renta/por-anio/{anio}/` |  Listar por año


### Usuarios — `/api/usuarios/`

GET | `/api/usuarios/` | Listar usuarios
POST | `/api/usuarios/` | Crear usuario
GET | `/api/usuarios/{id}/` | Ver usuario 
PATCH | `/api/usuarios/{id}/` | Actualizar usuario
DELETE | `/api/usuarios/{id}/` | Eliminar usuario
GET | `/api/usuarios/profile/` | Ver mi perfil 
PATCH | `/api/usuarios/profile/` | Editar mi perfil 
POST | `/api/usuarios/change-password/` | Cambiar mi contraseña 
POST | `/api/usuarios/{id}/toggle-active/` | Activar/desactivar usuario
GET | `/api/usuarios/stats/` | Estadísticas de usuarios 
---

## Ejemplos de uso con token

### Crear un empleado

```http
POST /api/empleados/
Authorization: Bearer <token>
Content-Type: application/json

{
  "cedula": "1234567890",
  "nombres": "Alison Liseth",
  "apellidos": "Venegas Calderon",
  "correo": "alison@nomina.com",
  "area": "Tecnología",
  "forma_pago": "transferencia",
  "banco": "Banco Pichincha",
  "tipo_cuenta": "ahorros",
  "numero_cuenta": "2200123456",
  "salario": "900.00",
  "numero_iess": "123456789001",
  "cargas_familiares":0,
  "fecha_ingreso": "2024-01-15"
}
```

### Crear una nómina

```http
POST /api/nominas/
Authorization: Bearer <token>
Content-Type: application/json

{
  "anio": 2025,
  "mes": 6,
  "tipo": "mensual"
}
```

### Agregar detalle a una nómina 

```http
POST /api/detalles/
Authorization: Bearer <token>
Content-Type: application/json

{
  "nomina": 1,
  "empleado": 1,
  "dias_laborados": 30,
  "horas_extras": "4.00",
  "bonos": "50.00",
  "ingreso_adicional": "0.00"
}
```

### Aprobar una nómina

```http
POST /api/nominas/1/aprobar/
Authorization: Bearer <token>
```

### Buscar empleados por nombre

```http
GET /api/empleados/?search=Juan&ordering=-salario
Authorization: Bearer <token>
```

### Ver tabla de IR por año

```http
GET /api/impuesto-renta/por-anio/2025/
Authorization: Bearer <token>
```

### Cambiar contraseña

```http
POST /api/usuarios/change-password/
Authorization: Bearer <token>
Content-Type: application/json

{
  "current_password": "contraseña_actual",
  "new_password": "nueva_contraseña_segura",
  "new_password2": "nueva_contraseña_segura"
}
```

---

## Colección Postman

Importar el archivo [`docs/Control Nómina API.postman_collection.json`](<docs/Control Nómina API.postman_collection.json>) en Postman.

---

## Tecnologias usadas

Python, 3.12, 
Django, 6.0 
Django REST Framework, 3.17 
SimpleJWT, 5.5  
django-filter, 25.2  
PostgreSQL, 14+ 
Gunicorn, 26.0 
uv, latest 
