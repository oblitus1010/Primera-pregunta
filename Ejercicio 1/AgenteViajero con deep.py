# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 11:22:04 2020

@author: briya
"""

import array
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

#Lectura de la matriz de costos
with open('datos.csv') as File:
    datos = File.read().splitlines()
    costos = []
#Recorremos cada lista de lista datos
    for i in datos:
        var = i.split(',') # en var guardamos la la primera lista de datos y quitamos ,
        costos.append([int(var[j]) for j in range(len(var))]) #en costos recorremos var convirtiendo a entero


# Maximizar=1 o minimizar=-1 
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
#  tipo individuo 
creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)
# operaciones
toolbox = base.Toolbox()

#  funcion que se llena el individuo 
# Attribute                             llena el individuo con randomicos

toolbox.register("attr_bool", random.randint, 1, 4)

# generacion del individuo y poblacion 
# Structure initializers                                                        tamaño del individuo
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 4)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# funcion objetivo 
def Rutacorta(individual):
    #Verificamos si el individuo tiene valores repetidos
    repetido = []
    for i in individual:
        if i not in repetido:
            repetido.append(i)
    valor = 1000
    fitness = 0 # Sera el costo mas bajo
    for i in range(len(individual)-1):
        # Busca el costo en la fila i, columna j y lo suma al fitness
        if((costos[individual[i]-1][individual[i+1]-1]) > 0):
                fitness += costos[individual[i]-1][individual[i+1]-1]
    fitness += costos[len(individual)-1][0] #suma la vuelta a el inicio
    
    if(len(repetido)>0):
        return valor,
    else:
        return fitness,

# operaciones 
toolbox.register("evaluate", Rutacorta)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=2)

def mostrar(selected):
    print(selected)
    return 0

def main():
    random.seed(64)
    # genera la poblacion 
    pop = toolbox.population(n=100)
    # el mejor individuo (min-max)
    hof = tools.HallOfFame(1)
    # estadisticas basicas
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, 
                                   stats=stats, halloffame=hof, verbose=False)
    
    return pop, log, hof

if __name__ == "__main__":
    pop, log, hof = main()
    print(hof)
    print(pop)
