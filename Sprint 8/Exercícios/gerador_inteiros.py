import random

# Declarar e inicializar uma lista contendo 250 inteiros obtidos de forma aleatória
lista = [random.randint(0, 1000) for _ in range(250)]

# Aplicar o método reverse sobre o conteúdo da lista
lista.reverse()

# Imprimir o resultado
print(lista)
