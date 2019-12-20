"""CPU functionality."""

import sys


HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL  = 0b01010000 # 00000rrr
RET = 0b00010001
ADD = 0b10100000 # 00000aaa 00000bbb
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.fl = 0b00000000 #00000LGE
        self.ram = [0] * 256 # 256 bytes
        self.reg = [0] * 9

        self.reg[7] = self.ram[0xF4]
        self.sp = self.reg[7]
        
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret
        self.branchtable[ADD] = self.handle_add
        # SPRINT
        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[JEQ] = self.handle_jeq
        self.branchtable[JNE] = self.handle_jne

        

    def handle_jne(self):
        # If E flag is clear (false, 0), jump to the address stored in the given register.
        register = self.ram[self.pc + 1]
        if (self.fl & 0b00000001) == 0:
            self.pc = self.reg[register]
        else:
            self.pc += 2


    def handle_jeq(self):
        # If equal flag is set (true), jump to the address stored in the given register.
        register = self.ram[self.pc + 1]
        if (self.fl & 0b00000001) > 0:
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def handle_cmp(self):
        registerA = self.ram[self.pc + 1]
        registerB = self.ram[self.pc + 2]
        self.alu("CMP", registerA, registerB)
        self.pc += 3
    
    def handle_jmp(self):
        register = self.ram[self.pc + 1]
        self.pc = self.reg[register]

    def handle_ldi(self):
        register = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        print(f"Adding value {value} to register {register}")
        self.pc += 3
        self.reg[register] = value
    
    def handle_prn(self):
        register = self.ram[self.pc + 1]
        print(f"=====================\nPrinting {self.reg[register]} from register {register}\n======================")
        self.pc += 2

    def handle_mul(self):
        register1 = self.ram[self.pc + 1]
        register2 = self.ram[self.pc + 2]
        self.alu("MUL", register1, register2)
        self.pc += 3

    def handle_add(self):
        register1 = self.ram[self.pc + 1]
        register2 = self.ram[self.pc + 2]
        self.alu("ADD", register1, register2)
        self.pc +=3
    
    def handle_push(self):
        self.sp -= 1
        register = self.ram[self.pc + 1]
        self.ram[self.sp] = self.reg[register]
        print(f"Pushing {self.reg[register]} from register {register} onto the Stack")
        self.pc += 2

    def handle_pop(self):
        register = self.ram[self.pc + 1]
        print(f"Popping {self.ram[self.sp]} off the stack into register {register}")
        self.reg[register] = self.ram[self.sp]
        self.sp += 1
        self.pc += 2

    def handle_call(self):
        print("CALL")
        # Push next instruction location to stack
        self.sp -= 1
        return_address = self.pc + 2
        self.ram[self.sp] = return_address
        print(f"Saving return address of {return_address} to stack")

        register = self.ram[self.pc + 1]
        print(f"Jumping from {self.pc} to {self.reg[register]}")
        self.pc = self.reg[register]

    def handle_ret(self):
        print("RET")
        # Pop the value from the top of the stack and store it in the PC.
        self.pc = self.ram[self.sp]
        self.sp += 1

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
            print(f"REG = {self.reg}")
            print(f"Adding reg[{reg_a}] which is {self.reg[reg_a]} with reg[{reg_b}] which is {self.reg[reg_b]}")
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            print(f"REG = {self.reg}")
            print(f"Multiplying reg[{reg_a}] which is {self.reg[reg_a]} with reg[{reg_b}] which is {self.reg[reg_b]}")
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

        elif op == "CMP":
            # 00000LGE
            print(f"REG = {self.reg}")
            print(f"Comparing reg[{reg_a}] which is {self.reg[reg_a]} with reg[{reg_b}] which is {self.reg[reg_b]}")
            if self.reg[reg_a] == self.reg[reg_b]:
                # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
                print("A == B")
                self.fl = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                print("A > B")
                self.fl = 0b00000010
                # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
            elif self.reg[reg_a] < self.reg[reg_b]:
                print("A < B")
                self.fl = 0b00000100
                # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.

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
            print(f"\nLine {self.pc + 1}: {bin(self.ram[self.pc])}")
            if self.ram[self.pc] == HLT:
                running = False
            else:
                self.branchtable[self.ram[self.pc]]()  # Substituting if-elif cascade with branchtable

            # elif self.ram[self.pc] == LDI:
            #     # register = self.ram[self.pc + 1]
            #     # value = self.ram[self.pc + 2]
            #     # print(f"Adding value {value} to register {register}")
            #     # self.pc += 3
            #     # self.reg[register] = value
            #     # ==========================
            #     self.branchtable[LDI]()
            # elif self.ram[self.pc] == PRN:
            #     # register = self.ram[self.pc + 1]
            #     # print(self.reg[register])
            #     # self.pc += 2
            #     # ===========================
            #     self.branchtable[PRN]()
            # elif self.ram[self.pc] == MUL:
            #     # register1 = self.ram[self.pc + 1]
            #     # register2 = self.ram[self.pc + 2]
            #     # self.alu("MUL", register1, register2)
            #     # self.pc += 3
            #     # ===========================
            #     self.branchtable[MUL]()




        pass