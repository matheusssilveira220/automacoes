from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import time
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("PASSWORD")
#abrir navegador
navegador = webdriver.Chrome()

#login
navegador.get("https://backoffice.omni.chat/#/retailer")
navegador.maximize_window()
time.sleep(1)
pyautogui.moveTo (x=150, y=430)
time.sleep(1)
pyautogui.click()
time.sleep(1)   
pyautogui.write("matheus.silveira@omni.chat")
time.sleep(1)
pyautogui.moveTo (x=150, y=500)
time.sleep(1)
pyautogui.click()  
time.sleep(1)
pyautogui.write(password)
time.sleep(1)
pyautogui.press("enter")
time.sleep(5)

#pesquisar cliente
pesquisa = navegador.find_element(By.XPATH, '//*[@id="search-box"]')
time.sleep(1)
pesquisa.click()
time.sleep(1)
pesquisa.send_keys("ESKALA")
time.sleep(1)
pyautogui.press("enter")
time.sleep(2)

#acessar cliente
selecionar_cliente = pesquisa.find_element(By.XPATH, '/html/body/app-root/app-menu/mat-sidenav-container/mat-sidenav-content/app-retailers/div/table/tbody/tr/td[1]')
time.sleep(1)
selecionar_cliente.click()
time.sleep(1)

#acessar tela de pagamentos
pyautogui.moveTo (x=643, y=320)
time.sleep(2)
pyautogui.click()  
time.sleep(5)