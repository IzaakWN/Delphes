from ROOT import TLorentzVector
from fold import fold

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel", "GenLevelCuts","Cuts", "CleanUp" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
    
    categoryData = [ ]
    
    # preparation for event selection
    muons20 = [ m for m in event.muons if m.PT>20 and abs(m.Eta) < 2.5 ]
    electrons25 = [ e for e in event.electrons if e.PT>25 and abs(e.Eta) < 2.5 ]
    leps = sorted(muons20+electrons25, key=lambda x: x.PT, reverse=True)
    event.leadingLeptons = leps[:5]
    event.bjets30 = [ jet for jet in event.jets if jet.BTag and jet.PT > 30 and abs(jet.Eta) < 2.5 ]
    for m in muons20:
        m.Mass = 0.1057
    for e in electrons25:
        e.Mass = 0.000511
    
    # clean-up cuts
    event.M_ll = 0
    event.M_jj = 0
    event.DeltaR_ll = 0
    event.DeltaR_jj = 0
    event.DeltaPhi_jjll = 0
    phi_ll = 0 
    if len(leps)>1: # TODO: check for opposite charge! 
        p_l1 = TLorentzVector(0,0,0,0)
        p_l2 = TLorentzVector(0,0,0,0)
        p_l1.SetPtEtaPhiM(leps[0].PT,leps[0].Eta,leps[0].Phi,leps[0].Mass)
        p_l2.SetPtEtaPhiM(leps[1].PT,leps[1].Eta,leps[1].Phi,leps[1].Mass)
        p_ll = p_l1 + p_l2
        event.M_ll = p_ll.M()
        phi_ll = p_ll.Phi()
        event.DeltaR_ll = TLorentzVector.DeltaR(p_l1,p_l2)    
    if len(event.bjets30)>1:
        p_j1 = TLorentzVector(0,0,0,0)
        p_j2 = TLorentzVector(0,0,0,0)
        p_j1.SetPtEtaPhiM(event.bjets30[0].PT,event.bjets30[0].Eta,event.bjets30[0].Phi,event.bjets30[0].Mass)
        p_j2.SetPtEtaPhiM(event.bjets30[1].PT,event.bjets30[1].Eta,event.bjets30[1].Phi,event.bjets30[1].Mass)
        p_jj = p_j1 + p_j2
        event.M_jj = p_jj.M()
        event.DeltaR_jj = TLorentzVector.DeltaR(p_j1,p_j2) 
        if phi_ll:
            event.DeltaPhi_jjll = fold( abs(phi_ll - (p_jj).Phi()) )
    gen_leptons15 = [ ]
    #hasElectron = event.electrons.GetEntries()

    # 0-1: generator level: single Wlnu and Hbb
    nLeptons = 0
    nBquarks = 0
    for particle in event.particles:
        D1 = particle.D1
        D2 = particle.D2
        if abs(particle.PID) in [23,24] and D1>=0 and D1<len(event.particles) and event.particles[D1]:
            for D in [ event.particles[particle.D1], event.particles[particle.D2] ]:
                if abs(D.PID) in [11,13,15]: # e, mu, tau
                    nLeptons+=1
        if abs(particle.PID) == 25 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
            if abs(event.particles[D1].PID) in [5]: # b-quark
                nBquarks+=2
    categoryData.append((nLeptons==2 and nBquarks==2) or event.particles.GetEntries()==0)
    categoryData.append((nLeptons==2 and nBquarks==2) or event.particles.GetEntries()==0) # same
    
    # 2: one muon or electron with PT > 20, 25 GeV -> TODO: also check opposite signs?
    #    MET > 20 GeV
    #    2 b-jets with PT > 30 GeV
    categoryData.append( len(leps)>1 and \
                         event.met[0].MET>20 and \
                         len(event.bjets30)>1 )

    # 3: clean-up cuts
    categoryData.append( event.M_ll<85 and 60<event.M_jj<160 and \
                         event.DeltaR_ll<2 and event.DeltaR_jj<3.1 and event.DeltaPhi_jjll>1.7 )
    
    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
    if category == 0:
        return categoryData[0]
        #      > GenLevel
    
    if category == 1:
        return categoryData[1]
        #      > GenLevel with cuts

    if category == 2:
        return categoryData[1] and categoryData[2]
        #      > signal            > selection

    if category == 3:
        return categoryData[1] and categoryData[2] and categoryData[3]
        #      > signal            > selection         > clean-up
        
    else:
        return False
