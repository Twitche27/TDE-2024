from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class Populacao(object):
    driver = None # Inicializa o driver como None
    def __init__(self, link):
        self.driver = webdriver.Chrome() # Inicializa o WebDriver do Chrome
        self.driver.get(link) # Abre o link especificado

    def selecionar_variaveis(self, lista_xpath):
        # Aguarda até que o logo de carregamento desapareça
        WebDriverWait(self.driver, 20).until(EC.invisibility_of_element((By.CLASS_NAME, "loading-logo carregado")))
        for x in lista_xpath: # Itera sobre a lista de xpaths
            # Clica em cada elemento especificado pelo xpath na lista
            self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'{x}'))))

    def selecionar_formato(self, xpath):
        # Aguarda até que o elemento de seleção de formato esteja clicável
        teste_element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'{xpath}')))
        teste = Select(teste_element) # Inicializa um objeto Select
        teste.select_by_visible_text('CSV (BR)') # Seleciona 'CSV (BR)' no dropdown

    def fazer_download(self, xpath):
        # Clica no botão de download especificado pelo xpath
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'{xpath}'))).click()

# Lista de xpaths a serem clicados
xpath_lista = ['//*[@id="panel-P-collapse"]/div[3]/div/div[2]/div/div/div/div/div[2]/div/div/div/button', 
              '//*[@id="panel-P-collapse"]/div[3]/div/div[2]/div/div/div/div/div[3]/div/div/div/button',
              '//*[@id="panel-P-collapse"]/div[3]/div/div[2]/div/div/div/div/div[4]/div/div/div/button',
              '//*[@id="panel-P-collapse"]/div[3]/div/div[2]/div/div/div/div/div[5]/div/div/div/button',
              '//*[@id="panel-P-collapse"]/div[3]/div/div[2]/div/div/div/div/div[6]/div/div/div/button',
              '//*[@id="panel-P-collapse"]/div[3]/div/div[2]/div/div/div/div/div[7]/div/div/div/button',
              '//*[@id="panel-P-collapse"]/div[3]/div/div[2]/div/div/div/div/div[8]/div/div/div/button',
              '//*[@id="arvore-245e-1"]/div/div/div/button', '//*[@id="arvore-325e-1"]/div/div/div/button',
              '//*[@id="botao-downloads"]']

if __name__ == '__main__':
    # Inicializa o objeto Populacao com a URL fornecida
    extrair = Populacao('https://sidra.ibge.gov.br/tabela/6579')
    # Seleciona as variáveis usando os xpaths fornecidos
    extrair.selecionar_variaveis(xpath_lista)
    # Seleciona o formato como 'CSV (BR)' usando o xpath fornecido
    extrair.selecionar_formato('//*[@id="container-posteriori"]/div/div[1]/table/tbody/tr[2]/td[2]/select')
    # Executa a ação de download clicando no botão de download
    extrair.fazer_download('//*[@id="opcao-downloads"]/strong')
    # Espera 2 segundos para garantir que o download comece (para visualização)
    time.sleep(2)
