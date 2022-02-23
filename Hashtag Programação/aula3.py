from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys

navegador = webdriver.Chrome("chromedriver.exe")

###############################DOLAR#####################################
navegador.get("https://www.google.com")

navegador.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotacao dolar")
navegador.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_dolar = navegador.find_element_by_xpath(
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
################################################
navegador.get("https://www.google.com")
navegador.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotacao euro")
navegador.find_element_by_xpath(
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_euro = navegador.find_element_by_xpath(
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
#################################################################
navegador.get("https://www.melhorcambio.com/ouro-hoje")
cotacao_ouro = navegador.find_element_by_xpath('//*[@id="comercial"]').get_attribute("value")
cotacao_ouro = cotacao_ouro.replace(",", ".")
####################################################################
tabela = pd.read_excel("Produtos.xlsx")
tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)


tabela["Preço Base Original"] = tabela["Preço Base Original"] * tabela["Cotação"]
tabela["Preço Base Reais"] = tabela["Preço Base Original"] * tabela["Margem"]

tabela["Preço Base Reais"] = tabela["Preço Base Reais"].map("R$ {:.2f}".format)

#####################

tabela.to_excel("Produtos Novo.xlsx", index=False)
navegador.quit()
