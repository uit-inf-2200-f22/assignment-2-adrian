# INF-2200 Computer Architecture and Organization

## Home exam part 1: MIPS Simulator

### Introduction and Design

In this assignment, you will implement a binary code simulator for a subset of the MIPS architecture. You will simulate the pipelined datapath and controller described in your textbook. We will provide you with the pre-code you should use as a starting point. Your simulator should support the following instructions:
- j: jump
- beq: branch equal
- bne: branch not equal
- lui: load upper intermediate
- slt: set less than
- lw: load word
- sw: store word
- add: add
- addu: add unsigned
- addi: add immediate
- addiu: add immediate unsigned
- sub: subtract
- subu: subtract unsigned
- and: binary and
- or: binary or
- nor: binary nor
- break: break execution

We also provide you with test cases and three sample programs that you can use during development and to test your solution. 

## Pre-code

The pre-code consists of Python-files that define the main simulator class’s API and implement the simple single-cycle control and datapath shown in Figure 1.

|![](assets/adder_flow.png) |
|:--:|
| **Figure 2: Simple single-cycle control and datapath implemented in pre-code** |

All control and datapath elements are subclasses of the CPUElement class. This class maintains four main data structures: 

-   A table of input data implemented as a dictionary (map) with one entry per input data. A unique name for each input is used as key and the input data as the value.
-   A table for the output data implemented as a dictionary that maps unique output names to output values with one entry per output
-   A table of input control signals implemented as a dictionary that maps unique signal names to signal values with one entry per input signal
-   A table of output control signals implemented as a dictionary that maps unique signal names to signal values with one entry per output signal


CPUelement defines the following eight methods:

-   **\_\_init\_\_**: Constructor. The default constructor does not do anything, but a subclass may not need to initialize data structures, etc.
-   **connect**: Called once per CPU Element instance during initialization to connect the data paths and control paths to other elements. **All subclasses of CPUElement must implement this method**.
-   **readinput**: Read input data from source elements, and update an internal table with the input data.
-   **readControlSignals**: Read and set control signals
-   **writeOutput**: Using the input data and control signals, do the necessary computation, and update an internal table with the output data. **All subclasses of CPUElement must implement this method**.
-   **setControlSignals**: Using the input data and control signals, do the necessary computation, and set the output control signals. **All subclasses of CPUElement must implement this method**.
-   **getOutputValue**: Called during ***readInput()*** to read the output data calculated in the previous iteration.
-   **getControlSignal**: Called during ***readControlSignals()*** to get a control signal set in the previous iteration.

You must implement a subclass for each type of element in your control or data path. You must also implement the ***initializeMemory()*** method in the Memory class so that the InstructionMemory and DataMemory instances can be initialized by reading binary data from a file. 

The simulator does the following:

1.  Create an object for each control and datapath element.
2.  Connect the elements by specifying input and output data and signals.
3.  For each cycle:

    1.  For each element, call ***readControlSignals()*** and ***readInput()***
    2.  For each element, call ***writeOutput()*** and ***setControlSignals()***
    3.  Check if the break instruction has been encountered and exit the loop if so.

4.  Print the content of the registers and the number of cycles that were executed.

The check for the break instruction is not implemented in the pre-code, and you must therefore add a mechanism to do this test. Also, note that the order the different elements are read from and written to is of significance and that reading to and writing from pipeline registers must be considered specially for the pipelining to work as intended. 

Included in the pre-code are a few simple programs with filetype “.mem”, implemented in binary code, which can be used to initialize the instruction and data memory elements. The file is a tab-delimited text file, where the first and second columns contain memory addresses and memory content, respectively, both represented as 32-bit hexadecimal numbers, and the third column contains comments. Note that although the comments are assembly code, your simulator should run using the binary code only. Also note that the memory addresses do start from different addresses, **0xbfc00000** and **0x0**, and that the program does not use any memory besides of that defined in the file. 

Although both the instruction memory element and data memory element will initially read the same memory file’s contents, they are treated as separate, isolated entities. The instruction memory will be read-only, and although the data memory also contains the instructions, modifying these will not work and should be avoided.

**Data hazards**

Your simulated datapath and controller should handle data hazards. You can choose to implement forwarding, stalling, or another approach. Your report should describe your chosen approach and discuss it’s cost, complexity, and performance compared to at least one alternative approach.

**Control hazards**

Your simulated datapath and controller should handle controller hazards. You need to find an approach, implement it, and describe it in the report.

**Testing**

We provide tests for you in the *tests/* directory. Refer to [README](tests/README.md) in the tests directory for details. Most these tests will simply assert that the intended registers hold some expected value after running the code in the memory files. Others might contain code that will cause a register-value to overflow after an operation (see curriculum chapter 2.4 for definition and 3.2 for detection), in such cases the test assumes that somewhere in your simulator you will raise the pre-defined exception found in common.py. And some tests will contain a mix of different conditions to test both the pipeline and the correctness of instructions from the instruction-set your simulator should implement. 

An important part of the assignment is to design test cases that demonstrate that your pipeline works correctly when the executed code causes data or control hazards. To do this, you need to write code with known data dependencies, which will cause data and control hazards. You should write this code in MIPS assembly using the instruction subset listed above, convert that code to binary by hand and run the code on your simulator.

**Deliverables**

The report should contain all necessary information for an expert to evaluate your design and implementation. You should assume that the expert has neither read the textbook nor the assignment text. 

The report should contain the following:

0. Cover page with your names, emails, GitHub usernames, and your GitHub repository
1.  Summary of the datapath and controllers you are simulating
2.  Description of data hazard handling approach including a discussion about the cost, complexity, and performance of the approach
3.  Controller hazard handling approach
4.  Description of the simulator implementation, including the functions you have implemented
5.  A detailed description of the test cases you have designed
6.  Summary of known bugs and problems, including a description of which of the provided tests fails (if any).

The report can be maximum 6 pages in single column and a 12 point font.

**Submission**

Submit to Wiseflow:
1. The report as a PDF.
2. The code in a zip file with the following format: In the *doc/* directory there shold be a file *readme.tx* that includes instructions for executing your code and testing it for correctness. All source code must be placed in a folder called *src/*. The test results should be in the *tests*/ directory. A file in the root, where the file name has the format *abc001*, i.e., your UiT username. 

**Grading**

The assignment grade is based mainly on your report. The source code may be checked if the report is unclear.
