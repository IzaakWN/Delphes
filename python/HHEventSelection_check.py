# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "GenLevel", "orParticlesGetEntries", "ParticlesGetEntries" ]



def eventCategory(event):
    """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
    
    categoryData = [ ]

    categoryData.append(True)
    categoryData.append(event.particles.GetEntries()==0)
    
    return categoryData



def isInCategory(category, categoryData):
    """Check if the event enters category X, given the tuple computed by eventCategory."""
    
    if category == 0:
        return categoryData[0]
    
    if category == 0:
        return categoryData[1]
    
    if category == 0:
        return categoryData[0] or categoryData[1]

    else:
        return False
