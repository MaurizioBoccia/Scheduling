#=====================================================================================================
# Classe Candidate
#   attributi:
#       1) Inst -> istanza
#
#       2) Fitness -> Valore della funzione obiettivo
#       3) Genotype -> Genotype[i] = (job, machine) ovvero job è in posizione i e viene eseguito sulla macchia indicatsa. N.B. i non è la posizione sulla macchina ma è la posizione assoluta
#       
#   metodi:
#       1)  RandomlyGenerate(self, seme)
#
#       2)  ComputeFitness(self)
#
#=====================================================================================================
#=====================================================================================================

from Instance import Instance

import numpy as np
import math 
import random

class Candidate():

    def __init__(self, Inst, seme, Codifica):

        self.Inst = Inst 

        self.seme = seme
        
        self.Codifica = Codifica

        self.Fitness = 0

        self.Genotype = []

        self.RandomlyGenerate()

        self.OverLoadMac = -1
        
        self.Recharges = []
        
        self.Makespan = []
        self.Fitness, self.Makespan, self.OverLoadMac, self.Recharges = self.ComputeFitness()

        
        
    def RandomlyGenerate(self):
                
        semeran = self.seme
        random.seed(semeran)

        arr = np.random.permutation(self.Inst.NumJobs)
        for i in range(self.Inst.NumJobs): 

            random.seed(semeran + i)

            self.Genotype.append((arr[i], random.randint(0, self.Inst.NumMachines-1)))
        # if semeran == 25:
        
        #     self.Genotype = [(23, 0), (34, 1), (36, 2), (18, 3), (12, 4), (25, 4), (27, 3), (14, 2), (29, 1), (40, 3), (22, 0), (24, 0), (41, 1), (46, 3), (19, 2), (42, 0), (49, 2), (3, 4), (45, 1), (4, 3), (20, 0), (6, 2), (16, 4), (26, 1), (33, 0), (32, 1), (17, 3), (28, 2), (43, 3), (35, 4), (37, 3), (5, 0), (21, 1), (9, 3), (13, 4), (39, 1), (31, 2), (15, 3), (38, 3), (8, 1), (7, 4), (44, 1), (1, 4), (11, 3), (47, 4), (30, 0), (2, 2), (48, 4), (10, 2), (0, 3)]
       
        return

    def CopyCandidate(self, candidateor):

        self.Codifica = candidateor.Codifica
        self.Fitness = candidateor.Fitness
        for i in range(len(candidateor.Genotype)):
            self.Genotype[i] = candidateor.Genotype[i]
        self.Inst = candidateor.Inst
        for i in range(len(candidateor.Makespan)):
            self.Makespan[i] = candidateor.Makespan[i]
        self.OverLoadMac = candidateor.OverLoadMac
        for i in range(len(candidateor.Recharges)):
            self.Recharges[i] = candidateor.Recharges[i]
        self.seme = candidateor.seme 
        
        return
        
    
        
        
        
    def ComputeFitness(self): 
        Codifica = self.Codifica
        tmac = [0 for i in range(self.Inst.NumMachines)]
        emac = [0 for i in range(self.Inst.NumMachines)]
        rech = [1 for i in range(self.Inst.NumMachines)]
        if Codifica == 0:
            for i in range(self.Inst.NumJobs):
                if emac[self.Genotype[i][1]]+self.Inst.Weight[self.Genotype[i][0]][self.Genotype[i][1]] > self.Inst.MaxChargeLevel:
                    emac[self.Genotype[i][1]] = self.Inst.Weight[self.Genotype[i][0]][self.Genotype[i][1]]
                    tmac[self.Genotype[i][1]] += self.Inst.ChargingTime
                    rech[self.Genotype[i][1]]+= 1
                else:
                    emac[self.Genotype[i][1]] += self.Inst.Weight[self.Genotype[i][0]][self.Genotype[i][1]]
                    
                tmac[self.Genotype[i][1]] += self.Inst.Dur[self.Genotype[i][0]][self.Genotype[i][1]]
        elif Codifica == 1:
            for i in range(self.Inst.NumJobs):
                lmac = -1
                cmac = 999999999
                for j in range(self.Inst.NumMachines):
                    rmac = tmac[j]
                    if emac[j]+self.Inst.Weight[self.Genotype[i][0]][j] > self.Inst.MaxChargeLevel:
                        rmac += self.Inst.ChargingTime
                    if rmac < cmac:
                        cmac = rmac
                        lmac = j
                if emac[lmac] +self.Inst.Weight[self.Genotype[i][0]][lmac] > self.Inst.MaxChargeLevel:
                    emac[lmac] = self.Inst.Weight[self.Genotype[i][0]][lmac]
                    tmac[lmac] += self.Inst.ChargingTime
                    rech[lmac]+= 1
                else:
                    emac[lmac] += self.Inst.Weight[self.Genotype[i][0]][lmac]
                    
                tmac[lmac] += self.Inst.Dur[self.Genotype[i][0]][lmac]
            
            
            
        elif Codifica == 2:
            Codifica = 2
        
        return max(tmac), tmac, tmac.index(max(tmac)), rech


           

