from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
from math import sqrt, pow, cos
from operator import attrgetter
from fold import fold

# Requirements:
# event.Hs
# event.bHs
# event.MET

labels = ["Wlnu","Wjj","Wbb","Hbb","HWW","HHbbWW","ttbbWW",\
          "b1","b2","nu"]#,"q","l"] # note "l" is only charged lepton
titles = ["Wlnu","Wjj","Wbb","Hbb","HWW","HHbbWW","ttbbWW",\
          "b1","b2","neutrinos"]#,"quarks","leptons","electrons","muons","taus"]
vars = ["Pt","Eta","Phi","M"]


class GenControlPlots(BaseControlPlots):
    """A class to create control plots for HH and tt -> bbWW"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="gen", dataset=dataset, mode=mode)



    def beginJob(self):
        
        self.add("NWlnu","Wlnu multiplicity gen",5,0,5)
        self.add("NWjj","Wjj multiplicity gen",10,0,10)
        self.add("NHbb","Hbb multiplicity gen",10,0,10)
        self.add("Ntb","tb multiplicity gen",10,0,10)
        
        self.add("NVirtualWs","virtual W's multiplicity gen",5,0,5)
        
        self.add2D("WWM","Wqq Mass vs. Wlnu Mass gen",100,0,150,100,0,150)
        self.add2D("WWMt","Wqq Mass vs. Wlnu Mt gen",100,0,150,100,0,150)
        self.add2D("WjjWjjM","Wqq Mass vs. Wqq Mass gen",100,0,100,100,0,150)
        self.add2D("WlnuWlnuM","Wlnu Mass vs. Wlnu Mass gen",100,0,150,100,0,150)
        self.add2D("WlnuWlnuMt","Wlnu Mt vs. Wlnu Mt gen",100,0,150,100,0,150)
        self.add2D("HHM","Hbb Mass vs. HWW Mass gen",100,0,150,100,0,150)
        self.add2D("bbWWM","bb Mass vs. WW Mass gen",100,0,250,100,0,250)
        
        self.add("DeltaR_qq","quark-quark DeltaR",100,0,4)
        self.add("DeltaR_q1l","closest quark-lepton DeltaR",100,0,4)
        self.add("DeltaR_q2l","2nd closest quark-lepton DeltaR",100,0,4)
        self.add("DeltaR_bb","bquark-bquark DeltaR",100,0,4)
        self.add("DeltaR_b1l","farthest bquark-lepton DeltaR",100,0,4)
        self.add("DeltaR_b2l","2nd farthest bquark-lepton DeltaR",100,0,4)
        
        self.add("DeltaPhi_qq","coupled quarks DeltaPhi gen",100,0,3.5)
        
        self.add2D("DeltaEtaDeltaPhi_qq","quark-quark DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_bb","bquark-bquark DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_q1l","closest quark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_q2l","2nd closest quark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b1l","farthest bquark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)
        self.add2D("DeltaEtaDeltaPhi_b2l","2nd farthest bquark-lepton DeltaPhi vs. DeltaEta",50,0,3.5,50,0,3.2)

        for i in range(len(labels)):
            label = labels[i]
            title = titles[i]
            self.add(label+"Eta",title+" Eta gen",100,-5,5)
            self.add(label+"Phi",title+" Phi gen",100,-5,5)
            if label=="Wlnu":
                self.add(label+"Pt",title+" Pt gen",100,0,600)
                self.add(label+"M",title+" Mass gen",100,0,200)
                self.add(label+"Mt",title+" Mt gen",100,0,250)
                self.add(label+"Mt_Wjjonshell",title+" with Wjj on-shell Mt gen",100,0,250)
            elif label=="HWW":
                self.add(label+"Pt",title+" Pt gen",100,0,600)
                self.add(label+"M",title+" Mass gen",200,0,800)
            elif label in ["HHbbWW","ttbbWW"]:
                self.add(label+"Pt",title+" Pt gen",100,0,600)
                self.add(label+"M",title+" Mass gen",150,0,1500)
            elif label in ["b1","b2","nu"]:#,"q","l","e","mu","tau"]:
                self.add(label+"Pt",title+" Pt gen",100,0,300)
                self.add(label+"M",title+" Mass gen",50,0,5)
            else:
                self.add(label+"Pt",title+" Pt gen",100,0,600)
                self.add(label+"M",title+" Mass gen",100,0,300)



    def process(self, event):
        
        result = { }
        
        leptons = [ ]
        neutrinos = [ ]
        #quark1s = [ ]
        quarks = [ ]
        
        nHiggs = 0
        nt = 0
        nW = 0
        nWlnu = 0
        nWjj = 0
        nHbb = 0
        ntb = 0
        nb = 0
        b = []
        W = []
        
        nVirtualWs = 0
        nVirtualWjjs = 0
        for label in labels:
            for var in vars:
                result[label+var] = [ ]
        result["WlnuMt"] = [ ]
        result["DeltaPhi_qq"] = [ ]

        p_Hbb = TLV(0,0,0,0)
        p_HWW = TLV(0,0,0,0)
        p_t = [TLV(0,0,0,0), TLV(0,0,0,0)] # four-momenta of the top quarks
        
        for particle in event.particles:
            
            PID = abs(particle.PID)
            D1 = particle.D1
            D2 = particle.D2

            ## __lepton__
            #if PID in [11,13,15]:#,15]: # e, mu, tau
                #result["lPt"].append( particle.PT )
                #result["lEta"].append( particle.Eta )
                #result["lPhi"].append( particle.Phi )
                #result["lM"].append( particle.Mass )
                #nLeptons += 1
                
            # top
            if PID == 6 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2:
                nt += 1
                p_t[nt-1].SetPtEtaPhiM(particle.PT, particle.Eta, particle.Phi, particle.Mass)
                if abs(event.particles[D2].PID) == 5: # b
                    ntb+=1
                    b.append(event.particles[D2])
                    W.append(event.particles[D1])
                elif abs(event.particles[D1].PID) == 5: # b
                    print "Warning in GenControlPlots: b is D1!"
                    ntb+=1
                    b.append(event.particles[D1])
                    W.append(event.particles[D2])

            # __W__
            if PID == 24 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # W
                nW += 1
                PID_D1 = abs( event.particles[D1].PID )
                PID_D2 = abs( event.particles[D2].PID )
                if PID_D1 in [11,13,15]: # e, mu, tau
                    leptons.append(event.particles[D1])
                    neutrinos.append(event.particles[D2])
                    nWlnu+=1
                    result["WlnuPt"].append( particle.PT )
                    result["WlnuEta"].append( particle.Eta )
                    result["WlnuPhi"].append( particle.Phi )
                    result["WlnuM"].append( particle.Mass )
                    result["WlnuMt"].append(sqrt( 2 * event.particles[D1].PT * event.particles[D2].PT * \
                                                (1-cos( event.particles[D1].Phi - event.particles[D2].Phi ))))
                    if abs(80.4-particle.Mass) > 10: # check if W is virtual
                        nVirtualWs += 1
                    result["nuPt"].append( event.particles[D2].PT )
                    result["nuEta"].append( event.particles[D2].Eta )
                    result["nuPhi"].append( event.particles[D2].Phi )
                    result["nuM"].append( event.particles[D2].Mass )
                elif PID_D1 in [1,2,3,4,5]: # d, u, s, c, b
                    nWjj+=1
                    #quark1s.append(event.particles[D1])
                    quarks.extend([event.particles[D1],event.particles[D2]])
                    result["DeltaPhi_qq"].append(fold(abs(event.particles[D1].Phi-event.particles[D2].Phi)))
                    result["WjjPt"].append( particle.PT )
                    result["WjjEta"].append( particle.Eta )
                    result["WjjPhi"].append( particle.Phi )
                    result["WjjM"].append( particle.Mass )
                    if abs(80.4-particle.Mass) > 10:
                        nVirtualWs += 1
                        nVirtualWjjs += 1
                elif PID_D1 in [12,14,16]: print "Warning: in GenControlPlots: PID_D1 of W is a neutrino!"
        
            # __Higgs__
            elif PID == 25 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # Higgs
                PID_D1 = abs( event.particles[D1].PID )
                nHiggs+=1
                if PID_D1 == 5: # b
                    nHbb+=1
                    b.extend([ event.particles[D1], event.particles[D2] ])
                    p_Hbb.SetPtEtaPhiM(particle.PT, particle.Eta, particle.Phi, particle.Mass)
                    result["HbbPt"].append( particle.PT )
                    result["HbbEta"].append( particle.Eta )
                    result["HbbPhi"].append( particle.Phi )
                    result["HbbM"].append( particle.Mass )
                if PID_D1 in [24]: # W
                    W.extend([ event.particles[D1], event.particles[D2] ])
                    p_HWW.SetPtEtaPhiM(particle.PT, particle.Eta, particle.Phi, particle.Mass)
                    result["HWWPt"].append( particle.PT )
                    result["HWWEta"].append( particle.Eta )
                    result["HWWPhi"].append( particle.Phi )
                    result["HWWM"].append( particle.Mass )

        if len(b)==2:
            if abs(b[0].Eta) > abs(b[1].Eta): # order b-jets w.r.t. to Eta
                b1 = b[1]
                b2 = b[0]
            else:
                b1 = b[0]
                b2 = b[1]
            result["b1Pt"].append( b1.PT )
            result["b1Eta"].append( b1.Eta )
            result["b1Phi"].append( b1.Phi )
            result["b1M"].append( b1.Mass )
            result["b2Pt"].append( b2.PT )
            result["b2Eta"].append( b2.Eta )
            result["b2Phi"].append( b2.Phi )
            result["b2M"].append( b2.Mass )

        if nt == 2: # tt
            q_tt = p_t[0] + p_t[1]
            result["ttbbWWPt"].append( q_tt.Pt() )
            result["ttbbWWEta"].append( q_tt.Eta() )
            result["ttbbWWPhi"].append( q_tt.Phi() )
            result["ttbbWWM"].append( q_tt.M() )

        if nHiggs == 2:
            q_HH = p_Hbb + p_HWW
            result["HHbbWWPt"].append( q_HH.Pt() )
            result["HHbbWWEta"].append( q_HH.Eta() )
            result["HHbbWWPhi"].append( q_HH.Phi() )
            result["HHbbWWM"].append( q_HH.M() )
            if len(result["HWWM"]) and len(result["HbbM"]): # needed when relaxed cut 4 jets pT < 20 GeV 
                result["HHM"] = [[ result["HWWM"][0],  result["HbbM"][0] ]]
#            result["HHMt"] = [[ result["HWWM"][0],  result["HbbM"][0] ]]

        # __WW_2D-plots__
        if len( result["WlnuM"] ) == 1 and len( result["WjjM"] ) == 1: # monoleptonic
            result["WWM"]  = [[ result["WlnuM"][0],  result["WjjM"][0] ]]
            result["WWMt"] = [[ result["WlnuMt"][0], result["WjjM"][0] ]]
            if nVirtualWjjs == 0:
                result["WlnuMt_Wjjonshell"] = result["WlnuMt"]
        elif len( result["WlnuM"] ) == 0 and len( result["WjjM"] ) == 2: # hadronic
            result["WjjWjjM"] = [[ result["WjjM"][0], result["WjjM"][1] ]]
        elif len( result["WlnuM"] ) == 2 and len( result["WjjM"] ) == 0: # dileptonic
            result["WlnuWlnuM"]  = [[ result["WlnuM"][0],  result["WlnuM"][1]  ]]
            result["WlnuWlnuMt"] = [[ result["WlnuMt"][0], result["WlnuMt"][1] ]]
        else: print "Warning! GenControlPlots.py: No WW 2D-plot!"

        # __bbWW_2D-plots__
        p_b = [TLV(), TLV()]
        if len(b) == 2:
            p_b[0].SetPtEtaPhiM(b[0].PT, b[0].Eta, b[0].Phi, b[0].Mass)
            p_b[1].SetPtEtaPhiM(b[1].PT, b[1].Eta, b[1].Phi, b[1].Mass)
            result["DeltaR_bb"] = TLV.DeltaR(p_b[0],p_b[1])
            result["DeltaEtaDeltaPhi_bb"] = [[ abs(b[0].Eta - b[1].Eta),
                                               fold(abs(b[0].Phi - b[1].Phi)) ]]
        if len(b) == 2 and len(W) > 1:
            q_W = [TLV(), TLV()]
            q_W[0].SetPtEtaPhiM(W[0].PT, W[0].Eta, W[0].Phi, W[0].Mass)
            q_W[1].SetPtEtaPhiM(W[1].PT, W[1].Eta, W[1].Phi, W[1].Mass)
            result["bbWWM"]  = [[ (p_b[0]+p_b[1]).M(),  (q_W[0]+q_W[1]).M() ]]

        p_q = [ ]
        if quarks:
            for quark in quarks:
                p_q.append(TLV())
                p_q[-1].SetPtEtaPhiM(quark.PT, quark.Eta, quark.Phi, quark.Mass)
            result["DeltaR_qq"] = TLV.DeltaR(p_q[0],p_q[1])
            result["DeltaEtaDeltaPhi_qq"] = [[ abs(quarks[0].Eta - quarks[1].Eta),
                                               fold(abs(quarks[0].Phi - quarks[1].Phi)) ]]

        if leptons:
            lepton = max(leptons, key=attrgetter('PT'))
            p_lepton = TLV()
            p_lepton.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)

            if quarks:
#                DeltaR_ql = sorted([ TLV.DeltaR(p_lepton,p) for p in p_q ])[:2]
                [p_q1,p_q2] = sorted(p_q, key = lambda p: TLV.DeltaR(p,p_lepton))[:2]
                result["DeltaR_q1l"] = TLV.DeltaR(p_lepton,p_q1)
                result["DeltaR_q2l"] = TLV.DeltaR(p_lepton,p_q2)
                result["DeltaEtaDeltaPhi_q1l"] = [[ abs(lepton.Eta - p_q1.Eta()),
                                               fold(abs(lepton.Phi - p_q1.Phi())) ]]
                result["DeltaEtaDeltaPhi_q2l"] = [[ abs(lepton.Eta - p_q2.Eta()),
                                               fold(abs(lepton.Phi - p_q2.Phi())) ]]
                                               
            if len(b)>1:
                [p_b1,p_b2] = sorted(p_b, key = lambda p: TLV.DeltaR(p,p_lepton), reverse=True)[:2] # farthest
                result["DeltaR_b1l"] = TLV.DeltaR(p_lepton,p_b1)
                result["DeltaR_b2l"] = TLV.DeltaR(p_lepton,p_b2)
                result["DeltaEtaDeltaPhi_b1l"] = [[ abs(lepton.Eta - p_b1.Eta()),
                                               fold(abs(lepton.Phi - p_b1.Phi())) ]]
                result["DeltaEtaDeltaPhi_b2l"] = [[ abs(lepton.Eta - p_b2.Eta()),
                                               fold(abs(lepton.Phi - p_b2.Phi())) ]]

        result["NWlnu"] = nWlnu
        result["NWjj"] = nWjj
        result["NHbb"] = nHbb
        result["Ntb"] = ntb
        result["NVirtualWs"] = nVirtualWs
        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], GenControlPlots())


