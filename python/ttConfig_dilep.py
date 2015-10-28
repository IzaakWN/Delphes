#configuration of the ControlPlot machinery

from collections import namedtuple
controlPlot     = namedtuple("controlPlot",    ["label","module","classname","kwargs"])
eventCollection = namedtuple("eventCollection",["label","collection"])
eventProducer   = namedtuple("eventProducer",  ["label","module","function","kwargs"])
eventWeight     = namedtuple("eventWeight",    ["label","module","classname","kwargs"])

class configuration:
  # default I/O
  defaultFilename = "controlPlots"
  RDSname = "rds_delphes"
  WSname = "workspace_ras"

  # mode: plots or dataset
  runningMode = "plots"
  #runningMode = "dataset"

  # event selection class
  eventSelection = "ttEventSelection_dilep"

  # control plot classes
  controlPlots = [ controlPlot("selection","EventSelectionControlPlots","EventSelectionControlPlots", { }),
                   controlPlot("leptons","LeptonControlPlots","LeptonControlPlots", { }) ]
                   #controlPlot("cleanup","CleanUpControlPlots_dilep","CleanUpControlPlots", { }),
                   #controlPlot("gen","GenControlPlots","GenControlPlots", { }) ]
                   #controlPlot("jets","JetControlPlots","JetControlPlots", { }),
                   #controlPlot("leptons","LeptonControlPlots","LeptonControlPlots", { }),
                   #controlPlot("reco","RecoControlPlots","RecoControlPlots", { }),
                   #controlPlot("reco2","RecoControlPlots2","RecoControlPlots2", { }),
                   #controlPlot("match","MatchControlPlots","MatchControlPlots", { }),
                   #controlPlot("res","ResControlPlots","ResControlPlots", { }) ]

  # event content: lists of eventCollection, eventProducer, and eventWeight objects respectively.
  eventCollections = [ eventCollection("muons","Muon"), 
                       eventCollection("electrons","Electron"), 
                       eventCollection("met","MissingET"),
                       eventCollection("jets","Jet"),
                       eventCollection("particles","Particle") ]
  eventProducers   = [ eventProducer("category","ttEventSelection_dilep","eventCategory",{ }) ] 
  eventWeights     = [ ]

class eventDumpConfig:
  # fine-tuning of the event content for display
  productsToPrint   = [ "category" ] # list of product to display (use the producer label)
  collectionsToHide = [ "tracks" ] # collections used in the analysis but not printed (use the collection label) 

