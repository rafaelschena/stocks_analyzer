
# Sistema principal
from lib import *


imprime_boas_vindas()

while True:
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('Menu Principal:')
    print('1 - Gerenciar base de dados')
    print('2 - Gráficos')
    print('99 - Sair do sistema')
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    opcao = input('Digite a opção desejada: ')
    while(not valida_entrada(opcao, [1, 2, 99])):
        print('Opção inválida')
        opcao = input('Digite a opção desejada: ')
    opcao = int(opcao)

    if opcao == 1:
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print('Gerenciar base de dados:')
        print('Digite uma opção:')
        print('1 - Atualizar banco de dados')
        print('2 - Incluir ativos no banco de dados')
        print('99 - Voltar')

        opcao = input('Digite a opção desejada: ')
        while (not valida_entrada(opcao, [1, 2, 99])):
            print('Opção inválida')
            opcao = input('Digite a opção desejada: ')
        opcao = int(opcao)

        if opcao == 1:
            atualiza_base_dados()
        elif opcao == 2:
            inclui_ativo(input('Digite o ativo:').upper())
        elif opcao == 99:
            continue

    elif opcao == 2:
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print('Gráficos:')
        print('Digite uma opção:')
        print('1 - Gráfico diário')
        print('2 - Gráfico semanal')
        print('3 - Gráfico mensal')
        print('99 - Voltar')

        opcao = input('Digite a opção desejada: ')
        while (not valida_entrada(opcao, [1, 2, 3, 99])):
            print('Opção inválida')
            opcao = input('Digite a opção desejada: ')
        opcao = int(opcao)

        if opcao == 1:
            desenha_grafico(input('Digite o ativo:').upper(), period='D')
        elif opcao == 2:
            desenha_grafico(input('Digite o ativo:').upper(), period='W')
        elif opcao == 3:
            desenha_grafico(input('Digite o ativo:').upper(), period='M')
        elif opcao == 99:
            continue

    elif opcao == 99:
        break

the_end()

'''
Melhorias a serem feitas:
    - escrever função para reconstruir lista original de ativos
    - implantar validação de ativos digitados
    - escrever funções para executar querys SQL no banco de dados
    - corrigir: verificar se os dados a serem gravados são mais atuais que os existentes na base de dados
    - implementar query para eliminar valores duplicados no banco de dados.
    - verificar consistência dos ativos do banco de dados com os da lista csv inicial, e caso falte algum, atualizar
    - plotar linhas horizontais de suporte e resistência principais
'''