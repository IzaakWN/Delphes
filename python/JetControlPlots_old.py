from BaseControlPlots import BaseControlPlots

# Requirements:
# event.jets
# event.bjets
# event.MEt

class JetControlPlots(BaseControlPlots):
    """A class to create control plots for jetmet"""

    def __init__(self, dir=None, dataset=None, mode="plots"):
      # create output file if needed. If no file is given, it means it is delegated
      BaseControlPlots.__init__(self, dir=dir, purpose="jetmet", dataset=dataset, mode=mode)

    def beginJob(self):
      # declare histograms
      self.add("Njets","Jet multiplicity",10,0,10)
      self.add("Jet1Pt","Jet Pt",100,0,200)
      self.add("Jet1Eta","Jet Eta",100,-5,5)
      self.add("Jet1Phi","Jet Phi",64,-3.2,3.2)
      self.add("Jet2Pt","Jet Pt",100,0,200)
      self.add("Jet2Eta","Jet Eta",100,-5,5)
      self.add("Jet2Phi","Jet Phi",64,-3.2,3.2)
      self.add("Jet3Pt","Jet Pt",100,0,200)
      self.add("Jet3Eta","Jet Eta",100,-5,5)
      self.add("Jet3Phi","Jet Phi",64,-3.2,3.2)
      self.add("Jet4Pt","Jet Pt",100,0,200)
      self.add("Jet4Eta","Jet Eta",100,-5,5)
      self.add("Jet4Phi","Jet Phi",64,-3.2,3.2)
      self.add("Nbjets","B Jet multiplicity",10,0,10)
      self.add("BJet1Pt","B Jet Pt",100,0,200)
      self.add("BJet1Eta","B Jet Eta",100,-5,5)
      self.add("BJet1Phi","B Jet Phi",64,-3.2,3.2)
      self.add("BJet2Pt","B Jet Pt",100,0,200)
      self.add("BJet2Eta","B Jet Eta",100,-5,5)
      self.add("BJet2Phi","B Jet Phi",64,-3.2,3.2)
      self.add("BJet3Pt","B Jet Pt",100,0,200)
      self.add("BJet3Eta","B Jet Eta",100,-5,5)
      self.add("BJet3Phi","B Jet Phi",64,-3.2,3.2)
      self.add("BJet4Pt","B Jet Pt",100,0,200)
      self.add("BJet4Eta","B Jet Eta",100,-5,5)
      self.add("BJet4Phi","B Jet Phi",64,-3.2,3.2)
      self.add("MET","MET",100,0,200)
      self.add("METphi","MET phi",64,-3.2,3.2)

    def process(self, event):
      #get information
      result = { }
      result["Njets"]  = event.jets.GetEntries()
      result["Jet1Pt"] = [ ]
      result["Jet1Eta"] = [ ]
      result["Jet1Phi"] = [ ]
      result["Jet2Pt"] = [ ]
      result["Jet2Eta"] = [ ]
      result["Jet2Phi"] = [ ]
      result["Jet3Pt"] = [ ]
      result["Jet3Eta"] = [ ]
      result["Jet3Phi"] = [ ]
      result["Jet4Pt"] = [ ]
      result["Jet4Eta"] = [ ]
      result["Jet4Phi"] = [ ]
      if event.jets.GetEntries()>0:
        result["Jet1Pt"].append(event.jets[0].PT)
        result["Jet1Eta"].append(event.jets[0].Eta)
        result["Jet1Phi"].append(event.jets[0].Phi)
      if event.jets.GetEntries()>1:
        result["Jet2Pt"].append(event.jets[1].PT)
        result["Jet2Eta"].append(event.jets[1].Eta)
        result["Jet2Phi"].append(event.jets[1].Phi)
      if event.jets.GetEntries()>2:
        result["Jet3Pt"].append(event.jets[2].PT)
        result["Jet3Eta"].append(event.jets[2].Eta)
        result["Jet3Phi"].append(event.jets[2].Phi)
      if event.jets.GetEntries()>3:
        result["Jet4Pt"].append(event.jets[3].PT)
        result["Jet4Eta"].append(event.jets[3].Eta)
        result["Jet4Phi"].append(event.jets[3].Phi)
      bjets=[]
      for jet in event.jets:
        if jet.BTag:
          bjets+=[jet]
      result["Nbjets"] = len(bjets)
      result["BJet1Pt"] = [ ]
      result["BJet1Eta"] = [ ]
      result["BJet1Phi"] = [ ]
      result["BJet2Pt"] = [ ]
      result["BJet2Eta"] = [ ]
      result["BJet2Phi"] = [ ]
      result["BJet3Pt"] = [ ]
      result["BJet3Eta"] = [ ]
      result["BJet3Phi"] = [ ]
      result["BJet4Pt"] = [ ]
      result["BJet4Eta"] = [ ]
      result["BJet4Phi"] = [ ]
      if len(bjets)>0:
        result["BJet1Pt"].append(bjets[0].PT)
        result["BJet1Eta"].append(bjets[0].Eta)
        result["BJet1Phi"].append(bjets[0].Phi)
      if len(bjets)>1:
        result["BJet2Pt"].append(bjets[1].PT)
        result["BJet2Eta"].append(bjets[1].Eta)
        result["BJet2Phi"].append(bjets[1].Phi)
      if len(bjets)>2:
        result["BJet3Pt"].append(bjets[2].PT)
        result["BJet3Eta"].append(bjets[2].Eta)
        result["BJet3Phi"].append(bjets[2].Phi)
      if len(bjets)>3:
        result["BJet4Pt"].append(bjets[3].PT)
        result["BJet4Eta"].append(bjets[3].Eta)
        result["BJet4Phi"].append(bjets[3].Phi)
      result["MET"] = event.met[0].MET
      result["METphi"] = event.met[0].Phi
      return result

if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], JetControlPlots())

