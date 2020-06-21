from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time



def inicializar():
    """
    Inicializa la pagina

    Devuelve el objeto webdriver
    """
    driver_path = 'test/chromedriver/chromedriverv83.exe'
    driver_path = 'chromedriver/chromedriverv83.exe'

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
    wait = WebDriverWait(driver, 5) # define el tiempo maximo de espera

    driver = reinicia(driver,wait)

    return driver,wait

def reinicia(driver,wait):
    """"
    Vuelve a la pagina de los mapas 
    """
    driver.get("https://jellyfish-forecast.herokuapp.com/")
    assert "Jellyfish" in driver.title
    boton_mapa = driver.find_elements_by_name('Mapas')[0]
    boton_mapa.click()
    return driver

#### TEST ####
def comprueba_error_fecha_no_introducida(driver,wait):
    """
    Comprueba que si se introduce una playa sin fecha lanza mensaje de error

    Si no se ha lanzado, lanza una excepcion

    Parametros:
    driver -- objeto webdriver
    """
    select = Select(driver.find_element_by_name('eleccion'))
    select.select_by_visible_text('Bahía.Coliumo')

    boton = driver.find_element_by_name('boton_consultar')
    boton.click()
    print('paso')

    wait.until(EC.element_to_be_clickable((By.NAME, 'alerta')))

def main():
    driver,wait = inicializar() # se abre la pagina de mapas
    try:
        print('Prueba 1: Se selecciona playa sin una fecha')
        comprueba_error_fecha_no_introducida(driver,wait)
        print("Exito")
    except:
        print("Fracaso")
        pass
    finally:
        driver.implicitly_wait(3)
        driver.close()


if __name__ == '__main__':
    main()


# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()