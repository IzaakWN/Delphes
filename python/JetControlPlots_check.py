from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
#from itertools import combinations # to make jets combinations
#from fold import fold



class JetControlPlots(BaseControlPlots):
    """A class to create control plots for jetmet"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="jetmet", dataset=dataset, mode=mode)



    def beginJob(self):
    
        #self.add("NUncleanedJets30","uncleaned jets multiplicity (Pt>30 GeV)",12,0,12)
        #self.add("NBjets","b-jets multiplicity (Pt>30 GeV)",8,0,8)
        #self.add("NBjets15","b-jets multiplicity (Pt>15 GeV)",10,0,10)
        #self.add("NBjets30","b-jets multiplicity (Pt>30 GeV)",8,0,8)
        #self.add("NJets","jets multiplicity (Pt>15 GeV)",30,0,30)
        #self.add("NJets15","jets multiplicity (Pt>15 GeV)",20,0,20)
        #self.add("NJets30","jets multiplicity (Pt>30 GeV)",12,0,12)
        
        self.add("DeltaR_j1l","closest jet-lepton DeltaR",100,0,4)
        self.add("DeltaR_j1l_uncleaned","closest jet-lepton uncleaned jet list",100,0,4)
        
        self.add("EtaMostForwardJet","Eta of most forward jet",10,0,5)
        self.add("EtaMostForwardJet20","Eta of most forward jet with PT<20",20,0,10)
        self.add("EtaMostForwardJet30","Eta of most forward jet with PT<30",20,0,10)
        self.add("EtaMostForwardJet50","Eta of most forward jet with PT<50",20,0,10)
        
        self.add("PTMostForwardJet","PT of most forward jet",100,0,250)
 


    def process(self, event):
        
        result = { }

        #lepton = None
        #p_neutrino = None
        #MET = event.met[0]
        if event.leadingLeptons and event.cleanedJets20:
            lepton = event.leadingLeptons[0]
            #p_neutrino = recoNeutrino(lepton.TLV,MET)
            jets_uncleaned = [j for j in event.jets if j.PT > 20 and abs(j.Eta)<2.5]
            jets = event.cleanedJets20[:]

            for jet in jets_uncleaned:
                if not hasattr(jet,'TLV'):
                    jet.TLV = TLV()
                    jet.TLV.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

            #ji = sorted(jets, key=lambda j: TLV.DeltaR(j.TLV,lepton.TLV))[:3] # closest jets
            result["DeltaR_j1l"] = min([TLV.DeltaR(j.TLV,lepton.TLV) for j in jets]) # closest jets
            result["DeltaR_j1l_uncleaned"] = min([TLV.DeltaR(j.TLV,lepton.TLV) for j in jets_uncleaned])



        jet_max = max(event.cleanedJets, key=lambda j: abs(j.Eta))
        EtaRegion = 0
        
        result["EtaMostForwardJet"] = abs(jet_max.Eta)
        result["PTMostForwardJet"] = jet_max.PT
        
        if 20 < jet_max.PT:
            result["EtaMostForwardJet20"] = abs(jet_max.Eta)
            if 30 < jet_max.PT:
                result["EtaMostForwardJet30"] = abs(jet_max.Eta)
                if 50 < jet_max.PT:
                    result["EtaMostForwardJet50"] = abs(jet_max.Eta)



        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], JetControlPlots())

