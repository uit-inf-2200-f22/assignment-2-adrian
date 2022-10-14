'''
Code written for inf-2200, University of Tromso
'''

from tkinter import TRUE
from pc import PC
from add import Add
from mux import Mux
from registerFile import RegisterFile, TestRegisterFile
from instructionMemory import InstructionMemory, TestInstructionMemory
from dataMemory import DataMemory, TestDataMemory
from constant import Constant
from control import Control, TestControl
from alu import Alu, TestAlu
from aluControl import AluControl, TestAluControl
from signExtend import SignExtend, TestSignExtend
from shiftLeftTwo import ShiftLeftTwo
from memory import Memory, TestMemory
from pcJump import PcJump, TestPcJump
from bne import BNE, TestBNE
from andGate import And

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

        # the self.startAddress function literally does not work, even tried modifying it myself
        startAddress = next(iter(sorted(self.instructionMemory.memory.keys())))
        print(f'start address: {startAddress}')

        self.addPC = Add()
        self.constant4 = Constant(4)
        self.control = Control()
        self.regMux = Mux()
        self.pc = PC(startAddress)
        self.signExtend = SignExtend()
        self.shiftLeftTwoPC = ShiftLeftTwo()
        self.pcJump = PcJump()
        self.aluMux = Mux()
        self.aluControl = AluControl()
        self.alu = Alu()
        self.shiftLeftTwo = ShiftLeftTwo()
        self.addBranch = Add()
        self.bne = BNE()
        self.andGate = And()
        self.pcIncOrBranchMux = Mux()
        self.jmpOrBranchMux = Mux()
        self.dmMux = Mux()
        

        self.elements = [self.pc, self.instructionMemory,
                         self.constant4, self.addPC,
                         self.control, self.regMux,
                         self.registerFile, self. signExtend,
                         self.aluControl, self.aluMux,
                         self.alu, self.shiftLeftTwo,
                         self.shiftLeftTwoPC, self.pcJump,
                         self.bne, self.dataMemory,
                         self.dmMux, self.andGate,
                         self.addBranch, self.pcIncOrBranchMux,
                         self.jmpOrBranchMux]

        self._connectCPUElements()

        '''MEMORY TEST'''
        # self.memory = TestMemory()
        # self.memory.setUp(memoryFile)
        # self.memory.test_correct_behaviour()

        '''INSTRUCTION MEMORY TEST'''
        # self.testIM = TestInstructionMemory()
        # self.testIM.setUp(memoryFile)
        # self.testIM.test_correct_behaviour()

        '''DATAMEMORY TEST'''
        # self.testDataMemory = TestDataMemory()
        # self.testDataMemory.setUp(memoryFile)
        # self.testDataMemory.test_correct_behaviour()

        '''CONTROL TEST'''
        # self.testControl = TestControl()
        # self.testControl.setUp()
        # self.testControl.test_correct_behaviour()

        '''ALUCONTROL TEST'''
        # self.testAluControl = TestAluControl()
        # self.testAluControl.setUp()        
        # self.testAluControl.test_correct_behaviour()

        '''ALU TEST'''
        # self.testAlu = TestAlu()
        # self.testAlu.setUp()
        # self.testAlu.test_correct_behaviour()

        '''SIGN EXTEND TEST'''
        # self.testSignExtend = TestSignExtend()
        # self.testSignExtend.setUp()
        # self.testSignExtend.test_correct_behaviour()

        '''REGISTER FILE TEST'''
        # self.testRegisterFile = TestRegisterFile()
        # self.testRegisterFile.setUp()
        # self.testRegisterFile.test_correct_behaviour()

        '''PCJUMP TEST'''
        # self.pcJump = TestPcJump()
        # self.pcJump.setUp()
        # self.pcJump.test_correct_behaviour()

        '''BNE TEST'''
        # self.bne = TestBNE()
        # self.bne.setUp()
        # self.bne.test_correct_behaviour()

    def _connectCPUElements(self):
        self.pc.connect(
            [(self.jmpOrBranchMux, 'nextAddress')],
            ['pcAddress'],
            [],
            []
        )

        self.instructionMemory.connect(
            [(self.pc, 'pcAddress')],
            ['shiftLeftTwo', 'control', 'rs', 'rt', 'muxZero', 'muxOne', 'signExtend', 'aluControl'],
            [],
            []
        )
        
        self.control.connect(
            [(self.instructionMemory, 'control')],
            [],
            [],
            ['regDst', 'aluSrc', 'memtoReg', 'regWrite', 'memRead', 'memWrite', 'branch', 'aluOp', 'jump', 'bne']
        )

        self.regMux.connect(
            [(self.instructionMemory, 'muxZero'), (self.instructionMemory, 'muxOne')],
            ['muxOut'],
            [(self.control, 'regDst')],
            [],
            'register destination Mux'
        )

        self.registerFile.connect(
            [(self.instructionMemory, 'rs'), (self.instructionMemory, 'rt'), (self.regMux, 'muxOut'), (self.dmMux, 'regWrite')],
            ['dataA', 'dataB'],
            [(self.control, 'regWrite')],
            []
        )

        self.signExtend.connect(
            [(self.instructionMemory, 'signExtend')],
            ['signExtendOutput'],
            [(self.control, 'aluOp')],
            []
        )

        self.aluMux.connect(
            [(self.registerFile, 'dataB'), (self.signExtend, 'signExtendOutput')],
            ['aluMuxOutput'],
            [(self.control, 'aluSrc')],
            [],
            'aluSrc Mux'
        )

        self.aluControl.connect(
            [(self.instructionMemory, 'aluControl')],
            [],
            [(self.control, 'aluOp')],
            ['aluOperation']
        )

        self.alu.connect(
            [(self.registerFile, 'dataA'), (self.aluMux, 'aluMuxOutput')],
            ['aluResult'],
            [(self.aluControl, 'aluOperation')],
            ['zeroSignal']
        )

        self.dataMemory.connect(
            [(self.alu, 'aluResult'), (self.registerFile, 'dataB')],
            ['memoryData'],
            [(self.control, 'memRead'), (self.control, 'memWrite')],
            []
        )
        
        self.dmMux.connect(
            [(self.alu, 'aluResult'), (self.dataMemory, 'memoryData')],
            ['regWrite'],
            [(self.control, 'memtoReg')],
            [],
            'data memory Mux'
        )

        self.shiftLeftTwo.connect(
            [(self.signExtend, 'signExtendOutput')],
            ['shiftLeftTwoOutput'],
            [],
            [],
        )

        self.addBranch.connect(
            [(self.addPC, 'pcIncrement'), (self.shiftLeftTwo, 'shiftLeftTwoOutput')],
            ['branchAdd'],
            [],
            [],
            'branch destination adder'
        )

        self.pcIncOrBranchMux.connect(
            [(self.addPC, 'pcIncrement'), (self.addBranch, 'branchAdd')],
            ['pcBranchOutput'],
            [(self.andGate, 'branch')],
            [],
            'pcIncOrBranchMux'
        )
        
        self.jmpOrBranchMux.connect(
            [(self.pcIncOrBranchMux, 'pcBranchOutput'), (self.pcJump, 'jumpAddress')],
            ['nextAddress'],
            [(self.control, 'jump')],
            [],
            'jmpOrBranchMux'
        )

        self.bne.connect(
            [],
            [],
            [(self.control, 'bne'), (self.alu, 'zeroSignal')],
            ['bneOutput']
        )
        
        self.andGate.connect(
            [],
            [],
            [(self.control, 'branch'), (self.bne, 'bneOutput')],
            ['branch']
        )

        self.shiftLeftTwoPC.connect(
            [(self.instructionMemory, 'shiftLeftTwo')],
            ['shiftLeftTwoPCOutput'],
            [],
            []
        )

        self.pcJump.connect(
            [(self.shiftLeftTwoPC, 'shiftLeftTwoPCOutput'), (self.addPC, 'pcIncrement')],
            ['jumpAddress'],
            [],
            []
        )

        self.constant4.connect(
            [],
            ['constant'],
            [],
            []
        )

        self.addPC.connect(
            [(self.pc, 'pcAddress'), (self.constant4, 'constant')],
            ['pcIncrement'],
            [],
            [],
            'pc increment output'
        )


    def startAddress(self):
        '''
        Returns first instruction from instruction memory
        '''

        return 20000000
        # mem = self.instructionMemory.memory
        # print(mem)
        # return next(iter(mem))
        # print(next(iter(sorted(self.instructionMemory.memory.keys()))))
        # return next(iter(sorted(self.instructionMemory.memory.keys())))

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

        stopping = False

        # The following is just a small sample implementation

        # self.pc.writeOutput()
        print(f'\n===========CYCLE {self.nCycles}===========')
        for elem in self.elements:
            elem.readControlSignals()
            elem.readInput()
            elem.writeOutput()
            elem.setControlSignals()
        self.registerFile.readInput()
        self.registerFile.writeOutput()
        self.registerFile.printAll()
        self.dataMemory.printAll()
        print(f'==========================================\n')
        if stopping:
            ncyclesstop = 20
            if self.nCycles > ncyclesstop:
                raise Exception(f'{ncyclesstop} cycles')
        # self.pc.readInput()

        