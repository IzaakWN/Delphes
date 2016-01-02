from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
from math import sqrt, pow, cos
from operator import attrgetter
from fold import fold
from copy import copy

# Requirements:
# event.Hs
# event.bHs
# event.MET

tree_vars = [ "Pt_q1","Pt_q2",
              "Pt_b1","Pt_b2",
              "Pt_bb","Pt_bl","Pt_q1l",
              #"Pt_qql", "Pt_qqb",
              "Pt_l","Pt_nu",
              "DeltaR_q1l","DeltaR_q2l",
              "DeltaR_b1l","DeltaR_b2l",
              "DeltaR_bb","DeltaR_qq",
              "DeltaR_qql","DeltaR_qqb",
              #"DeltaPhi_j1lbb",
              #"DeltaPhi_lMET","DeltaPhi_jjlnu",
              "M_bb", "M_qqlnu", "M_qql",
              "M_qqb1", "M_qqb2", "M_b1lnu","M_b2lnu",
              "M_bl", "M_qq", "M_q1l",
              #"MT_lnu","MT_jjlnu"
            ]


class GenControlPlots(BaseControlPlots):
    """A class to create control plots for HH and tt -> bbWW"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="gen", dataset=dataset, mode=mode)



    def beginJob(self):
        
        # declare tree and branches
        self.addTree("gen","Variables for MVA")
        for var in tree_vars:
            self.addBranch("gen",var)

<<<<<<< HEAD
        self.add("H1Pt","leading Higgs or top Pt gen",100,0,800)
        self.add("H1Pz","leading Higgs or top Pz gen",100,0,800)
        self.add("H2Pt","second leading Higgs or top Pt gen",100,0,800)
        self.add("H2Pz","second leading Higgs or top Pz gen",100,0,800)
=======
        self.add("HPt","H Pt gen",100,0,500)
        self.add("HPz","H Pz gen",100,0,500)
        self.add("tPt","top Pt gen",100,0,500)
        self.add("tPz","top Pz gen",100,0,500)
>>>>>>> 92a5b2407e73f5fbbed9c7af887987f88c5e80e3

        self.add("Pt_q1","leading quark Pt gen",100,0,300)
        self.add("Pt_q2","second leading quark Pt gen",100,0,300)
        self.add("Pt_b1","leading bquark Pt gen",100,0,300)
        self.add("Pt_b2","second leading bquark Pt gen",100,0,300)
        self.add("Pt_bb","bquark-bquark Pt gen",100,0,300)
        self.add("Pt_bl","closest bquark-lepton Pt gen",100,0,300)
        self.add("Pt_q1l","bquark-lepton Pt gen",100,0,300)
        #self.add("Pt_qql","quarks-lepton Pt gen",100,0,300)
        #self.add("Pt_qqb","quarks-bquark Pt gen",100,0,300) # bquark farthest away from the lepton
        self.add("Pt_l","lepton Pt gen",100,0,300)
        self.add("Pt_nu","neutrino Pt gen",100,0,300)

<<<<<<< HEAD
        self.add("MET_res","MET resolution gen",100,0,15)
=======
        self.add("MET_res","MET resolution gen",100,0,50)
>>>>>>> 92a5b2407e73f5fbbed9c7af887987f88c5e80e3
        self.add("MET_res_ang","MET angular resolution gen",100,0,4)
        
        self.add("M_qq","quarks Mass gen",100,0,300)
        self.add("M_q1l","closest quark-lepton Mass gen",100,0,300)
        self.add("M_bb","bquarks Mass gen",100,0,300)
        self.add("M_qqlnu","bosonic Higgs Mass gen",100,0,300)
        self.add("M_qql","hadronic top Pt gen",100,0,300)
        self.add("M_qqb1","hadronic top Mass gen",100,0,300) # bquark farthest away from the lepton
        self.add("M_qqb2","hadronic top Mass gen",100,0,300)
        self.add("M_b1lnu","closest bquark-lepton Mass gen",100,0,300)
        self.add("M_b2lnu","closest bquark-lepton Mass gen",100,0,300)
        self.add("M_bl","closest bquark-lepton Mass gen",100,0,300)
        
        self.add("CosTheta0_bb","H->bb restframe decay angle",100,0,3.5)
        #self.add("theta0_bb","H->bb restframe decay angle",100,0,3.5)
        #self.add("theta0_b_z","H->bb restframe decay angle",100,0,3.5)
        #self.add("theta0_bb_z","H->bb restframe decay angle",100,0,3.5)

        self.add("DeltaR_q1l","closest quark-lepton DeltaR",100,0,4)
        self.add("DeltaR_q2l","2nd closest quark-lepton DeltaR",100,0,4)
        self.add("DeltaR_b1l","farthest bquark-lepton DeltaR",100,0,4)
        self.add("DeltaR_b2l","2nd farthest bquark-lepton DeltaR",100,0,4)
        self.add("DeltaR_bl_lep","leptonic top - bquark-lepton DeltaR",100,0,4)
        self.add("DeltaR_bl_had","hadronic top - bquark-lepton DeltaR",100,0,4)
        self.add("DeltaR_bb","bquark-bquark DeltaR",100,0,4)
        self.add("DeltaR_qq","quark-quark DeltaR",100,0,4)
        self.add("DeltaR_qql","quarks-lepton DeltaR",100,0,4)
        self.add("DeltaR_qqb","quarks-bquark DeltaR",100,0,4)

        self.add2D("DeltaEtaDeltaPhi_qq","quark-quark DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_bb","bquark-bquark DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_q1l","closest quark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_q2l","2nd closest quark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b1l","farthest bquark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b2l","2nd farthest bquark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)



    def process(self, event):
        
        result = { }
<<<<<<< HEAD
        result["H1Pt"] = [ ]
        result["H1Pz"] = [ ]
        result["H2Pt"] = [ ]
        result["H2Pz"] = [ ]
        
        higgs = [ ]
=======
        result["HPt"] = [ ]
        result["HPz"] = [ ]
        result["tPt"] = [ ]
        result["tPz"] = [ ]
        
>>>>>>> 92a5b2407e73f5fbbed9c7af887987f88c5e80e3
        leptons = [ ]
        neutrinos = [ ]
        quarks = [ ]
        bquarks = [ ]
        bquark_had = None
        bquark_lep = None
        
        for particle in event.particles:
            
            PID = abs(particle.PID)
            D1 = particle.D1
            D2 = particle.D2
                
            # __top__
            if PID == 6 and 0 <= D1 < len(event.particles) and event.particles[D1] and D1!=D2:
<<<<<<< HEAD
                higgs.append(particle)
=======
                result["tPt"].append(particle.PT)
                result["tPz"].append(abs(particle.Pz))
>>>>>>> 92a5b2407e73f5fbbed9c7af887987f88c5e80e3
                if abs(event.particles[D2].PID) == 5: # b
                    bquarks.append(event.particles[D2])
                elif abs(event.particles[D1].PID) == 5: # b
                    print "Warning in GenControlPlots: b is D1!"
                    bquarks.append(event.particles[D1])
                if abs(event.particles[D1].PID) == 24: # look for daughter particle
                    looking = True
                    while looking:
                        D1 = event.particles[D1].D1
                        if abs(event.particles[D1].PID) in [11,13,15]:
                            bquark_lep = event.particles[D2] # bquark with leptonic W
                            looking = False
                        elif abs(event.particles[D1].PID) in [1,2,3,4,5]:
                            bquark_had = event.particles[D2] # bquark with hadronic W
                            looking = False

            # __W__
            elif PID == 24 and 0 <= D1 < len(event.particles) and event.particles[D1] and D1!=D2: # W
                PID_D1 = abs( event.particles[D1].PID )
                PID_D2 = abs( event.particles[D2].PID )
                if PID_D1 in [11,13,15]: # e, mu, tau
                    leptons.append(event.particles[D1])
                    neutrinos.append(event.particles[D2])
                elif PID_D1 in [1,2,3,4,5]: # d, u, s, c, b
                    quarks.extend([event.particles[D1],event.particles[D2]])
                elif PID_D1 in [12,14,16]: print "Warning: in GenControlPlots: PID_D1 of W is a neutrino!"
        
            # __Higgs__
            elif PID == 25 and 0 <= D1 < len(event.particles) and event.particles[D1] and D1!=D2: # Higgs
                PID_D1 = abs( event.particles[D1].PID )
<<<<<<< HEAD
                higgs.append(particle)
=======
                result["HPt"].append(particle.PT)
                result["HPz"].append(abs(particle.Pz))
>>>>>>> 92a5b2407e73f5fbbed9c7af887987f88c5e80e3
                if PID_D1 == 5: # b
                    bquarks.extend([ event.particles[D1], event.particles[D2] ])

        p_q = [ ]
        if len(quarks) == 2:
            for q in quarks:
                p_q.append(TLV())
                p_q[-1].SetPtEtaPhiM(q.PT, q.Eta, q.Phi, q.Mass)
        else: return { } # make code faster by ignoring uninteresting events
        
        p_b = [ ]
        if len(bquarks) == 2:
            for b in bquarks:
                p_b.append(TLV())
                p_b[-1].SetPtEtaPhiM(b.PT, b.Eta, b.Phi, b.Mass)
        else: return { } # make code faster by ignoring uninteresting events

        if len(leptons) == 1 and len(neutrinos) == 1:
            lepton = leptons[0]
            neutrino = neutrinos[0]
            p_l = TLV()
            p_nu = TLV()
            p_l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
            p_nu.SetPtEtaPhiM(neutrino.PT, neutrino.Eta, neutrino.Phi, neutrino.Mass)
            result["Pt_l"] = lepton.PT
            result["Pt_nu"] = neutrino.PT
            result["MET_res"] = abs(event.met[0].MET-neutrino.PT)/neutrino.PT
            result["MET_res_ang"] = fold(abs( event.met[0].Phi-neutrino.Phi ))
            
<<<<<<< HEAD
            if len(higgs)==2: # higgs or top
                [result["H1Pt"],result["H2Pt"]] = sorted([higgs[0].PT,higgs[1].PT],reverse=True)
                [result["H1Pz"],result["H2Pz"]] = sorted([abs(higgs[0].Pz),abs(higgs[1].Pz)],reverse=True)
=======
>>>>>>> 92a5b2407e73f5fbbed9c7af887987f88c5e80e3
            
            if p_q and p_b:

                [p_q1,p_q2] = sorted(p_q, key = lambda p: TLV.DeltaR(p,p_l))[:2]
                [p_b1,p_b2] = sorted(p_b, key = lambda p: TLV.DeltaR(p,p_l), reverse=True)[:2] # farthest
                p_qq = p_q1+p_q2
                p_bb = p_b1+p_b2

                result["Pt_q1"]  = p_q1.Pt()
                result["Pt_q2"]  = p_q2.Pt()
                result["Pt_b1"]  = p_b1.Pt()
                result["Pt_b2"]  = p_b2.Pt()
                result["Pt_bb"]  = p_bb.Pt()
                result["Pt_q1l"] = (p_q1+p_l).Pt()
                result["Pt_bl"]  = (p_b2+p_l).Pt()

                result["M_qq"]    =  p_qq.M()
                result["M_q1l"]   = (p_q1+p_l).M()
                result["M_bb"]    =  p_bb.M()
                result["M_qqlnu"] = (p_qq+p_l+p_nu).M()
                result["M_qql"]   = (p_qq+p_l).M()
                result["M_qqb1"]   = (p_qq+p_b1).M()
                result["M_qqb2"]   = (p_qq+p_b2).M()
                result["M_bl"]    = (p_b2+p_l).M()
                result["M_b1lnu"]  = (p_b1+p_l+p_nu).M()
                result["M_b2lnu"]  = (p_b2+p_l+p_nu).M()

                q = copy(p_b1)
                beta = p_bb.BoostVector()
                q.Boost(-beta) # boost b-jet four-momentum back to restframe
                q3 = q.Vect()
                p_bb3 = p_bb.Vect()
                result["CosTheta0_bb"] = p_bb3.Dot(q3) / p_bb3.Mag() / q3.Mag() # cos(theta)
                #result["theta0_bb"] = q.Angle(p_bb.Vect())
                #pz = TLV(0,0,1,0)
                #result["theta0_b_z"] = q.Angle(pz.Vect())
                #result["theta0_bb_z"] = p_bb.Angle(pz.Vect())

                result["DeltaR_q1l"] = TLV.DeltaR(p_q1,p_l)
                result["DeltaR_q2l"] = TLV.DeltaR(p_q2,p_l)
                result["DeltaR_b1l"] = TLV.DeltaR(p_b1,p_l)
                result["DeltaR_b2l"] = TLV.DeltaR(p_b2,p_l)
                result["DeltaR_bb"]  = TLV.DeltaR(p_b1,p_b2)
                result["DeltaR_qq"]  = TLV.DeltaR(p_q1,p_q2)
                result["DeltaR_qql"] = TLV.DeltaR(p_qq,p_l)
                result["DeltaR_qqb"] = TLV.DeltaR(p_qq,p_b1)

                result["DeltaEtaDeltaPhi_b1l"] = [[ abs(lepton.Eta - p_b1.Eta()),
                                               fold(abs(lepton.Phi - p_b1.Phi())) ]]
                result["DeltaEtaDeltaPhi_b2l"] = [[ abs(lepton.Eta - p_b2.Eta()),
                                               fold(abs(lepton.Phi - p_b2.Phi())) ]]
                result["DeltaEtaDeltaPhi_bb"] = [[ abs(bquarks[0].Eta - bquarks[1].Eta),
                                              fold(abs(bquarks[0].Phi - bquarks[1].Phi)) ]]

                result["DeltaEtaDeltaPhi_q1l"] = [[ abs(lepton.Eta - p_q1.Eta()),
                                               fold(abs(lepton.Phi - p_q1.Phi())) ]]
                result["DeltaEtaDeltaPhi_q2l"] = [[ abs(lepton.Eta - p_q2.Eta()),
                                               fold(abs(lepton.Phi - p_q2.Phi())) ]]
                result["DeltaEtaDeltaPhi_qq"] = [[ abs(quarks[0].Eta - quarks[1].Eta),
                                              fold(abs(quarks[0].Phi - quarks[1].Phi)) ]]
                
                if bquark_had and bquark_lep:
                    p_had = TLV()
                    p_lep = TLV()
                    p_lep.SetPtEtaPhiM(bquark_lep.PT, bquark_lep.Eta, bquark_lep.Phi, bquark_lep.Mass)
                    p_had.SetPtEtaPhiM(bquark_had.PT, bquark_had.Eta, bquark_had.Phi, bquark_had.Mass)
                    result["DeltaR_bl_had"] = TLV.DeltaR(p_had,p_l)
                    result["DeltaR_bl_lep"] = TLV.DeltaR(p_lep,p_l)

        else: return { } # make code faster by ignoring uninteresting events
            

        result["gen"] = [ ]
        for var in tree_vars:
            if var in result:
                result["gen"].append(result[var])
            else: # if one variable does not exist for this event, no tree
                del result["gen"]
                break
        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], GenControlPlots())


