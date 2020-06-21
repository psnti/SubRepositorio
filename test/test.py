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
    # driver_path = 'chromedriver/chromedriverv83.exe'

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
    wait = WebDriverWait(driver, 5) # define el tiempo maximo de espera

    driver = reinicia(driver,wait)

    time.sleep(2)

    return driver,wait

def reinicia(driver,wait):
    """"
    Vuelve a la pagina de los mapas 
    """
    driver.get("https://jellyfish-forecast.herokuapp.com/")
    assert "Jellyfish" in driver.title
    boton_mapa = driver.find_element_by_name('Mapas')
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
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div/div/div/form/select/option[5]').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div/div/div/form/div[2]/button').click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.NAME, 'alerta')))

def comprueba_graficos(driver,wait):
    # wait.until(EC.element_to_be_clickable((By.ID, 'datepicker')))
    time.sleep(1)
    driver.find_element_by_id('datepicker').send_keys('06/12/2020')
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div/div/div/form/select/option[5]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div/div/div/form/div[2]/button').click()
    try:
        driver.find_element_by_id('data-container')
    except Exception as identifier:
        raise Exception('Graficos no mostrados')

def main():
    driver,wait = inicializar() # se abre la pagina de mapas
    try:
        try:
            print('Prueba 1: Se selecciona playa sin una fecha')
            comprueba_error_fecha_no_introducida(driver,wait)
            print("OK, slata mensaje de error")
        except Exception as e:
            print("MAL: no salta mensaje de error")
        try:
            reinicia(driver,wait)
            print('Prueba 1: Se selecciona playa sin una fecha')
            comprueba_graficos(driver,wait)
            print("OK, aparecen los gráficos")
        except Exception as e:
            print("MAL: no aparecen los gráficos")
    except Exception as identifier:
        print(type(identifier))
        print(identifier)
    finally:
        time.sleep(10)
        driver.close()
    
    


if __name__ == '__main__':
    main()


# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()