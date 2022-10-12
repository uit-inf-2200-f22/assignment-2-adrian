'''
Implements an alu (arithemtic logic unit) control unit for controling the alu
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement
from common import Break

class AluControl(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1),         'aluControl should have only one input'
        assert(len(outputValueNames) == 0),     'aluControl should not have any outputs'
        assert(len(control) == 1),              'aluControl should have one control input'
        assert(len(outputSignalNames) == 1),    'aluControl should have one control signal output' 

        self.controlName = control[0][1]
        self.inputName = inputSources[0][1]
        self.outputSignalName = outputSignalNames[0]

    def writeOutput(self):
        self.outputValues['none'] = 0

    def setControlSignals(self): 
        controlSignal = self.controlSignals[self.controlName]
        ctrlStr = f'{controlSignal:03b}'
        # print("Writing control output for aluControl...")
        signal = self.inputValues[self.inputName]        
        binStr = f'{signal:06b}'
        
        signalValue = int(binStr[0:6],2)
        # print("signalValue is: ", signalValue)
        # print("aluOP is: ", ctrlStr)

        if ctrlStr == '000':
            # print("I-instruction detected...")
            # print("output: add")
            self.outputControlSignals[self.outputSignalName] = 2

        elif ctrlStr == '001':
            # # print("branch on equal operation detected...")
            # # print("output: sub")
            self.outputControlSignals[self.outputSignalName] = 6
        
        if ctrlStr == '010':
            # print("R-instruction detected...")
            if signalValue == 32:
                # print("output: add")
                self.outputControlSignals[self.outputSignalName] = 2
            if signalValue == 33:
                # print("output: addu")
                self.outputControlSignals[self.outputSignalName] = 3        # There does not seem to be any official aluOperation output matchin a addu, so 3 is arbitrarily chosen here, it seems...
            if signalValue == 34:
                # print("output: sub")
                self.outputControlSignals[self.outputSignalName] = 6
            if signalValue == 35:
                # print("output: subu")
                self.outputControlSignals[self.outputSignalName] = 4        # There does not seem to be any official aluOperation output matchin a subu, so 4 is arbitrarily chosen here, i think atleast... apparently addu and subu i removed from later mips implementation
            if signalValue == 36:
                # print("output: and")
                self.outputControlSignals[self.outputSignalName] = 0
            if signalValue == 37:
                # print("output: or")
                self.outputControlSignals[self.outputSignalName] = 1
            if signalValue == 39:
                # print("output: nor")
                self.outputControlSignals[self.outputSignalName] = 5
            if signalValue == 42:
                # print("output: set on less than")
                self.outputControlSignals[self.outputSignalName] = 7
            if signalValue == 13:
                print("BREAKING BREAKING BREAKING BREAKING BREAKING BREAKING BREAKING BREAKING BREAKING BREAKING BREAKING BREAKING BREAKING BREAKING ")
                raise Break("break instruction detected")
        # print("output value set!\n")

        if ctrlStr == '011':
            # print("I-instruction detected...")
            # print("output: lui")
            self.outputControlSignals[self.outputSignalName] = 8
        if ctrlStr == '100':
            # print("I-instruction detected...")
            # print("output: addiu")
            self.outputControlSignals[self.outputSignalName] = 3

class TestAluControl(unittest.TestCase):
    def setUp(self):
        self.aluControl = AluControl()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['signal'],
            [],
            ['controlSignal'],
        )
        self.aluControl.connect(
            [(self.testInput, 'signal')],
            [],
            [(self.testInput, 'controlSignal')],
            ['aluControl']
        )
        self.testOutput.connect(
            [],
            [],
            [(self.aluControl, 'aluControl')],
            []
        )
    
    def test_correct_behaviour(self):
        # print("=======TEST ALUCTRL=======")
        self.testInput.setOutputValue('signal', int('000001', 2))
        self.testInput.setControlSignals('controlSignal', 2)

        self.aluControl.readInput()
        self.aluControl.readControlSignals()
        self.aluControl.setControlSignals()

        self.testOutput.readControlSignals()

        control = self.testOutput.controlSignals['aluControl']
        # print("ctrl output: ", control)
        # print("==========================\n")