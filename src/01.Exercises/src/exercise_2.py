from ga import generate_offspring
from pylab import *
from random import Random
import sys

""" 
-------------------------------------------------------------------------
Edit this part to do the exercises

Try different values for either:
    (1) the number of dimensions of the search space
    (2) how close the parent is to the global optimum
    (3) the mutation rate
 If you vary one of the three things, you may want to keep the other two
 at a constant value to better understand the effects (as shown in the
 example below).
"""

# (1) Vary the number of dimensions of the search space
num_vars_1 = 2
num_vars_2 = 2;
num_vars_3 = 2;

# (2) Vary how close the parent is to the optimum
value_1 = 10;
value_2 = 10;
value_3 = 10

# The parents are created for the three conditions
x0_1 = value_1*ones(num_vars_1);
x0_2 = value_2*ones(num_vars_2);
x0_3 = value_3*ones(num_vars_3);

# (3) Vary the standard deviation of the Gaussian mutations
std_dev_1 = 1;
std_dev_2 = 5;
std_dev_3 = 10;

# Number of offspring to be generated
num_offspring = 200;

"""
-------------------------------------------------------------------------
"""

args = {}
if __name__ == "__main__":
    if len(sys.argv) > 1 :
        rng = Random(int(sys.argv[1]))
    else :
        rng = Random()
    
    # Generate offspring for the three conditions
    args["fig_title"] = 'Random sampling (condition 1)'
    parent_fitness_1, offspring_fitness_1 = generate_offspring(rng, x0_1, 
                                                               std_dev_1, 
                                                               num_offspring, 
                                                               False, args);
    args["fig_title"] = 'Random sampling (condition 2)'
    parent_fitness_2, offspring_fitness_2 = generate_offspring(rng, x0_2, 
                                                               std_dev_2, 
                                                               num_offspring, 
                                                               False, args);
    args["fig_title"] = 'Random sampling (condition 3)'
    parent_fitness_3, offspring_fitness_3 = generate_offspring(rng, x0_3,
                                                               std_dev_3, 
                                                               num_offspring, 
                                                               False, args);

    """
    Boxplot of the offspring fitnesses. The fitness of the parent is plotted as
    a dashed, green line.
    """
    fig = figure('Offspring fitness')
    ax = fig.gca()
    ax.boxplot([offspring_fitness_1, offspring_fitness_2, offspring_fitness_3],
               notch=False)
    ax.plot([0.5, 1.5], [parent_fitness_1, parent_fitness_1], 'g--', label='Parent fitness');
    ax.plot([1.5, 2.5], [parent_fitness_2, parent_fitness_2], 'g--');
    ax.plot([2.5, 3.5], [parent_fitness_3, parent_fitness_3], 'g--');
    ax.set_xticklabels(['1', '2', '3'])
    ax.set_xlabel('Condition')
    ax.set_ylabel('Fitness')
    ax.set_ylim(ymin=0)
    ax.legend()
    show()
