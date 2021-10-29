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
        assert (len(outputValueNames) == 8), 'Instruction memory should have 8 outputs'
        assert(len(control) == 0), 'Instruction memory should not have control input'
        assert (len(outputSignalNames) == 0), 'Instruction memory should not have any control outputs'

        self.memory = self.memory
        self.inputName = inputSources[0][1]
        self.shiftLeftTwo = outputValueNames[0]
        self.control = outputValueNames[1]
        self.rs = outputValueNames[2]
        self.rt = outputValueNames[3]
        self.muxZero = outputValueNames[4]
        self.muxOne = outputValueNames[5]
        self.signExtend = outputValueNames[6]
        self.aluControl = outputValueNames[7]
    
    def writeOutput(self):
        print("Writing output for IM...")
        print("trying to access: ", self.inputValues[self.inputName])
        instruction = f'{self.memory[self.inputValues[self.inputName]]:032b}'
        print(f'instruction: {instruction}\n')

        shiftLeftTwo = instruction[6:32]
        control = instruction[0:6]
        rs = instruction[6:11]
        rt = instruction[11:16]
        muxZero = instruction[11:16]
        muxOne = instruction[16:21]
        signExtend = instruction[16:32]
        aluControl = instruction[26:32]

        self.outputValues[self.shiftLeftTwo] = int(shiftLeftTwo,2)
        self.outputValues[self.control] = int(control,2)
        self.outputValues[self.rs] = int(rs,2)
        self.outputValues[self.rt] = int(rt,2)
        self.outputValues[self.muxZero] = int(muxZero,2)
        self.outputValues[self.muxOne] = int(muxOne,2)
        self.outputValues[self.signExtend] = int(signExtend,2)
        self.outputValues[self.aluControl] = int(aluControl,2)
        

class TestInstructionMemory(unittest.TestCase):
    def setUp(self, memoryFile):
        self.IM = InstructionMemory(memoryFile)
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['address'],
            [],
            []
        )
        self.IM.connect(
            [(self.testInput, 'address')],
            ['shiftLeftTwo', 'control', 'rs', 'rt', 'muxZero', 'muxOne', 'signExtend', 'aluControl'],
            [],
            []
        )
        self.testOutput.connect(
            [(self.IM, 'shiftLeftTwo'), (self.IM, 'control'), (self.IM, 'rt'), (self.IM, 'rs'), (self.IM, 'muxZero'), (self.IM, 'muxOne'), (self.IM, 'signExtend'), (self.IM, 'aluControl')],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        
        self.IM.memory[2820997123] = 2888105987

        self.testInput.setOutputValue('address', 2820997123)

        self.IM.readInput()
        self.IM.writeOutput()
        self.testOutput.readInput()

        print("========TESTING IM========")
        print(f'instruction: {2888105987:032b}')

        shiftLeftTwo = self.testOutput.inputValues['shiftLeftTwo']
        print(f'shiftLeftTwo: {shiftLeftTwo:026b}')

        control = self.testOutput.inputValues['control']
        print(f'control: {control:06b}')

        rs = self.testOutput.inputValues['rs']
        print(f'rt: {rs:05b}')

        rt = self.testOutput.inputValues['rt']
        print(f'rs: {rt:05b}')

        muxZero = self.testOutput.inputValues['muxZero']
        print(f'muxZero: {muxZero:05b}')

        muxOne = self.testOutput.inputValues['muxOne']
        print(f'muxOne: {muxOne:05b}')

        signExtend = self.testOutput.inputValues['signExtend']
        print(f'signExtend: {signExtend:016b}')

        aluControl = self.testOutput.inputValues['aluControl']
        print(f'aluControl: {aluControl:06b}')
        print("==========================\n")