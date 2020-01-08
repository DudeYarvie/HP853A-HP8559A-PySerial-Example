##						HP853A_HP8559A Example.py
##Written By: Jarvis Hill
##E-mail: hilljarvis@gmail.com
##Date: 09/30/13
##
##Purpose: This program will, 
##1. Communicate with a HP853A display of the HP8559A spectrum analyzer (SA) via PROLOGIX GPIB-USB Controller.
##2. Send the plot trace A&B commands  and receive the ASCII format data string for SA traces
##3. Convert ASCII data string into integer array 
##4. Replicate the trace on the SA display by plotting the arrays using MATPLOTlib library

import serial      ##Enables serial communication
import time        ##Enables delays in seconds 
import array
import math        ##Enables non-standard math functions (ceil, floor, etc.)
import os          ##Enbales Windows os commands (e.g. "system pause")

##Libraries for plotting
import numpy as np
import matplotlib.pyplot as plt


##Serial COMM parameters
port = 'COM20'
baud = 57600

##Global Variables
dec_values=[]


##Reads response from SA
def read_data(ser):
        line = ''
        while True:
                ch = ser.read()
                line +=ch
                if ch == '\r': break
        ##print line
        return line
       
##Configures serial port and GPIB controller to communicate with SA                
def Config_gpib_comms():
        ser = serial.Serial(port,baud,timeout =10) ##Creates serial comm with GPIB controller on COM port and times out after 10 seconds if no connection
        ser.write("++ver\n")            ##Verify GPIB controller
        read_data(ser)                  ## Read and print controllers response
        ser.write("++mode 1\n")	        ##Places the controller in "TALK" mode allowing commands to be sent to the SA
        time.sleep(.5)                  ##delays .5 seconds
        ser.write("++auto 1\n")	        ##Contoller will automatically listen after writing to device
        time.sleep(.5)          
        ser.write("++addr 18\n")        ##Sets GPIB  that controller talks to, set to GPIB address configured on the device
        time.sleep(.5)
        ser.write('++eos 0\n')          #Appends CR+LF to transmission data, having \n is just for the controller, it removes this then
                                        #transmits the data
        
        print 'Set HP853A GPIB Address to 18'
        time.sleep(1)  					#Delay (N) seconds

        ##Identify Device
        ser.write('OI\n')                 
        device = read_data(ser)
        print 'Device ID: %s'%device

        return ser

#Enables remote control for front panel settings on SA
def enable_control(ser):
        print 'enabling remote control'
      
        #Enable CLEAR WRITE mode for Trace A
        ser.write('AC1\n')
        time.sleep(.5)


##Read and plot trace data
def read_TA(ser):

        #Define lists to store trace data
        dec_values=[]
        ASCII_values=[]

        ##requests TRACE A data from SA 
        ser.write('TA\n')         
        	
        ##Stores and prints trace data received to IDLE window
        data = ''
        data = read_data(ser)

        ##Parse the trace data string and retreive only the 481 trace y-coords. (ASCII values), not the commas
        for I in range (0,481):
                J = (4*I)+1
                ASCII_value = data[J:J+3]
                ASCII_values.append((ASCII_value))
        ##print ASCII_values       		#Prints the y-coord trace data string (3 bytes = 1 y-coord.)
                
        ##Convert ASCII trace data string into integer array
        for I in range (0,481):
                temp = ASCII_values[I]

                ##Check if data value is '-50' which = a blank space
                if temp == '-50':

                        #appends a zero for the trace data point
                        dec_values.append(0)
                else:
                        #TA loads y-coords sequentially, 3 bytes represnts 1 coord.
                        #The following converts the y-coord. ASCII string to an integer
                        dec_value = int(temp)
                        dec_values.append(dec_value)

        ##print dec_values          	#Print dec equivalent values of trace data for debugging
        
        #close serial COM
        ser.close()
        
        ##plot trace data retrieved
        plt.ylim(0,1000)                #Set y scale to 1000, max y-coord of SA = 975
        plt.xlim(0,482)
        plt.plot(dec_values)
        plt.show()


##Main Program                
def main():
        
        #Begin communication with Prologix GPIB controller and HP853A
        ser = Config_gpib_comms()
        time.sleep(1)
        print 'Communicating with HP853A...'
        time.sleep(.5)

        ##Clears Trace A data
        ser.write('CA\n')
        time.sleep(.5)

        ##Enable front panel contol of HP853A
        enable_control(ser)

        ##Read Trace A data from HP853A
        print 'Reading Trace A data'
        time.sleep(.5)
        read_TA(ser)
                
        print 'Closing communication with device'
        ser.close()
		
	#Pause until button is pressed
        ##os.system("pause")
	

if __name__ == '__main__':
    main()


        

