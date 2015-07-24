from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector
from reconstruct import *
from math import sqrt, cos

HM_max = 125 + 50
HM_min = 125 - 50
WM_max = 80 + 30

particleSelection = ["Wjj","Hbb","HWW","HHbbWW"]
vars = ["Pt","Eta","M"]
algs = ["_b1","_b2","_b3","_b4"]#,"_c1","_c2"]
alg_titles = ["(one b-tag)","(two b-tag)","(two b-tag with MW<100 GeV)","(two b-tag with windows)"]#,"(no b-tag W on-shell)","(no b-tag)"]


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
        
        self.add("WlnuMt","Wlnu reco Mt",100,0,300)

        for particle in particleSelection:
            for i in range(len(algs)):
                self.add(particle+algs[i]+"Pt",particle+" Pt reco "+alg_titles[i],100,0,600)
                self.add(particle+algs[i]+"Eta",particle+" Eta reco "+alg_titles[i],100,-5,5)
                if particle=="HWW":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,800)
                elif particle=="Hbb":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,300)
                    self.add(particle+algs[i]+"M_window1",particle+" Mass reco "+alg_titles[i]+" window",100,85,200)
                    self.add(particle+algs[i]+"M_window2",particle+" Mass reco "+alg_titles[i]+" window",100,85,200)
                elif particle=="HHbbWW":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,1500)
                else:
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,300)
    
#        self.add("JetCombs_c1M","combined jets Mass (combination alg.)",100,0,1000)
#        self.add("JetCombs_c2M","combined jets Mass (combination alg.2)",100,0,1000)



    def process(self, event):
    
        result = { }
        
        hasMuon = (event.muons.GetEntries()>0)
        hasElectron = (event.electrons.GetEntries()>0)
        hasLepton = hasMuon or hasElectron
        
        # choose which lepton has to be reconstructed
        if hasMuon:
            if hasElectron:
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
            result["WlnuMt"].append(recoWlnuMt(event.muons[0],event.met[0]))
#            sqrt(2*event.met[0].MET*event.muons[0].PT*(1-cos( event.muons[0].Phi-event.met[0].Phi) ))
        elif hasElectron:
            q_Wlnu1 = recoWlnu1(11,event.electrons[0],event.met[0])
            result["Wlnu1Pt"].append(q_Wlnu1.Pt())
            result["Wlnu1Eta"].append(q_Wlnu1.Eta())
            result["Wlnu1M"].append(q_Wlnu1.M())
            q_Wlnu2 = recoWlnu2(11,event.electrons[0],event.met[0])
            result["Wlnu2Pt"].append(q_Wlnu2.Pt())
            result["Wlnu2Eta"].append(q_Wlnu2.Eta())
            result["Wlnu2M"].append(q_Wlnu2.M())
            result["WlnuMt"].append(recoWlnuMt(event.electrons[0],event.met[0]))
        
    
    
        # __Wjj,_Hbb___
        for particle in particleSelection:
            for var in vars:
                for alg in algs:
                    result[particle+alg+var] = []
        bjets = event.bjets30
        jets = event.cleanedJets30
#        result["JetCombs_c1M"] = [ ]
#        result["JetCombs_c2M"] = [ ]
        if len(jets)>3:
        
