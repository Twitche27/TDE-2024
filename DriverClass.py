from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import WebDriver, presence_of_element_located
from selenium.common.exceptions import NoSuchWindowException, ElementClickInterceptedException, WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from tkinter import messagebox, Tk
import re
from typing import Optional

class Driver:
    __driver: WebDriver
    def __init__(self) -> None:
        c = Options()
        c.add_argument("start-maximized")
        c.add_argument("--remote-debugging-port=7777")
        try:
            self.__driver = webdriver.Chrome(options=c)
        except (WebDriverException):
            Tk().withdraw()  
            messagebox.showerror("Error", "Erro: Há outro navegador com o mesmo port aberto.")
            Tk().destroy()
    
    @property
    def driver(self):
        return self.__driver

class DriverTabnet(Driver):
    def __init__(self) -> None:
        super().__init__()

    def __select_options(self, ano: str) -> str:
        WebDriverWait(self.__driver, 5).until(presence_of_element_located((By.ID, "F")))
        select = Select(self.__driver.find_element(By.ID, 'C'))
        select.select_by_visible_text("Idade da mãe")
        select = Select(self.__driver.find_element(By.ID, 'A'))
        select.deselect_by_visible_text("2022")
        select.select_by_visible_text(ano)
        self.__driver.find_element(By.ID, "fig8").click()
        select = Select(self.__driver.find_element(By.ID, 'S8'))
        select.deselect_by_visible_text("Todas as categorias")
        select.select_by_visible_text("Menor de 10 anos")
        select.select_by_visible_text("10 a 14 anos")
        select.select_by_visible_text("15 a 19 anos")
        self.__driver.find_element(By.ID, "Z").click()
        self.__driver.find_element(By.XPATH, "//input[@value='prn']").click()
        self.__driver.find_element(By.XPATH, "//input[@class='mostra']").click()
        self.__driver.switch_to.window(self.__driver.window_handles[1])
        return self.__driver.find_element(By.XPATH, "//pre").text

def access_tabnet(self, uf: str, ano: str) -> str:
        try:
            self.__driver.get("https://datasus.saude.gov.br/nascidos-vivos-desde-1994/")
            self.__driver.find_element(By.NAME, "radiobutton").click()
            select = Select(self.__driver.find_element(By.ID, 'mySelect'))
            select.select_by_visible_text(uf)
            return self.__select_options(ano)
        except TimeoutException:  
            Tk().withdraw()  
            messagebox.showerror("Error", "Erro: A página demorou muito para carregar.")
            Tk().destroy()
        except NoSuchWindowException:
            Tk().withdraw()  
            messagebox.showerror("Error", "Erro: A página não existe ou o navegador foi fechado.")
            Tk().destroy()
    
class DriverNoticias(Driver):
    def __init__(self) -> None:
        super().__init__()
    
    def __select_noticia(self, ano: str) -> dict[str, float]:
        noticias = self.driver.find_elements(By.XPATH, "//h3")
        expression = "( )?IBGE divulga (o )?rendimento domiciliar per capita (((para)|(de)) )?" + ano
        for noticia in noticias:   
            if ((re.search(expression, noticia.text[:-11])) or ((noticia.text[:-11] == "IBGE divulga rendimento domiciliar per capita segundo a PNAD Contínua para o FPE") and (noticia.text[-4:] == str(int(ano)+1)))):
                try:
                    noticia.click()
                    break
                except ElementClickInterceptedException:
                    self.driver.find_element(By.ID, "cookie-btn").click()
                    noticia.click()
                    break
        UFs = self.driver.find_elements(By.XPATH, "//td")
        return {x.text: float(y.text.replace('.', '').replace(',', '.').replace("R$", "").replace(" ", "")) for x, y in zip(UFs[0::2], UFs[1::2])}

    def access_ibge_noticias(self, ano: str) -> dict[str, float]|None:
        try:
            self.driver.get("https://agenciadenoticias.ibge.gov.br/busca-avancada.html") 
            self.driver.find_element(By.CLASS_NAME, "input__texto").send_keys("rendimento domiciliar per capita")
            self.driver.find_element(By.ID, "exata_contem").click()
            self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
            return self.__select_noticia(ano)
        except NoSuchWindowException:
            Tk().withdraw()  
            messagebox.showerror("Error", "Erro: A página não existe ou o navegador foi fechado.")
            Tk().destroy()
            return None