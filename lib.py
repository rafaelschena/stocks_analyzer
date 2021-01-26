# Todas as classes e funções são criadas neste módulo, que deve ser importado no sistema principal
from typing import Any, Union

import pandas as pd
import yfinance as yf
import sqlite3
from ast import literal_eval
import warnings
warnings.filterwarnings(action="ignore")
from pandas import DataFrame, Series
from pandas.io.parsers import TextFileReader

# Variáveis globais utilizadas em várias funções
today = pd.datetime.today()
ontem = pd.to_datetime(-1, unit='D', origin=today)
ontem = str(ontem)[0:10]+' 23:59:59'
ontem = pd.to_datetime(ontem)


def imprime_boas_vindas():
    print('#################################################################')
    print('############### Bem-vindo ao Stocks Analyzer ####################')
    print('#################################################################')
    print('')

def the_end():
    print('################ Stocks Analyzer Encerrado ######################')


def valida_entrada(entrada, opcoes):
    try:
        input = int(entrada)
    except:
        return False
    if(input not in opcoes):
        return False
    else:
        return True



def download_dados(inicio=None, intervalo='1d'):
    '''
    Faz o download de dados do Yahoo Finance e formata o índice da coluna com o nome do ativo no primeiro nível e os
    dados de Open/High/Low/Close/Adj. Close/Volume em segundo nível.
    :param inicio:
    :param intervalo:
    :return:
    '''
    period_tabela = {
        '1d': 'diária',
        '1wk': 'semanal',
        #'1mo': 'mensal'
    }
    acoes = pd.read_csv('./data/acoes.csv', names=['Codigo'])
    acoes = list(acoes.Codigo)
    print(f'Baixando dados até {ontem} com periodicidade {period_tabela[intervalo]}.')
    print('Download de dados do Yahoo Finance:')
    df = yf.download(acoes, start=inicio, end=ontem, interval=intervalo).drop_duplicates()

    # Reordenando os níveis de índice nas colunas
    df.columns = df.columns.reorder_levels([1, 0])
    # Ordenando as colunas em ordem alfabética
    df.sort_index(axis=1, inplace=True)
    return df

def atualiza_base_dados():
    '''
    Faz o download da lista de ações a serem importadas
    Pressupõe que haja um arquivo acoes.csv com o exato código do Yahoo Finance
    :return:
    '''
    # Extraindo os códigos das ações da lista
    # Pressupõe que haja um arquivo acoes.csv com o exato código do Yahoo Finance
    acoes = pd.read_csv('./data/acoes.csv', names=['Codigo'])
    acoes = list(acoes.Codigo)

    # Definindo o dia de hoje como o término do período de download
    db_valido = verifica_banco_dados()

    if db_valido:
        period_tabela = {
            '1d': 'diaria',
            '1wk': 'semanal',
            #'1mo': 'mensal'
        }
        for key in period_tabela:
            hist = carrega_base_dados(tabela=period_tabela[key])
            print(f"Últimos registros no banco de dados com periodicidade {key}")
            print(hist.tail())
            ultima = hist.index[-1]
            inicio = pd.to_datetime(1, unit='D', origin=ultima)
            inicio = str(inicio)[0:10]
            print(f'Banco de dados atualizado até {str(ultima)[0:10]}.')

            if (pd.to_datetime(inicio) < ontem):
                new_data = download_dados(inicio=inicio, intervalo=key)
                print(f"Novos dados a serem gravados na tabela {period_tabela[key]}:")
                print(new_data.tail())
                grava_banco_dados(new_data, tabela=period_tabela[key])
    #            print("Últimos registros no banco de dados:")
    #            print(pd.read_sql_query("SELECT * FROM diaria ORDER BY Date DESC LIMIT 10", conn))

            else:
                print('Banco de dados já está atualizado.')

    else:
        cria_banco_dados("replace")

def cria_banco_dados(se_existente="append"):
    # Criação do banco de dados com o dia de hoje como o término do período de download

    period_tabela = {
        '1d': 'diaria',
        '1wk': 'semanal',
        #'1mo': 'mensal'
    }
    for key in period_tabela:
        new_data = download_dados(intervalo=key)
        grava_banco_dados(new_data, tabela=period_tabela[key], se_existente=se_existente)


def verifica_banco_dados():
    try:
        f = open("./data/historico_bovespa.db")
        f.close()
        conn = sqlite3.connect("./data/historico_bovespa.db")
        try:
            hist = pd.read_sql_query("SELECT * FROM diaria ORDER BY Date DESC LIMIT 1", conn)
            week = pd.read_sql_query("SELECT * FROM semanal ORDER BY Date DESC LIMIT 1", conn)
            #month = pd.read_sql_query("SELECT * FROM mensal ORDER BY Date DESC LIMIT 1", conn)
            if type(hist) == pd.core.frame.DataFrame and type(week) == pd.core.frame.DataFrame:
                return True
            else:
                print("Banco de dados corrompido.")
                return False
        except pd.io.sql.DatabaseError:
            print("Banco de dados corrompido.")
            return False

    except FileNotFoundError:
        print("Não existe ainda um banco de dados.")
        return False


