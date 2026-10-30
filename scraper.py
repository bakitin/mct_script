from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class CaprendizajeScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def abrir_login(self):
        url_login = "https://caprendizaje.sena.edu.co/sgva/SGVA_Diseno/pag/login.aspx"
        self.driver.get(url_login)
        print("[Selenium] Página de inicio de sesión abierta.")
        

    def presionar_boton(self, id_elemento):
        boton = self.driver.find_element(By.ID, id_elemento)
        self.driver.execute_script("arguments[0].click();", boton)
        print(f"[Selenium] Botón pulsado: {id_elemento}")
        
    def insertar_credenciales(
        self,
        usuario,
        contrasena,
        id_campo_usuario,
        id_campo_contrasena,
    ):
        campo_usuario = self.driver.find_element(By.ID, id_campo_usuario)
        campo_usuario.send_keys(usuario)

        campo_contrasena = self.driver.find_element(By.ID, id_campo_contrasena)
        campo_contrasena.send_keys(contrasena)

    def limpiar_elemento_por_clase(self, nombre_clase):
        selector_css = "." + nombre_clase.strip().replace(" ", ".")
        elementos_encontrados = self.driver.find_elements(
            By.CSS_SELECTOR, selector_css
        )
        for elemento in elementos_encontrados:
            self.driver.execute_script("arguments[0].remove();", elemento)

    def verificar_sesion(self):
        elemento_sesion = self.driver.find_element(By.ID, "lbl_especialidad")
        if elemento_sesion:
            print("[Selenium] Sesión iniciada correctamente.")

    def extraer_ofertas(self):
        ofertas_formateadas = []
        try:
            textos_ofertas = []
            nombres_empresas = []
            contenedor_ofertas = self.driver.find_element(By.ID, "div_solicitudes")
            botones_ofertas = contenedor_ofertas.find_elements(By.ID, "solicitud_aplicar")
            titulos_empresas = contenedor_ofertas.find_elements(
                By.CLASS_NAME,
                "aprendizLabelTituloSolicitudesBA",
            )
            nombres_empresas = [
                titulo.text.strip() for titulo in titulos_empresas
            ]

            if len(nombres_empresas) != len(botones_ofertas):
                raise RuntimeError(
                    "La cantidad de nombres de empresa no coincide "
                    "con la cantidad de ofertas."
                )

            print(
                f"[Selenium] Ofertas disponibles para revisar: "
                f"{len(botones_ofertas)}"
            )
            for indice, boton_oferta in enumerate(botones_ofertas):
                self.driver.execute_script("arguments[0].click();", boton_oferta)
                time.sleep(2)
                selector_css = "." + "modal-body aprendizModalCuerpo".strip().replace(" ", ".")
                modales_encontrados = self.driver.find_elements(
                    By.CSS_SELECTOR, selector_css
                )
            
                for modal in modales_encontrados:
                    if modal.is_displayed():
                        textos_ofertas.append(modal.text)
                        
            ofertas_formateadas = self._formatear_oferta(textos_ofertas)

            for oferta, nombre_empresa in zip(
                ofertas_formateadas,
                nombres_empresas,
            ):
                oferta["Empresa"] = nombre_empresa

            print(
                f"[Selenium] Ofertas extraídas y formateadas: "
                f"{len(ofertas_formateadas)}"
            )
        finally:
            self._cerrar()
        print("[Selenium] Navegador cerrado.")
        return ofertas_formateadas

    def _formatear_oferta(self, textos_ofertas):
        ofertas_formateadas = []

        for texto_oferta in textos_ofertas:
            oferta_formateada = {}
            campo_actual = None
            lineas_oferta = texto_oferta.splitlines()

            for linea in lineas_oferta:
                linea = linea.strip()

                if linea in [
                    "Aplicar",
                    "Cerrar",
                    "TECNÓLOGO EN ANALISIS Y DESARROLLO DE SOFTWARE.",
                ] or not linea:
                    continue

                if linea in ["Perfil:", "Funciones a desarrollar:"]:
                    campo_actual = linea[:-1]
                    oferta_formateada[campo_actual] = ""
                    continue

                if campo_actual is not None and ":" not in linea:
                    if oferta_formateada[campo_actual]:
                        oferta_formateada[campo_actual] += " " + linea
                    else:
                        oferta_formateada[campo_actual] = linea
                    continue

                if ":" in linea:
                    clave, valor = linea.split(":", 1)
                    oferta_formateada[clave.strip()] = valor.strip()
                    campo_actual = None

            ofertas_formateadas.append(oferta_formateada)

        return ofertas_formateadas
        
        
        
   
    def _cerrar(self):
        self.driver.quit()
