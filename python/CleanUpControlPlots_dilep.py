from BaseControlPlots import BaseControlPlots
#from ROOT import TLorentzVector
#from reconstruct import reconstructWlnu

# Requirements:
# event.muons
# event.electrons

class CleanUpControlPlots(BaseControlPlots):
    """A class to create control plots for leptons"""

    def __init__(self, dir=None, dataset=None, mode="plots"):
      # create output file if needed. If no file is given, it means it is delegated
      BaseControlPlots.__init__(self, dir=dir, purpose="cleanup", dataset=dataset, mode=mode)

    def beginJob(self):
      # declare histograms
      self.add("M_ll","lepton-lepton Mass",100,0,300)
      self.add("M_jj","bjet-bjet Mass",100,0,300)
      self.add("DeltaR_ll","lepton-lepton DeltaR_ll",100,0,4.5)
      self.add("DeltaR_jj","bjet-bjet DeltaR_jj",100,0,4.5)
      self.add("DeltaPhi_jjll","DeltaPhi_jjll",100,0,3.5)

    # get information
    def process(self, event):
    
        result = { }
        
        if event.M_ll:
            result["M_ll"] = event.M_ll
        if event.M_jj:
            result["M_jj"] = event.M_jj
        if event.DeltaR_ll:
            result["DeltaR_ll"] = event.DeltaR_ll
        if event.DeltaR_jj:
            result["DeltaR_jj"] = event.DeltaR_jj
        if event.DeltaPhi_jjll:
            result["DeltaPhi_jjll"] = event.DeltaPhi_jjll

        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], LeptonControlPlots())

