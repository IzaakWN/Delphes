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
        
        self.add("NHiggs","Higgs multiplicity gen",10,0,10)
        self.add("NW","W's multiplicity gen",10,0,10)
        self.add("NLeptons","leptons multiplicity gen",10,0,10)
        self.add("NElectrons","electrons multiplicity gen",10,0,10)
        self.add("NMuons","muons multiplicity gen",10,0,10)
        self.add("NTaus","taus multiplicity gen",10,0,10)
        self.add("Nb","b-quarks multiplicity gen",10,0,10)
        self.add("bMPID","b-quark's mother PID gen",12000,-3000,3000)
        
        self.add("NWlnu","leptons from Wlnu multiplicity gen",5,0,5) # note: no nu's
        self.add("NWenu","electrons from Wlnu multiplicity gen",10,0,5)
        self.add("NWmunu","muons from Wlnu multiplicity gen",5,0,5)
        self.add("NWtaunu","taus from Wlnu multiplicity gen",5,0,5)
        
        self.add("NHb","b's from H multiplicity gen",10,0,10)
        self.add("Ntb","b's from t multiplicity gen",10,0,10)
        self.add("NWq","quarks from W multiplicity gen",10,0,10)
        
        self.add("NVirtualWs","virtual W's multiplicity gen",5,0,5)
        self.add("WlnuPID","Wlnu's daughters PID gen",12,10,22)
        self.add("WDPID","W's daughters PID gen",30,0,30)
        self.add("tDPID","t's daughters PID gen",30,0,30)
        
        self.add2D("WWM","Wlnu vs. Wqq Mass gen",100,0,150,100,0,150)
        self.add2D("WWMt","Wlnu Mt vs. Wqq Mass gen",100,0,150,100,0,150)
        self.add2D("WjjWjjM","Wqq vs. Wqq Mass gen",100,0,100,100,0,150)
        self.add2D("WlnuWlnuM","Wlnu vs. Wlnu Mass gen",100,0,150,100,0,150)
        self.add2D("WlnuWlnuMt","Wlnu vs. Wlnu Mt gen",100,0,150,100,0,150)


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
        nWenu = 0
        nWmunu = 0
        nWtaunu = 0
        nWq = 0
        nHb = 0
        ntb = 0
        nb = 0
        tb = []
        
        nVirtualWs = 0
        nVirtualWjjs = 0
        for label in labels:
            for var in vars:
                result[label+var] = [ ]
        result["WlnuMt"] = [ ]
        result["bMPID"] = [ ]
        result["WlnuPID"] = [ ]
        result["WDPID"] = [ ]
        result["tDPID"] = [ ]

        p_Hbb = TLorentzVector(0,0,0,0)
        p_HWW = TLorentzVector(0,0,0,0)
#        p = TLorentzVector(0,0,0,0) # four-momentum for p_t
        p_t = [TLorentzVector(0,0,0,0), TLorentzVector(0,0,0,0)] # four-momenta of the top quarks
        
        for particle in event.particles:
            
            PID = abs(particle.PID)
            D1 = particle.D1
            D2 = particle.D2
            
#            if D1>=0 and D2>=0 and D1<len(event.particles) and D2<len(event.particles) and event.particles[D1] and event.particles[D2]:
#                print "PID=%s" % PID
#                print "D1=%s" % D1
#                print "D2=%s" % D2
#                print "D1 PID=%s" % abs(event.particles[D1].PID)
#                print "D2 PID=%s\n" % abs(event.particles[D2].PID)

