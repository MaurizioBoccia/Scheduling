from Instance import Instance
from Heuristic import Heuristic

import time
import sys

#======================================================
# Legge l'istanza da un file txt
#======================================================

#FileName = input('Inserisci il nome del file di input: ')
#FileName = "Ins_V2_J50_T20_R60_B10_W4_S108_N8.txt"
#FileName = "Ins_V10_J100_T10_R60_B10_W2_S244_N4.txt"
#FileName = "Ins_V2_J200_T10_R60_B10_W4_S275_N5.txt"
#FileName = "Ins_V2_J150_T20_R60_B10_W4_S13_N3.txt"
#FileName = "Ins_V2_J10_T10_R60_B10_W2_S6_N6.txt"
#FileName = "Ins_V5_J10_T10_R60_B10_W1_S30_N0.txt"
#FileName = input()
FileName = sys.argv[1]
Inst = Instance(FileName)

#======================================================

#======================================================================
# Risolve il problema con l'euristica di ricerca locale
#======================================================================

Heur = Heuristic(Inst)

start_time = time.time()

Step1Status, LowerBound = Heur.BinPackingPhase()

if Step1Status == 2 :
    # risolve il problema di parallel machine scheduling
    LowerBound, UpperBound = Heur.ParallelMachinePhase()
    time_step2 = 0
    time_step3 = 0

end_Step1 = time.time()
time_step1 = end_Step1 - start_time

Step2Status = 0

if Step1Status == 1 :

    start_Step2 = time.time()

    Step2Status, InitialUpperBound = Heur.AssignmentPhase()

    end_Step2 = time.time()

    time_step2 = end_Step2 - start_Step2 


if Step1Status == 1 and Step2Status == 1 :  

    start_Step3 = time.time()

    Step3Status, FinalUpperBound = Heur.LocalSearchPhase()

    end_Step3 = time.time()

    time_step3 = end_Step3 - start_Step3 

end_time = time.time()

print("\n\n--- %s seconds ---" % (end_time - start_time))

#======================================================================
#======================================================================
# Aggiunge le informazioni relative alla soluzione nel file results.txt
#======================================================================

if Step1Status == 1 and Step3Status == 1 :
    
    file_out = open("resultsHeur.txt", "a")

    Indice = 0
    while Indice < len(FileName):
        if FileName[Indice] == "W":
            break
        Indice = Indice + 1 

    avgw = FileName[Indice+1]

    file_out.write("%s \t %g \t %g \t %g \t %g \t %g \t %g \t %g \t %d \t %g \t %g \t %g \t %g\n" %(FileName, 
                   Inst.NumMachines, Inst.NumJobs, Inst.ChargingTime, Inst.MaxChargeLevel, 
                   int(avgw), LowerBound, time_step1, InitialUpperBound, time_step2, 
                   FinalUpperBound, time_step3, (end_time - start_time)))

    file_out.close()

if Step1Status == 2 :

    file_out = open("resultsHeur.txt", "a")

    Indice = 0
    while Indice < len(FileName):
        if FileName[Indice] == "W":
            break
        Indice = Indice + 1 

    avgw = FileName[Indice+1]

    file_out.write("%s \t %g \t %g \t %g \t %g \t %g \t %g \t %g \t %d \t %g \t %g \t %g \t %g\n" %(FileName, 
                   Inst.NumMachines, Inst.NumJobs, Inst.ChargingTime, Inst.MaxChargeLevel, 
                   int(avgw), LowerBound, time_step1, UpperBound, time_step2, UpperBound, 
                   time_step3, (end_time - start_time)))

    file_out.close()