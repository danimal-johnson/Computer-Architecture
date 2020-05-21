"""CPU functionality."""

import sys

# Registers:
IM = 5  # Interrupt Mask register
IS = 6  # Interrupt Status register
SP = 7  # Stack Pointer

# Instructions
LDI = 0b10000010  # 0x82
PRN = 0b01000111  # 0x47
HLT = 0b00000001  # 0x01


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 25  # Initialize RAM to zeroes
        self.reg = [0] * 8  # Initialize all registers to zero
        self.reg[SP] = 0xF4  # Set Stack Pointer to memory address 0xF4

        # Internal Registers
        self.PC = 0         # Program Counter starts at address 0x00
        self.FL = 0x00  # Flags
        # IR, MAR, MDR not initialized

        self.halted = False
        # self.load() # Already in ls8.py

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]
        print("Loading...")
        for instruction in program:
            self.ram[address] = instruction
            address += 1
        print("Done.")

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        print("Running the CPU.")

        while not self.halted:
            ir = self.ram[self.PC]  # Instruction
            op1 = self.ram[self.PC + 1]    # Operand 1
            op2 = self.ram[self.PC + 2]    # Operand 2
            print("Instruction = ", ir)

            if ir == HLT:
                self.halted = True
                sys.exit(0)

            elif ir == LDI:
                self.reg[op1] = op2
                self.PC += 3

            elif ir == PRN:
                print("Output: ", self.reg[op1])
                self.PC += 2

            else:
                print("Instruction ", ir, "not implemented. Halting.")
                sys.exit(0)
