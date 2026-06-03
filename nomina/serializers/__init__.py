from .empleado import EmpleadoSerializer, EmpleadoSummarySerializer
from .nomina import NominaSerializer, NominaSummarySerializer
from .detalle_nomina import DetalleNominaSerializer, DetalleNominaSummarySerializer
from .descuentos import DescuentoSerializer
from .sbu import SBUSerializer
from .impuesto_renta import ImpuestoRentaSerializer
from .auth import CustomTokenSerializer, CustomTokenView
from .user import UserSerializer, CreateUserSerializer, UserProfileSerializer, ChangePasswordSerializer