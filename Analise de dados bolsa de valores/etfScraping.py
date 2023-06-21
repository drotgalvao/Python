from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import pdb

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.etf.com/etfanalytics/etf-finder')

time.sleep(15)

botao_100 = driver.find_element("xpath", '/html/body/div[2]/div/div/main/div[1]/section/div[2]/div[3]/div/article/div/div[2]/div/div/div/div/div/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div/div[5]/button/span')

driver.execute_script("arguments[0].click();", botao_100) # Resolve o problema de clique com o Selenium
#botao_100.click()

numero_paginas = driver.find_element("xpath", '/html/body/div[2]/div/div/main/div[1]/section/div[2]/div[3]/div/article/div/div[2]/div/div/div/div/div/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/ul/li[8]/a')

numero_paginas = int(numero_paginas.text)

lista_tabela_por_pagina = []

elemento = driver.find_element("xpath", '/html/body/div[2]/div/div/main/div[1]/section/div[2]/div[3]/div/article/div/div[2]/div/div/div/div/div/div[3]/div[2]/div/div[1]/div/div[1]/table')

# html_tabela = elemento.get_attribute('outerHTML')

# tabela = pd.read_html(html_tabela)[0]

# print(tabela)
print(numero_paginas)

for pagina in range(1, numero_paginas+1):

    html_tabela = elemento.get_attribute('outerHTML')

    tabela = pd.read_html(str(html_tabela))[0]

    lista_tabela_por_pagina.append(tabela)


    botao_avancar_pagina = driver.find_element("xpath", '//a[contains(@class, "page-link") and text()="Next"]')


    
    driver.execute_script("arguments[0].click();", botao_avancar_pagina)
    #botao_avancar_pagina.click()

tabela_cadastro_etfs = pd.concat(lista_tabela_por_pagina) #Lista com todos os ETFS parte 1

print(tabela_cadastro_etfs) 

#Salva em excel
#tabela_cadastro_etfs.to_excel('nome_arquivo.xlsx', index=False) #Salva em excel

voltar_pagina_um = driver.find_element("xpath", '//*[@id="panel:r0:0"]/div/div[2]/div[2]/ul/li[2]/a')

driver.execute_script("arguments[0].click();", voltar_pagina_um)

botao_mudar_pra_performance = driver.find_element("xpath", '/html/body/div[2]/div/div/main/div[1]/section/div[2]/div[3]/div/article/div/div[2]/div/div/div/div/div/div[3]/div[2]/div/ul/li[2]')

driver.execute_script("arguments[0].click();", botao_mudar_pra_performance)

botao_100 = driver.find_element("xpath", '/html/body/div[2]/div/div/main/div[1]/section/div[2]/div[3]/div/article/div/div[2]/div/div/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[5]/button/span')

driver.execute_script("arguments[0].click();", botao_100) # Resolve o problema de clique com o Selenium

# Tudo igual a partir daqui

lista_tabela_por_pagina = []

elemento = driver.find_element("xpath", '/html/body/div[2]/div/div/main/div[1]/section/div[2]/div[3]/div/article/div/div[2]/div/div/div/div/div/div[3]/div[2]/div/div[2]/div/div[1]/table')

for pagina in range(1, numero_paginas+1):

    html_tabela = elemento.get_attribute('outerHTML')

    tabela = pd.read_html(str(html_tabela))[0]

    lista_tabela_por_pagina.append(tabela)


    botao_avancar_pagina = driver.find_element("xpath", '//a[contains(@class, "page-link") and text()="Next"]')


    
    driver.execute_script("arguments[0].click();", botao_avancar_pagina)
    #botao_avancar_pagina.click()

tabela_rentabilidade_etfs = pd.concat(lista_tabela_por_pagina) #Lista com todos os ETFS rentabilidade parte 2

print(tabela_rentabilidade_etfs)

tabela_cadastro_etfs = tabela_cadastro_etfs.set_index("Ticker")

tabela_rentabilidade_etfs = tabela_rentabilidade_etfs.set_index("Ticker")
tabela_rentabilidade_etfs = tabela_rentabilidade_etfs[['1 YR', '3 YR', '5 YR', '10 YR']]

base_de_dados_final = tabela_cadastro_etfs.join(tabela_rentabilidade_etfs, how='inner')

base_de_dados_final.to_excel('nome_arquivo.xlsx', index=False)

pdb.set_trace()

# while True:
#     time.sleep(1)  # Espera 1 segundo
#     # Coloque aqui o código que deseja executar repetidamente

