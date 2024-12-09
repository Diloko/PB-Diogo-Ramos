import random
import names

qtd_nomes_unicos = 3000
qtd_nomes_aleatorios = 1000000

aux = []

# Gerar nomes únicos
for i in range(0, qtd_nomes_unicos):
    aux.append(names.get_full_name())

print("Gerando {} nomes aleatórios".format(qtd_nomes_aleatorios))

dados = []

# Gerar lista de nomes aleatórios a partir dos nomes únicos
for i in range(0, qtd_nomes_aleatorios):
    dados.append(random.choice(aux))

# Salvar os nomes em um arquivo de texto, um por linha
with open("nomes_aleatorios.txt", "w") as file:
    for nome in dados:
        file.write(nome + "\n")
