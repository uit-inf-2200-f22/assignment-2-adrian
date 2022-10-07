'''
Code written for inf-2200, University of Tromso
'''

import sys
from mipsSimulator import MIPSSimulator

def runSimulator(sim):
    # Replace this with your own main loop!
    while (1):
        sim.tick()
        print(sim.pc.currentAddress())

if __name__ == '__main__':
    assert(len(sys.argv) == 3), 'Usage: python %s memoryFile breakinmemoryfile' % (sys.argv[0])
    memoryFile = sys.argv[1]
    breakinmemoryfile = sys.argv[2]
    
    simulator = MIPSSimulator(memoryFile, breakinmemoryfile)
    runSimulator(simulator) 