"""CPU functionality."""

import sys


HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.fl = 0
        self.ram = [0] * 256 # 256 bytes
        self.reg = [0] * 9
        pass

    def ram_read(self, pc):
        print(self.ram[pc])

    def ram_write(self, value):
        self.ram.append(value) 

    def load(self):
        """Load a program into memory."""
        
        address = 0
        filename = sys.argv[1]
        program = []

        with open(f"examples/{filename}") as f:
            for line in f:
                n = line.split('#')
                n[0] = n[0].strip()

                if n[0] == '':
                    continue
                val = int(n[0], 2)
                program.append(val)
        
                
        # print(f"Program = {program}")

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            print(f"REG = {self.reg}")
            print(f"Multiplying reg[{reg_a}] which is {self.reg[reg_a]} with reg[{reg_b}] which is {self.reg[reg_b]}")
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc), 
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        
        while running:
            if self.ram[self.pc] == HLT:
                running = False
            elif self.ram[self.pc] == LDI:
                register = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                print(f"Adding value {value} to register {register}")
                self.pc += 3
                self.reg[register] = value
            elif self.ram[self.pc] == PRN:
                register = self.ram[self.pc + 1]
                print(self.reg[register])
                self.pc += 2
            elif self.ram[self.pc] == MUL:
                register1 = self.ram[self.pc + 1]
                register2 = self.ram[self.pc + 2]
                self.alu("MUL", register1, register2)
                self.pc += 3

            




        pass


