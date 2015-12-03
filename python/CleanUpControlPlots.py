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
              "leptonPt","MET",
              "DeltaR_j1l","DeltaR_j2l",
              "DeltaR_b1l","DeltaR_b2l",
              "DeltaR_bb1","DeltaR_jj",
              "DeltaR_jjl","DeltaR_jjb",
              "DeltaPhi_lMET","DeltaPhi_j1lbb",
              "M_bb_closest", "M_jjlnu",
              "M_jjb", "M_blnu",
              "M_bl", "M_j1l",
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
        self.add("Nbjets30","bjets multiplicity (Pt > 30 GeV)",10,0,10)
        self.add("jet1Pt","jet 1 Pt",100,0,250)
        self.add("jet2Pt","jet 2 Pt",100,0,250)
        self.add("bjet1Pt","bjet 1 Pt",100,0,250)
        self.add("bjet2Pt","bjet 2 Pt",100,0,250)
        self.add("Pt_bb","bjets Pt",100,0,500)
        self.add("Pt_bl","closest bjet-lepton Pt",100,0,500)
        self.add("Pt_j1l","closest jet-lepton Pt",100,0,500)
        self.add("leptonPt","lepton Pt",100,0,250)
        self.add("MET","MET",100,0,300)

        self.add("M_jj_all","jet-jet combinations Mass",100,0,300)
        self.add("M_jj_all_cut","jet-jet combinations (cut) Mass",100,0,300)
        self.add("M_jj","leading jet-jet Mass",100,0,300)
        self.add("M_jj_cut","leading jet-jet (cut) Mass",100,0,300)
#        self.add("M_jj_b2b","jet-jet b2b Mass",100,0,300)
#        self.add("M_jj_b2b_(cut)","jet-jet b2b Mass",100,0,300)
        self.add("M_jjb","hadronic top reco Mass",100,0,700)
        self.add("M_jjl_all","jets-lepton combinations Mass",100,0,450)
        self.add("M_jjl","leading jets-lepton Mass",100,0,450)
        self.add("M_jjlnu","leading jets-lepton-MET Mass",100,0,700)
        self.add("M_j1l","closest jet-lepton Mass",100,0,450)
#        self.add("M_j2l","2nd closest jet-lepton Mass",100,0,450)
        self.add("M_bb_leading","leading bjet-bjet Mass",100,0,300)
#        self.add("M_bb_leading_cut","leading bjet-bjet (cut) Mass",100,0,300)
        self.add("M_bb_closest","closest bjet-bjet Mass",100,0,300)
        self.add("M_bb_closest_cut","closest bjet-bjet (cut) Mass",100,0,300)
        self.add("M_bb_farthest","farthest bjet-bjet Mass",100,0,300)
        self.add("M_bb_cut","bjet-bjet (cut) Mass",100,0,300)
        self.add("M_bl","closest bjet-lepton Mass",100,0,300)
        self.add("MT_lnu","Wlnu Mt",100,0,300)
        self.add("MT_jjlnu","HWW Mt",100,0,300)
        self.add("M_blnu","leptonic top reco Mass",100,0,500)

