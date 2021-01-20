
# Sistema principal
from lib import *


imprime_boas_vindas()

while True:
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('Digite uma opção:')
    print('1 - Atualizar base de dados')
    print('2 - Incluir ativo na base de dados')
    print('3 - Exibir gráfico')
    print('99 - Sair do sistema')
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    opcao = int(input('Digite a opção desejada: '))
    if opcao == 1:
        atualiza_base_dados()
    elif opcao == 2:
        inclui_ativo(input('Digite o ativo:').upper())
    elif opcao == 3:
        desenha_grafico(input('Digite o ativo:').upper())
    elif opcao == 99:
        break

the_end()

'''
Melhorias a serem feitas:
    - escrever função para reconstruir lista original de ativos
    - escrever funções para executar querys SQL no banco de dados
    - verificar se um ativo já está na lista de downloads antes de incluir novamente
    - verificar consistência dos ativos do banco de dados com os da lista csv inicial, e caso falte algum, atualizar
    - corrigir escalas da função desenha_grafico
    - plotar gráfico em periodicidades semanais e mensais
    - plotar linhas horizontais de suporte e resistência principais
'''