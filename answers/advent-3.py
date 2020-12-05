import sys
from typing import List, Tuple
from math import prod

def get_map_from_file(filename):
    with open(filename, 'r') as infile:
        return [ line for line in infile ]

def ride_some_slope(map_of_trees: List, slope: Tuple ):
    y_repeat_interval = len(map_of_trees[0]) - 1
    toboggan_x = 0
    toboggan_y = 0
    trees = 0
    while toboggan_x < len(map_of_trees):
        #print("x:{} y:{}".format(toboggan_x, toboggan_y))
        if map_of_trees[toboggan_x][toboggan_y] == '#':
            trees += 1
            #print("trees: {}".format(trees))
        toboggan_x += slope[0]
        toboggan_y = (toboggan_y + slope[1]) % y_repeat_interval
    return trees



def main():
    if len(sys.argv) < 2:
        print("provide advent3 input")
        sys.exit(1)
    map_to_airport = get_map_from_file(sys.argv[1])
    #print(map_to_airport)
    slopes = [
        (1,1),
        (1,3),
        (1,5),
        (1,7),
        (2,1)
    ]
    trees_hit = []
    for slope in slopes:
        num_trees = ride_some_slope(map_to_airport, slope)
        trees_hit.append(num_trees)
        print("we hit {} trees with a right-{} down-{} slope".format(num_trees, slope[1], slope[0]))
    print("product of the hit trees is {}".format(prod(trees_hit)))

if __name__ == '__main__':
    main()
