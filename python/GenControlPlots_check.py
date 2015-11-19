from BaseControlPlots import BaseControlPlots
from ROOT import TLorentzVector as TLV
from math import sqrt, pow, cos
from operator import attrgetter
from fold import fold



class GenControlPlots(BaseControlPlots):
    """A class to create control plots for HH and tt -> bbWW"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="gen", dataset=dataset, mode=mode)



    def beginJob(self):
        
        self.add("NtauW","tau->W multiplicity gen",5,0,5)
        
        self.add("NWlnu","W->lnu multiplicity gen",5,0,5)
        self.add("NWqq","W->qq multiplicity gen",5,0,5)
        self.add("WMotherPID","PID of W's mother gen",30,0,30)
        
        self.add("NHbb","H->bb multiplicity gen",5,0,5)
        self.add("NHWW","H->WW multiplicity gen",5,0,5)
        self.add("NHZZ","H->ZZ multiplicity gen",5,0,5)
        self.add("NHother","H->other multiplicity gen",5,0,5)
        self.add("NHHbbWW","HH->bbWW multiplicity gen",5,0,5)
        self.add("NHHother","H->other multiplicity gen",5,0,5)
        
        self.add("NParticlesGetEntries","HH->bbWW multiplicity gen",5,-2,2)



    def process(self, event):
        
        result = { }
        
        result["WMotherPID"] = [ ]
        
        if event.particles.GetEntries() > 0:
            result["NParticlesGetEntries"] = 1
        elif event.particles.GetEntries() == 0:
            result["NParticlesGetEntries"] = 0
            return result
        elif event.particles.GetEntries() < 0:
            result["NParticlesGetEntries"] = -1
        
        NtauW = 0
        
        NWlnu = 0
        NWqq = 0
        
        NHbb = 0
        NHWW = 0
        NHZZ = 0
        NHother = 0
        NHHbbWW = 0
        NHHother = 0
        
        for particle in event.particles:
            PID = abs(particle.PID)
            D1 = particle.D1
            D2 = particle.D2
            
            # __tau__
            if PID == 15 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
                if D1.PID == 24:
                    NtauW += 1

            # __W__
            if PID == 24 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # W
                PID_D1 = abs( event.particles[D1].PID )
                if PID_D1 in [11,13,15]: # e, mu, tau
                    NWlnu += 1
                elif PID_D1 in [1,2,3,4,5]: # d, u, s, c, b
                    NWqq += 1
        
            # __Higgs__
            elif PID == 25 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # Higgs
                PID_D1 = abs( event.particles[D1].PID )
                result["WMotherPID"].append(event.particles[particle.M1].PID)
                if PID_D1 == 5: # b
                    NHbb += 1
                elif PID_D1 == 24: # W
                    NHWW += 1
                elif PID_D1 == 25: # Z
                    NHZZ += 1
                else:
                    NHother+=1

        result["NtauW"] = NtauW
        result["NWlnu"] = NWlnu
        result["NWqq"] = NWqq
        result["NHbb"] = NHbb
        result["NHWW"] = NHWW
        result["NHZZ"] = NHZZ
        result["NHother"] = NHother
        if NHbb == 1 and NHWW ==1:
            NHHbbWW = 1
        else:
            NHHother = 1
        result["NHHbbWW"] = NHHbbWW
        result["NHHother"] = NHHother
        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], GenControlPlots())


