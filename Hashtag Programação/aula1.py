import pyautogui
import pyperclip
import time
import pandas as pd

pyautogui.PAUSE = 1

######################### ACESSANDO BANCO DE DADOS ###########################
pyautogui.click(x=766, y=1068)

pyautogui.hotkey("ctrl", "t")
pyperclip.copy("https://drive.google.com/drive/folders/149xknr9JvrlEnhNWO49zPcw0PW5icxga")
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")

time.sleep(5)

######################### ACESSANDO E BAIXANDO O ARQUIVO ######################

pyautogui.click(x=457, y=297, clicks = 2)
time.sleep(2)
pyautogui.rightClick(x=415, y=386)
pyautogui.click(x=550, y=829)

########################## ANALISE DE DADOS ####################################

tabela = pd.read.excel(r"C://Users/Pichau/Downloads/Vendas - Dez.xlsx")
faturamento = tabela["Valor Final"].sum()
quantidade= tabela["Quantidade"].sum()