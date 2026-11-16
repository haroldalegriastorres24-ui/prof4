from abc import ABC, abstractmethod
from excepciones import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError
)

# 1. Clase abstracta que representa entidades generales
class EntidadBase(ABC):
    def __init__(self, id_entidad: str):
        if not id_entidad or not isinstance(id_entidad, str):
            raise DatoInvalidoError("El ID de la entidad debe ser una cadena de texto no vacía.")
        self._id = id_entidad.strip()

    @property
    def id(self):
        return self._id

    @abstractmethod
    def validar_datos(self):
        pass


# 2. Clase Cliente con encapsulación y validaciones estrictas
class Cliente(EntidadBase):
    def __init__(self, id_cliente: str, nombre: str, correo: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.validar_datos()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in valor or "." not in valor:
            raise DatoInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self._correo = valor.strip()

    def validar_datos(self):
        if not self._id or not self._nombre or not self._correo:
            raise DatoInvalidoError("Todos los datos del cliente son obligatorios.")


# 3. Clase abstracta Servicio
class Servicio(EntidadBase):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible
        self.validar_datos()

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    def validar_datos(self):
        if not self._nombre or len(self._nombre.strip()) < 3:
            raise DatoInvalidoError("El nombre del servicio es inválido.")
        if not isinstance(self._tarifa_base, (int, float)) or self._tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser un número mayor a cero.")

    # Simulación de sobrecarga de métodos mediante parámetros opcionales
    @abstractmethod
    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass


# Servicios especializados (Herencia y Polimorfismo)
class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        self.capacidad = capacidad
        super().__init__(id_servicio, nombre, tarifa_base, disponible)

    def validar_datos(self):
        super().validar_datos()
        if self.capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a 0 personas.")

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        if duracion <= 0:
            raise DatoInvalidoError("La duración en horas debe ser mayor a cero.")
        subtotal = self._tarifa_base * duracion
        total = (subtotal - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El costo total de la sala no puede ser menor o igual a cero.")
        return round(total, 2)

    def describir_servicio(self) -> str:
        return f"Sala '{self._nombre}' (Capacidad: {self.capacidad} pers.) - Base: ${self._tarifa_base}/h"


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, categoria: str, disponible: bool = True):
        self.categoria = categoria
        super().__init__(id_servicio, nombre, tarifa_base, disponible)

    def validar_datos(self):
        super().validar_datos()
        if not self.categoria:
            raise DatoInvalidoError("La categoría del equipo es obligatoria.")

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        if duracion <= 0:
            raise DatoInvalidoError("Los días de alquiler deben ser mayores a cero.")
        seguro_equipo = 15.0  # Cargo fijo adicional por seguro
        subtotal = (self._tarifa_base * duracion) + seguro_equipo
        total = (subtotal - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El costo total del alquiler resultó inconsistente.")
        return round(total, 2)

    def describir_servicio(self) -> str:
        return f"Equipo '{self._nombre}' [{self.categoria}] - Base: ${self._tarifa_base}/día (+ seguro)"


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        self.especialidad = especialidad
        super().__init__(id_servicio, nombre, tarifa_base, disponible)

    def validar_datos(self):
        super().validar_datos()
        if not self.especialidad:
            raise DatoInvalidoError("La especialidad de la asesoría es obligatoria.")

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        if duracion <= 0:
            raise DatoInvalidoError("Las horas de asesoría deben ser mayores a cero.")
        subtotal = self._tarifa_base * duracion
        # Si dura más de 5 horas aplica bono extra de descuento automático
        if duracion > 5:
            descuento += 20.0
        total = (subtotal - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El cálculo de la asesoría arrojó un valor negativo o cero.")
        return round(total, 2)

    def describir_servicio(self) -> str:
        return f"Asesoría '{self._nombre}' (Área: {self.especialidad}) - Base: ${self._tarifa_base}/h"


# 4. Clase Reserva
class Reserva(EntidadBase):
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        super().__init__(id_reserva)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self._estado = "PENDIENTE"
        self._costo_total = 0.0
        self.validar_datos()

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def validar_datos(self):
        if not isinstance(self.cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere un objeto Cliente válido.")
        if not isinstance(self.servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere un objeto Servicio válido.")
        if self.duracion <= 0:
            raise DatoInvalidoError("La duración de la reserva debe ser positiva.")

    def procesar_y_confirmar(self, impuesto: float = 0.19, descuento: float = 0.0):
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre}' no está disponible.")
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado {self._estado}.")
        
        try:
            self._costo_total = self.servicio.calcular_costo(self.duracion, impuesto, descuento)
            self._estado = "CONFIRMADA"
            self.servicio.disponible = False
        except CalculoInconsistenteError as e:
            # Encadenamiento de excepciones solicitado en el enunciado
            raise OperacionNoPermitidaError("Fallo al procesar el cobro de la reserva.") from e

    def cancelar(self):
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError("La reserva ya se encuentra cancelada.")
        self._estado = "CANCELADA"
        self.servicio.disponible = True
