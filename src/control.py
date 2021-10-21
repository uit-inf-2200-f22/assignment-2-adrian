'''
Implements CP Element for control
'''

import unittest
from cpuElement import CPUElement
from testElement import TestElement

class Control(CPUElement):
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'Control should have 1 input'
        assert(len(outputValueNames) == 0), 'Control has no outputs'
        assert(len(control) == 0), 'Control should have no control signal inputs'
        assert(len(outputSignalNames) == 9), 'Control should have 9 control outputs'

        self.inputName = inputSources[0][1]

        self.regDst = outputSignalNames[0]
        self.jump = outputSignalNames[1]
        self.branch = outputSignalNames[2]
        self.memRead = outputSignalNames[3]
        self.memtoReg = outputSignalNames[4]
        self.ALUOp = outputSignalNames[5]
        self.memWrite = outputSignalNames[6]
        self.ALUSrc = outputSignalNames[7]
        self.regWrite = outputSignalNames[8]

    def writeOutput(self):
        pass # randomControl has no data output

    def setControlSignals(self):

        signal = self.inputValues[self.inputName]
        
        binStr = f'{signal:032b}'
        signalValue = int(binStr[0:6], 2)
        print("input signal value: ", signalValue)
        # if the opcode is all zeros, aka has the value zero, R-format is detected
        if signalValue == 0:
            print("r-format detected")
            self.outputControlSignals[self.regDst] = 1
            self.outputControlSignals[self.ALUSrc] = 0
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.ALUOp] = 2

            self.outputControlSignals[self.jump] = 100

        if signalValue == 35:
            print("lw detected")
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.ALUSrc] = 1
            self.outputControlSignals[self.memtoReg] = 1
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 1
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.ALUOp] = 0

            self.outputControlSignals[self.jump] = 100

        if signalValue == 43:
            print("sw detected")
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.ALUSrc] = 1
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 0
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 1
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.ALUOp] = 0

            self.outputControlSignals[self.jump] = 100

        if signalValue == 4:
            print("beq detected")
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.ALUSrc] = 1
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 0
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 1
            self.outputControlSignals[self.ALUOp] = 1

            self.outputControlSignals[self.jump] = 100

class TestControl(unittest.TestCase):
    def setUp(self):
        self.testInput = TestElement()
        self.control = Control()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['controlSignal'],
            [],
            []
        )
        self.control.connect(
            [(self.testInput, 'controlSignal')],
            [],
            [],
            ['regDst', 'aluSrc', 'memtoReg', 'regWrite', 'memRead', 'memWrite', 'branch', 'aluOp', 'jump']
        )
        self.testOutput.connect(
            [],
            [],
            [],
            []
        )

    def test_correct_behavior(self):
        print("========R-FORMAT========")
        print("binary input: " + f'{36231392:032b}')
        self.testInput.setOutputValue('controlSignal', int(f'{36231392:032b}', 2))

        self.control.readInput()
        self.control.setControlSignals()
        print("========================")

        print("========LOAD WORD=======")
        print("binary input: " + f'{2385041632:032b}')
        self.testInput.setOutputValue('controlSignal', int(f'{2385041632:032b}', 2))

        self.control.readInput()
        self.control.setControlSignals()
        print("========================")

        print("=======STORE WORD=======")
        print("binary input: " + f'{2921912544:032b}')
        self.testInput.setOutputValue('controlSignal', int(f'{2921912544:032b}', 2))

        self.control.readInput()
        self.control.setControlSignals()
        print("========================")

        print("======BRANCH EQUAL======")
        print("binary input: " + f'{304666848:032b}')
        self.testInput.setOutputValue('controlSignal', int(f'{304666848:032b}', 2))

        self.control.readInput()
        self.control.setControlSignals()
        print("========================")
