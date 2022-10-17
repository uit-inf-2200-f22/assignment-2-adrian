'''
Implements base class for memory elements.

Note that since both DataMemory and InstructionMemory are subclasses of the Memory
class, they will read the same memory file containing both instructions and data
memory initially, but the two memory elements are treated separately, each with its
own, isolated copy of the data from the memory file.

Code written for inf-2200, University of Tromso
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement
import common

class Memory(CPUElement):
    def __init__(self, filename):
    
        # Dictionary mapping memory addresses to data
        # Both key and value must be of type 'long'
        self.memory = {}

        # defines which '<' part of the code is to be run, since the memfiles folder contains mem files with different 
        # programs in one file, and the last one overwrites the previous in the dictionary.
        # A value of 0 deactivates this function completely, as it is probably is needed for the pytest or what not. 
        self.breakinmemoryfile = 0
        
        self.initializeMemory(filename)
    
    def initializeMemory(self, filename):
        '''
        Helper function that reads initializes the data memory by reading input
        data from a file.
        '''

        # Thanks to Daniel Ursin for pointing me in the right direction on this one.
        # Mem is now a list with each line being an element in the list
        mem = open(filename, "r").readlines()

        address = []
        instruction = []

        print("initalizing memory...")

        # Loops through each line in the mem lists, adds every word, separated by a tab, into a new list
        # which is then added to a dictionary.
        l = 0
        for line in mem:
            if line[0] == '#' or line[0] == '\n' or line[0] == '>':
                if line[0] == '>' and l != self.breakinmemoryfile:
                    l += 1
                elif l == self.breakinmemoryfile and self.breakinmemoryfile != 0:
                    break
                continue
            line = line.split("\t")
            if l == self.breakinmemoryfile:    
                # The following lines removes the 0x from the string, as it messes with certain low values
                if len(line[0]) > 2 :
                    line[0] = line[0][0: 0:] + line[0][1 + 1::]
                if len(line[1]) > 2 :
                    line[1] = line[1][0: 0:] + line[1][1 + 1::]
                    
                # Add adresses and instructions to the dictionary
                addr = int(line[0], 16)
                instr = int(line[1], 16)
                print(f'{addr:08x} maps to {instr:08x}')
                self.memory[addr] = instr
            else:
                continue
        
        keys = list(self.memory.keys())
        q = 0
        print("printing memory")
        for line in self.memory:
            print(line, "\t", self.memory[keys[q]])
            q = q+1

        print("initalizing memory complete\n")

    def printAll(self):
        print(f'Memory\n-----')
        for key in sorted(self.memory.keys()):
            print("%s\t=> %s\t(%s)" % (hex(int(key)), common.fromUnsignedWordToSignedWord(self.memory[key]), hex(int(self.memory[key]))))
        print(f'-----')

class TestMemory(unittest.TestCase):
    def setUp(self, file):
        self.memory = Memory(file)

    def test_correct_behaviour(self):
        print("========TESTING MEM=======")
        for i in self.memory.memory:
            print(f'{i} : {self.memory.memory[i]} \t {self.memory.memory[i]:032b}')
        print("==========================\n")