from ROOT import TLorentzVector

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "Lepton4Jets", "2Bjets", "OneLepton" ] #[ "GenLevel", "Lepton4Jets" ]



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
    
    # 0: at least one muon or electron with Pt > 20 GeV
    categoryData.append( len(muons20+electrons20) > 0 )
    
    # 1: exactly one muon or electron with Pt > 20 GeV
    categoryData.append( len(muons20+electrons20) == 1 )

    # 2: Pt of leading 4 jets > 30 GeV after removing leptonic jets in (0)
    if event.jets.GetEntries() > 3:
        categoryData.append(event.cleanedJets[3].PT>30.)
    else:
        categoryData.append(False)
    
    # 3: al least one b-tags
    event.bjets = [ jet for jet in event.cleanedJets if jet.BTag and jet.PT > 30 ]
    categoryData.append( len(event.bjets)>1 )
    
    # 4: al least two b-tags
    categoryData.append( len(event.bjets)>2 )

    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
#    if category==0:
#        return True

    if category == 0:
        return categoryData[0] and categoryData[2]
        #      > lepton            > 4 jets

    elif category == 1:
        return categoryData[0] and categoryData[2] and categoryData[4]
        #      > lepton            > 4 jets            > 2 b-jets

    elif category == 2:
        return categoryData[1] and categoryData[2] and categoryData[4]
        #      > lepton            > 4 jets            > 2 b-jets

    else:
        return False
