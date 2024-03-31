import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet

# ----------------Download de dados----------------
dados = yf.download('JNJ', start='2020-01-01', end = '2023-12-31', progress = False)
dados = dados.reset_index()
# ----------------Separação de dados para o prophet----------------
dados_treino = dados[dados['Date'] < '2023-07-31']
dados_teste = dados[dados['Date'] >= '2023-07-31']

dados_prophet_treino = dados_treino[['Date', 'Close']].rename(columns = {'Date': 'ds', 'Close': 'y'})#o prophet EXIGE que os dados de treino estajam na coluna ds e o de teste estejam na coluna y

# ----------------Criar e treinar modelo----------------
modelo = Prophet(weekly_seasonality = True,
                 yearly_seasonality = True,
                 daily_seasonality = False)
modelo.add_country_holidays(country_name='US')
modelo.fit(dados_prophet_treino)
# ----------------Criar datas futuras para a previsão----------------
futuro = modelo.make_future_dataframe(periods = 150)
previsao = modelo.predict(futuro)
# ----------------Criar datas futuras para a previsão----------------
plt.figure(figsize = (14,8))
plt.plot(dados_treino['Date'], dados_treino['Close'], label='Dados de treino', color = 'blue')
plt.plot(dados_teste['Date'], dados_teste['Close'], label='Dados Reais(teste)', color = 'green')
plt.plot(previsao['ds'], previsao['yhat'], label='Previsão', color = 'orange', linestyle = '--')

plt.axvline(dados_treino['Date'].max(), color='red', linestyle = '--', label = 'Inicio da Previsão')
plt.xlabel('Data')
plt.ylabel('Preço do Fechamento')
plt.title('Previsão de Preço de Fechamento vs Dados reais')
plt.legend()

plt.show()
print(previsao)