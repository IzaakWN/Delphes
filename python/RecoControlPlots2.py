from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector
from reconstruct import *
from math import sqrt, cos

# Requirements:
# event.muons
# event.electrons
# event.jets
# event.bjets
# event.met
# event.Hs
# event.bHs
# event.MEt

particleSelection = ["Wlnu","Wjj","Hbb","HWW","HHbbWW"]
vars = ["Pt","Eta","M"]
algs = ["_d1"]
alg_titles = ["(2D alg.)"]


class RecoControlPlots2(BaseControlPlots):
    """A class to create control plots for leptons"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="leptons", dataset=dataset, mode=mode)



    def beginJob(self):

        for particle in particleSelection:
            for i in range(len(algs)):
                self.add(particle+algs[i]+"Pt",particle+" Pt reco "+alg_titles[i],100,0,600)
                self.add(particle+algs[i]+"Eta",particle+" Eta reco "+alg_titles[i],100,-5,5)
                if particle=="HWW":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,800)
                elif particle=="HHbbWW":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],150,0,1500)
                else:
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,300)



    def process(self, event):
    
        result = { }

        for particle in particleSelection:
            for var in vars:
                for alg in algs:
                    result[particle+alg+var] = []
        
        hasLepton = (event.muons.GetEntries()>0) or (event.electrons.GetEntries()>0)

        category6 = len([ jet for jet in event.cleanedJets30 if jet.Eta < 2.5 ]) > 3 \
                    and len([ jet for jet in event.bjets30 if jet.Eta < 2.5 ]) > 1

        if hasLepton and len(event.bjets30)>1 and category6:
        
            vectors = recoHWW_d1(event)
            if len(vectors) > 0:
                [ q_Wlnu_d1, q_Wjj_d1, q_Hbb_d1, q_HWW_d1, q_HHbbWW_d1 ] = vectors
                
                result["Wlnu_d1Pt"].append(q_Wlnu_d1.Pt())
                result["Wlnu_d1Eta"].append(q_Wlnu_d1.Eta())
                result["Wlnu_d1M"].append(q_Wlnu_d1.M())
                
                result["Wjj_d1Pt"].append(q_Wjj_d1.Pt())
                result["Wjj_d1Eta"].append(q_Wjj_d1.Eta())
                result["Wjj_d1M"].append(q_Wjj_d1.M())
                
                result["Hbb_d1Pt"].append(q_Hbb_d1.Pt())
                result["Hbb_d1Eta"].append(q_Hbb_d1.Eta())
                result["Hbb_d1M"].append(q_Hbb_d1.M())
                
                result["HWW_d1Pt"].append(q_HWW_d1.Pt())
                result["HWW_d1Eta"].append(q_HWW_d1.Eta())
                result["HWW_d1M"].append(q_HWW_d1.M())
                
                result["HHbbWW_d1Pt"].append(q_HHbbWW_d1.Pt())
                result["HHbbWW_d1Eta"].append(q_HHbbWW_d1.Eta())
                result["HHbbWW_d1M"].append(q_HHbbWW_d1.M())
#            
#                print "RecoControlPlots2.py: succes!"
#            
#            else:
#                print "RecoControlPlots2.py: d1 did not come through..."

        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], recoControlPlots())


