import random
from collections import namedtuple
import time

start = time.time()


class GeneticAlgorithm:

    def __init__(self, items, len_genome=10, len_population=100, n_generations=50, volume_limit=200):
        self.len_genome = len_genome
        self.len_population = len_population
        self.n_generations = n_generations
        self.volume_limit = volume_limit

        if not items:
            raise Exception("No item in list!")
        else:
            self.items = items

    def generate_genome(self):
        return random.choices([0, 1], k=self.len_genome)

    def generate_population(self):
        return [self.generate_genome() for i in range(self.len_population)]

    def fitness(self, genome):
        fitness_score = 0
        total_volume = 0
        for ind, gene in enumerate(genome):
            if gene == 0:
                continue
            fitness_score += self.items[ind].value
            total_volume += self.items[ind].volume
            if total_volume > self.volume_limit:
                fitness_score = 0
                break
        return fitness_score

    def selection(self, fit_population):
        return random.choices(fit_population, weights=[p[1] for p in fit_population], k=2)

    def single_point_crossover(self, selections, n_genes_swap=3):
        parent_1 = selections[0]
        parent_2 = selections[1]
        child_1 = parent_1[:-n_genes_swap] + parent_2[-n_genes_swap:]
        child_2 = parent_2[:-n_genes_swap] + parent_1[-n_genes_swap:]
        return [child_1, child_2]

    def mutation(self, genome):
        index = random.randint(0, self.len_genome - 1)
        genome[index] = abs(genome[index] - 1)
        return genome

    def elitism(self, population, fit_population, n_transfer=5):
        next_gen = []
        for i in range(n_transfer):
            next_gen.append(population[fit_population[i][0]])
        return next_gen

    def run(self):
        population = self.generate_population()

        for generation in range(self.n_generations):
            fit_population = []
            for pop_index, genome in enumerate(population):
                fit_population.append([pop_index, self.fitness(genome)])

            fit_population = sorted(fit_population, key=lambda x: x[1], reverse=True)
            next_generation = self.elitism(population, fit_population)
            while len(next_generation) <= self.len_population:
                selected = self.selection(fit_population)
                selected = [population[selected[0][0]], population[selected[1][0]]]
                children = self.single_point_crossover(selected)

                for c in range(len(children)):  # mutate children
                    children[c] = self.mutation(children[c])

                next_generation += children

            if not generation == self.n_generations - 1:  # do not update population in last loop.
                population = next_generation

        return population[fit_population[0][0]]

    def print_result(self, genome):
        total_value = 0
        total_volume = 0
        for ind, gene in enumerate(genome):
            if gene == 1:
                total_value += self.items[ind].value
                total_volume += self.items[ind].volume
                print(f"{self.items[ind].name} --> value: {self.items[ind].value} | volume: {self.items[ind].volume}")

        print(f"\nTotal Value: {total_value}\nTotal Volume: {total_volume}")


if __name__ == "__main__":

    Item = namedtuple("Item", ["name", "value", "volume"])

    book = Item('Book', 50, 80)
    phone = Item('Phone', 100, 10)
    flip_flop = Item('Flip Flop', 30, 30)
    towel = Item('Towel', 30, 40)
    umbrella = Item('Umbrella', 15, 90)
    swimsuit = Item('Swimsuit', 90, 50)
    jacket = Item('Jacket', 10, 150)
    sunglasses = Item('Sunglasses', 70, 40)
    laptop = Item('Laptop', 50, 100)
    city_map = Item('City Map', 10, 5)

    items = [book, phone, flip_flop, towel, umbrella, swimsuit, jacket, sunglasses, laptop, city_map]

    model = GeneticAlgorithm(items=items)
    solution = model.run()
    model.print_result(solution)

    finish = time.time()

    print("\nTotal Time: ", finish - start)
