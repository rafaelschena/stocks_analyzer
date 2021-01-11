
# Sistema principal
from lib import *

imprime_boas_vindas()

while True:
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print('Digite uma opção:')
    print('1 - Atualizar base de dados')
    print('2 - Exibir dados')
    print('99 - Sair do sistema')
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    opcao = int(input('Digite a opção desejada: '))
    if opcao == 1:
        download_base_dados()
    elif opcao == 2:
        break
    elif opcao == 99:
        break

the_end()