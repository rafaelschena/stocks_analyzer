
# Sistema principal
from lib import *
import warnings

warnings.filterwarnings(action="ignore")

imprime_boas_vindas()

while True:
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('Digite uma opção:')
    print('1 - Atualizar base de dados')
    print('2 - Exibir gráfico')
    print('99 - Sair do sistema')
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    opcao = int(input('Digite a opção desejada: '))
    if opcao == 1:
        atualiza_base_dados()
    elif opcao == 2:
        desenha_grafico(input('Digite o ativo:').upper())
    elif opcao == 99:
        break

the_end()

'''
Melhorias a serem feitas:
    - testar o comportamento da função caso o banco de dados exista, mas esteja vazio.
    - atualizar o banco com novos ativos que nunca foram baixados
    - caso a última linha esteja toda vazia(não sejam os dados finais do dia), não acrescentar ao banco de dados
        Uma ideia é baixar dados até o dia anterior a hoje.
    - corrigir escalas da função desenha_grafico
    - encontrar funções
    - plotar linhas horizontais de suporte e resistência principais
'''