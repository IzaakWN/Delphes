# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
    
    categoryData = [ ]

#    # preparation for gen level selection
#    nLeptons = 0
#    nBquarks = 0
#    nBquarks15 = 0
#    for particle in event.particles:
#        D1 = particle.D1
#        D2 = particle.D2
#        # W, Z -> lv
#        if abs(particle.PID) in [23,24] and D1>=0 and D1<len(event.particles) and event.particles[D1]:
#            for D in [ event.particles[D1], event.particles[D2] ]:
#                if abs(D.PID) in [11,13,15]: # e, mu, tau
#                    nLeptons+=1
#        # H -> bb
#        if abs(particle.PID) == 25 and D1>=0 and D1<len(event.particles) and event.particles[D1]:
#            if abs(event.particles[D1].PID) in [5]: # b-quark
#                nBquarks+=2

    categoryData.append(True)
    # event.particles.GetEntries()==0
    
    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""

    # dileptonic final state
    
    if category == 0:
        return categoryData[0]
        #      > GenLevel

    else:
        return False
