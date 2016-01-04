from optparse import OptionParser
import sys
import os
import ConfigParser
import ROOT
from ROOT import TFile, gDirectory, TChain, TMVA, TCut, TCanvas, THStack, TH1F
from array import array
from copy import deepcopy
from math import sqrt
import CMS_lumi, tdrstyle
from HHPlotterTools import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = "Simulation preliminary"
CMS_lumi.cmsTextSize = 0.65
CMS_lumi.outOfFrame = True
tdrstyle.setTDRStyle()

# Manual: http://tmva.sourceforge.net/docu/TMVAUsersGuide.pdf
# Method options: http://tmva.sourceforge.net/optionRef.html
# Examples in python:
#   https://aholzner.wordpress.com/2011/08/27/a-tmva-example-in-pyroot/
#   https://dbaumgartel.wordpress.com/2014/03/14/machine-learning-examples-scikit-learn-versus-tmva-cern-root/
# Tutorial: https://indico.cern.ch/event/395374/other-view?view=standard#20151109.detailed
# Warning: use ROOT 34.0.0 or newer for larger buffer for the xml reader!
#
# BDT parameters to tune: number of cycles, tree depth, ...
#   - AdaBoost:         https://en.wikipedia.org/wiki/AdaBoost
#   - AdaBoostBeta=0.5: learning rate
#   - Gini-coefficient: https://en.wikipedia.org/wiki/Gini_coefficient
#                       used to select the best variable to be used in each tree node
#   - nTrees=800:    number of boost steps, too large mainly costs time or cause overtraining
#   - MaxDepth=3:  ~ 2-5, maximum tree depth (depends on the interaction of variables)
#   - MinNodeSize=5%
#   - nCuts=20:  grid points in variable range to find optimal cut in node splitting
#
# MLP parameters to tune: number of neurons on each hidden layer, learning rate, activation function
#   - VarTransform=N: normalize variables
#   - HiddenLayers: number of nodes in NN layers
#         N     = one hidden layer with N nodes (N = number of variables)
#         N,N   = two hidden layers
#         N+2,N = two hidden layers with the N+2 nodes in the first hidden layer
#   - LearningRate=0.02
#

# extra options
argv = sys.argv
parser = OptionParser()
parser.add_option("-t", "--test", dest="test", default=False, action="store_true",
                  help="Only train one configuration as test.")
parser.add_option("-p", "--onlyPlot", dest="onlyPlot", default=False, action="store_true",
                  help="Only plot, don't go through training.")
(opts, args) = parser.parse_args(argv)

# list of methods
Methods = [ ("BDT","BDT"),
            ("BDT","BDTTuned"),
#            ("BDT","BDTPreselection"),
#            ("BDT","BDTNTrees"),
#            ("BDT","BDTMaxDepth"),
#            ("BDT","BDTCuts"),
#            ("BDT","BDTBoost"),
            ("BDT","BDTBoost1"),
            #("BDT","BDTBoost2"),
            ("BDT","BDTBoost3"),
            ("BDT","BDTBoost4"),
#            ("BDT","BDTNodeSize"),
#            ("MLP","MLPTanh"),
#            ("MLP","MLPLearningRate"),
#            ("MLP","MLPNodes"),
#            ("MLP","MLPNodes1"),
#            ("MLP","MLPNodes2"),
            #("MLP","MLPSigmoid")
          ]
methods = [ method[1] for method in Methods ]

# file with trees
file_HH = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_all.root")
file_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_all.root")
treeS1 = file_HH.Get("stage_1/cleanup/cleanup")
treeB1 = file_tt.Get("stage_1/cleanup/cleanup")
treeS2 = file_HH.Get("stage_2/cleanup/cleanup")
treeB2 = file_tt.Get("stage_2/cleanup/cleanup")
treeS3 = file_HH.Get("stage_3/cleanup/cleanup")
treeB3 = file_tt.Get("stage_3/cleanup/cleanup")
treeS2_gen = file_HH.Get("stage_2/gen/gen")
treeB2_gen = file_tt.Get("stage_2/gen/gen")

h0_S = file_HH.Get("stage_0/selection/category") # ~ 166483
h0_B = file_tt.Get("stage_0/selection/category") # ~ 164661
print h0_S.GetBinContent(1)
print h0_B.GetBinContent(1)
S_tot = 166483.0 #h0_S.GetBinContent(1)
B_tot = 164661.0 #h0_B.GetBinContent(1)
S1 = treeS1.GetEntries() #h0_S.GetBinContent(2)
B1 = treeB1.GetEntries() #h0_B.GetBinContent(2)
S2 = treeS2.GetEntries() #h0_S.GetBinContent(3)
B2 = treeB2.GetEntries() #h0_B.GetBinContent(3)
S3 = h0_S.GetBinContent(4) # treeS3.GetEntries()
B3 = h0_B.GetBinContent(4) # treeB3.GetEntries()
print "S_tot = %i, S1 = %i, S2 = %i, S3 = %i" % (S_tot,S1,S2,S3)
print "B_tot = %i, B1 = %i, B2 = %i, B3 = %i" % (B_tot,B1,B2,B3)

# yields to calculate significance
L = 3000 # / fb
sigma_S = 40 # fb
sigma_B = 984500 # fb
N_S = sigma_S * L * 0.0715 # expected number of events
N_B = sigma_B * L * 0.2873
print "P_initial = %.4f, S = %.1f, B = %.1f" % (N_S/sqrt(1+N_B),N_S,N_B)
print "P1 = %.4f, S = %.1f, B = %.1f" % (N_S*S1/S_tot/sqrt(1+N_B*B1/B_tot),N_S*S1/S_tot,N_B*B1/B_tot)
print "P2 = %.4f, S = %.1f, B = %.1f" % (N_S*S2/S_tot/sqrt(1+N_B*B2/B_tot),N_S*S2/S_tot,N_B*B2/B_tot)




class configuration(object):

    def __init__(self, name, varNames, stage, gen=False):
        self.name = name
        self.varNames = varNames
        self.treeS = None
        self.treeB = None
        self.S = 0
        self.B = 0
        self.hist_effs = [ ]
        self.hist_effs_train = [ ]
        self.stage = stage
#        self.significances
        if stage==1:
            self.treeS = treeS1
            self.treeB = treeB1
            self.S = treeS1.GetEntries()
            self.B = treeB1.GetEntries()
        elif stage==2:
            if gen:
                self.treeS = treeS2_gen
                self.treeB = treeB2_gen
                self.S = treeS2.GetEntries()
                self.B = treeB2.GetEntries()
            else:
                self.treeS = treeS2
                self.treeB = treeB2
                self.S = treeS2.GetEntries()
                self.B = treeB2.GetEntries()
        elif stage==3:
            self.treeS = treeS3
            self.treeB = treeB3
            self.S = treeS3.GetEntries()
            self.B = treeB3.GetEntries()
        # check existence of variables
        if self.treeS and self.treeB:
            listS = self.treeS.GetListOfBranches()
            listB = self.treeB.GetListOfBranches()
            for var in varNames:
                if (var not in listS) or (var not in listB):
                    sys.exit(">>> ERROR: "+self.name+": variable \""+var+"\" not in the tree!")



def train(config):
    print "\n>>> train with configuration "+config.name

    TMVA.Tools.Instance()
    f_out = TFile("MVA/HH_MVA_"+config.name+".root","RECREATE")

    factory = TMVA.Factory( "TMVAClassification", f_out,
                            ":".join([ "!V",
                            "!Silent",
                            "Color",
                            "DrawProgressBar",
                            "Transformations=I;D;P;G,D",
                            "AnalysisType=Classification" ]) )

    for name in config.varNames:
        if name[0] == "N":
            factory.AddVariable(name,"I")
        else:
            factory.AddVariable(name,"F")

    factory.AddSignalTree(config.treeS)
    factory.AddBackgroundTree(config.treeB)

    cut_S = TCut("")
    cut_B = TCut("")
    factory.PrepareTrainingAndTestTree( cut_S, cut_B,
                                        ":".join([ "!V",
                                                   "nTrain_Signal=0",
                                                   "nTrain_Background=0",
                                                   "SplitMode=Random",
                                                   "NormMode=NumEvents" ]) )

#    # LD: Linear Classifier
#    factory.BookMethod(TMVA.Types.kLD, "LD", "H:!V")

    # BDT: Boosted Decision Tree
    factory.BookMethod(TMVA.Types.kBDT, "BDT", "!H:!V" )
    # BDTTuned
    factory.BookMethod(TMVA.Types.kBDT, "BDTTuned",
                       ":".join([ "!H","!V",
                                  "NTrees=1500",
#                                  "MinNodeSize=2.%", # 2.%
#                                  "nEventsMin=200",
                                  "MaxDepth=3", # 3 -> 5 -> 3
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.08", # 0.1 -> 0.05
                                  "SeparationType=GiniIndex",
                                  "nCuts=70" # 20 -> 70 -> 100
                                 ]) )
