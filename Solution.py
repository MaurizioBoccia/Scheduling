
#=====================================================================================================
# Classe Solution
#   attributi:
#       1) Inst -> istanza 
#
#       2) IsFeas -> True se la soluzioe è ammissibile
#
#       2) Makespan -> tempo di completamento
#      
#       4) ListOfJobs -> ListOfJobs[m][p] = (flag,j) 
#          j è il job in posizione p sulla macchina m se flag = 0, 
#          se flag = 1 j è una ricarica posta in posizione p sulla macchina m
#
#   metodi:
#       1) UpdateSol(self, genotype) -> aggiorna la soluzione
#
#=====================================================================================================

from Instance import Instance

import gurobipy as gp
from gurobipy import GRB
import numpy

class Solution():

    def __init__(self,  Inst, Candidate):

        self.Inst = Inst
        
        self.Candidate = Candidate
        
        self.UpdateSol(self.Candidate)
        
        self.Makespan = self.Candidate.Fitness
     
    def UpdateSol(self,Candidate):

        update = False
        

        self.ListOfJobs = [[] for i in range(self.Inst.NumMachines)]
        
        for i in self.Candidate.Genotype:
            self.ListOfJobs[i[1]].append(i[0])
        # print(self.Candidate.Genotype)
        Step1Status = 0
        machlist =  []
        
        for i in numpy.argsort(self.Candidate.Makespan):
            machlist.insert(0, i)
        for i in machlist:
            stat, numchar = self.BPP(self.ListOfJobs[i],self.Candidate.Recharges[i])
            
            if numchar < self.Candidate.Recharges[i]:
                update = True
                self.Candidate.Makespan[i] -= self.Inst.ChargingTime*(self.Candidate.Recharges[i] - numchar)
                self.Candidate.Recharges[i] = numchar
                
            else: 
                break
        if update == True:
            self.Candidate.Fitness = max(self.Candidate.Makespan)

        return update
    
    
    def BPP(self,jobs,ncharges):
        #-----------------------------------------------------#
            # scrive la formulazione del problema di bin paching
            #-----------------------------------------------------#
    
            self.BPmod = gp.Model("BinPackProb")
    
            self.BPmod.setParam(GRB.Param.TimeLimit, 720)
    
            # insiemi di indici
            self.job = len(jobs)
            self.charge = range(ncharges)
    
            # definizione delle variabili
            self.Gvar = self.BPmod.addVars(self.charge, obj=1.0, vtype=GRB.BINARY, name="G")
            # print(jobs)
            self.Cvar = self.BPmod.addVars(self.charge, jobs, obj=0.0, vtype=GRB.BINARY, name="C")
    
            # vincoli di assegnamento
            self.BPmod.addConstrs(
                (self.Cvar.sum('*', j) == 1 for j in jobs), "Assignment")
    
            # vincoli di capacità
            m = 0 # i pesi per la macchina 1 sono gli stessi anche per le altre macchine
            self.BPmod.addConstrs(
                (gp.quicksum(self.Inst.Weight[j,m] * self.Cvar[i,j] for j in jobs) -
                 self.Inst.MaxChargeLevel * self.Gvar[i] <= 0 for i in self.charge), "Capacity")
            
            # vincoli di ordinamento delle ricariche
            self.BPmod.addConstrs(
                (self.Gvar[i] - self.Gvar[i-1] <= 0  for i in range(1, ncharges)), "Sorting")
    
            #self.BPmod.write("BinPacking.lp")
    
            self.BPmod.optimize()
    
            self.LowerBound = 0
            
            Step1Status = 0
            
            if self.BPmod.status == GRB.OPTIMAL or self.BPmod.status == GRB.SUBOPTIMAL or self.BPmod.status == GRB.TIME_LIMIT:
    
                Step1Status = 1
    
                # calcola il lower bound del problema
                self.LowerBound = self.BPmod.objVal 
                # max(0,(int(self.BPmod.objVal) - self.Inst.NumMachines)) * self.Inst.ChargingTime
                # for j in range(self.Inst.NumJobs):
                    # self.LowerBound = self.LowerBound + self.Inst.Dur[j][0]
    
                # self.LowerBound = math.ceil(self.LowerBound / self.Inst.NumMachines)
                    
                # definisce i bin e il relativo peso
    
                # self.Bin = []
    
                # for i in range(int(self.BPmod.objVal)):
    
                #     listOfJobs = []
                #     weight = 0
                #     dur = 0
    
                #     for j in self.job :
    
                #         if self.Cvar[i,j].x > 0.5 :
    
                #             weight = weight + self.Inst.Weight[j][m] 
                #             dur = dur + self.Inst.Dur[j][m]
    
                #             listOfJobs.append(j)
    
                #     dur = dur + self.Inst.ChargingTime
    
                #     self.Bin.append((dur, weight, listOfJobs, -1))
    
            return Step1Status, self.LowerBound
    
    
    
    