from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector
from reconstruct import *
from math import sqrt, cos

HM_max = 125 + 15
HM_min = 125 - 30
WM_max = 80 + 30
WM_offshell_max = 60

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
                    self.add("HWW"+algs[i]+"Mc","HWW Mc reco "+alg_titles[i],100,0,800)
                elif particle=="Hbb":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,300)
                    self.add(particle+algs[i]+"M_window1",particle+" Mass reco "+alg_titles[i]+" window",100,85,200)
                    self.add(particle+algs[i]+"M_window2",particle+" Mass reco "+alg_titles[i]+" window",100,85,200)
                elif particle=="HHbbWW":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,1500)
                elif particle=="Wjj":
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,300)
                    self.add2D("WWM"+algs[i],"Wjj Mass vs. Wlnu Mass",100,0,200,100,0,200)
                    self.add2D("WWMt"+algs[i],"Wjj Mass vs. Wlnu Mt",100,0,200,100,0,300)
                else:
                    self.add(particle+algs[i]+"M",particle+" Mass reco "+alg_titles[i],100,0,300)

#        self.add("JetCombs_c1M","combined jets Mass (combination alg.)",100,0,1000)
#        self.add("JetCombs_c2M","combined jets Mass (combination alg.2)",100,0,1000)



    def process(self, event):
    
        result = { }

        # __Wlnu__
        WlnuMt = 0
        lepton = event.leadingLepton
        leptonPID = event.leadingLeptonPID
        if lepton:
            q_Wlnu1 = recoWlnu1(leptonPID,lepton,event.met[0])
            result["Wlnu1Pt"] = q_Wlnu1.Pt()
            result["Wlnu1Eta"] = q_Wlnu1.Eta()
            result["Wlnu1M"] = q_Wlnu1.M()
            q_Wlnu2 = recoWlnu2(leptonPID,lepton,event.met[0])
            result["Wlnu2Pt"] = q_Wlnu2.Pt()
            result["Wlnu2Eta"] = q_Wlnu2.Eta()
            result["Wlnu2M"] = q_Wlnu2.M()
            WlnuMt = recoWlnu2Mt(lepton,event.met[0])
            result["WlnuMt"] = WlnuMt
#        elif hasElectron:
#            q_Wlnu1 = recoWlnu1(11,event.electrons[0],event.met[0])
#            result["Wlnu1Pt"] = q_Wlnu1.Pt()
#            result["Wlnu1Eta"] = q_Wlnu1.Eta()
#            result["Wlnu1M"] = q_Wlnu1.M()
#            q_Wlnu2 = recoWlnu2(11,event.electrons[0],event.met[0])
#            result["Wlnu2Pt"] = q_Wlnu2.Pt()
#            result["Wlnu2Eta"] = q_Wlnu2.Eta()
#            result["Wlnu2M"] = q_Wlnu2.M()
#            WlnuMt = recoWlnu2Mt(event.electrons[0],event.met[0])
#            result["WlnuMt"] = WlnuMt

    
    
        # __Wjj,_Hbb___
        bjets = event.bjets30
        jets = event.cleanedJets15[:10]
        if len(jets)>3:
        