#    # BDTPreselection
#    factory.BookMethod(TMVA.Types.kBDT, "BDTPreselection",
#                       ":".join([ "!H","!V",
#                                  "NTrees=1500",
#                                  "DoPreselection=True",
##                                  "MinNodeSize=2.%", # 2.%
##                                  "nEventsMin=200",
#                                  "MaxDepth=3", # 3 -> 5 -> 3
#                                  "BoostType=AdaBoost",
#                                  "AdaBoostBeta=0.05", # 0.1 -> 0.05
#                                  "SeparationType=GiniIndex",
#                                  "nCuts=80" # 20 -> 70 -> 100
#                                 ]) )
#    # BDTNTrees
#    factory.BookMethod(TMVA.Types.kBDT, "BDTNTrees",
#                       ":".join([ "!H","!V",
#                                  "NTrees=1500", # 2000 -> 1500
##                                  "MinNodeSize=2.%",
##                                  "nEventsMin=200",
#                                  "MaxDepth=3",
#                                  "BoostType=AdaBoost",
#                                  "AdaBoostBeta=0.05",
#                                  "SeparationType=GiniIndex",
#                                  "nCuts=80"
#                                 ]) )
#    # BDTMaxDepth
#    factory.BookMethod(TMVA.Types.kBDT, "BDTMaxDepth",
#                       ":".join([ "!H","!V",
#                                  "NTrees=2000",
##                                  "MinNodeSize=2.%",
##                                  "nEventsMin=200",
#                                  "MaxDepth=2", # 3 -> 5 -> 2
#                                  "BoostType=AdaBoost",
#                                  "AdaBoostBeta=0.05",
#                                  "SeparationType=GiniIndex",
#                                  "nCuts=80"
#                                 ]) )

    # BDTBoost1
    factory.BookMethod(TMVA.Types.kBDT, "BDTBoost1",
                       ":".join([ "!H","!V",
                                  "NTrees=1500",
#                                  "MinNodeSize=2.%",
#                                  "nEventsMin=200",
                                  "MaxDepth=3",
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.10", # 0.1 -> 0.05 -> 0.01 -> 0.1
                                  "SeparationType=GiniIndex",
                                  "nCuts=70"
                                 ]) )
#    # BDTBoost2
#    factory.BookMethod(TMVA.Types.kBDT, "BDTBoost2",
#                       ":".join([ "!H","!V",
#                                  "NTrees=1500",
##                                  "MinNodeSize=2.%",
##                                  "nEventsMin=200",
#                                  "MaxDepth=3",
#                                  "BoostType=AdaBoost",
#                                  "AdaBoostBeta=0.15", # 0.1 -> 0.05 -> 0.01 -> 0.1
#                                  "SeparationType=GiniIndex",
#                                  "nCuts=70"
#                                 ]) )
    # BDTBoost3
    factory.BookMethod(TMVA.Types.kBDT, "BDTBoost3",
                       ":".join([ "!H","!V",
                                  "NTrees=1500",
#                                  "MinNodeSize=2.%",
#                                  "nEventsMin=200",
                                  "MaxDepth=3",
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.20", # 0.1 -> 0.05 -> 0.01 -> 0.1
                                  "SeparationType=GiniIndex",
                                  "nCuts=70"
                                 ]) )
    # BDTBoost4
    factory.BookMethod(TMVA.Types.kBDT, "BDTBoost4",
                       ":".join([ "!H","!V",
                                  "NTrees=1500",
#                                  "MinNodeSize=2.%",
#                                  "nEventsMin=200",
                                  "MaxDepth=3",
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.30", # 0.1 -> 0.05 -> 0.01 -> 0.1
                                  "SeparationType=GiniIndex",
                                  "nCuts=70"
                                 ]) )
#    # BDTNodeSize
#    factory.BookMethod(TMVA.Types.kBDT, "BDTNodeSize",
#                       ":".join([ "!H","!V",
#                                  "NTrees=1800",
#                                  "MinNodeSize=5.%", # 10.% -> 20.% -> 1.%
##                                  "nEventsMin=200",
#                                  "MaxDepth=3",
#                                  "BoostType=AdaBoost",
#                                  "AdaBoostBeta=0.05",
#                                  "SeparationType=GiniIndex",
#                                  "nCuts=50"
#                                 ]) )
#
#    # MLPTanh
#    factory.BookMethod( TMVA.Types.kMLP, "MLPTanh",
#                        ":".join([ "!H","!V",
#                                   "LearningRate=0.01",
##                                   "NCycles=200",
#                                   "NeuronType=tanh",
#                                   "VarTransform=N",
#                                   "HiddenLayers=N,N",
#                                   "UseRegulator"
#                                  ]) )
#    # MLPLearningRate
#    factory.BookMethod( TMVA.Types.kMLP, "MLPLearningRate",
#                        ":".join([ "!H","!V",
#                                   "LearningRate=0.1", # 0.8 -> 0.1 -> 0.01 -> 0.1
##                                   "NCycles=200",
#                                   "NeuronType=sigmoid",
#                                   "VarTransform=N",
#                                   "HiddenLayers=N,N",
#                                   "UseRegulator"
#                                  ]) )
#    # MLPNodes
#    # Warning: use ROOT 34 or newer for larger buffer for the xml reader
#    factory.BookMethod( TMVA.Types.kMLP, "MLPNodes",
#                        ":".join([ "!H","!V",
#                                   "LearningRate=0.01",
##                                   "NCycles=200",
#                                   "NeuronType=tanh",
#                                   "VarTransform=N",
#                                   "HiddenLayers=N+4,N",
#                                   "UseRegulator"
#                                  ]) )
#    # MLPNodes1
#    # Warning: use ROOT 34 or newer for larger buffer for the xml reader
#    factory.BookMethod( TMVA.Types.kMLP, "MLPNodes1",
#                        ":".join([ "!H","!V",
#                                   "LearningRate=0.01",
##                                   "NCycles=200",
#                                   "NeuronType=tanh",
#                                   "VarTransform=N",
#                                   "HiddenLayers=N",
#                                   "UseRegulator"
#                                  ]) )
#    # MLPNodes2
#    # Warning: use ROOT 34 or newer for larger buffer for the xml reader
#    factory.BookMethod( TMVA.Types.kMLP, "MLPNodes2",
#                        ":".join([ "!H","!V",
#                                   "LearningRate=0.01",
##                                   "NCycles=200",
#                                   "NeuronType=sigmoid",
#                                   "VarTransform=N",
#                                   "HiddenLayers=N,N+4",
#                                   "UseRegulator"
#                                  ]) )
#    # MLPSigmoid
#    factory.BookMethod( TMVA.Types.kMLP, "MLPSigmoid",
#                        ":".join([ "!H","!V",
#                                  "LearningRate=0.01",
##                                  "NCycles=200",
#                                  "NeuronType=sigmoid",
#                                  "VarTransform=N",
#                                  "HiddenLayers=N,N",
#                                  "UseRegulator"
#                                  ]) )

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
    f_out.Close()

    # move files from weights/ to MVA/weights/configname
    weightsdir = "MVA/weights/"+config.name
#    if not os.path.exists("MVA"):
#        os.makedirs("MVA")
#    if not os.path.exists("MVA/trees"):
#        os.makedirs("MVA/trees")
#    if not os.path.exists("MVA/weights"):
#        os.makedirs("MVA/weights")
    if not os.path.exists(weightsdir):
        os.makedirs(weightsdir)
    for method in methods:
        os.rename("weights/TMVAClassification_"+method+".weights.xml",
                  weightsdir+"/TMVAClassification_"+method+".weights.xml")
        os.rename("weights/TMVAClassification_"+method+".class.C",
                  weightsdir+"/TMVAClassification_"+method+".class.C")
    os.rename("MVA/HH_MVA_"+config.name+".root",
              "MVA/trees/HH_MVA_"+config.name+".root")



# SIGNIFICANCE
def significance(config,histS,histB,test=False):
    
    Pmax = 0
    Smax = 0
    Bmax = 0
    Simax = 0
    Bimax = 0
    imax = 0

    eS = N_S / S_tot
    eB = N_B / B_tot
    if test:
        eS = eS * config.S / histS.Integral(1,N)
        eB = eB * config.B / histS.Integral(1,N)

    # scan cut over all bins, find cut with highest significance
    N = histS.GetNbinsX()
    for i in range(1,N):
        Si = histS.Integral(i,N)
        Bi = histB.Integral(i,N)
        if Si and Bi:
          S = eS * Si # yield
          B = eB * Bi
          P = S / (1+sqrt(B))
          if Pmax<P and S > 10 and B > 10:
              Pmax = P
              Smax = S
              Bmax = B
              Simax = Si
              Bimax = Bi
              imax = i

    cut = histS.GetXaxis().GetBinCenter(imax)
    return [Pmax,Smax,Bmax,Simax,Bimax,Simax/S_tot,Bimax/B_tot,cut]



# SIGNIFICANCE
def significanceBins(histS,histB):
    
    P2 = 0

    # calculate significance per bin and add using variance addition law:
    #                      sigma^2 = sum(sigma_i^2)
    # if S or B bin is empty, merge with next bins until both are nonzero
    N = histS.GetNbinsX()
    Si = 0
    Bi = 0
    for i in reversed(range(1,N)):
        # merge with previous bins B or S were 0 there
        S = Si + N_S * histS.GetBinContent(i) / S_tot # yield for bin i
        B = Bi + N_B * histB.GetBinContent(i) / B_tot
        
        if S and B : # both nonzero
            Si = 0 # reset
            Bi = 0 # reset
            P2 += S*S/(B+2*sqrt(B)+1) # P^2 += P_i^2
        else: # at least on zero
            Si += S # save S for next bins until both nonzero
            Bi += B # save B for next bins until both nonzero

    return sqrt(P2)



