from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.expected_conditions import WebDriver, element_to_be_clickable, presence_of_element_located
from selenium.common.exceptions import TimeoutException
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

    def acess_tabnet(self, uf: str, ano: str):
        #fazer fail safe do navegador estar aberto
        self.__driver.get("https://datasus.saude.gov.br/nascidos-vivos-desde-1994/")
        self.__driver.find_element(By.NAME, "radiobutton").click()
        select = Select(self.__driver.find_element(By.ID, 'mySelect'))
        select.select_by_visible_text(uf)
        self.__select_options(ano)
    
    def acess_ibge_noticias(self, ano: str) -> dict[str, int]:
        self.__driver.get("https://agenciadenoticias.ibge.gov.br/busca-avancada.html")
        self.__driver.find_element(By.CLASS_NAME, "input__texto").send_keys("rendimento domiciliar per capita")
        self.__driver.find_element(By.ID, "exata_contem").click()
        self.__driver.find_element(By.XPATH, "//input[@type='submit']").click()
        WebDriverWait(self.__driver, 5).until(element_to_be_clickable((By.ID, "cookie-btn"))).click()
        return self.__select_noticia(ano)
        
    def __select_noticia(self, ano: str) -> dict[str, int]:
        noticias = self.__driver.find_elements(By.XPATH, "//h3")
        expression = "IBGE divulga o rendimento domiciliar per capita ((para)|(de))? " + f"{ano}"
        for noticia in noticias:
            if ((re.search(expression, noticia.text[:-11])) or ((noticia.text[:-11] == "IBGE divulga rendimento domiciliar per capita segundo a PNAD Contínua para o FPE") and (noticia.text[-4:] == ano))):
                noticia.click()
                break
        UFs = self.__driver.find_elements(By.XPATH, "//td")
        return {x.text: int(y.text.replace('.', '')) for x, y in zip(UFs[0::2], UFs[1::2])}
        
    def __select_options(self, ano: str) -> str:
        try:
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
        except TimeoutException:    
            messagebox.showerror("Error", "Erro: A página demorou muito para carregar.")

def main():
    driver = Driver()
    driver.acess_ibge_noticias('2021')

main()