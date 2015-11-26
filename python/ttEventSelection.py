from ROOT import TLorentzVector as TLV

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel", "Selection20", "Selection30", "CleanUp", "Max5Jets" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
    
    categoryData = [ ]
    event.cleanedJets = [ jet for jet in event.jets ][:10]
    muons20 = [ m for m in event.muons if m.PT>20 and m.Eta<2.5 ]
    electrons20 = [ e for e in event.electrons if e.PT>20 and e.Eta<2.5 ]
    leps = sorted(muons20+electrons20, key=lambda x: x.PT, reverse=True)
    event.leadingLeptons = leps[:5]
    
    for m in muons20:
        m.Mass = 0.1057
        m.TLV = TLV()
        m.TLV.SetPtEtaPhiM(m.PT, m.Eta, m.Phi, m.Mass)
    for e in electrons20:
        e.Mass = 0.000511
        e.TLV = TLV()
        e.TLV.SetPtEtaPhiM(e.PT, e.Eta, e.Phi, e.Mass)
    
    event.DeltaPt_jl = [ ]
    event.DeltaR_jl = [ ]
    for lepton in leps: # remove all muons and electrons from jets
        for jet in event.cleanedJets:
            jet.TLV = TLV()
            jet.TLV.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
#            event.DeltaPt_jl.append(abs(lepton.TLV.Pt()-jet.TLV.Pt())/lepton.TLV.Pt())
#            event.DeltaR_jl.append(TLV.DeltaR(l,jet.TLV))
#            if event.DeltaR_jl[-1] < 0.5 and event.DeltaPt_jl[-1] < 0.2:
            if abs(lepton.TLV.Pt()-jet.TLV.Pt())/lepton.TLV.Pt() < 0.5 and \
               TLV.DeltaR(lepton.TLV,jet.TLV) < 0.2:
                event.cleanedJets.remove(jet)

    event.cleanedJets15 = [ jet for jet in event.cleanedJets if jet.PT > 15 and abs(jet.Eta) < 2.5 ]
    event.cleanedJets20 = [ jet for jet in event.cleanedJets15 if jet.PT > 20 and abs(jet.Eta) < 2.5 ]
    event.cleanedJets30 = [ jet for jet in event.cleanedJets20 if jet.PT > 30 and abs(jet.Eta) < 2.5 ]
    event.bjets30 = [ jet for jet in event.cleanedJets30 if jet.BTag and abs(jet.Eta) < 2.5 ]

    # 0: generator level: single Wlnu and Hbb
    nLeptons = 0
    nBquarks = 0
    for particle in event.particles:
        D1 = particle.D1
        if abs(particle.PID) == 24 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
            if abs(event.particles[D1].PID) in [11,13,15]: # e, mu, tau
                nLeptons+=1
        if abs(particle.PID) ==  6 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
            for D in [ event.particles[particle.D1], event.particles[particle.D2] ]:
                if abs(D.PID) == 5: # b-quark
                    nBquarks+=1
    categoryData.append((nLeptons==1 and nBquarks==2) or event.particles.GetEntries()==0)

    # 1: at least one muon or electron with Pt > 20 GeV
    categoryData.append( len(leps) )
    
    # 2: exactly one muon or electron with Pt > 20 GeV
    categoryData.append( len(leps) == 1 )
    
    # 3: Pt of leading 4 jets > 20 GeV
    categoryData.append( len(event.cleanedJets20)>3 )
#    categoryData.append(len(event.cleanedJets30)>2 and len(event.cleanedJets15)>3)

    # 4: Pt of leading 4 jets > 30 GeV
    categoryData.append( len(event.cleanedJets30)>3 )

    # 5: at least one b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>0 )
    
    # 6: at least two b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>1 )
    
    # 7: MET > 20 GeV cut
    categoryData.append( event.met[0].MET>20 )

    # 8: clean-up cuts
    [b1,b2] = min(combinations(event.bjets30),key=lambda bb: TLV.DeltaR(bb[0].TLV,bb[1].TLV))
    categoryData.append( 60<(b1.TLV+b2.TLV).M()<160 and \
                         TLV.DeltaR(b1.TLV,b2.TLV)<3.1 )
    
    # 9: at most 5 jets with Pt > 30 GeV
    categoryData.append( len(event.cleanedJets30)<6 )

    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
    if category == 0:
        return categoryData[0] and categoryData[2] and categoryData[3] and categoryData[6] and categoryData[7]
        #      > signal
    
    if category == 1:
        return categoryData[0] and categoryData[2] and categoryData[3] and categoryData[6] and categoryData[7]
        #      > signal            > exact 1 lepton    > 4 jets20          > 2 b-jets         > MET

    if category == 2:
        return categoryData[0] and categoryData[2] and categoryData[3] and categoryData[6] and categoryData[7] and categoryData[8]
        #      > signal            > exact 1 lepton    > 4 jets20          > 2 b-jets         > MET                > cleanup

    if category == 3:
        return categoryData[0] and categoryData[2] and categoryData[4] and categoryData[6] and categoryData[7] and categoryData[8]
        #      > signal            > exact 1 lepton    > 4 jets30          > 2 b-jets          > MET               > cleanup

    if category == 4:
        return categoryData[0] and categoryData[2] and categoryData[4] and categoryData[6] and categoryData[7] and categoryData[8] and categoryData[9]
        #      > signal            > exact 1 lepton    > 4 jets30          > 2 b-jets          > MET               > cleanup           > max 5 jets
        
    else:
        return False
