
# Objetivo: achar um vetor de inteiros (entre i_min e i_max) com i_length posicoes cuja a soma de todos os termos seja o mais proximo possivel de target

#O algoritmo rodara epochs vezes -> numero de populacoes geradas. Sera impresso a media de fitness de cada uma das epochs populacoes

#RODAR COM PYTHON 2!!! (senao colocar () em print e tirar x de xrange
  

from roleta import *
# from genetic2020 import *
i_length = 10 # items de genes do individuo/cromossomo -> genes
i_min = 0 # valor minimo do gene
i_max = 1 # valor maximo do gene
p_count = 1000 # numero de individuo/cromossomo 
epochs = 20

pesoMaximo = 100

peso = [5, 14, 4, 85, 28, 16, 9, 1, 19, 8]
# [[0   0  0   1   1   1   1   1   1  1 ],[0   1  0   1   1   1   1   1   1  1 ]]
importancia = [6, 2, 3, 4, 5, 6, 7, 8, 9 , 15]
target = sum(importancia)

p = population(p_count, i_length, i_min, i_max)

# p = [[0, 0, 1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 0, 1, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1, 1, 1], [1, 1, 1, 0, 1, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 1, 1, 0, 1]]

fitness_history = [media_fitness(p, target, peso, importancia)]

gurizada = []

for i in range(epochs):
    print('EPOCA NUMERO: ',i)

    p = evolve(p, p_count, peso, target, i_length, importancia, pesoMaximo)
    gurizada.append([p, media_fitness(p, target, peso,importancia)])
    fitness_history.append(media_fitness(p, target, peso,importancia))

melhor = 100000000
for datum in fitness_history:    
    if(datum < melhor):
        melhor = datum
    
# p = [[0, 0, 1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 0, 1, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1, 1, 1], [1, 1, 1, 0, 1, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 1, 1, 0, 1]]

best = gurizada[len(gurizada)-1][0]
melhorValor = 0
melhorCombinacao = []
somImportancia = 0
for i in range(len(best)):
    for j in range(len(best[i])):
        if(best[i][j] == 1):
            somImportancia = somImportancia + importancia[j]
    if(melhorValor < somImportancia):
        melhorValor = somImportancia
        melhorCombinacao = best[i]
    somImportancia = 0

print('Melhor Valor', melhorValor)
print('Melhor Combinação', melhorCombinacao)

