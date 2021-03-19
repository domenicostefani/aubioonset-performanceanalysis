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

import pylab
from random import Random
import inspyred
import sys
import computeLatency
import os

PARALLEL = False
RESFOLDER="evolutionaryOptimizerResults/"

# """--Parameters for aubio ---------------------------------------------------"""
AUDIO_DIRECTORY = "audiofiles"
AUBIOONSET_COMMAND = "aubioonset"
default_onset_method = "hfc"
default_buffer_size = 64
HOP_SIZE = 64
MIN_IOI = 0.02

MIN_ONSET_THRESH   = 0.1
MAX_ONSET_THRESH   = 3.6
MIN_SILENCE_THRESH = -60
MAX_SILENCE_THRESH = -30

# """--Parameters for the EC---------------------------------------------------"""

# THESE WORK (with arithmetic_crossover & gaussian_mutation) but not optimal
# populationSize = 6
# numberOfGenerations = 30
# numberOfEvaluations = 2500                    # used with evaluation_termination
# tournamentSize = 3
# mutationRate = 0.7
# gaussianMean = 0
# gaussianStdev = 1.0
# crossoverRate = 0.9
# selectionSize = populationSize
# numElites = 0


populationSize = 10
numberOfGenerations = 30
numberOfEvaluations = 400                    # used with evaluation_termination
tournamentSize = 4
mutationRate = 0.7
gaussianMean = 0
gaussianStdev = 3.0
crossoverRate = 0.7
selectionSize = populationSize
numElites = 1

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
        # self.genCount = 0               # generation count

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
            onset_threshold = candidate[0]
            silence_threshold = candidate[1]
            info, metrics = computeLatency.perform_main_analysis(audio_directory = self.aubioparameters['audio_directory'],
                                                                 aubioonset_command = self.aubioparameters['aubioonset_command'],
                                                                 onset_method = self.aubioparameters['onset_method'],
                                                                 buffer_size = self.aubioparameters['buffer_size'],
                                                                 hop_size = self.aubioparameters['hop_size'],
                                                                 silence_threshold = silence_threshold,
                                                                 onset_threshold = onset_threshold,
                                                                 minimum_inter_onset_interval_s = self.aubioparameters['minimum_inter_onset_interval_s'],
                                                                 max_onset_difference_s = self.aubioparameters['max_onset_difference_s'],
                                                                 do_ignore_early_onsets = self.aubioparameters['do_ignore_early_onsets'],
                                                                 samplerate = self.aubioparameters['samplerate'],
                                                                 failsafe = self.aubioparameters['failsafe'],
                                                                 save_results=False)
            # info, metrics = computeLatency.perform_main_analysis(audio_directory = "audiofiles", #self.aubioparameters['audio_directory'],
            #                                                      aubioonset_command = "aubioonset", #self.aubioparameters['aubioonset_command'],
            #                                                      onset_method = "hfc", #self.aubioparameters['onset_method'],
            #                                                      buffer_size = 64, #self.aubioparameters['buffer_size'],
            #                                                      hop_size = 64, #self.aubioparameters['hop_size'],
            #                                                      onset_threshold = onset_threshold, #onset_threshold,
            #                                                      silence_threshold = silence_threshold, #silence_threshold,
            #                                                      minimum_inter_onset_interval_s = 0.02, #self.aubioparameters['minimum_inter_onset_interval_s'],
            #                                                      max_onset_difference_s = 0.02, #self.aubioparameters['max_onset_difference_s'],
            #                                                      do_ignore_early_onsets = True, #self.aubioparameters['do_ignore_early_onsets'],
            #                                                      samplerate = 48000, #self.aubioparameters['samplerate'],
            #                                                      failsafe = True, #self.aubioparameters['failsafe'],
            #                                                      save_results = False)
            if metrics:
                fitness_c  = metrics["macroavg_tech_metrics"]["f1-score"]
            else:
                fitness_c = 0
            fitness.append(fitness_c)

            # For testing purpose I'll leave the next line here
            # fitness.append(self.rng.random())
            # import time
            # time.sleep(3)
        # self.genCount += 1
        return fitness

