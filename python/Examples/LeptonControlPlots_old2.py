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
      self.add("NMuons",";N muons (p_{T}>20 GeV);N",10,0,10)
      self.add("Muon1Pt",";Muon Pt;N",100,0,500)
      self.add("Muon1Eta",";Muon Eta;N",50,-2.5,2.5)
      self.add("Muon2Pt",";Muon Pt;N",100,0,500)
      self.add("Muon2Eta",";Muon Eta;N",50,-2.5,2.5)
      self.add("NElectrons",";N electrons (p_{T}>20 GeV);N",10,0,10)
      self.add("Electron1Pt",";Electron Pt;N",100,0,500)
      self.add("Electron1Eta",";Electron Eta;N",50,-2.5,2.5)
      self.add("Electron2Pt",";Electron Pt;N",100,0,500)
      self.add("Electron2Eta",";Electron Eta;N",50,-2.5,2.5)

    def process(self, event):
      #get information
      result = { }
      result["NMuons"] = len([m for m in event.muons if m.PT>20])
      result["Muon1Pt"] = [ ]
      result["Muon1Eta"] = [ ]
      result["Muon2Pt"] = [ ]
      result["Muon2Eta"] = [ ]
      if event.muons.GetEntries()>0:
        result["Muon1Pt"].append(event.muons[0].PT)
        result["Muon1Eta"].append(event.muons[0].Eta)
      if event.muons.GetEntries()>1:
        result["Muon2Pt"].append(event.muons[1].PT)
        result["Muon2Eta"].append(event.muons[1].Eta)
      result["NElectrons"] = len([e for e in event.electrons if e.PT>20])
      result["Electron1Pt"] = [ ]
      result["Electron1Eta"] = [ ]
      result["Electron2Pt"] = [ ]
      result["Electron2Eta"] = [ ]
      if event.electrons.GetEntries()>0:
        result["Electron1Pt"].append(event.electrons[0].PT)
        result["Electron1Eta"].append(event.electrons[0].Eta)
      if event.electrons.GetEntries()>1:
        result["Electron2Pt"].append(event.electrons[1].PT)
        result["Electron2Eta"].append(event.electrons[1].Eta)
      return result

if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], LeptonControlPlots())

