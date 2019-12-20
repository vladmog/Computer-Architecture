#!/usr/bin/env python3

"""Main."""

import sys

# program = sys.argv[1]
# print(f"Program = {program}")


from cpu import *

cpu = CPU()

cpu.load()
cpu.run()