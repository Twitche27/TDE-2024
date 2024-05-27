from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import WebDriver
from selenium.common.exceptions import NoSuchWindowException, ElementClickInterceptedException, WebDriverException
from selenium.webdriver.common.by import By
from tkinter import messagebox, Tk
import re

class Driver:
    __driver: WebDriver
    def __init__(self) -> None:
        c = Options()
        c.add_argument("start-maximized")
        c.add_argument("--remote-debugging-port=7777")
        try:
            self.__driver = webdriver.Chrome(options=c)
        except (WebDriverException):
            window = Tk()
            window.withdraw()  
            messagebox.showerror("Error", "Erro: Há outro navegador com o mesmo port aberto.")
            window.destroy()
            
    def __select_noticia(self, ano: str) -> dict[str, float]:
        noticias = self.driver.find_elements(By.XPATH, "//h3")
        expression = "( )?IBGE divulga (o )?rendimento domiciliar per capita (((para)|(de)) )?" + ano
        for noticia in noticias:   
            if ((re.search(expression, noticia.text[:-11])) or ((noticia.text[:-11] == "IBGE divulga rendimento domiciliar per capita segundo a PNAD Contínua para o FPE") and (noticia.text[-4:] == str(int(ano)+1)))):
                try:
                    noticia.click()
                    break
                except ElementClickInterceptedException:
                    self.__driver.find_element(By.ID, "cookie-btn").click()
                    noticia.click()
                    break
        UFs = self.driver.find_elements(By.XPATH, "//td")
        return {x.text: float(y.text.replace('.', '').replace(',', '.').replace('R$', '').replace(' ', '')) for x, y in zip(UFs[0::2], UFs[1::2])}

    def access_ibge_noticias(self, ano: str) -> dict[str, float]:
        try:
            self.__driver.get("https://agenciadenoticias.ibge.gov.br/busca-avancada.html") 
            self.__driver.find_element(By.CLASS_NAME, "input__texto").send_keys("rendimento domiciliar per capita")
            self.__driver.find_element(By.ID, "exata_contem").click()
            self.__driver.find_element(By.XPATH, "//input[@type='submit']").click()
            return self.__select_noticia(ano)
        except NoSuchWindowException:
            window = Tk()
            window.withdraw()  
            messagebox.showerror("Error", "Erro: A página não existe ou o navegador foi fechado.")
            window.destroy()
            return
    
    @property
    def driver(self):
        return self.__driver