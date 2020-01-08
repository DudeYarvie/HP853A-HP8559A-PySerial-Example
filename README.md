# HP853A-HP8559A-PySerial-Example
Example code demonstrating how to retrieve trace/measurement data fromt he HP8559A spectrum analyzer using Python or MATLAB. The scripts  communicate to the instrument via the GPIB/HPIB interface using a Prologix GPIB-USB controller.

# File Descriptions
HP853A_HP8559A_Example.py provides the example for using Python to control the spectrum analyzer
HP853A_HP8559A_Example.m provides the example for using MATLAB to control the spectrum analyzer
PrologixGpibUsbManual-6.0.pdf user manual for GPIB controller

# Usage
1. Download Python v2.7 or MATLAB (choose 32 or 64 bit based on the your OS bitness)
2. Set the GPIB address of the spetrum analyzer display (HP853A) following the user manual instructions
3. Connect the Prologix GPIB-USB controller to the host PC and ensure the driver automatically downloads. The controller should appear as a COM port on your PC if the driver is installed correctly. The driver may be found on the MFG website for manual installation.
5. Connect the Prologix GPIB-USB controller to the GPIB/HPIB port on the back of the spectrum analyzer.
7. Execute the script