# HISTOGRAMS: TMVA output
def plotTest(config):
    print "\n>>> examine training with test sample for configuration "+config.name

    reader = TMVA.Reader()
    f = TFile("MVA/trees/HH_MVA_"+config.name+".root")
    TestTree = gDirectory.Get("TestTree")

    vars = [ ]
    for name in config.varNames:
        vars.append(array('f',[0]))
        reader.AddVariable(name,vars[-1])

    significances = [ ]
    for Method, method in Methods:
        reader.BookMVA(method,"MVA/weights/"+config.name+"/TMVAClassification_"+method+".weights.xml")

        c = makeCanvas()
        if Method == "MLP":
            histS = TH1F("histS", "", 150, -0.4, 1.4)
            histB = TH1F("histB", "", 150, -0.4, 1.4)
        else:
            histS = TH1F("histS", "", 150, -1.4, 1.4)
            histB = TH1F("histB", "", 150, -1.4, 1.4)

        config.hist_effs.append(deepcopy(gDirectory.Get("Method_"+Method+"/"+method+"/MVA_"+method+"_rejBvsS")) )
        config.hist_effs_train.append(deepcopy(gDirectory.Get("Method_"+Method+"/"+method+"/MVA_"+method+"_trainingRejBvsS")) )
        TestTree.Draw(method+">>histS","classID == 0","goff")
        TestTree.Draw(method+">>histB","classID == 1", "goff")

        [Pmax,Smax,Bmax,Simax,Bimax,effS,effB,cut] = significance(config,histS,histB,test=True)
        Pbins = significanceBins(histS, histB)
        significances.append( ">>> "+config.name+" - "+method + \
                              ":\n>>>\t\t%.4f significance (%.4f with bins) with yields" % (Pmax,Pbins) + \
                              "\n>>>\t\tS = %.1f, B = %.1f and a cut at %.4f." % (Smax,Bmax,cut) + \
                              " (Si=%.1f (%.2f%%) and Bi=%.1f (%.4f%%))" % (Simax,100*effS,Bimax,100*effB) )
        #significances.append("lol")

        histB.Draw() # draw first: mostly bigger
        histS.Draw("same")
        makeAxes(histB,histS,xlabel=(Method+" response"),ylabel="")
        legend = makeLegend(histS,histB,title=" ",entries=["signal","background"],position='RightTopTop',transparent=True)
        #legend = makeLegend(histS,histB,title=" ",tt=True,position='RightTopTop',transparent=True)
        legend.Draw()
#        histB.SetStats(0)
        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(histS,histB)
        c.SaveAs("MVA/"+method+"_"+config.name+".png")
        c.Close()
        gDirectory.Delete("histS")
        gDirectory.Delete("histB")

    for s in significances:
        print s
    
    return significances



# HISTOGRAMS: TMVA output
def plotApplication(config):
    print "\n>>> examine training with application to all data for configuration "+config.name

    treeS = config.treeS
    treeB = config.treeB
    reader = TMVA.Reader()
    f = TFile("MVA/trees/HH_MVA_"+config.name+".root")
    
    vars = [ ]
    for name in config.varNames:
        vars.append(array('f',[0]))
        reader.AddVariable(name,vars[-1])

    significances = [ ]
    for Method, method in Methods:
        reader.BookMVA(method,"MVA/weights/"+config.name+"/TMVAClassification_"+method+".weights.xml")
        if Method == "MLP":
            histS = TH1F("histS", "", 150, -0.4, 1.4)
            histB = TH1F("histB", "", 150, -0.4, 1.4)
        else:
            histS = TH1F("histS", "", 150, -1.4, 1.4)
            histB = TH1F("histB", "", 150, -1.4, 1.4)
        
        # fill histograms
        treeS.ResetBranchAddresses()
        for i in range(len(config.varNames)):
            treeS.SetBranchAddress(config.varNames[i],vars[i])
        for evt in range(0,treeS.GetEntries()):
            treeS.GetEntry(evt)
            histS.Fill( reader.EvaluateMVA(method) )
        treeB.ResetBranchAddresses()
        for i in range(len(config.varNames)):
            treeB.SetBranchAddress(config.varNames[i],vars[i])
        for evt in range(0,treeB.GetEntries()):
            treeB.GetEntry(evt)
            histB.Fill( reader.EvaluateMVA(method) )

        c = makeCanvas()
        [Pmax,Smax,Bmax,Simax,Bimax,effS,effB,cut] = significance(config,histS,histB)
        Pbins = significanceBins(histS, histB)
        significances.append( ">>> "+config.name+" - "+method + \
                              ":\n>>>\t\t%.4f significance (%.4f with bins) with yields" % (Pmax,Pbins) + \
                              "\n>>>\t\tS = %.1f, B = %.1f and a cut at %.4f." % (Smax,Bmax,cut) + \
                              " (Si=%.1f (%.2f%%) and Bi=%.1f (%.4f%%))" % (Simax,100*effS,Bimax,100*effB) )

        histB.Draw()
        histS.Draw("same")
        makeAxes(histS,xlabel=(Method+" response"),ylabel="")
        makeAxes(histB,histS,xlabel=(Method+" response"),ylabel="")
        legend = makeLegend(histS,histB,title=" ",entries=["signal","background"],position='RightTopTop',transparent=True)
#        legend = makeLegend(histS,histB,title=" ",tt=True,position='RightTopTop',transparent=True)
        legend.Draw()
#        histB.SetStats(0)
        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(histS,histB)
        c.SaveAs("MVA/"+method+"_"+config.name+"_Appl.png")
        c.Close()
        gDirectory.Delete("histS")
        gDirectory.Delete("histB")

    for s in significances:
        print s

    return significances



# HISTOGRAMS: compare all methods and variable configurations
def compare(configs,stage="",methods0=methods):
    if configs:
        print "\n>>> compare methods with "+", ".join([c.name for c in configs])
    else:
        return
    
    hist_effs = [ ]
    for config in configs:
        for hist in config.hist_effs:
            if hist.GetTitle().replace("MVA_","") in methods0:
#                print "type(hist) = %s" % type(hist)
                hist_effs.append(hist)
    if not hist_effs:
        print ">>> No histograms!"
        return
    
    c = makeCanvas()
    hist_effs[0].Draw()
    hist_effs[0].SetStats(0)
    if len(hist_effs)>1:
        for hist in hist_effs[1:]:
            hist.Draw("same")
    makeAxes(*hist_effs,xlabel="signal efficiency",ylabel="background rejection")
    labels = [ ]
    for config in configs:
        labels.extend([config.name+", "+method for method in methods0])
    legend = makeLegend(*hist_effs,title="#splitline{background rejection}{vs. signal efficiency}",
                                   entries=labels, position="RightTop")
    legend.Draw()
    CMS_lumi.CMS_lumi(c,14,33)
    setLineColor(*hist_effs)
    #for hist in hist_effs:
        #hist.SetLineStyle(1)
        #hist.SetLineWidth(2)
    c.SaveAs("MVA/BrejvsSeffs_"+stage+".png")
    c.Close()



# HISTOGRAMS: eff
def eff(config,method):
    print "\n>>> make single efficiency with "+method
    
    hist = None
    hist_train = None
    for h,h_train in zip(config.hist_effs,config.hist_effs_train):
        if h.GetTitle().replace("MVA_","") == method:
            hist = h
            hist_train = h_train
            break
    else:
        print ">>> No histograms!"
        return
    
    c = makeCanvas()
    hist.Draw()
    makeAxes(hist,xlabel="signal efficiency",tt=True,ylabel="background rejection")
    hist.SetStats(0)
    CMS_lumi.CMS_lumi(c,14,33)
    setLineStyle(hist)
    c.SaveAs("MVA/BrejvsSeffs_"+config.name+"_"+method+".png")
    c.Close()
    
    c = makeCanvas()
    hist.Draw()
    hist_train.Draw("same")
    makeAxes(hist,hist_train,xlabel="signal efficiency",tt=True,ylabel="background rejection")
    legend = makeLegend(hist,hist_train,title=" ", transparent=True,
                                   entries=["test sample","training sample"], position="RightTop")
    legend.Draw()
    CMS_lumi.CMS_lumi(c,14,33)
    setLineStyle(hist,hist_train)
    c.SaveAs("MVA/BrejvsSeffs_"+config.name+"_"+method+"_train.png")
    c.Close()




# 2D COLOR HISTOGRAM: Correlation matrices
def correlation(config):
    print "\n>>> make correlation matrix plots"
    ROOT.gStyle.SetPalette(1) # for rainbow colors

    reader = TMVA.Reader()
    f = TFile("MVA/trees/HH_MVA_"+config.name+".root")
    TestTree = gDirectory.Get("TestTree")

    c = makeCanvas(square=True, scaleleftmargin=1.5)
    histS = f.Get("CorrelationMatrixS")
    histS.Draw("colz")
    makeLabels2D(histS,xaxis=True,yaxis=True)
    histS.SetLabelSize(0.030,"x")
    histS.SetLabelSize(0.040,"y")
    CMS_lumi.CMS_lumi(c,14,33)
    c.SaveAs("MVA/CorrelationMatrixS_"+config.name+".png")
    c.Close()

    c = makeCanvas(square=True, scaleleftmargin=1.5)
    histB = f.Get("CorrelationMatrixB")
    histB.Draw("colz")
    makeLabels2D(histB,xaxis=True,yaxis=True)
    histB.SetLabelSize(0.030,"x")
    histB.SetLabelSize(0.040,"y")
    c.SaveAs("MVA/CorrelationMatrixB_"+config.name+".png")
    c.Close()



