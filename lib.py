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


    if(NoHist):
        print("Não existe ainda um banco de dados.")
        conn = sqlite3.connect("./data/historico_bovespa.db")
        print('Download de dados do Yahoo Finance:')
        new_data = yf.download(acoes)
        print('Download de dados concluído com sucesso.')
    else:
        f.close()
        # Download de todoas as ações da lista, a partir do ponto que já existe no HD
        conn = sqlite3.connect("./data/historico_bovespa.db")
        hist = pd.read_sql_query("SELECT * FROM HIST", conn)

        # Reconstrói o dataset com Date como index, e colunas multi-index com tuplas
        hist.set_index('Date', drop=True, inplace=True)
        hist.index = pd.to_datetime(hist.index)
        hist.columns = list(map(literal_eval, hist.columns))
        hist.columns = pd.MultiIndex.from_tuples(hist.columns)
        print("Últimos registros no banco de dados")
        print(hist.tail())
        ultima = hist.index[-1]

        inicio = pd.to_datetime(1, unit='D', origin=ultima)
        inicio = str(inicio).rstrip('00:00:00').rstrip()
        print('Download de dados do Yahoo Finance:')
        new_data = yf.download(acoes, start=inicio)
        print('Download de dados concluído com sucesso.')

    # Reordenando os níveis de índice nas colunas
    new_data.columns = new_data.columns.reorder_levels([1, 0])

    # Ordenando as colunas em ordem alfabética
    new_data.sort_index(axis=1, inplace=True)

    print("Novos dados")
    print(new_data.head())

#    hist = pd.concat([hist, new_data])

    new_data.to_sql('hist', conn, if_exists="append")
    print("Dados atualizados com sucesso. Últimos registros no banco de dados")
    print(pd.read_sql_query("SELECT * FROM hist ORDER BY Date DESC LIMIT 10", conn))
    conn.close()

'''
Melhorias a serem feitas:
    - testar o comportamento da função caso o banco de dados exista, mas esteja vazio.
    - atualizar o banco com novos ativos que nunca foram baixados
    - caso a última linha esteja toda vazia(não sejam os dados finais do dia), não acrescentar ao banco de dados
        Uma ideia é baixar dados até o dia anterior a hoje.
'''