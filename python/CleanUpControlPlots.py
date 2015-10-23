from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector
from itertools import combinations # to make jets combinations
from fold import fold
from reconstruct import max_b2b
from copy import copy
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
      # declare histograms
      self.add("M_jj","jet-jet Mass",100,0,300)
      self.add("M_jj_cut","jet-jet (DeltaPhi cut) Mass",100,0,300)
      self.add("M_jj_b2b","jet-jet b2b Mass",100,0,300)
      self.add("M_jjl","jets-lepton Mass",100,0,300)
      self.add("M_bb","bjet-bjet Mass",100,0,300)
      self.add("M_bb_cut","bjet-bjet (DeltaPhi cut) Mass",100,0,300)
      self.add("M_bl","lepton-bjet Mass",100,0,300)

      self.add("DeltaPt_jl","lepton-bjet Mass",100,0,2)
      self.add2D("DeltaRDeltaPt_jl","lepton-bjet DeltaPt vs. DeltaR",100,0,4.5,100,0,2)

      self.add("DeltaR_jj","jet-jet DeltaR",100,0,4.5)
      self.add("DeltaR_bb","bjet-bjet DeltaR",100,0,4.5)
      self.add("DeltaR_jjbb","jets-bjets DeltaR_jjbb",100,0,4.5)

      self.add("DeltaPhi_jj","jet-jet DeltaPhi",100,0,4.5)
      self.add("DeltaPhi_jj_b2b","jet-jet DeltaPhi",100,0,4.5)
      self.add("DeltaPhi_jl","lepton-jet DeltaPhi",100,0,4.5)
      self.add("DeltaPhi_jjl","lepton-jets DeltaPhi",100,0,4.5)
      self.add("DeltaPhi_bb","bjet-bjet DeltaPhi",100,0,4.5)
      self.add("DeltaPhi_bl","lepton-bjet DeltaPhi",100,0,4.5)
      self.add("DeltaPhi_bbl","lepton-bjets DeltaPhi",100,0,4.5)

      self.add2D("DeltaEtaDeltaPhi_jj","jet-jet DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_jl","lepton-jet combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_j1l","lepton-jet1 combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_j2l","lepton-jet2 combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_j3l","lepton-jet3 combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      #self.add2D("DeltaEtaDeltaPhi_j4l","lepton-jet combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_jjl","lepton-jets combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_bb","bjet-bjet DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_bl","lepton-bjet combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_bbl","lepton-bjets combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)
      self.add2D("DeltaEtaDeltaPhi_jjbb","jets-bjets combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,3.5,50,0,3.2)

      self.add2D("MDeltaPhi_jj_b2b","jet-jet DeltaPhi vs. Mass (Pt>30 GeV)",100,0,200,50,0,3.2)

    # get information
    def process(self, event):
    
        result = { }

        result["M_jj"] = [ ]
        result["M_jj_cut"] = [ ]
        result["M_jj_b2b"] = [ ]
        result["M_jjl"] = [ ]
        result["M_bb"] = [ ]
        result["M_bb_cut"] = [ ]
        result["M_bl"] = [ ]

        result["DeltaPt_jl"] = event.DeltaPt_jl
        result["DeltaRDeltaPt_jl"] = map(lambda R,Pt: [R,Pt], event.DeltaR_jl,event.DeltaPt_jl)

        result["DeltaR_jj"] = [ ]
        result["DeltaR_bb"] = [ ]
        result["DeltaR_jjbb"] = [ ]

        result["DeltaPhi_jj"] = [ ]
        result["DeltaPhi_jj_b2b"] = [ ]
        result["DeltaPhi_jl"] = [ ]
        result["DeltaPhi_jjl"] = [ ]
        result["DeltaPhi_bb"] = [ ]
        result["DeltaPhi_bl"] = [ ]
        result["DeltaPhi_bbl"] = [ ]
        result["DeltaPhi_jjbb"] = [ ]

        result["DeltaEtaDeltaPhi_jj"] = [ ]
        result["DeltaEtaDeltaPhi_jl"] = [ ]
        result["DeltaEtaDeltaPhi_j1l"] = [ ]
        result["DeltaEtaDeltaPhi_j2l"] = [ ]
        result["DeltaEtaDeltaPhi_j3l"] = [ ]
        result["DeltaEtaDeltaPhi_j4l"] = [ ]
        result["DeltaEtaDeltaPhi_jjl"] = [ ]
        result["DeltaEtaDeltaPhi_bb"] = [ ]
        result["DeltaEtaDeltaPhi_bl"] = [ ]
        result["DeltaEtaDeltaPhi_bbl"] = [ ]
        result["DeltaEtaDeltaPhi_jjbb"] = [ ]

        result["MDeltaPhi_jj_b2b"] = [ ]

        bjets = event.bjets30[:3]
        jets = [ j for j in event.cleanedJets30[:8] if j not in bjets[:2] ][:6]
        lepton = None
        p_lepton = TLorentzVector()
        if len(event.leadingLeptons):
            lepton = event.leadingLeptons[0]
            p_lepton.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)

        # jet - jet
        p_jets = [ ]
        p_jjs = [ ]
        for jet in jets:
            p_jets.append(TLorentzVector())
            p_jets[-1].SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

            # jet - lepton
            if lepton:
                DeltaPhi = fold(abs(lepton.Phi - jet.Phi))
                result["DeltaPhi_jl"].append(DeltaPhi)
                result["DeltaEtaDeltaPhi_jl"].append([ abs(lepton.Eta - jet.Eta),
                                                       DeltaPhi ])

        # jet i - lepton
        if lepton:
            p_ji = sorted(p_jets, key=lambda p: TLorentzVector.DeltaR(p,p_lepton))[:4]
            if len(p_ji)>0:
                result["DeltaEtaDeltaPhi_j1l"].append([ abs(lepton.Eta - p_ji[0].Eta()),
                                                   fold(abs(lepton.Phi - p_ji[0].Phi())) ])
                if len(p_ji)>1:
                    result["DeltaEtaDeltaPhi_j2l"].append([ abs(lepton.Eta - p_ji[1].Eta()),
                                                       fold(abs(lepton.Phi - p_ji[1].Phi())) ])
                    if len(p_ji)>2:
                        result["DeltaEtaDeltaPhi_j3l"].append([ abs(lepton.Eta - p_ji[2].Eta()),
                                                           fold(abs(lepton.Phi - p_ji[2].Phi())) ])
                        if len(p_ji)>3:
                            result["DeltaEtaDeltaPhi_j4l"].append([ abs(lepton.Eta - p_ji[3].Eta()),
                                                               fold(abs(lepton.Phi - p_ji[3].Phi())) ])

        # jet comb
        p_jj_b2b = None
        DeltaPhi_b2b = 0 # > pi
        for p1, p2 in combinations(p_jets,2):
            p_jj = p1 + p2
            p_jjs.append( p_jj )
            DeltaPhi = fold(abs(p1.Phi() - p2.Phi()))
            result["M_jj"].append(p_jj.M())
            result["DeltaR_jj"].append(TLorentzVector.DeltaR( p1, p2 ))
            result["DeltaPhi_jj"].append(DeltaPhi)
            result["DeltaEtaDeltaPhi_jj"].append([ abs(p1.Eta() - p2.Eta()),
                                                   DeltaPhi  ])
            
            # jets comb - lepton
            if lepton:
                if (fold(abs(lepton.Phi - p1.Phi())) < 1.5 or \
                    fold(abs(lepton.Phi - p2.Phi())) < 1.5 ) and DeltaPhi > 1:
                    result["M_jj_cut"].append(p_jj.M())
                DeltaPhi = fold(abs(lepton.Phi - p_jj.Phi()))
                result["M_jjl"].append( (p_lepton+p_jj).M() )
                result["DeltaPhi_jjl"].append( DeltaPhi )
                result["DeltaEtaDeltaPhi_jjl"].append([ abs(lepton.Eta - p_jj.Eta()),
                                                        DeltaPhi  ])
            # find best b2b comb
            beta = p_jj.BoostVector()
            q1 = copy(p1)
            q2 = copy(p2)
            q1.Boost(-beta)
            q2.Boost(-beta)
            DeltaPhi = fold(abs(q1.Phi()-q2.Phi()))
            if DeltaPhi > DeltaPhi_b2b:
                p_jj_b2b = copy(p_jj) # .copy() not needed
                DeltaPhi_b2b = DeltaPhi

        if p_jj_b2b:
            result["M_jj_b2b"] = p_jj_b2b.M()
            result["DeltaPhi_jj_b2b"] = DeltaPhi_b2b
            result["MDeltaPhi_jj_b2b"].append([ p_jj_b2b.M(), DeltaPhi_b2b ])

        # bjet - bjet
        p_bjets = [ ]
        DeltaPhi_bj = [ ]
        for bjet in bjets:
            p_bjets.append(TLorentzVector())
            p_bjets[-1].SetPtEtaPhiM(bjet.PT, bjet.Eta, bjet.Phi, bjet.Mass)
            if lepton:
                DeltaPhi = fold(abs(lepton.Phi - bjet.Phi))
                DeltaPhi_bj.append(DeltaPhi)
                result["DeltaPhi_bl"].append(DeltaPhi)
                result["DeltaEtaDeltaPhi_bl"].append([ abs(lepton.Eta - bjet.Eta),
                                                       DeltaPhi  ])
        if lepton and len(DeltaPhi_bj):
            i = min(xrange(len(DeltaPhi_bj)),key=DeltaPhi_bj.__getitem__)
            result["M_bl"].append((p_lepton+p_bjets[i]).M())

        # bjet comb
        for p1, p2 in combinations(p_bjets,2):
            p_bb = p1 + p2
            DeltaPhi = fold(abs(p1.Phi() - p2.Phi()))
            result["M_bb"].append(p_bb.M())
            result["DeltaR_bb"].append(TLorentzVector.DeltaR( p1, p2 ))
            result["DeltaPhi_bb"].append( DeltaPhi )
            result["DeltaEtaDeltaPhi_bb"].append([ abs(p1.Eta() - p2.Eta()),
                                                   DeltaPhi  ])
            if DeltaPhi < 2.1:
                result["M_bb_cut"].append(p_bb.M())
            
            # bjets comb - lepton
            if lepton:
                DeltaPhi = fold(abs(lepton.Phi - p_bb.Phi()))
                result["DeltaPhi_bbl"].append( DeltaPhi )
                result["DeltaEtaDeltaPhi_bbl"].append([ abs(lepton.Eta - p_bb.Eta()),
                                                        DeltaPhi  ])

            # bjets comb - jets comb
            for p_jj in p_jjs:
                result["DeltaR_jjbb"].append(TLorentzVector.DeltaR( p_bb, p_jj ))
                result["DeltaEtaDeltaPhi_jjbb"].append([ abs(p_bb.Eta() - p_jj.Eta()),
                                                    fold(abs(p_bb.Phi() - p_jj.Phi()))  ])
        

        return result




if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], LeptonControlPlots())

