from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class CaprendizajeScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def abrir_login(self):
        url = "https://caprendizaje.sena.edu.co/sgva/SGVA_Diseno/pag/login.aspx"
        self.driver.get(url)
        print("[Selenium] Página de inicio de sesión abierta.")
        

    def presionar_boton(self,id):
        button = self.driver.find_element(By.ID,id)
        self.driver.execute_script("arguments[0].click();", button)
        print(f"[Selenium] Botón pulsado: {id}")
        
    def insertar_credenciales(self,usuario,contrasena,campousuario,campocontrasena):
        user_fild = self.driver.find_element(By.ID,campousuario)
        user_fild.send_keys(usuario)

        password_fild = self.driver.find_element(By.ID,campocontrasena)
        password_fild.send_keys(contrasena)

    def limpiar_elemento_por_clase(self, nombre_clase):
        selector_css = "." + nombre_clase.strip().replace(" ", ".")
        elementos = self.driver.find_elements(By.CSS_SELECTOR, selector_css)
        for elemento in elementos:
            self.driver.execute_script("arguments[0].remove();", elemento)

    def verificar_sesion(self):
        elementos = self.driver.find_element(By.ID, "lbl_especialidad")
        if elementos:
            print("[Selenium] Sesión iniciada correctamente.")

    def extraer_ofertas(self):
        ofertas_extraidas = []
        row_principal = self.driver.find_element(By.ID, "div_solicitudes")
        botones = row_principal.find_elements(By.ID, "solicitud_aplicar")
        print(f"[Selenium] Ofertas disponibles para revisar: {len(botones)}")
        for boton in botones:
            self.driver.execute_script("arguments[0].click();", boton)
            time.sleep(2)
            selector_css = "." + "modal-body aprendizModalCuerpo".strip().replace(" ", ".")
            elementos = self.driver.find_elements(By.CSS_SELECTOR, selector_css)
        
            for info in elementos:
                if info.is_displayed():
                    ofertas_extraidas.append(info.text)
                    
        ofertas = self._formatear_oferta(ofertas_extraidas)
        print(f"[Selenium] Ofertas extraídas y formateadas: {len(ofertas)}")
        self._cerrar()
        print("[Selenium] Navegador cerrado.")
        return ofertas

    def _formatear_oferta(self, ofertas):
        ofertas_formateadas = []

        for oferta in ofertas:
            oferta_formateada = {}
            campo_actual = None
            lineas = oferta.splitlines()

            for linea in lineas:
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
