from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
from ROOT import TTree, TBranch
from itertools import combinations # to make jets combinations
from copy import copy
from fold import fold
from math import sqrt, cos, pi
#from reconstruct import max_b2b
from reconstruct import recoNeutrino, recoWlnu2Mt

# variables for in tree
tree_vars = [ "Njets20","Nbjets30",
              "jet1Pt","jet2Pt",
              "bjet1Pt","bjet2Pt",
              "Pt_bb","Pt_bl","Pt_j1l",
              "Pt_b1lnu", "Pt_b2lnu",
              "Pt_jjl", "Pt_jjb1", "Pt_jjb2",
              "leptonPt","MET",
              "DeltaR_j1l","DeltaR_j2l",
              "DeltaR_b1l","DeltaR_b2l",
              "DeltaR_bb1","DeltaR_jj",
              "DeltaR_jjl","DeltaR_jjb",
              "DeltaPhi_j1lbb",
              "DeltaPhi_lMET","DeltaPhi_jjlnu",
              "M_bb_closest", "M_jjlnu",
              "M_jjb1", "M_jjb2",
              "M_b1lnu", "M_b2lnu",
              "M_bl", "M_jjl",
              "M_jj", "M_j1l",
              "MT_lnu","MT_jjlnu" ]

# Requirements:
# event.muons
# event.electrons

