
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

    - verificar consistência dos ativos do banco de dados com os da lista csv inicial, e caso falte algum, atualizar
    - atualizar o banco com novos ativos que nunca foram baixados
    - testar o comportamento da função caso o banco de dados exista, mas esteja vazio.
    - corrigir escalas da função desenha_grafico
    - plotar linhas horizontais de suporte e resistência principais
'''