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
              "leptonPt","MET",
              "DeltaR_j1l","DeltaR_j2l",
              "DeltaR_b1l","DeltaR_b2l",
              "DeltaR_bb1","DeltaR_jjl_leading",
              "DeltaPhi_METl",
              "M_bb_closest",
              "M_jjb_leading", "M_blnu",
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
        self.add("leptonPt","lepton Pt",100,0,250)
        self.add("MET","MET",100,0,300)

        self.add("M_jj","jet-jet combinations Mass",100,0,300)
        self.add("M_jj_cut","jet-jet combinations (cut) Mass",100,0,300)
        self.add("M_jj_leading","leading jet-jet Mass",100,0,300)
        self.add("M_jj_leading_cut","leading jet-jet (cut) Mass",100,0,300)
#        self.add("M_jj_b2b","jet-jet b2b Mass",100,0,300)
#        self.add("M_jj_b2b_(cut)","jet-jet b2b Mass",100,0,300)
        self.add("M_jjb_leading","leading jet-jet-bjet Mass",200,0,700)
        self.add("M_jjl","jets-lepton combinations Mass",150,0,450)
        self.add("M_jjl_leading","leading jets-lepton combinations Mass",150,0,450)
        self.add("M_bb_leading","leading bjet-bjet Mass",100,0,300)
        self.add("M_bb_leading_cut","leading bjet-bjet (cut) Mass",100,0,300)
        self.add("M_bb_closest","closest bjet-bjet Mass",100,0,300)
        self.add("M_bb_closest_cut","closest bjet-bjet (cut) Mass",100,0,300)
        self.add("M_bb_farthest","farthest bjet-bjet Mass",100,0,300)
        self.add("M_bb_cut","bjet-bjet combinations (cut) Mass",100,0,300)
        self.add("M_b1l","closest bjet-lepton Mass",100,0,300)
        self.add("MT_lnu","Wlnu Mt",100,0,300)
        self.add("MT_jjlnu","Wlnu Mt",100,0,300)
        self.add("M_blnu","blnu reco Mass",100,0,500)

#        self.add("DeltaPt_jl","lepton-bjet Mass",100,0,2)
#        self.add2D("DeltaRDeltaPt_jl","lepton-bjet DeltaPt vs. DeltaR",100,0,4.5,100,0,2)

        self.add("DeltaR_jj","jet-jet combinations DeltaR",100,0,4)
        self.add("DeltaR_j1l","closest jet-lepton DeltaR",100,0,4)
        self.add("DeltaR_j2l","2nd closest jet-lepton DeltaR",100,0,4)
        self.add("DeltaR_jjl","jets-lepton combinations DeltaR",100,0,5)
        self.add("DeltaR_jjl_leading","leading jets-lepton DeltaR",100,0,4.5)
        self.add("DeltaR_bb1","closest bjet-bjet combination DeltaR",100,0,4)
        self.add("DeltaR_b1l","farthest bjet-lepton DeltaR",100,0,4)
        self.add("DeltaR_b2l","2nd farthest bjet-lepton DeltaR",100,0,4)
        self.add("DeltaRi_b1l","farthest bjet-lepton DeltaRi",100,0,4)
        self.add("DeltaRi_b2l","2nd farthest bjet-lepton DeltaRi",100,0,4)

        self.add("DeltaPhi_jj","jet-jet combinations DeltaPhi",100,0,3.5)
