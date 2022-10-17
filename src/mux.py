'''
Code written for inf-2200, University of Tromso
'''

from os import name
import unittest
from cpuElement import CPUElement
from testElement import TestElement

class Mux(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames, name):
        '''
        Connect mux to input sources and controller
        
        Note that the first inputSource is input zero, and the second is input 1
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)
        
        assert(len(inputSources) == 2), 'Mux should have two inputs'
        assert(len(outputValueNames) == 1), 'Mux has only one output'
        assert(len(control) == 1), 'Mux has one control signal'
        assert(len(outputSignalNames) == 0), 'Mux does not have any control output'
        
        # Basically det som står her, er basically for å splitte opp evnt lister osv. slik som inputZero og inputOne, de kommer begge fra inputSources
        self.inputZero = inputSources[0][1]         # Lager to inputs som inneholder navnet til inputene, her: input zero
        self.inputOne = inputSources[1][1]          # her lages navnet til input nummer 2
        self.outputName = outputValueNames[0]       # OutputValueNames er bare en string, som har navnet til outputet
        self.controlName = control[0][1]            # Henter verdi nummer 2 fra første element i dictionary, altså navnet til control signalet

        self.name = name

    def writeOutput(self):
        muxControl = self.controlSignals[self.controlName]
        print(f'------{self.name}------')
        print(f'control signal: {muxControl}')
        assert(isinstance(muxControl, int))
        assert(not isinstance(muxControl, bool))  # ...  (not bool)
        assert(muxControl == 0 or muxControl == 1), 'Invalid mux control signal value: %d' % (muxControl)

        # print(f'input 0 {self.inputValues[self.inputZero]}')
        # print(f'input 1 {self.inputValues[self.inputOne]}')

        if muxControl == 0:
            # print("outputting 0\n")
            self.outputValues[self.outputName] = self.inputValues[self.inputZero]
        else:
            # print("outputting 1\n")
            self.outputValues[self.outputName] = self.inputValues[self.inputOne]

        print("")

    # def printOutput(self):
        '''
        # Debug function that prints the output value
        '''
        # print('mux.output = %d' % (self.outputValues[self.outputName],))


class TestMux(unittest.TestCase):
    def setUp(self):
        self.mux = Mux()
        self.testInput = TestElement()
        self.testOutput = TestElement()
        
        self.testInput.connect(
            [],
            ['dataA', 'dataB'],
            [],
            ['muxControl']
        )
        
        self.mux.connect(
            [(self.testInput, 'dataA'), (self.testInput, 'dataB')], # Her sendes objektet TestElement, i for am self.testInput inn som verdi mappet til både dataA og dataB
            ['muxData'],
            [(self.testInput, 'muxControl')],                       # Samme her...
            []
        )
        
        self.testOutput.connect(
            [(self.mux, 'muxData')],                                # self.testOutput er da et objekt som skal motta data, da sendes bare self.mux, som er et mux objekt
            [],                                                     # inn som et argument, eller verdi, rart tar objektet som tar imot verdien å leser dette av ved å
            [],                                                     # kalle på de rette funksjonenen?
            []
        )
    
    def test_correct_behaviour(self):
        self.testInput.setOutputValue('dataA', 10)                  # Setter output verdi som mappes til 'dataA' til 10,
        self.testInput.setOutputValue('dataB', 20)                  # Setter output verdi som mappes til 'dataB' til 20
        
        self.testInput.setOutputControl('muxControl', 0)            # Setter verdien som mappes til 'muxControl' til 0
        
        self.mux.readInput()                                        # Leser input fra det som da er testInput, som ble connecta da self.mux ble calla me self. input som argument self.inputValues inneholder nå en verdi som er mappet til name, kopierer egentlig bare verdiene fra inputen!
        self.mux.readControlSignals()                               # Leser control signalet, som er 0, self.controlSignals har nå en control verdi, som er mappet til navnet gitt med controlsignalet
        self.mux.writeOutput()                                      # Nå inneholder self.inputValues 2 navn som mapper til 2 forskjellige verdier, og self.controlsignal inneholder et navn, som mapper til en verdi, som ble satt tidligere. basert på denne verdien, vil nå outputValue ha et tall mappet til det navnet vi har designert  
        self.testOutput.readInput()                                 # Nå kjører det objektet som skal ta imot outputen til MUX'en en readinput, som er self.mux mappet til 'muxData', samme navnet som verdien ble mappet til i mux. inputValues inneholder nå en et mux objekt
        output = self.testOutput.inputValues['muxData']             # Henter ut mux objektet som er mappet til 'muxData'? nei, se kommentar 4 linjer ned
        
        self.assertEqual(output, 10)                                # sammenligner nå mux objektet med tallet 10... what?
                                                                    # Nu skjønne æ... mux OBJEKTET blir sendt inn som et argument i readInput. Fordi i readInput så kalle den basically mux.getOutputValue, som leser av self.outputValue til muxen, og mapper den i en ny inputValues liste
        self.testInput.setOutputControl('muxControl', 1)
        
        self.mux.readInput()
        self.mux.readControlSignals()
        self.mux.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues['muxData']
        
        self.assertEqual(output, 20)
        
    def assert_callback(self, arg):
        self.testInput.setOutputControl('muxControl', arg)
        self.mux.readControlSignals()
        self.mux.writeOutput()
        
    def test_assert_on_incorrect_input(self):
        self.testInput.setOutputValue('dataA', 10)
        self.testInput.setOutputValue('dataB', 20)
        self.mux.readInput()
        
        self.assertRaises(AssertionError, self.assert_callback, '1')
        self.assertRaises(AssertionError, self.assert_callback, '0')
        self.assertRaises(AssertionError, self.assert_callback, True)
        self.assertRaises(AssertionError, self.assert_callback, False)

if __name__ == '__main__':
    unittest.main()
