'''
Implements CP Element for control
'''

from cpuElement import CPUElement

class Control(CPUElement):
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'Control should have 1 input'
        assert(len(outputValueNames) == 0), 'Control has only no outputs'
        assert(len(control) == 0), 'Control should have no control signal inputs'
        assert(len(outputSignalNames) == 9), 'Control should have 9 control outputs'

        self.inputName = inputSources[0][1]

        self.regDst = outputSignalNames[0]
        self.jump = outputSignalNames[1]
        self.branch = outputSignalNames[2]
        self.memRead = outputSignalNames[3]
        self.memtoReg = outputSignalNames[4]
        self.ALUOp = outputSignalNames[5]
        self.memWrite = outputSignalNames[6]
        self.ALUSrc = outputSignalNames[7]
        self.regWrite = outputSignalNames[8]

    def writeOutput(self):
        pass # randomControl has no data output

    def setControlSignal(self):
        src, inputValue = self.inputValues

        input = self.inputValues[self.inputName]
        
        # Do something depending on the input
        if inputValue == 103:
            return 0