#        self.add("DeltaPhi_jj_b2b","jet-jet DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j1l","closest jet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j2l","2nd closest jet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjl","jets-lepton combinations DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjl_leading","leading jets-lepton combinations DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_bb1","closest bjet-bjet combination DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_b1l","farthest bjet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_b2l","2nd farthest bjet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_METl","MET-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjlnu","jet-jet-lepton-MET DeltaPhi",100,0,3.5)

        self.add2D("DeltaEtaDeltaPhi_jj","jet-jet combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j1l","closest jet-lepton combination DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j2l","2nd closest jet-lepton combination DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j3l","3rd closest jet-lepton combination DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjl","jets-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjl_leading","leading jets-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_bb1","closest bjet-bjet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b1l","farthest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b2l","2nd farthest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)

#        self.add2D("MDeltaPhi_jj_b2b","jet-jet DeltaPhi vs. Mass",100,0,200,50,0,3.2)



    # get information
    def process(self, event):
    
        result = { }
        
        result["M_jj"] = [ ]
        result["M_jj_cut"] = [ ]
        result["M_jjl"] = [ ]
        result["M_bb_cut"] = [ ]

        #result["DeltaPt_jl"] = event.DeltaPt_jl
        #result["DeltaRDeltaPt_jl"] = map(lambda R,Pt: [R,Pt], event.DeltaR_jl,event.DeltaPt_jl)

        result["DeltaR_jj"] = [ ]
        result["DeltaR_jjl"] = [ ]
        result["DeltaR_jjbb"] = [ ]

        result["DeltaPhi_jj"] = [ ]
        result["DeltaPhi_jjl"] = [ ]

        result["DeltaEtaDeltaPhi_jj"] = [ ]
        result["DeltaEtaDeltaPhi_jjl"] = [ ]

        jets = event.cleanedJets20[:] # remove closest b-jets pair down below
        bjets = event.bjets30[:]
        MET = event.met[0]
        result["Njets20"] = len(event.cleanedJets20)
        result["Njets30"] = len(event.cleanedJets30)
        result["Nbjets30"] = len(event.bjets30)

        lepton = None
        if len(event.leadingLeptons):
            lepton = event.leadingLeptons[0]
            lepton.TLV = TLV()
            lepton.TLV.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
        
        for jet in event.cleanedJets20:
            jet.TLV = TLV()
            jet.TLV.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
        
        # bjet - bjet
        bl = [ ]
        if lepton and bjets:
            bl = sorted( bjets, key=lambda j: TLV.DeltaR(j.TLV,lepton.TLV), reverse=True ) # farthest->closest
            DeltaPhi = fold(abs(lepton.Phi - bl[0].Phi))
            DeltaEta = abs(lepton.Eta - bl[0].Eta)
            result["M_b1l"] = (lepton.TLV+bl[-1].TLV).M()
            result["DeltaR_b1l"] = TLV.DeltaR(lepton.TLV,bl[0].TLV)
            result["DeltaRi_b1l"] = sqrt( (pi-DeltaPhi)*(pi-DeltaPhi) + DeltaEta*DeltaEta )
            result["DeltaPhi_b1l"] = DeltaPhi
            result["DeltaEtaDeltaPhi_b1l"] = [[ DeltaEta, DeltaPhi ]]
            if len(bl)>1:
                DeltaPhi = fold(abs(lepton.Phi - bl[1].Phi))
                DeltaEta = abs(lepton.Eta - bl[1].Eta)
                result["M_bb_farthest"] = (bl[0].TLV+bl[1].TLV).M()
                result["DeltaR_b2l"] = TLV.DeltaR(lepton.TLV,bl[1].TLV)
                result["DeltaRi_b2l"] = sqrt( (pi-DeltaPhi)*(pi-DeltaPhi) + DeltaEta*DeltaEta )
                result["DeltaPhi_b2l"] = DeltaPhi
                result["DeltaEtaDeltaPhi_b2l"] = [[ DeltaEta, DeltaPhi ]]
        
        # bjet comb
        DeltaR_bb_closest = 100 # >> pi
        PT_bb_leading = 0
        bjet_closest = [ ]
        madeCut_closest = False
        for j1, j2 in combinations(bjets,2):
            p_bb = j1.TLV + j2.TLV
            DeltaR = TLV.DeltaR(j1.TLV, j2.TLV)
            madeCut = False
            if lepton:
                if DeltaR <2.5 and fold(abs(lepton.Phi - j1.Phi))>1 and \
                                   fold(abs(lepton.Phi - j2.Phi))>1 :
                    madeCut = True
                    result["M_bb_cut"].append(p_bb.M())
                    if p_bb.Pt() > PT_bb_leading:
                        result["M_bb_leading_cut"] = p_bb.Pt()

            if DeltaR < DeltaR_bb_closest:
                bjet_closest = [j1,j2]
                result["M_bb_closest"] = p_bb.M()
                result["DeltaR_bb1"] = TLV.DeltaR(j1.TLV,j2.TLV)
                result["DeltaPhi_bb1"] = fold(abs(j1.Phi - j2.Phi))
                result["DeltaEtaDeltaPhi_bb1"] = [[ abs(j1.Eta - j2.Eta),
                                                    result["DeltaPhi_bb1"] ]]
                DeltaR_bb_closest = DeltaR
                madeCut_closest = True
        
        if madeCut_closest:
            result["M_bb_closest_cut"] = p_bb.M()
        
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
        if len(bjets)>0:
            result["bjet1Pt"] = bjet_closest[0].PT
            if len(bjets)>1:
                result["bjet2Pt"] = bjet_closest[1].PT

        if lepton:
            
            # MET - lepton
            result["leptonPt"] = lepton.PT
            result["MET"] = MET.MET
            result["DeltaPhi_METl"] = abs(MET.Phi-lepton.Phi)
            result["MT_lnu"] = recoWlnu2Mt(lepton,MET)
        
            # jet i - lepton
            jil = sorted(jets, key=lambda j: TLV.DeltaR(j.TLV,lepton.TLV))[:3] # closest jets
            if len(jil)>0:
                result["DeltaR_j1l"] = TLV.DeltaR(lepton.TLV,jil[0].TLV)
                result["DeltaPhi_j1l"] = fold(abs(lepton.Phi - jil[0].Phi))
                result["DeltaEtaDeltaPhi_j1l"] = [[ abs(lepton.Eta - jil[0].Eta),
                                                    result["DeltaPhi_j1l"] ]]
                if len(jil)>1:
                    result["DeltaR_j2l"] = TLV.DeltaR(lepton.TLV,jil[1].TLV)
                    result["DeltaPhi_j2l"] = fold(abs(lepton.Phi - jil[1].Phi))
                    result["DeltaEtaDeltaPhi_j2l"] = [[ abs(lepton.Eta - jil[1].Eta),
                                                        result["DeltaPhi_j2l"] ]]
                    if len(jil)>2:
                        result["DeltaEtaDeltaPhi_j3l"] = [[ abs(lepton.Eta - jil[2].Eta),
                                                            fold(abs(lepton.Phi - jil[2].Phi)) ]]

        # jet comb
        p_jj_cut = [ ]
#        p_jj_b2b = None
#        p_jj_b2b_cut = None
#        DeltaPhi_b2b = 0 # < pi
        for j1, j2 in combinations(jets,2):
            p_jj = j1.TLV + j2.TLV
            DeltaPhi = fold(abs(j1.Phi - j2.Phi))
            result["M_jj"].append(p_jj.M())
            result["DeltaR_jj"].append(TLV.DeltaR( j1.TLV, j2.TLV ))
            result["DeltaPhi_jj"].append(DeltaPhi)
            result["DeltaEtaDeltaPhi_jj"].append([ abs(j1.Eta - j2.Eta),
                                                   DeltaPhi ])
            
            # jets comb - lepton
            madeCut = False
            if lepton:
                if ((TLV.DeltaR(lepton.TLV,j1.TLV)<1.5 and TLV.DeltaR(lepton.TLV,j2.TLV) < 2) or \
                    (TLV.DeltaR(lepton.TLV,j1.TLV)<2   and TLV.DeltaR(lepton.TLV,j2.TLV) < 1.5)) and \
                     DeltaPhi < 2:
                    madeCut = True
                    p_jj_cut.append(p_jj)
                    result["M_jj_cut"].append(p_jj.M())
                DeltaPhi = fold(abs(lepton.Phi - p_jj.Phi()))
                result["M_jjl"].append( (lepton.TLV+p_jj).M() )
                result["DeltaR_jjl"].append( TLV.DeltaR(lepton.TLV,p_jj) )
                result["DeltaPhi_jjl"].append( DeltaPhi )
                result["DeltaEtaDeltaPhi_jjl"].append([ abs(lepton.Eta - p_jj.Eta()),
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
            result["M_jj_leading"] = p_jj.M()
            if lepton:
                result["M_jjl_leading"] = (p_jj + lepton.TLV).M()
                result["DeltaR_jjl_leading"] = TLV.DeltaR(p_jj,lepton.TLV)
                result["DeltaPhi_jjl_leading"] = fold(abs(p_jj.Phi()-lepton.Phi))
                result["DeltaEtaDeltaPhi_jjl_leading"] = [[ abs(p_jj.Eta() - lepton.Eta),
                                                            result["DeltaPhi_jjl_leading"] ]]
                p_jjl = p_jj + lepton.TLV
                result["DeltaPhi_jjlnu"] = fold(abs(p_jjl.Phi()-MET.Phi))
                result["MT_jjlnu"] = sqrt(2 * MET.MET * p_jjl.Pt() * (1-cos( p_jjl.Phi() - MET.Phi)) )
                if len(bl): # take bjet closest to lepton
                    result["M_blnu"] = (bl[-1].TLV + lepton.TLV + recoNeutrino(lepton.TLV,MET)).M()
                    if len(bl)>1 and len(event.cleanedJets20)>3: # take bjet second closest to lepton
                        jets_tt = event.cleanedJets20[:]
                        jets_tt.remove(bl[-1])
                        jets_tt.remove(bl[-2])
                        p_jj_tt = jets_tt[0].TLV + jets_tt[1].TLV
                        result["M_jjb_leading"] = (p_jj_tt + bl[-2].TLV).M()
    

        if p_jj_cut:
            p = max(p_jj_cut, key=lambda p: p.Pt())
            result["M_jj_leading_cut"] = p.M()
        
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

