#!/usr/bin/env python3
import argparse
import json


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--distance-matrix-sample-tree', type=str, required=True)
    arg_parser.add_argument('--distance-matrix-sample-sample', type=str, required=True)
    arg_parser.add_argument('--distance-threshold', type=str)
    args = arg_parser.parse_args()

    with open(args.distance_matrix_sample_tree) as f:
        first_line = next(f)
        tree_leaf_list = first_line.rstrip().split('\t')
        sample_nearest_leaf = _get_sample_nearest_leaf(tree_leaf_list, f)

    with open(args.distance_matrix, "r") as f:
        first_line = next(f)
        target_list = first_line.rstrip().split('\t')
        _get_nearest_neighbours(target_list, sample_nearest_leaf, f, int(args.distance_threshold))


def _get_sample_nearest_leaf(tree_nodes, fd):
    _sample_nearest_leaf = {}
    for line in fd:
        distances = line.rstrip().split('\t')
        nearest_distance = int(distances[1])
        sample = tree_nodes[0].strip()
        nearest_leaf = tree_nodes[1]
        for i in range(2, len(distances)):
            if nearest_distance > int(distances[i]):
                nearest_distance = int(distances[i])
                nearest_leaf = tree_nodes[i]
        _sample_nearest_leaf[sample] = nearest_leaf.strip()

    return _sample_nearest_leaf


def _get_nearest_neighbours(target_samples, sample_nearest_leaf, fd, threshold):
    for line in fd:
        distances = line.rstrip().split('\t')
        data = []
        source_sample = distances[0].strip()
        for i in range(1, len(distances)):
            target_sample = target_samples[i].strip()
            if threshold >= int(distances[i]) and target_sample != source_sample:
                data.append({
                    "experiment_id": target_sample,
                    "leaf_id": sample_nearest_leaf[target_sample],
                    "distance": int(distances[i])
                })
        print('{}\t{}'.format(source_sample, json.dumps(data)))


if __name__ == "__main__":
    main()
