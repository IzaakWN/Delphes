from ROOT import TLorentzVector

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel", "Lepton4Jets", "2Bjets", "1Lepton", "Max6Jets" ]#, "Eta", "MET" ]



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
    recoMuon = False
    hasElectron = event.electrons.GetEntries()
    event.leadingLepton = None
    event.leadingLeptonPID = 0
    
    if event.muons.GetEntries():
        for muon in event.muons: # remove all muons from jets
            l.SetPtEtaPhiM(muon.PT, muon.Eta, muon.Phi, 0.106)
            for jet in event.cleanedJets:
                j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
                if TLorentzVector.DeltaR(l,j) < 0.5:
                    event.cleanedJets.remove(jet)
        if hasElectron:
            if event.electrons[0].PT < event.muons[0].PT:
                event.leadingLepton = event.muons[0]
                event.leadingLeptonPID = 13
            else:
                event.leadingLepton = event.electrons[0]
                event.leadingLeptonPID = 11
        else:
            event.leadingLepton = event.muons[0]
            event.leadingLeptonPID = 13
    elif hasElectron:
        event.leadingLepton = event.electrons[0]
        event.leadingLeptonPID = 11

    if hasElectron:
        for electron in event.electrons: # remove all electrons from jets
            l.SetPtEtaPhiM(electron.PT, electron.Eta, electron.Phi, 0.000511)
            for jet in event.cleanedJets:
                j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
                if TLorentzVector.DeltaR(l,j) < 0.5:
                    event.cleanedJets.remove(jet)

    event.cleanedJets15 = [ jet for jet in event.cleanedJets if jet.PT > 15 and abs(jet.Eta) < 2.5 ]
    event.cleanedJets30 = [ jet for jet in event.cleanedJets15 if jet.PT > 30 and abs(jet.Eta) < 2.5 ]
    event.bjets30 = [ jet for jet in event.cleanedJets30 if jet.BTag and abs(jet.Eta) < 2.5 ]
    
    # 0: at least one muon or electron with Pt > 20 GeV
    categoryData.append( len(muons20+electrons20) )
    
    # 1: exactly one muon or electron with Pt > 20 GeV
    categoryData.append( len(muons20+electrons20) == 1 )

    # 2: Pt of leading 4 jets > 30 GeV
    categoryData.append(len(event.cleanedJets30)>2 and len(event.cleanedJets15)>3)
    
    # 3: at least one b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>0 )
    
    # 4: at least two b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>1 )
    
    # 5: at most 6 jets with Pt > 30 GeV
    categoryData.append(len(event.cleanedJets30)<7)
    
    # 6: MET > 20 GeV cut
    categoryData.append( event.met[0].MET>20 )

    # 7: generator level: single Wlnu and Hbb
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
#        return categoryData[7]
#        #      > signal
        return isInCategory(1, categoryData)

    if category == 1:
        return categoryData[0] and categoryData[2] and categoryData[7]
        #      > lepton            > 4 jets            > signal
#        return isInCategory(3, categoryData)

    if category == 2:
        return categoryData[0] and categoryData[2] and categoryData[4] and categoryData[7]
        #      > lepton            > 4 jets            > 2 b-jets          > signal
#        return isInCategory(3, categoryData)

    if category == 3:
        return categoryData[1] and categoryData[2] and categoryData[4] and categoryData[7]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets        > signal

    if category == 3:
        return categoryData[1] and categoryData[2] and categoryData[4] and categoryData[5] and categoryData[7]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets          > max 6 jets        > signal
    
    if category == 4:
        return categoryData[1] and categoryData[2] and categoryData[4] and categoryData[5] and categoryData[6] and categoryData[7]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets          > max 6 jets        > MET               > signal
        
    else:
        return False