def main():

    allVars = [ "Njets20","Nbjets30",
                "jet1Pt","jet2Pt",
                "bjet1Pt","bjet2Pt",
                "Pt_bb","Pt_bl","Pt_j1l",
                "Pt_b1lnu", "Pt_b2lnu",
                "Pt_jjl", "Pt_jjb1", "Pt_jjb2",
                "leptonPt","MET",
                "DeltaR_j1l","DeltaR_j2l",
                "DeltaR_b1l","DeltaR_b2l",
                "DeltaR_bb1","DeltaR_jj",
                "DeltaR_jjl","DeltaR_jjb",
                "DeltaPhi_j1lbb",
                "DeltaPhi_lMET","DeltaPhi_jjlnu",
                "M_bb_closest", "M_jjlnu",
                "M_jjb1", "M_jjb2",

                "M_b1lnu", "M_b2lnu",
                "M_bl", "M_jjl",
                "M_jj", "M_j1l",
                "MT_lnu","MT_jjlnu" ]
                # Mbl better discrinant than Mblnu
                # MT_lnu better than MT_jjlnu
                # DeltaPhi_lMET is bad?

    allVars12 = [ "Njets20","Nbjets30",
                    "jet1Pt","jet2Pt",
                    "bjet1Pt","bjet2Pt",
                    "Pt_bb","Pt_bl","Pt_j1l",
                    "Pt_b1lnu", "Pt_b2lnu",
                    "Pt_jjl", "Pt_jjb1", "Pt_jjb2",
                    "leptonPt","MET",
                    "DeltaR_j1l","DeltaR_j2l",
                    "DeltaR_b1l","DeltaR_b2l",
                    "DeltaR_bb1","DeltaR_jj",
                    "DeltaR_jjl","DeltaR_jjb",
                    "DeltaPhi_j1lbb",
                    "DeltaPhi_lMET","DeltaPhi_jjlnu",
                    "M_bb_closest", "M_jjlnu",
                    "M_jjb1", #"M_jjb2",
                    "M_b2lnu", #"M_b1lnu",
                    "M_bl", "M_jjl",
                    "M_jj", "M_j1l",
                    "MT_lnu","MT_jjlnu" ]


    allVars12M = [ "Njets20","Nbjets30",
                    "jet1Pt","jet2Pt",
                    "bjet1Pt","bjet2Pt",
                    "Pt_bb","Pt_bl","Pt_j1l",
                    "Pt_b1lnu", "Pt_b2lnu",
                    "Pt_jjl", "Pt_jjb1", "Pt_jjb2",
                    "leptonPt","MET",
                    "DeltaR_j1l","DeltaR_j2l",
                    "DeltaR_b1l","DeltaR_b2l",
                    "DeltaR_bb1","DeltaR_jj",
                    "DeltaR_jjl","DeltaR_jjb",
                    "DeltaPhi_j1lbb",
                    "DeltaPhi_jjlnu",#"DeltaPhi_lMET",
                    "M_bb_closest", "M_jjlnu",
                    "M_jjb1", #"M_jjb2",
                    "M_b2lnu", #"M_b1lnu",
                    "M_bl", "M_jjl",
                    "M_jj", "M_j1l",
                    "MT_lnu","MT_jjlnu" ]

    allVarsN = [ #"Njets20","Nbjets30",
                "jet1Pt","jet2Pt",
                "bjet1Pt","bjet2Pt",
                "Pt_bb","Pt_bl","Pt_j1l",
                "Pt_b1lnu", "Pt_b2lnu",
                "Pt_jjl", "Pt_jjb1", "Pt_jjb2",
                "leptonPt","MET",
                "DeltaR_j1l","DeltaR_j2l",
                "DeltaR_b1l","DeltaR_b2l",
                "DeltaR_bb1","DeltaR_jj",
                "DeltaR_jjl","DeltaR_jjb",
                "DeltaPhi_j1lbb",
                "DeltaPhi_lMET","DeltaPhi_jjlnu",
                "M_bb_closest", "M_jjlnu",
                "M_jjb1", "M_jjb2",
                "M_b1lnu", "M_b2lnu",
                "M_bl", "M_jjl",
                "M_jj", "M_j1l",
                "MT_lnu","MT_jjlnu" ]

    allVars1 = [ #"Njets20","Nbjets30",
                "jet1Pt","jet2Pt",
                "bjet1Pt","bjet2Pt",
                "Pt_bb","Pt_bl","Pt_j1l",
                "Pt_b1lnu", "Pt_b2lnu",
                "Pt_jjl", "Pt_jjb1", "Pt_jjb2",
                "leptonPt","MET",
                "DeltaR_j1l","DeltaR_j2l",
                "DeltaR_b1l","DeltaR_b2l",
                "DeltaR_bb1","DeltaR_jj",
                "DeltaR_jjl","DeltaR_jjb",
                "DeltaPhi_j1lbb",
                "DeltaPhi_lMET","DeltaPhi_jjlnu",
                "M_bb_closest", "M_jjlnu",
                "M_jjb1", "M_jjb2",
                "M_b1lnu", "M_b2lnu",
                "M_bl", "M_jjl",
                "M_jj", "M_j1l",
                "MT_lnu","MT_jjlnu" ]

    allVars2 = [ "jet1Pt","jet2Pt",
                "bjet1Pt","bjet2Pt",
                "Pt_bb","Pt_bl","Pt_j1l",
                "Pt_b1lnu", "Pt_b2lnu",
                "Pt_jjl", "Pt_jjb1", "Pt_jjb2",
                "leptonPt","MET",
                "DeltaR_j1l","DeltaR_j2l",
                "DeltaR_b1l","DeltaR_b2l",
                "DeltaR_bb1","DeltaR_jj",
                "DeltaR_jjl","DeltaR_jjb",
                "DeltaPhi_j1lbb",
                "DeltaPhi_jjlnu", #"DeltaPhi_lMET"
                "M_bb_closest", "M_jjlnu",
                "M_jjb1", "M_jjb2",
                "M_b1lnu", "M_b2lnu",
                "M_bl", "M_jjl",
                "M_jj", "M_j1l",
                "MT_lnu","MT_jjlnu" ]

    betterVars = [  "jet1Pt","jet2Pt",
                    "bjet1Pt","bjet2Pt",
                    "Pt_bb","Pt_j1l",
                    "Pt_b1lnu", "Pt_b2lnu",
                    "Pt_jjb1", "Pt_jjb2",
                    "leptonPt","MET",
                    "DeltaR_j1l","DeltaR_j2l",
                    "DeltaR_b1l","DeltaR_b2l",
                    "DeltaR_bb1",
                    "DeltaR_jjl","DeltaR_jjb",
                    "DeltaPhi_j1lbb","DeltaPhi_jjlnu",
                    "M_bb_closest", "M_jjlnu",
                    "M_jjb1", "M_jjb2",
                    "M_b1lnu", "M_b2lnu",
                    "MT_lnu" ]


    #bestVars = [    "bjet1Pt","jet1Pt",
                    #"leptonPt", "MET",
                    #"DeltaR_j1l","DeltaR_j2l",
                    #"DeltaR_b1l","DeltaR_b2l",
                    #"DeltaR_bb1",
                    #"DeltaR_jjl","DeltaR_jjb",
                    #"DeltaPhi_j1lbb",
                    #"M_bb_closest", "M_jjlnu",
                    #"M_jjb", "M_bl", "M_j1l",
                    #"MT_lnu" ]

#    ANVars = [  "Njets20",
#                "Pt_bb","Pt_bl","Pt_j1l",
#                "leptonPt","MET",
#                "DeltaR_j1l","DeltaR_b1l",
#                "DeltaR_bb1","DeltaPhi_jjlbb",
#                "M_bb_closest", "M_jjlnu", # Higgs reconstruction
#                "M_jjb", "M_blnu",         # top reconstruction
#                "M_bl", "M_j1l" ]

#    favVars = [ "DeltaR_b1l", "DeltaR_b2l", "DeltaR_bb1",
#                "DeltaR_j1l", "DeltaR_j2l", "DeltaR_jjl",
#                "Pt_bb", "Pt_bl",
#                "M_bb_closest", "M_jjlnu",
#                "M_jjb", "M_bl", "M_j1l" ]

