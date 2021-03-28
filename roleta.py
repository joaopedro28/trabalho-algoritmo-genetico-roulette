
from random import randint, random
from operator import add
from functools import reduce

def select(arrFitness, peso, pesoMaximo, arrMochila): # Função da roleta 
    counti = 0
    countj = 0
    pesoIndividuo = 0 
    Pesado = [] #inicio de um array que vai conter as posições dos cromossomos que possuem as combinações que ultrapassam o pesoMaximo
    # o For abaixo foi criado para evitar que futuros cromossomos continuem com combinações que exedam o valor maximo que a mochila suporta
    for i in arrMochila:
        for j in arrMochila[counti]:
            if (j == 1):
                pesoIndividuo =  pesoIndividuo + peso[countj]
            countj += 1
        if (pesoIndividuo > pesoMaximo):
            Pesado.append(counti)
        counti += 1
        countj = 0
        pesoIndividuo=0
# Ja o For abaixo esta repreenchendo o array mochila somento com cromossomos que não ultrapassam o limite de peso.
    arrMochila = [i for j, i in enumerate(arrMochila) if j not in Pesado] 
# Aqui é feito uma escolha aleatória de um numero de 0 até a soma dos valores de fitness, para pegar o numero de Parents que serão usados nesta época
    p = randint(0, sum(arrFitness)) 
    for x, f in enumerate(arrFitness):
        if p <= 0:
            break
        p -= f
# É retornado o numero de Parents que haverão na população e as posições que ultrapassam o peso e que devem ser desconsideradas.
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
            importanciaCromossomo.append(importancia[count])
        count = count + 1
    
    sum = reduce(add, importanciaCromossomo, 0)
    return abs(target-sum)

def media_fitness(pop, target, peso, importancia):
    'Find average fitness for a population.'    
    
    summed = reduce(add, (fitness(x, importancia, target) for x in pop))

    return summed / (len(pop) * 1.0)

def evolve(pop, cromo, peso, target, i_length, importancia, pesoMaximo, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [ (fitness(x, importancia, target), x) for x in pop] #criação de um array que recebe as fitness de cada cromossomo da população [(fiteness,[população])]
    parents = [] #inicio do arrai de pais
    
    somatorio = 0 #variavel para o SUM dos fitness.

    for x in graded: # Ordenação da melhor fitness
        somatorio = somatorio + x[0]
        #Aqui será feita a ordenaçao do menor fitness para o maior fitness
        graded = [ x for x in sorted(graded)]
    
    arrFitness = []
    arrMochila = []
    for individual in graded: #separa em dois arrays um possuindo todas as fitness e um possuindo todas combinações 
        arrFitness.append(individual[0])
        arrMochila.append(individual[1])    
    resultado = select(arrFitness, peso, pesoMaximo, arrMochila) # Aplica o metodo de roleta
    while(resultado[0] <= 1): # Caso a roleta entregue apenas um parente, é refeito do Metodo para que não ocorra erro
        resultado = select(arrFitness, peso, pesoMaximo, arrMochila)

    # Este for utiliza as informações retornadas pela função select para descartar as posições que exedem o limite de peso.
    arrMochila = [i for j, i in enumerate(arrMochila) if j not in resultado[1]] 
        
    # Caso a roleta entregue um numero maior do que o de cromossomos restantes o resultado ira receber o valor minimo, que seria o proprio numero de cromossomos restantes.
    if(len(arrMochila) < resultado[0]):
        resultado[0] = len(arrMochila)
    # For serve para criar os Parents.
    for i in range(resultado[0]):
        parents.append(arrMochila[i])
    # Aqui ele faz a mutação conforme os Parents recebidos
    for individual in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(individual)-1)
            individual[pos_to_mutate] = randint(
                min(individual), max(individual))
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    'comeca a gerar filhos que faltam'
    while len(children) < desired_length:
        'escolhe pai e mae no conjunto de pais'
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = len(male) // 2
            'gera filho metade de cada'
            child = male[:half] + female[half:]
            'adiciona novo filho a lista de filhos'
            children.append(child)
    'adiciona a lista de pais (elites) os filhos gerados'
    parents.extend(children)
    return parents