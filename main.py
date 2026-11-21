
    try:
        reserva_a_cancelar = next(
            (reserva for reserva in sistema.reservas if reserva.id == "R04"),
            None
        )

        if reserva_a_cancelar is not None:
            reserva_a_cancelar.cancelar()
            sistema.logger.registrar_evento(
                "INFO",
                f"Reserva {reserva_a_cancelar.id} cancelada por el usuario."
            )
            print(
                f"[OK] Reserva {reserva_a_cancelar.id} "
                "cancelada correctamente. Servicio liberado.\n"
            )
        else:
            print("[!] No se pudo cancelar R04 porque no fue confirmada.\n")

    except ErrorSistemaFJ as e:
        sistema.logger.registrar_evento("ERROR", f"Error al cancelar: {e}")
        print(f"[X] Error al cancelar: {e}")