class CleanUpControlPlots(BaseControlPlots):
    """A class to create control plots for leptons"""

    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="cleanup", dataset=dataset, mode=mode)

    def beginJob(self):
      
        # declare tree and branches
        self.addTree("cleanup","Variables for MVA")
        for var in tree_vars:
            self.addBranch("cleanup",var)

        self.add("Njets20","jets multiplicity (Pt > 20 GeV)",15,0,15)
        self.add("Njets30","jets multiplicity (Pt > 30 GeV)",15,0,15)
        self.add("Nbjets30","bjets multiplicity (Pt > 30 GeV)",5,0,5)
        self.add("Nbjets30_cut_PUPPI","bjets multiplicity (Pt > 30 GeV)",5,0,5)
        self.add("Nbjets30_cut_all","bjets multiplicity (Pt > 30 GeV)",5,0,5)
        
        self.add("jet1Pt","leading jet Pt",100,0,250)
        self.add("jet2Pt","second leading jet Pt",100,0,250)
        self.add("bjet1Pt","leading b-jet Pt",100,0,250)
        self.add("bjet2Pt","second leading b-jet Pt",100,0,250)
        self.add("Pt_bb","closest bjets pair Pt",100,0,500)
        self.add("Pt_bl","closest bjet-lepton Pt",100,0,500)
        self.add("Pt_b1lnu","second closest bjet-lepton-neutrino Pt",100,0,500)
        self.add("Pt_b2lnu","closest bjet-lepton-neutrino Pt",100,0,500)
        self.add("Pt_j1l","closest jet-lepton Pt",100,0,500)
        self.add("Pt_jjl","leading jets-lepton Pt",100,0,500)
        self.add("Pt_jjb1","leading jets-bjet Pt",100,0,500)
        self.add("Pt_jjb2","leading jets-bjet Pt",100,0,500)
        self.add("Eta_bb","closest bjet pair Eta",100,0,500)
        self.add("leptonPt","lepton Pt",100,0,250)
        self.add("MET","MET",100,0,300)

        self.add("M_jj","leading jet-jet Mass",100,0,300)
        self.add("M_jjb1","hadronic top reco Mass",100,0,700)
        self.add("M_jjb2","hadronic top reco Mass",100,0,700)
        self.add2D("M_jjb_2D","M_jjb1 vs. M_jjb2",100,0,700,100,0,700)
        self.add2D("M_jj_NPU","NPU vs. M_jj",80,0,300,80,80,200)
        

        self.add("M_jjl","leading jets-lepton Mass",100,0,450)
        self.add("M_jjlnu","leading jets-lepton-MET Mass",100,0,800)
        self.add("M_j1l","closest jet-lepton Mass",100,0,450)
        self.add("M_bb_leading","leading bjet-bjet Mass",100,0,300)
        self.add("M_bb_closest","closest bjet-bjet Mass",100,0,300)
        self.add("M_bb_farthest","farthest bjet-bjet Mass",100,0,300)
        self.add("M_bl","closest bjet-lepton Mass",100,0,300)
        self.add("MT_lnu","Wlnu Mt",100,0,200)
        self.add("MT_jjlnu","HWW Mt",100,0,300)
        self.add("M_b1lnu","leptonic top reco Mass",100,0,500)
        self.add("M_b2lnu","leptonic top reco Mass",100,0,500)
        self.add2D("M_blnu_2D","M_b1lnu vs. M_b2lnu",100,0,500,100,0,500)
        
        self.add("DeltaR_jj","leading jet-jet DeltaR",100,0,4.5)
        self.add("DeltaR_j1l","closest jet-lepton DeltaR",100,0,4)
        self.add("DeltaR_j2l","2nd closest jet-lepton DeltaR",100,0,4)
        self.add("DeltaR_jjl","leading jets-lepton DeltaR",100,0,4.5)
        self.add("DeltaR_jjb","leading jets-bjet DeltaR",100,0,4.5)
        self.add("DeltaR_j1lbb","closest jet-lepton-bjets DeltaR",100,0,4.5)
        self.add("DeltaR_jjlbb","leading jets-lepton-bjets DeltaR",100,0,4.5)
        self.add("DeltaR_jjbbl","leading jets-bjet-bjet-lepton DeltaR",100,0,4.5)
        self.add("DeltaR_bb1","closest bjet-bjet pair DeltaR",100,0,4)
        self.add("DeltaR_b1l","farthest bjet-lepton DeltaR",100,0,4)
        self.add("DeltaR_b2l","2nd farthest bjet-lepton DeltaR",100,0,4)

        self.add("DeltaPhi_jj","leading jet-jet DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j1l","closest jet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j2l","2nd closest jet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjl","leading jets-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjb","leading jets-bjet DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j1lbb","closest jet-lepton-bjets DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjlbb","leading jets-lepton-bjets DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjbbl","leading jets-bjet-bjet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_bb1","closest bjet-bjet pair DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_b1l","farthest bjet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_b2l","2nd farthest bjet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_lMET","lepton-MET DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjlnu","jets-lepton-MET DeltaPhi",100,0,3.5)

        self.add2D("DeltaEtaDeltaPhi_jj","leading jet-jet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j1l","closest jet-lepton combination DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j2l","2nd closest jet-lepton combination DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j3l","3rd closest jet-lepton combination DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjl","leading jets-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjb","leading jets-bjet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j1lbb","closest jet-lepton-bjets DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjlbb","leading jets-lepton-bjets DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjbbl","leading jets-bjet-bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_bb1","closest bjet-bjet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b1l","farthest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b2l","2nd farthest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)

#         self.add2D("NVerticesNJets","all jet multiplicity vs. number vertices",20,100,190,15,0,15)
#         self.add2D("NVerticesNPUPPIJets","PUPPI jet multiplicity vs. number vertices",20,100,190,15,0,15)



    # get information
    def process(self, event):
    
        result = { }
        
        jets = event.cleanedJets20[:] # remove closest b-jets pair down below
        alljets = [ j for j in event.jets if j.PT > 20 and abs(j.Eta) < 2.5 ]
        bjets = event.bjets30[:]
        result["Njets20"] = len(event.cleanedJets20)
        result["Njets30"] = len(event.cleanedJets30)
        result["Nbjets30"] = len(event.bjets30)
        
        if len(jets) > 3 and len(event.leadingLeptons) == 1 and event.met[0].MET > 20: 
            result["Nbjets30_cut_PUPPI"] = len(event.bjets30) 
            result["Nbjets30_cut_all"] = len([ j for j in alljets if j.BTag and j.PT > 30 ])
            
        NPU = event.npu[0]
#         result["NVerticesNJets"] = [[ NPU.HT, len(alljets) ]]
#         result["NVerticesNPUPPIJets"] = [[ NPU.HT, len(jets) ]]

        lepton = None
        p_neutrino = None
        MET = event.met[0]
        if len(event.leadingLeptons):
            lepton = event.leadingLeptons[0]
            p_neutrino = recoNeutrino(lepton.TLV,MET)

        # bjet - bjet
        bl = [ ]
        p_bl = None
        if lepton and bjets:
            bl = sorted( bjets, key=lambda j: TLV.DeltaR(j.TLV,lepton.TLV), reverse=True ) # farthest->closest
            DeltaPhi = fold(abs(lepton.Phi - bl[0].Phi))
            DeltaEta = abs(lepton.Eta - bl[0].Eta)
            p_bl = lepton.TLV+bl[-1].TLV
            result["M_bl"] = p_bl.M() # closest b-jet with lepton
            result["Pt_bl"] = p_bl.Pt()
            result["DeltaR_b1l"] = TLV.DeltaR(lepton.TLV,bl[0].TLV)
            result["DeltaPhi_b1l"] = DeltaPhi
            result["DeltaEtaDeltaPhi_b1l"] = [[ DeltaEta, DeltaPhi ]]
            if len(bl)>1:
                DeltaPhi = fold(abs(lepton.Phi - bl[1].Phi))
                DeltaEta = abs(lepton.Eta - bl[1].Eta)
                result["M_bb_farthest"] = (bl[0].TLV+bl[1].TLV).M()
                result["DeltaR_b2l"] = TLV.DeltaR(lepton.TLV,bl[1].TLV)
                result["DeltaPhi_b2l"] = DeltaPhi
                result["DeltaEtaDeltaPhi_b2l"] = [[ DeltaEta, DeltaPhi ]]
        
        # bjet comb
        DeltaR_bb_closest = 1000 # >> pi
        bjet_closest = [ ]
        p_bb1 = None
        for j1, j2 in combinations(bjets,2):
            p_bb = j1.TLV + j2.TLV
            DeltaR = TLV.DeltaR(j1.TLV, j2.TLV)

            if DeltaR < DeltaR_bb_closest:
                bjet_closest = [j1,j2]
                p_bb1 = p_bb
                result["M_bb_closest"] = p_bb.M()
                result["Pt_bb"] = p_bb.Pt()
                result["DeltaR_bb1"] = TLV.DeltaR(j1.TLV,j2.TLV)
                result["DeltaPhi_bb1"] = fold(abs(j1.Phi - j2.Phi))
                result["DeltaEtaDeltaPhi_bb1"] = [[ abs(j1.Eta - j2.Eta),
                                                    result["DeltaPhi_bb1"] ]]
                DeltaR_bb_closest = DeltaR
        
        if len(bjets)>1:
            result["M_bb_leading"] = (bjets[0].TLV+bjets[1].TLV).M()

        # leading non-b-jets
        for bjet in bjet_closest: # remove closest bjet pair from jet list
            jets.remove(bjet)
        if len(jets)>0:
            result["jet1Pt"] = jets[0].PT
            if len(jets)>1:
                result["jet2Pt"] = jets[1].PT
        
        # leading bjets
        if len(bjets)>1:
            result["bjet1Pt"] = bjet_closest[0].PT
            result["bjet2Pt"] = bjet_closest[1].PT
        elif len(bjets):
            result["bjet1Pt"] = bjets[0].PT


        # jet comb
        if len(jets)>1:
                                                       
            # 120 GeV upper mass limit
#             jets120 = [ js for js in combinations(jets[:4],2) if (js[0].TLV+js[1].TLV).M() < 120 ]
#             if len(jets120):
#                 jets = max( jets120, key = lambda js: (js[0].TLV+js[1].TLV).Pt())
                
            p_jj = jets[0].TLV + jets[1].TLV
            result["M_jj"] = p_jj.M()
            result["DeltaR_jj"] = TLV.DeltaR(jets[0].TLV, jets[1].TLV)
            result["DeltaPhi_jj"] = fold(abs(jets[0].Phi - jets[1].Phi))
            result["DeltaEtaDeltaPhi_jj"] = [[ abs(jets[0].Eta - jets[1].Eta),
                                                       result["DeltaPhi_jj"] ]]
            result["M_jj_NPU"] = [[ p_jj.M(), NPU.HT ]]
                            
            # jjl
            if lepton:
                p_jjl = p_jj + lepton.TLV
                result["M_jjl"] = p_jjl.M()
                result["Pt_jjl"] = p_jjl.Pt()
                result["M_jjlnu"] = (p_jj + lepton.TLV + p_neutrino).M()
                result["DeltaR_jjl"] = TLV.DeltaR(p_jj,lepton.TLV)
                result["DeltaPhi_jjl"] = fold(abs(p_jj.Phi()-lepton.Phi))
                result["DeltaEtaDeltaPhi_jjl"] = [[ abs(p_jj.Eta() - lepton.Eta),
                                                            result["DeltaPhi_jjl"] ]]
                result["DeltaPhi_jjlnu"] = fold(abs(p_jjl.Phi()-MET.Phi))
                result["MT_jjlnu"] = sqrt(2 * MET.MET * p_jjl.Pt() * (1-cos( p_jjl.Phi() - MET.Phi)) )
                if len(bl)>1:
                    p_blnu = bl[-2].TLV + lepton.TLV + p_neutrino
                    p_b2lnu = bl[-1].TLV + lepton.TLV + p_neutrino
                    result["M_b1lnu"] = p_blnu.M()
                    result["M_b2lnu"] = p_b2lnu.M() # take bjet closest
                    result["M_blnu_2D"] = [[ result["M_b1lnu"], result["M_b2lnu"] ]]
                    result["Pt_b1lnu"] = p_blnu.Pt()
                    result["Pt_b2lnu"] = p_b2lnu.Pt()
                    if len(event.cleanedJets20)>3: # take bjet second closest to lepton
                        jets_tt = event.cleanedJets20[:]
                        jets_tt.remove(bl[-1])
                        jets_tt.remove(bl[-2])
                                                                               
                        # 120 GeV upper mass limit
#                         jets120 = [ js for js in combinations(jets_tt[:4],2) if (js[0].TLV+js[1].TLV).M() < 120 ]
#                         if len(jets120):
#                             jets_tt = max( jets120, key = lambda js: (js[0].TLV+js[1].TLV).Pt())
                        
                        p_jj = jets_tt[0].TLV + jets_tt[1].TLV
                        p_jjb = p_jj + bl[-2].TLV
                        p_jjb2 = p_jj + bl[-1].TLV
                        result["M_jjl"] = p_jjl.M()
                        result["M_jjb1"] = p_jjb.M()
                        result["M_jjb2"] = p_jjb2.M()
                        result["M_jjb_2D"] = [[ result["M_jjb1"], result["M_jjb2"] ]]
                        result["Pt_jjb1"] = p_jjb.Pt()
                        result["Pt_jjb2"] = p_jjb2.Pt()
                        result["DeltaR_jjb"] = TLV.DeltaR(p_jj,bl[-2].TLV)
                        result["DeltaPhi_jjb"] = fold(abs(p_jj.Phi()-bl[-2].Phi))
                        result["DeltaEtaDeltaPhi_jjb"] = [[ abs(p_jj.Eta() - bl[-2].Eta),
                                                                    result["DeltaPhi_jjb"] ]]
                        result["DeltaR_jjlbb"] = TLV.DeltaR(p_jjl,p_bb1)
                        result["DeltaPhi_jjlbb"] = fold(abs(p_jjl.Phi()-p_bb1.Phi()))
                        result["DeltaEtaDeltaPhi_jjlbb"] = [[ abs(p_jjl.Eta() - p_bb1.Eta()),
                                                              result["DeltaPhi_jjlbb"] ]]
                        result["DeltaR_jjbbl"] = TLV.DeltaR(p_jjb,p_bl)
                        result["DeltaPhi_jjbbl"] = fold(abs(p_jjb.Phi()-p_bl.Phi()))
                        result["DeltaEtaDeltaPhi_jjbbl"] = [[ abs(p_jjb.Eta() - p_bl.Eta()),
                                                              result["DeltaPhi_jjbbl"] ]]
        
        
        if lepton:
            
            # MET - lepton
            result["leptonPt"] = lepton.PT
            result["MET"] = MET.MET
            result["DeltaPhi_lMET"] = abs(MET.Phi-lepton.Phi)
            result["MT_lnu"] = recoWlnu2Mt(lepton,MET)
        
            # jet i - lepton
            ji = sorted(jets, key=lambda j: TLV.DeltaR(j.TLV,lepton.TLV))[:3] # closest jets
            if len(ji)>0 and p_bb1:
                p_j1l = lepton.TLV+ji[0].TLV
                result["M_j1l"] = p_j1l.M()
                result["Pt_j1l"] = p_j1l.Pt()
                result["DeltaR_j1l"] = TLV.DeltaR(lepton.TLV,ji[0].TLV)
                result["DeltaPhi_j1l"] = fold(abs(lepton.Phi - ji[0].Phi))
                result["DeltaEtaDeltaPhi_j1l"] = [[ abs(lepton.Eta - ji[0].Eta),
                                                    result["DeltaPhi_j1l"] ]]
                result["DeltaR_j1lbb"] = TLV.DeltaR(p_j1l,p_bb1)
                result["DeltaPhi_j1lbb"] = fold(abs(p_j1l.Phi()-p_bb1.Phi()))
                result["DeltaEtaDeltaPhi_j1lbb"] = [[ abs(p_j1l.Eta() - p_bb1.Eta()),
                                                      result["DeltaPhi_j1lbb"] ]]
                
                if len(ji)>1:
#                    result["M_j2l"] = (lepton.TLV+ji[1].TLV).M()
                    result["DeltaR_j2l"] = TLV.DeltaR(lepton.TLV,ji[1].TLV)
                    result["DeltaPhi_j2l"] = fold(abs(lepton.Phi - ji[1].Phi))
                    result["DeltaEtaDeltaPhi_j2l"] = [[ abs(lepton.Eta - ji[1].Eta),
                                                        result["DeltaPhi_j2l"] ]]
                    if len(ji)>2:
                        result["DeltaEtaDeltaPhi_j3l"] = [[ abs(lepton.Eta - ji[2].Eta),
                                                            fold(abs(lepton.Phi - ji[2].Phi)) ]]
        
        
        # respect the order of branches when adding variables
#        result["cleanup"] = [ result[var] for var in result if var in tree_vars ]
        result["cleanup"] = [ ]
        for var in tree_vars:
            if var in result:
                result["cleanup"].append(result[var])
            else: # if one variable does not exist for this event, no tree
                del result["cleanup"]
                break

        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], CleanUpControlPlots())

