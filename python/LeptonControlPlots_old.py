from BaseControlPlots import BaseControlPlots

# Requirements:
# event.muons
# event.electrons

class LeptonControlPlots(BaseControlPlots):
    """A class to create control plots for leptons"""

    def __init__(self, dir=None, dataset=None, mode="plots"):
      # create output file if needed. If no file is given, it means it is delegated
      BaseControlPlots.__init__(self, dir=dir, purpose="leptons", dataset=dataset, mode=mode)

    def beginJob(self):
      # declare histograms
      self.add("NMuons","Muon multiplicity",10,0,10)
      self.add("Muon1Pt","Muon Pt",100,0,250)
      self.add("Muon1Eta","Muon Eta",50,-2.5,2.5)
      self.add("Muon2Pt","Muon Pt",100,0,250)
      self.add("Muon2Eta","Muon Eta",50,-2.5,2.5)
      self.add("NElectrons","Electron multiplicity",10,0,10)
      self.add("Electron1Pt","Electron Pt",100,0,250)
      self.add("Electron1Eta","Electron Eta",50,-2.5,2.5)
      self.add("Electron2Pt","Electron Pt",100,0,250)
      self.add("Electron2Eta","Electron Eta",50,-2.5,2.5)

    def process(self, event):
      # get information
      result = { }
      
      result["NMuons"] = event.muons.GetEntries()
      result["Muon1Pt"] = [ ]
      result["Muon1Eta"] = [ ]
      result["Muon2Pt"] = [ ]
      result["Muon2Eta"] = [ ]
      if event.muons.GetEntries()>0: #
        result["Muon1Pt"].append(event.muons[0].PT)
        result["Muon1Eta"].append(event.muons[0].Eta)
      if event.muons.GetEntries()>1: #
        result["Muon2Pt"].append(event.muons[1].PT)
        result["Muon2Eta"].append(event.muons[1].Eta)
      
      result["NElectrons"] = event.electrons.GetEntries()
      result["Electron1Pt"] = [ ]
      result["Electron1Eta"] = [ ]
      result["Electron2Pt"] = [ ]
      result["Electron2Eta"] = [ ]
      if event.electrons.GetEntries()>0: #
        result["Electron1Pt"].append(event.electrons[0].PT)
        result["Electron1Eta"].append(event.electrons[0].Eta)
      if event.electrons.GetEntries()>1: # 
        result["Electron2Pt"].append(event.electrons[1].PT)
        result["Electron2Eta"].append(event.electrons[1].Eta)
      return result

if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], LeptonControlPlots())

