
#=====================================================================================================
# Classe GeneticAlg
#   attributi:
#       1) Inst -> istanza
#       2) PopSize -> numerosità della popolazione
#       3) NumOfIterations -> Numero di iterazioni svolte dall'algoritmo
# 
#       4) Population -> Population[i] candidato i-esimo
#       5) BestCandidateFitness -> migliore fitness tra gli elementi della popolazione attuale
#       6) BestCandidateInd -> indice del candidato con la migliore fitness
#
#       7) Sol -> migliore soluzione calcolata
#
#   metodi:
#       1) SelezioneMontecarlo(self) -> restituisce una coppia di genitori della popolazione corrente
#       2) GenPopulation(self) -> genera la soluzione iniziale
#       3) LocalSearch(self, 
#
#=====================================================================================================

from Instance import Instance
from Solution import Solution
from Candidate import Candidate
from SuperCandidate import SuperCandidate


import numpy as np
import math 
import random
import copy
import numpy

class GeneticAlg():

    def __init__(self, Inst, PopSize, NumOfGen, NumOfIterationsPerGen, ProbMutation1, ProbMutation2, NumElite, NumSuperCandidate, NumSuperFigli, Codifica):

        self.Inst = Inst 
        self.PopSize = PopSize 
        self.NumOfGen = NumOfGen
        self.NumOfIterationsPerGen = NumOfIterationsPerGen
        self.ProbMutation1 = ProbMutation1
        self.ProbMutation2 = ProbMutation2
        self.NumElite = NumElite
        self.BestCandidateFitness = 100000000
        self.BestCandidateInd = -1
        self.nsupcand = NumSuperCandidate
        self.NumSuperFigli = NumSuperFigli
        self.Codifica = Codifica
        # genera la popolazione iniziale
        self.GenInitialPopulation()

        bestfit = []
        avgfit = []

        # ALGORITMO GENETICO
        for gen in range(self.NumOfGen) :
            
            bestfit.append(self.BestCandidateFitness)
            
            poolfigli = []

            for iter in range(self.NumOfIterationsPerGen) :

                # Seleziona una coppia di genitori con il metodo Montecarlo
                genitore1, genitore2 = self.SelezioneMontecarlo()
                
                figlio1, figlio2 = self.Crossover(genitore1, genitore2)
                
                figlio1 = self.Mutation(figlio1, self.ProbMutation1, self.ProbMutation2)
                
                figlio2 = self.Mutation(figlio2, self.ProbMutation1, self.ProbMutation2)

                #if random.random() <= 0.01 : 
                #    figlio1 = self.RicercaLocale(figlio1)
                #if random.random() <= 0.01 :
                #    figlio2 = self.RicercaLocale(figlio2)
                
                if figlio1.Fitness <= self.BestCandidateFitness:
                    figlio1 = self.RicercaLocale(figlio1)
                    if figlio1.Fitness < self.BestCandidateFitness:
                        update, figlio1 = self.BestSol.UpdateSol(figlio1)
                
                if figlio2.Fitness <= self.BestCandidateFitness:
                    figlio2 = self.RicercaLocale(figlio2)
                    if figlio2.Fitness < self.BestCandidateFitness:
                        update, figlio2 = self.BestSol.UpdateSol(figlio2)
                    
                poolfigli.append((figlio1, figlio2))
        
        
            for i in poolfigli:
                self.UpdatePopulation(i[0], i[1])
                    
            popfit = []
                    
            for i in self.Population:
                popfit.append(i.Fitness)
                # print(popfit)
                # print(sum(popfit)/len(popfit))
                    
            avgfit.append(sum(popfit)/len(popfit))
        
            print(bestfit)
            print(avgfit)

        print(popfit)

    def Elite(self, NumElite):
        
        EliteArray = []
        val = []
        for i in self.Population:
                val.append(i.Fitness)
        idbest = numpy.argsort(val)
        
        for i in range(NumElite):
            EliteArray.append(idbest[i])

        return EliteArray

    def Crossover(self,genitore1,genitore2):

        # calcola primo e secondo punto crossover
        p1= random.randint(0,self.Inst.NumJobs-2)
        p2= random.randint(p1,self.Inst.NumJobs-1)
                
        offspring1 = copy.deepcopy(genitore1)
        offspring2 = copy.deepcopy(genitore2)
        
        for i in range(p1,p2+1):
            offspring1.Genotype[i] = copy.deepcopy(genitore2.Genotype[i])
            offspring2.Genotype[i] = copy.deepcopy(genitore1.Genotype[i])
        for i in range(p1):
            check=-1
            for j in range(p1,p2+1):
                if offspring1.Genotype[i][0] == genitore2.Genotype[j][0]:
                    check = j
                    while True:
                        doublecheck = False
                        for k in range(p1,p2+1):
                            if genitore1.Genotype[check][0] == genitore2.Genotype[k][0]:
                                check = k
                                doublecheck = True
                        if doublecheck == False:
                            break                    
                    break
            if check > -1:
                offspring1.Genotype[i] = copy.deepcopy(genitore1.Genotype[check])
                
            check=-1
            for j in range(p1,p2+1):
                if offspring2.Genotype[i][0] == genitore1.Genotype[j][0]:
                    check = j
                    while True:
                        doublecheck = False
                        for k in range(p1,p2+1):
                            if genitore2.Genotype[check][0] == genitore1.Genotype[k][0]:
                                check = k
                                doublecheck = True
                        if doublecheck == False:
                            break                    
                    break
            if check > -1:
                offspring2.Genotype[i] = copy.deepcopy(genitore2.Genotype[check])
        
        for i in range(p2+1,self.Inst.NumJobs):
            check=-1
            for j in range(p1,p2+1):
                if offspring1.Genotype[i][0] == genitore2.Genotype[j][0]:
                    check = j
                    while True:
                        doublecheck = False
                        for k in range(p1,p2+1):
                            if genitore1.Genotype[check][0] == genitore2.Genotype[k][0]:
                                check = k
                                doublecheck = True
                        if doublecheck == False:
                            break                    
                    break
            if check > -1:
                offspring1.Genotype[i] = copy.deepcopy(genitore1.Genotype[check])
                
            check=-1
            for j in range(p1,p2+1):
                if offspring2.Genotype[i][0] == genitore1.Genotype[j][0]:
                    check = j
                    while True:
                        doublecheck = False
                        for k in range(p1,p2+1):
                            if genitore2.Genotype[check][0] == genitore1.Genotype[k][0]:
                                check = k
                                doublecheck = True
                        if doublecheck == False:
                            break                    
                    break
            if check > -1:
                offspring2.Genotype[i] = copy.deepcopy(genitore2.Genotype[check])
        # print(p1,p2)
        # print(genitore1.Genotype)
        # print(genitore2.Genotype)
        # print(offspring1.Genotype)
        # print(offspring2.Genotype)
            offspring1.Fitness, offspring1.Makespan, offspring1.OverLoadMac, offspring1.Recharges = offspring1.ComputeFitness()
            offspring2.Fitness, offspring2.Makespan, offspring2.OverLoadMac, offspring2.Recharges = offspring2.ComputeFitness()
        return offspring1, offspring2
    
    def Mutation(self,offspring, threshold1, threshold2):
        
        # mutazione macchina
        check = random.random()
        if check <= threshold1:
            p1= random.randint(0,self.Inst.NumJobs-1)
            p2= random.randint(0,self.Inst.NumMachines-1)
            offspring.Genotype[p1]=(offspring.Genotype[p1][0],p2)
        
        # mutazione posizione job
        check = random.random()
        if check <= threshold2:
            p1= random.randint(0,self.Inst.NumJobs-1)
            p2= random.randint(0,self.Inst.NumJobs-1)
            check = offspring.Genotype[p1]
            offspring.Genotype[p1]=offspring.Genotype[p2]
            offspring.Genotype[p2]= check
        
             
        return offspring

    def SelezioneMontecarlo(self):

        # clacola la fitness inversa cumulata di ogni candidato
        SumInvFitness = 0
        for i in range(len(self.Population)) :
            SumInvFitness = SumInvFitness + 1/self.Population[i].Fitness

        FitnessCum = [1/(SumInvFitness * self.Population[0].Fitness)]
        for i in range(1, len(self.Population)) :
            FitnessCum.append(FitnessCum[i-1] + 1/(SumInvFitness * self.Population[i].Fitness))

        # individua genitore1
        first = random.random() 

        found = False
        if first <= FitnessCum[0] :
            genitore1 = self.Population[0]
            found = True
        i = 1
        while not found :
            if first <= FitnessCum[i] :
                genitore1 = self.Population[i]
                found = True
            i = i + 1

        # individua genitore2
        stop = False
        while not stop :
            second = random.random() 
            found = False
            if second <= FitnessCum[0] :
                genitore2 = self.Population[0]
                found = True
            i = 1
            while not found :
                if second <= FitnessCum[i] :
                    genitore2 = self.Population[i]
                    found = True
                i = i + 1

            if genitore1 != genitore2 :
                stop = True

        return genitore1, genitore2

    def UpdatePopulation(self, figlio1, figlio2):

        # selezione due moribondi

        # clacola la fitness inversa cumulata di ogni candidato
        SumFitness = 0
        for i in range(len(self.Population)) :
            SumFitness = SumFitness + self.Population[i].Fitness

        FitnessCum = [self.Population[0].Fitness]
        for i in range(1, len(self.Population)) :
            FitnessCum.append(FitnessCum[i-1] + self.Population[i].Fitness)

        EliteArray = self.Elite(self.NumElite)

        # individua moribondo 1 e lo sostituisce con figlio 1
        moribondo1 = -1
        moribondo2 = -1
        stop = False
        while not stop :
            first = random.random() * SumFitness
            found = False
            if first <= FitnessCum[0] :
                if 0 not in EliteArray :
                    self.Population[0] = figlio1
                    if figlio1.Fitness < self.BestCandidateFitness:
                        self.BestCandidateInd = 0
                        self.BestCandidateFitness = figlio1.Fitness   
                    moribondo1 = 0
                    stop = True
                found = True
            i = 1
            while not found :
                if first <= FitnessCum[i] :
                    if i not in EliteArray :
                        self.Population[i] = figlio1
                        if figlio1.Fitness < self.BestCandidateFitness:
                            self.BestCandidateInd = i
                            self.BestCandidateFitness = figlio1.Fitness   
                        moribondo1 = i
                        stop = True
                    found = True
                i = i + 1

        # individua moribondo 2 e lo sostituisce con figlio 2
        stop = False
        while not stop :
            second = random.random() *  SumFitness
            found = False
            if second <= FitnessCum[0] :
                if 0 not in EliteArray and moribondo1 != 0:
                    self.Population[0] = figlio2
                    if figlio2.Fitness < self.BestCandidateFitness:
                        self.BestCandidateInd = 0
                        self.BestCandidateFitness = figlio2.Fitness   
                    moribondo2 = 0
                    stop = True
                found = True
            i = 1
            while not found :
                if second <= FitnessCum[i] :
                    if i not in EliteArray and moribondo1 != i:
                        self.Population[i] = figlio2
                        if figlio2.Fitness < self.BestCandidateFitness:
                            self.BestCandidateInd = i
                            self.BestCandidateFitness = figlio2.Fitness   
                        moribondo2 = i
                        stop = True
                    found = True
                i = i + 1

        return

    def GenInitialPopulation(self):

        self.Population = []

        # Inserimento super candidati
        noffsup= self.NumSuperFigli
        for i in range(self.nsupcand):
            CandidateTemp = SuperCandidate(self.Inst,i, self.Codifica)
            if CandidateTemp.Fitness < self.BestCandidateFitness :
                    self.BestCandidateInd = i*(noffsup+1)
                    self.BestCandidateFitness = CandidateTemp.Fitness
            self.Population.append(CandidateTemp)
            # inserimento supercandidati modificati
            for j in range(noffsup):
                oldfit = CandidateTemp.Fitness
                NewCandidateTemp = copy.deepcopy(CandidateTemp)
                NewCandidateTemp = self.Mutation(NewCandidateTemp, 1, 1)
                NewCandidateTemp.Fitness = NewCandidateTemp.ComputeFitness()[0]
                if NewCandidateTemp.Fitness >= oldfit:
                    if NewCandidateTemp.Fitness < self.BestCandidateFitness :
                        self.BestCandidateInd = i*(noffsup+1) + j
                        self.BestCandidateFitness = NewCandidateTemp.Fitness
                    self.Population.append(NewCandidateTemp)
                else:
                    while NewCandidateTemp.Fitness < oldfit:
                        oldfit = NewCandidateTemp.Fitness
                        oldcand = copy.deepcopy(NewCandidateTemp)
                        NewCandidateTemp = self.Mutation(NewCandidateTemp, 1, 1)
                        NewCandidateTemp.Fitness = NewCandidateTemp.ComputeFitness()[0]
                    if oldcand.Fitness < self.BestCandidateFitness :
                        self.BestCandidateInd = i*(noffsup+1) + j
                        self.BestCandidateFitness = oldcand.Fitness
                    self.Population.append(oldcand)
                

        for i in range(self.nsupcand*(noffsup+1),self.PopSize) :
            CandidateTemp = Candidate(self.Inst, i, self.Codifica)
            if CandidateTemp.Fitness < self.BestCandidateFitness :
                self.BestCandidateInd = i
                self.BestCandidateFitness = CandidateTemp.Fitness

            self.Population.append(CandidateTemp)

        # preleva la migliore soluzione, la riottimizza risolvendo un problema di bin packing per ogni macchina
        #  e la memorizza in solution
        self.BestSol = Solution(self.Inst,self.Population[self.BestCandidateInd],self.Codifica)
        if self.BestSol.Makespan < self.BestCandidateFitness:
            self.Population[self.BestCandidateInd] = self.BestSol.Candidate
            self.BestCandidateFitness = self.BestSol.Makespan

        return

    def RicercaLocale(self, candidate):

        candidatetemp = Candidate(self.Inst, 1, 1)
        
        #bestCandidate = Candidate(self.Inst, 1, 1)
        #bestCandidate.CopyCandidate(candidate)  
        bestFitness = candidate.Fitness

        bestCandidate = copy.deepcopy(candidate)

        stop = False
        niter = 0

        while stop == False :

            stop = True
            niter = niter + 1

            for i in range(len(candidate.Genotype)-1):

                for j in range(i+1,len(candidate.Genotype)) :

                    #candidatetemp.CopyCandidate(candidate)
                    candidatetemp = copy.deepcopy(candidate)

                    temp = candidatetemp.Genotype[i]
                    candidatetemp.Genotype[i] = candidatetemp.Genotype[j]
                    candidatetemp.Genotype[j] = temp
                    candidatetemp.Fitness, candidatetemp.Makespan, candidatetemp.OverLoadMac, candidatetemp.Recharges = candidatetemp.ComputeFitness()

                    if candidatetemp.Fitness < bestFitness :
                        #bestCandidate.CopyCandidate(candidatetemp) 
                        bestCandidate = copy.deepcopy(candidatetemp)
                        bestFitness = candidatetemp.Fitness
                        stop = False
                        break

                    #candidatetemp.CopyCandidate(candidate)
                    candidatetemp = copy.deepcopy(candidate)

                    temp1 = list(candidatetemp.Genotype[i])
                    temp1[1] = candidatetemp.Genotype[j][1]
                    candidatetemp.Genotype[i] = tuple(temp1)

                    temp1 = list(candidatetemp.Genotype[j])
                    temp1[1] = candidatetemp.Genotype[i][1]
                    candidatetemp.Genotype[j] = tuple(temp1)
                    
                    candidatetemp.Fitness, candidatetemp.Makespan, candidatetemp.OverLoadMac, candidatetemp.Recharges = candidatetemp.ComputeFitness()

                    if candidatetemp.Fitness < bestFitness :
                        #bestCandidate.CopyCandidate(candidatetemp) 
                        bestCandidate = copy.deepcopy(candidatetemp)
                        bestFitness = candidatetemp.Fitness
                        stop = False
                if stop == False:
                    break
            
            if stop == True :
                for i in range(len(candidate.Genotype)):
                    for m in range(self.Inst.NumMachines) :
                        if m != candidate.Genotype[i][1] :

                            #candidatetemp.CopyCandidate(candidate)
                            candidatetemp = copy.deepcopy(candidate)

                            temp1 = list(candidatetemp.Genotype[i])
                            temp1[1] = m
                            candidatetemp.Genotype[i] = tuple(temp1)

                            candidatetemp.Fitness, candidatetemp.Makespan, candidatetemp.OverLoadMac, candidatetemp.Recharges = candidatetemp.ComputeFitness()

                            if candidatetemp.Fitness < bestFitness :
                                #bestCandidate.CopyCandidate(candidatetemp) 
                                bestCandidate = copy.deepcopy(candidatetemp)
                                bestFitness = candidatetemp.Fitness
                                stop = False
                                break
                    if stop == False:
                        break


        return bestCandidate





    
    