
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)


# Dados simulados da loja
usuarios = [
    {"id": 1, "nome": "Ana", "idade": 22, "senha": "ana123"},
    {"id": 2, "nome": "Bruno", "idade": 17, "senha": "bruno123"},
    {"id": 3, "nome": "Carlos", "idade": 30, "senha": "carlos123"},
]

produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500.00, "estoque": 10},
    {"id": 2, "nome": "Mouse", "preco": 80.00, "estoque": 50},
    {"id": 3, "nome": "Teclado", "preco": 150.00, "estoque": 20},
    {"id": 4, "nome": "Monitor", "preco": 900.00, "estoque": 15},
]

historico_compras = []


def buscar_usuario(nome):
    resultado = None

    for usuario in usuarios:
        if usuario["nome"] == nome:
            resultado = usuario

    return resultado


def autenticar_usuario(nome, senha):
    usuario = buscar_usuario(nome)

    if usuario is not None:
        if usuario["senha"] == senha:
            print("Login realizado com sucesso!")
            return True
        else:
            print("Senha incorreta!")
            return False

    print("Usuário não encontrado!")
    return False


def listar_produtos():
    print("\n===== PRODUTOS DISPONÍVEIS =====")

    for produto in produtos:
        print(
            f"ID: {produto['id']} | "
            f"Nome: {produto['nome']} | "
            f"Preço: R$ {produto['preco']:.2f} | "
            f"Estoque: {produto['estoque']}"
        )


def buscar_produto(produto_id):
    for produto in produtos:
        if produto["id"] == produto_id:
            return produto

    return None


def calcular_desconto(preco, desconto):
    resultado = preco - (preco * desconto / 100)
    return resultado


def calcular_frete(valor):
    if valor >= 500:
        return 0
    elif valor >= 200:
        return 15
    else:
        return 30


def adicionar_ao_carrinho(carrinho, produto_id, quantidade):
    produto = buscar_produto(produto_id)

    if produto is None:
        print("Produto não encontrado!")
        return carrinho

    if quantidade <= 0:
        print("Quantidade inválida!")
        return carrinho

    if produto["estoque"] < quantidade:
        print("Estoque insuficiente!")
        return carrinho

    item = {
        "produto_id": produto_id,
        "nome": produto["nome"],
        "preco": produto["preco"],
        "quantidade": quantidade,
    }

    carrinho.append(item)
    print("Produto adicionado ao carrinho!")

    return carrinho


def calcular_total(carrinho):
    total = 0

    for item in carrinho:
        total = total + item["preco"] * item["quantidade"]

    return total


def aplicar_cupom(total, cupom):
    if cupom == "PROMO10":
        total = calcular_desconto(total, 10)
    elif cupom == "PROMO20":
        total = calcular_desconto(total, 20)
    elif cupom == "PROMO30":
        total = calcular_desconto(total, 30)
    else:
        print("Cupom inválido!")

    return total


def finalizar_compra(usuario, carrinho, cupom=""):
    if len(carrinho) == 0:
        print("Carrinho vazio!")
        return None

    total = calcular_total(carrinho)

    if cupom != "":
        total = aplicar_cupom(total, cupom)

    frete = calcular_frete(total)
    valor_final = total + frete

    compra = {
        "usuario": usuario["nome"],
        "itens": carrinho.copy(),
        "subtotal": total,
        "frete": frete,
        "total": valor_final,
        "data": str(datetime.now()),
    }

    historico_compras.append(compra)

    for item in carrinho:
        produto = buscar_produto(item["produto_id"])
        if produto:
            produto["estoque"] = (
                produto["estoque"] - item["quantidade"]
            )

    print("\n===== RESUMO DA COMPRA =====")
    print("Cliente:", usuario["nome"])
    print("Subtotal: R$", round(total, 2))
    print("Frete: R$", round(frete, 2))
    print("Total: R$", round(valor_final, 2))

    carrinho.clear()

    return compra


def exibir_historico():
    print("\n===== HISTÓRICO DE COMPRAS =====")

    for compra in historico_compras:
        print(
            f"Cliente: {compra['usuario']} | "
            f"Data: {compra['data']} | "
            f"Total: R$ {compra['total']:.2f}"
        )


def exportar_historico():
    dados = json.dumps(historico_compras, indent=4)

    with open("historico.json", "w", encoding="utf-8") as arquivo:
        arquivo.write(dados)

    print("Histórico exportado com sucesso!")


def relatorio_vendas():
    total_vendido = 0
    quantidade_vendas = 0

    for compra in historico_compras:
        total_vendido += compra["total"]
        quantidade_vendas += 1

    if quantidade_vendas > 0:
        media = total_vendido / quantidade_vendas
    else:
        media = 0

    print("\n===== RELATÓRIO DE VENDAS =====")
    print("Quantidade de vendas:", quantidade_vendas)
    print("Total vendido: R$", round(total_vendido, 2))
    print("Média por venda: R$", round(media, 2))


def cadastrar_usuario(nome, idade, senha):
    novo_usuario = {
        "id": len(usuarios) + 1,
        "nome": nome,
        "idade": idade,
        "senha": senha,
    }

    usuarios.append(novo_usuario)
    print("Usuário cadastrado com sucesso!")

    return novo_usuario


def menu():
    usuario_logado = None
    carrinho = []

    while True:
        print("\n===== SISTEMA DA LOJA =====")
        print("1 - Login")
        print("2 - Listar produtos")
        print("3 - Adicionar produto ao carrinho")
        print("4 - Finalizar compra")
        print("5 - Histórico")
        print("6 - Relatório de vendas")
        print("7 - Cadastrar usuário")
        print("8 - Exportar histórico")
        print("9 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            senha = input("Senha: ")

            if autenticar_usuario(nome, senha):
                usuario_logado = buscar_usuario(nome)

        elif opcao == "2":
            listar_produtos()

        elif opcao == "3":
            listar_produtos()

            produto_id = int(input("ID do produto: "))
            quantidade = int(input("Quantidade: "))

            adicionar_ao_carrinho(
                carrinho, produto_id, quantidade
            )

        elif opcao == "4":
            if usuario_logado is None:
                print("Faça login antes de comprar!")
            else:
                cupom = input("Cupom de desconto (Enter para pular): ")

                finalizar_compra(
                    usuario_logado, carrinho, cupom
                )

        elif opcao == "5":
            exibir_historico()

        elif opcao == "6":
            relatorio_vendas()

        elif opcao == "7":
            nome = input("Nome do novo usuário: ")
            idade = int(input("Idade: "))
            senha = input("Senha: ")

            cadastrar_usuario(nome, idade, senha)

        elif opcao == "8":
            exportar_historico()

        elif opcao == "9":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()
