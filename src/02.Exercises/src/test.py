#! /usr/bin/python3

#  Author:  Domenico Stefani (domenico.stefani@unitn.it) (https://orcid.org/0000-0002-2126-0667)
#  Created: 16th March 2021

# #-----------------------------------------------------------------------------#  
# # Problem Formalization                                                       #  
# #-----------------------------------------------------------------------------#  
# 
# Fixed parameters:
# - Hop size
# - Buffer Size
# - Onset Method
# - Min IoI
# 
# Genotype: (free parameters)
# - Silence Threshold
# - Onset Threshold
# 
# Phenotype: (Manifestation of the genotype, used for performance evaluation)
# - macro avg. f1-score (f1-score for each playing technique in the dataset)
# 

# TODO: Check whether these are all used
from pylab import *
from random import Random
import inspyred
import sys
import numpy as np
from inspyred import ec
from inspyred import benchmarks
import ga2

# """--Parameters for aubio ---------------------------------------------------"""
AUDIO_DIRECTORY = "audiofiles"
aubioonset_command = "aubioonset"
onset_method = "hfc" # TODO: Later change this
BUFFER_SIZE = 64
HOP_SIZE = 64
MIN_IOI = 0.02

MIN_ONSET_THRESH   = 0.1 # TODO: Finetune when working
MAX_ONSET_THRESH   = 3.6
MIN_SILENCE_THRESH = -60
MAX_SILENCE_THRESH = -30

# """--Parameters for the EC---------------------------------------------------"""

populationSize = 10
numberOfGenerations = 15
numberOfEvaluations = 2500                    # used with evaluation_termination
tournamentSize = 7
mutationRate = 0.95
gaussianMean = 0
gaussianStdev = 10.0
crossoverRate = 0.50
# numCrossoverPoints =  5           TODO: check what this does
# selectionSize = populationSize    TODO: check what this does
numElites = 1

# """--Visualization-----------------------------------------------------------"""
display = True

def main(rng, display=False):
    problem = benchmarks.Rastrigin(2)#ConfigurationEvaluator(rng)

    # --------------------------------------------------------------------------- #
    # EA configuration TODO: Configure properly

    # the evolutionary algorithm (EvolutionaryComputation is a fully configurable evolutionary algorithm)
    # standard GA, ES, SA, DE, EDA, PAES, NSGA2, PSO and ACO are also available
    ea = inspyred.ec.EvolutionaryComputation(rng)

    # observers: provide various logging features
    # if display:
    # ea.observer = [#inspyred.ec.observers.stats_observer,
                   # inspyred.ec.observers.file_observer,
                    # inspyred.ec.observers.plot_observer
                    #inspyred.ec.observers.best_observer,
                    #inspyred.ec.observers.population_observer
                    # ]
    ea.observer = inspyred.ec.observers.plot_observer


    # selection operator
    #ea.selector = inspyred.ec.selectors.truncation_selection
    #ea.selector = inspyred.ec.selectors.uniform_selection
    #ea.selector = inspyred.ec.selectors.fitness_proportionate_selection
    #ea.selector = inspyred.ec.selectors.rank_selection
    ea.selector = inspyred.ec.selectors.tournament_selection

    # variation operators (mutation/crossover)
    ea.variator = [inspyred.ec.variators.arithmetic_crossover,
                   inspyred.ec.variators.blend_crossover,
                   inspyred.ec.variators.heuristic_crossover,
                   inspyred.ec.variators.laplace_crossover,
                   inspyred.ec.variators.simulated_binary_crossover,
                   inspyred.ec.variators.gaussian_mutation,
                   inspyred.ec.variators.nonuniform_mutation
                   ]

    # --------------------------------------------------------------------------- #

    # run the EA
    final_pop = ea.evolve(evaluator=problem.evaluator,
                          generator=problem.generator,
                          bounder=problem.bounder,
                          maximize=problem.maximize,
                          pop_size=populationSize,
                          max_generations=numberOfGenerations,
                          max_evaluations=numberOfEvaluations,
                          tournament_size=tournamentSize,
                          mutation_rate=mutationRate,
                          gaussian_mean=gaussianMean,
                          gaussian_stdev=gaussianStdev,
                          crossover_rate=crossoverRate,
                          num_elites=numElites)

    if display:
        final_pop.sort(reverse=True)
        print(final_pop[0])
        candidate = final_pop[0].candidate
        # TODO: Display
        # TODO: Save the results


if __name__ == "__main__":
    # # Initialize the random generator
    # if len(sys.argv) > 1 :
    #     seed = int(sys.argv[1])
    # else:
    #     seed = int(time.time())

    # rng = Random(int(seed))

    # main(rng, display=display)

    # if display:
    #     ioff()
    #     show()

    if len(sys.argv) > 1 :
        rng = Random(int(sys.argv[1]))
    else :
        rng = Random()
    args = {}
    args["num_vars"] = 2 # Number of dimensions of the search space
    args["gaussian_stdev"] = 0.5 # Standard deviation of the Gaussian mutations
    args["crossover_rate"]  = 0.8 # Crossover fraction
    args["tournament_size"] = 2 
    args["pop_size"] = 10 # population size

    args["num_elites"] = 1 # number of elite individuals to maintain in each gen
    args["mutation_rate"] = 0.5 # fraction of loci to perform mutation on

    # by default will use the problem's defined init_range
    # uncomment the following line to use a specific range instead
    #args["pop_init_range"] = [-500, 500] # Range for the initial population
    args["use_bounder"] = True # use the problem's bounder to restrict values
    # comment out the previously line to run unbounded

    args["max_generations"] = 100 # Number of generations of the GA
    display = True # Plot initial and final populations
    args["fig_title"] = 'GA'


    # choose problem
    # problem_class = benchmarks.Sphere
    problem_class = benchmarks.Rastrigin
    best_individual, best_fitness, final_pop = ga2.run_ga(rng, display=display,
                                           problem_class=problem_class,**args)
    print("Best Individual: "+str(best_individual))
    print("Best Fitness: "+str(best_fitness))
    
    if display :
        ioff()
        show()