#    genVars = [ "Pt_q1","Pt_q2",
#                "Pt_b1","Pt_b2",
#                #"Pt_bb","Pt_bl","Pt_q1l",
#                "Pt_l","Pt_nu",
#                "DeltaR_q1l","DeltaR_q2l",
#                "DeltaR_b1l","DeltaR_b2l",
#                "DeltaR_bb","DeltaR_qq",
#                "DeltaR_qql","DeltaR_qqb",
#                #"M_bb", "M_qqlnu",
#                #"M_qql",
#                #"M_qqb1", "M_qqb2", "M_b1lnu","M_b2lnu",
#                #"M_bl", "M_qq", "M_q1l",
#              ]



    if opts.test:
        print ">>> test mode"
        configs = [configuration("test", ["M_bb_closest", "DeltaR_bb1"], 1)]
    else:
        configs = [
                    configuration("everything", allVars, 1),
                    configuration("everythingN", allVarsN, 1),
                    configuration("everything1", allVars1, 1),
                    configuration("everything2", allVars2, 1),
                    configuration("everything12", allVars12, 1),
                    configuration("everything12M", allVars12M, 1),
                    configuration("better", betterVars, 1),
#                    configuration("better20",     betterVars, 1),
#                    configuration("everythingCleanUp", allVars, 2),
#                    configuration("everythingNCleanUp", allVarsN, 2),
#                    configuration("everything1CleanUp", allVars1, 2),
#                    configuration("everything2CleanUp", allVars2, 2),
#                    configuration("everything12CleanUp", allVars12, 2),
#                    configuration("betterCleanUp", betterVars, 2),
#                    configuration("generatorCleanUp", genVars, 2, gen=True),
#                    configuration("bestCleanUp", bestVars, 2),
                  ]

    if opts.onlyPlot:
        print ">>> plots only"
    else:
        for config in configs: #reversed(configs):
            train(config)
    significances_test = [ ]
    significances_Appl = [ ]
    for config in configs:
        significances_test.extend(plotTest(config))
        significances_Appl.extend(plotApplication(config))
    print "\n>>> compare all significances of test samples"
    for s in significances_test:
        print s
    print "\n>>> compare all significances of total sample"
    for s in significances_Appli:
        print s
#    compare([c for c in configs if c.stage==1],stage="stage_1")
#    compare([c for c in configs if c.stage==2],stage="stage_2",methods0=["BDTTuned"])
#    compare([c for c in configs if c.stage==2],stage="stage_2")
#    compare([c for c in configs if c.stage==3],stage="stage_3")
#    eff(configs[0],"BDTTuned")
#    eff(configs[4],"BDTBoost3")
#    eff(configs[2],"BDTBoost3")
#    compare(configs,stage="DBT",methods0=[m for m in methods if "BDT" in m])
#    compare(configs,stage="MLP",methods0=[m for m in methods if "MLP" in m])

#    for config in configs:
#        if "everything" in config.name:
#            correlation(config)



if __name__ == '__main__':
    main()
    print "\n>>> done"


# strong correlations between:
#    M_bb vs. DeltaR_bb
#    M_bb vs. bjet1, bjet2 for background
#

