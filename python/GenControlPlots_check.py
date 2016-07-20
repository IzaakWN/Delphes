from BaseControlPlots import BaseControlPlots



class GenControlPlots(BaseControlPlots):
    """A class to create control plots for HH and tt -> bbWW"""



    def __init__(self, dir=None, dataset=None, mode="plots"):
        # create output file if needed. If no file is given, it means it is delegated
        BaseControlPlots.__init__(self, dir=dir, purpose="gen", dataset=dataset, mode=mode)



    def beginJob(self):
        
        self.add("NtauW","tau->W multiplicity gen",5,0,5)
        
        self.add("NW","W multiplicity gen",20,0,20)
        self.add("NWlnu","W->lnu multiplicity gen",5,0,5)
        self.add("NWqq","W->qq multiplicity gen",5,0,5)
        self.add("NWWW","W->qq multiplicity gen",100,0,100)
        self.add("WMotherPID","PID of W's mother gen",100,0,100)
        
        self.add("HPt","H Pt gen",100,0,500)
        self.add("HPz","H Pz gen",100,0,500)
        self.add("tPt","top Pt gen",100,0,500)
        self.add("tPz","top Pz gen",100,0,500)

        self.add("NHqq","H->qq multiplicity gen",5,0,5)
        self.add("NHbb","H->bb multiplicity gen",5,0,5)
        self.add("NHll","H->ll multiplicity gen",5,0,5)
        self.add("NHZZ","H->ZZ multiplicity gen",5,0,5)
        self.add("NHWW","H->WW multiplicity gen",5,0,5)
        self.add("NHHH","H->WW multiplicity gen",5,0,5)
        self.add("NHother","H->other multiplicity gen",5,0,5)
        self.add("NHHbbWW","HH->bbWW multiplicity gen",5,0,5)
        self.add("NHHother","H->other multiplicity gen",5,0,5)
        
        self.add("NParticlesGetEntries","HH->bbWW multiplicity gen",4,-2,2)

        self.add("Match_Jet1_q","leading jet matches quark from W",5,0,5)
        self.add("Match_Jet2_q","second leading jet matches quark from W",5,0,5)
        self.add2D("Match_Jets_q","leading jets match quark from W",5,0,5,5,0,5)
        self.add2D("MatchLJets","non b tagged jet matches b quark vs. light quark",5,0,5,4,0,4)
        self.add2D("MatchBJets","b jet matches b quark vs. light quark",5,0,5,4,0,4)
        
        

    def process(self, event):
        
        result = { }
        
        result["HPt"] = [ ]
        result["HPz"] = [ ]
        result["tPt"] = [ ]
        result["tPz"] = [ ]
        result["WMotherPID"] = [ ]
        
        result["MatchLJets"] = [ ]
        result["MatchBJets"] = [ ]
        
        if event.particles.GetEntries() > 0:
            result["NParticlesGetEntries"] = 1
        elif event.particles.GetEntries() == 0:
            result["NParticlesGetEntries"] = 0
            return result
        elif event.particles.GetEntries() < 0:
            result["NParticlesGetEntries"] = -1
        
        NtauW = 0
        
        NW = 0
        NWlnu = 0
        NWqq = 0
        NWWW = 0
        
        NHqq = 0
        NHbb = 0
        NHll = 0
        NHZZ = 0
        NHWW = 0
        NHHH = 0
        NHother = 0
        NHHbbWW = 0
        NHHother = 0
        
        quarks = [ ]
        p_quarks = [ ]
        bquarks = [ ]
        p_bquarks = [ ]
        
        for particle in event.particles:
            PID = abs(particle.PID)
            D1 = particle.D1
            D2 = particle.D2
            
            # __tau__
            if PID == 15 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
                PID_D1 = abs( event.particles[D1].PID )
                if PID_D1 == 24:
                    NtauW += 1
                elif abs(event.particles[D2].PID) == 5: # b
                    bquarks.append(event.particles[D2])
                    p_bquarks.append(TLV())
                    p_bquarks[-1].SetPtEtaPhiM(bquarks[-1].PT, bquarks[-1].Eta, bquarks[-1].Phi, bquarks[-1].Mass)
                result["tPt"].append(particle.PT)
                result["tPz"].append(abs(particle.Pz))

            # __W__
            elif PID == 24 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # W
                NW += 1
                PID_D1 = abs( event.particles[D1].PID )
                if PID_D1 in [11,13,15]: # e, mu, tau
                    NWlnu += 1
                elif PID_D1 in [1,2,3,4,5]: # d, u, s, c, b
                    NWqq += 1
                    quarks.append(particles[D1])
                    quarks.append(particles[D2])
                    p_quarks.append(TLV())
                    p_quarks.append(TLV())
                    p_quarks[-2].SetPtEtaPhiM(quarks[-2].PT, quarks[-2].Eta, quarks[-2].Phi, quarks[-2].Mass)
                    p_quarks[-1].SetPtEtaPhiM(quarks[-1].PT, quarks[-1].Eta, quarks[-1].Phi, quarks[-1].Mass)

                elif PID_D1 == 24: # d, u, s, c, b
                    NWWW += 1
        
            # __Higgs__
            elif PID == 25 and D1>=0 and D1<len(event.particles) and event.particles[D1] and D1!=D2: # Higgs
                result["WMotherPID"].append(abs(event.particles[particle.M1].PID))
                PID_D1 = abs( event.particles[D1].PID )
                result["HPt"].append(particle.PT)
                result["HPz"].append(abs(particle.Pz))
                if PID_D1 in [1,2,3,4,5]: # d, u, s, c, b
                    NHqq += 1
                if PID_D1 == 5: # b
                    NHbb += 1
                    bquarks.append(particles[D1])
                    bquarks.append(particles[D2])
                    p_bquarks.append(TLV())
                    p_bquarks.append(TLV())
                    p_bquarks[-2].SetPtEtaPhiM(bquarks[-2].PT, bquarks[-2].Eta, bquarks[-2].Phi, bquarks[-2].Mass)
                    p_bquarks[-1].SetPtEtaPhiM(bquarks[-1].PT, bquarks[-1].Eta, bquarks[-1].Phi, bquarks[-1].Mass)
                elif PID_D1 in [11,12,13]: # e, mu, tau
                    NHll += 1
                elif PID_D1 == 23: # Z
                    NHZZ += 1
                elif PID_D1 == 24: # W
                    NHWW += 1
                elif PID_D1 == 25: # H
                    NHHH += 1
                else:
                    NHother+=1
        
        if NHbb == 1 and NHWW == 1:
            NHHbbWW = 1
        else:
            NHHother = 1

        result["NtauW"] = NtauW
        
        result["NW"] = NW
        result["NWlnu"] = NWlnu
        result["NWqq"] = NWqq
        result["NWWW"] = NWWW
        
        result["NHqq"] = NHqq
        result["NHbb"] = NHbb
        result["NHll"] = NHll
        result["NHZZ"] = NHZZ
        result["NHWW"] = NHWW
        result["NHHH"] = NHHH
        result["NHother"] = NHother
        result["NHHbbWW"] = NHHbbWW
        result["NHHother"] = NHHother
                
        # __Matching_leading_jets__
        jets = event.cleanedJets20[:] # remove closest b-jets pair down below
        bjets = event.bjets30[:]
        for bjet in min( combinations(bjets,2), key=lambda bj: TLV.DeltaR(bj[0].TLV,bj[1].TLV) ) : # remove closest bjet pair from jet list
            if bjet in jets:
                jets.remove(bjet)
        result["Match_Jet1_q"] = 0
        result["Match_Jet2_q"] = 0
        for p in p_quarks:
            if TLV.DeltaR(p,jets[0].TLV) < 0.4:
                result["Match_Jet1_q"] += 1
            if TLV.DeltaR(p,jets[1].TLV) < 0.4:
                result["Match_Jet2_q"] += 1
        result["Match_Jets_q"] = [[ result["Match_Jet1_q"], result["Match_Jet2_q"] ]]
        
        # __Matching_b_tagging__    
        for jet in event.cleanedJets20:
            NMatch_lq = 0
            NMatch_bq = 0
            for p in p_quarks: # quarks from W
                if TLV.DeltaR(jet.TLV,p) < 0.4:
                    NMatch_lq += 1
            for p in p_bquarks: # b quarks
                if TLV.DeltaR(jet.TLV,p) < 0.4:
                    NMatch_bq += 1
            if jet.BTag:
                result["NMatchBJets"].append([NMatch_lq,NMatch_bq])
            else:
                result["NMatchLJets"].append([NMatch_lq,NMatch_bq])
        
        return result



if __name__=="__main__":
    import sys
    from DelphesAnalysis.BaseControlPlots import runTest
    runTest(sys.argv[1], GenControlPlots())


