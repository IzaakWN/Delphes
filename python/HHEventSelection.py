from ROOT import TLorentzVector

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "Lepton4Jets" ] #[ "GenLevel", "Lepton4Jets" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
    
    categoryData = [ ]
    l = TLorentzVector()
    j = TLorentzVector()
    event.cleanedJets = [jet for jet in event.jets][:10] # never more than 10 jets
    
    # 0: exactly one muon or electron with Pt > 20 GeV
    if event.muons.GetEntries()>0:
        categoryData.append(event.muons[0].PT>20. and event.muons[1].PT<20.)
        for muon in event.muons: # remove all muons from jets
            l.SetPtEtaPhiM(muon.PT, muon.Eta, muon.Phi, 0.106)
            for jet in event.cleanedJets:
                j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
                if TLorentzVector.DeltaR(l,j) < 0.4:
                    event.cleanedJets.remove(jet)
    elif event.electrons.GetEntries()>0:
        categoryData.append(event.electrons[0].PT>20. and event.electrons[1].PT<20.)
        for electron in event.electrons: # remove all electrons from jets
            l.SetPtEtaPhiM(electron.PT, electron.Eta, electron.Phi, 0.000511)
            for jet in event.cleanedJets:
                j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
                if TLorentzVector.DeltaR(l,j) < 0.4:
                    event.cleanedJets.remove(jet)
    else:
        categoryData.append(False)

    # 1: Pt of leading 4 jets > 30 GeV after removing leptonic jets in (0) and (1)
    if event.jets.GetEntries() > 3:
        categoryData.append(event.cleanedJets[3].PT>30.)
    else:
        categoryData.append(False)

    # 2: generator level: single Wlnu and Hbb
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
    
    # 3: al least one b-tags
    bjets30 = [ jet for jet in event.cleanedJets if jet.BTag and jet.PT > 30 ]
    categoryData.append( len(bjets30)>1 )
    
    # 4: al least two b-tags
    categoryData.append( len(bjets30)>2 )

    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
#    if category==0:
#        return categoryData[2]
#    elif category==1::
#        return categoryData[0] and categoryData[2] and categoryData[3]
    if category==0:#1:#2:
        return categoryData[0] and categoryData[2] and categoryData[4]
    else:
        return False
