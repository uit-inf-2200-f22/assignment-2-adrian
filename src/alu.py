'''
Implements an arithmetic logic unit
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement
from common import Overflow, fromUnsignedWordToSignedWord, fromSignedWordToUnsignedWord

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
        print("Writing output for ALU...")
        controlSignal = self.controlSignals[self.controlInputName]
        # print(f'readData1: {readData1}')
        # print(f'readData2: {muxDecision}')

        if controlSignal == 2:
            print("add")
            result = readData1 + muxDecision
            print("adding", readData1, "and", muxDecision)
            if result > 2147483647:
                raise Overflow("Overflow on add")
            else:
                self.outputValues[self.outputName] = result

        elif controlSignal == 3:
            print("addiu/addu")
            result = readData1 + muxDecision
            if result > 2147483647:
                # Overflow positive
                print("overflowing...")
                self.outputValues[self.outputName] = fromUnsignedWordToSignedWord(int(f'{result:033b}'[1:33], 2))
            elif result < -2147483648:
                # Overflow negative
                print("overflowing...")
                # If you add 1, then perform an XOR, you get the correct number on the opposite side
                tmp = readData1 + muxDecision + 1
                self.outputValues[self.outputName] = int(f'{tmp:032b}'[1:33], 2) ^ 0xffffffff
            else:
                self.outputValues[self.outputName] = result

        elif controlSignal == 6:
            print("sub")
            result = readData1 - muxDecision
            if result < -2147483648:
                raise Overflow("Overflow on sub")
            else:
                self.outputValues[self.outputName] = result

        elif controlSignal == 4:
            print("subu")
            result = readData1 - muxDecision
            if result < 0:
                print("snipping")
                tmp = fromSignedWordToUnsignedWord(result)
                binStr = f'{tmp:033b}'
                binSnip = int(binStr[1:33], 2)
                self.outputValues[self.outputName] = binSnip
            else:
                self.outputValues[self.outputName] = result

        elif controlSignal == 0:
            self.outputValues[self.outputName] = readData1 & muxDecision
            
        elif controlSignal == 1:
            self.outputValues[self.outputName] = readData1 | muxDecision
        
        # nor = negated or, in case of 
        elif controlSignal == 5:
            print("nor")
            newStr = ""
            len1 = len(bin(readData1))-2
            len2 = len(bin(muxDecision))-2

            if len1 > len2:
                binStr1 = f'{readData1:0{len1}b}'
                binStr2 = f'{muxDecision:0{len1}b}'
                max = len1
            else:
                binStr1 = f'{readData1:0{len2}b}'
                binStr2 = f'{muxDecision:0{len2}b}'
                max = len2

            print(f'{binStr1} vs {binStr2}')
            i = 0
            while i < max:
                if binStr1[i] == '0' and binStr2[i] == '0':
                    newStr += "1"
                else:
                    newStr += "0"
                i += 1
            print(newStr)
            self.outputValues[self.outputName] = int(newStr,2)

        elif controlSignal == 7:
            if readData1 < muxDecision:
                self.outputValues[self.outputName] = 1
            else:
                self.outputValues[self.outputName] = 0
                
        # Here, in order to left shift 16 times, and be left with a 32 bit number, we neet to split it
        elif controlSignal == 8:
            print("shifting left")
            print(f'binStr: {muxDecision:032b}')
            result = muxDecision << 16
            binres = f'{result:048b}'[16:48]
            print(f'after shift: {binres}\t{int(binres, 2)}')
            self.outputValues[self.outputName] = int(binres, 2)
        else:
            print("no valid control signal given")
        print("alu output: ", self.outputValues[self.outputName])
        print("Alu complete\n")

    def setControlSignals(self):
        print("Writing control output for ALU...")
        readData1 = self.inputValues[self.inputNameOne]
        muxDecision = self.inputValues[self.inputNameTwo]
        result = readData1 - muxDecision
        print(f'readData1: {readData1}')
        print(f'readData2: {muxDecision}')
        print(f'readData1 - readData2: {result}\n')
        if result == 0:
            print(f'zero signal: 1')
            self.outputControlSignals[self.controlOutputName] = 1
        else:
            print(f'zero signal: 0')
            self.outputControlSignals[self.controlOutputName] = 0

        

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
        print("========TESTING ALU=======")
        print("AND...")
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
            print("\tTEST SUCCESS!")
        else:
            print("\tADD FAILED!")
        print("")

        print("SUB...")
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
        if output == 0:
            print("\tTEST SUCCESS!")
        else:
            print("\tSUB FAILED")
        print("")

        print("AND...")
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
            print("\tTEST SUCCESS!")
        else:
            print("\tAND FAILED")
        print("")

        print("OR...")
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
            print("\tTEST SUCCESS!")
        else:
            print("\tOR FAILED")
        print("")

        print("NOR...")
        print("excpected results: 4")
        self.testInput1.setOutputValue('readData1', 9)
        self.testInput2.setOutputValue('muxDecision', 2)
        self.testInput1.setControlSignals('aluControl', 5)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        
        self.testOutput.readInput()
        output = self.testOutput.inputValues['aluResult']
        print("Result: ", output)
        if output == 4:
            print("\tTEST SUCCESS!")
        else:
            print("\tNOR FAILED")
        print("")

        print("STL...")
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
            print("\tTEST SUCCESS!")
        else:
            print("\tSTL FAILED")
        print("")

        print("ADDU...")
        print("excpected results: 20101")
        self.testInput1.setOutputValue('readData1', 20000)
        self.testInput2.setOutputValue('muxDecision', 101)
        self.testInput1.setControlSignals('aluControl', 3)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        
        self.testOutput.readInput()
        output = self.testOutput.inputValues['aluResult']
        print("Result: ", output)
        if output == 20101:
            print("\tTEST SUCCESS!")
        else:
            print("\tADDU FAILED")
        print("")

        print("SUBU...")
        print("excpected results: 19899")
        self.testInput1.setOutputValue('readData1', 20000)
        self.testInput2.setOutputValue('muxDecision', 101)
        self.testInput1.setControlSignals('aluControl', 4)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()
        
        self.testOutput.readInput()
        output = self.testOutput.inputValues['aluResult']
        print("Result: ", output)
        if output == 19899:
            print("\tTEST SUCCESS!")
        else:
            print("\tSUBU FAILED")
        print("")

        print("ADDIU posofl...")
        print("expected result: -2147483648")
        self.testInput1.setOutputValue('readData1', 2147483647)
        self.testInput2.setOutputValue('muxDecision', 1)
        self.testInput1.setControlSignals('aluControl', 3)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()

        self.testOutput.readInput()
        self.testOutput.readControlSignals()
        output = self.testOutput.inputValues['aluResult']
        control = self.testOutput.controlSignals['zero']
        print("output: ", output, "zero: ", control)
        if output == -2147483648:
            print("\tTEST SUCCESS!")
        else:
            print("\tADD FAILED!")
        print("")

        print("ADDIU negofl...")
        print("expected result: 2147483647")
        self.testInput1.setOutputValue('readData1', -2147483648)
        self.testInput2.setOutputValue('muxDecision', -1)
        self.testInput1.setControlSignals('aluControl', 3)

        self.alu.readInput()
        self.alu.readControlSignals()
        self.alu.writeOutput()
        self.alu.setControlSignals()

        self.testOutput.readInput()
        self.testOutput.readControlSignals()
        output = self.testOutput.inputValues['aluResult']
        control = self.testOutput.controlSignals['zero']
        print("output: ", output, "zero: ", control)
        if output == 2147483647:
            print("\tTEST SUCCESS!")
        else:
            print("\tADD FAILED!")
        print("==========================\n")

if __name__ == '__main__':
    unittest.main()
