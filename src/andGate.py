'''
Implements a cpuElement for an and-gate
'''
import unittest
from cpuElement import CPUElement
from testElement import TestElement

class And(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0),         'And gate has no inputs'
        assert(len(outputValueNames) == 0),     'And gate has no outputs'
        assert(len(control) == 2),              'And gate has 2 control inputs'
        assert(len(outputSignalNames) == 1),    'And gate has 1 control signal output'

        self.controlInput = control[0][1]
        self.zeroControl = control[1][1]
        self.signalName = outputSignalNames[0]

    def writeOutput(self):
        self.outputValues['none'] = 0

    def setControlSignals(self):
        print("------AndGate------")
        control = self.controlSignals[self.controlInput] 
        zero = self.controlSignals[self.zeroControl]
        # print("Writing control output for andGate...")
        print(f'zero signal input {zero}')
        print(f'control signal: {control}')
        if control == 1 and zero == 1:
            print("AND GATE output: 1")
            print("BRANCHING\n")
            self.outputControlSignals[self.signalName] = 1
        else:
            print("AND GATE output: 0\n")
            self.outputControlSignals[self.signalName] = 0
