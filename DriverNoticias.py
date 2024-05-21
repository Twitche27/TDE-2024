from DriverClass import Driver
from selenium.common.exceptions import NoSuchWindowException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from tkinter import messagebox
import re

def access_ibge_noticias(self, ano: str) -> dict[str, float]:
        try:
            self.driver.get("https://agenciadenoticias.ibge.gov.br/busca-avancada.html") 
            self.driver.find_element(By.CLASS_NAME, "input__texto").send_keys("rendimento domiciliar per capita")
            self.driver.find_element(By.ID, "exata_contem").click()
            self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
            return self.__select_noticia(ano)
        except NoSuchWindowException:
            messagebox.showerror("Error", "Erro: A página não existe ou o navegador foi fechado.")
        
def __select_noticia(self, ano: str) -> dict[str, float]:
    noticias = self.driver.find_elements(By.XPATH, "//h3")
    expression = "IBGE divulga o rendimento domiciliar per capita ((para)|(de))?" + ano
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

Driver.access_ibge_noticias = access_ibge_noticias
Driver.__select_noticia = __select_noticia