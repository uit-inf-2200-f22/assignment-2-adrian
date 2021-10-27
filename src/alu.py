'''
Implements an arithmetic logic unit
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement

class Alu(CPUElement):

    def connect(self, input, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, input, outputValueNames, control, outputSignalNames)

        assert (len(input) == 2), 'Alu should have 2 inputs'
        assert (len(outputValueNames) == 1), 'Alu should have 1 output'
        assert (len(control) == 1), 'Alu should have 1 control input'
        assert (len(outputSignalNames) == 1), 'Alu should have 1 control output'

        self.inputNameOne = input[0][1]
        self.inputNameTwo = input[1][1]
        self.outputName = outputValueNames[0]
        self.controlInputName = control[0][1]
        self.controlOutputName = outputSignalNames[0]
    
    def writeOutput(self):
        readData1 = self.inputValues[self.inputNameOne]
        muxDecision = self.inputValues[self.inputNameTwo]

        controlSignal = self.controlSignals[self.controlInputName]

        if controlSignal == 2:
            self.outputValues[self.outputName] = readData1 + muxDecision
        elif controlSignal == 3:
            result = readData1 + muxDecision
            if result > 2147483648:
                raise ValueError("overflow")
            else:
                self.outputValues[self.outputName] = result
        elif controlSignal == 6:
            self.outputValues[self.outputName] = readData1 - muxDecision
        elif controlSignal == 4:
            result = readData1 - muxDecision
            if result < 0:
                raise ValueError("overflow")
            else:
                self.outputValues[self.outputName] = result
        elif controlSignal == 0:
            self.outputValues[self.outputName] = readData1 & muxDecision
        elif controlSignal == 1:
            self.outputValues[self.outputName] = readData1 | muxDecision
        elif controlSignal == 7:
            if readData1 < muxDecision:
                self.outputValues[self.outputName] = 1
            else:
                self.outputValues[self.outputName] = 0
        else:
            print("no valid control signal given")

    def setControlSignals(self):
        readData1 = self.inputValues[self.inputNameOne]
        muxDecision = self.inputValues[self.inputNameTwo]
        result = readData1 - muxDecision
        if result == 0:
            # rs - rt = 0, therefore zero signal is activated
            self.outputControlSignals[self.controlOutputName] = 1

class TestAlu(unittest.TestCase):
    def setUp(self):
        self.testInput1 = TestElement()
        self.testInput2 = TestElement()
        self.alu = Alu()
        self.testOutput = TestElement()

        self.testInput1.connect(
            [],
            ['readData1'],
            [],
            ['aluControl']
        )
        self.testInput2.connect(
            [],
            ['muxDecision'],
            [],
            []
        )
        self.alu.connect(
            [(self.testInput1, 'readData1'), (self.testInput2, 'muxDecision')],
            ['aluResult'],
            [(self.testInput1, 'aluControl')],
            ['zero']
        )
        self.testOutput.connect(
            [(self.alu, 'aluResult')],
            [],
            [(self.alu, 'zero')],
            []
        )

    def test_correct_behaviour(self):
        print("=======TESTING ADD=======")
        print("expected result: 150")
        self.testInput1.setOutputValue('readData1', 100)
        self.testInput2.setOutputValue('muxDecision', 50)
        self.testInput1.setControlSignals('aluControl', 2)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()

        self.testOutput.readInput()
        self.testOutput.readControlSignals()
        output = self.testOutput.inputValues['aluResult']
        control = self.testOutput.controlSignals['zero']
        print("output: ", output, "zero: ", control)
        if output == 150:
            print("TEST SUCCESS!")
        else:
            print("ADD FAILED!")
        print("=========================\n")

        print("=======TESTING SUB=======")
        print("expected result: 0")
        self.testInput1.setOutputValue('readData1', 100)
        self.testInput2.setOutputValue('muxDecision', 100)
        self.testInput1.setControlSignals('aluControl', 6)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        
        self.testOutput.readInput()
        self.testOutput.readControlSignals()
        output = self.testOutput.inputValues['aluResult']
        control = self.testOutput.controlSignals['zero']
        print("output: ", output, "zero: ", control)
        if output == 50:
            print("TEST SUCCESS!")
        else:
            print("SUB FAILED")
        print("=========================\n")

        print("=======TESTING AND=======")
        print("excpected result: 32")
        self.testInput1.setOutputValue('readData1', 100)
        self.testInput2.setOutputValue('muxDecision', 50)
        self.testInput1.setControlSignals('aluControl', 0)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        
        self.testOutput.readInput()
        output = self.testOutput.inputValues['aluResult']
        print("output: ", output)
        if output == 32:
            print("TEST SUCCESS!")
        else:
            print("AND FAILED")
        print("=========================\n")

        print("========TESTING OR=======")
        print("excpected result: 118")
        self.testInput1.setOutputValue('readData1', 100)
        self.testInput2.setOutputValue('muxDecision', 50)
        self.testInput1.setControlSignals('aluControl', 1)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        
        self.testOutput.readInput()
        output = self.testOutput.inputValues['aluResult']
        print("output: ", output)
        if output == 118:
            print("TEST SUCCESS!")
        else:
            print("OR FAILED")
        print("=========================\n")

        print("=======TESTING SLT=======")
        print("excpected result: 0")
        self.testInput1.setOutputValue('readData1', 100)
        self.testInput2.setOutputValue('muxDecision', 50)
        self.testInput1.setControlSignals('aluControl', 7)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        
        self.testOutput.readInput()
        output = self.testOutput.inputValues['aluResult']
        print("Result: ", output)
        if output == 0:
            print("TEST SUCCESS!")
        else:
            print("STL FAILED")
        print("=========================\n")