#! /usr/bin/env python
import ROOT 
from CPconfig import configuration
from array import array
from collections import namedtuple
tree = namedtuple("tree", ["tree","branches"])

def getArgSet(controlplots):
  assert isinstance(controlplots,list)
  merged = ROOT.RooArgSet()
  for ctrlplot in controlplots:
    merged.add(ctrlplot._obsSet)
  return merged

def runTest(path='../testfiles/', controlPlots=None):
  # these modules are only needed in that function, used for debugging.
  # so we only import them here.
  import Delphes
  import os
  import AnalysisEvent
  import EventSelection
  assert isinstance(controlPlots, BaseControlPlots)
  if os.path.isdir(path):
    dirList=os.listdir(path)
    files=[]
    for fname in dirList:
      files.append(path+fname)
  elif os.path.isfile(path):
    files=[path]
  else:
    files=[]
  events = AnalysisEvent.AnalysisEvent(files)
  EventSelection.prepareAnalysisEvent(events)
  controlPlots.beginJob()
  i = 0
  for event in events:
    if i%100==0 : print "Processing... event ", i
    controlPlots.processEvent(event)
    i += 1
  controlPlots.endJob()

class BaseControlPlots:
    """A class to create control plots"""
    
    def __init__(self, dir=None, purpose="generic", dataset=None, mode="plots"):
      """Initialize the ControlPlots, creating output file if needed. If no file is given, it means it is delegated."""
      self._mode = mode
      self._purpose = purpose
      # for plots
      if self._mode=="plots":
        # create output file if needed. If no file is given, it means it is delegated
        if dir is None:
          self._f = ROOT.TFile(configuration.defaultFilename+".root", "RECREATE")
          self._dir = self._f.mkdir(purpose)
        else :
          self._f = None
          self._dir = dir
        self._h_vector = { }
        self._t_vector = { } # IWN: for trees!
      # for ntuples
      if self._mode=="dataset":
        self._obsSet = ROOT.RooArgSet()
        if dataset is None:
          self._rds = ROOT.RooDataSet(configuration.RDSname, configuration.RDSname, self._obsSet)
	  self._ownedRDS = True
	else:
	  self._rds = dataset
	  self._ownedRDS = False
        self._rrv_vector = { }
        self._rooCategories = { }
    
    def beginJob(self):
      """Declare histograms, and for derived classes instantiate handles. Must be overloaded.""" 
      raise NotImplementedError

    def defineCategories(self, categories):
      """Define the categories, given a list of names. Only works for datasets"""
      if self._mode!="dataset": return
      for i, name in enumerate(categories):
        rc = ROOT.RooCategory("rc_"+self._purpose+"_"+str(i),name.split('/')[-1])
	rc.defineType("not_acc",0)
	rc.defineType("acc",1)
	self._rooCategories[i] = rc
	self._rds.addColumn(rc)
	self._obsSet.add(rc)

    def addHisto(self,*args):
      """Add one histograms to the list of products. Arguments are as for TH1F."""
      # this fills a distionnary name <-> histogram
      self._dir.cd()
      self._h_vector[args[0]] = ROOT.TH1F(*args)

    # IWN
    def addHisto2D(self,*args):
      """Add one 2D histograms to the list of products. Arguments are as for TH2F."""
      # this fills a distionnary name <-> 2D histogram
      self._dir.cd()
      self._h_vector[args[0]] = ROOT.TH2F(*args)

    # IWN
    def addTree(self,*args):
      """Add one TTree in a namedtuple to the list of products. Arguments are as for TTree."""
      # this fills a distionnary name <-> namedtuple tree
      self._dir.cd()
      self._t_vector[args[0]] = tree(ROOT.TTree(*args), [])

    # IWN
    def addBranch(self,*args):
      """Add one Branch to the tree in the list of products.
         Arguments are the tree and branch label."""
      # this adds a branch
      self._dir.cd()
      self._t_vector[args[0]].tree.Branch(args[1],0,args[1]+"/F")
      self._t_vector[args[0]].branches.append(self._t_vector[args[0]].tree.GetBranch(args[1]))

    def addVariable(self,*args):
      """Add one variable to the list of products. Arguments are as for RooRealVar."""
      # this fills a distionnary name <-> RooRealVar
      self._rrv_vector[args[0]] = ROOT.RooRealVar(self._purpose+args[0],*(args[1:]))
      self._obsSet.add(self._rrv_vector[args[0]])
      self._rds.addColumn(self._rrv_vector[args[0]])
    
    def add(self, *args):
      """Add one item to the list of products. Arguments are as for TH1F."""
      # TH1(name, title, nbinsx, xlow, xup)
      if self._mode=="plots":
        self.addHisto(*args)
      else:
        self.addVariable(*[args[i] for i in [0,1,3,4]])
    
    # IWN
    def add2D(self, *args):
      """Add one item to the list of products. Arguments are as for TH2F."""
      # TH2(name, title, nbinsx, xlow, xup, nbinsy, ylow, yup)
      if self._mode=="plots":
        self.addHisto2D(*args)
      else:
        self.addVariable(*[args[i] for i in [0,1,3,4]])

    def processEvent(self, event, weight = 1.):
      """process event and fill histograms"""
      self.fill(self.process(event),weight)
     
    def process(self, event):
      """Process event data to extract histogrammables. Must be overloaded."""
      raise NotImplementedError
      # this is just an example, we never get there
      # that method must return a dictionnary name <-> value that matches self._h_vector
      result = { }
      result["var1"] = 1.
      result["var2"] = 2.3
      result["var3"] = 5.711
      return result

    def setCategories(self, categories):
      """Set the categories, given a list of booleans. Only works for datasets"""
      if self._mode!="dataset": return
      for c, flag in enumerate(categories):
        if flag: self._rooCategories[c].setIndex(1)
	else: self._rooCategories[c].setIndex(0)

    def fillPlots(self, data, weight = 1.):
      """Fills histograms with the data provided as input."""
      for name,value in data.items():
        if name in self._t_vector: # for TTree:
        # One variable for each branch per event!
        # Respect the branch order when adding!
          if len(value) == len(self._t_vector[name].branches):
            vars = []
            for val,branch in zip(value,self._t_vector[name].branches):
              vars.append(array('f', [0]))
              branch.SetAddress(vars[-1])
              vars[-1][0] = val
            self._t_vector[name].tree.Fill()
        elif isinstance(value,list):
          for val in value:
            if isinstance(val,list):
              self._h_vector[name].Fill(val[0],val[1],weight) # (x,y,w) for TH2
            else:
              self._h_vector[name].Fill(val,weight) # for TH1
        else:
          self._h_vector[name].Fill(value,weight) # for TH1

    def fillRDS(self, data):
      """Fills roodataset with the data provided as input."""
      for rrv in self._rrv_vector:
        # data is not guaranteed to contain all variables,
        # so if we don't do this, these variables will keep the old value
        self._rrv_vector[rrv].setVal(-1000)
      for name,value in data.items():
        if isinstance(value,list):
	  #for now, we only store scalars, not vectors
	  pass
        else:
	  self._rrv_vector[name].setVal(value)
      if self._ownedRDS:
        self._rds.add(self._obsSet)  

    def fill(self, data, weight = 1.):
      """Fills whatever must be filled in"""
      if self._mode=="plots":
        self.fillPlots(data, weight)
      else:
        self.fillRDS(data)

    def endJob(self,level=""):
      """Save and close."""
      if self._mode=="plots":
        self._dir.cd()
        self._dir.Write()
        #c=ROOT.TCanvas("c","c",200,200)
	#for h in self._h_vector.values():
	#    h.Draw()
	#    c.SaveAs(configuration.defaultFilename+"_"+str(level)+"_"+self._dir.GetName()+"_"+h.GetName()+".pdf")
        if not self._f is None:
          self._f.Close()
      else:
        if self._ownedRDS:
          ws  = ROOT.RooWorkspace(self._purpose,self._purpose)
          getattr(ws,'import')(self._rds) 
          ws.writeToFile(configuration.defaultFilename+"_"+self._purpose+".root") 
