import sys
from collections import namedtuple

Policy = namedtuple('Policy', ['pos_1', 'pos_2', 'letter'])

def get_lines(filename):
    with open(filename, 'r') as infile:
        result = [ line for line in infile ]
    return result

def parse_policy(policy: str):
    occurrence_range, letter = policy.split()
    pos1, pos2 = [ int(x) for x in occurrence_range.split('-') ]
    return Policy(pos1, pos2, letter)

def validate_password(policy, password):
    p1 = password[policy.pos_1 - 1]
    p2 = password[policy.pos_2 - 1]
    if policy.letter == p1:
        if policy.letter == p2:
            return False
        return True
    elif policy.letter == p2:
        return True
    return False

def check_password(password_entry: str):
    policy_str, password = password_entry.split(":")
    password = password.strip()
    policy = parse_policy(policy_str)
    return validate_password(policy, password)


def main():
    if len(sys.argv) != 2:
        print("provide only one input, a single filename")
        sys.exit(1)
    passwords = get_lines(sys.argv[1])
    valid_count = 0
    for password in passwords:
        if check_password(password):
            valid_count += 1
    print("found {} valid passwords".format(valid_count))




if __name__ == '__main__':
    main()