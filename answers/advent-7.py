import sys
import re
from collections import namedtuple
from typing import List, Dict

class Bag():
    '''
    class to hold the 'contains' relationship for a particular bag type
    '''

    BagRule = namedtuple('BagRule', ["count", "name"])
    name_re = re.compile(r'(\w+ \w+) \w+')
    rule_re = re.compile(r'\s*(\d+) (\w+ \w+) \w+\.?|(no other bags\.)$')

    def __init__(self, rule: str):
        self.rule_spec = rule

    @property
    def rule_spec(self):
        return self.__rule_spec

    @rule_spec.setter
    def rule_spec(self, rule: str):
        self.__rule_spec = rule
        self.__rules = []
        name_part, rules = self.__rule_spec.split(" contain ")
        m = Bag.name_re.match(name_part)
        self.name = m.group(1)
        rules = rules.split(", ")
        for rule in rules:
            #print(rule)
            m = Bag.rule_re.match(rule)
            #print(m)
            if m.group(3) == "no other bags.":
                continue
            self.__rules.append(Bag.BagRule(int(m.group(1)), m.group(2)))

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def rules(self):
        return self.__rules

    def contains(self, bag_name) -> bool:
        for rule in self.__rules:
            if rule.name == bag_name:
                return True
        return False

    def __hash__(self):
        return self.name

    def __eq__(self, other_bag) -> bool:
        return other_bag.name == self.name

    def __repr__(self) -> str:
        return self.__name

def get_bags_containing(bag_list: List, containd_bag_name: str) -> List[Bag]:
    result = []
    for bag in bag_list:
        if bag.contains(containd_bag_name):
            result.append(bag)
    return result

def get_nested_sum(bag_index: Dict[str, Bag], bag_name: str, factor: int) -> int:
    running_sum = 0
    for rule in bag_index[bag_name].rules:
        running_sum += rule.count * factor
        running_sum += get_nested_sum(bag_index, rule.name, rule.count*factor)
    return running_sum

def main():
    if len(sys.argv) != 2:
        print("Single input filename required, no more, no less.")
        sys.exit(1)
    bags = []
    with open(sys.argv[1], 'r') as infile:
        for rule_line in infile:
            bags.append(Bag(rule_line))
    contains_shinygold = get_bags_containing(bags, "shiny gold")
    contains_shinygold_set = set([ bag.name for bag in contains_shinygold ])
    while len(contains_shinygold) != 0:
        next_bags = []
        for bag in contains_shinygold:
            next_bags += get_bags_containing(bags, bag.name)
        for bag in next_bags:
            contains_shinygold_set.add(bag.name)
        contains_shinygold = next_bags
    print("Found {} total bags that could contain shiny gold".format(len(contains_shinygold_set)))
    bagname_index = { b.name:b for b in bags }
    contained_bags_sum = get_nested_sum(bagname_index, "shiny gold", 1)
    print("shiny gold bag has {} nested bags".format(contained_bags_sum))


if __name__ == '__main__':
    main()