def grava_banco_dados(df, tabela='diaria', se_existente="append"):
    conn = sqlite3.connect("./data/historico_bovespa.db")
    df.to_sql(name=tabela, con=conn, if_exists=se_existente)
    print('Gravação dos dados concluída com sucesso.')
    conn.close()

def carrega_base_dados(tabela='diaria'):
    conn = sqlite3.connect("./data/historico_bovespa.db")
    try:
        hist = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
    except pd.io.sql.DatabaseError:
        print("Banco de dados corrompido. Iniciando download da base de dados.")
        return None
    conn.close()
    # Reconstrói o dataset com Date como index, e colunas multi-index com tuplas
    hist.set_index('Date', drop=True, inplace=True)
    hist.index = pd.to_datetime(hist.index)
    hist.columns = list(map(literal_eval, hist.columns))
    hist.columns = pd.MultiIndex.from_tuples(hist.columns)
    return hist


def inclui_ativo(ticker):
    '''
    Inclui o ativo no banco de dados
    :param ticker: ticker de ativo a ser incluído na base de dados
    :return:
    '''
    acoes = pd.read_csv('./data/acoes.csv', names=['Codigo']).Codigo

    if(ticker in acoes.values):
        print('Este ativo já faz parte da base de dados.')
    else:
        # Atualizando a base de dados existente
        atualiza_base_dados()
        period_tabela = {
            '1d': 'diaria',
            '1wk': 'semanal',
            #'1mo': 'mensal'
        }

        for key in period_tabela:
            hist = carrega_base_dados(tabela=period_tabela[key])
            hist = hist.loc[~hist.index.duplicated(keep='first')] # Linha adicionada
            print(f'Download de dados de {ticker} até {ontem} do Yahoo Finance com periodicidade {period_tabela[key]}:')
            new_data = yf.download(ticker, end=ontem).drop_duplicates()
            new_data = new_data.loc[~new_data.index.duplicated(keep='first')] # Linha adicionada

            # Adicionando o nome do ativo em formato de tupla no nome das colunas
            new_data.columns = [f'("{ticker}", "' + i + '")' for i in new_data.columns]
            new_data.columns = list(map(literal_eval, new_data.columns))
            new_data.columns = pd.MultiIndex.from_tuples(new_data.columns)

            hist = pd.concat([hist, new_data], axis=1)
            print('Gravando dados no banco de dados.')
            conn = sqlite3.connect("./data/historico_bovespa.db")
            hist.to_sql(period_tabela[key], conn, if_exists="replace")
            conn.commit()
            conn.close()
            print('Dados gravados com sucesso.')

        # Atualizando o arquivo csv com as ações a serem atualizadas
        acoes = acoes.append(pd.Series(ticker), ignore_index=True)
        acoes.to_csv('./data/acoes.csv', index=False, header=False)
        print('Lista de ativos atualizada.')

def desenha_grafico(ticker):
    from bokeh.plotting import figure, output_file, show, ColumnDataSource
    from bokeh.models import HoverTool
    from math import pi

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title=f"Gráfico de {ticker} Diário")
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.3
    hist = carrega_base_dados(tabela='diaria')
    df = hist[ticker].iloc[-250:]
#    df = hist[ticker]
    # Create a ColumnDataSource from df: source
    source = ColumnDataSource(df)

    inc = df[df.Close > df.Open]
    dec = df[df.Open > df.Close]
    w = 12 * 60 * 60 * 1000  # half day in ms
    p.segment(x0="Date", y0="High", x1="Date", y1="Low", color="black", source=source)
    p.vbar(x="Date", width=w, top="Close", bottom="Open", fill_color="#00FF00", line_color="black", source=inc)
    p.vbar(x="Date", width=w, top="Open", bottom="Close", fill_color="#FF0000", line_color="black", source=dec)

    # min250 = petr3.Low.min()
    # suporte = np.full((250,), min250)
    # max250 = petr3.High.max()
    # resist = pd.Series(np.full((250,), max250), index=petr3.index)
    # p.line(resist.index, resist, line_color='green', line_width=2)
    # p.line(suporte.index, suporte, line_color='red', line_width=2)

    output_file(f'{ticker}.html', title=f'{ticker} Diário')

    p.add_tools(HoverTool(
        tooltips=[("Data", "@Date{%F}"), ("Abertura", "@Open"), ("Fechamento", "@Close"), ("Máxima", "@High"),
                  ("Mínima", "@Low")],
        formatters={'@Date': 'datetime'}))

    show(p)  # open a browser