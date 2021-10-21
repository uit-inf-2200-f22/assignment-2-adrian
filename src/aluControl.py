'''
Implements an alu (arithemtic logic unit) control unit for controling the alu
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement

class AluControl(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1),         'aluControl should have only one input'
        assert(len(outputValueNames) == 0),     'aluControl should not have any outputs'
        assert(len(control) == 1),              'aluControl should have one control input'
        assert(len(outputSignalNames) == 1),    'aluControl should have one control signal output' 

        self.controlName = control[0][1]
        self.inputName = inputSources[0][1]
        self.outputControlName = outputSignalNames[0]

    def setControlSignals(self): 
        controlSignal = self.controlSignals[self.controlName]
        signal = self.inputValues[self.inputName]
        
        binStr = f'{signal:032b}'
        ctrlStr = f'{controlSignal:02b}'
        
        signalValue = int(binStr[28:32], 2)
        print("signalValue is: ", signalValue)
        print("binary: ", binStr[28:32])

        print("checking aluOP signal...")
        print("aluOP is: ", ctrlStr)
        if controlSignal == 0:
            print("load/store operation detected...")
            print("add detected...")
            self.outputControlSignals[self.outputControlName] = 2

        if ctrlStr[0] == '0':
            print("branch equal operation detected...")
            print("sub detected...")
            self.outputControlSignals[self.outputControlName] = 6
        
        if ctrlStr[0] == '1':
            print("arithemtic operation detected...")
            if signalValue == 0:
                print("add detected...")
                self.outputControlSignals[self.outputControlName] = 2
            if signalValue == 2:
                print("sub detected...")
                self.outputControlSignals[self.outputControlName] = 6
            if signalValue == 4:
                print("and detected...")
                self.outputControlSignals[self.outputControlName] = 0
            if signalValue == 5:
                print("or detected...")
                self.outputControlSignals[self.outputControlName] = 1
            if signalValue == 10:
                print("set less than detected...")
                self.outputControlSignals[self.outputControlName] = 7
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
    
    def test_correct_behavior(self):
        print("========START========")
        self.testInput.setOutputValue('signal', 8574458)
        self.testInput.setOutputControl('controlSignal', 2)

        self.aluControl.readInput()
        self.aluControl.readControlSignals()
        self.aluControl.setControlSignals()

        self.testOutput.readControlSignals()

        output = self.testOutput.controlSignals['aluControl']
        print("output: ", output)
        print("--------STOP--------")