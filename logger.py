# prof4
#Fase 4- componente practico-Practicas simuladas
from datetime import datetime

class LoggerSistema:
    def __init__(self, nombre_archivo="sistema_software_fj.log"):
        self.nombre_archivo = nombre_archivo

    def registrar_evento(self, nivel, mensaje):
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}\n"
        try:
            with open(self.nombre_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except IOError as e:
            print(f"Error crítico al escribir en el archivo de logs: {e}")
