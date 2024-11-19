import opentrons.simulate
from opentrons.simulate import format_runlog 


# read the file 

protocol_file = open('C:/users/geoff/github/Lab-practicals-and-teaching-materials/simple_protocol_test.py') 

# simulate() the protocol, keeping the runlog 
#opentrons.simulate.simulate(protocol_file) 

runlog, _bundle = opentrons.simulate.simulate(protocol_file) 

# print the runlog 

print(format_runlog(runlog)) 