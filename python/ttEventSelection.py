from ROOT import TLorentzVector as TLV
from itertools import combinations
from fold import fold

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel", "Selection20","QuarksCut", "NPUCut", "QuarksNPUCut" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
    
    categoryData = [ ]
    event.cleanedJets = [ jet for jet in event.puppijets ][:15]
    
    muons20 = [ m for m in event.muons if m.PT>20 and abs(m.Eta)<2.5 ]
    electrons25 = [ e for e in event.electrons if e.PT>25 and abs(e.Eta)<2.5 ]
    leps = sorted(muons20+electrons25, key=lambda x: x.PT, reverse=True)
    event.leadingLeptons = leps[:5]
    
    for m in muons20:
        m.Mass = 0.1057
        m.TLV = TLV()
        m.TLV.SetPtEtaPhiM(m.PT, m.Eta, m.Phi, m.Mass)
    for e in electrons25:
        e.Mass = 0.000511
        e.TLV = TLV()
        e.TLV.SetPtEtaPhiM(e.PT, e.Eta, e.Phi, e.Mass)
    for jet in event.cleanedJets:
        jet.TLV = TLV()
        jet.TLV.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

    for lepton in leps: # remove all leptons from jets
        for jet in event.cleanedJets:
            if TLV.DeltaR(lepton.TLV,jet.TLV) < 0.2:
                 event.cleanedJets.remove(jet)

    event.cleanedJets20 = [ jet for jet in event.cleanedJets if jet.PT > 20  and abs(jet.Eta) < 2.5 ]
    event.cleanedJets30 = [ jet for jet in event.cleanedJets20 if jet.PT > 30 ]
    
    # add btag to puppijets
    for bjet in [ jet for jet in event.jets if jet.BTag and jet.PT > 20 ]:
        bjet.TLV = TLV()
        bjet.TLV.SetPtEtaPhiM(bjet.PT, bjet.Eta, bjet.Phi, bjet.Mass)
        for jet in event.cleanedJets20:
            if TLV.DeltaR(bjet.TLV,jet.TLV) < 0.2:
                jet.BTag = bjet.BTag
    event.bjets30 = [ jet for jet in event.cleanedJets30 if jet.BTag ]

    # 0: generator level: single Wlnu and Hbb
    event.particle_dict = { 'H bosons' : [ ], 't quarks' : [ ],
                            'W bosons' : [ ], 'b quarks' : [ ],
                            'W quarks' : [ ], 'leptons'  : [ ], 'neutrinos' : [ ] }
    for particle in event.particles:
        D1 = particle.D1
        if abs(particle.PID) == 24 and 0 <= D1 < len(event.particles) and event.particles[D1]:
            event.particle_dict['W bosons'].append(particle)
            if abs(event.particles[D1].PID) in [11,13]: # e, mu
                event.particle_dict['leptons'].append(event.particles[D1])
                event.particle_dict['neutrinos'].append(event.particles[particle.D2])
            elif abs(event.particles[D1].PID) in [1,2,3,4,5]: # quarks
                event.particle_dict['W quarks'].extend([ event.particles[D1], event.particles[particle.D2] ])
#             elif abs(event.particles[D1].PID) in [12,14]:
#                 print "WARNING! D1 PID in [ 12, 14 ]"
        elif abs(particle.PID) ==  6 and 0 <= D1 < len(event.particles) and event.particles[D1]:
            event.particle_dict['t quarks'].append(particle)
            event.particle_dict['b quarks'].append(event.particles[particle.D2])
            
    categoryData.append( len(event.particle_dict['leptons']) == 1 and \
                         len(event.particle_dict['b quarks']) == 2 )
                         
    # 1: preselection cuts
    categoryData.append( len(leps) == 1 and \
                         event.met[0].MET > 20 and \
                         len(event.cleanedJets20) > 3 and \
                         len(event.bjets30) > 1 )
     
    # 2: pT, eta cuts on W -> qq
    categoryData.append( len([q for q in event.particle_dict['W quarks'] if q.PT > 25 and q.Eta < 2]) == 2 )
    
    # 3: NPU < 126
    categoryData.append( event.npu[0].HT < 126 )

    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
    if category == 0:
        return categoryData[0] #and categoryData[2] and categoryData[3] and categoryData[6] and categoryData[7]
        #      > signal
    
    if category == 1:
        return categoryData[0] and categoryData[1]
        #      > signal            > preselection
    
    if category == 2:
        return categoryData[0] and categoryData[1] and categoryData[2]
        #      > signal            > preselection      > W quark cuts
    
    if category == 3:
        return categoryData[0] and categoryData[1] and categoryData[3]
        #      > signal            > preselection      > NPU < 126
    
    if category == 4:
        return categoryData[0] and categoryData[1] and categoryData[2] and categoryData[3]
        #      > signal            > preselection      > W quark cuts      > NPU < 126
        
    else:
        return False

