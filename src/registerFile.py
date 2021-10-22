'''
Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
import common


class RegisterFile(CPUElement):
    def __init__(self):
        # Dictionary mapping register number to register value
        self.register = {}
        # Note that we won't actually use all the registers listed here...
        self.registerNames = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                              '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                              '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                              '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']
        # All registers default to 0
        for i in range(0, 32):
            self.register[i] = 0

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources,
                           outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 3),         'registerFile should have 3 inputs'
        assert(len(outputValueNames) == 2),     'registerFile should have 2 outputs'
        assert(len(control) == 1),              'registerFile should only have 1 control input'
        assert(len(outputSignalNames) == 0),    'registerFile does not have any control signal output'

        self.inputIM = inputSources[0][1]
        self.inputMuxIM = inputSources[1][1]
        self.inputMuxDM = inputSources[2][1] # Unsure how to do this excactly, the register file technically has to run twice now since the write data happens at the end of the path

        self.controlName = control[0]
        self.readData1 = outputValueNames[0]
        self.readData2 = outputValueNames[1]

    def printAll(self):
        '''
        Print the name and value in each register.
        '''

        print()
        print("Register file")
        print("================")
        for i in range(0, 32):
            print("%s \t=> %s (%s)" % (self.registerNames[i], common.fromUnsignedWordToSignedWord(
                self.register[i]), hex(int(self.register[i]))[:-1]))
        print("================")
        print()
        print()
        
        '''test for checking where the respective signals are found'''
        # value = 1829511764

        # binStr = f'{value:032b}'
    
        # test1 = binStr[6:11]
        # test2 = binStr[11:16]
        # test3 = binStr[16:21]

        # print("binStr: " + binStr)
        # print("25-21: " + test1)
        # print("20-16: " + test2)
        # print("15-11: " + test3)

    def writeOutput(self):
        binStr = f'{self.inputValues[self.inputIM]:032b}'

        rr1 = int(binStr[6:11], 2)
        rr2 = int(binStr[11:16], 2)

        wr = self.inputValues[self.inputMuxIM]

class TestRegisterFile(unittest.TestCase):
    def setUp(self):
        # Implement me!
        pass

    def test_correct_behavior(self):
        # Implement me!
        pass


if __name__ == '__main__':
    unittest.main()
