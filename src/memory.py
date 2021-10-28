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

        # Loops through each line in the mem lists, adds every word, separated by a tab, into a new list
        # which is then added to its respective list.
        for line in mem:
            if line[0] == '#':
                continue
            line = line.split("\t")
            # print(f'address: {int(line[0], 16)}')
            address.append(int(line[0], 16))
            instruction.append(int(line[1], 16))

        # Populating the self.memory dictionary
        i = 0
        while i < len(address):
            self.memory[int(address[i])] = int(instruction[i])
            i += 1


    def printAll(self):
        for key in sorted(self.memory.keys()):
            print("%s\t=> %s\t(%s)" % (hex(int(key)), common.fromUnsignedWordToSignedWord(self.memory[key]), hex(int(self.memory[key]))))

class TestMemory(unittest.TestCase):
    def setUp(self, file):
        self.memory = Memory(file)

    def test_correct_behaviour(self):
        print("========TESTING MEM=======")
        for i in self.memory.memory:
            print(f'{i} : {self.memory.memory[i]} \t {self.memory.memory[i]:032b}')
        print("==========================\n")