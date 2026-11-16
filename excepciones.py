class ErrorSistemaFJ(Exception):
    """Excepción base para todo el sistema de Software FJ."""
    pass

class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un parámetro tiene formato o valor incorrecto."""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio inactivo o no disponible."""
    pass

class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza al intentar cambiar el estado de una reserva de forma inválida."""
    pass

class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando el cálculo de costos arroja un resultado negativo o nulo."""
    pass
