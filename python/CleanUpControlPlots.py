from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
from ROOT import TTree, TBranch
from itertools import combinations # to make jets combinations
from copy import copy
from fold import fold
#from reconstruct import max_b2b
from reconstruct import recoWlnu2Mt

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
        self.addBranch("cleanup","DeltaR_b1l")
        self.addBranch("cleanup","DeltaR_b2l")
        self.addBranch("cleanup","DeltaR_bb1")
        self.addBranch("cleanup","M_bb_closest")
        self.addBranch("cleanup","jet1Pt")
        self.addBranch("cleanup","jet2Pt")
        self.addBranch("cleanup","bjet1Pt")
        self.addBranch("cleanup","bjet2Pt")
        self.addBranch("cleanup","DeltaR_j1l")
        self.addBranch("cleanup","DeltaR_j2l")
        self.addBranch("cleanup","leptonPt")
        self.addBranch("cleanup","MET")
        self.addBranch("cleanup","DeltaPhi_METl")
        self.addBranch("cleanup","MT_lnu")

        self.add("Njets20","jets multiplicity (Pt > 20 GeV)",100,0,250)
        self.add("Njets30","jets multiplicity (Pt > 30 GeV)",100,0,250)
        self.add("Nbjets30","bjets multiplicity (Pt > 30 GeV)",100,0,250)
        self.add("jet1Pt","jet 1 Pt",100,0,250)
        self.add("jet2Pt","jet2 Pt",100,0,250)
        self.add("bjetPt","jet 1 Pt",100,0,250)
        self.add("bjet2Pt","jet2 Pt",100,0,250)
        self.add("MET","MET",100,0,300)

        self.add("M_jj","jet-jet combinations Mass",100,0,300)
        self.add("M_jj_cut","jet-jet combinations (cut) Mass",100,0,300)
        self.add("M_jj_leading","leading jet-jet Mass",100,0,300)
        self.add("M_jj_leading_cut","jet-jet (cut) Mass",100,0,300)
