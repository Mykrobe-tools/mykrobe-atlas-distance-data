#!/usr/bin/env python3
import argparse

import numpy as np


def _dist_two_samples(genotype_calls, i, j):
    return np.sum(
            genotype_calls[i] * genotype_calls[j] * (genotype_calls[i] - genotype_calls[j]) != 0
        )


def _calculate_distance_matrix(genotype_calls):
    num_rows = len(genotype_calls)
    num_cols = num_rows
    distance_matrix = [[0] * num_cols for _ in range(num_rows)]

    for row in range(num_rows):
        for col in range(row+1, num_cols):
            distance = _dist_two_samples(genotype_calls, row, col)
            if distance != 0:
                distance_matrix[row][col] = distance
                distance_matrix[col][row] = distance

    return distance_matrix


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--genotype-calls', type=str)
    arg_parser.add_argument('--out-distances', type=str)
    args = arg_parser.parse_args()

    genotype_calls = []
    with open(args.genotype_calls, "r") as f:
        for line in f:
            data = []
            for c in line.rstrip('\n'):
                data.append(int(c))
            genotype_calls.append(np.array(data, dtype=np.uint16))

    distance_matrix = _calculate_distance_matrix(genotype_calls)

    with open(args.out_distances, "w") as output:
        for row in distance_matrix:
            print(",".join([str(d) for d in row]), file=output)

    print("complete!")


if __name__ == "__main__":
    main()
