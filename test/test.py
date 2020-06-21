from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import os


def inicializar():
    """
    Inicializa la pagina

    Devuelve el objeto webdriver
    """
    driver_path = 'test/chromedriver/chromedriverv83.exe'
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)

    driver = reinicia(driver)
    return driver

def reinicia(driver):
    """"
    Vuelve a la pagina de los mapas 
    """
    driver.get("https://jellyfish-forecast.herokuapp.com/")
    assert "Jellyfish" in driver.title
    return driver

#### TEST ####
def comprueba_error_fecha_no_introducida(driver):
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

def main():
    driver = inicializar() # se abre la pagina
    try:
        comprueba_error_fecha_no_introducida(driver)
    except expression as identifier:
        pass


if __name__ == '__main__':
    main()


# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()