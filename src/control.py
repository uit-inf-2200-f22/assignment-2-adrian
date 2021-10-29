'''
Implements CP Element for control
'''

# from _typeshed import OpenTextModeWriting
import unittest
from cpuElement import CPUElement
from testElement import TestElement

class Control(CPUElement):
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1),         'Control should have 1 input'
        assert(len(outputValueNames) == 0),     'Control has no outputs'
        assert(len(control) == 0),              'Control should have no control signal inputs'
        assert(len(outputSignalNames) == 10),    'Control should have 9 control outputs'

        self.inputName = inputSources[0][1]

        self.regDst = outputSignalNames[0]
        self.ALUSrc = outputSignalNames[1]
        self.memtoReg = outputSignalNames[2]
        self.regWrite = outputSignalNames[3]
        self.memRead = outputSignalNames[4]
        self.memWrite = outputSignalNames[5]
        self.branch = outputSignalNames[6]
        self.ALUOp = outputSignalNames[7]
        self.jump = outputSignalNames[8]
        self.bne = outputSignalNames[9]

    def writeOutput(self):
        pass # randomControl has no data output

    def setControlSignals(self):

        signalValue = self.inputValues[self.inputName]
        print("Writing control output for control unit...")
        print("input signal value: ", signalValue)
        # if the opcode is all zeros, aka has the value zero, R-format is detected
        '''R-FORMAT INSTRUCTIONS'''
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
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.bne] = 0

        '''I-FORMAT INSTRUCTIONS'''
        if signalValue == 15:
            print("lui detected")
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.ALUSrc] = 1
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.ALUOp] = 3
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.bne] = 0

        # addi and addiu are treated as the same
        if signalValue == 8:
            print("addi detected")
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.ALUSrc] = 1
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.ALUOp] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.bne] = 0

        if signalValue == 9:
            print("addiu detected")
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.ALUSrc] = 1
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.ALUOp] = 4
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.bne] = 0

        if signalValue == 4:
            print("beq detected")
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.ALUSrc] = 0
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 1
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 1
            self.outputControlSignals[self.ALUOp] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.bne] = 0

        if signalValue == 5:
            print("bne detected")
            self.outputControlSignals[self.regDst] = 1
            self.outputControlSignals[self.ALUSrc] = 0
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 0
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 1
            self.outputControlSignals[self.ALUOp] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.bne] = 1

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
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.bne] = 0

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
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.bne] = 0
            print(f'control memread, memwrite: {self.outputControlSignals[self.memRead]} {self.outputControlSignals[self.memWrite]}')

        '''J-FORMAT INSTRUCTIONS'''
        if signalValue == 2:
            print("J detected")
            self.outputControlSignals[self.regDst] = 0
            self.outputControlSignals[self.ALUSrc] = 0
            self.outputControlSignals[self.memtoReg] = 0
            self.outputControlSignals[self.regWrite] = 0
            self.outputControlSignals[self.memRead] = 0
            self.outputControlSignals[self.memWrite] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.ALUOp] = 1
            self.outputControlSignals[self.jump] = 1
            self.outputControlSignals[self.bne] = 0
        print("")

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
            ['regDst', 'aluSrc', 'memtoReg', 'regWrite', 'memRead', 'memWrite', 'branch', 'aluOp', 'jump', 'bne']
        )
        self.testOutput.connect(
            [],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        print("=======TESTING CTRL=======")
        print("binary input: " + f'{36231392:032b}'[0:6])
        self.testInput.setOutputValue('controlSignal', int(f'{36231392:032b}'[0:6], 2))

        self.control.readInput()
        self.control.setControlSignals()
        print("")

        print("LOAD WORD...")
        print("binary input: " + f'{2385041632:032b}'[0:6])
        self.testInput.setOutputValue('controlSignal', int(f'{2385041632:032b}'[0:6], 2))

        self.control.readInput()
        self.control.setControlSignals()
        print("")

        print("STORE WORD...")
        print("binary input: " + f'{2921912544:032b}'[0:6])
        self.testInput.setOutputValue('controlSignal', int(f'{2921912544:032b}'[0:6], 2))

        self.control.readInput()
        self.control.setControlSignals()
        print("")

        print("BRANCH ON EQUAL...")
        print("binary input: " + f'{304666848:032b}'[0:6])
        self.testInput.setOutputValue('controlSignal', int(f'{304666848:032b}'[0:6], 2))

        self.control.readInput()
        self.control.setControlSignals()
        print("")

        print("BRANCH ON NOT EQUAL...")
        print("binary input: " + f'{304666848:032b}'[0:6])
        self.testInput.setOutputValue('controlSignal', int(f'{304666848:032b}'[0:6], 2))

        self.control.readInput()
        self.control.setControlSignals()
        print("==========================\n")