#        self.add("DeltaPt_jl","lepton-bjet Mass",100,0,2)
#        self.add2D("DeltaRDeltaPt_jl","lepton-bjet DeltaPt vs. DeltaR",100,0,4.5,100,0,2)

        self.add("DeltaR_jj_all","jet-jet combinations DeltaR",100,0,4)
        self.add("DeltaR_jj","leading jet-jet DeltaR",100,0,4)
        self.add("DeltaR_j1l","closest jet-lepton DeltaR",100,0,4)
        self.add("DeltaR_j2l","2nd closest jet-lepton DeltaR",100,0,4)
        self.add("DeltaR_jjl_all","jets-lepton combinations DeltaR",100,0,5)
        self.add("DeltaR_jjl","leading jets-lepton DeltaR",100,0,4.5)
        self.add("DeltaR_jjb","leading jets-bjet DeltaR",100,0,4.5)
        self.add("DeltaR_j1lbb","closest jet-lepton-bjets DeltaR",100,0,4.5)
        self.add("DeltaR_jjlbb","leading jets-lepton-bjets DeltaR",100,0,4.5)
        self.add("DeltaR_bb1","closest bjet-bjet pair DeltaR",100,0,4)
        self.add("DeltaR_b1l","farthest bjet-lepton DeltaR",100,0,4)
        self.add("DeltaR_b2l","2nd farthest bjet-lepton DeltaR",100,0,4)
        self.add("DeltaR_b1l_i","farthest bjet-lepton DeltaR",100,0,4)
        self.add("DeltaR_b2l_i","2nd farthest bjet-lepton DeltaR",100,0,4)

        self.add("DeltaPhi_jj_all","jet-jet combinations DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jj","leading jet-jet DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j1l","closest jet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j2l","2nd closest jet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjl_all","jets-lepton combinations DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjl","leading jets-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjb","leading jets-bjet DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j1lbb","closest jet-lepton-bjets DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjlbb","leading jets-lepton-bjets DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_bb1","closest bjet-bjet pair DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_b1l","farthest bjet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_b2l","2nd farthest bjet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_lMET","lepton-MET DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjlnu","jets-lepton-MET DeltaPhi",100,0,3.5)

        self.add2D("DeltaEtaDeltaPhi_jj_all","jet-jet combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jj","leading jet-jet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j1l","closest jet-lepton combination DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j2l","2nd closest jet-lepton combination DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j3l","3rd closest jet-lepton combination DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjl_all","jets-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjl","leading jets-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjb","leading jets-bjet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j1lbb","closest jet-lepton-bjets DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjlbb","leading jets-lepton-bjets DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_bb1","closest bjet-bjet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b1l","farthest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b2l","2nd farthest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)



    # get information
    def process(self, event):
    
        result = { }
        
        result["M_jj_all"] = [ ]
        result["M_jj_all_cut"] = [ ]
        result["M_jjl_all"] = [ ]
        result["M_bb_cut"] = [ ]

        #result["DeltaPt_jl"] = event.DeltaPt_jl
        #result["DeltaRDeltaPt_jl"] = map(lambda R,Pt: [R,Pt], event.DeltaR_jl,event.DeltaPt_jl)

        result["DeltaR_jj_all"] = [ ]
        result["DeltaR_jjl_all"] = [ ]

        result["DeltaPhi_jj_all"] = [ ]
        result["DeltaPhi_jjl_all"] = [ ]

        result["DeltaEtaDeltaPhi_jj_all"] = [ ]
        result["DeltaEtaDeltaPhi_jjl_all"] = [ ]

        jets = event.cleanedJets20[:] # remove closest b-jets pair down below
        bjets = event.bjets30[:]
        result["Njets20"] = len(event.cleanedJets20)
        result["Njets30"] = len(event.cleanedJets30)
        result["Nbjets30"] = len(event.bjets30)

        lepton = None
        p_neutrino = None
        MET = event.met[0]
        if len(event.leadingLeptons):
            lepton = event.leadingLeptons[0]
            p_neutrino = recoNeutrino(lepton.TLV,MET)
#            lepton.TLV = TLV()
#            lepton.TLV.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
#        
#        for jet in event.cleanedJets20:
#            jet.TLV = TLV()
#            jet.TLV.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

        # bjet - bjet
        bl = [ ]
        if lepton and bjets:
            bl = sorted( bjets, key=lambda j: TLV.DeltaR(j.TLV,lepton.TLV), reverse=True ) # farthest->closest
            DeltaPhi = fold(abs(lepton.Phi - bl[0].Phi))
            DeltaEta = abs(lepton.Eta - bl[0].Eta)
            p_bl = lepton.TLV+bl[-1].TLV
            result["M_bl"] = p_bl.M() # closest b-jet with lepton
            result["Pt_bl"] = p_bl.Pt()
            result["DeltaR_b1l"] = TLV.DeltaR(lepton.TLV,bl[0].TLV)
            result["DeltaR_b1l_i"] = sqrt( (pi-DeltaPhi)*(pi-DeltaPhi) + DeltaEta*DeltaEta )
            result["DeltaPhi_b1l"] = DeltaPhi
            result["DeltaEtaDeltaPhi_b1l"] = [[ DeltaEta, DeltaPhi ]]
            if len(bl)>1:
                DeltaPhi = fold(abs(lepton.Phi - bl[1].Phi))
                DeltaEta = abs(lepton.Eta - bl[1].Eta)
                result["M_bb_farthest"] = (bl[0].TLV+bl[1].TLV).M()
                result["DeltaR_b2l"] = TLV.DeltaR(lepton.TLV,bl[1].TLV)
                result["DeltaR_b2l_i"] = sqrt( (pi-DeltaPhi)*(pi-DeltaPhi) + DeltaEta*DeltaEta )
                result["DeltaPhi_b2l"] = DeltaPhi
                result["DeltaEtaDeltaPhi_b2l"] = [[ DeltaEta, DeltaPhi ]]
        
        # bjet comb
        DeltaR_bb_closest = 1000 # >> pi
#        PT_bb_leading = 0
        bjet_closest = [ ]
        p_bb1 = None
        madeCut_closest = False
        for j1, j2 in combinations(bjets,2):
            p_bb = j1.TLV + j2.TLV
            DeltaR = TLV.DeltaR(j1.TLV, j2.TLV)
            madeCut = False
            if lepton:
                if DeltaR < 2.5 and fold(abs(lepton.Phi - j1.Phi))>1 and \
                                   fold(abs(lepton.Phi - j2.Phi))>1 :
                    madeCut = True
                    result["M_bb_cut"].append(p_bb.M())
#                    if p_bb.Pt() > PT_bb_leading:
#                        result["M_bb_leading_cut"] = p_bb.Pt()

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
                madeCut_closest = madeCut
        
        if madeCut_closest:
            result["M_bb_closest_cut"] = p_bb1.M()
        
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


        if lepton:
            
            # MET - lepton
            result["leptonPt"] = lepton.PT
            result["MET"] = MET.MET
            result["DeltaPhi_lMET"] = abs(MET.Phi-lepton.Phi)
            result["MT_lnu"] = recoWlnu2Mt(lepton,MET)
        
            # jet i - lepton
            ji = sorted(jets, key=lambda j: TLV.DeltaR(j.TLV,lepton.TLV))[:3] # closest jets
            if len(ji)>0:
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

        # jet comb
        p_jj_cut = [ ]
#        p_jj_b2b = None
#        p_jj_b2b_cut = None
#        DeltaPhi_b2b = 0 # < pi
        for j1, j2 in combinations(jets,2):
            p_jj = j1.TLV + j2.TLV
            DeltaPhi = fold(abs(j1.Phi - j2.Phi))
            result["M_jj_all"].append(p_jj.M())
            result["DeltaR_jj_all"].append(TLV.DeltaR( j1.TLV, j2.TLV ))
            result["DeltaPhi_jj_all"].append(DeltaPhi)
            result["DeltaEtaDeltaPhi_jj_all"].append([ abs(j1.Eta - j2.Eta),
                                                   DeltaPhi ])
            
            # jets comb - lepton
            madeCut = False
            if lepton:
                if ((TLV.DeltaR(lepton.TLV,j1.TLV)<1.5 and TLV.DeltaR(lepton.TLV,j2.TLV) < 2) or \
                    (TLV.DeltaR(lepton.TLV,j1.TLV)<2   and TLV.DeltaR(lepton.TLV,j2.TLV) < 1.5)) and \
                     DeltaPhi < 2:
                    madeCut = True
                    p_jj_cut.append(p_jj)
                    result["M_jj_all_cut"].append(p_jj.M())
                DeltaPhi = fold(abs(lepton.Phi - p_jj.Phi()))
                result["M_jjl_all"].append( (lepton.TLV+p_jj).M() )
                result["DeltaR_jjl_all"].append( TLV.DeltaR(lepton.TLV,p_jj) )
                result["DeltaPhi_jjl_all"].append( DeltaPhi )
                result["DeltaEtaDeltaPhi_jjl_all"].append([ abs(lepton.Eta - p_jj.Eta()),
                                                        DeltaPhi ])
#            # find best b2b comb
#            beta = p_jj.BoostVector()
#            q1 = copy(j1.TLV)
#            q2 = copy(j2.TLV)
#            q1.Boost(-beta)
#            q2.Boost(-beta)
#            DeltaPhi = fold(abs(q1.Phi()-q2.Phi()))
#            if DeltaPhi > DeltaPhi_b2b:
#                p_jj_b2b = copy(p_jj)
#                DeltaPhi_b2b = DeltaPhi
#                if madeCut:
#                    p_jj_b2b_cut = p_jj_b2b
#                    #DeltaPhi_b2b_cut = DeltaPhi
#
#        if p_jj_b2b:
#            result["M_jj_b2b"] = p_jj_b2b.M()
#            result["DeltaPhi_jj_b2b"] = DeltaPhi_b2b
#            result["MDeltaPhi_jj_b2b"] = [[ p_jj_b2b.M(), DeltaPhi_b2b ]]            
#            if p_jj_b2b_cut:
#                result["M_jj_b2b_cut"] = p_jj_b2b.M()

        if len(jets)>1:
            p_jj = jets[0].TLV + jets[1].TLV
            result["M_jj"] = p_jj.M()
            result["DeltaR_jj"] = TLV.DeltaR(jets[0].TLV, jets[1].TLV)
            result["DeltaPhi_jj"] = fold(abs(jets[0].Phi - jets[1].Phi))
            result["DeltaEtaDeltaPhi_jj"] = [[ abs(jets[0].Eta - jets[1].Eta),
                                                       result["DeltaPhi_jj"] ]]
            if lepton:
                result["M_jjl"] = (p_jj + lepton.TLV).M()
                result["M_jjlnu"] = (p_jj + lepton.TLV + p_neutrino).M()
                result["DeltaR_jjl"] = TLV.DeltaR(p_jj,lepton.TLV)
                result["DeltaPhi_jjl"] = fold(abs(p_jj.Phi()-lepton.Phi))
                result["DeltaEtaDeltaPhi_jjl"] = [[ abs(p_jj.Eta() - lepton.Eta),
                                                            result["DeltaPhi_jjl"] ]]
                p_jjl = p_jj + lepton.TLV
                result["DeltaPhi_jjlnu"] = fold(abs(p_jjl.Phi()-MET.Phi))
                result["MT_jjlnu"] = sqrt(2 * MET.MET * p_jjl.Pt() * (1-cos( p_jjl.Phi() - MET.Phi)) )
                if len(bl): # take bjet closest to lepton
                    result["M_blnu"] = (bl[-1].TLV + lepton.TLV + p_neutrino).M()
                    if len(bl)>1 and len(event.cleanedJets20)>3: # take bjet second closest to lepton
                        jets_tt = event.cleanedJets20[:]
                        jets_tt.remove(bl[-1])
                        jets_tt.remove(bl[-2])
                        p_jj_tt = jets_tt[0].TLV + jets_tt[1].TLV
                        result["M_jjb"] = (p_jj_tt + bl[-2].TLV).M()
                        result["DeltaR_jjb"] = TLV.DeltaR(p_jj,bl[-2].TLV)
                        result["DeltaPhi_jjb"] = fold(abs(p_jj.Phi()-bl[-2].Phi))
                        result["DeltaEtaDeltaPhi_jjb"] = [[ abs(p_jj.Eta() - bl[-2].Eta),
                                                                    result["DeltaPhi_jjb"] ]]
                        result["DeltaR_jjlbb"] = TLV.DeltaR(p_jjl,p_bb1)
                        result["DeltaPhi_jjlbb"] = fold(abs(p_jjl.Phi()-p_bb1.Phi()))
                        result["DeltaEtaDeltaPhi_jjlbb"] = [[ abs(p_jjl.Eta() - p_bb1.Eta()),
                                                              result["DeltaPhi_jjlbb"] ]]
    

        if p_jj_cut:
            p = max(p_jj_cut, key=lambda p: p.Pt())
            result["M_jj_cut"] = p.M()
        
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
  runTest(sys.argv[1], LeptonControlPlots())

