from DriverClass import Driver

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

def acess_tabnet(self, uf: str, ano: str) -> str:
        try:
            self.__driver.get("https://datasus.saude.gov.br/nascidos-vivos-desde-1994/")
            self.__driver.find_element(By.NAME, "radiobutton").click()
            select = Select(self.__driver.find_element(By.ID, 'mySelect'))
            select.select_by_visible_text(uf)
            return self.__select_options(ano)
        except TimeoutException:    
            messagebox.showerror("Error", "Erro: A página demorou muito para carregar.")
        except NoSuchWindowException:
            messagebox.showerror("Error", "Erro: A página não existe ou o navegador foi fechado.")

Driver.acess_tabnet = acess_tabnet