import sys
from functools import reduce
from typing import List

def get_groups(infile: str):
    with open(infile, 'r') as declarations:
        lines = [ line for line in declarations ]
        onebigstring = ''.join(lines)
        groups_as_bigstrings = onebigstring.split("\n\n")
        return [ group.split() for group in groups_as_bigstrings ]

def get_group_set1(group: List):
    group_sets = []
    for single_yes_answers in group:
        group_sets.append(set([ c for c in single_yes_answers ]))
    result = set()
    for answer_set in group_sets:
        result = result.union(answer_set)
    return result

def get_group_set2(group: List):
    group_sets = []
    for single_yes_answers in group:
        group_sets.append(set([c for c in single_yes_answers]))
    result = set(group_sets.pop())
    for answer_set in group_sets:
        result = result.intersection(answer_set)
    return result

def get_yesanswer_sets(groups_as_list_of_lists: List, set_fetch_function):
    yes_sets = []
    for group in groups_as_list_of_lists:
        yes_sets.append(set_fetch_function(group))
    return yes_sets


def main():
    if len(sys.argv) != 2:
        print("Single input filename required, no more, no less.")
        sys.exit(1)
    groups = get_groups(sys.argv[1])
    yes_sets1 = get_yesanswer_sets(groups, get_group_set1)
    answers_sum = reduce(lambda a, b: a + b, [len(st) for st in yes_sets1])
    print("sum of yes answers is {}".format(answers_sum))
    yes_sets2 = get_yesanswer_sets(groups, get_group_set2)
    answers_sum = reduce(lambda a, b: a + b, [len(st) for st in yes_sets2])
    print("sum of COMMON yes answers is {}".format(answers_sum))


if __name__ == '__main__':
    main()
