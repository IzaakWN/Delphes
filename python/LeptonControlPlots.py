from BaseControlPlots import BaseControlPlots
#from ROOT import TLorentzVector
#from reconstruct import reconstructWlnu

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
      self.add("NMuons20","muons multiplicity (Pt>20 GeV)",10,0,10)
      self.add("Muon1Pt","muon Pt",100,0,500)
      self.add("Muon1Eta","muon Eta",50,-2.5,2.5)
      self.add("Muon2Pt","muon Pt",100,0,500)
      self.add("Muon2Eta","muon Eta",50,-2.5,2.5)
      self.add("NElectrons20","electrons multiplicity (Pt>20 GeV)",10,0,10)
      self.add("NElectrons25","electrons multiplicity (Pt>25 GeV)",10,0,10)
      self.add("Electron1Pt","electron Pt",100,0,500)
      self.add("Electron1Eta","electron Eta",50,-2.5,2.5)
      self.add("Electron2Pt","electron Pt",100,0,500)
      self.add("Electron2Eta","electron Eta",50,-2.5,2.5)
      self.add("NLeptons20","lepton multiplicity (Pt>20 GeV)",10,0,10)
      self.add("Lepton1Pt","lepton Pt",100,0,500)
      self.add("Lepton1Eta","lepton Eta",50,-2.5,2.5)
      self.add("Lepton2Pt","lepton Pt",100,0,500)
      self.add("Lepton2Eta","lepton Eta",50,-2.5,2.5)

    # get information
    def process(self, event):
    
        result = { }
        
        # Muons
        result["NMuons20"] = len([m for m in event.muons if m.PT>20])
        if event.muons.GetEntries()>0:
            result["Muon1Pt"] = event.muons[0].PT
            result["Muon1Eta"] = event.muons[0].Eta
        if event.muons.GetEntries()>1:
            result["Muon2Pt"] = event.muons[1].PT
            result["Muon2Eta"] = event.muons[1].Eta

        # Electrons
        result["NElectrons20"] = len([e for e in event.electrons if e.PT>20])
        result["NElectrons25"] = len([e for e in event.electrons if e.PT>25])
        if event.electrons.GetEntries()>0:
            result["Electron1Pt"] = event.electrons[0].PT
            result["Electron1Eta"] = event.electrons[0].Eta
        if event.electrons.GetEntries()>1:
            result["Electron2Pt"] = event.electrons[1].PT
            result["Electron2Eta"] = event.electrons[1].Eta
        
        # Leptons
        result["NLeptons20"] = result["NMuons20"] + result["NElectrons20"]
        if len(event.leadingLeptons)>0:
            result["Lepton1Pt"] = event.leadingLeptons[0].PT
            result["Lepton1Eta"] = event.leadingLeptons[0].Eta
            if len(event.leadingLeptons)>1:
                result["Lepton2Pt"] = event.leadingLeptons[1].PT
                result["Lepton2Eta"] = event.leadingLeptons[1].Eta

        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], LeptonControlPlots())

