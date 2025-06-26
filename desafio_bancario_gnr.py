# Sistema para Controle Bancário Desafio Bootcamp Santander
# Versão 01
# Giuliano Nascimento Ribeiro
# Data de Entrega: 26/06/2025

opcao_gnr =   """
    ============= Opções Caixa Eletrônico =============

    1 - Depositar
    2 - Sacar
    3 - Extrato
    4 - Sair

    ===================================================

                Bem vindo ao Banco GNR!!!!

    => """

saldo_gnr = 0 
limite_gnr = 500
extrato_gnr = ""
controle_saques_gnr = 0
limite_saques_gnr = 3



while True:

    escolha_gnr = (input(opcao_gnr))

    if escolha_gnr == '1':
        valor_gnr = float(input("Informe o valor para Depósito: "))

        if valor_gnr > 0:
            saldo_gnr += valor_gnr
            extrato_gnr += f"Depósito: R$ {valor_gnr: 2f}\n"
            print(f"Depósito executado com sucesso! R$ {valor_gnr:.2f}")

        else:
            print(f"Falha na operação, o valor informado não é valido: R$ {valor_gnr:.2f}" )

    elif escolha_gnr == '2':
        
        valida_numero_saques_gnr = controle_saques_gnr >= limite_saques_gnr
        
        if valida_numero_saques_gnr:
            print(f"Falha na operação, limite de saques diários realizado, total de {limite_saques_gnr} saques.")
        
        else:
            valor_gnr = float(input("Informe o valor para Saque: "))
            valida_saldo_gnr = valor_gnr > saldo_gnr
            valida_limite_gnr = valor_gnr > limite_gnr
        
            if valida_saldo_gnr:
                print(f"Falha na operação, o saldo é insuficiente, saldo atual é R$ {saldo_gnr:.2f}")
        
            elif valida_limite_gnr:
                print(f"Falha na operação, valor solicitado acima limite autorizado: {limite_gnr:.2f}")

            elif valor_gnr > 0:
                saldo_gnr -= valor_gnr
                extrato_gnr += f"Saque: R$ {valor_gnr: 2f}\n"
                controle_saques_gnr += 1
                print(f"Saque executado com sucess! R$ {valor_gnr:.2f}, você pode realizar mais {limite_saques_gnr-controle_saques_gnr} saques.")
            else:
                print(f"Falha na operação, o valor informado não é valido: R$ {valor_gnr:.2f}")
    
    elif escolha_gnr == '3':
        print("\n=========Extrato Bancário Banco GNR=========")
        print("Não houve movimentações bancárias." if not extrato_gnr else extrato_gnr)
        print(f"\nSaldo Atual: R$ {saldo_gnr:.2f}")
        print("==============================================")

    elif escolha_gnr == '4':
        print("Obrigado por utilizar o sistema do Banco GNR")
        break

    else:
        print("Falha na operação, é necessário escolher uma opção válida")
