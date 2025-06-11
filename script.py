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
pyautogui.write (password)
time.sleep(1)
pyautogui.press("enter")
time.sleep(10)
