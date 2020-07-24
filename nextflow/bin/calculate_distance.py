#!/usr/bin/env python3
import argparse

import numpy as np


def _dist_two_samples(genotype_calls_1, genotype_calls_2):
    return np.sum(
            genotype_calls_1 * genotype_calls_2 * (genotype_calls_1 - genotype_calls_2) != 0
        )


def _calculate_1xn_distance(genotype_calls_1, genotype_calls_n):
    n = len(genotype_calls_n)
    distance_row = [0] * n

    for index in range(n):
        distance = _dist_two_samples(genotype_calls_1, genotype_calls_n[index])
        if distance != 0:
            distance_row[index] = distance

    return distance_row


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--genotype-calls1', type=str, required=True, help='genotype calls for samples in rows')
    arg_parser.add_argument('--genotype-calls2', type=str, required=True, help='genotype calls for samples in columns')
    arg_parser.add_argument('--out-distances', type=str, required=True, help='output file to store distance matrix')
    args = arg_parser.parse_args()

    genotype_calls2 = []
    samples_on_column = []
    with open(args.genotype_calls2, "r") as f:
        for line in f:
            line = line.rstrip('\n')
            sample, genotype_calls = line.split('\t', maxsplit=1)
            samples_on_column.append(sample)
            data = []
            for c in genotype_calls:
                data.append(int(c))
            genotype_calls2.append(np.array(data, dtype=np.uint16))

    with open(args.out_distances, "w") as output:
        print("", "\t", "\t".join(samples_on_column), file=output)
        with open(args.genotype_calls1, "r") as f:
            for line in f:
                line = line.rstrip('\n')
                sample, genotype_calls = line.split('\t', maxsplit=1)
                data = []
                for c in genotype_calls:
                    data.append(int(c))
                genotype_calls1 = np.array(data, dtype=np.uint16)

                distance_row = _calculate_1xn_distance(genotype_calls1, genotype_calls2)
                print(sample, "\t", "\t".join([str(d) for d in distance_row]), file=output)

    print("complete!")


if __name__ == "__main__":
    main()
