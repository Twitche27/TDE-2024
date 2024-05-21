from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.expected_conditions import WebDriver, element_to_be_clickable, presence_of_element_located
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from tkinter import messagebox
import re

class Driver():
    __driver: WebDriver
    def __init__(self) -> None:
        c = Options()
        s = Service()
        c.add_argument("start-maximized")
        c.add_argument("--remote-debugging-port=7777")
        self.__driver = webdriver.Chrome(service=s, options=c)

    
    
    def acess_ibge_noticias(self, ano: str) -> dict[str, int]:
        try:
            self.__driver.get("https://agenciadenoticias.ibge.gov.br/busca-avancada.html")
            self.__driver.find_element(By.CLASS_NAME, "input__texto").send_keys("rendimento domiciliar per capita")
            self.__driver.find_element(By.ID, "exata_contem").click()
            self.__driver.find_element(By.XPATH, "//input[@type='submit']").click()
            WebDriverWait(self.__driver, 5).until(element_to_be_clickable((By.ID, "cookie-btn"))).click()
            return self.__select_noticia(ano)
        except TimeoutException:
            messagebox.showerror("Error", "Erro: A página demorou muito para carregar.")
        except NoSuchWindowException:
            messagebox.showerror("Error", "Erro: A página não existe ou o navegador foi fechado.")
        
    def __select_noticia(self, ano: str) -> dict[str, int]:
        noticias = self.__driver.find_elements(By.XPATH, "//h3")
        expression = "IBGE divulga o rendimento domiciliar per capita ((para)|(de))? " + f"{ano}"
        for noticia in noticias:
            if ((re.search(expression, noticia.text[:-11])) or ((noticia.text[:-11] == "IBGE divulga rendimento domiciliar per capita segundo a PNAD Contínua para o FPE") and (noticia.text[-4:] == ano))):
                noticia.click()
                break
        UFs = self.__driver.find_elements(By.XPATH, "//td")
        return {x.text: int(y.text.replace('.', '').replace(',', '')) for x, y in zip(UFs[0::2], UFs[1::2])}
