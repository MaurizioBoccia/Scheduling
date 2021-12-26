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


           

