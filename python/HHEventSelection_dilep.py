from ROOT import TLorentzVector as TLV
from itertools import combinations
from fold import fold

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel_dilep", "GenLevelCuts_dilep", "Selection_dilep", "CleanUp_dilep", "StrictSelection_dilep",
                  "GenLevel", "GenLevelCuts","Cuts", "CleanUp", "StrictSelection" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong"""
    
    categoryData = [ ]
    
    # preparation for event selection
    muons20 = [ m for m in event.muons if m.PT>20 and abs(m.Eta) < 2.5 ]
    electrons25 = [ e for e in event.electrons if e.PT>25 and abs(e.Eta) < 2.5 ]
    leps = sorted(muons20+electrons25, key=lambda x: x.PT, reverse=True)
    event.leadingLeptons = leps[:5]
    event.jets20 = [ j for j in event.jets if j.PT > 20 and abs(j.Eta) < 2.5 ]
    event.bjets30 = [ j for j in event.jets if j.PT > 30 and abs(j.Eta) < 2.5 and j.BTag ]
    for m in muons20:
        m.Mass = 0.1057
    for e in electrons25:
        e.Mass = 0.000511
    for l1, l2 in combinations(leps[:3],2): # take opposite charge
        if l1.Charge*l2.Charge < 0:
            leps = [l1,l2]
            break
    
    # preparation for clean-up
    event.M_ll = 0
    event.M_bb = 0
    event.DeltaR_ll = 100 # >>> pi
    event.DeltaR_bb = 100 # >>> pi
    event.DeltaPhi_bbll = 0
    p_ll = None
    if len(leps)>1:
        p_l1 = TLV(0,0,0,0)
        p_l2 = TLV(0,0,0,0)
        p_l1.SetPtEtaPhiM(leps[0].PT,leps[0].Eta,leps[0].Phi,leps[0].Mass)
        p_l2.SetPtEtaPhiM(leps[1].PT,leps[1].Eta,leps[1].Phi,leps[1].Mass)
        p_ll = p_l1 + p_l2
        event.M_ll = p_ll.M()
        event.DeltaR_ll = TLV.DeltaR(p_l1,p_l2)
    if len(event.bjets30)>1:
        p_b1 = TLV(0,0,0,0)
        p_b2 = TLV(0,0,0,0)
        p_b1.SetPtEtaPhiM(event.bjets30[0].PT,event.bjets30[0].Eta,event.bjets30[0].Phi,event.bjets30[0].Mass)
        p_b2.SetPtEtaPhiM(event.bjets30[1].PT,event.bjets30[1].Eta,event.bjets30[1].Phi,event.bjets30[1].Mass)
        p_bb = p_b1 + p_b2
        event.M_bb = p_bb.M()
        event.DeltaR_bb = TLV.DeltaR(p_b1,p_b2)
        if p_ll:
            event.DeltaPhi_bbll = fold( abs(p_ll.Phi() - (p_bb).Phi()) )

    # preparation for gen level selection
    nLeptons = 0
    nBquarks = 0
    gen_leptons15 = [ ]
    gen_quarks15 = [ ]
    nBquarks15 = 0
    for particle in event.particles:
        D1 = particle.D1
        D2 = particle.D2
        # W, Z -> lv
        if abs(particle.PID) in [23,24] and 0 <= D1 < len(event.particles) and event.particles[D1]:
            for D in [ event.particles[D1], event.particles[D2] ]:
                if abs(D.PID) in [11,13]:#,15]: # e, mu, tau
                    if D.PT > 15 and abs(D.Eta) < 2.5:
                        gen_leptons15.append(D)
                    nLeptons+=1
        # H -> bb
        if abs(particle.PID) == 25 and 0 <= D1 < len(event.particles) and event.particles[D1]:
            if abs(event.particles[D1].PID) in [5]: # b-quark
                for D in [ event.particles[D1], event.particles[D2] ]:
                    if D.PT > 15: # and abs(D.Eta) < 2.5:
                      nBquarks15+=1
                nBquarks+=2

    # preparation for gen level cuts
    DeltaR_ll_gen = 100
#    DeltaR_ql_gen = 100
    if len(gen_leptons15)==2:
        p1 = TLV(0,0,0,0)
        p2 = TLV(0,0,0,0)
        p1.SetPtEtaPhiM(gen_leptons15[0].PT,gen_leptons15[0].Eta,gen_leptons15[0].Phi,gen_leptons15[0].Mass)
        p2.SetPtEtaPhiM(gen_leptons15[1].PT,gen_leptons15[1].Eta,gen_leptons15[1].Phi,gen_leptons15[1].Mass)
        DeltaR_ll_gen = TLV.DeltaR(p1,p2)
#    if len(gen_leptons15)==1 and len(gen_quarks15)==2:
#        pl = TLV(0,0,0,0)
#        pqs = [ TLV(0,0,0,0), TLV(0,0,0,0) ]
#        pl.SetPtEtaPhiM(gen_leptons15[0].PT,gen_leptons15[0].Eta,gen_leptons15[0].Phi,gen_leptons15[0].Mass)
#        pqs[0].SetPtEtaPhiM(gen_quarks15[0].PT,gen_quarks15[0].Eta,gen_quarks15[0].Phi,gen_quarks15[0].Mass)
#        pqs[1].SetPtEtaPhiM(gen_quarks15[1].PT,gen_quarks15[1].Eta,gen_quarks15[1].Phi,gen_quarks15[1].Mass)
#        DeltaR_ql_gen = min(TLV.DeltaR(pq,pl) for pq in pqs) 

    # 0-1: generator level: double Wlnu and Hbb
    categoryData.append((nLeptons==2 and nBquarks==2)) #or event.particles.GetEntries()==0)
    categoryData.append((len(gen_leptons15)==2 and nBquarks15==2 and DeltaR_ll_gen<2.5) or event.particles.GetEntries()==0)
    
    # 2: two muons or electrons with PT > 20, 25 GeV
    #    MET > 20 GeV
    #    at least 2 b-jets with PT > 30 GeV
    categoryData.append( len(leps)>1 and \
                         event.met[0].MET>20 and \
                         len(event.bjets30)>1 )
    
    # 3: two muons or electrons with PT > 20, 25 GeV
    #    MET > 20 GeV
    #    2 b-jets with PT > 30 GeV
    categoryData.append( len(leps)==2 and \
                         event.met[0].MET>20 and \
                         # require no other jets?
                         len(event.bjets30)==2 )

    # 4: clean-up cuts
    categoryData.append( event.M_ll<85 and 60<event.M_bb<160 and \
                         event.DeltaR_ll<2 and event.DeltaR_bb<3.1 and event.DeltaPhi_bbll>1.7 )
    
    # 5-6: generator level: single Wlnu, Wjj and Hbb
    categoryData.append((nLeptons==1 and nBquarks==2)) # or event.particles.GetEntries()==0)
    categoryData.append((len(gen_leptons15)==1 and nBquarks15==2) or event.particles.GetEntries()==0)
#    categoryData.append((len(gen_leptons15)==1 and nBquarks15==2 and DeltaR_ql_gen<2.5) or event.particles.GetEntries()==0)

    # 7: one muon or electron with PT > 20, 25 GeV
    #    MET > 20 GeV
    #    at least 2 jets
    #    at least 2 b-jets with PT > 30 GeV
    categoryData.append( len(leps)==1 and \
                         event.met[0].MET>20 and \
                         len(event.jets20)>3 and \
                         len(event.bjets30)>1 )

    # 8: one muon or electron with PT > 20, 25 GeV
    #    MET > 20 GeV
    #    2 jets
    #    2 b-jets with PT > 30 GeV
    categoryData.append( len(leps)==1 and \
                         event.met[0].MET>20 and \
                         len(event.jets20)==4 and \
                         len(event.bjets30)>1 )

    # 9: clean-up cuts
    categoryData.append( 60<event.M_bb<160 and \
                         event.DeltaR_bb<3.1 )
    
    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""


    # dileptonic final state
    
    if category == 0:
        return categoryData[0]
        #      > GenLevel
    
    if category == 1:
        return categoryData[1]
        #      > GenLevel with cuts

    if category == 2:
        return categoryData[1] and categoryData[2]
        #      > GenLevel          > selection

    if category == 3:
        return categoryData[1] and categoryData[2] and categoryData[4]
        #      > GenLevel          > selection         > clean-up

    if category == 4:
        return categoryData[1] and categoryData[3] and categoryData[4]
        #      > GenLevel          > strict selection  > clean-up
    
    
    # semileptonic final state
    
    if category == 5:
        return categoryData[5]
        #      > GenLevel
    
    if category == 6:
        return categoryData[6]
        #      > GenLevel with cuts

    if category == 7:
        return categoryData[6] and categoryData[7]
        #      > GenLevel          > selection

    if category == 8:
        return categoryData[6] and categoryData[7] and categoryData[9]
        #      > GenLevel          > selection         > clean-up

    if category == 9:
        return categoryData[6] and categoryData[8] and categoryData[9]
        #      > GenLevel          > strict selection  > clean-up


    else:
        return False
