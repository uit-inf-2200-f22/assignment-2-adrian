'''
Code written for inf-2200, University of Tromso
'''

from pc import PC
from add import Add
from mux import Mux
from registerFile import RegisterFile
from instructionMemory import InstructionMemory, TestInstructionMemory
from dataMemory import DataMemory
from constant import Constant
from randomControl import RandomControl
from alu import Alu, TestAlu
from aluControl import AluControl, TestAluControl
from signExtend import SignExtend, TestSignExtend

class MIPSSimulator():
    '''Main class for MIPS pipeline simulator.

    Provides the main method tick(), which runs pipeline
    for one clock cycle.

    '''

    def __init__(self, memoryFile):
        self.nCycles = 0  # Used to hold number of clock cycles spent executing instructions

        self.dataMemory = DataMemory(memoryFile)
        self.instructionMemory = InstructionMemory(memoryFile)
        self.registerFile = RegisterFile()

        self.constant3 = Constant(3)
        self.constant4 = Constant(4)
        self.randomControl = RandomControl()
        self.mux = Mux()
        self.adder = Add()
        self.pc = PC(101)#PC(PC(self.startAddress))       # Replace with PC(random number) if you want to test
        self.alu = Alu()


        self.elements = [self.constant3, self.constant4,
                         self.randomControl, self.adder, self.mux]

        self._connectCPUElements()

        '''INSTRUCTION MEMORY TEST'''
        # self.testIM = TestInstructionMemory()
        # self.testIM.setUp(memoryFile)
        # self.testIM.test_correct_behavior()

        '''SIGN EXTEND TEST'''
        # self.testSignExtend = TestSignExtend()
        # self.testSignExtend.setUp()
        # self.testSignExtend.test_correct_behavior()

        '''ALUCONTROL TEST'''
        # self.testAluControl = TestAluControl()
        # self.testAluControl.setUp()        
        # self.testAluControl.test_correct_behavior()

        '''ALU TEST'''
        self.testAlu = TestAlu()
        self.testAlu.setUp()
        self.testAlu.test_correct_behavior()


    def _connectCPUElements(self):
        self.constant3.connect(
            [],
            ['constant'],
            [],
            []
        )

        self.constant4.connect(
            [],
            ['constant'],
            [],
            []
        )

        self.randomControl.connect(
            [],
            [],
            [],
            ['randomSignal']
        )

        self.adder.connect(
            [(self.pc, 'pcAddress'), (self.constant4, 'constant')],
            ['sum'],
            [],
            []
        )

        self.mux.connect(
            [(self.adder, 'sum'), (self.constant3, 'constant')],
            ['muxOut'],
            [(self.randomControl, 'randomSignal')],
            []
        )

        self.pc.connect(
            [(self.mux, 'muxOut')],
            ['pcAddress'],
            [],
            []
        )
        
        self.dataMemory.connect(
            [(self.pc, 'pcAddress'), (self.alu, 'aluResult')],
            ['memoryData'],
            [(self.randomControl, 'memRead'), (self.randomControl, 'memWrite')],
            []
        )

        self.instructionMemory.connect(
            [(self.pc, 'address')],
            ['instruction'],
            [],
            []
        )

        # self.alu.connect(
        #     [],
        #     [],
        #     [],
        #     []
        # )

    def startAddress(self):
        '''
        Returns first instruction from instruction memory
        '''
        return next(iter(sorted(self.instructionMemory.memory.keys())))

    def clockCycles(self):
        '''Returns the number of clock cycles spent executing instructions.'''

        return self.nCycles

    def dataMemory(self):
        '''Returns dictionary, mapping memory addresses to data, holding
        data memory after instructions have finished executing.'''

        return self.dataMemory.memory

    def registerFile(self):
        '''Returns dictionary, mapping register numbers to data, holding
        register file after instructions have finished executing.'''

        return self.registerFile.register

    def printDataMemory(self):
        self.dataMemory.printAll()

    def printRegisterFile(self):
        self.registerFile.printAll()

    def tick(self):
        '''Execute one clock cycle of pipeline.'''

        self.nCycles += 1

        # The following is just a small sample implementation

        # self.pc.writeOutput()

        # for elem in self.elements:
        #     elem.readControlSignals()
        #     elem.readInput()
        #     elem.writeOutput()
        #     elem.setControlSignals()

        # self.pc.readInput()
