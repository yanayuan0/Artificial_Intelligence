from ga import *

class SumGA(GeneticAlgorithm):
    """
    An example of using the GeneticAlgorithm class to solve a particular
    problem, in this case finding strings with the maximum number of 1's.
    """
    def fitness(self, chromosome):
        """
        Fitness is the sum of the bits.
        """
        return sum(chromosome)

    def isDone(self):
        """
        Stop when the fitness of the the best member of the current
        population is equal to the maximum fitness.
        """
        return self.fitness(self.bestEver) == self.length


def main():
    # # use this main program to incrementally test the GeneticAlgorithm
    # # class as you implement it
    # ga = SumGA(10, 20, verbose=True)

    # #call method we implemented
    # ga.initializePopulation()
    # ga.evaluatePopulation()
    # for i, pop in enumerate(ga.population):
    #     print("population: " + str(pop))
    #     print("fitness: " + str(ga.scores[i]))
    
    # #best ever fitness and candidae solution
    # print("best ever fitness: " + str(ga.bestEverScore))
    # print("best candidate: " + str(ga.bestEver))

    # #test selection
    # newFitness = 0
    # for i in range(ga.popSize):
    #     newFitness += sum(ga.selection())
    # print("new total fitness: " + str(newFitness))
    # print("old total fitness: " + str(ga.totalFitness))

    # #test crossover
    # parent1 = ga.selection()
    # parent2 = ga.selection()
    # print(parent1)
    # print(parent2)
    # ga.crossover(parent1, parent2)

    # #test mutation
    # newFitness = 0
    # for i in range(ga.popSize):
    #     chro = ga.selection()
    #     ga.mutation(chro)
    #     newFitness += sum(chro)
    # print("new total fitness: " + str(newFitness))
    # print("old total fitness: " + str(ga.totalFitness))   

    # #test oneGeneration
    # ga.oneGeneration()
    # ga.evaluatePopulation()
    # print("avg fitness list" + str(ga.avgList))

    #test evolve
    # Chromosomes of length 20, population of size 50
    ga = SumGA(20, 50)
    # Evolve for 100 generations
    # High prob of crossover, low prob of mutation
    bestFound = ga.evolve(100, 0.6, 0.01)
    print(bestFound)
    ga.plotStats("Sum GA")

if __name__ == '__main__':
    main()
