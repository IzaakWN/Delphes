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
  eventSelection = "HHEventSelection"

  # control plot classes
  controlPlots = [ controlPlot("selection","EventSelectionControlPlots","EventSelectionControlPlots", { }),
                   controlPlot("gen","GenControlPlots_topo","GenControlPlots", { }),
                   controlPlot("cleanup","CleanUpControlPlots","CleanUpControlPlots", { }),
                   controlPlot("jets","JetControlPlots_check","JetControlPlots", { }),
                 ]

  # event content: lists of eventCollection, eventProducer, and eventWeight objects respectively.
  eventCollections = [ eventCollection("muons","Muon"), 
                       eventCollection("electrons","Electron"), 
                       #eventCollection("met","MissingET"),
                       eventCollection("met","PuppiMissingET"),
                       eventCollection("jets","Jet"),
                       eventCollection("puppijets","PuppiJet"),
                       eventCollection("particles","Particle"),
                       eventCollection("npu","NPU")
                     ]
  eventProducers   = [ eventProducer("category","HHEventSelection","eventCategory",{ }) ] 
  eventWeights     = [ ]

class eventDumpConfig:
  # fine-tuning of the event content for display
  productsToPrint   = [ "category" ] # list of product to display (use the producer label)
  collectionsToHide = [ "tracks" ] # collections used in the analysis but not printed (use the collection label) 

