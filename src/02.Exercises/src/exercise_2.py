from pylab import *
from random import Random
from ga import run_ga
import sys

"""   
-------------------------------------------------------------------------
Edit this part to do the exercises
"""

crossover_rates = [0, 0.12, 0.25, 0.5, 0.75] # Crossover fractions

# parameters for the GA
args = {}
args["num_vars"] = 10 # Number of dimensions of the search space
args["gaussian_stdev"] = 0.5 # Standard deviation of the Gaussian mutations
args["mutation_rate"] = 0.5 # fraction of loci to perform mutation on
args["tournament_size"] = 2 
args["num_elites"] = 1 # number of elite individuals to maintain in each gen
args["pop_size"] = 20 # population size
args["pop_init_range"] = [-10, 10] # Range for the initial population
args["max_generations"] = 50 # Number of generations of the GA

num_runs = 30 # Number of runs to be done for each condition
display = False # Plot initial and final populations

"""
-------------------------------------------------------------------------
"""

args["fig_title"] = 'GA'

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        rng = Random(int(sys.argv[1]))
    else :
        rng = Random()
    
    # run the GA *num_runs* times for each crossover fraction 
    # and record the best fits 
    best_fitnesses = [[run_ga(rng, display=display, 
                              crossover_rate=crossover_rate,**args)[1] 
                        for _ in range(num_runs)]
                        for crossover_rate in crossover_rates]

    fig = figure('GA (best fitness)')
    ax = fig.gca()
    ax.boxplot(best_fitnesses,notch=False)
    ax.set_xticklabels(crossover_rates)
    ax.set_xlabel('Crossover rate')
    ax.set_ylabel('Best fitness')
    show()
