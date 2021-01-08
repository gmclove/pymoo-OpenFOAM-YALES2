################# Parent Class for running OpenFOAM from python  #####################################

#### Seperate runSim class architecture
# from os import path

from RunOpenFOAMv4.ExecuteSimulations import ExecuteSimulations
from RunOpenFOAMv4.PostProcess import PostProcess
from RunOpenFOAMv4.PreProcess import PreProcess


class RunOFv4(ExecuteSimulations, PreProcess, PostProcess):
    def __init__(self, case, x, gen, solver, mesher, procLim, nProc):  # , ind=0):
        self.case = case
        print(case)
        # array of variables for this generation's population
        #self.x = x
        # generation number
        #self.gen = gen

        #super().__init__(x, gen, solver, mesher)

        #self.preProc = PreProcess.__init__(self, x, gen, mesher, nProc)

        # self.exec = ExecuteSimulations.__init__(self, x, gen, solver, procLim, nProc)
        # self.postProc = PostProcess.__init__(self, x, gen)
        #self.preProc = super(PreProcess).__init__(self, x, gen, mesher, nProc)
        self.preProc = PreProcess(x, gen, mesher, nProc)
        self.exec = ExecuteSimulations(x, gen, solver, procLim, nProc)
        self.postProc = PostProcess(x, gen)
        #super().__init__()

        ##### Pre-Process/Execute/Post-Process Objects #####
        #self.preProc = PreProcess(x, gen, mesher, nProc)
        #self.exec = ExecuteSimulations(x, gen, solver, procLim, nProc)
        #self.postProc = PostProcess(x, gen)

        # os.mkdir('./cases/gen%i' %self.gen)

    def runGen(self):
        ##### SET-UP CASE FILES #####
        print("PRE-PROCESS")
        self.preProc.main(case=self.case)
        #### EXECUTE SIMULATIONS #####
        print("EXECUTE")
        # decide to run cases in parallel or serial
        self.exec.run()
        ##### POST-PROCESS #####
        print("POST-PROCESS")
        obj = self.postProc.main(case=self.case)

        return obj
