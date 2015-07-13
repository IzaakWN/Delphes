#very simple EventSelection class aimed at demonstrating the 
#typical implementation of an EventSelection class

#On purpose, the categories are not in any "logical" order, and there is some redundant check when testing the category.
#This is mostly for illustration.

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "MuonChannel/Muon", "ElectronChannel/Electron", "MuonChannel/4Jets", "ElectronChannel/4Jets" ]

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
  # 3: generator level single lepton
  nLeptons=0
  nBquarks=0
  for particle in event.particles:
          if abs(particle.PID) == 24:
	     if abs(event.particles[particle.D1].PID) in [11,13,15]:
	       nLeptons+=1
          if abs(particle.PID) == 25:
	     if abs(event.particles[particle.D1].PID) in [5]:
	        nBquarks+=2
  categoryData.append((nLeptons==1 and nBquarks==2) or event.particles.GetEntries()==0)
    
  # DONE
  return categoryData

def isInCategory(category, categoryData):
  """Check if the event enters category X, given the tuple computed by eventCategory."""
  if category==0:
    return categoryData[0]==True and categoryData[3]==True
  elif category==1:
    return categoryData[1]==True and categoryData[3]==True
  elif category==2:
    return isInCategory(0,categoryData) and categoryData[2]==True and categoryData[3]==True
  elif category==3:
    return isInCategory(1,categoryData) and categoryData[2]==True and categoryData[3]==True
  else:
    return False
