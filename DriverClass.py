# Importação de bibliotecas necessárias
from selenium import webdriver  # Para controle do navegador
from selenium.webdriver.chrome.options import Options  # Para definir opções do navegador Chrome
from selenium.webdriver.support.expected_conditions import WebDriver  # Para condições esperadas (mas parece não estar sendo usado corretamente)
from selenium.common.exceptions import NoSuchWindowException, ElementClickInterceptedException, WebDriverException  # Exceções específicas do Selenium
from selenium.webdriver.common.by import By  # Para localizar elementos na página
from tkinter import messagebox, Tk  # Para exibir mensagens de erro
import re  # Para usar expressões regulares

# Definição da classe Driver
class Driver:
    __driver: WebDriver  # Declaração de um atributo privado __driver do tipo WebDriver

    # Método inicializador da classe
    def __init__(self) -> None:
        c = Options()  # Criação de um objeto Options para definir configurações do navegador
        c.add_argument("start-maximized")  # Argumento para iniciar o navegador maximizado
        c.add_argument("--remote-debugging-port=7777")  # Argumento para definir a porta de depuração remota

        # Tentativa de inicializar o WebDriver do Chrome
        try:
            self.__driver = webdriver.Chrome(options=c)  # Inicialização do driver com as opções configuradas
        except WebDriverException:  # Captura de exceção caso o driver não seja inicializado
            window = Tk()  # Criação de uma janela Tkinter
            window.withdraw()  # Ocultação da janela principal
            # Exibição de uma mensagem de erro
            messagebox.showerror("Error", "Erro: Há outro navegador com o mesmo port aberto.")
            window.destroy()  # Destruição da janela

    # Método privado para selecionar notícia
    def __select_noticia(self, ano: str) -> dict[str, float]:
        noticias = self.driver.find_elements(By.XPATH, "//h3")  # Encontrar todos os elementos <h3> na página
        # Expressão regular para encontrar a notícia específica
        expression = "( )?IBGE divulga (o )?rendimento domiciliar per capita (((para)|(de)) )?" + ano
        for noticia in noticias:  # Iterar sobre todas as notícias
            if ((re.search(expression, noticia.text[:-11])) or ((noticia.text[:-11] == "IBGE divulga rendimento domiciliar per capita segundo a PNAD Contínua para o FPE") and (noticia.text[-4:] == str(int(ano)+1)))):
                try:
                    noticia.click()  # Tentativa de clicar na notícia
                    break
                except ElementClickInterceptedException:  # Captura de exceção caso o clique seja interceptado
                    self.__driver.find_element(By.ID, "cookie-btn").click()  # Clicar no botão de cookies
                    noticia.click()  # Tentar clicar na notícia novamente
                    break
        UFs = self.driver.find_elements(By.XPATH, "//td")  # Encontrar todos os elementos <td> na página
        # Criação de um dicionário com os valores encontrados
        return {x.text: float(y.text.replace('.', '').replace(',', '.').replace('R$', '').replace(' ', '')) for x, y in zip(UFs[0::2], UFs[1::2])}

    # Método público para acessar notícias do IBGE
    def access_ibge_noticias(self, ano: str) -> dict[str, float]:
        try:
            self.__driver.get("https://agenciadenoticias.ibge.gov.br/busca-avancada.html")  # Acessar a URL
            self.__driver.find_element(By.CLASS_NAME, "input__texto").send_keys("rendimento domiciliar per capita")  # Inserir texto na barra de busca
            self.__driver.find_element(By.ID, "exata_contem").click()  # Clicar no botão de busca exata
            self.__driver.find_element(By.XPATH, "//input[@type='submit']").click()  # Clicar no botão de submissão
            return self.__select_noticia(ano)  # Chamar método privado para selecionar a notícia
        except NoSuchWindowException:  # Captura de exceção caso a janela não exista ou o navegador tenha sido fechado
            window = Tk()  # Criação de uma janela Tkinter
            window.withdraw()  # Ocultação da janela principal
            # Exibição de uma mensagem de erro
            messagebox.showerror("Error", "Erro: A página não existe ou o navegador foi fechado.")
            window.destroy()  # Destruição da janela
            return

    @property
    # Propriedade para acessar o driver
    def driver(self):
        return self.__driver
