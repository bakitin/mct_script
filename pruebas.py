from selenium import webdriver

url = "https://caprendizaje.sena.edu.co/sgva/SGVA_Diseno/pag/login.aspx"

driver = webdriver.Chrome()

try:
    driver.get(url)

    input("Presiona Enter cuando hayas terminado de observar la página...")

    print("Título:", driver.title)
    print("URL actual:", driver.current_url)
finally:
    driver.quit()