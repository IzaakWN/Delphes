import time
t0 = time.time()
#!/usr/bin/env python

#######################################################################################
###  Option parsing and main routine  #################################################
#######################################################################################

from optparse import OptionParser
import sys
import os

usage="""%prog [options]"""
description="""A simple script to generate control plots."""
epilog="""Example:
./ControlPlots.py -i ./ -o controlPlots_demo.root --all
"""
parser = OptionParser(usage=usage,add_help_option=True,description=description,epilog=epilog)
parser.add_option("-c", "--conf", dest="conf", default=None,
                  help="Configuration file.")
parser.add_option("-i", "--inputPath", dest="path",
                  help="Read input file from DIR.", metavar="DIR")
parser.add_option("-o", "--output", dest='outputname', default=None,
                  help="Save output as FILE.", metavar="FILE")
parser.add_option("--all",action="store_true",dest="all",
                  help="Process all levels.")
parser.add_option("-l", "--level", dest="levels",
                  help="Specify a coma-separated list of levels to be processed. No space is allowed.")
parser.add_option("--Njobs", type="int", dest='Njobs', default="1",
                  help="Number of jobs when splitting the processing.")
parser.add_option("--jobNumber", type="int", dest='jobNumber', default="0",
                  help="Number of the job is a splitted set of jobs.")
parser.add_option("-t", "--txtFile", dest="txt", default=None,
                  help="Read input file from text file at DIR.", metavar="DIR")

(options, args) = parser.parse_args()

#special treatment of the config file... the rest of the options will be parsed in main.
if options.conf is not None:
  try:
    theUserConf = __import__(os.path.splitext(options.conf)[0])
  except:
    raise ImportError("%s is not a valid configuration file."%options.conf)
  else:
    os.environ["DelphesAnalysisCfg"]=options.conf
from CPconfig import configuration
if options.outputname is None:
  options.outputname = configuration.defaultFilename+".root"

import Delphes
import ROOT
import itertools
#import time
from importlib import import_module
from AnalysisEvent import AnalysisEvent
from BaseControlPlots import getArgSet
import EventSelection
import cProfile



def main(options):
  """simplistic program main"""
  # do basic arg checking
  if options.path is None:
    print "Error: no input path specified."
    parser.print_help()
    return
  levels = []
  if options.all:
    levels = range(EventSelection.eventCategories())
  elif not options.levels is None:
    levels= map(int,options.levels.split(','))
  levels.sort()
  if len(levels)==0:
    print "Error: no level specified for processing."
    parser.print_help()
    return
  if min(levels)<0:
    print "Error: levels must be positive integers."
    parser.print_help()
    return
  if max(levels)>=EventSelection.eventCategories():
    print "Error: last level is",EventSelection.eventCategories()-1
    parser.print_help()
    return
  if options.Njobs<1:
    print "Error: Njobs must be strictly positive."
    parser.print_help()
    return
  if options.jobNumber>=options.Njobs:
    print "Error: jobNumber must be strictly smaller than Njobs."
    parser.print_help()
    return
  # IWN
  if options.txt:
    if not options.txt.endswith(".txt"): 
      print "Error: file is not a txt file."
      parser.print_help()
      return
# if all ok, run the procedure
  runAnalysis(path=options.path,txt=options.txt,outputname=options.outputname, levels=levels, Njobs=options.Njobs, jobNumber=options.jobNumber)



#######################################################################################
### Central Routine: manage input/output, loop on events, manage weights and plots  ###
#######################################################################################

