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

    def __init__(self, Inst, seme):

        self.Inst = Inst 

        self.seme = seme

        self.Fitness = 0

        self.Genotype = []

        self.RandomlyGenerate()

        self.Fitness = self.ComputeFitness()


    def RandomlyGenerate(self):
                
        semeran = self.seme
        random.seed(semeran)

        arr = np.random.permutation(self.Inst.NumJobs)
        
        for i in range(self.Inst.NumJobs): 

            random.seed(semeran + i)

            self.Genotype.append((arr[i], random.randint(0, self.Inst.NumMachines-1)))

        return


    def ComputeFitness(self): 
        
        tmac = [0 for i in range(self.Inst.NumMachines)]
        emac = [0 for i in range(self.Inst.NumMachines)]
        for i in range(self.Inst.NumJobs):
            if emac[self.Genotype[i][1]]+self.Inst.Weight[self.Genotype[i][0]][self.Genotype[i][1]] > self.Inst.MaxChargeLevel:
                emac[self.Genotype[i][1]] = self.Inst.Weight[self.Genotype[i][0]][self.Genotype[i][1]]
                tmac[self.Genotype[i][1]] += self.Inst.ChargingTime
            else:
                emac[self.Genotype[i][1]] += self.Inst.Weight[self.Genotype[i][0]][self.Genotype[i][1]]
            tmac[self.Genotype[i][1]] += self.Inst.Dur[self.Genotype[i][0]][self.Genotype[i][1]]
                    
        return max(tmac)


           

