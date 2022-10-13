'''
Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
from testElement import TestElement
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

        assert(len(inputSources) == 4),         'registerFile should have 4 inputs'
        assert(len(outputValueNames) == 2),     'registerFile should have 2 outputs'
        assert(len(control) == 1),              'registerFile should only have 1 control input'
        assert(len(outputSignalNames) == 0),    'registerFile does not have any control signal output'

        self.rs = inputSources[0][1]
        self.rt = inputSources[1][1]
        self.inputMuxIM = inputSources[2][1]
        self.inputMuxDM = inputSources[3][1] # Unsure how to do this excactly, the register file technically has to run twice now since the write data happens at the end of the path

        self.controlName = control[0][1]
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

    def writeOutput(self):
        print("Writing output for registers...")
        controlSignal = self.controlSignals[self.controlName]

        rr1 = self.inputValues[self.rs]
        rr2 = self.inputValues[self.rt]

        wr = self.inputValues[self.inputMuxIM]

        self.outputValues[self.readData1] = self.register[rr1]
        self.outputValues[self.readData2] = self.register[rr2]
        
        if controlSignal == 1:
            print(f'writing {self.inputValues[self.inputMuxDM]} to register {wr}')
            self.register[wr] = self.inputValues[self.inputMuxDM]
        print("")

class TestRegisterFile(unittest.TestCase):
    def setUp(self):
        self.testInput = TestElement()
        self.registerFile = RegisterFile()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['RS', 'RT', 'RD', 'DM'],
            [],
            ['regWrite']
        )
        self.registerFile.connect(
            [(self.testInput, 'RS'), (self.testInput, 'RT'), (self.testInput, 'RD'), (self.testInput, 'DM')],
            ['rd1', 'rd2'],
            [(self.testInput, 'regWrite')],
            []
        )
        self.testOutput.connect(
            [(self.registerFile, 'rd1'), (self.registerFile, 'rd2')],
            [],
            [],
            []
        )
    # latex article class: "ieetran"?

    def test_correct_behaviour(self):
        print("========TESTING REG=======")
        print("WRITE REG...")
        print("reg 2 & 4: 21 & 69")
        print("regWrite: 0")
        self.registerFile.register[2] = 21
        self.registerFile.register[4] = 69
        self.testInput.setOutputValue('RS', 2)
        self.testInput.setOutputValue('RT', 4)
        self.testInput.setOutputValue('RD', 9)
        self.testInput.setControlSignals('regWrite', 0)
        
        self.registerFile.readInput()
        self.registerFile.readControlSignals()
        self.registerFile.writeOutput()

        self.testOutput.readInput()
        op1, op2 =self.testOutput.inputValues['rd1'], self.testOutput.inputValues['rd2']

        print(f'output: {op1} {op2}')
        print("")

        print("READ REG...")
        print("reg 2 & 4: 80085 & 420")
        print("dm input value: 1337")
        print("regWrite: 1")
        self.registerFile.register[2] = 80085
        self.registerFile.register[4] = 420
        self.testInput.setOutputValue('RS', 2)
        self.testInput.setOutputValue('RT', 4)
        self.testInput.setOutputValue('RD', 9)
        self.testInput.setOutputValue('DM', 1337)
        self.testInput.setControlSignals('regWrite', 1)

        self.registerFile.readInput()
        self.registerFile.readControlSignals()
        self.registerFile.writeOutput()
        
        print(f'register 9 now contains: {self.registerFile.register[9]}')
        print("==========================\n")

if __name__ == '__main__':
    unittest.main()
