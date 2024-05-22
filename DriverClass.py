from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import WebDriver
from tkinter import messagebox
from selenium.common.exceptions import WebDriverException

class Driver:
    __driver: WebDriver
    def __init__(self) -> None:
        c = Options()
        c.add_argument("start-maximized")
        c.add_argument("--remote-debugging-port=7777")
        try:
            self.__driver = webdriver.Chrome(options=c)
        except (WebDriverException):
            messagebox.showerror("Error", "Erro: Há outro navegador com o mesmo port aberto.")
    
    @property
    def driver(self):
        return self.__driver
    
