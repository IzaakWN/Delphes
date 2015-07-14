from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector

# Requirements:
# event.jets
# event.bjets
# event.met


class ResControlPlots(BaseControlPlots):
    """A class to create control plots for resolution"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="jetmet", dataset=dataset, mode=mode)



    def beginJob(self):
    
        # b-tagging efficiency
        self.add("NHbb","b-quark from Hbb multiplicity generator",5,0,5)
        self.add("Nb","b-quark multiplicity generator",5,0,5)
        self.add("Nbtags","b-tag multiplicity",6,0,6)
        self.add("Ngoodbtag","Correct b-tags from H",3,0,3)
        self.add("Nbadbtag","Fake b-tags from W",4,0,4)
        self.add("Nqqbtag","Both q's from W b-tagged",5,0,5)



    def process(self, event):
        
        result = { }
        
        
        # resolution
        
        
        # b-tagging efficiency
        nb = 0
        nHbb = 0
        nbtags = 0
        nGoodbtag = 0
        nBadbtag = 0
        nqqbtag = 0
        p_bjet = TLorentzVector()
        p_quark = TLorentzVector()
        p_quark1 = TLorentzVector()
        p_quark2 = TLorentzVector()
        bjets = [ ]
        
        for jet in event.jets:
            if jet.BTag:
                nbtags += 1
                bjets += [jet]
        
        # good btag
        for particle in event.particles:
            D = particle.D1
            if D>=0 and D<len(event.particles) and event.particles[D]:
                D1 = event.particles[particle.D1]
                # Higgs
                if abs( particle.PID ) == 25:
                    # look at only one b-quark
                    if abs( D1.PID ) == 5:
                        nHbb += 2
                        for bjet in bjets:
                            p_bjet.SetPtEtaPhiM(bjet.PT,bjet.Eta,bjet.Phi,bjet.Mass)
                            p_quark.SetPtEtaPhiM(D1.PT,D1.Eta,D1.Phi,D1.Mass)
                            if TLorentzVector.DeltaR(p_bjet,p_quark) < 0.2:
                                nGoodbtag += 1
                                bjets.remove(bjet)
                                break # break jet-loop for next particle
                # W
                elif abs( particle.PID ) == 24:
                    # look at both quarks
                    if abs( D1.PID ) != 5: # b-quark; also allow for leptons
                        for bjet in bjets:
                            D2 = event.particles[particle.D2]
                            p_bjet.SetPtEtaPhiM(bjet.PT,bjet.Eta,bjet.Phi,bjet.Mass)
                            p_quark1.SetPtEtaPhiM(D1.PT, D1.Eta, D1.Phi, D1.Mass)
                            p_quark2.SetPtEtaPhiM(D2.PT, D2.Eta, D2.Phi, D2.Mass)
                            if TLorentzVector.DeltaR( p_bjet, p_quark1 ) < 0.2:
                                nBadbtag += 1
                                if TLorentzVector.DeltaR( p_bjet, p_quark2 ) < 0.2:
                                     nqqbtag += 1 # check if both q are b-tagged as one jet
                                bjets.remove(bjet)
    #                        elif TLorentzVector.DeltaR( p_bjet, p_quark2 ) < 0.2:
    #                            nBadbtag += 1
    #                            bjets.remove(bjet)

        result["Nb"] = nb
        result["Nbtags"] = nbtags
        result["NHbb"] = nHbb
        result["Ngoodbtag"] = nGoodbtag
        result["Nbadbtag"] = nBadbtag
        result["Nqqbtag"] = nqqbtag

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


#        for particle in event.particles:
#            M1 = particle.M1
#            # b-quark
#            if abs(particle.PID) == 5 and M1>=0 and M1<len(event.particles) and event.particles[M1]:
#                nb += 1
#                # mother is Higgs
#                if event.particles[M1].PID == 25:
#                    nHHb += 1
#                    for jet in event.jets:
#                        if jet.BTag:
#                            nbtags += 1
#                            p_bjet.SetPtEtaPhiM(jet.PT,jet.Eta,jet.Phi,jet.Mass)
#                            p_quark.SetPtEtaPhiM(particle.PT,particle.Eta,particle.Phi,particle.Mass)
#                            if TLorentzVector.DeltaR(p_bjet,p_quark)<0.2:
#                                nGoodbtag += 1
#                                event.jets.Remove(jet)
#                                break # go to next particle in event.particles
#
#                            
#        result["Nb"] = nb
#        result["NHHb"] = nHHb
#        result["Ngoodbtag"] = nGoodbtag
#        result["Nbadbtag"] = nbtags - nGoodbtag



