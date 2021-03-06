from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector
from reconstruct import *
from math import sqrt, cos

HM_max = 125 + 15
HM_min = 125 - 30
WM_max = 80 + 30
WM_offshell_max = 60

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
        BaseControlPlots.__init__(self, dir=dir, purpose="reco2", dataset=dataset, mode=mode)



    def beginJob(self):

        for particle in particleSelection:
            for i in range(len(algs)):
                self.add(particle+algs[i]+"Pt",particle+" Pt reco "+alg_titles[i],100,0,600)
                self.add(particle+algs[i]+"Eta",particle+" Eta reco "+alg_titles[i],100,-5,5)
                if particle=="HWW":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,800)
                elif particle=="HHbbWW":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,1500)
                else:
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,300)
        self.add("Hbb_d1M_window1","Hbb Mass reco (2D alg.) window1",100,85,160)
        self.add("Hbb_d1M_window2","Hbb Mass reco (2D alg.) window2",100,85,160)

        self.add2D("WWM_d1","Wjj Mass vs. Wlnu Mass (2D alg.)",100,0,300,100,0,300)
        
        self.add("case_d1","2D-reco case",5,0,5)
        self.add("Failed1_d1","2D-reco failed part 1 case",5,0,5)
        self.add("Failed2_d1","2D-reco failed part 2 case",5,0,5)
        self.add("JetCombs_d1M","combined jets Mass (2D alg.)",100,0,1000)



    def process(self, event):
    
        result = { }
        cases = [0,0,0]

#        category6 = len([ jet for jet in event.cleanedJets30 if jet.Eta < 2.5 ]) > 3 \
#                    and len([ jet for jet in event.bjets30 if jet.Eta < 2.5 ]) > 1

        if len(event.leadingLeptons) and len(event.bjets30)>1 and len(event.cleanedJets30)>3:# and category6:
        
            vectors = recoHWW_d1(event)
            if len(vectors) == 3:
                control = vectors
                cases = control[:3]
                masses = control[3:]
            
            elif len(vectors) > 3:
                [ q_Wlnu_d1, q_Wjj_d1, q_Hbb_d1, q_HWW_d1, q_HHbbWW_d1, control] = vectors
                cases = control[:3]
                masses = control[3:]
                
                result["Wlnu_d1Pt"] = q_Wlnu_d1.Pt()
                result["Wlnu_d1Eta"] = q_Wlnu_d1.Eta()
                result["Wlnu_d1M"] = q_Wlnu_d1.M()
                
                result["Wjj_d1Pt"] = q_Wjj_d1.Pt()
                result["Wjj_d1Eta"] = q_Wjj_d1.Eta()
                result["Wjj_d1M"] = q_Wjj_d1.M()
                
                result["Hbb_d1Pt"] = q_Hbb_d1.Pt()
                result["Hbb_d1Eta"] = q_Hbb_d1.Eta()
                result["Hbb_d1M"] = q_Hbb_d1.M()
                
                result["HWW_d1Pt"] = q_HWW_d1.Pt()
                result["HWW_d1Eta"] = q_HWW_d1.Eta()
                result["HWW_d1M"] = q_HWW_d1.M()
                
                result["HHbbWW_d1Pt"] = q_HHbbWW_d1.Pt()
                result["HHbbWW_d1Eta"] = q_HHbbWW_d1.Eta()
                result["HHbbWW_d1M"] = q_HHbbWW_d1.M()
    
                result["WWM_d1"] = [[ q_Wlnu_d1.M(), q_Wjj_d1.M() ]]
                
                if HM_min < q_Hbb_d1.M() < HM_max: #and HM_min < q_HWW_d1.M() < HM_max:
                    result["Hbb_d1M_window1"] = q_Hbb_d1.M()
                    if q_Wlnu_d1.M() < WM_max and q_Wjj_d1.M() < WM_offshell_max:
                        result["Hbb_d1M_window2"] = q_Hbb_d1.M()

            result["case_d1"] = cases[0]
            result["Failed1_d1"] = cases[1]
            result["Failed2_d1"] = cases[2]
            result["JetCombs_d1M"] = masses
        
        
        
        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], recoControlPlots())


