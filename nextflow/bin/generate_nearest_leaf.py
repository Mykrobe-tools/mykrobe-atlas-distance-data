#!/usr/bin/env python3
import argparse
import json


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--distance-matrix-sample-tree', type=str, required=True)
    args = arg_parser.parse_args()

    with open(args.distance_matrix_sample_tree, "r") as f:
        first_line = next(f)
        target_list = first_line.rstrip().split('\t')
        _get_nearest_leaves(target_list, f)


def _get_nearest_leaves(tree_nodes, fd):
    for line in fd:
        distances = line.rstrip().split('\t')
        nearest_distance = int(distances[1])
        nearest_leaf = tree_nodes[1]
        for i in range(2, len(distances)):
            if nearest_distance > int(distances[i]):
                nearest_distance = int(distances[i])
                nearest_leaf = tree_nodes[i]
        data = {
            "leaf_id": nearest_leaf.strip(),
            "distance": nearest_distance
        }
        print('{}\t{}'.format(distances[0], json.dumps(data)))


if __name__ == "__main__":
    main()
