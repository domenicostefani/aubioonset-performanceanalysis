from pylab import *
import plot_utils
from inspyred import ec, benchmarks

def generator(random, args):
    return asarray([random.uniform(args["pop_init_range"][0],
                                   args["pop_init_range"][1]) 
                    for _ in range(args["num_vars"])])

def run_ga(random, display=False, num_vars=0, problem_class=benchmarks.Sphere, 
           maximize=False, use_bounder=True, **kwargs) :
    
    #create dictionaries to store data about initial population, and lines
    initial_pop_storage = {}
    
    algorithm = ec.EvolutionaryComputation(random)
    algorithm.terminator = ec.terminators.generation_termination
    algorithm.replacer = ec.replacers.generational_replacement    
    algorithm.variator = [ec.variators.uniform_crossover,ec.variators.gaussian_mutation]
    algorithm.selector = ec.selectors.tournament_selection
    
    if display :
        algorithm.observer = plot_utils.plot_observer
    
    kwargs["num_selected"]=kwargs["pop_size"]

    problem = problem_class(num_vars)

    if use_bounder :
        kwargs["bounder"]=problem.bounder
    if "pop_init_range" in kwargs :
        kwargs["generator"]=generator
    else :
        kwargs["generator"]=problem.generator
        
    final_pop = algorithm.evolve(evaluator=problem.evaluator,  
                          maximize=problem.maximize,
                          initial_pop_storage=initial_pop_storage,
                          num_vars=num_vars,
                          **kwargs)

    best_guy = final_pop[0].candidate
    best_fitness = final_pop[0].fitness
    final_pop_fitnesses = asarray([guy.fitness for guy in final_pop])
    final_pop_candidates = asarray([guy.candidate for guy in final_pop])

    return best_guy, best_fitness, final_pop
