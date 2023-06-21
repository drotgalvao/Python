import pandas as pd
import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

ativos = ["^BVSP", "BRL=X"]

hoje = datetime.datetime.now()
um_ano_atras = hoje - datetime.timedelta(days=365)

dados_mercado = yf.download(ativos, um_ano_atras, hoje)

dados_fechamento = dados_mercado["Adj Close"]
dados_fechamento.columns = ["DOLAR", "IBOV"]
dados_fechamento = dados_fechamento.dropna()

dados_fechamento_mensal = dados_fechamento.resample("M").last()
dados_fechamento_anual = dados_fechamento.resample("Y").last()

print(dados_fechamento_anual)
print(dados_fechamento_mensal)
print(dados_fechamento)

retorno_no_ano = dados_fechamento_anual.pct_change().dropna()
retorno_no_mes = dados_fechamento_mensal.pct_change().dropna()
retorno_no_dia = dados_fechamento.pct_change().dropna()

#print(retorno_no_ano)
#print(retorno_no_mes)
print(retorno_no_dia)

retorno_dia_dolar = round(retorno_no_dia.iloc[-1, 0] * 100, 2)
retorno_dia_ibov = round(retorno_no_dia.iloc[-1, 1] * 100, 2)

retorno_mes_dolar = round(retorno_no_mes.iloc[-1, 0] * 100, 2)
retorno_mes_ibov = round(retorno_no_mes.iloc[-1, 1] * 100, 2)

retorno_ano_dolar = round(retorno_no_ano.iloc[-1, 0] * 100, 2)
retorno_ano_ibov = round(retorno_no_ano.iloc[-1, 1] * 100, 2)

print(retorno_dia_dolar)
print(retorno_dia_ibov)
print(retorno_mes_dolar)
print(retorno_mes_ibov)
print(retorno_ano_dolar)
print(retorno_ano_ibov)

plt.style.use("cyberpunk")

dados_fechamento.plot(y = 'IBOV',use_index=True, legend = False)

plt.title("IBOVESPA")

plt.savefig("ibov.png", dpi=300, bbox_inches="tight")

plt.show()

dados_fechamento.plot(y = 'DOLAR',use_index=True, legend = False)

plt.title("DOLAR")

plt.savefig("dolar.png", dpi=300, bbox_inches="tight")

plt.show()

load_dotenv()

senha = os.environ.get("senha_email")
email = "diegohenriquegalvao@gmail.com"

msg = EmailMessage()
msg['Subject'] = 'Relatório de Mercado'
msg['From'] = email
msg['To'] = email

msg.set_content(f"""Prezado diretor, segue o relatorio diario:
Bolsa:
No ano o Ibovespa esta tendo uma rentabilidade de {retorno_ano_ibov}%,
enquanto no mes a rentabilidade foi de {retorno_mes_ibov}%,
 e no dia de {retorno_dia_ibov}%.

Dolar:
No ano o Dolar esta tendo uma rentabilidade de {retorno_ano_dolar}%,
enquanto no mes a rentabilidade foi de {retorno_mes_dolar}%,
 e no dia de {retorno_dia_dolar}%.
 
 Abs,
 Diego Henrique Galvao""")

with open("ibov.png", "rb") as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype="image", subtype="png", filename="ibov.png")

with open("dolar.png", "rb") as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype="image", subtype="png", filename="dolar.png")

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email, senha)
    smtp.send_message(msg)
