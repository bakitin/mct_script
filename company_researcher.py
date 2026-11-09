

class CompanyResearcher:
    def __init__(self, ofertas):
        self.ofertas = ofertas
        pass
        

    def buscar_empresa(self):
        empresas = self._obtener_nombre_empresas()

        resultados = []

        for nombre in empresas:
            resultados.append({"Empresa": nombre,"Fuentes":[]})
            
        
        return resultados

    def guardar_fuentes(self):
        pass

    def _obtener_nombre_empresas(self):
        nombres_empresas = []

        for oferta in self.ofertas:
            empresa = oferta.get("Empresa", "")
            empresa_limpia = empresa.strip()

            if not empresa_limpia:
                raise ValueError("Una oferta no tiene nombre de empresa")

            nombres_empresas.append(empresa_limpia)

        return nombres_empresas