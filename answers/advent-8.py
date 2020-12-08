import sys
from collections import namedtuple

Instruction = namedtuple('Instuction', ['op', 'arg'])

class Machine:
    '''
    virtual machine base on North Pole Airlines' in-flight entertainment console
    '''
    def __init__(self, bootcode_filename: str):
        self.boot_code = []
        self.acc = 0 # accumulator
        self.line_history = None
        self.ip = None # instruction pointer register
        with open(bootcode_filename, 'r') as bootfile:
            for line in bootfile:
                op, arg = line.split()
                self.boot_code.append(Instruction(op, int(arg)))

    def run(self):
        self.line_history = []
        #instruction_runtime = enumerate(self.boot_code)
        self.ip = 0
        self.acc = 0
        while True:
            if self.ip >= len(self.boot_code):
                return 0
            if self.ip in self.line_history:
                return 1
            self.line_history.append(self.ip)
            if self.boot_code[self.ip].op == "acc":
                self.acc += self.boot_code[self.ip].arg
                self.ip += 1
            elif self.boot_code[self.ip].op == "jmp":
                self.ip += self.boot_code[self.ip].arg
            elif self.boot_code[self.ip].op == "nop":
                self.ip +=1
            else:
                raise Exception("UnknownInstruction: {}".format(self.boot_code[self.ip].op))

    def part1(self):
        self.run()
        print("repeating instruction {} at address {} with accumulator {}".format(
            self.boot_code[self.ip], self.ip, self.acc
        ))

    def part2(self):
        for i in range(len(self.boot_code)):
            if self.boot_code[i].op == "nop":
                tmp_jmp = Instruction("jmp", self.boot_code[i].arg)
                orig_nop = self.boot_code[i]
                self.boot_code[i] = tmp_jmp
                if self.run() == 0:
                    break
                self.boot_code[i] = orig_nop
            elif self.boot_code[i].op == "jmp":
                tmp_nop = Instruction("nop", self.boot_code[i].arg)
                orig_jmp = self.boot_code[i]
                self.boot_code[i] = tmp_nop
                if self.run() == 0:
                    break
                self.boot_code[i] = orig_jmp
        print("program terminated successfully. acc: {}".format(self.acc))

def main():
    if len(sys.argv) != 2:
        print("Single input filename required, no more, no less.")
        sys.exit(1)
    m = Machine(sys.argv[1])
    m.part1()
    m.part2()

if __name__ == '__main__':
    main()