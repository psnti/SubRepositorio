from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select,WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

driver_path = 'test/chromedriver/chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
try:
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)
except:
    driver_path = 'chromedriver/chromedriverv83.exe'
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_path)

wait = WebDriverWait(driver, 60) # define el tiempo maximo de espera

driver.get("https://jellyfish-forecast.herokuapp.com/")

assert "Jellyfish" in driver.title

mensaje = ''

# voy a pagina inicial del mapa
boton_mapa = driver.find_element_by_name('Mapas')
boton_mapa.click()


## prueba 1 : mensaje error
print('Caso 1: Mensaje de error si no se introduce fecha')
mensaje += '\nCaso 1: Mensaje de error si no se introduce fecha'
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/div/div/div/form/select/option[5]')))
driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div/div/div/form/select/option[5]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="fecha"]').click()
driver.find_element_by_xpath('//*[@id="boton_envia"]').click()
try:
    wait.until(EC.element_to_be_clickable((By.NAME, 'alerta')))
    print('\tCorrecto')
    mensaje += '\n\tCorrecto'
except Exception as identifier:
    print('\tFallo')
    mensaje += '\n\tFallo'


# voy a pagina inicial del mapa
boton_mapa = driver.find_element_by_name('Mapas')
boton_mapa.click()


## prueba 2: muestra graficos
print('Caso 2: Aparecen los graficos correctamente')
mensaje += '\nCaso 2: Aparecen los graficos correctamente'
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div/div/div/div/form/select/option[5]')))
driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div/div/div/form/select/option[5]').click()
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fecha"]')))
driver.find_element_by_xpath('//*[@id="fecha"]').send_keys('01-01')
driver.find_element_by_xpath('//*[@id="fecha"]').click()
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="boton_envia"]')))
driver.find_element_by_xpath('//*[@id="boton_envia"]').click()
try:
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[1]/div[2]/div/div/div/h5[2]')))
    print('\tCorrecto')
    mensaje += '\n\tCorrecto'
except Exception as identifier:
    print('\tFallo')
    mensaje += '\n\tFallo'


## prueba 3: exportar archivo
print('Caso 3: Descarga de archivo generado')
mensaje += '\nCaso 3: Descarga de archivo generado'
try:
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="boton_exportar"]/a')))
    driver.find_element_by_xpath('//*[@id="boton_exportar"]/a').click()
    print('\tCorrecto')
    mensaje += '\n\tCorrecto'
except Exception as identifier:
    print('\tFallo')
    mensaje += '\n\tFallo'

driver.close()

log = open('test/test.log','w')
log.write(mensaje)
log.close()