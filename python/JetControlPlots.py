from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector

# Requirements:
# event.jets
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
        
        self.add("Nuncleanedjets30","uncleaned jets multiplicity (Pt>30 GeV)",12,0,12)
        self.add("Njets30","jets multiplicity (Pt>30 GeV)",12,0,12)
        self.add("Nbjets30","b-jets multiplicity (Pt>30 GeV)",8,0,8)
        
        self.add2D("JetiEta","jeti abs(Eta)",14,0,14,20,0,5)
        self.add("NjetsEta3","jets multiplicity (Pt>30 GeV, Eta<3)",12,0,12)
        self.add("NjetsEta25","jets multiplicity (Pt>30 GeV, Eta<2.5)",12,0,12)
        self.add("NjetsEta2","jets multiplicity (Pt>30 GeV, Eta<2)",12,0,12)
        
        self.add("MET","MET",100,0,300)
        self.add("METPhi","MET Phi",64,-3.2,3.2)
        for type in types:
            for i in n:
                self.add(type+i+"Pt",type+i+" Pt",100,0,250)
                self.add(type+i+"Eta",type+i+" Eta",100,-5,5)
                self.add(type+i+"Phi",type+i+"jet1 Phi",100,-3.2,3.2)
                self.add(type+i+"M",type+i+" Mass",100,0,60)



    def process(self, event):
        
        result = { }
        
        for type in types:
            for i in n:
                for var in vars:
                    result[type+i+var] = [ ]
        
        jets = event.cleanedJets30
        result["Nuncleanedjets30"]  = len([j for j in event.jets if j.PT>30])
        result["Njets30"]  = len(jets)
        
        nJetsEta3 = 0 # Eta < 3
        nJetsEta25 = 0 # Eta < 2.5
        nJetsEta2 = 0 # Eta < 2
        result["JetiEta"] = [ ]
        for i in range(len(jets)):
            result["JetiEta"].append([ i, abs(jets[i].Eta) ])
            if jets[i].Eta < 3:
                nJetsEta3 += 1
                if jets[i].Eta < 2.5:
                    nJetsEta25 += 1
                    if jets[i].Eta < 2:
                        nJetsEta2 += 1
        result["NjetsEta3"] = nJetsEta3
        result["NjetsEta25"] = nJetsEta25
        result["NjetsEta2"] = nJetsEta2
                    
        
        
        # MET
        result["MET"] = event.met[0].MET
        result["METPhi"] = event.met[0].Phi
        
        # four leading jets
        if event.jets.GetEntries()>0:
            result["jet1Pt"].append(event.jets[0].PT)
            result["jet1Eta"].append(event.jets[0].Eta)
            result["jet1Phi"].append(event.jets[0].Phi)
            result["jet1M"].append(event.jets[0].Mass)
        if event.jets.GetEntries()>1:
            result["jet2Pt"].append(event.jets[1].PT)
            result["jet2Eta"].append(event.jets[1].Eta)
            result["jet2Phi"].append(event.jets[1].Phi)
            result["jet2M"].append(event.jets[1].Mass)
        if event.jets.GetEntries()>2:
            result["jet3Pt"].append(event.jets[2].PT)
            result["jet3Eta"].append(event.jets[2].Eta)
            result["jet3Phi"].append(event.jets[2].Phi)
            result["jet3M"].append(event.jets[2].Mass)
        if event.jets.GetEntries()>3:
            result["jet4Pt"].append(event.jets[3].PT)
            result["jet4Eta"].append(event.jets[3].Eta)
            result["jet4Phi"].append(event.jets[3].Phi)
            result["jet4M"].append(event.jets[3].Mass)

        # b-jets
        bjets30 = event.bjets30
<<<<<<< HEAD
        result["Nbjets30"] = len(bjets30)
=======
        result["Nbjets30"] = len(bjets)
>>>>>>> f0e6ac99b7c213ab1a9cc84801dbda7163a58d20
    
        if len(bjets30)>0:
            result["bjet1Pt"].append(bjets30[0].PT)
            result["bjet1Eta"].append(bjets30[0].Eta)
            result["bjet1Phi"].append(bjets30[0].Phi)
            result["bjet1M"].append(bjets30[0].Mass)
        if len(bjets30)>1:
            result["bjet2Pt"].append(bjets30[1].PT)
            result["bjet2Eta"].append(bjets30[1].Eta)
            result["bjet2Phi"].append(bjets30[1].Phi)
            result["bjet2M"].append(bjets30[1].Mass)
        if len(bjets30)>2:
            result["bjet3Pt"].append(bjets30[2].PT)
            result["bjet3Eta"].append(bjets30[2].Eta)
            result["bjet3Phi"].append(bjets30[2].Phi)
            result["bjet3M"].append(bjets30[2].Mass)
        if len(bjets30)>3:
            result["bjet4Pt"].append(bjets30[3].PT)
            result["bjet4Eta"].append(bjets30[3].Eta)
            result["bjet4Phi"].append(bjets30[3].Phi)
            result["bjet4M"].append(bjets30[3].Mass)
        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], JetControlPlots())

