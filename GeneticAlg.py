
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


import numpy as np
import math 
import random
import copy
import numpy

class GeneticAlg():

    def __init__(self, Inst, PopSize, NumOfIterations):

        self.Inst = Inst 
        self.PopSize = PopSize 
        self.NumOfIterations = NumOfIterations 

        # genera la popolazione iniziale

        self.Population = []

        self.BestCandidateFitness = 100000000
        self.BestCandidateInd = -1
        for i in range(self.PopSize) :
            CandidateTemp = Candidate(Inst, i)
            if CandidateTemp.Fitness < self.BestCandidateFitness :
                self.BestCandidateInd = i
                self.BestCandidateFitness = CandidateTemp.Fitness

            self.Population.append(CandidateTemp)

        # preleva la migliore soluzione, la riottimizza risolvendo un problema di bin packing per ogni macchina
        #  e la memorizza in solution
        self.BestSol = Solution(Inst,self.Population[self.BestCandidateInd])

        # ALGORITMO GENETICO
        for iter in range(self.NumOfIterations) :
            # Seleziona una coppia di genitori con il metodo Montecarlo
            Newpop = self.Elite(self.Population,3)
            self.BestCandidateInd = 0
            
            while len(Newpop) <= self.PopSize:
                genitore1, genitore2 = self.SelezioneMontecarlo()
                
                
                offspring1, offspring2 = self.Crossover(genitore1, genitore2)
    
    
                offspring1 = self.Mutation(offspring1,0.10,0.10)
                
                offspring2 = self.Mutation(offspring2,0.10,0.10)
                
                offspring1.Makespan, offspring1.OverLoadMac, offspring1.Recharges = offspring1.ComputeFitness()

                offspring1.Fitness = max(offspring1.Makespan)
                if offspring1.Fitness < self.BestCandidateFitness:
                    self.BestCandidateFitness = offspring1.Fitness
                    self.BestSol = offspring1
                    self.BestCandidateInd = len(Newpop)
                
                Newpop.append(offspring1)
                    
                
                offspring2.Makespan, offspring2.OverLoadMac, offspring2.Recharges = offspring2.ComputeFitness()

                offspring2.Fitness = max(offspring2.Makespan)
                if offspring2.Fitness < self.BestCandidateFitness:
                    self.BestCandidateFitness = offspring2.Fitness
                    self.BestSol = offspring2
                    self.BestCandidateInd = len(Newpop)
                
                
                Newpop.append(offspring2)
            
            self.Population = Newpop
            
            self.BestSol = Solution(Inst,self.Population[self.BestCandidateInd])


    def Elite(self,Oldpop,nelite):
        
        Newpop = []
        val = []
        for i in Oldpop:
                val.append(i.Fitness)
        idbest = numpy.argsort(val)
        
        for i in range(nelite):
            Newpop.append(Oldpop[idbest[i]])
        return Newpop

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
                    break
            if check > -1:
                offspring1.Genotype[i] = copy.deepcopy(genitore1.Genotype[j])
                
            check=-1
            for j in range(p1,p2+1):
                if offspring2.Genotype[i][0] == genitore1.Genotype[j][0]:
                    check = j
                    break
            if check > -1:
                offspring2.Genotype[i] = copy.deepcopy(genitore2.Genotype[j])
        
        for i in range(p2+1,self.Inst.NumJobs):
            check=-1
            for j in range(p1,p2+1):
                if offspring1.Genotype[i][0] == genitore2.Genotype[j][0]:
                    check = j
                    break
            if check > -1:
                offspring1.Genotype[i] = copy.deepcopy(genitore1.Genotype[j])
                
            check=-1
            for j in range(p1,p2+1):
                if offspring2.Genotype[i][0] == genitore1.Genotype[j][0]:
                    check = j
                    break
            if check > -1:
                offspring2.Genotype[i] = copy.deepcopy(genitore2.Genotype[j])
        # print(p1,p2)
        # print(genitore1.Genotype)
        # print(genitore2.Genotype)
        # print(offspring1.Genotype)
        # print(offspring2.Genotype)
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


    
    