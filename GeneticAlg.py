
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
        #self.BestSol = Solution(Inst)
        #self.BestSol.update(self.Population[self.BestCandidateInd])

        # ALGORITMO GENETICO
        for iter in range(self.NumOfIterations) :
            # Seleziona una coppia di genitori con il metodo Montecarlo
            genitore1, genitore2 = self.SelezioneMontecarlo()




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


    
    