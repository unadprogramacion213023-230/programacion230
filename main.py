import logging  # este Permite registrar errores en un archivo externo [cite: 92, 105]
from abc import ABC, abstractmethod  # Necesario para crear clases abstractas 

# CONFIGURACIÓN DE LOGS: Crea un archivo llamado 'errores.log' para registrar fallos [cite: 92]
logging.basicConfig(filename='errores.log', level=logging.ERROR, format='%(asctime)s: %(message)s')

# --- 1. EXCEPCIONES PERSONALIZADAS ---
# Estas clases permiten manejar errores específicos del negocio [cite: 91]
class ErrorSistema(Exception): pass
class DatoInvalidoError(ErrorSistema): pass

# --- 2. CLASE ABSTRACTA ENTIDAD ---
# Representa una entidad general del sistema [cite: 95]
class Entidad(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad  # Encapsulación protegida

    @abstractmethod
    def obtener_datos(self):
        pass

# --- 3. CLASE CLIENTE ---
# Gestiona la información de los usuarios con validaciones 
class Cliente(Entidad):
    def __init__(self, id_entidad, nombre, correo):
        super().__init__(id_entidad)
        if "@" not in correo:  # Validación de datos [cite: 93]
            raise DatoInvalidoError(f"Correo electrónico inválido: {correo}")
        self.__nombre = nombre  # Atributo privado para encapsulación
        self.__correo = correo

    def obtener_datos(self):
        return f"Cliente: {self.__nombre} (ID: {self._id_entidad})"

# --- 4. CLASE ABSTRACTA SERVICIO Y DERIVADAS ---
# Define la estructura para los diferentes servicios [cite: 97, 98]
class Servicio(ABC):
    def __init__(self, tipo, costo_por_hora):
        self.tipo = tipo
        self.costo_por_hora = costo_por_hora

    @abstractmethod
    def calcular_costo(self, horas):
        pass

class AlquilerEquipo(Servicio):
    def calcular_costo(self, horas):
        return self.costo_por_hora * horas

class AsesoriaEspecializada(Servicio):
    # Polimorfismo: implementa su propia lógica de cálculo 
    def calcular_costo(self, horas):
        return (self.costo_por_hora * horas) * 1.10  # Incluye un 10% de cargo administrativo

# --- 5. CLASE RESERVA ---
# Clase principal que coordina la operación y maneja excepciones [cite: 99]
class Reserva:
    def __init__(self, cliente, servicio, horas):
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas

    def procesar_reserva(self):
        try:
            # Bloque de intento de ejecución [cite: 91]
            if self.horas <= 0:
                raise DatoInvalidoError("La duración debe ser mayor a cero horas.")
            
            total = self.servicio.calcular_costo(self.horas)
            print(f"Reserva Confirmada: {self.cliente.obtener_datos()} - {self.servicio.tipo}. Total: ${total}")
            
        except DatoInvalidoError as e:
            # Captura errores de datos inválidos y los guarda en el log 
            print(f"Error en los datos: {e}")
            logging.error(f"Fallo en reserva: {e}")
        except Exception as e:
            # Captura cualquier otro error inesperado [cite: 91]
            print(f"Ocurrió un error inesperado.")
            logging.error(f"Error crítico: {e}")
        finally:
            # Se ejecuta siempre, garantizando estabilidad [cite: 85, 91]
            print("Finalizando proceso de reserva.")

# --- 6. SIMULACIÓN DE OPERACIONES ---
# Demuestra que el sistema funciona incluso con errores [cite: 106]
def ejecutar():
    print("--- SIMULACIÓN SISTEMA SOFTWARE FJ ---")
    
    # 1. Creación de clientes (Válidos e Inválidos)
    try:
        c1 = Cliente(101, "Carlos Pérez", "carlos@mail.com")
        c2 = Cliente(102, "Marta Ruiz", "correo_sin_arroba") # Esto generará error
    except DatoInvalidoError as e:
        print(f"No se pudo crear cliente: {e}")
        logging.error(e)
        c2 = None

    # 2. Definición de servicios
    s1 = AlquilerEquipo("Portátil Dell", 25000)
    s2 = AsesoriaEspecializada("Asesoría Java", 50000)

    # 3. Procesamiento de reservas (Éxito y Fallo)
    reserva1 = Reserva(c1, s1, 5)  # Exitosa
    reserva1.procesar_reserva()

    if c1:
        reserva2 = Reserva(c1, s2, -2) # Fallida por horas negativas
        reserva2.procesar_reserva()

if __name__ == "__main__":
    ejecutar()