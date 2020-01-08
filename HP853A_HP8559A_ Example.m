%%               NFMWI_Spectrum_DAQ.m
%%Written by: Jarvis Hill
%%Date: 10/04/13
%%Purpose: This program will, 
%%1. Communicate with a HP853A display of the HP8559A spectrum analyzer (SA) via PROLOGIX GPIB-USB Controller.
%%2. Send the plot trace commands and receive the ASCII format data string for SA traces
%%3. Convert ASCII data string into integer array 
%%4. Plot a replicate of the trace(s) seen on the instrument screen

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%Setup GPIB COM with Instrument%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Initialize serial object
SA = serial('COM20');

set(SA,'InputBufferSize',1923)

%Open serial communication with instrument
%Baudrate and parity don't matter they are hardset by Prologix
%controller
fopen(SA);
pause(.1)
    
%Verify GPIB Controller
instrument = query(SA, '++ver');
fprintf('GPIB Controller ID: %s\n', instrument)
pause(.1)

%Set GPIB controller to read-after-write mode
fprintf(SA,'++auto 1');
pause(.1)

%Place controller in TALK mode so commands can be sent to instrument
fprintf(SA,'++mode 1');
pause(.1)

%Set GPIB address in controller to address on instrument
fprintf(SA, '++addr 18');
pause(.1)

%Append CR+LF to SA commands.  Having \n is just for the controller,
%it romeoves this then forwards command to instrument
fprintf(SA,'++eos 0');
pause(.1)

%Identify connected instrument
instr_idn = query(SA,'OI');
fprintf('Instrument: %s', instr_idn)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%      Spectrum DAQ                %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Request trace data
fprintf(SA,'TA');
data = fscanf(SA,'%s',1923);

%parse ascii y-coords. from data string minus the commas
ASCII_value = 0;        						%Initialize variables to zero
temp = 0;

ASCII_values = [];      						%Define array for ascii y-coords.
   

for I = 1:481
    J = (4*I)+1-4;								%-4 to account for offeset of MATLAB indexing starting at 1 instead of 0
    ASCII_value = data(J:J+2);
    temp = ASCII_value;
    
    %%converts string to integer
    if temp == '-50'
        ASCII_values(I) = 0;  					%'-50'= blank space, so just place a 0 in that integer position
    else 
        ASCII_values(I) = str2num(ASCII_value); %converts strings other than '-50' to integers
    end
    
end

%Plot SA trace data
figure
axis([0 481 0 900])
plot(ASCII_values)

%Close serial connection
fclose(SA);    



    
    
    
    
 
    
    
    
    
    
    
    