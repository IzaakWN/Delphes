from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
from math import sqrt, pow, cos
from operator import attrgetter
from fold import fold

# Requirements:
# event.Hs
# event.bHs
# event.MET


class GenControlPlots(BaseControlPlots):
    """A class to create control plots for HH and tt -> bbWW"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="gen", dataset=dataset, mode=mode)



    def beginJob(self):
        
        self.add("DeltaR_qq","quark-quark DeltaR",100,0,4)
        self.add("DeltaR_q1l","closest quark-lepton DeltaR",100,0,4)
        self.add("DeltaR_q2l","2nd closest quark-lepton DeltaR",100,0,4)
        self.add("DeltaR_bb","bquark-bquark DeltaR",100,0,4)
        self.add("DeltaR_b1l","farthest bquark-lepton DeltaR",100,0,4)
        self.add("DeltaR_b2l","2nd farthest bquark-lepton DeltaR",100,0,4)
        
        self.add2D("DeltaEtaDeltaPhi_qq","quark-quark DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_bb","bquark-bquark DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_q1l","closest quark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_q2l","2nd closest quark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b1l","farthest bquark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b2l","2nd farthest bquark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)



    def process(self, event):
        
        result = { }
        
        leptons = [ ]
#        neutrinos = [ ]
        quarks = [ ]
        bquarks = []
        
        for particle in event.particles:
            
            PID = abs(particle.PID)
            D1 = particle.D1
            D2 = particle.D2
                
            # __top__
            if PID == 6 and 0 <= D1 < len(event.particles) and event.particles[D1] and D1!=D2:
                if abs(event.particles[D2].PID) == 5: # b
                    bquarks.append(event.particles[D2])
                elif abs(event.particles[D1].PID) == 5: # b
                    print "Warning in GenControlPlots: b is D1!"
                    bquarks.append(event.particles[D1])

            # __W__
            if PID == 24 and 0 <= D1 < len(event.particles) and event.particles[D1] and D1!=D2: # W
                PID_D1 = abs( event.particles[D1].PID )
                PID_D2 = abs( event.particles[D2].PID )
                if PID_D1 in [11,13,15]: # e, mu, tau
                    leptons.append(event.particles[D1])
#                    neutrinos.append(event.particles[D2])
                elif PID_D1 in [1,2,3,4,5]: # d, u, s, c, b
                    quarks.extend([event.particles[D1],event.particles[D2]])
                elif PID_D1 in [12,14,16]: print "Warning: in GenControlPlots: PID_D1 of W is a neutrino!"
        
            # __Higgs__
            elif PID == 25 and 0 <= D1 < len(event.particles) and event.particles[D1] and D1!=D2: # Higgs
                PID_D1 = abs( event.particles[D1].PID )
                if PID_D1 == 5: # b
                    bquarks.extend([ event.particles[D1], event.particles[D2] ])

        p_q = [ ]
        if len(quarks) == 2:
            for q in quarks:
                p_q.append(TLV())
                p_q[-1].SetPtEtaPhiM(q.PT, q.Eta, q.Phi, q.Mass)
            result["DeltaR_qq"] = TLV.DeltaR(p_q[0],p_q[1])
            result["DeltaEtaDeltaPhi_qq"] = [[ abs(quarks[0].Eta - quarks[1].Eta),
                                               fold(abs(quarks[0].Phi - quarks[1].Phi)) ]]
        else: return { } # make code faster by ignoring uninteresting events
        
        p_b = [ ]
        if len(bquarks) == 2:
            for b in bquarks:
                p_b.append(TLV())
                p_b[-1].SetPtEtaPhiM(b.PT, b.Eta, b.Phi, b.Mass)
            result["DeltaR_bb"] = TLV.DeltaR(p_b[0],p_b[1])
            result["DeltaEtaDeltaPhi_bb"] = [[ abs(bquarks[0].Eta - bquarks[1].Eta),
                                               fold(abs(bquarks[0].Phi - bquarks[1].Phi)) ]]
        else: return { } # make code faster by ignoring uninteresting events

        if len(leptons) == 1:
            lepton = leptons
            p_l = TLV()
            p_l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)

            if quarks:
                [p_q1,p_q2] = sorted(p_q, key = lambda p: TLV.DeltaR(p,p_l))[:2]
                result["DeltaR_q1l"] = TLV.DeltaR(p_l,p_q1)
                result["DeltaR_q2l"] = TLV.DeltaR(p_l,p_q2)
                result["DeltaEtaDeltaPhi_q1l"] = [[ abs(lepton.Eta - p_q1.Eta()),
                                               fold(abs(lepton.Phi - p_q1.Phi())) ]]
                result["DeltaEtaDeltaPhi_q2l"] = [[ abs(lepton.Eta - p_q2.Eta()),
                                               fold(abs(lepton.Phi - p_q2.Phi())) ]]
        else: return { } # make code faster by ignoring uninteresting events
                                               
            if bquarks:
                [p_b1,p_b2] = sorted(p_b, key = lambda p: TLV.DeltaR(p,p_l), reverse=True)[:2] # farthest
                result["DeltaR_b1l"] = TLV.DeltaR(p_l,p_b1)
                result["DeltaR_b2l"] = TLV.DeltaR(p_l,p_b2)
                result["DeltaEtaDeltaPhi_b1l"] = [[ abs(lepton.Eta - p_b1.Eta()),
                                               fold(abs(lepton.Phi - p_b1.Phi())) ]]
                result["DeltaEtaDeltaPhi_b2l"] = [[ abs(lepton.Eta - p_b2.Eta()),
                                               fold(abs(lepton.Phi - p_b2.Phi())) ]]
        else: return { } # make code faster by ignoring uninteresting events

        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], GenControlPlots())


