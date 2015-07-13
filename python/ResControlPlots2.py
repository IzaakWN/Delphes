from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector

# Requirements:
# event.jets
# event.bjets
# event.met

class ResControlPlots2(BaseControlPlots):
    """A class to create control plots for resolution"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="jetmet", dataset=dataset, mode=mode)



    def beginJob(self):
    
        # b-tagging efficiency
        self.add("NHbb","b-quark from Hbb multiplicity generator",5,0,5)
        self.add("Nb","b-quark multiplicity generator",5,0,5)
        self.add("Nbtags","b-tag multiplicity",6,0,6)
        self.add("Ngoodbtag","Correct b-tags",5,0,5)
        self.add("Nbadbtag","Incorrect b-tags",5,0,5)



    def process(self, event):
        
        result = { }
        
        
        # resolution
        
        
        # b-tagging efficiency
        nb = 0
        nHbb = 0
        nbtags = 0
        nGoodbtag = 0
        p_bjet = TLorentzVector()
        p_quark = TLorentzVector()

        for particle in event.particles:
            M1 = particle.M1
            # b-quark
            if abs( particle.PID ) == 5 and M1>=0 and M1<len(event.particles) and event.particles[M1]:
                nb += 1
                # mother is Higgs
                if abs( event.particles[M1].PID ) == 25:
                    nHbb += 1
                    for jet in event.jets:
                        if jet.BTag:
                            nbtags += 1
                            p_bjet.SetPtEtaPhiM(jet.PT,jet.Eta,jet.Phi,jet.Mass)
                            p_quark.SetPtEtaPhiM(particle.PT,particle.Eta,particle.Phi,particle.Mass)
                            if TLorentzVector.DeltaR(p_bjet,p_quark)<0.2:
                                nGoodbtag += 1
                                event.jets.Remove(jet)
                                break # go to next particle in event.particles

        result["Nb"] = nb
        result["Nbtags"] = nbtags
        result["NHbb"] = nHbb
        result["Ngoodbtag"] = nGoodbtag
        result["Nbadbtag"] = nbtags - nGoodbtag

        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], JetControlPlots())







#        for particle in event.particles:
#            D1 = particle.D1
#            # Higgs
#            if particle.PID == 25 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
#                # look at only one b-quark
#                if abs( event.particles[D1].PID ) == 5:
#                    nHbb += 2
#                    for jet in event.jets:
#                        if jet.BTag:
#                            nbtags += 1
#                            p_bjet.SetPtEtaPhiM(jet.PT,jet.Eta,jet.Phi,jet.Mass)
#                            p_quark.SetPtEtaPhiM(particle.PT,particle.Eta,particle.Phi,particle.Mass)
#                            if TLorentzVector.DeltaR(p_bjet,p_quark)<0.2:
#                                nGoodbtag += 1
##                                event.jets.Remove(jet)
##                                break # go to next particle in event.particles




