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
FileName = "Ins_V5_J50_T10_R60_B6_W1_S120_N0.txt"
#FileName = input()
#FileName = sys.argv[1]

Inst = Instance(FileName)

#======================================================
# Implementa un algoritmo genetico
#======================================================

PopSize = 50
NumOfIterations = 100

GA = GeneticAlg(Inst, PopSize, NumOfIterations)