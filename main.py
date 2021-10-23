import argparse
import csv
from os import listdir
from os.path import isfile, join
import numpy as np
import random
from collections import defaultdict
from itertools import combinations


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    pages = {}
    filenames = get_file_names(args.dir)
    same_pairs = {}
    mixed_pairs = defaultdict(set)
    for filename in filenames:
        file_path = join(args.dir, filename)
        lines_num = get_line_numbers(file_path)
        pages[filename.split(".")[0]] = lines_num

    for page_name, page_lines in pages.items():
        same_pairs[page_name] = generate_pairs(page_lines)

    key_pairs = get_keys_pages(pages)
    for pair in key_pairs:
        first_lines = pages[pair[0]]
        second_lines = pages[pair[1]]
        mixed_pairs[pair] = generate_mix_pairs(first_lines, second_lines, min(first_lines, second_lines))

    store_results(same_pairs, mixed_pairs)


def get_keys_pages(pages):
    pages = list(pages)
    return [(x, y) for idx, x in enumerate(pages) for y in pages[idx + 1:]]


def generate_pairs(num_lines):
    line_numbers = list(range(0, num_lines))
    pairs_iterator = combinations(line_numbers, 2)
    pairs = set()
    for pair in pairs_iterator:
        pairs.add(pair)
    return pairs


def generate_mix_pairs(first_lines, second_lines, num_of_pairs):
    pairs = set()
    for i in range(num_of_pairs):
        first_index = random.randint(0, first_lines - 1)
        second_index = random.randint(0, second_lines - 1)
        pairs.add((first_index, second_index))
    return pairs


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help="The directory of the csvs")
    return parser


def get_file_names(dir_path):
    return [f for f in listdir(dir_path) if isfile(join(dir_path, f))]


def get_line_numbers(file_path):
    file = open(file_path)
    reader = csv.reader(file)
    lines = len(list(reader))
    return lines


def store_results(same_pairs, mixed_pairs):
    with open("match.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for page, pairs in same_pairs.items():
            for pair in pairs:
                row = [page, pair[0], pair[1]]
                writer.writerow(row)

    with open("mismatch.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for pages, pairs in mixed_pairs.items():
            for pair in pairs:
                row = [pages[0], pages[1], pair[0], pair[1]]
                writer.writerow(row)


if __name__ == '__main__':
    main()
