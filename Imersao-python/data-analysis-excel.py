import pandas as pd
import plotly.express as px
df_principal = pd.read_excel(
    'C:\Alura\Imersao-python\dados-consolidadas.xlsx', sheet_name='Principal')
df_total_acoes = pd.read_excel(
    'C:\Alura\Imersao-python\dados-consolidadas.xlsx', sheet_name='Total_de_acoes')
df_gpt = pd.read_excel(
    'C:\Alura\Imersao-python\dados-consolidadas.xlsx', sheet_name='chat_gpt')
df_ticker = pd.read_excel(
    'C:\Alura\Imersao-python\dados-consolidadas.xlsx', sheet_name='Ticker')
pd.options.display.float_format = '{:.2f}'.format

# ----------------Tabela Princial----------------
# aqui podemos printar apenas as 10 primeiras colunas
'''print(df_principal.head(10))'''
# selecionando quais colunas quero que o dataframe contenha
df_principal = df_principal[['Ativo', 'Data',
                             'Último (R$)', 'Var. Dia (%)']].copy()
# renomeando colunas
df_principal = df_principal.rename(
    columns={'Último (R$)': 'Valor Final', 'Var. Dia (%)': 'Var-dia-pct'})
# fazendo os cálculos feitos no excel e aqui criamos uma coluna
df_principal['Var-pct'] = df_principal['Var-dia-pct'] / 100
df_principal['Valor-inc'] = df_principal['Valor Final'] / \
    (1 + df_principal['Var-pct'])

# aqui acontece um tipo de procv, onde comparamos os dois dataframes e informamos quais colunas são comparáveis e qual a principal.
df_principal = df_principal.merge(
    df_total_acoes, left_on='Ativo', right_on='Código', how='left')
df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(
    int)  # convertendo para int
df_principal = df_principal.rename(
    columns={'Qtde. Teórica': 'qtd-teorica'}).copy()  # renomear coluna
df_principal = df_principal.drop(columns='Código').copy()  # dropar coluna

df_principal['Variacao-rs'] = (df_principal['Valor Final'] -
                               df_principal['Valor-inc']) * df_principal['qtd-teorica']
# apply é usado para aplicar funções personalizadas
# lambda é usado para criar uma função anonima, apply e lambda são comumente usados
df_principal['Resultado'] = df_principal['Variacao-rs'].apply(
    lambda x: 'Subiu' if x > 0 else ('Desceu' if x < 0 else 'Estável'))
df_principal = df_principal.merge(
    df_ticker, left_on='Ativo', right_on='Ticker', how='left')
df_principal = df_principal.merge(
    df_gpt, left_on='Nome', right_on='Nome', how='left')
df_principal = df_principal.rename(columns={'Nome': 'nome-empresa'}).copy()
df_principal = df_principal.drop(columns='Ticker').copy()
df_principal['Cat-idade'] = df_principal['idade'].apply(
    lambda x: 'Maior que 100' if x > 100 else ('Menor que 50' if x < 50 else 'Entre 50 e 100 anos'))

# ----------------Tabela Análise----------------

maior = df_principal['Variacao-rs'].max()  # Maior valor
menor = df_principal['Variacao-rs'].min()  # Menor valor
media = df_principal['Variacao-rs'].mean()  # média valor
media_subiu = df_principal[df_principal['Resultado']
                           == 'Subiu']['Variacao-rs'].mean()
media_desceu = df_principal[df_principal['Resultado']
                            == 'Desceu']['Variacao-rs'].mean()
df_subiu = df_principal[df_principal['Resultado'] == 'Subiu']
df_analise_segmento = df_subiu.groupby(
    'Segmento')['Variacao-rs'].sum().reset_index()
df_analise_saldo = df_principal.groupby(
    'Resultado')['Variacao-rs'].sum().reset_index()

# ----------------Gráficos----------------
fig = px.bar(df_analise_saldo, x='Resultado', y='Variacao-rs', text='Variacao-rs',
             # o text mostra os valores dentro das barras
             title='Variação Reais por Resultado')

# ----------------Print----------------
print('Tabela: \n', df_principal, '\n')
print(' Table de quem subiu: \n', df_subiu, '\n')
print(' Análise por Segmento:\n ', df_analise_segmento, '\n')
print(' Análise por Resultado:\n', df_analise_saldo, '\n')
print(' Maior Valor: ', maior, '\n')
print(' Menor Valor: ', menor, '\n')
print(' Média dos Valores: ', media, '\n')
print(' Média de Quem Subiu:', media_subiu, '\n')
print(' Média de Quem Desceu:', media_desceu, '\n')
fig.show()