#            # __neutrinos__
#            if PID in [12,14,16]: # nu
#                result["nuPt"].append( particle.PT )
#                result["nuEta"].append( particle.Eta )
#                result["nuPhi"].append( particle.Phi )
#                result["nuM"].append( particle.Mass )
#            
#            # __lepton__
#            elif PID in [11,13,15]:#,15]: # e, mu, tau
#                result["lPt"].append( particle.PT )
#                result["lEta"].append( particle.Eta )
#                result["lPhi"].append( particle.Phi )
#                result["lM"].append( particle.Mass )
#                nLeptons += 1
#                if PID == 11:
#                    nElectrons += 1
#                    result["ePt"].append( particle.PT )
#                    result["eEta"].append( particle.Eta )
#                    result["ePhi"].append( particle.Phi )
#                    result["eM"].append( particle.Mass )
#                elif PID == 13:
#                    nMuons += 1
#                    result["muPt"].append( particle.PT )
#                    result["muEta"].append( particle.Eta )
#                    result["muPhi"].append( particle.Phi )
#                    result["muM"].append( particle.Mass )
#                elif PID == 15:
#                    nTaus += 1
#                    result["tauPt"].append( particle.PT )
#                    result["tauEta"].append( particle.Eta )
#                    result["tauPhi"].append( particle.Phi )
#                    result["tauM"].append( particle.Mass )
#
#            # __quark__
#            elif PID in [1,2,3,4,6]: # d, u, s, c, t   Note: no b-quark!!!
#                result["qPt"].append( particle.PT )
#                result["qEta"].append( particle.Eta )
#                result["qPhi"].append( particle.Phi )
#                result["qM"].append( particle.Mass )
#                
#                # top
#                if PID == 6 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2:
#                    nt += 1
#                    p_t[nt-1].SetPtEtaPhiM(particle.PT, particle.Eta, particle.Phi, particle.Mass)
#                    result["tDPID"].extend( [abs(event.particles[D1].PID), abs(event.particles[D2].PID) ])
#                    if abs(event.particles[D1].PID) == 5: # b
#                        ntb+=1
#                        tb.append(event.particles[D1])
#                    elif abs(event.particles[D2].PID) == 5: # b
#                        ntb+=1
#                        tb.append(event.particles[D2])
#                    
#            
#            # __b-quark__
#            elif PID == 5:
#                nb += 1
#                M1 = particle.M1
#                if M1>=0 and M1<len(event.particles) and event.particles[M1]:
#                    result["bMPID"].append( abs(event.particles[M1].PID) )

            # __W__
            if PID == 24 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # W
                nW += 1
                PID_D1 = abs( event.particles[D1].PID )
                PID_D2 = abs( event.particles[D2].PID )
#                if PID_D1 != 24:
                result["WDPID"].extend( [PID_D1, PID_D2] ) # all W daughters
                elif PID_D1 in [11,13,15]: # e, mu, tau
                    result["WlnuPt"].append( particle.PT )
                    result["WlnuEta"].append( particle.Eta )
                    result["WlnuPhi"].append( particle.Phi )
                    result["WlnuM"].append( particle.Mass )
                    result["WlnuMt"].append(sqrt( 2 * event.particles[D1].PT * event.particles[D2].PT * \
                                                  (1-cos( event.particles[D1].Phi - event.particles[D2].Phi ))))
                    result["WlnuPID"].extend( [PID_D1, PID_D2] ) # all W daughters
                    nWlnu+=1
                    if 11 in [PID_D1, PID_D2]:
                        nWenu += 1
                    elif 13 in [PID_D1, PID_D2]:
                        nWmunu += 1
                    elif 15 in [PID_D1, PID_D2]:
                        nWtaunu += 1
                    if abs(80.4-particle.Mass) > 10: # check if W is virtual
                        nVirtualWs += 1
                elif PID_D1 in [1,2,3,4,5]: # d, u, s, c, b
                    result["WjjPt"].append( particle.PT )
                    result["WjjEta"].append( particle.Eta )
                    result["WjjPhi"].append( particle.Phi )
                    result["WjjM"].append( particle.Mass )
#                    if PID_D1 == 5:
#                        result["WbbPt"].append( particle.PT )
#                        result["WbbEta"].append( particle.Eta )
#                        result["WbbPhi"].append( particle.Phi )
#                        result["WbbM"].append( particle.Mass )
                    nWq+=2
                    if abs(80.4-particle.Mass) > 10:
                        nVirtualWs += 1
                        nVirtualWjjs += 1
                elif PID_D1 in [12,14,16]: print "Warning: in GenControlPlots: PID_D1 of W is a neutrino!"
        
