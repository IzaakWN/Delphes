from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector
from math import sqrt, pow, cos

# Requirements:
# event.Hs
# event.bHs
# event.MEt

labels = ["Wlnu","Wjj","Wbb","Hbb","HWW","HHbbWW","ttbbWW",\
          "b1","b2","q","nu","l","e","mu","tau"] # note "l" is only charged lepton
titles = ["Wlnu","Wjj","Wbb","Hbb","HWW","HHbbWW","ttbbWW",\
          "b1","b2","quarks","neutrinos","leptons","electrons","muons","taus"]
vars = ["Pt","Eta","Phi","M"]


class GenControlPlots(BaseControlPlots):
    """A class to create control plots for HH and tt -> bbWW"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="Hmet", dataset=dataset, mode=mode)



    def beginJob(self):
        
        self.add("NLeptons","leptons multiplicity gen",10,0,10)
        self.add("NElectrons","electrons multiplicity gen",10,0,10)
        self.add("NMuons","muons multiplicity gen",10,0,10)
        self.add("NTaus","taus multiplicity gen",10,0,10)
        self.add("NHiggs","Higgs multiplicity gen",10,0,10)
        self.add("NW","W's multiplicity gen",10,0,10)
        self.add("Nb","bottom quarks multiplicity gen",10,0,10)
        self.add("Nt","top quarks multiplicity gen",10,0,10)
        
        self.add("NWlnu","Wlnu multiplicity gen",5,0,5)
        self.add("NWjj","Wjj multiplicity gen",10,0,10)
        self.add("NHbb","Hbb multiplicity gen",10,0,10)
        self.add("Ntb","tb multiplicity gen",10,0,10)
        
        self.add("WDPID","W's daughters PID gen",30,0,30)
        self.add("bMPID","b-quark's mother PID gen",12000,-3000,3000)
        self.add("tDPID","t's daughters PID gen",30,0,30)
        
        self.add("NVirtualWs","virtual W's multiplicity gen",5,0,5)
        
        self.add2D("WWM","Wqq Mass vs. Wlnu Mass gen",100,0,150,100,0,150)
        self.add2D("WWMt","Wqq Mass vs. Wlnu Mt gen",100,0,150,100,0,150)
        self.add2D("WjjWjjM","Wqq Mass vs. Wqq Mass gen",100,0,100,100,0,150)
        self.add2D("WlnuWlnuM","Wlnu Mass vs. Wlnu Mass gen",100,0,150,100,0,150)
        self.add2D("WlnuWlnuMt","Wlnu Mt vs. Wlnu Mt gen",100,0,150,100,0,150)
        self.add2D("HHM","Hbb Mass vs. HWW Mass gen",100,0,150,100,0,150)
        self.add2D("bbWWM","bb Mass vs. WW Mass gen",100,0,250,100,0,250)


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
            if label=="HWW":
                self.add(label+"Pt",title+" Pt gen",100,0,600)
                self.add(label+"M",title+" Mass gen",200,0,800)
            elif label in ["HHbbWW","ttbbWW"]:
                self.add(label+"Pt",title+" Pt gen",100,0,600)
                self.add(label+"M",title+" Mass gen",150,0,1500)
            elif label in ["b1","b2","q","nu","l","e","mu","tau"]:
                self.add(label+"Pt",title+" Pt gen",100,0,300)
                self.add(label+"M",title+" Mass gen",50,0,5)
            else:
                self.add(label+"Pt",title+" Pt gen",100,0,600)
                self.add(label+"M",title+" Mass gen",100,0,300)



    def process(self, event):
        
        result = { }
        
        nHiggs = 0
        nt = 0
        nW = 0
        nLeptons = 0
        nMuons = 0
        nElectrons = 0
        nTaus = 0
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
        result["WDPID"] = [ ]
        result["bMPID"] = [ ]
        result["tDPID"] = [ ]

        p_Hbb = TLorentzVector(0,0,0,0)
        p_HWW = TLorentzVector(0,0,0,0)
        p_t = [TLorentzVector(0,0,0,0), TLorentzVector(0,0,0,0)] # four-momenta of the top quarks
        
        for particle in event.particles:
            
            PID = abs(particle.PID)
            D1 = particle.D1
            D2 = particle.D2

            # __lepton__
            if PID in [11,13,15]:#,15]: # e, mu, tau
                result["lPt"].append( particle.PT )
                result["lEta"].append( particle.Eta )
                result["lPhi"].append( particle.Phi )
                result["lM"].append( particle.Mass )
                nLeptons += 1
                if PID == 11:
                    nElectrons += 1
                    result["ePt"].append( particle.PT )
                    result["eEta"].append( particle.Eta )
                    result["ePhi"].append( particle.Phi )
                    result["eM"].append( particle.Mass )
                elif PID == 13:
                    nMuons += 1
                    result["muPt"].append( particle.PT )
                    result["muEta"].append( particle.Eta )
                    result["muPhi"].append( particle.Phi )
                    result["muM"].append( particle.Mass )
                elif PID == 15:
                    nTaus += 1
                    result["tauPt"].append( particle.PT )
                    result["tauEta"].append( particle.Eta )
                    result["tauPhi"].append( particle.Phi )
                    result["tauM"].append( particle.Mass )

            # __quark__
            if PID in [1,2,3,4,6]: # d, u, s, c, t   Note: no b-quark!!!
                result["qPt"].append( particle.PT )
                result["qEta"].append( particle.Eta )
                result["qPhi"].append( particle.Phi )
                result["qM"].append( particle.Mass )
                
                # top
                if PID == 6 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2:
                    nt += 1
                    p_t[nt-1].SetPtEtaPhiM(particle.PT, particle.Eta, particle.Phi, particle.Mass)
                    result["tDPID"].extend( [abs(event.particles[D1].PID), abs(event.particles[D2].PID) ])
                    if abs(event.particles[D2].PID) == 5: # b
                        ntb+=1
                        b.append(event.particles[D2])
                        W.append(event.particles[D1])
                    elif abs(event.particles[D1].PID) == 5: # b
                        print "Warning in GenControlPlots: b is D1!"
                        ntb+=1
                        b.append(event.particles[D1])
                        W.append(event.particles[D2])

            
            # __b-quark__
            elif PID == 5:
                nb += 1
                M1 = particle.M1
                if M1>=0 and M1<len(event.particles) and event.particles[M1]:
                    result["bMPID"].append( abs(event.particles[M1].PID) )

            # __W__
            if PID == 24 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # W
                nW += 1
                PID_D1 = abs( event.particles[D1].PID )
                PID_D2 = abs( event.particles[D2].PID )
                result["WDPID"].extend( [PID_D1, PID_D2] ) # all W daughters
                if PID_D1 in [11,13,15]: # e, mu, tau
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
#            if len(result["HWWM"]) and len(result["HbbM"]):
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
        if len(b) == 2 and len(W) > 1:
            q_b = [TLorentzVector(), TLorentzVector()]
            q_W = [TLorentzVector(), TLorentzVector()]
            for i in [0,1]:
                q_b[i].SetPtEtaPhiM(b[i].PT, b[i].Eta, b[i].Phi, b[i].Mass)
                q_W[i].SetPtEtaPhiM(W[i].PT, W[i].Eta, W[i].Phi, W[i].Mass)
            result["bbWWM"]  = [[ (q_b[0]+q_b[1]).M(),  (q_W[0]+q_W[1]).M() ]]

        result["NLeptons"] = nLeptons
        result["NElectrons"] = nElectrons
        result["NMuons"] = nMuons
        result["NTaus"] = nTaus
        result["NHiggs"] = nHiggs
        result["NW"] = nW
        result["NWlnu"] = nWlnu
        result["NWjj"] = nWjj
        result["NHbb"] = nHbb
        result["Nb"] = nb
        result["Nt"] = nt
        result["Ntb"] = ntb
        result["NVirtualWs"] = nVirtualWs
        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], GenControlPlots())

