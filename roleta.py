
from random import randint, random
from operator import add
from functools import reduce

def select(arrFitness, peso, pesoMaximo, arrMochila):
    counti = 0
    countj = 0
    pesoIndividuo = 0
    Pesado = []
    # print('arr mochila', arrMochila)
    for i in arrMochila:
        # print('arr mochila - posicao i ', arrMochila[i])
        # print('arr mochila - posicao counti ', arrMochila[counti])
        for j in arrMochila[counti]:
            # print('IIIIIIIIIIIIII',i)
            if (j == 1):
                # print('JOTAJOTA',j)
                # print(peso[countj])
                pesoIndividuo =  pesoIndividuo + peso[countj]
            countj += 1
        if (pesoIndividuo > pesoMaximo):
            Pesado.append(counti)
        counti += 1
        countj = 0
        pesoIndividuo=0
    
    # print('AAAAAAAAAAAAARRAY MOCHILA - ANTES', arrMochila)
    # print(len(arrMochila))
    # somelist = range(len(arrMochila))
    arrMochila = [i for j, i in enumerate(arrMochila) if j not in Pesado]
    # print('AAAAAAAAAAAAARRAY MOCHILA - DEPOIS', arrMochila)    
    p = randint(0, sum(arrFitness)) 
    for x, f in enumerate(arrFitness):
        # print(x,f)
        if p <= 0:
            break
        p -= f
    return [x, Pesado]

def individual(length, min, max):
    'Create a member of the population.'
    return [ randint(min,max) for x in range(length) ]

def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values

    """
    return [ individual(length, min, max) for x in range(count) ]

def fitness(cromossomo, importancia, target):
    """
    Determine the fitness of an individual. Higher is better.

    individual: the individual to evaluate
    target: the target number individuals are aiming for

    O fitness do individuo perfeito sera ZERO, ja que o somatorioatorio dara o target
    reduce: reduz um vetor a um escalar, neste caso usando o operador add
    """
    importanciaCromossomo = []
    count = 0
    
    for gene in cromossomo:
        if(gene == 1):
            # print(peso[count])
            importanciaCromossomo.append(importancia[count])
        count = count + 1
    
    sum = reduce(add, importanciaCromossomo, 0)
    return abs(target-sum)

def media_fitness(pop, target, peso, importancia):
    'Find average fitness for a population.'    
    
    summed = reduce(add, (fitness(x, importancia, target) for x in pop))

    return summed / (len(pop) * 1.0)

def evolve(pop, cromo, peso, target, i_length, importancia, pesoMaximo, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [ (fitness(x, importancia, target), x) for x in pop]
    parents = []
    #variavel para o SUM dos fitness.
    somatorio = 0

    for x in graded:
        somatorio = somatorio + x[0]
        #Aqui será feita a ordenaçao do menor fitness para o maior fitness
        graded = [ x for x in sorted(graded)]
    
    arrFitness = []
    arrMochila = []
    for individual in graded:
        arrFitness.append(individual[0])
        arrMochila.append(individual[1])    
    resultado = select(arrFitness, peso, pesoMaximo, arrMochila)
    while(resultado[0] <= 1):
        resultado = select(arrFitness, peso, pesoMaximo, arrMochila)

    # print('resultado', resultado)
    # print('graded - antes de titrar os pesados', graded)
    # print('ARRAY MOCHILA DENTRO DO EVOLVE', arrMochila)
    arrMochila = [i for j, i in enumerate(arrMochila) if j not in resultado[1]]
    # print('arrmochila- depois de tirar os pesados', arrMochila)
    
    if(len(arrMochila) < resultado[0]):
        resultado[0] = len(arrMochila)

    for i in range(resultado[0]):
        parents.append(arrMochila[i])
    # print('PARENTS - ', parents)
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))
    # print('PARADA 2')
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    'comeca a gerar filhos que faltam'
    while len(children) < desired_length:
        # print('PAIS',parents)
        'escolhe pai e mae no conjunto de pais'
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        # print(male,female)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) // 2
            'gera filho metade de cada'
            child = male[:half] + female[half:]
            'adiciona novo filho a lista de filhos'
            children.append(child)
    # print('PARADA 3')
    'adiciona a lista de pais (elites) os filhos gerados'
    parents.extend(children)
    # print('PARADA 4')
    return parents