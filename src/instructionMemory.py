'''
Implements CPU element for Instruction Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement
from memory import Memory
from pc import PC
class InstructionMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        assert (len(inputSources) == 1), 'Instruction memory should only have 1 input'
        assert (len(outputValueNames) == 1), 'Instruction memory should only have 1 output'
        assert(len(control) == 0), 'Instruction memory should not have control input'
        assert (len(outputSignalNames) == 0), 'Instruction memory should not have any control outputs'

        self.inputName = inputSources[0][1]
        self.outputName = outputValueNames[0]
        self.memory = self.memory
    
    def writeOutput(self):
        
        self.outputValues[self.outputName] = self.inputValues[self.inputName]   # Med antalgelse at instructionMemory.readInput() blir kjørt før dette, kan outputValues dictionariet få en key self.inputname, med verdi som ligger mappet til self.inputName i self.inputValues.


class testInstructionMemory(unittest.TestCase):
    def setUp(self, memoryFile):
        self.instructionMem = InstructionMemory(memoryFile)
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['address'],
            [],
            []
        )
        self.instructionMem.connect(
            [(self.testInput, 'address')],
            ['instruction'],
            [],
            []
        )
        self.testOutput.connect(
            [(self.instructionMem, 'instruction')],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):

        self.testInput.setOutputValue('address', 1918171615)

        self.instructionMem.readInput()
        self.instructionMem.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues['instruction']

        self.assertEqual(output, 1918171615)

        # bare for en kjapp print confirmation
        if output == 1918171615:
            print("success!")
            return 0
        
        