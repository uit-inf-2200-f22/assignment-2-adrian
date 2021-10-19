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
       
        # binStr now contains a string of binary code 0-31 bit, reads the 15th, if 1, makes 15-31 1, if not, 0
        # the binStrings are indexed from the top, meaning binStr[0] is the 32nd bit.
        binStr = f'{signal:032b}'
        print("=======STARTING=======")
        print("input binary string", binStr)
        print("16 bit that should be extended:    ", binStr[16:32])
        i = 0
        newString = ""
        if binStr[16] == "1":
            newNum = int(binStr[16:32], 2)
            # the binary string in this case is 00100011100011001111111111111111
            # and what should be extended is 1111111111111111, following two's complement, this would be equal to -1,
            # however, python treats this number as
            print("This should be the number!: ", fromSignedWordToUnsignedWord(newNum))
        else:
            while i <= 15:
                newString += "0"
                print("extending sign... " + newString)
                i += 1
        newString += binStr[16:32]
        print("this is inputStr : " + binStr)
        print("this is newString: " + newString)

        print("converting to decimal...")

        print("=======RETURNING=======")
        self.outputValues[self.outputName] = newString



class testSignExtend(unittest.TestCase):
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

    def test_correct_behavior(self):

        self.testInput.setOutputValue('signal', 596443135)

        self.signExtend.readInput()
        self.signExtend.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['signExtended']

        print(output)
