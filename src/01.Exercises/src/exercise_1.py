from pylab import *
from ga import generate_offspring
from random import Random
import sys
matplotlib.use('TKAgg',force=True)


"""
-------------------------------------------------------------------------
Edit this part to do the exercises

Choose the parent x0 that will be mutated. It can have an arbitrary 
number of dimensions, but plotting of the fitness landscape is only 
possible for the 1D or 2D case.
"""

#x0 = [10] # 1 parameter
x0 = [10, 10]; # 2 parameters
# x0 = 10*ones(50); # 50 parameters

# Set the standard deviation of the Gaussian mutations
std_dev = 10

# Set number of offspring to be generated
num_offspring = 25

"""
-------------------------------------------------------------------------
"""

args = {}
args["fig_title"] = 'Random sampling'

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        rng = Random(int(sys.argv[1]))
    else :
        rng = Random()
    plot_fitness_landscape = True # Set to False to disable the plots
    parent_fitness, offspring_fitnesses = generate_offspring(rng, x0, std_dev,
                                                    num_offspring, 
                                                    plot_fitness_landscape,
                                                    args)
    
    """
    Boxplot of the offspring fitnesses. The fitness of the parent is plotted as
    a dashed, green line.
    """
    fig = figure('Offspring fitness')
    ax = fig.gca()
    ax.boxplot(offspring_fitnesses)
    ax.set_xticklabels([])
    ax.plot([0,2], [parent_fitness,parent_fitness], 'g--', label='Parent fitness');
    ax.set_ylabel('Fitness')
    ax.set_ylim(ymin=0)
    ax.legend()
    show()
