'''
Implements a CPU element for extending a 16bit number, and keeping its signed, or most significant bit 
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement
from common import fromSignedWordToUnsignedWord, fromUnsignedWordToSignedWord

class SignExtend(CPUElement):

    def connect(self, inputSource, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSource, outputValueNames, control, outputSignalNames)

        assert (len(inputSource) == 1), 'SignExtend should only have one input'
        assert (len(outputValueNames) == 1), 'SignExtend has only one output'
        assert (len(control) == 1), 'SignExtend should only have 1 control input'
        assert (len(outputSignalNames) == 0), 'SignExtend does not have control output'

        self.outputName = outputValueNames[0]
        self.inputName = inputSource[0][1]
        self.lui = control[0][1]


    def writeOutput(self):
        signal = self.inputValues[self.inputName]
        controlOne = self.controlSignals[self.lui]

        # binStr now contains a string of binary code, that should e extended, reads the first bit and calculates accordingly
        # the binStrings are indexed from the top, meaning binStr[0] is the 16th bit.
        binStr = f'{signal:016b}'
        print("Writing output for signExtend...")
        print("input binary string", binStr)
        i = 0
        newString = ""                                  # Since adding characters at the start of a string in python
        if binStr[0] == "1":
            unsigned = False
            while i <= 15:
                newString += "1"
                i += 1
        else:
            unsigned = True
            while i <= 15:
                newString += "0"
                i += 1
        newString += binStr
        print("new result")
        print(f'str: {newString}')
        print(f'int: {int(newString, 2)}')
        if not unsigned:
            # !!    UPDATE 2022 FALL, I now know the branch does not shift 16, as in LUI, therefore we now longer require the branch control signal. Don't know why i thought this.   !!
            # Since the outgoing value, in case of negative sign bit, is a negative integer, 
            # the resulting lui shiftleft and branch addition might turn out wrong, therefor, 
            # we check for that, and send out the pure, two's complement representation of the 
            # number, in positive a positive integer form. This is a python problem when converting to INT.
            if controlOne == 3:
                result = int(newString, 2)
                self.outputValues[self.outputName] = result
                print("potato")
                print(f'output: \n int:{result} \nstr: {result:032b}')
            else:
                result = fromUnsignedWordToSignedWord(int(newString, 2))
                self.outputValues[self.outputName] = result
                print("tomato")
                print(f'output: \nint: {result} \nstr: {result:032b}')
        else:
            result = int(newString, 2)
            self.outputValues[self.outputName] = int(newString, 2)
            print(f'output: \nint: {result} \nstr: {result:032b}')
        print("")


class TestSignExtend(unittest.TestCase):
    def setUp(self):
        self.signExtend = SignExtend()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['signal'],
            [],
            ['aluOp']
        )
        self.signExtend.connect(
            [(self.testInput, 'signal')],
            ['signExtended'],
            [(self.testInput, 'aluOp')],
            []
        )
        self.testOutput.connect(
            [(self.signExtend, 'signExtended')],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        
        print("========TESTING SE========")
        print("\t'negative' value...")
        self.testInput.setOutputValue('signal', 65535)
        self.testInput.setControlSignals('aluOp', 0)

        self.signExtend.readInput()
        self.signExtend.readControlSignals()
        self.signExtend.writeOutput()
        self.testOutput.readInput()

        predictedvalue1 = -1
        print("expected value: ", predictedvalue1)

        output = self.testOutput.inputValues['signExtended']

        print(f'output: {output}')
        if output == predictedvalue1:
            print("SUCCESS!")
        else:
            print("FAILED!")
        print("")

        print("\t'positive' value...")
        self.testInput.setOutputValue('signal', 32767)
        self.testInput.setControlSignals('aluOp', 0)
        
        self.signExtend.readInput()
        self.signExtend.readControlSignals()
        self.signExtend.writeOutput()
        self.testOutput.readInput()

        expectedvalue2 = 32767
        print("expected value: ", expectedvalue2)

        output = self.testOutput.inputValues['signExtended']

        print(f'output: {output}')
        if output == expectedvalue2:
            print("SUCCESS!")
        else:
            print("FAILED!")
        print("")

        print("\t'negative' value LUI...")
        self.testInput.setOutputValue('signal', 36865)
        self.testInput.setControlSignals('aluOp', 3)
        
        self.signExtend.readInput()
        self.signExtend.readControlSignals()
        self.signExtend.writeOutput()
        self.testOutput.readInput()

        expectedvalue2 = 4294938625
        print("expected value: ", expectedvalue2)

        output = self.testOutput.inputValues['signExtended']

        print(f'output: {output}')
        if output == expectedvalue2:
            print("SUCCESS!")
        else:
            print("FAILED!")
        print("")

        print("\t'positive' value LUI...")
        self.testInput.setOutputValue('signal', 4097)
        self.testInput.setControlSignals('aluOp', 3)
        
        self.signExtend.readInput()
        self.signExtend.writeOutput()
        self.testOutput.readInput()

        expectedvalue2 = 4097
        print("expected value: ", expectedvalue2)

        output = self.testOutput.inputValues['signExtended']

        print(f'output: {output}')
        if output == expectedvalue2:
            print("SUCCESS!")
        else:
            print("FAILED!")
        print("==========================\n")

if __name__ == '__main__':
    unittest.main()