#        self.add("M_jj_b2b","jet-jet b2b Mass",100,0,300)
#        self.add("M_jj_b2b_cut","jet-jet b2b Mass",100,0,300)
        self.add("M_jjb_leading","jet-jet-bjet Mass",100,0,300)
        self.add("M_jjl","jets-lepton combinations Mass",150,0,450)
        self.add("M_bb_leading","bjet-bjet Mass",100,0,300)
        self.add("M_bb_closest","closest bjet-bjet Mass",100,0,300)
        self.add("M_bb_cut","bjet-bjet combinations (cut) Mass",100,0,300)
        self.add("M_bb_leading_cut","bjet-bjet (cut) Mass",100,0,300)
        self.add("M_bb_closest_cut","closest bjet-bjet (cut) Mass",100,0,300)
        self.add("M_b1l","closest bjet-lepton Mass",100,0,300)
        self.add("MT_lnu","Wlnu Mt",100,0,300)

        #self.add("DeltaPt_jl","lepton-bjet Mass",100,0,2)
        #self.add2D("DeltaRDeltaPt_jl","lepton-bjet DeltaPt vs. DeltaR",100,0,4.5,100,0,2)

        self.add("DeltaR_jj","jet-jet combinations DeltaR",100,0,4)
        self.add("DeltaR_j1l","closest jet-lepton DeltaR",100,0,4)
        self.add("DeltaR_j2l","2nd closest jet-lepton DeltaR",100,0,4)
        self.add("DeltaR_jjl","jets-lepton combinations DeltaR",100,0,4)
        self.add("DeltaR_bb1","closest bjet-bjet combinations DeltaR",100,0,4)
        self.add("DeltaR_b1l","closest bjet-lepton DeltaR",100,0,4)
        self.add("DeltaR_b2l","2nd closest bjet-lepton DeltaR",100,0,4)

        self.add("DeltaPhi_jj","jet-jet combinations DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jj_b2b","jet-jet DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j1l","closest jet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_j2l","2nd closest jet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_jjl","jets-lepton combinations DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_bb1","closest bjet-bjet combinations DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_b1l","closest bjet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_b2l","2nd closest bjet-lepton DeltaPhi",100,0,3.5)
        self.add("DeltaPhi_METl","MET-lepton DeltaPhi",100,0,3.5)

        self.add2D("DeltaEtaDeltaPhi_jj","jet-jet combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j1l","closest jet-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j2l","2nd closest jet-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_j3l","3rd closest jet-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_jjl","jets-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_bb1","closest bjet-bjet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b1l","closest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b2l","2nd closest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)

#        self.add2D("MDeltaPhi_jj_b2b","jet-jet DeltaPhi vs. Mass",100,0,200,50,0,3.2)



    # get information
    def process(self, event):
    
        result = { }

        result["cleanup"] = [ ] # respect the order of branches when adding variables
        
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

        jets = event.cleanedJets20 # remove closest b-jets pair down below
        bjets = event.bjets30
        result["Njets20"] = len(event.cleanedJets20)
        result["Njets30"] = len(event.cleanedJets30)
        result["Nbjets30"] = len(event.bjets30)

        lepton = None
        if len(event.leadingLeptons):
            lepton = event.leadingLeptons[0]
        
        # bjet - bjet
        bl = [ ]
        if lepton:
            bl = sorted( bjets, key=lambda j: TLV.DeltaR(j.TLV,lepton.TLV) )[:2] # need closest
            result["M_b1l"] = (lepton.TLV+bl[0].TLV).M()
            result["DeltaR_b1l"] = TLV.DeltaR(lepton.TLV,bl[0].TLV)
            result["cleanup"].append(result["DeltaR_b1l"])
            result["DeltaPhi_b1l"] = fold(abs(lepton.Phi - bl[0].Phi))
            result["DeltaEtaDeltaPhi_b1l"] = [[ abs(lepton.Eta - bl[0].Eta),
                                                result["DeltaPhi_b1l"] ]]
            if len(p_bl)>1:
                result["DeltaR_b2l"] = TLV.DeltaR(lepton.TLV,bl[1].TLV)
                result["cleanup"].append(result["DeltaR_b2l"])
                result["DeltaPhi_b2l"] = fold(abs(lepton.Phi - bl[1].Phi))
                result["DeltaEtaDeltaPhi_b2l"] = [[ abs(lepton.Eta - bl[1].Eta),
                                                    result["DeltaPhi_b2l"] ]]

        # bjet comb
        DeltaR_bb_closest = 100 # >> pi
        PT_bb_leading = 0
        bjet_closest = [ ]
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
                bjet_closest = [j1.TLV,j2.TLV]
                result["M_bb_closest"] = p_bb.M()
                result["cleanup"].append(result["M_bb_closest"])
                result["DeltaR_bb1"] = TLV.DeltaR(lepton, p_bb)
                result["cleanup"].append(result["DeltaR_bb1"])
                result["DeltaPhi_bb1"] = fold(abs(lepton.Phi - p_bb.Phi()))
                result["DeltaEtaDeltaPhi_bb1"] = [[ abs(lepton.Eta - p_bb.Eta),
                                                    fold(abs(lepton.Phi - p_bb.Phi())) ]]
                DeltaR_bb_closest = DeltaR
                if madeCut:
                    result["M_bb_closest_cut"] = p_bb.M()
        
        if len(bjets)>1:
            result["M_bb_leading"] = (p_bjets[0]+p_bjets[1]).M()



        # leading non-b-jets
        for bjet in bjet_closest: # remove closest bjets pair from jet list
            jets.remove(bjet)
        if len(jets)>0:
            result["jet1Pt"] = jets[0].PT
            result["cleanup"].append(result["jet1Pt"])
            if len(jets)>1:
                result["jet2Pt"] = jets[1].PT
                result["cleanup"].append(result["jet2Pt"])
        
        # leading bjets
        if len(bjets)>0:
            result["bjet1Pt"] = bjets[0].PT
            result["cleanup"].append(result["bjet1Pt"])
            if len(bjets)>1:
                result["bjet2Pt"] = bjets[1].PT
                result["cleanup"].append(result["bjet2Pt"])
        
        
        
        
        
        # jet - jet
        p_jjs = [ ]
        p_jj_cut = [ ]
#        p_jj_b2b = None
#        p_jj_b2b_cut = None
#        DeltaPhi_b2b = 0 # < pi

        # jet i - lepton
        if lepton:
            jil = sorted(jets, key=lambda j: TLV.DeltaR(j.TLV,lepton.TLV))[:3]
            if len(p_ji)>0:
                result["DeltaR_j1l"] = TLV.DeltaR(lepton.TLV,jil[0].TLV)
                result["cleanup"].append(result["DeltaR_j1l"])
                result["DeltaPhi_j1l"] = fold(abs(lepton.Phi - jil[0].Phi))
                result["DeltaEtaDeltaPhi_j1l"] = [[ abs(lepton.Eta - ji[0].Eta),
                                                    result["DeltaPhi_j1l"] ]]
                if len(p_ji)>1:
                    result["DeltaR_j2l"] = TLV.DeltaR(lepton.TLV,ji[1].TLV)
                    result["cleanup"].append(result["DeltaR_j2l"])
                    result["DeltaPhi_j2l"] = fold(abs(lepton.Phi - ji[1].Phi))
                    result["DeltaEtaDeltaPhi_j2l"] = [[ abs(lepton.Eta - ji[1].Eta),
                                                        result["DeltaPhi_j2l"] ]]
                    if len(p_ji)>2:
                        result["DeltaEtaDeltaPhi_j3l"] = [[ abs(lepton.Eta - ji[2].Eta),
                                                            fold(abs(lepton.Phi - ji[2].Phi)) ]]

        # jet comb
        for j1, j2 in combinations(jets,2):
            p_jj = j1 + j2
            p_jjs.append( p_jj )
            DeltaPhi = fold(abs(j1.Phi - j2.Phi))
            result["M_jj"].append(p_jj.M())
            result["DeltaR_jj"].append(TLV.DeltaR( j1, j2 ))
            result["DeltaPhi_jj"].append(DeltaPhi)
            result["DeltaEtaDeltaPhi_jj"].append([ abs(j1.Eta - j2.Eta),
                                                   DeltaPhi ])
            
            # jets comb - lepton
            madeCut = False
            if lepton:
                if ((TLV.DeltaR(lepton.TLV,j1)<1.5 and TLV.DeltaR(lepton.TLV,j2) < 2) or \
                    (TLV.DeltaR(lepton.TLV,j1)<2   and TLV.DeltaR(lepton.TLV,j2) < 1.5)) and \
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
            result["M_jj_leading"] = (p_jets[0] + p_jets[1]).M()
            if lepton:
                result["M_jjb_leading"] = (p_jets[0] + p_jets[1] + bl.TLV).M()

        if p_jj_cut:
            p = max(p_jj_cut, key=lambda p: p.Pt())
            result["M_jj_leading_cut"] = p.M()

        # MET - lepton
        if lepton:
            result["leptonPt"] = lepton.PT
            result["cleanup"].append(result["leptonPt"])
            result["MET"] = event.met[0].MET
            result["cleanup"].append(result["MET"])
            result["DeltaPhi_METl"] = abs(event.met[0].Phi-lepton.Phi)
            result["cleanup"].append(result["DeltaPhi_METl"])
            result["MT_lnu"] = recoWlnu2Mt(lepton,event.met[0])
            result["cleanup"].append(result["MT_lnu"])
        
#        for key, value in result.iteritems():
#            if not isinstance(value, (int, long, float)):
#                if isinstance(value, list):
#                    if len(value):
#                        if not isinstance(value[0], (int, long, float)):
#                            print ">>> We have a bad list: " + key + ", type" + type(value[0])
#                    else:
#                        print ">>> We have an empty list: " + key
#                
#                else:
#                    print ">>> We has it: " + ", type" + type(value[0])

        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], LeptonControlPlots())

