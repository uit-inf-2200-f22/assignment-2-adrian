'''
Implements a simple cpu element that inverses the zero signal from the alu if bne opcode is registered
'''

import unittest
from cpuElement import CPUElement
from testElement import TestElement

class BNE(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0),         'bne has noy got any input sources'
        assert(len(outputValueNames) == 0),     'bne has one output'
        assert(len(control) == 2),              'bne has two input control signals'
        assert(len(outputSignalNames) == 1),    'bne has no output control signal'

        self.controlSignal = control[0][1]
        self.zeroSignal = control[1][1]
        self.outputSignal = outputSignalNames[0]
    
    def writeOutput(self):
        self.outputValues['none'] = 0

    def setControlSignals(self):
        ctrlSignal = self.controlSignals[self.controlSignal]
        zeroSignal = self.controlSignals[self.zeroSignal]
        print("Writing control output for bne sign inverter...")
        print(f'control signal: {ctrlSignal}')
        print(f'zero signal: {zeroSignal}')
        if ctrlSignal == 1:
            if zeroSignal == 1:
                self.outputControlSignals[self.outputSignal] = 0
            else:
                self.outputControlSignals[self.outputSignal] = 1
        else:
            print(f'output: {zeroSignal}')
            self.outputControlSignals[self.outputSignal] = zeroSignal
        print("")

class TestBNE(unittest.TestCase):
    def setUp(self):
        self.testInput = TestElement()
        self.bne = BNE()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            [],
            [],
            ['ctrl', 'zero']
        )
        self.bne.connect(
            [],
            [],
            [(self.testInput, 'ctrl'), (self.testInput, 'zero')],
            ['outputSignal']
        )
        self.testOutput.connect(
            [],
            [],
            [(self.bne, 'outputSignal')],
            []
        )
    
    def test_correct_behaviour(self):
        print("=======TESTING BNE=======")
        print("input...")
        print("ctrl: 0\tzero: 1")
        print("excpected outcome: 1")
        self.testInput.setControlSignals('ctrl', 0)
        self.testInput.setControlSignals('zero', 1)

        self.bne.readControlSignals()
        self.bne.setControlSignals()

        self.testOutput.readControlSignals()

        output = self.testOutput.controlSignals['outputSignal']
        print(f'output signal: {output}')
        if output == 1:
            print("SUCCESS")
        else:
            print("FAIL")
        
        print("")

        print("input...")
        print("ctrl: 1\tzeroSignal: 0")
        print("excpected outcome: 1")
        self.testInput.setControlSignals('ctrl', 1)
        self.testInput.setControlSignals('zero', 0)

        self.bne.readControlSignals()
        self.bne.setControlSignals()

        self.testOutput.readControlSignals()

        output = self.testOutput.controlSignals['outputSignal']
        print(f'output signal: {output}')
        if output == 1:
            print("SUCCESS")
        else:
            print("FAIL")
        print("=========================\n")
