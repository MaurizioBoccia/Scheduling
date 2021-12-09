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

import numpy
import numpy as np
import math 
import random

class SuperCandidate():

    def __init__(self, Inst, seme):

        self.Inst = Inst 

        self.seme = seme

        self.Fitness = 0

        self.Genotype = []

        self.RandomlyGenerate()

        self.OverLoadMac = -1
        
        self.Recharges = []
        
        self.Makespan = []
        self.Genotype, self.Fitness, self.Makespan, self.OverLoadMac, self.Recharges = self.ComputeCandidate(seme)

        
    def ComputeCandidate(self,seme): 
        
        tmac = [0 for i in range(self.Inst.NumMachines)]
        emac = [0 for i in range(self.Inst.NumMachines)]
        rech = [1 for i in range(self.Inst.NumMachines)]
        dur = []
        wei = []
        Genotype = []
        for i in range(self.Inst.NumJobs):
            wei.append(self.Inst.Weight[i][0])
            dur.append(self.Inst.Dur[i][0])
            
        if seme == 0:
            idbest = numpy.argsort(dur)
        else:
            idbest = numpy.argsort(wei)
            
        for i in idbest:
            temp1 = -1
            temp2 = sum(dur[i] + self.Inst.ChargingTime for i in range(self.Inst.NumJobs))
            temp3 = 0
            for j in range(self.Inst.NumMachines):
                if emac[j]+wei[i]> self.Inst.MaxChargeLevel:
                    if tmac[j] + self.Inst.ChargingTime + dur[i] < temp2:
                        temp1 = j
                        temp2 = tmac[j] + self.Inst.ChargingTime + dur[i]
                        temp3 = 1
                else:
                    if tmac[j] + dur[i] < temp2:
                        temp1 = j
                        temp2 = tmac[j] + dur[i]
                        temp3 = 0
            Genotype.append((i,temp1))
            tmac[temp1]+=dur[i]+self.Inst.ChargingTime*temp3
            rech[temp1]+= temp3
            emac[temp1]= wei[i] + (1-temp3)*emac[temp1]            
                            
        return Genotype, max(tmac), tmac, tmac.index(max(tmac)), rech


           

