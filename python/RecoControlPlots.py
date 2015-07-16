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

particleSelection = ["Wjj","Hbb","HWW","HHbbWW"]
vars = ["Pt","Eta","M"]
algs = ["_b1","_b2"]#,"_c1","_c2"]
alg_titles = ["(one b-tag)","(two b-tag)","(no b-tag W on-shell)","(no b-tag)"]


class RecoControlPlots(BaseControlPlots):
    """A class to create control plots for leptons"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="leptons", dataset=dataset, mode=mode)



    def beginJob(self):

        self.add("Wlnu1Pt","Wlnu Pt reco",100,0,600) # Wlnu
        self.add("Wlnu1Eta","Wlnu Eta reco",100,-5,5)
        self.add("Wlnu1M","Wlnu Mass reco",100,0,200)
        
        self.add("Wlnu2Pt","Wlnu Pt reco 2",100,0,600) # Wlnu 2 without mass constrain
        self.add("Wlnu2Eta","Wlnu Eta reco 2",100,-5,5)
        self.add("Wlnu2M","Wlnu Mass reco 2",100,0,200)

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
    
        self.add("M_jetComb1","combined jets Mass (combination alg.)",100,0,1000) # M_jetComb combination alg.
        self.add("M_jetComb2","combined jets Mass (combination alg.2)",100,0,1000) # M_jetComb combination alg. 2
        self.add("WlnuMt","Wlnu reco Mt",100,0,300)



    def process(self, event):
    
        result = { }
        
        hasMuon = (event.muons.GetEntries()>0)
        hasElectron = (event.electrons.GetEntries()>0)
        hasLepton = hasMuon or hasElectron
        
        # choose which lepton has to be reconstructed
        if hasMuon:
            if hasElectron: # muon
                recoMuon = event.muons[0].PT > event.electrons[0].PT
            else:
                recoMuon = True
        else:
            recoMuon = False

        # __Wlnu__
        result["Wlnu1Pt"] = [ ]
        result["Wlnu1Eta"] = [ ]
        result["Wlnu1M"] = [ ]
        result["Wlnu2Pt"] = [ ]
        result["Wlnu2Eta"] = [ ]
        result["Wlnu2M"] = [ ]
        result["WlnuMt"] = [ ]
            
        if recoMuon:
            q_Wlnu1 = recoWlnu1(13,event.muons[0],event.met[0])
            result["Wlnu1Pt"].append(q_Wlnu1.Pt())
            result["Wlnu1Eta"].append(q_Wlnu1.Eta())
            result["Wlnu1M"].append(q_Wlnu1.M())
            q_Wlnu2 = recoWlnu2(13,event.muons[0],event.met[0])
            result["Wlnu2Pt"].append(q_Wlnu2.Pt())
            result["Wlnu2Eta"].append(q_Wlnu2.Eta())
            result["Wlnu2M"].append(q_Wlnu2.M())
            result["WlnuMt"].append(sqrt(2*event.met[0].MET*event.muons[0].PT*(1-cos( event.muons[0].Phi-event.met[0].Phi) )))
        elif hasElectron:
            q_Wlnu1 = recoWlnu1(11,event.electrons[0],event.met[0])
            result["Wlnu1Pt"].append(q_Wlnu1.Pt())
            result["Wlnu1Eta"].append(q_Wlnu1.Eta())
            result["Wlnu1M"].append(q_Wlnu1.M())
            q_Wlnu2 = recoWlnu2(11,event.electrons[0],event.met[0])
            result["Wlnu2Pt"].append(q_Wlnu2.Pt())
            result["Wlnu2Eta"].append(q_Wlnu2.Eta())
            result["Wlnu2M"].append(q_Wlnu2.M())
            result["WlnuMt"].append(sqrt(2*event.met[0].MET*event.electrons[0].PT*(1-cos( event.electrons[0].Phi-event.met[0].Phi) )))
        
    
    
        # __Wjj,_Hbb___
        for particle in particleSelection:
            for var in vars:
                for alg in algs:
                    result[particle+alg+var] = []
        bjets = event.bjets
        result["M_jetComb1"] = [ ]
        result["M_jetComb2"] = [ ]
        if len(event.cleanedJets)>3:
        
#            # Combination alg.
#            [q_Hbb_c1, q_Wjj1_c1, M_jetComb] = recoHW_c1(event.cleanedJets)      # Combination alg.
#            result["Hbb_c1Pt"].append(q_Hbb_c1.Pt())
#            result["Hbb_c1Eta"].append(q_Hbb_c1.Eta())
#            result["Hbb_c1M"].append(q_Hbb_c1.M())
#            result["Wjj_c1Pt"].append(q_Wjj_c1.Pt())
#            result["Wjj_c1Eta"].append(q_Wjj_c1.Eta())
#            result["Wjj_c1M"].append(q_Wjj_c1.M())
#            result["M_jetComb1"].extend(M_jetComb1)
#            if hasLepton: # HWWc
#                q_HWW_c1 = q_Wjj_c1 + q_Wlnu1
#                result["HWW_c1Pt"].append(q_HWW_c1.Pt())
#                result["HWW_c1Eta"].append(q_HWW_c1.Eta())
#                result["HWW_c1M"].append(q_HWW_c1.M())
#                q_HHbbWW_c1 = q_Hbb_c1 + q_HWW_c1
#                result["HHbbWW_c1Pt"].append(q_HHbbWW_c1.Pt())
#                result["HHbbWW_c1Eta"].append(q_HHbbWW_c1.Eta())
#                result["HHbbWW_c1M"].append(q_HHbbWW_c1.M())
#
#            # Combination alg. 2
#            [q_Hbb_c2, q_Wjj_c2, M_jetCom_b2] = recoHW_c2(event.cleanedJets)    # Combination alg. 2
#            result["Hbb_c2Pt"].append(q_Hbb_c2.Pt())
#            result["Hbb_c2Eta"].append(q_Hbb_c2.Eta())
#            result["Hbb_c2M"].append(q_Hbb_c2.M())
#            result["Wjj_c2Pt"].append(q_Wjj_c2.Pt())
#            result["Wjj_c2Eta"].append(q_Wjj_c2.Eta())
#            result["Wjj_c2M"].append(q_Wjj_c2.M())
#            result["M_jetCom_b2"].extend(M_jetComb2)
#            if hasLepton: # HWW_c2
#                q_HWW_c2 = q_Wjj_c2 + q_Wlnu1
#                result["HWW_c2Pt"].append(q_HWW_c2.Pt())
#                result["HWW_c2Eta"].append(q_HWW_c2.Eta())
#                result["HWW_c2M"].append(q_HWW_c2.M())
#                q_HHbbWW_c2 = q_Hbb_c2 + q_HWW_c2
#                result["HHbbWW_c2Pt"].append(q_HHbbWW_c2.Pt())
#                result["HHbbWW_c2Eta"].append(q_HHbbWW_c2.Eta())
#                result["HHbbWW_c2M"].append(q_HHbbWW_c2.M())

            # Single b-tagging
            if len(bjets)>0:
#                [q_Hbb_b1,q_Wjj_b1] = recoHW_b1(bjets,event.cleanedJets)       # Single b-tagging
#                result["Hbb_b1Pt"].append(q_Hbb_b1.Pt())
#                result["Hbb_b1Eta"].append(q_Hbb_b1.Eta())
#                result["Hbb_b1M"].append(q_Hbb_b1.M())
#                result["Wjj_b1Pt"].append(q_Wjj_b1.Pt())
#                result["Wjj_b1Eta"].append(q_Wjj_b1.Eta())
#                result["Wjj_b1M"].append(q_Wjj_b1.M())
##                if abs(q_Hbb.M()-125.6)>20: # check invariant mass within 16% error
##                    print "Warning: Hbb reco: abs(q_Hbb.M()-125.6)>20"
#                if hasLepton: # HWW_b1
#                    q_HWW_b1 = q_Wjj_b1 + q_Wlnu1
#                    result["HWW_b1Pt"].append(q_HWW_b1.Pt())
#                    result["HWW_b1Eta"].append(q_HWW_b1.Eta())
#                    result["HWW_b1M"].append(q_HWW_b1.M())
#                    q_HHbbWW_b1 = q_Hbb_b1 + q_HWW_b1
#                    result["HHbbWW_b1Pt"].append(q_HHbbWW_b1.Pt())
#                    result["HHbbWW_b1Eta"].append(q_HHbbWW_b1.Eta())
#                    result["HHbbWW_b1M"].append(q_HHbbWW_b1.M())

                # Double b-tagging
                if len(bjets)>1:
                    [q_Hbb_b2,q_Wjj_b2] = recoHW_b2(bjets,event.cleanedJets) # Double b-tagging
                    result["Hbb_b2Pt"].append(q_Hbb_b2.Pt())
                    result["Hbb_b2Eta"].append(q_Hbb_b2.Eta())
                    result["Hbb_b2M"].append(q_Hbb_b2.M())
                    result["Wjj_b2Pt"].append(q_Wjj_b2.Pt())
                    result["Wjj_b2Eta"].append(q_Wjj_b2.Eta())
                    result["Wjj_b2M"].append(q_Wjj_b2.M())
                    if hasLepton: # HWW2
                        q_HWW_b2 = q_Wjj_b2 + q_Wlnu1
                        result["HWW_b2Pt"].append(q_HWW_b2.Pt())
                        result["HWW_b2Eta"].append(q_HWW_b2.Eta())
                        result["HWW_b2M"].append(q_HWW_b2.M())
                        q_HHbbWW_b2 = q_Hbb_b2 + q_HWW_b2
                        result["HHbbWW_b2Pt"].append(q_HHbbWW_b2.Pt())
                        result["HHbbWW_b2Eta"].append(q_HHbbWW_b2.Eta())
                        result["HHbbWW_b2M"].append(q_HHbbWW_b2.M())
    
        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], recoControlPlots())


