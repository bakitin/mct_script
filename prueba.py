from ddgs import DDGS
import time

def _investigar_empresa_gratis(nombre_empresa, ciudad):
    print(f"🔍 Buscando información en la web sobre: {nombre_empresa}...")
    consulta = f"{nombre_empresa} {ciudad} Colombia a que se dedica"
    
    texto_recolectado = []
    # Lista de motores de respaldo (el primero es el predeterminado)
    motores = ["auto", "duckduckgo", "google", "bing", "yahoo"]
    
    for motor in motores:
        try:
            # Ponemos un pequeño timeout por si el servidor se queda pensando para bloquearnos
            ddgs = DDGS(timeout=10) 
            resultados = ddgs.text(consulta, max_results=3, backend=motor)
            
            if resultados:
                for res in resultados:
                    texto_recolectado.append(f"- Fuente: {res.get('href', 'Sin enlace')} Resumen: {res.get('body', 'Sin resumen')}")
                
                # Si funcionó y trajo datos, devolvemos la lista y rompemos el ciclo
                return texto_recolectado
                
        except Exception as e:
            # Si este motor falla o nos bloquea, simplemente intentamos con el siguiente
            continue
            
    # Si llega hasta aquí, significa que TODOS los motores fallaron o bloquearon la IP
    print("⚠️ Todos los motores de búsqueda bloquearon la petición.")
    return ["No se encontró información en internet."]

texto = _investigar_empresa_gratis("Colpensiones", "Cali")
if texto and texto[0] != "No se encontró información en internet.":
    print(texto[0])
else:
    print(texto[0])