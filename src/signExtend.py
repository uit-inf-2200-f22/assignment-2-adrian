'''
Implements a CPU element for extending a 16bit number, and keeping its signed, or most significant bit 
'''
from cpuElement import CPUElement

class signExtend(CPUElement):

    def connect(self, inputSource, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSource, outputValueNames, control, outputSignalNames)

        assert (len(inputSource) == 1), 'SignExtend should only have one input'
        assert (len(outputValueNames) == 1), 'SignExtend has only one output'
        assert (len(control) == 0), 'SignExtend does not have a control signal'
        assert (len(outputSignalNames) == 0), 'SignExtend does not have control output'

        self.outputName = outputValueNames[0]

    def writeOutput(self):
        n = self.outputName
        nStr = str(n)

        # Should be implemented later, have to see how python handles the 15-0 bit part when it is passed as an integer

