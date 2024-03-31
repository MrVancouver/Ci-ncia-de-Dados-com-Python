import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# ----------------Importação dos dados financeiros de uma empresa na bolsa via yahoo finance----------------
# função que faz "download" da ação que eu escolhi, e o período e retorna como dataframe para o pandas
dados = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-31')
# dessa maneira conseguimos mudar o nome das colunas
dados.columns = ['Abertura', 'Maximo', 'Minimo',
                 'Fechamento', 'Fechamento AJ.', 'Volume']
# A data é um índice para a biblioteca pandas que serve como rótulo para cada linha do dataframe
dados = dados.rename_axis('Data')

# ----------------Gráfico de Fechamento----------------
dados['Fechamento'].plot(figsize=(10, 6))  # largura de 10 e altura de 6
plt.title('Variação do Preço por data', fontsize=16)
plt.legend(['Fechamento'])

# ----------------Organização das tabelas----------------
df = dados.head(60).copy()  # aqui pegamos as primeiras 60 linhas
df['Data'] = df.index  # Convertemos o índice para uma coluna
# transformando as colunas de datas em números e criando mais uma coluna
df['Data'] = df['Data'].apply(mdates.date2num)

# ----------------Criando um Gráfico do 0----------------
fig, ax = plt.subplots(figsize=(15, 8))  # Cria um quadro branco medindo 15x8
width = 0.7  # Largura do Candle
# Determinando a cor do Candle, if fechamento maior que abertura fica verde, else fica vermelho
for i in range(len(df)):
    if df['Fechamento'].iloc[i] > df['Abertura'].iloc[i]:
        color = 'green'
    else:
        color = 'red'
    ax.plot([df['Data'].iloc[i], df['Data'].iloc[i]], [df['Minimo'].iloc[i],
            df['Maximo'].iloc[i]], color=color, linewidth=1)
    ax.add_patch(plt.Rectangle((df['Data'].iloc[i] - width/2, min(df['Abertura'].iloc[i], df['Fechamento'].iloc[i])),
                               width,
                               abs(df['Fechamento'].iloc[i] - df['Abertura'].iloc[i]), facecolor=color))

# Aqui estamos fazendo as médias móveis de cada dia
# a funçao rolling chama um parâmetro para fazer um cálculo estatístico, no caso window onde ele vai fazer o cálculo de 7 em 7 linhas e o mean() virá para fazer a média
df['MA7'] = df['Fechamento'].rolling(window=7).mean()
df['MA14'] = df['Fechamento'].rolling(window=14).mean()

# desenhando a linha de dados das médias móveis
ax.plot(df['Data'], df['MA7'], color='orange', label='Média móvel 7 dias')
ax.plot(df['Data'], df['MA14'], color='blue', label='Média móvel de 14 dias')
ax.legend()  # aqui chamamos a legenda de cada média móvel

ax.xaxis_date()  # aqui informamos ao matplotlib que as datas estão no eixo x do gráfico
# aqui damos um formato para as datas no gráfico
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)  # aqui informamos a rotação dos dados no eixo x

# titulo acima do gráfico
plt.title("Gráfico de Candlestick - PETR4.SA com matplotlib")
plt.xlabel("Data")  # título do eixo x
plt.ylabel("Preço")  # título do eixo y
plt.grid(True)  # grade no gráfico para facilitar a visão dos valores

# ----------------Criando Gráfico de Candlesticks e Subplots usanddo o PLotly----------------

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=('Candlestick', 'Volume Transacionado'),
                    row_width=[0.2, 0.7])

fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Abertura'],
                             high=df['Maximo'],
                             low=df['Minimo'],
                             close=df['Fechamento'],
                             name='Candlestick'),
              row=1, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA7'],
                         mode='lines',
                         name='MA7 - Média Móvel 7 Dias'),
              row=1, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA14'],
                         mode='lines',
                         name='MA7 - Média Móvel 14 Dias'),
              row=1, col=1)

# ----------------API Mágica----------------
dados_fin = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-31')
mpf.plot(dados_fin.head(30), type='candle', figsize=(
    16, 8), volume=True, mav=(7, 14), style='yahoo')

# print(df)
# plt.show()# essa função plota o gráfico feito
fig.show()  # mostrando o gráfico do matplotlib