def main(rng, onset_method=default_onset_method, buffer_size=default_buffer_size, display=False, runstring=""):

    aubioonset_command = AUBIOONSET_COMMAND
    real_onset_method = onset_method
    if onset_method == "mkl(noaw)":
        print("Disabling whitening")
        onset_method = "mkl"
        aubioonset_command = "./utility_scripts/customAubio/aubioonset-mkl-nowhitening"
    aubioparameters = {"audio_directory" : AUDIO_DIRECTORY,
                       "aubioonset_command" : aubioonset_command,
                       "onset_method" : onset_method,
                       "buffer_size" : buffer_size,
                       "hop_size" : HOP_SIZE,
                       "minimum_inter_onset_interval_s" : MIN_IOI,
                       "max_onset_difference_s" : 0.02,
                       "do_ignore_early_onsets" : True,
                       "samplerate" : 48000,
                       "failsafe" : True,
                       "real_onset_method":real_onset_method}
    problem = ConfigurationEvaluator(rng,aubioparameters)

    # --------------------------------------------------------------------------- #

    # the evolutionary algorithm (EvolutionaryComputation is a fully configurable evolutionary algorithm)
    # standard GA, ES, SA, DE, EDA, PAES, NSGA2, PSO and ACO are also available
    ea = inspyred.ec.EvolutionaryComputation(rng)

    # observers: provide various logging features
    # if display:
    ea.observer = [#inspyred.ec.observers.stats_observer,
                   inspyred.ec.observers.file_observer,
                   inspyred.ec.observers.plot_observer
                    #inspyred.ec.observers.best_observer,
                    #inspyred.ec.observers.population_observer
                  ]


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
                   inspyred.ec.variators.laplace_crossover,
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
    _statfile = open(RESFOLDER+"inspyred-statistics-"+runstring+".txt","a") 
    _indfile = open(RESFOLDER+"inspyred-individuals-"+runstring+".txt","a")

                        #   Parameters for multiprocessing (Currently not working)
                        # 
                        #   evaluator=inspyred.ec.evaluators.parallel_evaluation_mp,
                        #   mp_evaluator=problem.evaluator, 
                        #   mp_num_cpus=1,

                        #   Parameters for Parallel (Currently TODO: test)

                        # 
    if PARALLEL:
        final_pop = ea.evolve(generator=problem.generator,
                              evaluator=inspyred.ec.evaluators.parallel_evaluation_pp,
                              pp_evaluator=problem.evaluator, 
                              pp_dependencies=(computeLatency.perform_main_analysis,),
                              pp_modules=("computeLatency",),
                              pp_nprocs=12,
                              bounder=problem.bounder,
                              maximize=problem.maximize,
                              pop_size=populationSize,
                              max_generations=numberOfGenerations,
                              #max_evaluations=numberOfEvaluations,
                              tournament_size=tournamentSize,
                              mutation_rate=mutationRate,
                              gaussian_mean=gaussianMean,
                              gaussian_stdev=gaussianStdev,
                              crossover_rate=crossoverRate,
                              num_selected=selectionSize,
                              num_elites=numElites,
                              statistics_file = _statfile,
                              individuals_file =_indfile)
    else:
        final_pop = ea.evolve(generator=problem.generator,
                              evaluator=problem.evaluator, 
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
                              num_selected=selectionSize,
                              num_elites=numElites,
                              statistics_file = _statfile,
                              individuals_file =_indfile)

    _statfile.close()
    _indfile.close()

    if display:
        final_pop.sort(reverse=True)
        print(final_pop[0])
        best_onset_threshold = final_pop[0].candidate[0]
        best_silence_threshold = final_pop[0].candidate[1]


        info, metrics = computeLatency.perform_main_analysis(audio_directory = aubioparameters['audio_directory'],
                                                            aubioonset_command = aubioparameters['aubioonset_command'],
                                                            onset_method = aubioparameters['onset_method'],
                                                            buffer_size = aubioparameters['buffer_size'],
                                                            hop_size = aubioparameters['hop_size'],
                                                            onset_threshold = best_onset_threshold,
                                                            silence_threshold = best_silence_threshold,
                                                            minimum_inter_onset_interval_s = aubioparameters['minimum_inter_onset_interval_s'],
                                                            max_onset_difference_s = aubioparameters['max_onset_difference_s'],
                                                            do_ignore_early_onsets = aubioparameters['do_ignore_early_onsets'],
                                                            samplerate = aubioparameters['samplerate'],
                                                            failsafe = aubioparameters['failsafe'])
        res = computeLatency.create_string(info = info,
                                           metrics = metrics,
                                           use_oldformat=False,
                                           do_copy = True,
                                           failsafe = True)
        print(res)

        resfile = open(RESFOLDER+"best-"+aubioparameters['real_onset_method'] +"-"+str(aubioparameters['buffer_size'])+"res.txt","w")
        resfile.write(res+"\n")
        resfile.close()

if __name__ == "__main__":
    if len(sys.argv) == 4 :
        rng = Random(int(sys.argv[1]))
        _method = sys.argv[2]
        _bufsize = int(sys.argv[3])
    else:
        print("Error! Wrong number of arguments")
        print("Usage: "+sys.argv[0]+" <seed> <onset_method> <buffer_size>")
        exit()

    os.system("mkdir -p "+RESFOLDER)

    import time
    runstring = str(_method)+"-"+str(_bufsize)+"-"+time.strftime("%Y%m%d-%H%M%S")

    import logging
    logger = logging.getLogger('inspyred.ec')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('inspyred.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    main(rng,onset_method=_method, buffer_size=_bufsize,display=display, runstring=runstring)

    if display:
        pylab.ioff()
        print(runstring)
        pylab.savefig(RESFOLDER+runstring)
