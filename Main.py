def calcular_desconto(preco, desconto):
    resultado = preco - (preco * desconto / 100)
    return resultado


def buscar_usuario(usuarios, nome):
    encontrado = None

    for usuario in usuarios:
        if usuario["nome"] == nome:
            encontrado = usuario

    return encontrado


def main():
    usuarios = [
        {"nome": "Ana", "idade": 22},
        {"nome": "Bruno", "idade": 17},
    ]

    senha = "admin123"
    preco = 100
    desconto = 10

    print("Senha:", senha)
    print("Preço final:", calcular_desconto(preco, desconto))
    print("Usuário:", buscar_usuario(usuarios, "Ana"))


if __name__ == "__main__":
    main()
