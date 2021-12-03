from Instance import Instance
from GeneticAlg import GeneticAlg
#from Candidate import Candidate

import time
import sys
import random

#======================================================
# Legge l'istanza da un file txt
#======================================================

#FileName = input('Inserisci il nome del file di input: ')
FileName = "Ins_V2_J10_T10_R60_B6_W1_S0_N0.txt"
#FileName = input()
#FileName = sys.argv[1]

Inst = Instance(FileName)

#======================================================
# Implementa un algoritmo genetico
#======================================================

PopSize = 10
NumOfGen = 100
NumOfIterationsPerGen = 2
ProbMutation1 = 0.1
ProbMutation2 = 0.1
NumElite = 2

GA = GeneticAlg(Inst, Inst, PopSize, NumOfGen, NumOfIterationsPerGen, ProbMutation1, ProbMutation2, NumElite)
print(GA.BestCandidateFitness)