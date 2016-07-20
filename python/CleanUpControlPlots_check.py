from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
from ROOT import TTree, TBranch
from itertools import combinations # to make jets combinations
# from copy import copy 
# from fold import fold
from math import sqrt, cos, pi
#from reconstruct import max_b2b
# from reconstruct import recoNeutrino, recoWlnu2Mt

# Requirements:
# event.muons
# event.electrons

class CleanUpControlPlots(BaseControlPlots):
    """A class to create control plots for leptons"""

    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="cleanup", dataset=dataset, mode=mode)

    def beginJob(self):
      
        # declare tree and branches

        self.add("M_jj100","jet-jet combinations Mass",100,0,300)



    # get information
    def process(self, event):
    
        result = { }
        
        jets = [ j for j in event.cleanedJets20 if not j.BTag ][:5]
        if len(jets) > 1 :
            jets100 = [ js for js in [j1.TLV+j2.TLV for j1, j2 in combinations(jets,2)] if js.M() < 100 ]
            if len(jets100):
                jets100 = max( jets100, key = lambda js: js.Pt())
                result["M_jj100"] = jets100.M()
            else:
                result["M_jj100"] = ( jets[0].TLV + jets[1].TLV ).M()
            
        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], CleanUpControlPlots())