def runAnalysis(path, txt, levels, outputname="controlPlots.root", Njobs=1, jobNumber=1):
  """produce all the plots in one go"""

  # inputs
  dcapDir = False
  if "dcap://" in path:
    split = path.split("/")
    decapDir = os.path.isdir("/"+"/".join(split[3:]))
  if os.path.isdir(path) or decapDir:
    if txt: # IWN: use txt file with all names
      f = open(txt)
      dirList=list(itertools.islice([line[:-1] for line in f], jobNumber, None, Njobs))
      f.close()
    else:
      dirList=list(itertools.islice(os.listdir(path), jobNumber, None, Njobs))
    files=[]
    for fname in dirList:
      files.append(path+"/"+fname)
  elif os.path.isfile(path):
    files=[path]
  else:
    files=[path]

  # output
  output = ROOT.TFile(outputname, "RECREATE")
  if configuration.runningMode=="dataset":
    ROOT.RooAbsData.setDefaultStorageType(ROOT.RooAbsData.Tree)
    rds = ROOT.RooDataSet(configuration.RDSname, configuration.RDSname, ROOT.RooArgSet())

  # events iterator, plus configuration of standard collections and producers
  events = AnalysisEvent(files)
  EventSelection.prepareAnalysisEvent(events)

  # prepare the plots
  controlPlots=[]
  if configuration.runningMode=="plots":
    leafList = [None]*EventSelection.eventCategories()
    createDirectory(EventSelection.categoriesHierarchy(), output, leafList)
    for levelDir in leafList:
      levelPlots=[]
      for cp in configuration.controlPlots:
        levelPlots.append(getattr(import_module(cp.module),cp.classname)(dir=levelDir.mkdir(cp.label),mode="plots"))
      controlPlots.append(levelPlots)
  else:
    for cp in configuration.controlPlots:
      controlPlots.append(getattr(import_module(cp.module),cp.classname)(dir=None, mode="dataset", dataset=rds))

  # book histograms (separate iteration for clarity)
  if configuration.runningMode=="plots":
    for level in levels:
     for conf,cp in zip(configuration.controlPlots,controlPlots[level]):
       cp.beginJob(**conf.kwargs)
  else:
    for conf,cp in zip(configuration.controlPlots,controlPlots):
      cp.beginJob(**conf.kwargs)
    for cp in controlPlots[:1]:
      cp.defineCategories(EventSelection.categoryNames)

  # process events
  i = 0
  DeltaTb = 0
  tb = time.time()
  n = events.GetEntries()
  ETA = " "
  print "\n\n\t__%s_events_to_process.__" %n
  for event in events:
    # printout
    if i%1000==0 :
      if i%10000==0 :
        if DeltaTb>0:
#           ETA = " ETA: %s" % time.strftime("%H h. %M min. %S s.", time.gmtime( DeltaTb/i*(n-i) ))
#           runtime = "\n    Running for %s" % time.strftime("%H h. %M min. %S s.", time.gmtime(time.time()-t0))
#           print runtime.replace(" 00 h.","").replace("for 0","for ") + ETA.replace(" 00 h.","").replace(": 0",": ")
          (m,s) = divmod(time.time()-t0,60)
          (h,m) = divmod(m,60)
          runtime = "\n    Running for %i h. %i min. %i s." % (h,m,s)
          (m,s) = divmod(DeltaTb/i*(n-i),60)
          (h,m) = divmod(m,60)
          ETA = " ETA: %i h. %i min. %i s." % (h,m,s)
          print runtime.replace(" 0 h.","") + ETA.replace(" 0 h.","")
      DeltaTb += time.time()-tb
      print "%d%%: Processing... event %d. Last batch in %f s." % (i*100/n,i,(time.time()-tb))
      tb = time.time()
    i += 1
    if configuration.runningMode=="plots":
      # loop on channels
      plots = filter(lambda x: EventSelection.isInCategory(x,event.category) ,levels)
      # process the event once (for the first level)
      selectionPlotsData=[]
      for level in plots[:1]:
        for cp in controlPlots[level]:
          selectionPlotsData.append(cp.process(event))
      # fill the histograms
      for level in plots:
        for cp, data in zip(controlPlots[level],selectionPlotsData):
          cp.fill(data, event.weight(category=level))
    else:
      for cp in controlPlots[:1]:
        # set categories (first CP only)
        cp.setCategories(map(lambda c: EventSelection.isInCategory(c, event.category),range(EventSelection.eventCategories())))
      for cp in controlPlots:
        # process event (all CP)
        cp.processEvent(event)
      # add to the dataset
      rds.add(getArgSet(controlPlots))
  
  # save all
  if configuration.runningMode=="plots":
    for level in levels:
     for cp in controlPlots[level]: 
       cp.endJob(level)
  else:
   for cp in controlPlots: 
     cp.endJob()

  # for dataset, write the merged RDS to file
  if configuration.runningMode=="dataset":
    output.cd()
    ws_ras = ROOT.RooWorkspace(configuration.WSname, configuration.WSname)
    getattr(ws_ras,'import')(rds.get())
    output.Add(ws_ras)
    ws_ras.Write()
    rds.tree().Write()
  
  # close the file
  output.Close()

  print "\nDone. Only took %s!\n" % time.strftime("%H:%M:%S", time.gmtime(time.time()-t0))



def createDirectory(dirStructure, directory, leafList):
  """Recursively creates the directories for the various stages"""
  for key,item in dirStructure.iteritems():
    if isinstance(item, dict):
      createDirectory(item, directory.mkdir(key), leafList)
    else:
      leafList[item]=directory.mkdir("stage_"+str(item),key)



#######################################################################################
### Program bootstrap  ################################################################
#######################################################################################

if __name__ == "__main__":
  main(options)
  #cProfile.run('main(options)', 'controlPlots.prof')

