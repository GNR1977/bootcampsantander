import textwrap
from datetime import datetime

# Variáveis globais para armazenar os dados dos usuários e contas
# Em uma aplicação maior, estas seriam persistidas em um banco de dados, por exemplo.
USUARIOS = []
CONTAS = []
AGENCIA = "0001" # Agência fixa para todas as contas

# --- Funções de Menu ---
def menu():
    menu_str = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_str))

# --- Funções de Usuário ---
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    # Verifica se já existe um usuário com o CPF informado
    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Adiciona o novo usuário como um dicionário à lista de usuários
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    """Retorna o dicionário do usuário se o CPF for encontrado, caso contrário, None."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# --- Funções de Conta ---
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário para a nova conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return None

    # Define os valores iniciais para uma nova conta
    saldo_inicial = 0.0
    limite_saque_por_transacao = 500.0
    saques_realizados_hoje = 0
    limite_saques_diarios = 3
    historico_transacoes = [] # Lista para armazenar o histórico de transações

    # Cria a conta como um dicionário e a adiciona à lista de contas
    conta = {
        "numero": numero_conta,
        "agencia": agencia,
        "cpf_titular": cpf, # Ligação da conta ao CPF do titular
        "saldo": saldo_inicial,
        "limite": limite_saque_por_transacao,
        "numero_saques_hoje": saques_realizados_hoje,
        "limite_saques_diarios": limite_saques_diarios,
        "historico": historico_transacoes
    }
    contas.append(conta)
    print("=== Conta criada com sucesso! ===")
    return conta

def listar_contas(contas, usuarios):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    for conta in contas:
        # Encontra o nome do titular usando o CPF armazenado na conta
        usuario_info = filtrar_usuario(conta["cpf_titular"], usuarios)
        nome_titular = usuario_info["nome"] if usuario_info else "Titular Desconhecido"

        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero']}
            Titular:\t{nome_titular}
            Saldo:\t\tR$ {conta['saldo']:.2f}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# --- Funções de Operações Bancárias ---

def depositar(conta, valor):
    """Realiza um depósito na conta especificada."""
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False
    
    conta['saldo'] += valor
    # Adiciona a transação ao histórico da conta
    conta['historico'].append(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Depósito:\tR$ {valor:.2f}")
    print("\n=== Depósito realizado com sucesso! ===")
    return True

def sacar(conta, valor):
    """Realiza um saque da conta especificada."""
    excedeu_saldo = valor > conta['saldo']
    excedeu_limite_transacao = valor > conta['limite']
    excedeu_limite_saques_diarios = conta['numero_saques_hoje'] >= conta['limite_saques_diarios']

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        return False
    elif excedeu_limite_transacao:
        print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R\$ {conta['limite']:.2f}. @@@")
        return False
    elif excedeu_limite_saques_diarios:
        print(f"\n@@@ Operação falhou! Número máximo de {conta['limite_saques_diarios']} saques diários excedido. @@@")
        return False
    elif valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False
    else:
        conta['saldo'] -= valor
        conta['numero_saques_hoje'] += 1
        # Adiciona a transação ao histórico da conta
        conta['historico'].append(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - Saque:\t\tR$ {valor:.2f}")
        print("\n=== Saque realizado com sucesso! ===")
        return True

def exibir_extrato(conta):
    """Exibe o extrato da conta especificada."""
    print("\n================ EXTRATO ================")
    if not conta['historico']:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta['historico']:
            print(transacao)
    print(f"\nSaldo atual:\t\tR$ {conta['saldo']:.2f}")
    print("==========================================")

# --- Funções Auxiliares para Operações do Menu ---

def selecionar_conta_para_operacao(usuarios, contas, nome_da_operacao):
    """
    Função auxiliar para selecionar uma conta de um usuário para realizar uma operação.
    Retorna o dicionário da conta selecionada ou None se não encontrada/selecionada.
    """
    cpf = input(f"Informe o CPF do cliente para {nome_da_operacao}: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Cliente não encontrado! @@@")
        return None

    contas_do_usuario = [c for c in contas if c['cpf_titular'] == cpf]

    if not contas_do_usuario:
        print("\n@@@ Cliente não possui contas cadastradas! @@@")
        return None

    if len(contas_do_usuario) == 1:
        # Se o cliente tem apenas uma conta, retorna-a diretamente
        return contas_do_usuario[0]
    else:
        # Se o cliente tem múltiplas contas, pede para selecionar
        print("\nContas disponíveis para este cliente:")
        for i, c in enumerate(contas_do_usuario):
            print(f"{i+1}. Conta: {c['numero']} (Agência: {c['agencia']}) Saldo: R\$ {c['saldo']:.2f}")
        
        while True:
            try:
                escolha = int(input("Selecione o NÚMERO da conta para operar: ")) - 1
                if 0 <= escolha < len(contas_do_usuario):
                    return contas_do_usuario[escolha]
                else:
                    print("Seleção inválida. Por favor, tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

def realizar_deposito_menu(usuarios, contas):
    """Função wrapper para a operação de depósito via menu."""
    conta_selecionada = selecionar_conta_para_operacao(usuarios, contas, "depósito")
    if conta_selecionada:
        try:
            valor = float(input("Informe o valor do depósito: "))
            depositar(conta_selecionada, valor)
        except ValueError:
            print("\n@@@ Valor inválido. Por favor, insira um número. @@@")

def realizar_saque_menu(usuarios, contas):
    """Função wrapper para a operação de saque via menu."""
    conta_selecionada = selecionar_conta_para_operacao(usuarios, contas, "saque")
    if conta_selecionada:
        try:
            valor = float(input("Informe o valor do saque: "))
            sacar(conta_selecionada, valor)
        except ValueError:
            print("\n@@@ Valor inválido. Por favor, insira um número. @@@")

def exibir_extrato_menu(usuarios, contas):
    """Função wrapper para a operação de extrato via menu."""
    conta_selecionada = selecionar_conta_para_operacao(usuarios, contas, "exibir extrato")
    if conta_selecionada:
        exibir_extrato(conta_selecionada)

# --- Função Principal ---
def main():
    while True:
        opcao = menu()

        if opcao == "d":
            realizar_deposito_menu(USUARIOS, CONTAS)

        elif opcao == "s":
            realizar_saque_menu(USUARIOS, CONTAS)

        elif opcao == "e":
            exibir_extrato_menu(USUARIOS, CONTAS)

        elif opcao == "nu":
            criar_usuario(USUARIOS)

        elif opcao == "nc":
            # O número da conta é sequencial, baseado na quantidade de contas já existentes
            next_account_number = len(CONTAS) + 1
            criar_conta(AGENCIA, next_account_number, USUARIOS, CONTAS)

        elif opcao == "lc":
            listar_contas(CONTAS, USUARIOS)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Garante que a função main() seja chamada apenas quando o script é executado diretamente
if __name__ == "__main__":
    main()