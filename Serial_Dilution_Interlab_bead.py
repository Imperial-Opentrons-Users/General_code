#Serial Dilution
#Load Buffer in Column 1 of 12-well reservoir
#Load Dye in Column 2 of 12-well reservoir

from opentrons import protocol_api

metadata = {
'protocolName': 'Serial dilution',
'description': 'Serial dilution for iGEM Interlab',
'apiLevel': '2.8'
}

# protocol run function. the part after the colon lets your editor know

tiprack_num=1
def run(protocol: protocol_api.ProtocolContext):

#from opentrons import simulate
#metadata = {'apiLevel': '2.8'}
#protocol = simulate.get_protocol_api('2.8')

#Labware
    plate = protocol.load_labware('costar96flatbottomtransparent_96_wellplate_200ul', 1)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    reservoir = protocol.load_labware('brooksreservoirplate_12_wellplate_21000ul', 3)
#pipettes
    p300 = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack_1])
    protocol.max_speeds['Z'] = 100
#commands

#distributing pbs
    p300.distribute(100, reservoir.wells_by_name()['A1'], plate.rows_by_name()['A'][1:])

#distributing dye
    p300.pick_up_tip()
    for i in range(2):
        p300.transfer(100,reservoir['A2'], plate['A'+str(i+1)], mix_before=(4, 75), touch_tip=True, blow_out=True, blowout_location='destination well',new_tip='never')
#serial dilution
    for i in range(9):
        p300.transfer(100, plate['A'+str(i+2)], plate['A'+str(i+3)], mix_before=(2, 75), touch_tip=True, blow_out=True, blowout_location='destination well',new_tip='never')
    p300.drop_tip()
    for line in protocol.commands(): 
        print(line)
