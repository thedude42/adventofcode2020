import sys
import re
from typing import List

id_fields = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    "cid"
]

def parse_inputfile(infile: str):
    with open(infile, 'r') as input_file:
        result = []
        scanned_codes = []
        for line in input_file:
            if line != "\n":
                scanned_codes.append(line)
            else:
                result.append(scanned_codes)
                scanned_codes = []
        if len(scanned_codes) > 0:
            result.append(scanned_codes)
        return result

def validate_scanned_id(id_list: List):
    print("processing list: {}".format(id_list))
    checklist = { field:False for field in id_fields }
    field_vals = {}
    for id_line in id_list:
        for id_item in id_line.split():
            item, value = id_item.split(":")
            field_vals[item] = value
            # this throws on bad input
            checklist[item] = True
    for k,v in checklist.items():
        print("{}:{}".format(k,v))
        if not v and k != "cid":
            return None
    return field_vals

field_ranges = {
    "byr":(1920,2002),
    "iyr":(2010,2020),
    "eyr":(2020,2030),
}

hgt_re = re.compile(r'(\d{2,3})(cm|in)')
hgt_ranges = {
    "in":(59,76),
    "cm":(150,193)
}

hcl_re = re.compile(r'#[0-9a-f]{6}')
ecl_re = re.compile(r'amb|blu|brn|gry|grn|hzl|oth')
pid_re = re.compile(r'[0-9]{9}')

def validate_field_values(field_vals):
    for k,v in field_vals.items():
        print("checking k:v of {}:{}".format(k,v))
        if k in ["byr", "iyr", "eyr"]:
            if not numeric_range_validate(int(v), *field_ranges[k]):
                print("field {} is not within spec: {}".format(k, v))
                return False
        elif k == "hgt":
            m = hgt_re.match(v)
            if not m or not numeric_range_validate(int(m.group(1)), *hgt_ranges[m.group(2)]):
                print("field {} is not within spec: {}".format(k, v))
                return False
        elif k == "hcl":
            if not hcl_re.match(v):
                print("field {} is not within spec: {}".format(k, v))
                return False
        elif k == "ecl":
            if not ecl_re.match(v):
                print("field {} is not within spec: {}".format(k, v))
                return False
        elif k == "pid":
            if not pid_re.match(v):
                print("field {} is not within spec: {}".format(k, v))
                return False
    return True


def numeric_range_validate(inval: int, min: int, max: int):
    if inval < min or inval > max:
        return False
    return True

def main():
    if len(sys.argv) != 2:
        print("require one argument: file name of input")
        sys.exit(1)
    valid_ids_p1 = 0
    valid_ids_p2 = 0
    scanned_ids = parse_inputfile(sys.argv[1])
    for id in scanned_ids:
        fields = validate_scanned_id(id)
        if fields:
            valid_ids_p1 += 1
        if fields and validate_field_values(fields):
            valid_ids_p2 += 1
    print("we found {} valid IDs on pass 1".format(valid_ids_p1))
    print("we found {} valid IDs on pass 2".format(valid_ids_p2))

if __name__ == '__main__':
    main()