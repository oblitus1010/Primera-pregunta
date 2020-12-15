# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 09:59:03 2020

@author: briya
"""

import random

#Matriz de rutas y costos
#Leyendo los datos de un archivo csv
with open('datos.csv') as File:
    datos = File.read().splitlines()
    costos = []
#Recorremos cada lista de lista datos
    for i in datos:
        var = i.split(',') # en var guardamos la la primera lista de datos y quitamos ,
        costos.append([int(var[j]) for j in range(len(var))]) #en costos recorremos var convirtiendo a entero
        
#Lista de ciudades
ciudades = [1,2,3,4]
print(costos)

modelEnd = [1,1,1,1,1,1,1,1,1,1] 
largeIndividual = 4 

num = 5 #Cantidad de individuos
generation = 5 #Generaciones
pressure = 3 #individual>2
mutation_chance = 0.2

def es_unico(x, li):
    flag = True;
    for i in range(len(li)):
        if (x==li[i]):
            flag = False
            break
    return flag

def individual(min, max):
    lista = []
    i = 0
    while(i < largeIndividual):
        x = random.randint(min, max)
        if es_unico(x, lista):
            lista.append(x)
            i += 1
            
    return lista

def newPopulation():
    return [individual(1,4) for i in range(num)]


# Funcion que retorna el fitness del individuo mas apto
def functionType(individual):
    
    fitness = 0 # Sera el costo mas bajo
    
    for i in range(len(individual)-1):
        # Busca el costo en la fila i, columna j y lo suma al fitness
        fitness += costos[individual[i]-1][individual[i+1]-1]
    
    fitness += costos[len(individual)-1][0]
    
    return fitness


def selection_and_reproduction(population):
    evaluating = [ (functionType(i), i) for i in population]
    print("eval",evaluating)
    evaluating = [i[1] for i in sorted(evaluating, reverse=True)]
    #print("eval",evaluating)
    population = evaluating
    selected = evaluating[(len(evaluating)-pressure):]
    for i in range(len(population)-pressure):
        
        pointChange = random.randint(1,largeIndividual-1)
        father = random.sample(selected, 2)
        #print("father sample",father)
        population[i][:pointChange] = father[0][:pointChange]
        population[i][pointChange:] = father[1][pointChange:]
        
# =============================================================================
#         print("-------------")
#         print(father[0])
#         print(father[1])
#         print(pointChange)
#         print(population[i])
# =============================================================================
        
    return population

def mutation(population):
    for i in range(len(population)-pressure):
        if random.random() <= mutation_chance: 
            pointChange = random.randint(1,largeIndividual-1) 
            new_val = random.randint(1,4) 
            print("--")
            print(population[i])
            while new_val == population[i][pointChange]:
                new_val = random.randint(1,4)
            population[i][pointChange] = new_val
            print(pointChange)
            print(population[i])
    return population

def no_repetido(lista):
    flag = True
    for i in range(len(lista)-1):
        if(lista[i] in lista[i+1:]):
            flag = False
        
    return flag

def best_of_generation(evaluating):  
    lista = []
    menor_costo = evaluating[0][0]
    for i in range(len(evaluating)):
        if((menor_costo > evaluating[i][0]) and no_repetido(evaluating[i][1])):
            menor_costo = evaluating[i][0]
            lista = [menor_costo,evaluating[i][1]]
    return lista
# Principal
population = newPopulation()

for i in range(generation):
    
    print("\n*********GENERACION ",i," ***********\n")
    print("\nPopulation Begin:\n%s"%(population))
    population = selection_and_reproduction(population)
    print("\Selection Population:\n%s"%(population))
    population = mutation(population)
    print("\Mutation Population:\n%s"%(population))
    evaluating = [(functionType(i), i) for i in population]
    print("eval",evaluating)
    print("\nEl mejor de la generacion : ", best_of_generation(evaluating))