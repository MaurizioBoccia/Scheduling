
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
        
        update, self.Candidate = self.UpdateSol(Candidate)
        
        self.Makespan = self.Candidate.Fitness
     
    def UpdateSol(self,Candidate):

        update = False
        

        ListOfJobs = [[] for i in range(self.Inst.NumMachines)]
        
        for i in Candidate.Genotype:
            ListOfJobs[i[1]].append(i[0])
        # print(self.Candidate.Genotype)
        Step1Status = 0
        machlist =  []
        
        for i in numpy.argsort(Candidate.Makespan):
            machlist.insert(0, i)
        for i in machlist:
            stat, numchar, job2charges = self.BPP(ListOfJobs[i],Candidate.Recharges[i])
            
            if stat == 1 and numchar < Candidate.Recharges[i]:
                update = True
                Candidate.Makespan[i] -= self.Inst.ChargingTime*(Candidate.Recharges[i] - numchar)
                Candidate.Recharges[i] = numchar
                
                orderedj = []
                for j in job2charges:
                    for k in j:
                        orderedj.append(k)
                cont = 0
                for j in range(len(Candidate.Genotype)):
                    if Candidate.Genotype[j][1] == i:
                        Candidate.Genotype[j] = (orderedj[cont], i)
                        cont+=1
            else: 
                break
        if update == True:
            Candidate.Fitness = max(Candidate.Makespan)

        return update, Candidate
    
    
    def BPP(self,jobs,ncharges):
        #-----------------------------------------------------#
            # scrive la formulazione del problema di bin paching
            #-----------------------------------------------------#
    
            self.BPmod = gp.Model("BinPackProb")
    
            self.BPmod.setParam(GRB.Param.TimeLimit, 720)
    
            # insiemi di indici
            self.job = len(jobs)

            self.charge = range(int(ncharges))

    
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
                (self.Gvar[i] - self.Gvar[i-1] <= 0  for i in range(1, int(ncharges))), "Sorting")
    
            #self.BPmod.write("BinPacking.lp")
    
            self.BPmod.optimize()
    
            self.LowerBound = 0
            self.Bin = []
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
    
                
    
                for i in range(int(self.BPmod.objVal)):
    
                     listj = []
                #     weight = 0
                #     dur = 0
    
                     for j in jobs :

                        if self.Cvar[i,j].x > 0.5 :
    
                #             weight = weight + self.Inst.Weight[j][m] 
                #             dur = dur + self.Inst.Dur[j][m]
    
                            listj.append(j)
                     self.Bin.append(listj)
    
                #     dur = dur + self.Inst.ChargingTime
    
                #     self.Bin.append((dur, weight, listOfJobs, -1))
    
            return Step1Status, self.LowerBound, self.Bin
    
    
    
    