#            # __Higgs__
#            elif PID == 25 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # Higgs
#                PID_D1 = abs( event.particles[D1].PID )
#                nHiggs+=1
##                if abs(event.particles[particle.D1].PID) in [1,2,3,4,5]: # d, u, s, c, b
##                    result["HjjPt"].append( particle.PT )
##                    result["HjjEta"].append( particle.Eta )
##                    result["HjjPhi"].append( particle.Phi )
#                if PID_D1 == 5: # b
#                    nHb+=2
#                    p_Hbb.SetPtEtaPhiM(particle.PT, particle.Eta, particle.Phi, particle.Mass)
#                    result["HbbPt"].append( particle.PT )
#                    result["HbbEta"].append( particle.Eta )
#                    result["HbbPhi"].append( particle.Phi )
#                    result["HbbM"].append( particle.Mass )
#                    if abs(event.particles[D1].Eta)>abs(event.particles[D2].Eta): # order b-jets w.r.t. to Eta
#                        D1 = D2
#                        D2 = particle.D1
#                    result["b1Pt"].append( event.particles[D1].PT )
#                    result["b1Eta"].append( event.particles[D1].Eta )
#                    result["b1Phi"].append( event.particles[D1].Phi )
#                    result["b1M"].append( event.particles[D1].Mass )
#                    result["b2Pt"].append( event.particles[D2].PT )
#                    result["b2Eta"].append( event.particles[D2].Eta )
#                    result["b2Phi"].append( event.particles[D2].Phi )
#                    result["b2M"].append( event.particles[D2].Mass )
#                if PID_D1 in [24]: # W
#                    p_HWW.SetPtEtaPhiM(particle.PT, particle.Eta, particle.Phi, particle.Mass)
#                    result["HWWPt"].append( particle.PT )
#                    result["HWWEta"].append( particle.Eta )
#                    result["HWWPhi"].append( particle.Phi )
#                    result["HWWM"].append( particle.Mass )
#        
#        if len(tb)==2:
#            if abs(tb[0].Eta)>abs(tb[1].Eta): # order b-jets w.r.t. to Eta
#                tb1 = tb[1]
#                tb2 = tb[0]
#            else:
#                tb1 = tb[0]
#                tb2 = tb[1]
#            result["b1Pt"].append( tb1.PT )
#            result["b1Eta"].append( tb1.Eta )
#            result["b1Phi"].append( tb1.Phi )
#            result["b1M"].append( tb1.Mass )
#            result["b2Pt"].append( tb2.PT )
#            result["b2Eta"].append( tb2.Eta )
#            result["b2Phi"].append( tb2.Phi )
#            result["b2M"].append( tb2.Mass )
#
#        if nt == 2: # tt
#            q_tt = p_t[0] + p_t[1]
#            result["ttbbWWPt"].append( q_tt.Pt() )
#            result["ttbbWWEta"].append( q_tt.Eta() )
#            result["ttbbWWPhi"].append( q_tt.Phi() )
#            result["ttbbWWM"].append( q_tt.M() )
#
#        if nHiggs == 2: # HHbbWW
#            q_HH = p_Hbb + p_HWW
#            result["HHbbWWPt"].append( q_HH.Pt() )
#            result["HHbbWWEta"].append( q_HH.Eta() )
#            result["HHbbWWPhi"].append( q_HH.Phi() )
#            result["HHbbWWM"].append( q_HH.M() )

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
        
        else: print "Danger! No WW 2D-plot! See GenControlPlots.py"
            
#        if len(WlnuM)>0 or len(WjjM)>0:
#            if len(WlnuM) == 1 and len(WjjM) == 1: # monoleptonic
#                result["WWM"].append([WlnuM[0],WjjM[0]])
#            elif len(WlnuM) == 0 and len(WjjM) == 2: # hadronic
#                result["WjjWjjM"].append([WjjM[0],WjjM[1]])
#            elif len(WlnuM) == 2 and len(WjjM) == 0: # dileptonic
#                result["WlnuWlnuM"].append([WlnuM[0],WlnuM[1]])
#            else: print "Danger! No WWM, line 289!"

#        if len(WlnuMt) == 1 and len(WjjMt) == 1:
##            if len(WlnuM) == 1 and len(WjjM) == 1: # monoleptonic
#            result["WWMt"].append([WlnuMt[0],WjjMt[0]])

        result["NHiggs"] = nHiggs
        result["NW"] = nW
        result["NLeptons"] = nLeptons
        result["NElectrons"] = nElectrons
        result["NMuons"] = nMuons
        result["NTaus"] = nTaus
        result["NWlnu"] = nWlnu
        result["NWenu"] = nWenu
        result["NWmunu"] = nWmunu
        result["NWtaunu"] = nWtaunu
        result["NWq"] = nWq
        result["NHb"] = nHb
        result["Nb"] = nb
        result["Ntb"] = ntb
        result["NVirtualWs"] = nVirtualWs
        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], GenControlPlots())


