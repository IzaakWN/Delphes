from ROOT import TLorentzVector

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel", "Lepton4Jets", "2Bjets", "1Lepton", "Max6Jets", "MET", "4Jets20" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
    
    categoryData = [ ]
    l = TLorentzVector()
    j = TLorentzVector()
    event.cleanedJets = [ jet for jet in event.jets ][:10]
    muons20 = [ m for m in event.muons if m.PT>20 and m.Eta<2.5 ]
    electrons20 = [ e for e in event.electrons if e.PT>20 and e.Eta<2.5 ]
    leps = sorted(muons20+electrons20, key=lambda x: x.PT, reverse=True)
    event.leadingLeptons = leps[:5]
    #event.leadingLeptons[0].P = TLorentzVector()
    #event.leadingLeptons[0].P.SetPtEtaPhiM(event.leadingLeptons[0].PT, event.leadingLeptons[0].Eta,
                                           #event.leadingLeptons[0].Phi, event.leadingLeptons[0].Mass)
    for m in muons20:
        m.Mass = 0.1057
    for e in electrons20:
        e.Mass = 0.000511
    
    event.DeltaPt_jl = [ ]
    event.DeltaR_jl = [ ]
    for lepton in leps: # remove all muons and electrons from jets
        l.SetPtEtaPhiM(lepton.PT, lepton.Eta, lepton.Phi, lepton.Mass)
        for jet in event.cleanedJets:
            j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
            event.DeltaPt_jl.append(abs(l.Pt()-j.Pt())/l.Pt())
            event.DeltaR_jl.append(TLorentzVector.DeltaR(l,j))
            if event.DeltaR_jl[-1] < 0.5 and event.DeltaPt_jl[-1] < 0.2:
                event.cleanedJets.remove(jet)

    event.cleanedJets15 = [ jet for jet in event.cleanedJets if jet.PT > 15 and abs(jet.Eta) < 2.5 ]
    event.cleanedJets20 = [ jet for jet in event.cleanedJets15 if jet.PT > 20 and abs(jet.Eta) < 2.5 ]
    event.cleanedJets30 = [ jet for jet in event.cleanedJets20 if jet.PT > 30 and abs(jet.Eta) < 2.5 ]
    event.bjets30 = [ jet for jet in event.cleanedJets30 if jet.BTag and abs(jet.Eta) < 2.5 ]
    nonbjets30 = [ jet for jet in event.cleanedJets30 if (not jet.BTag) and abs(jet.Eta) < 2.5 ]

    # 0: at least one muon or electron with Pt > 20 GeV
    categoryData.append( len(leps) )
    
    # 1: exactly one muon or electron with Pt > 20 GeV
    categoryData.append( len(leps) == 1 )

    # 2: Pt of leading 4 jets > 30 GeV
    categoryData.append(len(event.cleanedJets30)>3)
#    categoryData.append(len(event.cleanedJets30)>2 and len(event.cleanedJets15)>3)

    # 3: at least one b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>0 )
    
    # 4: at least two b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>1 )
    
    # 5: at most 6 jets with Pt > 30 GeV
    categoryData.append(len(event.cleanedJets30)<7)
    
    # 6: MET > 20 GeV cut
    categoryData.append( event.met[0].MET>20 )
    
    # 7: Pt of leading 4 jets > 20 GeV
    categoryData.append(len(event.cleanedJets20)>3)

    # 8: generator level: single Wlnu and Hbb
    nLeptons = 0
    nBquarks = 0
    for particle in event.particles:
        D1 = particle.D1
        if abs(particle.PID) == 24 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
            if abs(event.particles[D1].PID) in [11,13,15]: # e, mu, tau
                nLeptons+=1
        if abs(particle.PID) == 25 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
            if abs(event.particles[D1].PID) in [5]: # b-quark
                nBquarks+=2
    categoryData.append((nLeptons==1 and nBquarks==2) or event.particles.GetEntries()==0)

    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
    if category == 0:
        return categoryData[8]
        #      > signal

    if category == 1: # in [0,1]
        return categoryData[1] and categoryData[2] and categoryData[8]
        #      > lepton            > 4 jets            > signal

    if category == 2:
        return categoryData[1] and categoryData[2] and categoryData[4] and categoryData[8]
        #      > lepton            > 4 jets            > 2 b-jets          > signal

    if category == 3:
        return categoryData[1] and categoryData[2] and categoryData[4] and categoryData[8]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets          > signal

    if category == 4:
        return categoryData[1] and categoryData[2] and categoryData[4] and categoryData[5] and categoryData[8]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets          > max 6 jets        > signal
    
    if category == 5:
        return categoryData[1] and categoryData[2] and categoryData[4] and categoryData[5] and categoryData[6] and categoryData[8]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets          > max 6 jets        > MET               > signal
    
    if category == 6:
        return categoryData[1] and categoryData[7] and categoryData[4] and categoryData[8]
        #      > exact 1 lepton    > 4 jets > 20 GeV   > 2 b-jets          > signal
        
    else:
        return False
