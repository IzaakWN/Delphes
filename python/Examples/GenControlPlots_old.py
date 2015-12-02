from BaseControlPlots import BaseControlPlots

# Requirements:
# event.Hs
# event.bHs
# event.MEt

class GenControlPlots(BaseControlPlots):
    """A class to create control plots for Hmet"""

    def __init__(self, dir=None, dataset=None, mode="plots"):
      # create output file if needed. If no file is given, it means it is delegated
      BaseControlPlots.__init__(self, dir=dir, purpose="Hmet", dataset=dataset, mode=mode)

    def beginJob(self):
      # declare histograms
      self.add("Nhiggs","Higgs multiplicity",10,0,10)
      self.add("Nleptons","Lepton multiplicity",10,0,10)
      self.add("Nbquarks","b-quark multiplicity",10,0,10)
      self.add("Nlquarks","l-quark multiplicity",10,0,10)
      self.add("HbbPt","H Pt",100,0,200)
      self.add("HbbEta","H Eta",100,-5,5)
      self.add("HbbPhi","H Phi",64,-3.2,3.2)
      self.add("HWWPt","H Pt",100,0,200)
      self.add("HWWEta","H Eta",100,-5,5)
      self.add("HWWPhi","H Phi",64,-3.2,3.2)

    def process(self, event):
      #get information
      result = { }
      nHiggs=0
      nLeptons=0
      nBquarks=0
      nLquarks=0
      result["HbbPt"] = []
      result["HbbEta"] = []
      result["HbbPhi"] = []
      result["HWWPt"] = []
      result["HWWEta"] = []
      result["HWWPhi"] = []
      for particle in event.particles:
          if abs(particle.PID) == 24:
	     if abs(event.particles[particle.D1].PID) in [11,13,15]:
	       nLeptons+=1
	     if abs(event.particles[particle.D1].PID) in [1,2,3,4]:
	       nLquarks+=2
          if abs(particle.PID) == 25:
	     if abs(event.particles[particle.D1].PID) in [5]:
	        nBquarks+=2
                result["HbbPt"].append( particle.PT )
	        result["HbbEta"].append( particle.Eta )
	        result["HbbPhi"].append( particle.Phi )
	     if abs(event.particles[particle.D1].PID) in [24]:
	        result["HWWPt"].append( particle.PT )
	        result["HWWEta"].append( particle.Eta )
	        result["HWWPhi"].append( particle.Phi )
	     nHiggs+=1
      result["Nhiggs"]  = nHiggs
      result["Nleptons"]  = nLeptons
      result["Nbquarks"]  = nBquarks
      result["Nlquarks"]  = nLquarks
      return result

if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], GenControlPlots())

