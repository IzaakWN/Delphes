from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
from ROOT import TTree, TBranch
from itertools import combinations # to make jets combinations
from copy import copy
from fold import fold
#from reconstruct import max_b2b
#from reconstruct import reconstructWlnu

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
      self.addBranch("cleanup","jet1Pt")
      self.addBranch("cleanup","jet2Pt")
      self.addBranch("cleanup","bjet1Pt")
      self.addBranch("cleanup","bjet2Pt")
      self.addBranch("cleanup","DeltaPhi_METl")
      self.addBranch("cleanup","DeltaR_j1l")
      self.addBranch("cleanup","DeltaR_j2l")
      self.addBranch("cleanup","DeltaR_b1l")
      self.addBranch("cleanup","DeltaR_b2l")
      self.addBranch("cleanup","DeltaR_bb1")
      self.addBranch("cleanup","M_bb_closest")
    
      # declare histograms
      self.add("M_jj","jet-jet combinations Mass",100,0,300)
      self.add("M_jj_cut","jet-jet combinations (cut) Mass",100,0,300)
      self.add("M_jj_leading","leading jet-jet Mass",100,0,300)
      self.add("M_jj_leading_cut","jet-jet (cut) Mass",100,0,300)
      self.add("M_jj_b2b","jet-jet b2b Mass",100,0,300)
      self.add("M_jj_b2b_cut","jet-jet b2b Mass",100,0,300)
      self.add("M_jjl","jets-lepton combinations Mass",150,0,450)
      self.add("M_bb","bjet-bjet combinations Mass",100,0,300)
      self.add("M_bb_leading","bjet-bjet Mass",100,0,300)
      self.add("M_bb_closest","closest bjet-bjet Mass",100,0,300)
      self.add("M_bb_cut","bjet-bjet combinations (cut) Mass",100,0,300)
      self.add("M_bb_leading_cut","bjet-bjet (cut) Mass",100,0,300)
      self.add("M_bb_closest_cut","closest bjet-bjet (cut) Mass",100,0,300)
      self.add("M_b1l","closest bjet-lepton Mass",100,0,300)

      #self.add("DeltaPt_jl","lepton-bjet Mass",100,0,2)
      #self.add2D("DeltaRDeltaPt_jl","lepton-bjet DeltaPt vs. DeltaR",100,0,4.5,100,0,2)

      self.add("DeltaR_jj","jet-jet combinations DeltaR",100,0,4)
      self.add("DeltaR_jl","jet-lepton combinations DeltaR",100,0,4)
      self.add("DeltaR_j1l","closest jet-lepton DeltaR",100,0,4)
      self.add("DeltaR_j2l","2nd closest jet-lepton DeltaR",100,0,4)
      self.add("DeltaR_jjl","jets-lepton combinations DeltaR",100,0,4)
      self.add("DeltaR_bb","bjet-bjet combinations DeltaR",100,0,4)
      self.add("DeltaR_bb1","closest bjet-bjet combinations DeltaR",100,0,4)
      self.add("DeltaR_bl","bjet-lepton combinations DeltaR",100,0,4)
      self.add("DeltaR_b1l","closest bjet-lepton DeltaR",100,0,4)
      self.add("DeltaR_b2l","2nd closest bjet-lepton DeltaR",100,0,4)
      self.add("DeltaR_jjbb","jets-bjets combinations DeltaR",100,0,4)

      self.add("DeltaPhi_jj","jet-jet combinations DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_jj_b2b","jet-jet DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_jl","jet-lepton combinations DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_j1l","closest jet-lepton DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_j2l","2nd closest jet-lepton DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_jjl","jets-lepton combinations DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_bb","bjet-bjet combinations DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_bb1","closest bjet-bjet combinations DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_bl","bjet-lepton combinations DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_b1l","closest bjet-lepton DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_b2l","2nd closest bjet-lepton DeltaPhi",100,0,3.5)
      self.add("DeltaPhi_METl","MET-lepton DeltaPhi",100,0,3.5)

      self.add2D("DeltaEtaDeltaPhi_jj","jet-jet combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_jl","jet-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_j1l","closest jet-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_j2l","2nd closest jet-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_j3l","3rd closest jet-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_jjl","jets-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_bb","bjet-bjet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_bb1","closest bjet-bjet DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_bl","bjet-lepton combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_b1l","closest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_b2l","2nd closest bjet-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_jjbb","jets-bjets combinations DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)

      self.add2D("MDeltaPhi_jj_b2b","jet-jet DeltaPhi vs. Mass",100,0,200,50,0,3.2)
    


    # get information
    def process(self, event):
    
        result = { }

        result["cleanup"] = [ ] # respect the order of branches when adding variables
        
        result["M_jj"] = [ ]
        result["M_jj_cut"] = [ ]
        result["M_jjl"] = [ ]
        result["M_bb"] = [ ]
        result["M_bb_cut"] = [ ]

        #result["DeltaPt_jl"] = event.DeltaPt_jl
        #result["DeltaRDeltaPt_jl"] = map(lambda R,Pt: [R,Pt], event.DeltaR_jl,event.DeltaPt_jl)

        result["DeltaR_jj"] = [ ]
        result["DeltaR_jl"] = [ ]
        result["DeltaR_jjl"] = [ ]
        result["DeltaR_bb"] = [ ]
        result["DeltaR_bl"] = [ ]
        result["DeltaR_jjbb"] = [ ]

        result["DeltaPhi_jj"] = [ ]
        result["DeltaPhi_jl"] = [ ]
        result["DeltaPhi_jjl"] = [ ]
        result["DeltaPhi_bb"] = [ ]
        result["DeltaPhi_bl"] = [ ]

        result["DeltaEtaDeltaPhi_jj"] = [ ]
        result["DeltaEtaDeltaPhi_jl"] = [ ]
        result["DeltaEtaDeltaPhi_jjl"] = [ ]
        result["DeltaEtaDeltaPhi_bb"] = [ ]
        result["DeltaEtaDeltaPhi_bl"] = [ ]
        result["DeltaEtaDeltaPhi_jjbb"] = [ ]

        nonbjets = [ j for j in event.cleanedJets20 if not j.BTag ]
        bjets = event.bjets30
        
        # leading jets
        if len(nonbjets)>0:
            result["cleanup"].append(nonbjets[0].PT)
            if len(nonbjets)>1:
                result["cleanup"].append(nonbjets[1].PT)
        
        # leading bjets
        if len(bjets)>0:
            result["cleanup"].append(bjets[0].PT)
            if len(bjets)>1:
                result["cleanup"].append(bjets[1].PT)

        # MET - lepton
        result["DeltaPhi_METl"] = abs(event.met[0].Phi-lepton.Phi)
        
        jets = [ j for j in jets if not j.BTag ]
        p_jets = [ ]
        p_jjs = [ ]
        p_jj_cut = [ ]
        p_jj_b2b = None
        p_jj_b2b_cut = None
        DeltaPhi_b2b = 0 # < pi

        p_bjets = [ ]
        p_bb_cut = [ ]
        DeltaR_bl = [ ]
        DeltaR_bb_closest = 100 # >> pi
        PT_bb_leading = 0

        lepton = None
        p_lepton = TLV()
        if len(event.leadingLeptons):
            lepton = event.leadingLeptons[0]
            p_lepton.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
        
        
        
        # jet - jet
        for jet in jets:
            p_jets.append(TLV())
            p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

            # jet - lepton
            if lepton:
                DeltaPhi = fold(abs(lepton.Phi - jet.Phi))
                result["DeltaPhi_jl"].append(DeltaPhi)
                result["DeltaR_jl"].append(TLV.DeltaR(p_lepton,p_jets[-1]))
                result["DeltaEtaDeltaPhi_jl"].append([ abs(lepton.Eta - jet.Eta),
                                                       DeltaPhi ])

        # jet i - lepton
        if lepton:
            p_ji = sorted(p_jets, key=lambda p: TLV.DeltaR(p,p_lepton))[:3]
            if len(p_ji)>0:
                result["DeltaR_j1l"] = TLV.DeltaR(p_lepton,p_ji[0])
                result["cleanup"].append(result["DeltaR_j1l"])
                result["DeltaPhi_j1l"] = fold(abs(lepton.Phi - p_ji[0].Phi()))
                result["DeltaEtaDeltaPhi_j1l"] = [[ abs(lepton.Eta - p_ji[0].Eta()),
                                                    result["DeltaPhi_j1l"] ]]
                if len(p_ji)>1:
                    result["DeltaR_j2l"] = TLV.DeltaR(p_lepton,p_ji[1])
                    result["cleanup"].append(result["DeltaR_j2l"])
                    result["DeltaPhi_j2l"] = fold(abs(lepton.Phi - p_ji[1].Phi()))
                    result["DeltaEtaDeltaPhi_j2l"] = [[ abs(lepton.Eta - p_ji[1].Eta()),
                                                        result["DeltaPhi_j2l"] ]]
                    if len(p_ji)>2:
                        result["DeltaEtaDeltaPhi_j3l"] = [[ abs(lepton.Eta - p_ji[2].Eta()),
                                                            fold(abs(lepton.Phi - p_ji[2].Phi())) ]]

        # jet comb
        for p1, p2 in combinations(p_jets,2):
            p_jj = p1 + p2
            p_jjs.append( p_jj )
            DeltaPhi = fold(abs(p1.Phi() - p2.Phi()))
            result["M_jj"].append(p_jj.M())
            result["DeltaR_jj"].append(TLV.DeltaR( p1, p2 ))
            result["DeltaPhi_jj"].append(DeltaPhi)
            result["DeltaEtaDeltaPhi_jj"].append([ abs(p1.Eta() - p2.Eta()),
                                                   DeltaPhi ])
            
            # jets comb - lepton
            madeCut = False
            if lepton:
                if ((TLV.DeltaR(p_lepton,p1)<1.5 and TLV.DeltaR(p_lepton,p2) < 2) or \
                    (TLV.DeltaR(p_lepton,p1)<2   and TLV.DeltaR(p_lepton,p2) < 1.5)) and \
                     DeltaPhi < 2:
                    madeCut = True
                    p_jj_cut.append(p_jj)
                    result["M_jj_cut"].append(p_jj.M())
                DeltaPhi = fold(abs(lepton.Phi - p_jj.Phi()))
                result["M_jjl"].append( (p_lepton+p_jj).M() )
                result["DeltaR_jjl"].append( TLV.DeltaR(p_lepton,p_jj) )
                result["DeltaPhi_jjl"].append( DeltaPhi )
                result["DeltaEtaDeltaPhi_jjl"].append([ abs(lepton.Eta - p_jj.Eta()),
                                                        DeltaPhi ])
            # find best b2b comb
            beta = p_jj.BoostVector()
            q1 = copy(p1)
            q2 = copy(p2)
            q1.Boost(-beta)
            q2.Boost(-beta)
            DeltaPhi = fold(abs(q1.Phi()-q2.Phi()))
            if DeltaPhi > DeltaPhi_b2b:
                p_jj_b2b = copy(p_jj)
                DeltaPhi_b2b = DeltaPhi
                if madeCut:
                    p_jj_b2b_cut = p_jj_b2b
                    #DeltaPhi_b2b_cut = DeltaPhi
                    
        if p_jj_b2b:
            result["M_jj_b2b"] = p_jj_b2b.M()
            result["DeltaPhi_jj_b2b"] = DeltaPhi_b2b
            result["MDeltaPhi_jj_b2b"] = [[ p_jj_b2b.M(), DeltaPhi_b2b ]]            
            if p_jj_b2b_cut:
                result["M_jj_b2b_cut"] = p_jj_b2b.M()

        if len(jets)>1:
            result["M_jj_leading"] = (p_jets[0] + p_jets[1]).M()

        if p_jj_cut:
            p = max(p_jj_cut, key=lambda p: p.Pt())
            result["M_jj_leading_cut"] = p.M()

        # bjet - bjet
        for bjet in bjets:
            p_bjets.append(TLV())
            p_bjets[-1].SetPtEtaPhiM(bjet.PT, bjet.Eta, bjet.Phi, bjet.Mass)
            if lepton:
                DeltaPhi = fold(abs(lepton.Phi - bjet.Phi))
                DeltaR_bl.append( (p_bjets[-1], TLV.DeltaR(p_lepton,p_bjets[-1])) )
                result["DeltaR_bl"].append(DeltaR_bl[-1][1])
                result["DeltaPhi_bl"].append(DeltaPhi)
                result["DeltaEtaDeltaPhi_bl"].append([ abs(lepton.Eta - bjet.Eta),
                                                       DeltaPhi ])
        if lepton and len(DeltaR_bl):
            p_bl = [ p for (p,D) in sorted(DeltaR_bl, key=lambda x: x[1])[:2] ] # need closest
            result["M_b1l"] = (p_lepton+p_bl[0]).M()
            result["DeltaR_b1l"] = TLV.DeltaR(p_lepton,p_bl[0])
            result["cleanup"].append(result["DeltaR_b1l"])
            result["DeltaPhi_b1l"] = fold(abs(lepton.Phi - p_bl[0].Phi()))
            result["DeltaEtaDeltaPhi_b1l"] = [[ abs(lepton.Eta - p_bl[0].Eta()),
                                                result["DeltaPhi_b1l"] ]]
            if len(DeltaR_bl)>1:
                result["DeltaR_b2l"] = TLV.DeltaR(p_lepton,p_bl[1])
                result["cleanup"].append(result["DeltaR_b2l"])
                result["DeltaPhi_b2l"] = fold(abs(lepton.Phi - p_bl[1].Phi()))
                result["DeltaEtaDeltaPhi_b2l"] = [[ abs(lepton.Eta - p_bl[1].Eta()),
                                                    result["DeltaPhi_b2l"] ]]

        # bjet comb
        for p1, p2 in combinations(p_bjets,2):
            p_bb = p1 + p2
            result["M_bb"].append(p_bb.M())
            result["DeltaR_bb"].append( TLV.DeltaR(p1,p2) )
            result["DeltaPhi_bb"].append( fold(abs(p1.Phi() - p2.Phi())) )
            result["DeltaEtaDeltaPhi_bb"].append([ abs(p1.Eta() - p2.Eta()),
                                                   result["DeltaPhi_bb"][-1] ])
            madeCut = False
            if lepton:
                if result["DeltaR_bb"][-1]<2.5 and \
                   (fold(abs(lepton.Phi - p1.Phi()))>1 or fold(abs(lepton.Phi - p2.Phi()))>1):
                    madeCut = True
                    result["M_bb_cut"].append(p_bb.M())
                    if p_bb.Pt() > PT_bb_leading:
                        result["M_bb_leading_cut"] = p_bb.Pt()

            if result["DeltaR_bb"][-1] < DeltaR_bb_closest:
                result["M_bb_closest"] = p_bb.M()
                result["DeltaR_bb1"] = result["DeltaR_bb"][-1]
                result["DeltaPhi_bb1"] = result["DeltaPhi_bb"][-1]
                result["DeltaEtaDeltaPhi_bb1"] = result["DeltaEtaDeltaPhi_bb"][-1]
                result["cleanup"].append(result["DeltaR_bb1"])
                result["cleanup"].append(result["M_bb_closest"])
                DeltaR_bb_closest = result["DeltaR_bb"][-1]
                if madeCut:
                    result["M_bb_closest_cut"] = p_bb.M()

            # bjets comb - jets comb
            for p_jj in p_jjs:
                result["DeltaR_jjbb"].append(TLV.DeltaR( p_bb, p_jj ))
                result["DeltaEtaDeltaPhi_jjbb"].append([ abs(p_bb.Eta() - p_jj.Eta()),
                                                    fold(abs(p_bb.Phi() - p_jj.Phi())) ])
        
        if len(bjets)>1:
            result["M_bb_leading"] = (p_bjets[0]+p_bjets[1]).M()

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

