'''
Implements a cpu element for joining the upper 4 bits of the pc+4 
'''

import unittest
from testElement import TestElement
from cpuElement import CPUElement

class PcJump(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2),         'pcJump should have 2 inputs'
        assert(len(outputValueNames) == 1),     'pcJump only has one output'
        assert(len(control) == 0),              'pcJump has no control signal inputs'
        assert(len(outputSignalNames) == 0),    'pcJump does not have any control signal outputs'

        self.lstInput = inputSources[0][1]
        self.adderInput = inputSources[1][1]
        
        self.jumpAddress = outputValueNames[0]

    def writeOutput(self):
        print("Writing output for pcJump...")
        dataA = f'{self.inputValues[self.lstInput]:028b}'
        dataB = f'{self.inputValues[self.adderInput]:032b}'[0:4]    # compressed way to get the first(last) 4 bits in the add
        print("jumping to: ", int(dataB + dataA,2))
        self.outputValues[self.jumpAddress] = int(dataB + dataA,2)
        print("")

class TestPcJump(unittest.TestCase):
    def setUp(self):
        self.testInput = TestElement()
        self.pcJump = PcJump()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['lstInput','adderInput'],
            [],
            []
        )
        self.pcJump.connect(
            [(self.testInput, 'lstInput'), (self.testInput, 'adderInput')],
            ['jumpAddress'],
            [],
            []
        )
        self.testOutput.connect(
            [(self.pcJump, 'jumpAddress')],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        print("========TESTING PCJ=======")
        print("leftshittwo input:     1010000000000000000000000000")
        print("pc+4adder input:   11000000000000000000000000000000")
        print("excpected result:  11001010000000000000000000000000")
        self.testInput.setOutputValue('lstInput', int('1010000000000000000000000000',2))
        self.testInput.setOutputValue('adderInput', int('11000000000000000000000000000000',2))

        self.pcJump.readInput()
        self.pcJump.writeOutput()

        self.testOutput.readInput()

        jumpAddress = 'jumpAddress'
        print(f'output:            {self.testOutput.inputValues[jumpAddress]:032b}')
        assert(self.testOutput.inputValues['jumpAddress'] == int('11001010000000000000000000000000',2   )), 'output value does not mactch excpected result'
        print("=========================\n")