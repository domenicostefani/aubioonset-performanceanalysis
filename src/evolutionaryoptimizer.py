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
import pylab
from random import Random
import inspyred
import sys
import numpy as np
import computeLatency
from inspyred import ec

NUMBER_OF_AVAILABLE_CPUS = 6

# """--Parameters for aubio ---------------------------------------------------"""
AUDIO_DIRECTORY = "audiofiles"
aubioonset_command = "aubioonset"
default_onset_method = "hfc" # TODO: Later change this
default_buffer_size = 64
HOP_SIZE = 64
MIN_IOI = 0.02

MIN_ONSET_THRESH   = 0.1 # TODO: Finetune when working
MAX_ONSET_THRESH   = 3.6
MIN_SILENCE_THRESH = -60
MAX_SILENCE_THRESH = -30

# """--Parameters for the EC---------------------------------------------------"""

populationSize = 6
numberOfGenerations = 30
numberOfEvaluations = 2500                    # used with evaluation_termination
tournamentSize = 3
mutationRate = 0.7
gaussianMean = 0
gaussianStdev = 1.0
crossoverRate = 0.9
# numCrossoverPoints =  5           TODO: check what this does
selectionSize = populationSize
numElites = 0

# """--Visualization-----------------------------------------------------------"""
display = True

# """--------------------------------------------------------------------------"""

# this object is used for single-thread evaluations (only pickleable objects can be used in multi-thread)
class ConfigurationEvaluator():
    def __init__(self,rng,aubioparameters):
        self.rng = rng                  # spre inizialized pseudo-random generator (to preserve eventual fixed seed)
        # self.bounder = ec.Bounder(0, 1) # Discrete bounder to boolean values TODO: check the proper Bounder to use
        # self.bounder = ec.DiscreteBounder([0,1]) # Discrete bounder to boolean values
        self.bounder = None
        self.maximize = True           # Flag to define the problem nature
        self.genCount = 0               # generation count

        self.aubioparameters = aubioparameters

    ## Generator method
    #  This generates new individuals
    def generator(self, random, args):
        onset_threshold = self.rng.uniform(MIN_ONSET_THRESH, MAX_ONSET_THRESH)
        silence_threshold = self.rng.uniform(MIN_SILENCE_THRESH, MAX_SILENCE_THRESH)
        return [onset_threshold,silence_threshold]

    ## Evaluator method
    #  This evaluates the fitness of the given individual/s (@candidates)
    def evaluator(self, candidates, args):
        fitness = []
        for candidate in candidates:
            # onset_threshold = candidate[0]
            # silence_threshold = candidate[1]
            # info, metrics = computeLatency.perform_main_analysis(audio_directory = self.aubioparameters['audio_directory'],
            #                                                      aubioonset_command = self.aubioparameters['aubioonset_command'],
            #                                                      onset_method = self.aubioparameters['onset_method'],
            #                                                      buffer_size = self.aubioparameters['buffer_size'],
            #                                                      hop_size = self.aubioparameters['hop_size'],
            #                                                      silence_threshold = silence_threshold,
            #                                                      onset_threshold = onset_threshold,
            #                                                      minimum_inter_onset_interval_s = self.aubioparameters['minimum_inter_onset_interval_s'],
            #                                                      max_onset_difference_s = self.aubioparameters['max_onset_difference_s'],
            #                                                      do_ignore_early_onsets = self.aubioparameters['do_ignore_early_onsets'],
            #                                                      samplerate = self.aubioparameters['samplerate'],
            #                                                      failsafe = self.aubioparameters['failsafe'])
            # if metrics:
            #     fitness_c  = metrics["macroavg_tech_metrics"]["f1-score"]
            # else:
            #     fitness_c = 0
            # fitness.append(fitness_c)
            fitness.append(1)
        # self.genCount += 1
        return fitness

def main(rng, onset_method=default_onset_method, buffer_size=default_buffer_size, display=False):
    aubioparameters = {"audio_directory" : AUDIO_DIRECTORY,
                       "aubioonset_command" : aubioonset_command,
                       "onset_method" : onset_method,
                       "buffer_size" : buffer_size,
                       "hop_size" : HOP_SIZE,
                       "minimum_inter_onset_interval_s" : MIN_IOI,
                       "max_onset_difference_s" : 0.02,
                       "do_ignore_early_onsets" : True,
                       "samplerate" : 48000,
                       "failsafe" : True}
    problem = ConfigurationEvaluator(rng,aubioparameters)

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
                #    inspyred.ec.variators.blend_crossover,
                #    inspyred.ec.variators.heuristic_crossover,
                #    inspyred.ec.variators.laplace_crossover,
                # #    inspyred.ec.variators.simulated_binary_crossover,
                   inspyred.ec.variators.gaussian_mutation,
                #    inspyred.ec.variators.nonuniform_mutation
                   ]

    # replacement operator
    #ea.replacer = inspyred.ec.replacers.truncation_replacement
    #ea.replacer = inspyred.ec.replacers.steady_state_replacement
    #ea.replacer = inspyred.ec.replacers.random_replacement
    # ea.replacer = inspyred.ec.replacers.plus_replacement
    # ea.replacer = inspyred.ec.replacers.comma_replacement     #No elitism, bad in this case
    #ea.replacer = inspyred.ec.replacers.crowding_replacement
    #ea.replacer = inspyred.ec.replacers.simulated_annealing_replacement
    #ea.replacer = inspyred.ec.replacers.nsga_replacement
    #ea.replacer = inspyred.ec.replacers.paes_replacement
    ea.replacer = inspyred.ec.replacers.generational_replacement

    # termination condition
    #ea.terminator = inspyred.ec.terminators.evaluation_termination
    #ea.terminator = inspyred.ec.terminators.no_improvement_termination
    #ea.terminator = inspyred.ec.terminators.diversity_termination
    #ea.terminator = inspyred.ec.terminators.time_termination
    ea.terminator = inspyred.ec.terminators.generation_termination

    # --------------------------------------------------------------------------- #


if __name__ == "__main__":
    if len(sys.argv) == 4 :
        rng = Random(int(sys.argv[1]))
        _method = sys.argv[2]
        _bufsize = int(sys.argv[3])
    else:
        print("Error! Wrong number of arguments")
        print("Usage: "+sys.argv[0]+" <seed> <onset_method> <buffer_size>")
        exit()

    # main(rng,onset_method=_method, buffer_size=_bufsize,display)

    if display:
        pylab.ioff()
        pylab.show()