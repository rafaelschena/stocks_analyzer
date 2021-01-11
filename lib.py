# Todas as classes e funções são criadas neste módulo, que deve ser importado no sistema principal
from typing import Any, Union

import pandas as pd
import yfinance as yf
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

def download_base_dados():
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

    # Download de todoas as ações da lista, a partir do ponto que já existe no HD

    try:
        historico = pd.read_csv('./data/base_bovespa.csv')
        # Reconstruir o dataset com multi-index, indexado por data
    except FileNotFoundError:
        data = yf.download(acoes)

    # Reordenando os níveis de índice nas colunas
    data.columns = data.columns.reorder_levels([1, 0])

    # Ordenando as colunas em ordem alfabética
    data.sort_index(axis=1, inplace=True)

    # Salvando em um arquivo .csv
    data.to_csv('./data/base_bovespa.csv')