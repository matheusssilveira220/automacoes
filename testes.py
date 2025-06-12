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
time.sleep(2)
user = navegador.find_element(By.XPATH, "//input[@placeholder='Email']")
time.sleep(2)
user.click()