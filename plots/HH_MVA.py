from optparse import OptionParser
import sys
import os
import ConfigParser
import ROOT
from ROOT import TFile, gDirectory, TChain, TMVA, TCut, TCanvas, THStack, TH1F
from array import array
from copy import deepcopy
import CMS_lumi, tdrstyle
from HHPlotterTools import *
ROOT.gROOT.SetBatch(ROOT.kTRUE)

# W

# Manual: http://tmva.sourceforge.net/docu/TMVAUsersGuide.pdf
# Method ptions: http://tmva.sourceforge.net/optionRef.html
# Example in python: https://aholzner.wordpress.com/2011/08/27/a-tmva-example-in-pyroot/
# Tutorial: https://indico.cern.ch/event/395374/other-view?view=standard#20151109.detailed
#
# AdaBoost: https://en.wikipedia.org/wiki/AdaBoost
# Gini-coefficient https://en.wikipedia.org/wiki/Gini_coefficient
#   used to select the best variable to be used in each tree node
#
#

argv = sys.argv
parser = OptionParser()
parser.add_option("-t", "--test", dest="test", default=False, action="store_true",
                  help="Only train one configuration as test.")
parser.add_option("-p", "--onlyPlot", dest="onlyPlot", default=False, action="store_true",
                  help="Only plot, don't go through training.")
(opts, args) = parser.parse_args(argv)

    
f_in_HH = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_all.root")
f_in_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_all.root")
treeS = f_in_HH.Get("stage_2/cleanup/cleanup")
treeB = f_in_tt.Get("stage_2/cleanup/cleanup")
methods = [ ("LD","LD"), ("BDT","BDT"), ("BDT","BDTTuned"), ("MLP","MLPTuned") ] #, ("MLP","MLP")



class configuration(object):

    def __init__(self, name="nameless"):
        self.name = name
        self.varNames = [ ]
        self.treeS = treeS
        self.treeB = treeB
        self.hist_effs = [ ]



def train(config):
    print "\n>>> train with configuration "+config.name

    TMVA.Tools.Instance()
    f_out = TFile("HH_MVA_"+config.name+".root","RECREATE")

    factory = TMVA.Factory( "TMVAClassification", f_out,
                            ":".join([ "!V",
                            "!Silent",
                            "Color",
                            "DrawProgressBar",
                            "Transformations=I;D;P;G,D",
                            "AnalysisType=Classification" ]) )

    for name in config.varNames:
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

    # LD: Linear Classifier
    factory.BookMethod(TMVA.Types.kLD, "LD", "H:!V")

    # BDT: Boosted Decision Tree
    factory.BookMethod(TMVA.Types.kBDT, "BDT", "!H:!V" )

    # BDTTuned
    factory.BookMethod(TMVA.Types.kBDT, "BDTTuned",
                       ":".join([ "!H","!V",
                                  "NTrees=2000", # ~ number of boost steps, too large mainly costs time
                                  "nEventsMin=200",
                                  "MaxDepth=5", #  ~ 2-5 maximum tree depth (depends on the interaction of variables
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.5", # ~ 0.01-0.5
                                  "SeparationType=GiniIndex",
                                  "nCuts=20" ]) )

#    # MLP: Neutal Network
#    factory.BookMethod( TMVA.Types.kMLP, "MLP", "H:!V:" )

    # MLPTuned
    factory.BookMethod( TMVA.Types.kMLP, "MLPTuned",
                        ":".join([ "!H","!V",
                                   "NeuronType=tanh",
                                   "VarTransform=N",
                                   "HiddenLayers=N+10", # number of nodes in NN layers
                                   "UseRegulator" ]) ) # L2 norm regulator to avoid overtraining

 
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
    f_out.Close()
    for method in methods:
        os.rename("weights/TMVAClassification_"+method[1]+".weights.xml",
                  "weights/TMVAClassification_"+method[1]+"_"+config.name+".weights.xml")
#        os.rename("weights/TMVAClassification_"+method[1]+".weights.class.C",
#                  "weights/TMVAClassification_"+method[1]+"_"+config.name+".weights.class.C")



def plot(config):
    print "\n>>> examine training with configuration "+config.name

    reader = TMVA.Reader()
    f = TFile("HH_MVA_"+config.name+".root")
    TestTree = gDirectory.Get("TestTree")

    vars = [ ]
    for name in config.varNames:
        vars.append(array('f',[0]))
        reader.AddVariable(name,vars[-1])

    # HISTOGRAMS: TMVA output
    for Method, method in methods:
        reader.BookMVA(method,"weights/TMVAClassification_"+method+"_"+config.name+".weights.xml")

        c = makeCanvas()
        if Method == "MLP":
            histS = TH1F("histS", "", 26, -0.2, 1.2)
            histB = TH1F("histB", "", 26, -0.2, 1.2)
        else:
            histS = TH1F("histS", "", 48, -1.2, 1.2)
            histB = TH1F("histB", "", 48, -1.2, 1.2)
        config.hist_effs.append(deepcopy(gDirectory.Get("Method_"+Method+"/"+method+"/MVA_"+method+"_rejBvsS")) )
        TestTree.Draw(method+">>histS","classID == 0","goff") # causes problem when training not run
        TestTree.Draw(method+">>histB","classID == 1", "goff")
