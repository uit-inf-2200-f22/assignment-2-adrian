'''
Implements base class for memory elements.

Note that since both DataMemory and InstructionMemory are subclasses of the Memory
class, they will read the same memory file containing both instructions and data
memory initially, but the two memory elements are treated separately, each with its
own, isolated copy of the data from the memory file.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
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
        
        # Remove this and replace with your implementation!
        # Implementation MUST populate the dictionary in self.memory!

        # mem er nå en liste som inneholder 1 linje per element i listen
        mem = open(filename, "r").readlines()

        address = []
        instruction = []

        # Loops through each line in the mem lists, adds every word, separated by a tab, into a new list
        # which is then added to its respective list.
        for line in mem:
            if line[0] == '#':
                continue
            parse = line.split("\t")
            address.append(int(parse[0], 16))
            instruction.append(int(parse[1], 16))

        i = 0
        while i < len(address):
            self.memory.pop(int(address[i]), int(instruction[i]))
            i += 1

        
    def printAll(self):
        for key in sorted(self.memory.keys()):
            print("%s\t=> %s\t(%s)" % (hex(int(key)), common.fromUnsignedWordToSignedWord(self.memory[key]), hex(int(self.memory[key]))))
