import yfinance as yf
import pandas as pd
import quantstats as qs
import datetime as dt

data_hoje =dt.datetime.today()

current_month = dt.datetime.now().month
current_year = dt.datetime.now().year
last_day = dt.datetime(current_year, current_month+1, 1) - dt.timedelta(days=1)

#print(last_day)

tickers_df = pd.read_excel('C:\\Users\\diego\\OneDrive\\Área de Trabalho\\Projeto python\\tickers.xlsx', sheet_name='Sheet1', header=None)

#Teste para primeira ação
#primeira_acao = comp_historica.iloc[0,0]
#print(primeira_acao)

# Extract tickers as a list
tickers = tickers_df[0].tolist()

#print(tickers)

dados_cotacoes = yf.download(tickers, start='2015-01-01', end=data_hoje)['Adj Close']

#print(dados_cotacoes)

dados_cotacoes.index = pd.to_datetime(dados_cotacoes.index)

dados_cotacoes = dados_cotacoes.sort_index()

#print(dados_cotacoes)

r7 = dados_cotacoes.resample("M").last().pct_change().rolling(7).mean().dropna(axis = 0, how = 'all')

#print(r7)

r7 = r7.rank(axis = 1, ascending = False).T.sort_values(last_day)

r7.to_excel('C:\\Users\\diego\\OneDrive\\Área de Trabalho\\Projeto python\\r7.xlsx')

print(r7)