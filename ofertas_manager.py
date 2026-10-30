import os
import hashlib



class OfertasManager():
    def __init__(self, ruta):
        self.ruta = ruta


    def guardar_ofertas(self,ofertas):
        lista = []
        ofertas_nuevas = self._filtrar_ofertas_nuevas(ofertas)
        repetidas = len(ofertas) - len(ofertas_nuevas)
        print(
            f"[TXT] Recibidas: {len(ofertas)} | "
            f"Nuevas: {len(ofertas_nuevas)} | "
            f"Repetidas: {repetidas}"
        )

        if not os.path.exists(self.ruta):
            with open(self.ruta, "a", encoding="utf-8"):
                pass
            print(f"[TXT] Archivo creado: {self.ruta}")

        if ofertas_nuevas:
            for oferta in ofertas_nuevas:
                identificador = self._crear_identificador(oferta)
                oferta_formateada = self._formatear_para_txt(oferta,identificador)
                lista.append(oferta_formateada)
            texto = "\n".join(lista)
    
            with open(self.ruta, "a", encoding="utf-8") as archivo:
                archivo.write(texto)
            print(f"[TXT] Agregadas {len(ofertas_nuevas)} ofertas nuevas.")
        else:
            print("[TXT] No hay ofertas nuevas para agregar.")

        return ofertas_nuevas


    def _formatear_para_txt(self,oferta, identificador):
        lineas = []
        separador = "=" * 40
        lineas.append(separador)
        lineas.append("ID: "+identificador)
        for clave, valor in oferta.items():
            lineas.append(f"{clave}: {valor}")
        lineas.append(separador)
        return "\n".join(lineas)
    

    def _crear_identificador(self,oferta):
        campos_estables = [
            oferta.get("Correo electrónico", ""),
            oferta.get("Persona de contacto", ""),
            oferta.get("Dirección", ""),
            oferta.get("Fecha de creación", ""),
            oferta.get("Fecha de cierre", ""),
            oferta.get("Funciones a desarrollar", "")
        ]
        texto = "|".join(campos_estables)
        huella = hashlib.sha256(texto.encode("utf-8")).hexdigest()
        identificador = "CAP-" + huella[:8].upper()
        return identificador

    def _leer_identificadores(self):
        conjunto = []
        existe = os.path.exists(self.ruta)
        if not existe:
            return []    
        with open(self.ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        for linea in contenido.splitlines():
            if linea.startswith("ID:"):
                linea_limpia = linea.split(":")
                conjunto.append(linea_limpia[1].strip())
        return conjunto

    def _filtrar_ofertas_nuevas(self,ofertas) -> list:
        lista_nueva = []
        lista_id = self._leer_identificadores()
        
        for oferta in ofertas:
            identificador = self._crear_identificador(oferta)

            if identificador not in lista_id:
                lista_nueva.append(oferta)

        return lista_nueva 