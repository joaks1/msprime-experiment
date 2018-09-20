#! /usr/bin/env python

import sys
import os
import datetime

import msprime


def main():
    number_of_replicates = 20000
    number_of_fragments = 2 
    sample_size = 1
    generations_since_fragmentation = 20000.0
    fragment_population_size = 10000.0 
    ancestral_population_size = 100000.0
    mutation_rate = 1e-6
    migration_rate = 0.0

    seed = 12345
    
    population_configs = []
    population_splits = []
    fragmentation_size_change = None
    migration_rate_matrix = []

    for i in range(number_of_fragments):
        population_configs.append(
                msprime.PopulationConfiguration(
                    sample_size = sample_size,
                    initial_size = fragment_population_size,
                    growth_rate = 0.0))
        if i > 0:
            population_splits.append(
                    msprime.MassMigration(
                        time = generations_since_fragmentation,
                        source = i,
                        destination = 0,
                        proportion = 1.0))
    fragmentation_size_change = msprime.PopulationParametersChange(
            time = generations_since_fragmentation,
            initial_size = ancestral_population_size,
            growth_rate = 0.0,
            population_id = 0)
    migration_rate_matrix = [
            [0.0 for i in range(number_of_fragments)
                    ] for j in range(number_of_fragments)
            ]
    for i in range(number_of_fragments):
        for j in range(number_of_fragments):
            if i != j:
                migration_rate_matrix[i][j] = migration_rate

    start_time = datetime.datetime.now()
    trees = msprime.simulate(
            sample_size = None, # will be determined from pop configs
            Ne = 1.0, # reference effective pop size,
            length = 1,
            recombination_rate = 0.0,
            mutation_rate = mutation_rate,
            population_configurations = population_configs,
            migration_matrix = migration_rate_matrix,
            demographic_events = population_splits + [fragmentation_size_change],
            random_seed = seed,
            num_replicates = number_of_replicates)
    mid_time = datetime.datetime.now()
    # pis = [t.get_pairwise_diversity() for t in trees]
    ntrees = 0
    for t in trees:
        ntrees += 1
    stop_time = datetime.datetime.now()
    sys.stdout.write('ntrees = {0}\n'.format(ntrees))
    sys.stdout.write('sim time = {0}\n'.format(str(mid_time - start_time)))
    sys.stdout.write('iter time = {0}\n'.format(str(stop_time - mid_time)))
    
if __name__ == '__main__':
    main()