#            # Combination alg.
#            [q_Hbb_c1, q_Wjj1_c1, M_jetComb] = recoHW_c1(jets)      # Combination alg.
#            result["Hbb_c1Pt"].append(q_Hbb_c1.Pt())
#            result["Hbb_c1Eta"].append(q_Hbb_c1.Eta())
#            result["Hbb_c1M"].append(q_Hbb_c1.M())
#            result["Wjj_c1Pt"].append(q_Wjj_c1.Pt())
#            result["Wjj_c1Eta"].append(q_Wjj_c1.Eta())
#            result["Wjj_c1M"].append(q_Wjj_c1.M())
#            result["JetCombs_c1M"].extend(JetCombs_c1M)
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
#            [q_Hbb_c2, q_Wjj_c2, JetCombs_c2M] = recoHW_c2(jets)    # Combination alg. 2
#            result["Hbb_c2Pt"].append(q_Hbb_c2.Pt())
#            result["Hbb_c2Eta"].append(q_Hbb_c2.Eta())
#            result["Hbb_c2M"].append(q_Hbb_c2.M())
#            result["Wjj_c2Pt"].append(q_Wjj_c2.Pt())
#            result["Wjj_c2Eta"].append(q_Wjj_c2.Eta())
#            result["Wjj_c2M"].append(q_Wjj_c2.M())
#            result["JetCombs_c2M"].extend(JetCombs_c2M)
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
                [q_Hbb_b1,q_Wjj_b1] = recoHW_b1(bjets,jets)       # Single b-tagging
                result["Hbb_b1Pt" ].append(q_Hbb_b1.Pt())
                result["Hbb_b1Eta"].append(q_Hbb_b1.Eta())
                result["Hbb_b1M"  ].append(q_Hbb_b1.M())
                result["Wjj_b1Pt" ].append(q_Wjj_b1.Pt())
                result["Wjj_b1Eta"].append(q_Wjj_b1.Eta())
                result["Wjj_b1M"  ].append(q_Wjj_b1.M())
                if hasLepton: # HWW_b1
                    q_HWW_b1 = q_Wjj_b1 + q_Wlnu1
                    result["HWW_b1Pt" ].append(q_HWW_b1.Pt())
                    result["HWW_b1Eta"].append(q_HWW_b1.Eta())
                    result["HWW_b1M"  ].append(q_HWW_b1.M())
                    q_HHbbWW_b1 = q_Hbb_b1 + q_HWW_b1
                    result["HHbbWW_b1Pt" ].append(q_HHbbWW_b1.Pt())
                    result["HHbbWW_b1Eta"].append(q_HHbbWW_b1.Eta())
                    result["HHbbWW_b1M"  ].append(q_HHbbWW_b1.M())
                    if HM_min < q_Hbb_b1.M() < HM_max and HM_min < q_HWW_b1.M() < HM_max:
                        result["Hbb_b1M_window1"] = q_Hbb_b1.M()
                        if q_Wlnu1.M() < WM_max and q_Wjj_b1.M() < WM_max:
                            result["Hbb_b1M_window2"] = q_Hbb_b1.M()

                # Double b-tagging
                if len(bjets)>1:
                    [q_Hbb_b2,q_Wjj_b2] = recoHW_b2(bjets,jets) # Double b-tagging
                    result["Hbb_b2Pt" ].append(q_Hbb_b2.Pt())
                    result["Hbb_b2Eta"].append(q_Hbb_b2.Eta())
                    result["Hbb_b2M"  ].append(q_Hbb_b2.M())
                    result["Wjj_b2Pt" ].append(q_Wjj_b2.Pt())
                    result["Wjj_b2Eta"].append(q_Wjj_b2.Eta())
                    result["Wjj_b2M"  ].append(q_Wjj_b2.M())
                    if hasLepton:
                        q_HWW_b2 = q_Wjj_b2 + q_Wlnu1
                        result["HWW_b2Pt" ].append(q_HWW_b2.Pt())
                        result["HWW_b2Eta"].append(q_HWW_b2.Eta())
                        result["HWW_b2M"  ].append(q_HWW_b2.M())
                        q_HHbbWW_b2 = q_Hbb_b2 + q_HWW_b2
                        result["HHbbWW_b2Pt" ].append(q_HHbbWW_b2.Pt())
                        result["HHbbWW_b2Eta"].append(q_HHbbWW_b2.Eta())
                        result["HHbbWW_b2M"  ].append(q_HHbbWW_b2.M())
                        if HM_min < q_Hbb_b2.M() < HM_max and HM_min < q_HWW_b2.M() < HM_max:
                            result["Hbb_b2M_window1"] = q_Hbb_b2.M()
                            if q_Wlnu1.M() < WM_max and q_Wjj_b2.M() < WM_max:
                                result["Hbb_b2M_window2"] = q_Hbb_b2.M()
                    
                    # Double b-tagging 2
                    [q_Hbb_b3,q_Wjj_b3] = recoHW_b3(bjets,jets) # Double b-tagging 2
                    result["Hbb_b3Pt" ].append(q_Hbb_b3.Pt())
                    result["Hbb_b3Eta"].append(q_Hbb_b3.Eta())
                    result["Hbb_b3M"  ].append(q_Hbb_b3.M())
                    result["Wjj_b3Pt" ].append(q_Wjj_b3.Pt())
                    result["Wjj_b3Eta"].append(q_Wjj_b3.Eta())
                    result["Wjj_b3M"  ].append(q_Wjj_b3.M())
                    if hasLepton:
                        q_HWW_b3 = q_Wjj_b3 + q_Wlnu1
                        result["HWW_b3Pt" ].append(q_HWW_b3.Pt())
                        result["HWW_b3Eta"].append(q_HWW_b3.Eta())
                        result["HWW_b3M"  ].append(q_HWW_b3.M())
                        q_HHbbWW_b3 = q_Hbb_b3 + q_HWW_b3
                        result["HHbbWW_b3Pt" ].append(q_HHbbWW_b3.Pt())
                        result["HHbbWW_b3Eta"].append(q_HHbbWW_b3.Eta())
                        result["HHbbWW_b3M"  ].append(q_HHbbWW_b3.M())
                        if HM_min < q_Hbb_b3.M() < HM_max and HM_min < q_HWW_b3.M() < HM_max:
                            result["Hbb_b3M_window1"] = q_Hbb_b3.M()
                            if q_Wlnu1.M() < WM_max and q_Wjj_b3.M() < WM_max:
                                result["Hbb_b3M_window2"] = q_Hbb_b3.M()
                    
                    # Double b-tagging 3
                    [q_Hbb_b4,q_Wjj_b4] = recoHW_b4(bjets,jets) # Double b-tagging 2
                    result["Hbb_b4Pt" ].append(q_Hbb_b4.Pt())
                    result["Hbb_b4Eta"].append(q_Hbb_b4.Eta())
                    result["Hbb_b4M"  ].append(q_Hbb_b4.M())
                    result["Wjj_b4Pt" ].append(q_Wjj_b4.Pt())
                    result["Wjj_b4Eta"].append(q_Wjj_b4.Eta())
                    result["Wjj_b4M"  ].append(q_Wjj_b4.M())
                    if hasLepton:
                        q_HWW_b4 = q_Wjj_b4 + q_Wlnu1
                        result["HWW_b4Pt" ].append(q_HWW_b4.Pt())
                        result["HWW_b4Eta"].append(q_HWW_b4.Eta())
                        result["HWW_b4M"  ].append(q_HWW_b4.M())
                        q_HHbbWW_b4 = q_Hbb_b4 + q_HWW_b4
                        result["HHbbWW_b4Pt" ].append(q_HHbbWW_b4.Pt())
                        result["HHbbWW_b4Eta"].append(q_HHbbWW_b4.Eta())
                        result["HHbbWW_b4M"  ].append(q_HHbbWW_b4.M())
                        if HM_min < q_Hbb_b4.M() < HM_max and HM_min < q_HWW_b4.M() < HM_max:
                            result["Hbb_b4M_window1"] = q_Hbb_b4.M()
                            if q_Wlnu1.M() < WM_max and q_Wjj_b4.M() < WM_max:
                                result["Hbb_b4M_window2"] = q_Hbb_b4.M()
    
        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], recoControlPlots())


