
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
#       1) ApdateSol(self, genotype) -> aggiorna la soluzione
#
#=====================================================================================================

from Instance import Instance

class Solution():

    def __init__(self, Inst):

        self.Inst = Inst 

        self.IsEas = False

        self.Makespan = 0

        self.ListOfJobs = [[] for i in range(Inst.NumMachines)]

        numrich = 0

     
    def ApdateSol(self, genotype):

        update = True

        # ..............


        return update