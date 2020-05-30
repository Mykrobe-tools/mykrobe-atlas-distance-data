#!/usr/bin/env python3
import argparse
import json


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--bigsi-result', type=str)
    arg_parser.add_argument('--sample-list', type=str)
    args = arg_parser.parse_args()

    with open(args.sample_list, "r") as f:
        samples = [line.rstrip('\n') for line in f]

    matrix = _call_genotypes(args.bigsi_result, samples)
    for s in samples:
        print(''.join(str(x) for x in matrix[s]))


def _call_genotypes(bigsi_result, samples):
    num_probes = int(_count_line_number(bigsi_result) / 2)
    matrix = _initialise_matrix(samples, num_probes)
    with open(bigsi_result, "r") as json_file:
        for i in range(num_probes):
            ref_probe_result = json.loads(json_file.readline().rstrip('\n'))
            for r in ref_probe_result["results"]:
                matrix[r["sample_name"]][i] += 1
            alt_probe_result = json.loads(json_file.readline().rstrip('\n'))
            for r in alt_probe_result["results"]:
                matrix[r["sample_name"]][i] += 2
    return matrix


def _count_line_number(filename):
    with open(filename, "r") as f:
        return sum(1 for _ in f)


def _initialise_matrix(samples, num_cols):
    return {s: [0] * num_cols for s in samples}


if __name__ == "__main__":
    main()
