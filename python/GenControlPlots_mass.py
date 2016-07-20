from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
from math import sqrt, pow, cos
from operator import attrgetter
from fold import fold

# Requirements:
# event.Hs
# event.bHs
# event.MET



class GenControlPlots(BaseControlPlots):
    """A class to create control plots for HH and tt -> bbWW"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="gen", dataset=dataset, mode=mode)



    def beginJob(self):
        
        self.add("NW_offshell","offshell W's multiplicity gen",5,0,5)
        self.add("NWlnu","Wlnu multiplicity gen",5,0,5)
        self.add("NWqq","Wqq multiplicity gen",5,0,5)
        
        self.add2D("WWM","Wqq Mass vs. Wlnu Mass gen",100,0,150,100,0,150)
        self.add("WlnuM","Wqq Mass gen",100,0,150)
        self.add("WqqM","Wqq Mass gen",100,0,150)



    def process(self, event):
        
        result = { }
        result["WlnuM"] = [ ]
        result["WqqM"] = [ ]
        
        dict = event.particle_dict
        
        nW_offshell = 0
        nWlnu = 0
        nWqq = 0
        
        for W in dict['W bosons']:
        
            if abs(event.particles[W.D1].PID) in [11,13]: # LEPTONIC W
                nWlnu+=1
                result["WlnuM"].append( W.Mass )
                if abs(80.4-particle.Mass) > 10: # check if W is virtual
                    nW_offshell += 1
                        
            elif abs(event.particles[W.D1].PID) in [1,2,3,4,5]: # HADRONIC W
                    nWqq+=1
                result["WqqM"].append( W.Mass )
                if abs(80.4-particle.Mass) > 10:
                    nW_offshell += 1


        # __WW_2D-plots__
        if len( result["WlnuM"] ) == 1 and len( result["WqqM"] ) == 1: # semileptonic
            result["WWM"]  = [[ result["WlnuM"][0],  result["WqqM"][0] ]]
        else: print "Warning! GenControlPlots.py: No WW 2D-plot!"

        result["NWlnu"] = nWlnu
        result["NWqq"] = nWqq
        result["NW_offshell"] = nW_offshell
        
        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], GenControlPlots())


