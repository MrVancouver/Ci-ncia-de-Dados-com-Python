import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

dados = yf.download('AAPL', start='2023-01-01', end='2023-12-31')
#dados.columns = (['Abertura','Maxima', 'Minima', 'Fechamento', 'Fechamento AJ.', 'Volume'])
#dados = dados.rename_axis('Competencia')
mpf.plot(dados.head(90), type='candle', figsize = (24,12), volume = False, mav=(7,14,21), style = 'yahoo', title='Variação dos Valores da AAPL', xlabel = 'Data', ylabel = 'Preço')
print(mpf.plot)