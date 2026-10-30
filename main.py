from scraper import CaprendizajeScraper
from ofertas_manager import OfertasManager
import time


print("[Main] Iniciando Caprendizaje Bot.")
scraper = CaprendizajeScraper()
ofertas_manager = OfertasManager("data/ofertas.txt")

print("[Main] Abriendo la página de acceso.")
scraper.abrir_login()
scraper.presionar_boton("aprendices")
print("[Main] Enviando las credenciales de acceso.")
scraper.insertar_credenciales("1006049956","5529FA44","tbLoginUsuario","__tbPasswordUsuario")
scraper.presionar_boton("ini_session_aprendiz")
scraper.verificar_sesion()
time.sleep(2)
scraper.limpiar_elemento_por_clase("modal fade in")
scraper.limpiar_elemento_por_clase("modal-backdrop fade in")
time.sleep(2)
scraper.presionar_boton("btnBuscarEmpresa")
time.sleep(5)
ofertas = scraper.extraer_ofertas()
print("[Main] Guardando las ofertas nuevas.")
resultado = ofertas_manager.guardar_ofertas(ofertas)

print(f"[Main] Proceso finalizado. Nuevas guardadas: {len(resultado)}")
