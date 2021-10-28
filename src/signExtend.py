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
        assert (len(control) == 0), 'SignExtend does not have a control signal'
        assert (len(outputSignalNames) == 0), 'SignExtend does not have control output'

        self.outputName = outputValueNames[0]
        self.inputName = inputSource[0][1]


    def writeOutput(self):
        signal = self.inputValues[self.inputName]

        # binStr now contains a string of binary code, that should e extended, reads the first bit and calculates accordingly
        # the binStrings are indexed from the top, meaning binStr[0] is the 16th bit.
        binStr = f'{signal:016b}'
        print("Writing output for signExtend...")
        print("input binary string", binStr)
        print("")
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

        if not unsigned:
            self.outputValues[self.outputName] = fromUnsignedWordToSignedWord(int(newString, 2))       
        else:
            self.outputValues[self.outputName] = int(newString, 2)


class TestSignExtend(unittest.TestCase):
    def setUp(self):
        self.signExtend = SignExtend()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['signal'],
            [],
            []
        )
        self.signExtend.connect(
            [(self.testInput, 'signal')],
            ['signExtended'],
            [],
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
        print("'negative' value...")
        self.testInput.setOutputValue('signal', 65278)
        
        self.signExtend.readInput()
        self.signExtend.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['signExtended']

        print(f'output: {output}')
        if output == -258:
            print("SUCCESS!")
        else:
            print("FAILED!")
        print("")
        print("'positive' value...")

        self.testInput.setOutputValue('signal', 32767)
        
        self.signExtend.readInput()
        self.signExtend.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['signExtended']

        print(f'output: {output}')
        if output == 32767:
            print("SUCCESS!")
        else:
            print("FAILED!")
        print("==========================\n")