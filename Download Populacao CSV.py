from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "/path/to/download/directory",
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
})
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://sidra.ibge.gov.br/tabela/6579")
time.sleep(5)

anos = driver.find_elements(By.CLASS_NAME, "sidra-toggle") # acha todos os botões de "ano"
for i in range(2,9):
  anos[i].click() # clica nos botões de 2020 a 2014 (2021 já está selecionado)

try: # tira a opção de UT = Brasil
  brasil_botao = driver.find_element(By.XPATH, '//*[@id="arvore-245e-1"]/div/div/div/button')
  brasil_botao.click()
except NoSuchElementException:
  print("erro")

try: # seleciona a opção UT = UF
  uf_botao = driver.find_element(By.XPATH, '//*[@id="arvore-325e-1"]/div/div/div/button')
  uf_botao.click()
except NoSuchElementException:
  print("erro")

try: # seleciona o botão de download
  download_botao = driver.find_element(By.XPATH, '//*[@id="botao-downloads"]')
  download_botao.click()
except NoSuchElementException:
  print("erro")

time.sleep(5)

try: # seleciona o botão de formato do arquivo
  formato_botao = driver.find_element(By.XPATH, '//*[@id="container-posteriori"]/div/div[1]/table/tbody/tr[2]/td[2]/select')
  formato_botao.click()
except NoSuchElementException:
  print("erro")

try: # seleciona a opção de csv (BR)
  csv_opcao = driver.find_element(By.XPATH, '//*[@id="container-posteriori"]/div/div[1]/table/tbody/tr[2]/td[2]/select/option[4]')
  csv_opcao.click()
except NoSuchElementException:
  print("erro")

try: # seleciona o botão de download
  download2_botao = driver.find_element(By.XPATH, '//*[@id="opcao-downloads"]/strong')
  download2_botao.click()
except NoSuchElementException:
  print("erro")

time.sleep(5)