#            # Combination alg.
#            [q_Hbb_c1, q_Wjj1_c1, M_jetComb] = recoHW_c1(jets)      # Combination alg.
#            result["Hbb_c1Pt"] = q_Hbb_c1.Pt()
#            result["Hbb_c1Eta"] = q_Hbb_c1.Eta()
#            result["Hbb_c1M"] = q_Hbb_c1.M()
#            result["Wjj_c1Pt"] = q_Wjj_c1.Pt()
#            result["Wjj_c1Eta"] = q_Wjj_c1.Eta()
#            result["Wjj_c1M"] = q_Wjj_c1.M()
#            result["JetCombs_c1M"] = JetCombs_c1M
#            if hasLepton: # HWWc
#                q_HWW_c1 = q_Wjj_c1 + q_Wlnu1
#                result["HWW_c1Pt"] = q_HWW_c1.Pt()
#                result["HWW_c1Eta"] = q_HWW_c1.Eta()
#                result["HWW_c1M"] = q_HWW_c1.M()
#                q_HHbbWW_c1 = q_Hbb_c1 + q_HWW_c1
#                result["HHbbWW_c1Pt"] = q_HHbbWW_c1.Pt()
#                result["HHbbWW_c1Eta"] = q_HHbbWW_c1.Eta()
#                result["HHbbWW_c1M"] = q_HHbbWW_c1.M()
#
#            # Combination alg. 2
#            [q_Hbb_c2, q_Wjj_c2, JetCombs_c2M] = recoHW_c2(jets)    # Combination alg. 2
#            result["Hbb_c2Pt"] = q_Hbb_c2.Pt()
#            result["Hbb_c2Eta"] = q_Hbb_c2.Eta()
#            result["Hbb_c2M"] = q_Hbb_c2.M()
#            result["Wjj_c2Pt"] = q_Wjj_c2.Pt()
#            result["Wjj_c2Eta"] = q_Wjj_c2.Eta()
#            result["Wjj_c2M"] = q_Wjj_c2.M()
#            result["JetCombs_c2M"] = JetCombs_c2M
#            if hasLepton: # HWW_c2
#                q_HWW_c2 = q_Wjj_c2 + q_Wlnu1
#                result["HWW_c2Pt"] = q_HWW_c2.Pt()
#                result["HWW_c2Eta"] = q_HWW_c2.Eta()
#                result["HWW_c2M"] = q_HWW_c2.M()
#                q_HHbbWW_c2 = q_Hbb_c2 + q_HWW_c2
#                result["HHbbWW_c2Pt"] = q_HHbbWW_c2.Pt()
#                result["HHbbWW_c2Eta"] = q_HHbbWW_c2.Eta()
#                result["HHbbWW_c2M"] = q_HHbbWW_c2.M()

            # Single b-tagging
            if len(bjets)>0 and lepton:
                
                [q_Hbb_b1,q_Wjj_b1] = recoHW_b1(bjets,jets)       # Single b-tagging
                q_HWW_b1 = q_Wjj_b1 + q_Wlnu1
                q_HHbbWW_b1 = q_Hbb_b1 + q_HWW_b1
                result["Hbb_b1Pt" ] = q_Hbb_b1.Pt()
                result["Hbb_b1Eta"] = q_Hbb_b1.Eta()
                result["Hbb_b1M"  ] = q_Hbb_b1.M()
                result["Wjj_b1Pt" ] = q_Wjj_b1.Pt()
                result["Wjj_b1Eta"] = q_Wjj_b1.Eta()
                result["Wjj_b1M"  ] = q_Wjj_b1.M()
                result["HWW_b1Pt" ] = q_HWW_b1.Pt()
                result["HWW_b1Eta"] = q_HWW_b1.Eta()
                result["HWW_b1M"  ] = q_HWW_b1.M()
                result["HHbbWW_b1Pt" ] = q_HHbbWW_b1.Pt()
                result["HHbbWW_b1Eta"] = q_HHbbWW_b1.Eta()
                result["HHbbWW_b1M"  ] = q_HHbbWW_b1.M()
                if HM_min < q_Hbb_b1.M() < HM_max: #and HM_min < q_HWW_b1.M() < HM_max:
                    result["Hbb_b1M_window1"] = q_Hbb_b1.M()
                    if q_Wjj_b1.M() < WM_offshell_max:
                        result["Hbb_b1M_window2"] = q_Hbb_b1.M()
                result["WWM_b1"] = [[ q_Wjj_b1.M(), q_Wlnu1.M() ]]
                result["WWMt_b1"] = [[ q_Wjj_b1.M(), WlnuMt ]]
                result["HWW_b2Mc"] = recoHWWMC1(q_Wjj_b1,leptonPID,lepton,event.met[0])

                # Double b-tagging
                if len(bjets)>1 and lepton:
                    [q_Hbb_b2,q_Wjj_b2] = recoHW_b2(bjets,jets) # Double b-tagging
                    result["Hbb_b2Pt" ] = q_Hbb_b2.Pt()
                    result["Hbb_b2Eta"] = q_Hbb_b2.Eta()
                    result["Hbb_b2M"  ] = q_Hbb_b2.M()
                    result["Wjj_b2Pt" ] = q_Wjj_b2.Pt()
                    result["Wjj_b2Eta"] = q_Wjj_b2.Eta()
                    result["Wjj_b2M"  ] = q_Wjj_b2.M()
                    q_HWW_b2 = q_Wjj_b2 + q_Wlnu1
                    result["HWW_b2Pt" ] = q_HWW_b2.Pt()
                    result["HWW_b2Eta"] = q_HWW_b2.Eta()
                    result["HWW_b2M"  ] = q_HWW_b2.M()
                    q_HHbbWW_b2 = q_Hbb_b2 + q_HWW_b2
                    result["HHbbWW_b2Pt" ] = q_HHbbWW_b2.Pt()
                    result["HHbbWW_b2Eta"] = q_HHbbWW_b2.Eta()
                    result["HHbbWW_b2M"  ] = q_HHbbWW_b2.M()
                    if HM_min < q_Hbb_b2.M() < HM_max: #and HM_min < q_HWW_b2.M() < HM_max:
                        result["Hbb_b2M_window1"] = q_Hbb_b2.M()
                        if q_Wjj_b2.M() < WM_offshell_max:
                            result["Hbb_b2M_window2"] = q_Hbb_b2.M()
                    result["WWM_b2"] = [[ q_Wjj_b2.M(), q_Wlnu1.M() ]]
                    result["WWM_b2"] = [[ q_Wjj_b2.M(), WlnuMt ]]
                    result["HWW_b2Mc"] = recoHWWMC1(q_Wjj_b2,leptonPID,lepton,event.met[0])
                    
                    # Double b-tagging 2
                    [q_Hbb_b3,q_Wjj_b3] = recoHW_b3(bjets,jets) # Double b-tagging 2
                    q_HWW_b3 = q_Wjj_b3 + q_Wlnu1
                    q_HHbbWW_b3 = q_Hbb_b3 + q_HWW_b3
                    result["Hbb_b3Pt" ] = q_Hbb_b3.Pt()
                    result["Hbb_b3Eta"] = q_Hbb_b3.Eta()
                    result["Hbb_b3M"  ] = q_Hbb_b3.M()
                    result["Wjj_b3Pt" ] = q_Wjj_b3.Pt()
                    result["Wjj_b3Eta"] = q_Wjj_b3.Eta()
                    result["Wjj_b3M"  ] = q_Wjj_b3.M()
                    result["HWW_b3Pt" ] = q_HWW_b3.Pt()
                    result["HWW_b3Eta"] = q_HWW_b3.Eta()
                    result["HWW_b3M"  ] = q_HWW_b3.M()
                    result["HHbbWW_b3Pt" ] = q_HHbbWW_b3.Pt()
                    result["HHbbWW_b3Eta"] = q_HHbbWW_b3.Eta()
                    result["HHbbWW_b3M"  ] = q_HHbbWW_b3.M()
                    if HM_min < q_Hbb_b3.M() < HM_max: #and HM_min < q_HWW_b3.M() < HM_max:
                        result["Hbb_b3M_window1"] = q_Hbb_b3.M()
                        if q_Wjj_b3.M() < WM_offshell_max:
                            result["Hbb_b3M_window2"] = q_Hbb_b3.M()
                    result["WWM_b3"] = [[ q_Wjj_b3.M(), q_Wlnu1.M() ]]
                    result["WWM_b3"] = [[ q_Wjj_b3.M(), WlnuMt ]]
                    result["HWW_b3Mc"] = recoHWWMC1(q_Wjj_b3,leptonPID,lepton,event.met[0])
                    
                    # Double b-tagging 3
                    [q_Hbb_b4,q_Wjj_b4] = recoHW_b4(bjets,jets) # Double b-tagging 2
                    q_HWW_b4 = q_Wjj_b4 + q_Wlnu1
                    q_HHbbWW_b4 = q_Hbb_b4 + q_HWW_b4
                    result["Hbb_b4Pt" ] = q_Hbb_b4.Pt()
                    result["Hbb_b4Eta"] = q_Hbb_b4.Eta()
                    result["Hbb_b4M"  ] = q_Hbb_b4.M()
                    result["Wjj_b4Pt" ] = q_Wjj_b4.Pt()
                    result["Wjj_b4Eta"] = q_Wjj_b4.Eta()
                    result["Wjj_b4M"  ] = q_Wjj_b4.M()
                    result["HWW_b4Pt" ] = q_HWW_b4.Pt()
                    result["HWW_b4Eta"] = q_HWW_b4.Eta()
                    result["HWW_b4M"  ] = q_HWW_b4.M()
                    result["HHbbWW_b4Pt" ] = q_HHbbWW_b4.Pt()
                    result["HHbbWW_b4Eta"] = q_HHbbWW_b4.Eta()
                    result["HHbbWW_b4M"  ] = q_HHbbWW_b4.M()
                    if HM_min < q_Hbb_b4.M() < HM_max: #and HM_min < q_HWW_b4.M() < HM_max:
                        result["Hbb_b4M_window1"] = q_Hbb_b4.M()
                        if q_Wjj_b4.M() < WM_offshell_max:
                            result["Hbb_b4M_window2"] = q_Hbb_b4.M()
                    result["WWM_b4"] = [[ q_Wjj_b4.M(), q_Wlnu1.M() ]]
                    result["WWM_b4"] = [[ q_Wjj_b4.M(), WlnuMt ]]
                    result["HWW_b4Mc"] = recoHWWMC1(q_Wjj_b4,leptonPID,lepton,event.met[0])
    
        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], recoControlPlots())


