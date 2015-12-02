from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector
from operator import attrgetter

# Requirements:
# event.jets
# event.bjets
# event.met

class ResControlPlots(BaseControlPlots):
    """A class to create control plots for resolution"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="resolution", dataset=dataset, mode=mode)



    def beginJob(self):
    
        self.add("leptonDeltaPt","lepton resolution DeltaPt/Pt",100,0,20)
        self.add("leptonDeltaEta","lepton resolution DeltaEta/Eta",100,0,10)
        self.add("leptonDeltaPhi","lepton resolution DeltaPhi/Phi",100,0,10)
        self.add("nuMETDeltaPt","neutrino-MET resolution DeltaPt/Pt",100,0,100)
        self.add("nuMETDeltaPhi","neutrino-MET resolution DeltaPhi/Phi",100,0,10)



    def process(self, event):
        
        result = { }
        
        leptons = [ ]
        neutrinos = [ ]
        
        for particle in event.particles:
        
            D1 = particle.D1
            D2 = particle.D2
        
            if particle.PID == 24 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # W
                D1 = event.particles[D1]
                D2 = event.particles[D2]
                if abs(D1.PID) == 11 and event.electrons.GetEntries(): # e
                    leptons.append(D1)
                elif abs(D1.PID) == 13 and event.muons.GetEntries(): # mu
                    leptons.append(D1)
                if abs(D2.PID) in [12,14]: # neutrino's
                    neutrinos.append(D2)
    
        if leptons:
            leadingLepton = max(leptons, key=attrgetter('PT'))
            result["leptonDeltaPt" ] = abs(leadingLepton.PT  - event.leadingLepton.PT)/event.leadingLepton.PT
            result["leptonDeltaEta"] = abs(leadingLepton.Eta - event.leadingLepton.Eta)/event.leadingLepton.Eta
            result["leptonDeltaPhi"] = abs(leadingLepton.Phi - event.leadingLepton.Phi)/event.leadingLepton.Phi
            leadingNeutrino = max(neutrinos, key=attrgetter('PT'))
            result["nuMETDeltaPt" ] = abs(leadingNeutrino.PT  - event.met[0].MET)/leadingNeutrino.PT
            result["nuMETDeltaPhi"] = abs(leadingNeutrino.Phi - event.met[0].Phi)/leadingNeutrino.Phi

        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], JetControlPlots())

