#very simple EventSelection class aimed at demonstrating the
#typical implementation of an EventSelection class

#On purpose, the categories are not in any "logical" order, and there is some redundant check when testing the category.
#This is mostly for illustration.

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel", "Lepton4Jets" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
    
    categoryData = [ ]
    
    # 0: Pt of the leading muon > 20 GeV
    if event.muons.GetEntries()>0:
        categoryData.append(event.muons[0].PT>20.)
    else:
        categoryData.append(False)

    # 1: Pt of the leading electron > 20 GeV
    if event.electrons.GetEntries()>0:
        categoryData.append(event.electrons[0].PT>20.)
    else:
        categoryData.append(False)

    # 2: Pt of leading 4 jets > 30 GeV
    if event.jets.GetEntries()>3:
        categoryData.append(event.jets[3].PT>30.)
    else:
        categoryData.append(False)

#    # 3: generator level single lepton
#    nLeptons=0
#    nBquarks=0
#    for particle in event.particles:
#        D1 = particle.D1
#        if abs(particle.PID) == 24 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
#            if abs(event.particles[D1].PID) in [11,13,15]: # e, mu, tau
#                nLeptons+=1
#        if abs(particle.PID) == 25 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
#            if abs(event.particles[D1].PID) in [5]: # b-quark
#                nBquarks+=2
#    categoryData.append((nLeptons==1 and nBquarks==2) or event.particles.GetEntries()==0)

    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
    if category==0:
        return True #categoryData[3]
    if category==1:
        return (categoryData[0] or categoryData[1]) and categoryData[2] # for ttbar no categoryData[3]
    else:
        return False
