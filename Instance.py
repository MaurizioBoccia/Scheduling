
import numpy as np
import math 

#=====================================================================================================
# Classe Instance
#   attributi:
#       1) Name -> nome dell'istanza
#
#       3) NumMachines -> numero di macchine
#       2) NumJobs -> numero di clienti
#       4) ChargingTime -> tempo di ricarica
#       5) MaxChargeLevel -> valore massimo della ricarica
#
#       6) Dur -> Dur[j i] durata del job j sulla macchina i
#       7) Weight -> Weight[j i] peso del job j sulla macchina i
#
#   metodi: 
#
#=====================================================================================================
  

class Instance():

    def __init__(self, Name):

        self.name = Name 

        #apre il file in lettura
        file = open(Name,"r")
        a=file.readlines()
        split_string = a[0].split("\t")

        #numero di macchine
        StringTemp=split_string[0]
        StringTempSplitted = StringTemp.split(':')
        self.NumMachines = int(StringTempSplitted[1])

        #numero di job
        StringTemp=split_string[1]
        StringTempSplitted = StringTemp.split(':')
        self.NumJobs = int(StringTempSplitted[1])

        #charging time
        StringTemp=split_string[2]
        StringTempSplitted = StringTemp.split(':')
        self.ChargingTime = int(StringTempSplitted[1])

        #valore massimo della ricarica
        StringTemp=split_string[3]
        StringTempSplitted = StringTemp.split(':')
        self.MaxChargeLevel = int(StringTempSplitted[1])

        self.Dur = np.zeros((self.NumJobs + 1, self.NumMachines))
        for r in range (2, 2 + self.NumJobs) :
            StringTempSplitted = a[r].split("\t")
            for i in range(self.NumMachines) :
                self.Dur[r-2][i] = float(StringTempSplitted[i])

        for i in range(self.NumMachines) :
            self.Dur[self.NumJobs][i] = float(self.ChargingTime)

        self.Weight = np.zeros((self.NumJobs, self.NumMachines))    
        for r in range (4 + self.NumJobs, 4 + 2*self.NumJobs) :
            StringTempSplitted = a[r].split("\t")
            for i in range(self.NumMachines) :
                self.Weight[r - 4 - self.NumJobs][i] = float(StringTempSplitted[i])

        file.close()


 
