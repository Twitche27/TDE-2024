from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from xpath import xpath_lista
import time

class Populacao(object):
    driver = None
    def __init__(self, link):
        self.driver = webdriver.Chrome()
        self.driver.get(link)

    def selecionar_variaveis(self, xpath):
        WebDriverWait(self.driver, 20).until(EC.invisibility_of_element((By.CLASS_NAME, "loading-logo carregado")))
        for x in xpath:
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'{x}'))))

    def selecionar_formato(self, xpath):
        teste_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'{xpath}')))
        teste = Select(teste_element)
        teste.select_by_visible_text('CSV (BR)')

    def fazer_download(self, xpath):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'{xpath}'))).click()


if __name__ == '__main__':
    extrair = Populacao('https://sidra.ibge.gov.br/tabela/6579')
    extrair.selecionar_variaveis(xpath_lista)
    extrair.selecionar_formato('//*[@id="container-posteriori"]/div/div[1]/table/tbody/tr[2]/td[2]/select')
    extrair.fazer_download('//*[@id="opcao-downloads"]/strong')
    time.sleep(5)
