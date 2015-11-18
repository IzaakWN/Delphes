from ROOT import TLorentzVector

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel", "Selection20", "Selection30", "MET", "Max5Jets" ]



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
    
    # 2: Pt of leading 4 jets > 20 GeV
    categoryData.append( len(event.cleanedJets20)>3 )
#    categoryData.append(len(event.cleanedJets30)>2 and len(event.cleanedJets15)>3)

    # 3: Pt of leading 4 jets > 30 GeV
    categoryData.append( len(event.cleanedJets30)>3 )

    # 4: at least one b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>0 )
    
    # 5: at least two b-jet with Pt > 30 GeV
    categoryData.append( len(event.bjets30)>1 )
    
    # 6: MET > 20 GeV cut
    categoryData.append( event.met[0].MET>20 )
    
    # 7: at most 6 jets with Pt > 30 GeV
    categoryData.append( len(event.cleanedJets30)<6 )

    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
    if category == 0:
        return categoryData[1] and categoryData[2] and categoryData[5]
        #      > signal
    
    if category == 1:
        return categoryData[1] and categoryData[2] and categoryData[5]
        #      > exact 1 lepton    > 4 jets > 20 GeV   > 2 b-jets

    if category == 2:
        return categoryData[1] and categoryData[3] and categoryData[5]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets

    if category == 3:
        return categoryData[1] and categoryData[3] and categoryData[5] and categoryData[6]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets          > MET
    
    if category == 4:
        return categoryData[1] and categoryData[3] and categoryData[5] and categoryData[6] and categoryData[7]
        #      > exact 1 lepton    > 4 jets            > 2 b-jets          > MET               > max 5 jets
        
    else:
        return False
