from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.expected_conditions import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from subprocess import CREATE_NO_WINDOW

class Driver():
    __driver: WebDriver
    def __init__(self) -> None:
        c = Options()
        s = Service()
        c.add_argument("start-maximized")
        c.add_argument("--remote-debugging-port=7777")
        s.creation_flags = CREATE_NO_WINDOW
        self.__driver = webdriver.Chrome(service=s, options=c)

    def acess_tabnet(self, uf: str):
        self.__driver.get("https://datasus.saude.gov.br/nascidos-vivos-desde-1994/")
        self.__driver.find_element(By.NAME, "radiobutton").click()
        select = Select(self.__driver.find_element(By.ID, 'mySelect'))
        select.select_by_visible_text(uf)
        
    def select_options(self, ano: str) -> str:
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