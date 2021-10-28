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
        ctrlStr = f'{controlSignal:02b}'

        signal = self.inputValues[self.inputName]        
        binStr = f'{signal:06b}'
        
        # Only the 4 last bits in the func field are relevant
        signalValue = binStr[2:6]
        print("signalValue is: ", signalValue)
        print("aluOP is: ", ctrlStr)

        if controlSignal == 0:
            print("I-instruction detected...")
            print("add...")
            self.outputControlSignals[self.outputSignalName] = 2
        
        if ctrlStr[0] == '0':
            print("branch on equal operation detected...")
            print("sub...")
            self.outputControlSignals[self.outputSignalName] = 6
        
        if ctrlStr[0] == '1':
            print("R-instruction detected...")
            if signalValue == 0:
                print("add detected...")
                self.outputControlSignals[self.outputSignalName] = 2
            if signalValue == 1:
                print("addu detected...")
                self.outputControlSignals[self.outputSignalName] = 3        # There does not seem to be any official aluOperation output matchin a addu, so 3 is arbitrarily chosen here, it seems...
            if signalValue == 2:
                print("sub detected...")
                self.outputControlSignals[self.outputSignalName] = 6
            if signalValue == 3:
                print("subu detected...")
                self.outputControlSignals[self.outputSignalName] = 4        # There does not seem to be any official aluOperation output matchin a subu, so 4 is arbitrarily chosen here, i think atleast...
            if signalValue == 4:
                print("and detected...")
                self.outputControlSignals[self.outputSignalName] = 0
            if signalValue == 5:
                print("or detected...")
                self.outputControlSignals[self.outputSignalName] = 1
            if signalValue == 7:
                print("nor detected...")
                self.outputControlSignals[self.outputSignalName] = 5
            if signalValue == 10:
                print("set on less than detected...")
                self.outputControlSignals[self.outputSignalName] = 7
            if signalValue == 13:
                print("break deteced")
                raise Break("break instruction detected")
        print("output value set!")

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
        print("=======TEST ALUCTRL=======")
        self.testInput.setOutputValue('signal', int('000001', 2))
        self.testInput.setControlSignals('controlSignal', 2)

        self.aluControl.readInput()
        self.aluControl.readControlSignals()
        self.aluControl.setControlSignals()

        self.testOutput.readControlSignals()

        control = self.testOutput.controlSignals['aluControl']
        print("ctrl output: ", control)
        print("==========================\n")