from Instance import Instance
from GeneticAlg import GeneticAlg
#from Candidate import Candidate

import time
import sys
import random

#======================================================
# Legge l'istanza da un file txt
#======================================================

# FileName = "Ins_V5_J50_T20_R60_B10_W4_S131_N1.txt"
FileName = "Ins_V5_J200_T20_R60_B10_W2_S314_N4.txt"
# FileName = "Ins_V2_J10_T10_R60_B6_W1_S0_N0.txt"
#FileName = input()
#FileName = sys.argv[1]

Inst = Instance(FileName)

#======================================================
# Implementa un algoritmo genetico
#======================================================

PopSize = 200
NumOfGen = 20
NumOfIterationsPerGen = 4
ProbMutation1 = 0.1
ProbMutation2 = 0.1
NumElite = 2
NumSuperCandidate = 4

GA = GeneticAlg(Inst, PopSize, NumOfGen, NumOfIterationsPerGen, ProbMutation1, ProbMutation2, NumElite, NumSuperCandidate)
print(GA.BestCandidateFitness)