#--- Factory                  : Ranking input variables (method specific)...
#--- BDT                      : Ranking result (top variable is best ranked)
#--- BDT                      : ------------------------------------------------
#--- BDT                      : Rank : Variable       : Variable Importance
#--- BDT                      : ------------------------------------------------
#--- BDT                      :    1 : M_bb_closest   : 5.107e-02
#--- BDT                      :    2 : DeltaR_j1l     : 4.654e-02
#--- BDT                      :    3 : Pt_bb          : 4.504e-02
#--- BDT                      :    4 : M_bl           : 4.249e-02
#--- BDT                      :    5 : DeltaPhi_j1lbb : 4.129e-02
#--- BDT                      :    6 : leptonPt       : 3.910e-02
#--- BDT                      :    7 : DeltaR_j2l     : 3.784e-02
#--- BDT                      :    8 : DeltaR_bb1     : 3.749e-02
#--- BDT                      :    9 : DeltaR_b1l     : 3.688e-02
#--- BDT                      :   10 : DeltaR_b2l     : 3.680e-02
#--- BDT                      :   11 : bjet1Pt        : 3.558e-02
#--- BDT                      :   12 : jet1Pt         : 3.446e-02
#--- BDT                      :   13 : DeltaR_jj      : 3.382e-02
#--- BDT                      :   14 : M_jjb          : 3.294e-02
#--- BDT                      :   15 : DeltaR_jjl     : 3.289e-02
#--- BDT                      :   16 : MT_jjlnu       : 3.278e-02
#--- BDT                      :   17 : DeltaPhi_lMET  : 3.268e-02
#--- BDT                      :   18 : MT_lnu         : 3.263e-02
#--- BDT                      :   19 : Pt_bl          : 3.250e-02
#--- BDT                      :   20 : DeltaR_jjb     : 3.235e-02
#--- BDT                      :   21 : M_j1l          : 3.179e-02
#--- BDT                      :   22 : MET            : 3.104e-02
#--- BDT                      :   23 : Pt_j1l         : 3.072e-02
#--- BDT                      :   24 : bjet2Pt        : 2.860e-02
#--- BDT                      :   25 : M_jjlnu        : 2.814e-02
#--- BDT                      :   26 : jet2Pt         : 2.801e-02
#--- BDT                      :   27 : M_blnu         : 2.709e-02
#--- BDT                      :   28 : Njets20        : 2.676e-02
#--- BDT                      :   29 : Nbjets30       : 2.070e-02
#--- BDT                      : ------------------------------------------------
#--- BDTTuned                 : Ranking result (top variable is best ranked)
#--- BDTTuned                 : ------------------------------------------------
#--- BDTTuned                 : Rank : Variable       : Variable Importance
#--- BDTTuned                 : ------------------------------------------------
#--- BDTTuned                 :    1 : Pt_bb          : 7.524e-02
#--- BDTTuned                 :    2 : M_bb_closest   : 5.382e-02
#--- BDTTuned                 :    3 : DeltaR_j1l     : 5.261e-02
#--- BDTTuned                 :    4 : M_bl           : 5.027e-02
#--- BDTTuned                 :    5 : bjet1Pt        : 4.347e-02
#--- BDTTuned                 :    6 : DeltaR_bb1     : 4.096e-02
#--- BDTTuned                 :    7 : leptonPt       : 3.963e-02
#--- BDTTuned                 :    8 : M_jjb          : 3.827e-02
#--- BDTTuned                 :    9 : jet1Pt         : 3.795e-02
#--- BDTTuned                 :   10 : M_j1l          : 3.778e-02
#--- BDTTuned                 :   11 : Pt_bl          : 3.690e-02
#--- BDTTuned                 :   12 : DeltaR_j2l     : 3.675e-02
#--- BDTTuned                 :   13 : DeltaPhi_j1lbb : 3.655e-02
#--- BDTTuned                 :   14 : DeltaR_b1l     : 3.516e-02
#--- BDTTuned                 :   15 : DeltaR_jjl     : 3.303e-02
#--- BDTTuned                 :   16 : M_jjlnu        : 3.246e-02
#--- BDTTuned                 :   17 : Pt_j1l         : 2.920e-02
#--- BDTTuned                 :   18 : MT_jjlnu       : 2.773e-02
#--- BDTTuned                 :   19 : jet2Pt         : 2.751e-02
#--- BDTTuned                 :   20 : bjet2Pt        : 2.666e-02
#--- BDTTuned                 :   21 : DeltaR_b2l     : 2.628e-02
#--- BDTTuned                 :   22 : DeltaR_jjb     : 2.593e-02
#--- BDTTuned                 :   23 : MT_lnu         : 2.531e-02
#--- BDTTuned                 :   24 : Nbjets30       : 2.486e-02
#--- BDTTuned                 :   25 : M_blnu         : 2.341e-02
#--- BDTTuned                 :   26 : Njets20        : 2.216e-02
#--- BDTTuned                 :   27 : MET            : 2.196e-02
#--- BDTTuned                 :   28 : DeltaR_jj      : 2.022e-02
#--- BDTTuned                 :   29 : DeltaPhi_lMET  : 1.793e-02
#--- BDTTuned                 : ------------------------------------------------
#--- BDTPreselection          : Ranking result (top variable is best ranked)
#--- BDTPreselection          : ------------------------------------------------
#--- BDTPreselection          : Rank : Variable       : Variable Importance
#--- BDTPreselection          : ------------------------------------------------
#--- BDTPreselection          :    1 : Pt_bb          : 7.524e-02
#--- BDTPreselection          :    2 : M_bb_closest   : 5.382e-02
#--- BDTPreselection          :    3 : DeltaR_j1l     : 5.261e-02
#--- BDTPreselection          :    4 : M_bl           : 5.027e-02
#--- BDTPreselection          :    5 : bjet1Pt        : 4.347e-02
#--- BDTPreselection          :    6 : DeltaR_bb1     : 4.096e-02
#--- BDTPreselection          :    7 : leptonPt       : 3.963e-02
#--- BDTPreselection          :    8 : M_jjb          : 3.827e-02
#--- BDTPreselection          :    9 : jet1Pt         : 3.795e-02
#--- BDTPreselection          :   10 : M_j1l          : 3.778e-02
#--- BDTPreselection          :   11 : Pt_bl          : 3.690e-02
#--- BDTPreselection          :   12 : DeltaR_j2l     : 3.675e-02
#--- BDTPreselection          :   13 : DeltaPhi_j1lbb : 3.655e-02
#--- BDTPreselection          :   14 : DeltaR_b1l     : 3.516e-02
#--- BDTPreselection          :   15 : DeltaR_jjl     : 3.303e-02
#--- BDTPreselection          :   16 : M_jjlnu        : 3.246e-02
#--- BDTPreselection          :   17 : Pt_j1l         : 2.920e-02
#--- BDTPreselection          :   18 : MT_jjlnu       : 2.773e-02
#--- BDTPreselection          :   19 : jet2Pt         : 2.751e-02
#--- BDTPreselection          :   20 : bjet2Pt        : 2.666e-02
#--- BDTPreselection          :   21 : DeltaR_b2l     : 2.628e-02
#--- BDTPreselection          :   22 : DeltaR_jjb     : 2.593e-02
#--- BDTPreselection          :   23 : MT_lnu         : 2.531e-02
#--- BDTPreselection          :   24 : Nbjets30       : 2.486e-02
#--- BDTPreselection          :   25 : M_blnu         : 2.341e-02
#--- BDTPreselection          :   26 : Njets20        : 2.216e-02
#--- BDTPreselection          :   27 : MET            : 2.196e-02
#--- BDTPreselection          :   28 : DeltaR_jj      : 2.022e-02
#--- BDTPreselection          :   29 : DeltaPhi_lMET  : 1.793e-02
#--- BDTPreselection          : ------------------------------------------------
#--- BDTBoost                 : Ranking result (top variable is best ranked)
#--- BDTBoost                 : ------------------------------------------------
#--- BDTBoost                 : Rank : Variable       : Variable Importance
#--- BDTBoost                 : ------------------------------------------------
#--- BDTBoost                 :    1 : Pt_bb          : 6.399e-02
#--- BDTBoost                 :    2 : M_bb_closest   : 5.562e-02
#--- BDTBoost                 :    3 : DeltaR_j1l     : 4.644e-02
#--- BDTBoost                 :    4 : M_bl           : 4.528e-02
#--- BDTBoost                 :    5 : leptonPt       : 4.222e-02
#--- BDTBoost                 :    6 : bjet1Pt        : 4.093e-02
#--- BDTBoost                 :    7 : DeltaPhi_j1lbb : 4.030e-02
#--- BDTBoost                 :    8 : jet1Pt         : 3.871e-02
#--- BDTBoost                 :    9 : DeltaR_bb1     : 3.766e-02
#--- BDTBoost                 :   10 : DeltaR_b1l     : 3.714e-02
#--- BDTBoost                 :   11 : Pt_bl          : 3.695e-02
#--- BDTBoost                 :   12 : DeltaR_j2l     : 3.544e-02
#--- BDTBoost                 :   13 : M_j1l          : 3.498e-02
#--- BDTBoost                 :   14 : M_jjb          : 3.421e-02
#--- BDTBoost                 :   15 : DeltaR_jjl     : 3.359e-02
#--- BDTBoost                 :   16 : DeltaR_b2l     : 3.248e-02
#--- BDTBoost                 :   17 : MT_jjlnu       : 3.180e-02
#--- BDTBoost                 :   18 : Pt_j1l         : 3.023e-02
#--- BDTBoost                 :   19 : DeltaR_jj      : 2.953e-02
#--- BDTBoost                 :   20 : jet2Pt         : 2.878e-02
#--- BDTBoost                 :   21 : M_jjlnu        : 2.748e-02
#--- BDTBoost                 :   22 : DeltaR_jjb     : 2.671e-02
#--- BDTBoost                 :   23 : MET            : 2.609e-02
#--- BDTBoost                 :   24 : M_blnu         : 2.556e-02
#--- BDTBoost                 :   25 : MT_lnu         : 2.531e-02
#--- BDTBoost                 :   26 : bjet2Pt        : 2.526e-02
#--- BDTBoost                 :   27 : DeltaPhi_lMET  : 2.500e-02
#--- BDTBoost                 :   28 : Nbjets30       : 2.129e-02
#--- BDTBoost                 :   29 : Njets20        : 2.101e-02
#--- BDTBoost                 : ------------------------------------------------
#--- BDTNodeSize              : Ranking result (top variable is best ranked)
#--- BDTNodeSize              : ------------------------------------------------
#--- BDTNodeSize              : Rank : Variable       : Variable Importance
#--- BDTNodeSize              : ------------------------------------------------
#--- BDTNodeSize              :    1 : Pt_bb          : 7.524e-02
#--- BDTNodeSize              :    2 : M_bb_closest   : 5.382e-02
#--- BDTNodeSize              :    3 : DeltaR_j1l     : 5.261e-02
#--- BDTNodeSize              :    4 : M_bl           : 5.027e-02
#--- BDTNodeSize              :    5 : bjet1Pt        : 4.347e-02
#--- BDTNodeSize              :    6 : DeltaR_bb1     : 4.096e-02
#--- BDTNodeSize              :    7 : leptonPt       : 3.963e-02
#--- BDTNodeSize              :    8 : M_jjb          : 3.827e-02
#--- BDTNodeSize              :    9 : jet1Pt         : 3.795e-02
#--- BDTNodeSize              :   10 : M_j1l          : 3.778e-02
#--- BDTNodeSize              :   11 : Pt_bl          : 3.690e-02
#--- BDTNodeSize              :   12 : DeltaR_j2l     : 3.675e-02
#--- BDTNodeSize              :   13 : DeltaPhi_j1lbb : 3.655e-02
#--- BDTNodeSize              :   14 : DeltaR_b1l     : 3.516e-02
#--- BDTNodeSize              :   15 : DeltaR_jjl     : 3.303e-02
#--- BDTNodeSize              :   16 : M_jjlnu        : 3.246e-02
#--- BDTNodeSize              :   17 : Pt_j1l         : 2.920e-02
#--- BDTNodeSize              :   18 : MT_jjlnu       : 2.773e-02
#--- BDTNodeSize              :   19 : jet2Pt         : 2.751e-02
#--- BDTNodeSize              :   20 : bjet2Pt        : 2.666e-02
#--- BDTNodeSize              :   21 : DeltaR_b2l     : 2.628e-02
#--- BDTNodeSize              :   22 : DeltaR_jjb     : 2.593e-02
#--- BDTNodeSize              :   23 : MT_lnu         : 2.531e-02
#--- BDTNodeSize              :   24 : Nbjets30       : 2.486e-02
#--- BDTNodeSize              :   25 : M_blnu         : 2.341e-02
#--- BDTNodeSize              :   26 : Njets20        : 2.216e-02
#--- BDTNodeSize              :   27 : MET            : 2.196e-02
#--- BDTNodeSize              :   28 : DeltaR_jj      : 2.022e-02
#--- BDTNodeSize              :   29 : DeltaPhi_lMET  : 1.793e-02
#--- BDTNodeSize              : ------------------------------------------------
#--- MLPTanh                  : Ranking result (top variable is best ranked)
#--- MLPTanh                  : ---------------------------------------
#--- MLPTanh                  : Rank : Variable       : Importance
#--- MLPTanh                  : ---------------------------------------
#--- MLPTanh                  :    1 : M_blnu         : 4.243e+01
#--- MLPTanh                  :    2 : jet2Pt         : 3.702e+01
#--- MLPTanh                  :    3 : Nbjets30       : 3.673e+01
#--- MLPTanh                  :    4 : M_jjb          : 3.333e+01
#--- MLPTanh                  :    5 : M_jjlnu        : 3.175e+01
#--- MLPTanh                  :    6 : leptonPt       : 3.155e+01
#--- MLPTanh                  :    7 : bjet1Pt        : 2.960e+01
#--- MLPTanh                  :    8 : M_j1l          : 2.880e+01
#--- MLPTanh                  :    9 : Pt_bl          : 2.619e+01
#--- MLPTanh                  :   10 : jet1Pt         : 2.590e+01
#--- MLPTanh                  :   11 : MET            : 2.587e+01
#--- MLPTanh                  :   12 : M_bl           : 2.497e+01
#--- MLPTanh                  :   13 : Pt_j1l         : 2.325e+01
#--- MLPTanh                  :   14 : DeltaR_j1l     : 2.201e+01
#--- MLPTanh                  :   15 : MT_jjlnu       : 2.136e+01
#--- MLPTanh                  :   16 : Pt_bb          : 1.852e+01
#--- MLPTanh                  :   17 : bjet2Pt        : 1.512e+01
#--- MLPTanh                  :   18 : Njets20        : 1.493e+01
#--- MLPTanh                  :   19 : MT_lnu         : 1.350e+01
#--- MLPTanh                  :   20 : DeltaR_j2l     : 8.169e+00
#--- MLPTanh                  :   21 : DeltaPhi_j1lbb : 7.823e+00
#--- MLPTanh                  :   22 : DeltaPhi_lMET  : 7.810e+00
#--- MLPTanh                  :   23 : DeltaR_bb1     : 7.090e+00
#--- MLPTanh                  :   24 : M_bb_closest   : 6.706e+00
#--- MLPTanh                  :   25 : DeltaR_jjl     : 4.859e+00
#--- MLPTanh                  :   26 : DeltaR_jj      : 4.054e+00
#--- MLPTanh                  :   27 : DeltaR_jjb     : 3.592e+00
#--- MLPTanh                  :   28 : DeltaR_b2l     : 3.525e+00
#--- MLPTanh                  :   29 : DeltaR_b1l     : 1.730e+00
#--- MLPTanh                  : ---------------------------------------
#--- MLPLearningRate          : Ranking result (top variable is best ranked)
#--- MLPLearningRate          : ---------------------------------------
#--- MLPLearningRate          : Rank : Variable       : Importance
#--- MLPLearningRate          : ---------------------------------------
#--- MLPLearningRate          :    1 : bjet1Pt        : 9.320e+01
#--- MLPLearningRate          :    2 : M_j1l          : 8.667e+01
#--- MLPLearningRate          :    3 : jet2Pt         : 7.767e+01
#--- MLPLearningRate          :    4 : Nbjets30       : 6.502e+01
#--- MLPLearningRate          :    5 : M_jjb          : 5.243e+01
#--- MLPLearningRate          :    6 : M_blnu         : 5.071e+01
#--- MLPLearningRate          :    7 : M_bl           : 5.014e+01
#--- MLPLearningRate          :    8 : MT_jjlnu       : 4.915e+01
#--- MLPLearningRate          :    9 : DeltaR_j1l     : 4.729e+01
#--- MLPLearningRate          :   10 : Pt_j1l         : 4.644e+01
#--- MLPLearningRate          :   11 : leptonPt       : 4.469e+01
#--- MLPLearningRate          :   12 : MET            : 4.177e+01
#--- MLPLearningRate          :   13 : jet1Pt         : 3.717e+01
#--- MLPLearningRate          :   14 : M_jjlnu        : 3.009e+01
#--- MLPLearningRate          :   15 : Pt_bl          : 2.516e+01
#--- MLPLearningRate          :   16 : bjet2Pt        : 2.476e+01
#--- MLPLearningRate          :   17 : MT_lnu         : 2.408e+01
#--- MLPLearningRate          :   18 : Pt_bb          : 2.200e+01
#--- MLPLearningRate          :   19 : M_bb_closest   : 1.829e+01
#--- MLPLearningRate          :   20 : DeltaR_bb1     : 1.613e+01
#--- MLPLearningRate          :   21 : Njets20        : 1.542e+01
#--- MLPLearningRate          :   22 : DeltaPhi_j1lbb : 1.366e+01
#--- MLPLearningRate          :   23 : DeltaR_j2l     : 7.622e+00
#--- MLPLearningRate          :   24 : DeltaR_jjl     : 7.140e+00
#--- MLPLearningRate          :   25 : DeltaPhi_lMET  : 7.029e+00
#--- MLPLearningRate          :   26 : DeltaR_jjb     : 4.896e+00
#--- MLPLearningRate          :   27 : DeltaR_b2l     : 4.818e+00
#--- MLPLearningRate          :   28 : DeltaR_jj      : 4.212e+00
#--- MLPLearningRate          :   29 : DeltaR_b1l     : 3.381e+00
#--- MLPLearningRate          : ---------------------------------------
#--- MLPSigmoid               : Ranking result (top variable is best ranked)
#--- MLPSigmoid               : ---------------------------------------
#--- MLPSigmoid               : Rank : Variable       : Importance
#--- MLPSigmoid               : ---------------------------------------
#--- MLPSigmoid               :    1 : Nbjets30       : 4.272e+01
#--- MLPSigmoid               :    2 : jet2Pt         : 3.808e+01
#--- MLPSigmoid               :    3 : M_blnu         : 3.721e+01
#--- MLPSigmoid               :    4 : bjet1Pt        : 3.662e+01
#--- MLPSigmoid               :    5 : M_jjb          : 3.201e+01
#--- MLPSigmoid               :    6 : M_bl           : 3.127e+01
#--- MLPSigmoid               :    7 : M_jjlnu        : 2.721e+01
#--- MLPSigmoid               :    8 : Pt_j1l         : 2.716e+01
#--- MLPSigmoid               :    9 : leptonPt       : 2.697e+01
#--- MLPSigmoid               :   10 : M_j1l          : 2.694e+01
#--- MLPSigmoid               :   11 : MET            : 2.621e+01
#--- MLPSigmoid               :   12 : jet1Pt         : 2.408e+01
#--- MLPSigmoid               :   13 : Pt_bl          : 2.283e+01
#--- MLPSigmoid               :   14 : MT_jjlnu       : 2.236e+01
#--- MLPSigmoid               :   15 : DeltaR_j1l     : 1.929e+01
#--- MLPSigmoid               :   16 : Pt_bb          : 1.831e+01
#--- MLPSigmoid               :   17 : Njets20        : 1.567e+01
#--- MLPSigmoid               :   18 : bjet2Pt        : 1.534e+01
#--- MLPSigmoid               :   19 : MT_lnu         : 1.264e+01
#--- MLPSigmoid               :   20 : M_bb_closest   : 8.698e+00
#--- MLPSigmoid               :   21 : DeltaR_bb1     : 8.336e+00
#--- MLPSigmoid               :   22 : DeltaPhi_j1lbb : 7.951e+00
#--- MLPSigmoid               :   23 : DeltaR_j2l     : 7.844e+00
#--- MLPSigmoid               :   24 : DeltaPhi_lMET  : 5.962e+00
#--- MLPSigmoid               :   25 : DeltaR_jjl     : 5.891e+00
#--- MLPSigmoid               :   26 : DeltaR_jjb     : 4.691e+00
#--- MLPSigmoid               :   27 : DeltaR_b2l     : 3.658e+00
#--- MLPSigmoid               :   28 : DeltaR_jj      : 3.211e+00
#--- MLPSigmoid               :   29 : DeltaR_b1l     : 1.633e+00
#--- MLPSigmoid               : ---------------------------------------
#--- Factory                  :
#--- BDT                      : Ranking result (top variable is best ranked)
#--- BDT                      : ------------------------------------------------
#--- BDT                      : Rank : Variable       : Variable Importance
#--- BDT                      : ------------------------------------------------
#--- BDT                      :    1 : Pt_bb          : 6.040e-02
#--- BDT                      :    2 : M_bb_closest   : 5.833e-02
#--- BDT                      :    3 : DeltaR_j1l     : 5.184e-02
#--- BDT                      :    4 : bjet1Pt        : 5.083e-02
#--- BDT                      :    5 : DeltaR_jjl     : 4.871e-02
#--- BDT                      :    6 : M_bl           : 4.817e-02
#--- BDT                      :    7 : DeltaR_j2l     : 4.633e-02
#--- BDT                      :    8 : DeltaR_bb1     : 4.625e-02
#--- BDT                      :    9 : leptonPt       : 4.541e-02
#--- BDT                      :   10 : jet1Pt         : 4.393e-02
#--- BDT                      :   11 : DeltaR_b2l     : 4.321e-02
#--- BDT                      :   12 : bjet2Pt        : 4.268e-02
#--- BDT                      :   13 : DeltaR_jjb     : 4.240e-02
#--- BDT                      :   14 : DeltaPhi_jjlbb : 4.126e-02
#--- BDT                      :   15 : DeltaR_b1l     : 4.117e-02
#--- BDT                      :   16 : Pt_bl          : 3.937e-02
#--- BDT                      :   17 : M_jjb          : 3.922e-02
#--- BDT                      :   18 : M_j1l          : 3.921e-02
#--- BDT                      :   19 : Pt_j1l         : 3.898e-02
#--- BDT                      :   20 : MET            : 3.869e-02
#--- BDT                      :   21 : M_jjlnu        : 3.662e-02
#--- BDT                      :   22 : jet2Pt         : 3.229e-02
#--- BDT                      :   23 : Nbjets30       : 2.469e-02
#--- BDT                      : ------------------------------------------------
#--- BDTTuned                 : Ranking result (top variable is best ranked)
#--- BDTTuned                 : ------------------------------------------------
#--- BDTTuned                 : Rank : Variable       : Variable Importance
#--- BDTTuned                 : ------------------------------------------------
#--- BDTTuned                 :    1 : Pt_bb          : 8.149e-02
#--- BDTTuned                 :    2 : bjet1Pt        : 6.355e-02
#--- BDTTuned                 :    3 : M_bb_closest   : 6.133e-02
#--- BDTTuned                 :    4 : DeltaR_j1l     : 5.980e-02
#--- BDTTuned                 :    5 : M_bl           : 5.135e-02
#--- BDTTuned                 :    6 : DeltaR_jjl     : 4.996e-02
#--- BDTTuned                 :    7 : M_j1l          : 4.843e-02
#--- BDTTuned                 :    8 : Pt_bl          : 4.532e-02
#--- BDTTuned                 :    9 : jet1Pt         : 4.404e-02
#--- BDTTuned                 :   10 : DeltaR_bb1     : 4.318e-02
#--- BDTTuned                 :   11 : leptonPt       : 4.191e-02
#--- BDTTuned                 :   12 : Pt_j1l         : 4.179e-02
#--- BDTTuned                 :   13 : M_jjb          : 4.087e-02
#--- BDTTuned                 :   14 : M_jjlnu        : 3.829e-02
#--- BDTTuned                 :   15 : DeltaR_j2l     : 3.776e-02
#--- BDTTuned                 :   16 : DeltaR_b1l     : 3.629e-02
#--- BDTTuned                 :   17 : DeltaPhi_jjlbb : 3.508e-02
#--- BDTTuned                 :   18 : DeltaR_b2l     : 3.324e-02
#--- BDTTuned                 :   19 : DeltaR_jjb     : 3.186e-02
#--- BDTTuned                 :   20 : jet2Pt         : 3.133e-02
#--- BDTTuned                 :   21 : MET            : 3.104e-02
#--- BDTTuned                 :   22 : Nbjets30       : 2.719e-02
#--- BDTTuned                 :   23 : bjet2Pt        : 2.491e-02
#--- BDTTuned                 : ------------------------------------------------
#--- BDTBoost                 : Ranking result (top variable is best ranked)
#--- BDTBoost                 : ------------------------------------------------
#--- BDTBoost                 : Rank : Variable       : Variable Importance
#--- BDTBoost                 : ------------------------------------------------
#--- BDTBoost                 :    1 : Pt_bb          : 7.080e-02
#--- BDTBoost                 :    2 : M_bb_closest   : 5.765e-02
#--- BDTBoost                 :    3 : DeltaR_j1l     : 5.600e-02
#--- BDTBoost                 :    4 : bjet1Pt        : 5.348e-02
#--- BDTBoost                 :    5 : jet1Pt         : 5.150e-02
#--- BDTBoost                 :    6 : M_bl           : 4.813e-02
#--- BDTBoost                 :    7 : leptonPt       : 4.611e-02
#--- BDTBoost                 :    8 : DeltaR_jjl     : 4.425e-02
#--- BDTBoost                 :    9 : DeltaR_bb1     : 4.410e-02
#--- BDTBoost                 :   10 : DeltaPhi_jjlbb : 4.385e-02
#--- BDTBoost                 :   11 : M_j1l          : 4.331e-02
#--- BDTBoost                 :   12 : Pt_bl          : 4.229e-02
#--- BDTBoost                 :   13 : M_jjb          : 4.180e-02
#--- BDTBoost                 :   14 : DeltaR_b1l     : 4.106e-02
#--- BDTBoost                 :   15 : Pt_j1l         : 4.062e-02
#--- BDTBoost                 :   16 : DeltaR_j2l     : 4.037e-02
#--- BDTBoost                 :   17 : DeltaR_jjb     : 4.015e-02
#--- BDTBoost                 :   18 : MET            : 3.733e-02
#--- BDTBoost                 :   19 : DeltaR_b2l     : 3.637e-02
#--- BDTBoost                 :   20 : M_jjlnu        : 3.436e-02
#--- BDTBoost                 :   21 : bjet2Pt        : 3.176e-02
#--- BDTBoost                 :   22 : jet2Pt         : 3.071e-02
#--- BDTBoost                 :   23 : Nbjets30       : 2.398e-02
#--- BDTBoost                 : ------------------------------------------------
#--- MLPTanh                  : Ranking result (top variable is best ranked)
#--- MLPTanh                  : ---------------------------------------
#--- MLPTanh                  : Rank : Variable       : Importance
#--- MLPTanh                  : ---------------------------------------
#--- MLPTanh                  :    1 : M_jjlnu        : 2.939e+01
#--- MLPTanh                  :    2 : M_j1l          : 2.937e+01
#--- MLPTanh                  :    3 : Nbjets30       : 2.818e+01
#--- MLPTanh                  :    4 : jet1Pt         : 2.736e+01
#--- MLPTanh                  :    5 : bjet1Pt        : 2.496e+01
#--- MLPTanh                  :    6 : jet2Pt         : 2.480e+01
#--- MLPTanh                  :    7 : M_bl           : 2.245e+01
#--- MLPTanh                  :    8 : leptonPt       : 2.146e+01
#--- MLPTanh                  :    9 : M_jjb          : 2.016e+01
#--- MLPTanh                  :   10 : bjet2Pt        : 1.956e+01
#--- MLPTanh                  :   11 : MET            : 1.929e+01
#--- MLPTanh                  :   12 : Pt_bl          : 1.604e+01
#--- MLPTanh                  :   13 : Pt_bb          : 1.523e+01
#--- MLPTanh                  :   14 : DeltaR_j1l     : 1.438e+01
#--- MLPTanh                  :   15 : Pt_j1l         : 1.410e+01
#--- MLPTanh                  :   16 : M_bb_closest   : 9.402e+00
#--- MLPTanh                  :   17 : DeltaPhi_jjlbb : 9.238e+00
#--- MLPTanh                  :   18 : DeltaR_j2l     : 5.915e+00
#--- MLPTanh                  :   19 : DeltaR_bb1     : 5.855e+00
#--- MLPTanh                  :   20 : DeltaR_jjl     : 4.661e+00
#--- MLPTanh                  :   21 : DeltaR_b2l     : 2.672e+00
#--- MLPTanh                  :   22 : DeltaR_jjb     : 1.765e+00
#--- MLPTanh                  :   23 : DeltaR_b1l     : 1.214e+00
#--- MLPTanh                  : ---------------------------------------
#--- MLPNodes2                : Ranking result (top variable is best ranked)
#--- MLPNodes2                : ---------------------------------------
#--- MLPNodes2                : Rank : Variable       : Importance
#--- MLPNodes2                : ---------------------------------------
#--- MLPNodes2                :    1 : Nbjets30       : 3.640e+01
#--- MLPNodes2                :    2 : bjet1Pt        : 3.223e+01
#--- MLPNodes2                :    3 : jet2Pt         : 2.938e+01
#--- MLPNodes2                :    4 : M_jjlnu        : 2.839e+01
#--- MLPNodes2                :    5 : M_j1l          : 2.815e+01
#--- MLPNodes2                :    6 : M_bl           : 2.232e+01
#--- MLPNodes2                :    7 : jet1Pt         : 2.209e+01
#--- MLPNodes2                :    8 : bjet2Pt        : 2.021e+01
#--- MLPNodes2                :    9 : DeltaR_j1l     : 1.914e+01
#--- MLPNodes2                :   10 : M_jjb          : 1.773e+01
#--- MLPNodes2                :   11 : leptonPt       : 1.656e+01
#--- MLPNodes2                :   12 : MET            : 1.632e+01
#--- MLPNodes2                :   13 : Pt_j1l         : 1.604e+01
#--- MLPNodes2                :   14 : Pt_bb          : 1.586e+01
#--- MLPNodes2                :   15 : Pt_bl          : 1.546e+01
#--- MLPNodes2                :   16 : M_bb_closest   : 1.221e+01
#--- MLPNodes2                :   17 : DeltaPhi_jjlbb : 7.891e+00
#--- MLPNodes2                :   18 : DeltaR_bb1     : 6.806e+00
#--- MLPNodes2                :   19 : DeltaR_j2l     : 5.982e+00
#--- MLPNodes2                :   20 : DeltaR_jjl     : 4.551e+00
#--- MLPNodes2                :   21 : DeltaR_b2l     : 2.913e+00
#--- MLPNodes2                :   22 : DeltaR_jjb     : 2.199e+00
#--- MLPNodes2                :   23 : DeltaR_b1l     : 1.619e+00
#--- MLPNodes2                : ---------------------------------------
#--- MLPSigmoid               : Ranking result (top variable is best ranked)
#--- MLPSigmoid               : ---------------------------------------
#--- MLPSigmoid               : Rank : Variable       : Importance
#--- MLPSigmoid               : ---------------------------------------
#--- MLPSigmoid               :    1 : jet2Pt         : 3.211e+01
#--- MLPSigmoid               :    2 : bjet1Pt        : 3.062e+01
#--- MLPSigmoid               :    3 : M_jjlnu        : 3.035e+01
#--- MLPSigmoid               :    4 : Nbjets30       : 2.980e+01
#--- MLPSigmoid               :    5 : M_j1l          : 2.702e+01
#--- MLPSigmoid               :    6 : jet1Pt         : 2.367e+01
#--- MLPSigmoid               :    7 : M_jjb          : 2.227e+01
#--- MLPSigmoid               :    8 : M_bl           : 2.131e+01
#--- MLPSigmoid               :    9 : leptonPt       : 2.028e+01
#--- MLPSigmoid               :   10 : Pt_bb          : 1.789e+01
#--- MLPSigmoid               :   11 : bjet2Pt        : 1.738e+01
#--- MLPSigmoid               :   12 : DeltaR_j1l     : 1.694e+01
#--- MLPSigmoid               :   13 : Pt_bl          : 1.593e+01
#--- MLPSigmoid               :   14 : Pt_j1l         : 1.455e+01
#--- MLPSigmoid               :   15 : M_bb_closest   : 1.428e+01
#--- MLPSigmoid               :   16 : MET            : 1.202e+01
#--- MLPSigmoid               :   17 : DeltaPhi_jjlbb : 8.912e+00
#--- MLPSigmoid               :   18 : DeltaR_j2l     : 5.719e+00
#--- MLPSigmoid               :   19 : DeltaR_jjl     : 5.219e+00
#--- MLPSigmoid               :   20 : DeltaR_bb1     : 5.198e+00
#--- MLPSigmoid               :   21 : DeltaR_b2l     : 2.768e+00
#--- MLPSigmoid               :   22 : DeltaR_jjb     : 1.624e+00
#--- MLPSigmoid               :   23 : DeltaR_b1l     : 1.194e+00
#--- MLPSigmoid               : ---------------------------------------