#        entries = mychain.GetEntriesFast()
#        for i in xrange( entries ):
#            j = mychain.LoadTree( i )
#            if TestTree.classID == 0:
#                histS.Fill(TestTree.BDT)
#            elif TestTree.classID == 1:
#                histB.Fill(TestTree.BDT)

        histS.SetLineColor(ROOT.kRed)
        histS.SetLineWidth(2)
        histB.SetLineColor(ROOT.kBlue)
        histB.SetLineWidth(2)
        histB.SetStats(0)

        histB.Draw() # draw first: mostly bigger
        histS.Draw("same")
        makeAxes(histS,histB,xlabel=method+" response",ylabel="")
        legend = makeLegend(histS,histB,title=method+" response",entries=["signal","background"])
        legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        c.SaveAs("MVA/"+method+"_"+config.name+".png")
        c.Close()
        gDirectory.Delete("histS")
        gDirectory.Delete("histB")



# HISTOGRAMS: compare all methods and variable configurations
def compare(configs):
    print "\n>>> compare all methods with all variable configurations"
    
    hist_effs = [ ]
    for config in configs:
        hist_effs.extend(config.hist_effs)
    
    if not hist_effs:
        return
    
    c = makeCanvas()
    hist_effs[0].Draw()
    hist_effs[0].SetLineWidth(2)
    hist_effs[0].SetStats(0)
    makeAxes(hist_effs[0],xlabel="signal efficiency",ylabel="background rejection")
    if len(hist_effs)>1:
        for hist in hist_effs[1:]:
            hist.Draw("same")
            hist.SetLineWidth(2)
    labels = [ ]
    for config in configs:
        labels.extend([config.name+", "+method[1] for method in methods])
    legend = makeLegend(*hist_effs,title="#splitline{background rejection}{vs. signal efficiency}",
                                   entries=labels, position="RightTop")
    legend.Draw()
    setLineColor(*hist_effs)
    CMS_lumi.CMS_lumi(c,14,33)
    c.SaveAs("MVA/BrejvsSeffs_"+config.name+".png")
    c.Close()



# 2D COLOR HISTOGRAM: Correlation matrices
def correlation(config):
    print "\n>>> make correlation matrix plots"

    reader = TMVA.Reader()
    f = TFile("HH_MVA_"+config.name+".root")
    TestTree = gDirectory.Get("TestTree")

    c = makeCanvas(square=True, scaleleftmargin=1.6, scalerightmargin=3)
    histS = f.Get("CorrelationMatrixS")
    histS.Draw("colz")
    makeLabels2D(histS,xaxis=True,yaxis=True)
    histS.SetLabelSize(0.072,"x")
    histS.SetLabelSize(0.072,"y")
#    CMS_lumi.CMS_lumi(c,14,33)
    c.SaveAs("MVA/CorrelationMatrixS.png")
    c.Close()

    c = makeCanvas(square=True, scaleleftmargin=1.6, scalerightmargin=3)
    histB = f.Get("CorrelationMatrixB")
    histB.Draw("colz")
    makeLabels2D(histB,xaxis=True,yaxis=True)
    histB.SetLabelSize(0.72,"x")
    histB.SetLabelSize(0.72,"y")
#    CMS_lumi.CMS_lumi(c,14,33)
    c.SaveAs("MVA/CorrelationMatrixB.png")
    c.Close()



def main():
    
    varNames = [ "DeltaR_j1l", "DeltaR_j2l",
                 "DeltaR_b1l", "DeltaR_b2l",
                 "DeltaR_bb1", "M_bb_closest",
                 "jet1Pt",  "jet2Pt",
                 "bjet1Pt", "bjet2Pt", ]

    configs = [ configuration(), configuration("topology"), configuration("best") ]

    configs[0].name = "everything"
    configs[0].varNames = varNames[:]

    configs[1].name = "topology"
    configs[1].varNames = varNames[:6]

    configs[2].name = "best"
    configs[2].varNames = ["DeltaR_bb1", "M_bb_closest", "DeltaR_b1l", "DeltaR_j1l"]
    
    if opts.test:
        configs = configs[2:3]

    for config in configs:
        if not opts.onlyPlot:
            train(config)
        plot(config)
    compare(configs)
    correlation(configs[0])



if __name__ == '__main__':
    main()


