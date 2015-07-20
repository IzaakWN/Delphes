from ROOT import TLorentzVector

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel", "Lepton4Jets", "2Bjets", "1Lepton", "MET&Eta" ] #[ "GenLevel", "Lepton4Jets" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
    
    categoryData = [ ]
    l = TLorentzVector()
    j = TLorentzVector()
    event.cleanedJets = [jet for jet in event.jets][:10]
    muons20 = [m for m in event.muons if m.PT>20]
    electrons20 = [e for e in event.electrons if e.PT>20]
    
    if event.muons.GetEntries() > 0:
        for muon in event.muons: # remove all muons from jets
            l.SetPtEtaPhiM(muon.PT, muon.Eta, muon.Phi, 0.106)
            for jet in event.cleanedJets:
                j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
                if TLorentzVector.DeltaR(l,j) < 0.4:
                    event.cleanedJets.remove(jet)
    if event.electrons.GetEntries() > 0:
        for electron in event.electrons: # remove all electrons from jets
            l.SetPtEtaPhiM(electron.PT, electron.Eta, electron.Phi, 0.000511)
            for jet in event.cleanedJets:
                j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
                if TLorentzVector.DeltaR(l,j) < 0.4:
                    event.cleanedJets.remove(jet)
    
    event.cleanedJets30 = [jet for jet in event.cleanedJets if jet.PT > 30]
    event.bjets30 = [ jet for jet in event.cleanedJets30 if jet.BTag]
    
    # 0: at least one muon or electron with Pt > 20 GeV
    categoryData.append( len(muons20+electrons20) > 0 )
    
    # 1: exactly one muon or electron with Pt > 20 GeV
    categoryData.append( len(muons20+electrons20) == 1 )

    # 2: Pt of leading 4 jets > 30 GeV after removing leptonic jets in (0)
    if event.jets.GetEntries() > 3:
        categoryData.append(event.cleanedJets[3].PT>30.)
    else:
        categoryData.append(False)
    
    # 3: at least one b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>0 )
    
    # 4: at least two b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>1 )
    
    # 5: MET > 20 GeV cut
    categoryData.append( event.met[0].MET>20 )
    
    # 6: at least 2 b-jets and 2 non-b-jets with Eta < 2.5
    categoryData.append( len([jet for jet in event.cleanedJets30 if jet.Eta < 2.5]) > 3
                         and len([jet for jet in event.bjets30 if jet.Eta < 2.5]) > 1 )

    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
    if category == 0:
        return True

    if category == 1:
        return categoryData[0] and categoryData[2]
        #      > lepton            > 4 jets
    
    elif category == 2:
        return categoryData[0] and categoryData[2] and categoryData[4]
        #      > lepton            > 4 jets            > 2 b-jets
    
    elif category == 3:
        return categoryData[1] and categoryData[2] and categoryData[4]
        #      > lepton            > 4 jets            > 2 b-jets
    
    elif category == 4:
        return categoryData[1] and categoryData[2] and categoryData[4] and categoryData[5] and categoryData[6]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets          > MET               > 2 jets Eta
    
    else:
        return False