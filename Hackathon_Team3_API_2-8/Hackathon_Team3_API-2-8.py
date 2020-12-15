# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 10:19:15 2020

@author: Team 3
"""
# Protocol for Immunostaining

#Initialisation
from opentrons import simulate
import time
import math

execute = 'n'
while(execute=='n'):  
    metadata = {'apiLevel': '2.8'}
    protocol = simulate.get_protocol_api('2.8')


    #Labware
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
    tempdeck = protocol.load_module('temperature module gen2', 3)
    reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 4)
    PBSreservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 5)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 7) 
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
    tiprack_3 = protocol.load_labware('opentrons_96_tiprack_300ul', 9)
    p300_2 = protocol.load_instrument('p300_multi', mount='left', tip_racks=[tiprack_1,tiprack_2,tiprack_3])
    protocol.max_speeds['Z'] = 10 
    
    #Temperature control
    cool_reagents = tempdeck.load_labware('opentrons_24_aluminumblock_generic_2ml_screwcap')
    tempdeck.set_temperature(4) # set block to 4°C
    for line in protocol.commands(): 
                print(line)
      
    #Sample number question (need to round volumes up as multichannel will use all wells in a column)
    while True:    
        samples = int(input("Enter number of samples (1-96): "))
        if samples>96:
            print("\nError: Too many samples. Try again")
        else: 
            samples = math.ceil(samples/8)*8
            break
        
    print("\nRounding up to",samples,"samples.")
    Vol_200=round(samples*0.2+2)
    Vol_100=round(samples*0.1+2)
    Vol_50=round(samples*0.05+2)
    Vol_PBS=round(samples*0.2+1)
    Total_PBS=round((Vol_200+(Vol_100*3)+(Vol_50*4)+(round(Vol_PBS)*9))*1.05)
    
    #Antibody dilution questions
    while True:
        p_dil = int(input("Enter primary antibody dilution = 1:"))
        s_dil = int(input("Enter secondary antibody dilution = 1:"))
        prim_ab_add=round(Vol_50/p_dil*1000)
        seco_ab_add=round(Vol_50/s_dil*1000)
        if prim_ab_add and seco_ab_add in range (1,21):
            tiprack_4 = protocol.load_labware('opentrons_96_tiprack_20ul', 6)
            pipette = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[tiprack_4])
            print("\n-Ensure the single-channel p20 pipette and the corresponding tips are installed-")
            break
        elif prim_ab_add and seco_ab_add in range(21,701):
            tiprack_4 = protocol.load_labware('opentrons_96_tiprack_300ul', 6)
            pipette = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_4])
            print("\n-Ensure the single-channel p300 pipette and the corresponding tips are installed-")
            break
        elif prim_ab_add or seco_ab_add >700:
            print("\nError: Antibody stock too dilute. Try again")
        else:
            print("\nError: Antibody stock too concentrated. Try again")
    # Create a txt file to save the run info

    with open('immuno_run.txt', 'w', newline='') as f:
        print('Number of samples = {}'.format(samples), file=f)
    # Working volumes for reservoirs 
        print("\nPrepare PBS (Total) = {}".format(Total_PBS),"mL", file=f) 
        print("Prepare and add the following reagents to the designated reservoir wells at position 4:", file=f)
        print("\nPBST (PBS, 0.1% Tween) in A1 = {}".format(Vol_200),"mL", file=f) # add cold
        print("\nFixing Solution (PBS, 4% paraformaldehyde, pH 7.4) in A2 = {}". format(Vol_100),"mL", file=f)
        print("\nDetergent Solution (PBS, 0.1% Triton) in A3 = {}".format(Vol_100),"mL", file=f)
        print("\nBlocking Solution (PBST, 1% BSA, 22.5mg/mL glycine) in A4 = {}".format(Vol_100),"mL", file=f)
        print("\nPrimary antibody dilutant (PBST, 1% BSA) in A5 ={}".format(Vol_50),"mL", file=f)
        print("\nSecondary antibody dilutant (PBST, 1% BSA) in A6 ={}".format(Vol_50),"mL", file=f)
        print("\nF-actin stain (PBS, 1:50 Flash Phalloidin Red) in A7 ={}".format(Vol_50),"mL", file=f)
        print("\nNuclear stain (PBS, 0.1% DAPI nuclear stain) in A8 ={}".format(Vol_50),"mL", file=f)
        print("\nAdd {}". format(round(Vol_PBS)),"mL of remaining PBS to wells 1-9 in the reservoir at position 5.", file=f)
        #Antibodies setup
        print("\nAntibody setup:", file=f)
        print("\nPrimary antibody to add to {}". format(Vol_50),"mL of primary dilutant (1:",p_dil,") ={}".format(round(prim_ab_add)), "µL", file=f)
        print("Place a {}".format(round(prim_ab_add+10)),"µL aliqout of the primary antibody stock into A1 in the cold block at position 3.", file=f)
        print("\nSecondary antibody to add to {}".format(Vol_50),"mL of secondary dilutant (1:",s_dil,") ={}". format(round(seco_ab_add)), "µL", file=f)
        print("Place a {}".format(round(seco_ab_add+10)),"µL aliquot of the secondary antibody stock into A2 in the cold block at position 3.", file=f)
    
    # Working volumes for reservoirs 
    print("\nPrepare PBS (Total) =",Total_PBS,"mL") 
    print("Prepare and add the following reagents to the designated reservoir wells at position 4:")
    print("\nPBST (PBS, 0.1% Tween) in A1 =",Vol_200,"mL") # add cold
    print("\nFixing Solution (PBS, 4% paraformaldehyde, pH 7.4) in A2 =",Vol_100,"mL")
    print("\nDetergent Solution (PBS, 0.1% Triton) in A3 =",Vol_100,"mL")
    print("\nBlocking Solution (PBST, 1% BSA, 22.5mg/mL glycine) in A4 =",Vol_100,"mL")
    print("\nPrimary antibody dilutant (PBST, 1% BSA) in A5 =",Vol_50,"mL")
    print("\nSecondary antibody dilutant (PBST, 1% BSA) in A6 =",Vol_50,"mL")
    print("\nF-actin stain (PBS, 1:50 Flash Phalloidin Red) in A7 =",Vol_50,"mL")
    print("\nNuclear stain (PBS, 0.1% DAPI nuclear stain) in A8 =",Vol_50,"mL")
    print("\nAdd",round(Vol_PBS),"mL of remaining PBS to wells 1-9 in the reservoir at position 5.")
    #Antibodies setup
    print("\nAntibody setup:")
    print("\nPrimary antibody to add to",Vol_50,"mL of primary dilutant (1:",p_dil,") =",round(prim_ab_add), "µL")
    print("Place a",round(prim_ab_add+10),"µL aliqout of the primary antibody stock into A1 in the cold block at position 3.")
    print("\nSecondary antibody to add to",Vol_50,"mL of secondary dilutant (1:",s_dil,") =",round(seco_ab_add), "µL")
    print("Place a",round(seco_ab_add+10),"µL aliquot of the secondary antibody stock into A2 in the cold block at position 3.")
    print("\nMake sure the Opentrons is covered or in the dark\n- Run protocol when all reagents are placed -")
    #Protocol steps
    #assuming samples are filled column-wise
    final_row,final_col = str(plate.wells(samples-1)).split()[0][1],int(str(plate.wells(samples-1)).split()[0][2:])
        
    def add_reagent_m(x,vol):
        tic = time.perf_counter()
        p300_2.distribute(vol, reservoir.wells_by_name()[x], plate.rows_by_name()['A'][:final_col],trash = True, blow_out = False,disposal_volume=0)
        toc = time.perf_counter()
        return toc-tic
    def rem_reagent_m(x,vol): # This now disposes of liquids into 
        tic = time.perf_counter()
        p300_2.consolidate(vol, plate.rows_by_name()['A'][:final_col], protocol.fixed_trash["A1"])
        toc = time.perf_counter()
        return toc-tic
    def add_wash(x,vol):
        tic = time.perf_counter()
        p300_2.distribute(vol, PBSreservoir.wells_by_name()[x], plate.rows_by_name()['A'][:final_col],trash = True, blow_out = False,disposal_volume=0)
        toc = time.perf_counter()
        return toc-tic
    def add_prim_res(vol):
        tic = time.perf_counter()
        pipette.transfer(prim_ab_add, cool_reagents['A1'], reservoir['A5'], touch_tip=True)
        toc = time.perf_counter()
        return toc-tic
    def add_seco_res(vol):
        tic = time.perf_counter()
        pipette.transfer(seco_ab_add, cool_reagents['A2'], reservoir['A6'], touch_tip=True)
        toc = time.perf_counter()
        return toc-tic
    def add_prim_well(vol):
        tic = time.perf_counter()
        p300_2.distribute(vol, reservoir["A5"], plate.rows_by_name()['A'][:final_col],trash = True, blow_out =False, mix_before=(8,300))
        toc = time.perf_counter()
        return toc-tic
    def add_seco_well(vol):
        tic = time.perf_counter()
        p300_2.distribute(vol, reservoir["A6"], plate.rows_by_name()['A'][:final_col],trash = True, blow_out =False, mix_before=(8,300))
        toc = time.perf_counter()
        return toc-tic
    
    start=time.perf_counter()
    #Aspirate media
    rem_reagent_m('A1',200)
    
    #Rinse with PBST
    add_reagent_m('A1',100)
    rem_reagent_m('A1',100)
    
    #Add/Remove PFA
    t1=add_reagent_m('A2',100)
    protocol.delay(10*60-t1)
    rem_reagent_m('A1',100)
    
    #Wash with PBS
    add_wash('A1',200)
    rem_reagent_m('A1',200)
    add_wash('A2',200)
    rem_reagent_m('A1',200)
    
    #Add/Remove PBS PBS/0.1% Triton X-100
    t2=add_reagent_m('A3', 100)
    protocol.delay(10*60-t2)
    rem_reagent_m('A1',100)
    
    #Wash with PBS
    add_wash('A3',200)
    rem_reagent_m('A1',200)
    add_wash('A4',200)
    rem_reagent_m('A1',200)
    
    #Add/Remove Blocking solution 
    t3=add_reagent_m('A4', 100)
    protocol.delay(30*60-t3)
    
    #Add/Remove A.B 1 solution 
    add_prim_res(prim_ab_add)
    rem_reagent_m('A1',100)
    t4=add_prim_well(50)
    protocol.delay(120*60-t4)
    rem_reagent_m('A1',50)
    
    #Wash with PBS
    add_wash('A5',200)
    
    #Add/Remove A.B 2 solution 
    add_seco_res(seco_ab_add)
    rem_reagent_m('A1',200)
    t5=add_seco_well(50)
    protocol.delay(60*60-t5)
    rem_reagent_m('A1',50)
    
    #Wash with PBS
    add_wash('A6',200)
    rem_reagent_m('A1',200)
    add_wash('A7',200)
    rem_reagent_m('A1',200)
    
    #Add/Remove Red dye solution
    t6=add_reagent_m('A6', 50)
    protocol.delay(20*60-t6)
    rem_reagent_m('A1',50)
    
    #Add/Remove DAPI dye solution
    t7=add_reagent_m('A6', 50)
    protocol.delay(60-t7)
    rem_reagent_m('A1',50)
    
    #Wash with PBS
    add_wash('A8',200)
    rem_reagent_m('A1',200)
    add_wash('A9',200)
    finish=time.perf_counter()
    
    #Timer
    totaltime= (251*60)-(t1+t2+t3+t4+t5+t6+t7)
    hours=math.floor((totaltime/60)/60)
    minutes=math.floor((totaltime/60)%60)
    seconds=round(((((totaltime/60)%60)%1)*0.6*100),1)
    
    #Run protocol
    execute=(input("Press y to run protocol\nPress n to recheck and run again\n"))
    

print("\nExecuting...")
print("\n")
for line in protocol.commands(): 
    print(line)
print("\nTime taken: 0"+str(hours)+" hr, "+str(minutes)+" min, "+str(seconds)+" sec.")
print("\nProtocol Finished. Remove plate")
Switchoff=(input("Deactivate Temperature Module? (y/n): "))
if Switchoff=="y":
    tempdeck.deactivate
    print("\nTemperature Module deactivated.")
else:
    tempdeck.set_temperature(4)
    print("\nTemperature Module active ("+str(tempdeck.temperature)+"°C)")