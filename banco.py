import textwrap

def validar_cpf_basico(cpf):
    """Verifica se o CPF tem 11 dígitos e é numérico."""
    return len(cpf) == 11 and cpf.isdigit()

def formatar_cpf_para_display(cpf_11_digitos):
    """Formata o CPF no padrão XXX.XXX.XXX-XX."""
    return f"{cpf_11_digitos[:3]}.{cpf_11_digitos[3:6]}.{cpf_11_digitos[6:9]}-{cpf_11_digitos[9:]}"


def menu(): 
    menu = """\n
    ************ MENU ***************
    [d] \tDepositar
    [s] \tSacar
    [e] \tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q] \tSair
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n$$$$$$$$$ Depósito realizado com sucesso! $$$$$$$$$")
    else:
        print("\nXXXXXXXX Operação falhou! O valor informado é inválido. XXXXXXXX")
        
    return saldo, extrato

def sacar (*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nXXXXXXXX Operação falhou! Você não tem saldo suficiente.XXXXXXXX")
    
    elif excedeu_limite:
        print("\nXXXXXXXX Operação falhou! O valor do saque excede o limite. XXXXXXXX")
    
    elif excedeu_saques:
        print("XXXXXXXX\n Operação falhou! Número máximo de saques excedido. XXXXXXXX")
    
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t \t R$ {valor: .2f}\n"
        numero_saques += 1
        print("\n$$$$$$$$$ Saque realizado com sucesso $$$$$$$$$")

    else:
        print("\nXXXXXXXX Operação falhou! O valor informado é inválido. XXXXXXXX")
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n -------------Extrato--------------")
    print(" Não foram realizadas movimentações. " if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo: .2f}")
    print("------------------------------------")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    
    if not validar_cpf_basico(cpf):
        print("\nXXXXXXXX Operação falhou! O CPF deve conter 11 dígitos numéricos. XXXXXXXX")
        return

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nXXXXXXXX Já existe usuário com esse CPF! XXXXXXXX")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento(dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    cpf_formatado = formatar_cpf_para_display(cpf)
    print(f"++++++++ Usuário com CPF {cpf_formatado} criado com sucesso! ++++++++")

def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def criar_conta(agencia, numero_conta, usuarios):
    cpf_input = input("Informe o CPF do usuário: ")

    # VALIDAÇÃO DO CPF DE BUSCA
    if not validar_cpf_basico(cpf_input):
        print("\nXXXXXXXX Operação falhou! O CPF informado é inválido (deve ter 11 dígitos numéricos). XXXXXXXX")
        return None
        
    usuario = filtrar_usuario(cpf_input, usuarios)

    if usuario:
        print("\n ++++++++ Conta criada com sucesso! ++++++++")
        return{"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\nXXXXXXXX Usuário não encontrado, fluxo de criação de conta encerrado! XXXXXXXX")
    return None

def listar_contas(contas):
    if not contas:
        print("\nSem contas cadastradas para exibir.")
        return

    print("\n############ LISTA DE CONTAS ############")
    for conta in contas:
        cpf_11_digitos = conta['usuario']['cpf']
        cpf_formatado = formatar_cpf_para_display(cpf_11_digitos)
        
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']:04d}
            Titular:\t{conta['usuario']['nome']}
            CPF:\t\t{cpf_formatado}
        """
        print("=" * 50)
        print(textwrap.dedent(linha))
    print("=" * 50)


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            
            saldo, extrato, numero_saques = sacar(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            
            )
        
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == "nu":
            criar_usuario(usuarios)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
        
        elif opcao == "lc":
            listar_contas(contas)
        
        elif opcao == "q":
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
