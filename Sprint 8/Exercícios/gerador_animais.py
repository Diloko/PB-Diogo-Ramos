import random

animais = ["Cachorro", "Gato", "Leão", "Tigre", "Elefante", "Girafa", "Cobra", "Coelho",
           "Cavalo", "Ovelha", "Galinha", "Porco", "Vaca", "Rinoceronte", "Canguru", 
           "Pato", "Rato", "Papagaio", "Macaco", "Jacaré"]

# Ordenar os nomes em ordem crescente
animais.sort()

# Iterar sobre os itens da lista, imprimindo-os um por um
for animal in animais:
    print(animal)

# Armazenar o conteúdo da lista em um arquivo de texto, com um item por linha, em formato CSV
with open("animais.csv", "w") as file:
    for animal in animais:
        file.write(animal + "\n")
