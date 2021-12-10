
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

    def __init__(self, Inst, PopSize, NumOfGen, NumOfIterationsPerGen, ProbMutation1, ProbMutation2, NumElite):

        self.Inst = Inst 
        self.PopSize = PopSize 
        self.NumOfGen = NumOfGen
        self.NumOfIterationsPerGen = NumOfIterationsPerGen
        self.ProbMutation1 = ProbMutation1
        self.ProbMutation2 = ProbMutation2
        self.NumElite = NumElite

        # genera la popolazione iniziale

        self.Population = []

        self.BestCandidateFitness = 100000000
        self.BestCandidateInd = -1
        # Inserimento super candidate
        nsupcand = 4
        for i in range(nsupcand):
            CandidateTemp = SuperCandidate(Inst,i)
            if CandidateTemp.Fitness < self.BestCandidateFitness :
                    self.BestCandidateInd = i
                    self.BestCandidateFitness = CandidateTemp.Fitness
            self.Population.append(CandidateTemp)

        for i in range(nsupcand,self.PopSize) :
            CandidateTemp = Candidate(Inst, i)
            if CandidateTemp.Fitness < self.BestCandidateFitness :
                self.BestCandidateInd = i
                self.BestCandidateFitness = CandidateTemp.Fitness

            self.Population.append(CandidateTemp)

        # preleva la migliore soluzione, la riottimizza risolvendo un problema di bin packing per ogni macchina
        #  e la memorizza in solution
        self.BestSol = Solution(Inst,self.Population[self.BestCandidateInd])
        if self.BestSol.Makespan < self.Population[self.BestCandidateInd].Fitness:
            self.Population[self.BestCandidateInd] = self.BestSol.Candidate

        # ALGORITMO GENETICO
        for gen in range(self.NumOfGen) :

            for iter in range(self.NumOfIterationsPerGen) :

                # Seleziona una coppia di genitori con il metodo Montecarlo
                genitore1, genitore2 = self.SelezioneMontecarlo()
                
                figlio1, figlio2 = self.Crossover(genitore1, genitore2)
                
                if figlio1.Fitness < self.BestCandidateFitness:
                    update, figlio1 = self.BestSol.UpdateSol(figlio1)
                
                if figlio2.Fitness < self.BestCandidateFitness:
                    update, figlio2 = self.BestSol.UpdateSol(figlio2)
                
                figlio1 = self.Mutation(figlio1, self.ProbMutation1, self.ProbMutation2)
                
                figlio2 = self.Mutation(figlio2, self.ProbMutation1, self.ProbMutation2)
                
                if figlio1.Fitness < self.BestCandidateFitness:
                    update, figlio1 = self.BestSol.UpdateSol(figlio1)
                
                if figlio2.Fitness < self.BestCandidateFitness:
                    update, figlio2 = self.BestSol.UpdateSol(figlio2)
                    
                self.UpdatePopulation(figlio1, figlio2)


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



    
    