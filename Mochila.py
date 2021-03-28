
# Objetivo: achar um vetor de inteiros (entre i_min e i_max) com i_length posicoes cuja a soma de todos os termos seja o mais proximo possivel de target

#O algoritmo rodara epochs vezes -> numero de populacoes geradas. Sera impresso a media de fitness de cada uma das epochs populacoes

#RODAR COM PYTHON 2!!! (senao colocar () em print e tirar x de xrange


from roleta import *

i_length = 10 # items de genes do individuo/cromossomo -> genes
i_min = 0 # valor minimo do gene
i_max = 1 # valor maximo do gene
p_count = 1000 # numero de individuo/cromossomo 
epochs = 20 # numero de epocas 

pesoMaximo = 100  # peso maximo que a mochila que suporta

peso = [5, 14, 4, 85, 28, 16, 9, 1, 19, 8]  # array com os pesos individuais de cada item
importancia = [6, 2, 3, 4, 5, 6, 7, 8, 9 , 15] # array com os valores das importancias de cada item
target = sum(importancia) # soma das importancias e objetivo a ser alcançado

p = population(p_count, i_length, i_min, i_max) # geração de uma população aleatória inicial de 0 e 1

grupoDePopulacaoFitness = [p,[media_fitness(p, target, peso, importancia)]] # array que armazena as populações e suas fitness durante as epocas

for i in range(epochs): # For para passar por todas as epocas
    p = evolve(p, p_count, peso, target, i_length, importancia, pesoMaximo) # Função de evolução 
    grupoDePopulacaoFitness.append([p, media_fitness(p, target, peso,importancia)]) #Armazena a população e sua fitness 

UltimoPopulacao = grupoDePopulacaoFitness[len(grupoDePopulacaoFitness)-1][0] # pega o valor da população da ultima epoca
melhorValor = 0 # inicia a variavel que vai conter o melhor valor da importancia
melhorCombinacao = [] #inicia a variavel que vai conter o valor da melhor combinação
somaImportancia = 0 #inicia a variavel que vai conter o valor da soma das importancias
for i in range(len(UltimoPopulacao)): # for na ultima população ex: [[0,1],[0,1],[0,1]] , é usado para achar a melhor combinação dos items da ultima população
    for j in range(len(UltimoPopulacao[i])): # for em cada cromossomo ex: [0,1]
        if(UltimoPopulacao[i][j] == 1): #verificação se o valor é 1, o que significa que esta na mochila
            somaImportancia +=  importancia[j] # Se o item esta na mochila é feito um somatorio de sua importancia
    if(melhorValor < somaImportancia): # Comparação entre o melhor valor ja encontrado e o somatorio do cromossomo atual
        melhorValor = somaImportancia # 
        melhorCombinacao = UltimoPopulacao[i] 
    somaImportancia = 0

print('Melhor Valor', melhorValor) 
print('Melhor Combinação', melhorCombinacao)

