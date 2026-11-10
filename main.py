from scraper import CaprendizajeScraper
from ofertas_manager import OfertasManager
from config import Config
from gemini_service import GeminiService
from email_service import EmailService
import time



print("[Main] Iniciando Caprendizaje Bot.")
caprendizaje_scraper = CaprendizajeScraper()
ofertas_manager = OfertasManager("data/ofertas.txt")
config = Config()
print("[Main] Configuración cargada.")

print("[Main] Abriendo la página de acceso.")
caprendizaje_scraper.abrir_login()
caprendizaje_scraper.presionar_boton("aprendices")
print("[Main] Enviando las credenciales de acceso.")
caprendizaje_scraper.insertar_credenciales(
    config.numero_documento,
    config.contrasena_caprendizaje,
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
print(f"[Main] Ofertas extraídas: {len(ofertas_extraidas)}")
print("[Main] Guardando las ofertas nuevas.")
ofertas_nuevas = ofertas_manager.guardar_ofertas(ofertas_extraidas)

print(
    f"[Main] Proceso finalizado. Nuevas guardadas: "
    f"{len(ofertas_nuevas)}"
)

if ofertas_nuevas:
    print("[Main] Ofertas nuevas listas para Gemini.")
    gemini_service = GeminiService(config.gemini_api_key)
    resultados_gemini = gemini_service.generar_correos(ofertas_nuevas)
    print(f"[Main] Resultados recibidos de Gemini: {len(resultados_gemini)}")

    email_service = EmailService(config.smtp_host, config.smtp_port)
    print("[Main] Conectando con el servidor SMTP.")
    email_service.conectar_smtp(
        config.cuenta_correo,
        config.contrasena_aplicacion,
    )

    mensajes_enviados = 0
    print("[Main] Enviando postulaciones.")
    try:
        for mensaje in email_service.crear_mensajes(resultados_gemini):
            email_service.enviar_correo(mensaje)
            mensajes_enviados += 1
            print(
                f"[Correo] Postulación enviada a {mensaje['To']} "
                f"({mensajes_enviados}/{len(resultados_gemini)})."
            )
    finally:
        email_service.desconectar_smtp()
        print("[Main] Conexión SMTP cerrada.")

    print(f"[Main] Postulaciones enviadas: {mensajes_enviados}")

else:
    print("[Main] No hay ofertas nuevas para enviar a Gemini.")
