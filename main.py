from scraper import CaprendizajeScraper
from ofertas_manager import OfertasManager
from config import Config
import time



print("[Main] Iniciando Caprendizaje Bot.")
caprendizaje_scraper = CaprendizajeScraper()
ofertas_manager = OfertasManager("data/ofertas.txt")
config = Config()

print("[Main] Abriendo la página de acceso.")
caprendizaje_scraper.abrir_login()
caprendizaje_scraper.presionar_boton("aprendices")
print("[Main] Enviando las credenciales de acceso.")
caprendizaje_scraper.insertar_credenciales(
    config.cc,
    config.password,
    "tbLoginUsuario",
    "__tbPasswordUsuario",
)
caprendizaje_scraper.presionar_boton("ini_session_aprendiz")
caprendizaje_scraper.verificar_sesion()
time.sleep(2)
caprendizaje_scraper.limpiar_elemento_por_clase("modal fade in")
caprendizaje_scraper.limpiar_elemento_por_clase("modal-backdrop fade in")
time.sleep(2)
caprendizaje_scraper.presionar_boton("btnBuscarEmpresa")
time.sleep(5)
ofertas_extraidas = caprendizaje_scraper.extraer_ofertas()
print("[Main] Guardando las ofertas nuevas.")
ofertas_nuevas = ofertas_manager.guardar_ofertas(ofertas_extraidas)

print(
    f"[Main] Proceso finalizado. Nuevas guardadas: "
    f"{len(ofertas_nuevas)}"
)
