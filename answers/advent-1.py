import sys, math

def get_lines(filename):
    with open(filename, 'r') as infile:
        result = [ int(line) for line in infile ]
    return result

def brute_calculate(expense_report):
    for x in expense_report:
        for y in expense_report:
            for z in expense_report:
                if x != y and x + y + z == 2020:
                    return x*y*z

def main():
    if len(sys.argv) != 2:
        print("provide only one input, a single filename")
        sys.exit(1)
    expense_report = get_lines(sys.argv[1])
    print("Result: {}".format(brute_calculate(expense_report)))


if __name__ == '__main__':
    main()