#
#--- Factory                  : Ranking input variables (method specific)...
#--- LD                       : Ranking result (top variable is best ranked)
#--- LD                       : ---------------------------------------
#--- LD                       : Rank : Variable     : Discr. power
#--- LD                       : ---------------------------------------
#--- LD                       :    1 : DeltaR_j1l   : 1.805e-01
#--- LD                       :    2 : DeltaR_b1l   : 1.188e-01
#--- LD                       :    3 : DeltaR_bb1   : 1.044e-01
#--- LD                       :    4 : DeltaR_j2l   : 1.375e-02
#--- LD                       :    5 : bjet1Pt      : 1.611e-03
#--- LD                       :    6 : DeltaR_b2l   : 6.553e-04
#--- LD                       :    7 : jet2Pt       : 6.379e-04
#--- LD                       :    8 : bjet2Pt      : 6.369e-04
#--- LD                       :    9 : M_bb_closest : 5.200e-04
#--- LD                       :   10 : jet1Pt       : 2.463e-04
#--- LD                       : ---------------------------------------
#--- BDT                      : Ranking result (top variable is best ranked)
#--- BDT                      : ----------------------------------------------
#--- BDT                      : Rank : Variable     : Variable Importance
#--- BDT                      : ----------------------------------------------
#--- BDT                      :    1 : DeltaR_b1l   : 1.536e-01
#--- BDT                      :    2 : DeltaR_j1l   : 1.407e-01
#--- BDT                      :    3 : DeltaR_j2l   : 1.183e-01
#--- BDT                      :    4 : jet1Pt       : 1.051e-01
#--- BDT                      :    5 : M_bb_closest : 1.014e-01
#--- BDT                      :    6 : DeltaR_bb1   : 9.944e-02
#--- BDT                      :    7 : DeltaR_b2l   : 8.322e-02
#--- BDT                      :    8 : bjet2Pt      : 6.784e-02
#--- BDT                      :    9 : bjet1Pt      : 6.658e-02
#--- BDT                      :   10 : jet2Pt       : 6.382e-02
#--- BDT                      : ----------------------------------------------
#--- BDTTuned                 : Ranking result (top variable is best ranked)
#--- BDTTuned                 : ----------------------------------------------
#--- BDTTuned                 : Rank : Variable     : Variable Importance
#--- BDTTuned                 : ----------------------------------------------
#--- BDTTuned                 :    1 : DeltaR_j2l   : 1.144e-01
#--- BDTTuned                 :    2 : DeltaR_j1l   : 1.143e-01
#--- BDTTuned                 :    3 : DeltaR_b1l   : 1.091e-01
#--- BDTTuned                 :    4 : DeltaR_bb1   : 1.050e-01
#--- BDTTuned                 :    5 : M_bb_closest : 1.010e-01
#--- BDTTuned                 :    6 : bjet2Pt      : 9.433e-02
#--- BDTTuned                 :    7 : DeltaR_b2l   : 9.308e-02
#--- BDTTuned                 :    8 : jet2Pt       : 9.258e-02
#--- BDTTuned                 :    9 : bjet1Pt      : 8.958e-02
#--- BDTTuned                 :   10 : jet1Pt       : 8.670e-02
#--- BDTTuned                 : ----------------------------------------------
#--- MLP                      : Ranking result (top variable is best ranked)
#--- MLP                      : -------------------------------------
#--- MLP                      : Rank : Variable     : Importance
#--- MLP                      : -------------------------------------
#--- MLP                      :    1 : DeltaR_j1l   : -nan
#--- MLP                      :    2 : DeltaR_j2l   : -nan
#--- MLP                      :    3 : DeltaR_b1l   : -nan
#--- MLP                      :    4 : DeltaR_b2l   : -nan
#--- MLP                      :    5 : DeltaR_bb1   : -nan
#--- MLP                      :    6 : M_bb_closest : -nan
#--- MLP                      :    7 : jet1Pt       : -nan
#--- MLP                      :    8 : jet2Pt       : -nan
#--- MLP                      :    9 : bjet1Pt      : -nan
#--- MLP                      :   10 : bjet2Pt      : -nan
#--- MLP                      : -------------------------------------
#--- MLPTuned                 : Ranking result (top variable is best ranked)
#--- MLPTuned                 : -------------------------------------
#--- MLPTuned                 : Rank : Variable     : Importance
#--- MLPTuned                 : -------------------------------------
#--- MLPTuned                 :    1 : DeltaR_b2l   : 5.444e+01
#--- MLPTuned                 :    2 : M_bb_closest : 3.649e+01
#--- MLPTuned                 :    3 : bjet1Pt      : 2.796e+01
#--- MLPTuned                 :    4 : bjet2Pt      : 2.388e+01
#--- MLPTuned                 :    5 : jet1Pt       : 2.355e+01
#--- MLPTuned                 :    6 : jet2Pt       : 1.579e+01
#--- MLPTuned                 :    7 : DeltaR_j1l   : 1.142e+01
#--- MLPTuned                 :    8 : DeltaR_bb1   : 8.354e+00
#--- MLPTuned                 :    9 : DeltaR_b1l   : 1.892e+00
#--- MLPTuned                 :   10 : DeltaR_j2l   : 1.080e+00
#--- MLPTuned                 : -------------------------------------
#


