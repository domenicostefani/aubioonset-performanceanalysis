from pylab import *
from random import Random
from ga import run_ga
import sys

"""    
-------------------------------------------------------------------------
Edit this part to do the exercises
"""

num_vars = 2 # Number of dimensions of the search space
std_devs = [0.01, 0.1, 1.0] # Standard deviation of the Gaussian mutations
max_generations = 50 # Number of generations of the GA
num_runs = 30 # Number of runs to be done for each stdev

# parameters for the GA
args = {}
args["crossover_rate"] = 0 # Crossover fraction
args["tournament_size"] = 2
args["mutation_rate"] = 1.0 # fraction of loci to perform mutation on
args["num_elites"] = 1 # number of elite individuals to maintain in each gen
args["pop_size"] = 20 # population size
args["pop_init_range"] = [-10, 10] # Range for the initial population
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
    
    # run the GA *num_runs* times for each std_dev and record the best fits
    best_fitnesses = [[run_ga(rng, num_vars=num_vars, 
                              max_generations=max_generations, display=display,
                              gaussian_stdev=std_dev,**args)[1] 
                        for _ in range(num_runs)]
                        for std_dev in std_devs]

    fig = figure('GA (best fitness)')
    ax = fig.gca()
    ax.boxplot(best_fitnesses)
    ax.set_xticklabels(std_devs)
    ax.set_yscale('log')
    ax.set_xlabel('Std. dev.')
    ax.set_ylabel('Best fitness')
    show()
