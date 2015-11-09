from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector
from itertools import combinations # to make jets combinations
from fold import fold

# Requirements:
# event.jets
# event.cleanedJets
# event.bjets30
# event.met

types = ["jet","bjet"]
n = ["1","2","3","4"]
vars = ["Pt","Eta","Phi","M"]

class JetControlPlots(BaseControlPlots):
    """A class to create control plots for jetmet"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="jetmet", dataset=dataset, mode=mode)



    def beginJob(self):
        
        
        # declare tree and branches
        self.addTree("jets","Jet variables for MVA")
        self.addBranch("jets","jet1Pt")
        self.addBranch("jets","jet2Pt")
        self.addBranch("jets","bjet1Pt")
        self.addBranch("jets","bjet2Pt")
    
        self.add("NUncleanedJets30","uncleaned jets multiplicity (Pt>30 GeV)",12,0,12)
        self.add("NJets30","jets multiplicity (Pt>30 GeV)",12,0,12)
        self.add("NBjets30","b-jets multiplicity (Pt>30 GeV)",8,0,8)
        self.add("NJets15","jets multiplicity (Pt>15 GeV)",20,0,20)
        self.add("NBjets15","b-jets multiplicity (Pt>15 GeV)",10,0,10)
        
        self.add2D("JetiEta","jet i abs(Eta)",14,0,14,20,0,5)
        
        #self.add("JetsDeltaR","jet combinations DeltaR (Pt>30 GeV)",100,0,8)
        #self.add("BJetsDeltaR","b-jet combinations DeltaR (Pt>30 GeV)",100,0,8)
        #self.add2D("JetsDeltaEtaDeltaPhi","jet combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,5,50,0,3.2)
        #self.add2D("BJetsDeltaEtaDeltaPhi","b-jet combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,5,50,0,3.2)
        #self.add2D("LeptonJetDeltaEtaDeltaPhi","lepton-jet combinations DeltaPhi vs. DeltaEta (Pt>30 GeV)",50,0,5,50,0,3.2)
        
        self.add("MET","MET",100,0,300)
        self.add("METPhi","MET Phi",64,-3.2,3.2)
        for type in types:
            for i in n:
                self.add(type+i+"Pt",type+" "+i+" Pt",100,0,250)
                self.add(type+i+"Eta",type+" "+i+" Eta",100,-5,5)
                self.add(type+i+"Phi",type+" "+i+" Phi",100,-3.2,3.2)
                self.add(type+i+"M",type+" "+i+" Mass",100,0,60)
        type = "nonbjet"
        for i in ["1","2"]:
            self.add(type+i+"Pt",type+" "+i+" Pt",100,0,250)
            self.add(type+i+"Eta",type+" "+i+" Eta",100,-5,5)
            self.add(type+i+"Phi",type+" "+i+" Phi",100,-3.2,3.2)
            self.add(type+i+"M",type+" "+i+" Mass",100,0,60)



    def process(self, event):
        
        result = { }
        
        result["jets"] = [ ] # respect the order of branches when adding variables
        
        for type in types:
            for i in n:
                for var in vars:
                    result[type+i+var] = [ ]
        
        jets = event.cleanedJets30[:8]
        result["NUncleanedJets30"]  = len([j for j in event.jets if j.PT>30])
        result["NJets30"]  = len(jets)
        result["NJets15"]  = len([j for j in event.cleanedJets if j.PT>15])
        
        result["JetiEta"] = [ ]
        for i in range(len(jets)):
            result["JetiEta"].append([ i, abs(jets[i].Eta) ])
                    
        
        # MET
        result["MET"] = event.met[0].MET
        result["METPhi"] = event.met[0].Phi
        
        # four leading jets
        if len(jets)>0:
            result["jet1Pt"].append(jets[0].PT)
            result["jets"].append(result["jet1Pt"][-1])
            result["jet1Eta"].append(jets[0].Eta)
            result["jet1Phi"].append(jets[0].Phi)
            result["jet1M"].append(jets[0].Mass)
        if len(jets)>1:
            result["jet2Pt"].append(jets[1].PT)
            result["jets"].append(result["jet2Pt"][-1])
            result["jet2Eta"].append(jets[1].Eta)
            result["jet2Phi"].append(jets[1].Phi)
            result["jet2M"].append(jets[1].Mass)
        if len(jets)>2:
            result["jet3Pt"].append(jets[2].PT)
            result["jet3Eta"].append(jets[2].Eta)
            result["jet3Phi"].append(jets[2].Phi)
            result["jet3M"].append(jets[2].Mass)
        if len(jets)>3:
            result["jet4Pt"].append(jets[3].PT)
            result["jet4Eta"].append(jets[3].Eta)
            result["jet4Phi"].append(jets[3].Phi)
            result["jet4M"].append(jets[3].Mass)

        # b-jets
        bjets = event.bjets30
        result["NBjets30"] = len(bjets)
        result["NBjets15"]  = len([j for j in event.cleanedJets if j.PT>15 and j.BTag])
    
        if len(bjets)>0:
            result["bjet1Pt"].append(bjets[0].PT)
            result["jets"].append(result["bjet1Pt"][-1])
            result["bjet1Eta"].append(bjets[0].Eta)
            result["bjet1Phi"].append(bjets[0].Phi)
            result["bjet1M"].append(bjets[0].Mass)
            jets.remove(bjets[0])
        if len(bjets)>1:
            result["bjet2Pt"].append(bjets[1].PT)
            result["jets"].append(result["bjet2Pt"][-1])
            result["bjet2Eta"].append(bjets[1].Eta)
            result["bjet2Phi"].append(bjets[1].Phi)
            result["bjet2M"].append(bjets[1].Mass)
            jets.remove(bjets[1])
        if len(bjets)>2:
            result["bjet3Pt"].append(bjets[2].PT)
            result["bjet3Eta"].append(bjets[2].Eta)
            result["bjet3Phi"].append(bjets[2].Phi)
            result["bjet3M"].append(bjets[2].Mass)
        if len(bjets)>3:
            result["bjet4Pt"].append(bjets[3].PT)
            result["bjet4Eta"].append(bjets[3].Eta)
            result["bjet4Phi"].append(bjets[3].Phi)
            result["bjet4M"].append(bjets[3].Mass)
            
        jets = [ j for j in jets if not j.BTag ]
        if len(jets)>0:
            result["nonbjet1Pt"] = jets[0].PT
            result["nonbjet1Eta"] = jets[0].Eta
            result["nonbjet1Phi"] = jets[0].Phi
            result["nonbjet1M"] = jets[0].Mass
        if len(jets)>1:
            result["nonbjet2Pt"] = jets[1].PT
            result["nonbjet2Eta"] = jets[1].Eta
            result["nonbjet2Phi"] = jets[1].Phi
            result["nonbjet2M"] = jets[1].Mass
        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], JetControlPlots())

