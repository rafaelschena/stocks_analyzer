# Todas as classes e funções são criadas neste módulo, que deve ser importado no sistema principal
from typing import Any, Union

import pandas as pd
import yfinance as yf
import sqlite3
from ast import literal_eval

from pandas import DataFrame, Series
from pandas.io.parsers import TextFileReader


def imprime_boas_vindas():
    print('#################################################################')
    print('############### Bem-vindo ao Stocks Analyzer ####################')
    print('#################################################################')
    print('')

def the_end():
    print('#################################################################')
    print('################ Stocks Analyzer Encerrado ######################')
    print('#################################################################')
    print('')

def atualiza_base_dados():
    '''
    Faz o download da lista de ações a serem importadas do Índice Brasil Amplo (ações com maior liquidez)
    Disponível em http://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-brasil-amplo-ibra.htm

    :return:
    '''
    ibra = pd.read_csv("./data/IBrA.csv", delimiter=';')

    # Alterando nome das colunas para evitar erros por acentuação
    ibra.columns = ['Codigo', 'Empresa', 'Tipo', 'Qtd_Teorica', 'Part']

    # Extraindo os códigos das ações da lista e acrescentando .SA a todos os símbolos para poder fazer o download
    acoes = ibra.Codigo
    acoes = [i + '.SA' for i in acoes]

    NoHist = False
#    f = None
    try:
        f = open("./data/historico_bovespa.db")
    except FileNotFoundError:
        NoHist = True

    # Definindo o dia de hoje como o término do período de download
    today = pd.datetime.today()
    ontem = pd.to_datetime(-1, unit='D', origin=today)
    today = str(today)[0:10]
    ontem = str(ontem)[0:10]

    if(NoHist):
        print("Não existe ainda um banco de dados.")
        conn = sqlite3.connect("./data/historico_bovespa.db")
        print('Download de dados do Yahoo Finance:')
        new_data = yf.download(acoes, end=today) # Início será no primeiro dia disponível na API
        print('Download de dados concluído com sucesso.')
    else:
        f.close()
        # Download de todoas as ações da lista, a partir do ponto que já existe no HD

#        conn = sqlite3.connect("./data/historico_bovespa.db")
#        hist = pd.read_sql_query("SELECT * FROM HIST", conn)

        # Reconstrói o dataset com Date como index, e colunas multi-index com tuplas
#        hist.set_index('Date', drop=True, inplace=True)
#        hist.index = pd.to_datetime(hist.index)
#        hist.columns = list(map(literal_eval, hist.columns))
#        hist.columns = pd.MultiIndex.from_tuples(hist.columns)
        hist = carrega_base_dados()
        print("Últimos registros no banco de dados")
        print(hist.tail())
        ultima = hist.index[-1]

        inicio = pd.to_datetime(1, unit='D', origin=ultima)
        inicio = str(inicio)[0:10]
        print(f'Banco de dados atualizado até {str(ultima)[0:10]}. Baixando dados até {ontem}.')
        print('Download de dados do Yahoo Finance:')
        new_data = yf.download(acoes, start=inicio, end=today)
        print('Download de dados concluído com sucesso.')

    # Reordenando os níveis de índice nas colunas
    new_data.columns = new_data.columns.reorder_levels([1, 0])

    # Ordenando as colunas em ordem alfabética
    new_data.sort_index(axis=1, inplace=True)

    print("Novos dados")
    print(new_data.head())


    conn = sqlite3.connect("./data/historico_bovespa.db")
    new_data.to_sql('hist', conn, if_exists="append")
    print("Dados atualizados com sucesso. Últimos registros no banco de dados")
    print(pd.read_sql_query("SELECT * FROM hist ORDER BY Date DESC LIMIT 10", conn))
    conn.close()

def carrega_base_dados():
    conn = sqlite3.connect("./data/historico_bovespa.db")
    hist = pd.read_sql_query("SELECT * FROM HIST", conn)
    conn.close()
    # Reconstrói o dataset com Date como index, e colunas multi-index com tuplas
    hist.set_index('Date', drop=True, inplace=True)
    hist.index = pd.to_datetime(hist.index)
    hist.columns = list(map(literal_eval, hist.columns))
    hist.columns = pd.MultiIndex.from_tuples(hist.columns)
    return hist

def desenha_grafico(ticker):
    from bokeh.plotting import figure, output_file, show
    from math import pi

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title=f"Gráfico {ticker} Diário")
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.3
    hist = carrega_base_dados()
    df = hist[ticker].iloc[-250:]
    inc = df.Close > df.Open
    dec = df.Open > df.Close
    w = 12 * 60 * 60 * 1000  # half day in ms
    p.segment(df.index, df.High, df.index, df.Low, color="black")
    p.vbar(df.index[inc], w, df.Open[inc], df.Close[inc], fill_color="#00FF00", line_color="black")
    p.vbar(df.index[dec], w, df.Open[dec], df.Close[dec], fill_color="#FF0000", line_color="black")

    output_file(f'{ticker}.html', title=f'{ticker} Diário')

    show(p)  # open a browser