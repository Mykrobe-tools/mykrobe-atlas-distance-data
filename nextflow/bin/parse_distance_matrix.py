#!/usr/bin/env python3
import argparse
import json


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--distance-matrix', type=str, required=True)
    arg_parser.add_argument('--distance-threshold', type=str)
    args = arg_parser.parse_args()

    with open(args.distance_matrix, "r") as f:
        first_line = next(f)
        target_list = first_line.rstrip().split('\t')
        if args.distance_threshold is not None:
            _get_nearest_leaves(target_list, f)


def _get_nearest_leaves(tree_nodes, fd):
    for line in f:
        distances = line.rstrip().split('\t')
        min = distances[1]
        nearest_leaf = tree_nodes[1]
        for i in range(2, len(distances)):
            if min > distances[i]:
                min = distances[i]
                nearest_leaf = tree_nodes[i]
        data = {
            "leaf_id": nearest_leaf,
            "distance": min
        }
        print('{}\t{}'.format(distances[0], json.dumps(data)))


if __name__ == "__main__":
    main()
