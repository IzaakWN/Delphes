from optparse import OptionParser
import sys
import ConfigParser
import ROOT
from ROOT import TFile, gDirectory, TChain, TMVA, TCut, TCanvas, THStack, TH1F
from array import array
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
methods = [ ]



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
                                        ":".join([ "nTrain_Signal=0",
                                                   "nTrain_Background=0",
                                                   "SplitMode=Random",
                                                   "NormMode=NumEvents",
                                                   "!V" ]) )

    method = factory.BookMethod(TMVA.Types.kBDT, "BDT",
                                ":".join([ "!H",    # help text, too large mainly costs time
                                           "!V",
                                           "NTrees=1000", # ~ number of boost steps
                                           "nEventsMin=150",
                                           "MaxDepth=3", #  ~ 2-5 maximum tree depth (depends on the interaction of variables
                                           "BoostType=AdaBoost",
                                           "AdaBoostBeta=0.5", # ~ 0.01-0.5
                                           "SeparationType=GiniIndex",
                                           "nCuts=20",
                                           "PruneMethod=NoPruning" ]) )

    method = factory.BookMethod(TMVA.Types.kBDT, "BDTTuned",
                                ":".join([ "!H",
                                           "!V",
                                           "NTrees=2000",
                                           "nEventsMin=200",
                                           "MaxDepth=5",
                                           "BoostType=AdaBoost",
                                           "AdaBoostBeta=0.5",
                                           "SeparationType=GiniIndex",
                                           "nCuts=20" ]) )
    
    global methods
    methods = [ ("BDT","BDT"), ("BDT","BDTTuned") ]
 
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
    f_out.Close()



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
        reader.BookMVA(method,"weights/TMVAClassification_"+method+".weights.xml")

        c = makeCanvas()
        histS = TH1F("histS", "", 44, -1.1, 1.1)
        histB = TH1F("histB", "", 44, -1.1, 1.1)
        config.hist_effs.append(gDirectory.Get("Method_"+Method+"/"+method+"/MVA_"+method+"_rejBvsS"))
        TestTree.Draw(method+">>histS","classID == 0","goff") # causes problem when training not run
        TestTree.Draw(method+">>histB","classID == 1", "goff")
#        entries = mychain.GetEntriesFast()
#        for i in xrange( entries ):
#            j = mychain.LoadTree( i )
#            if TestTree.classID == 0:
#                histS.Fill(TestTree.BDT)
#            elif TestTree.classID == 1:
#                histB.Fill(TestTree.BDT)

        norm(histS,histB)
        histS.SetLineColor(ROOT.kRed)
        histS.SetLineWidth(2)
        histB.SetLineColor(ROOT.kBlue)
        histB.SetLineWidth(2)
        histB.SetStats(0)
        histB.GetXaxis().SetTitle(method+" output")

        histB.Draw() # draw first: mostly bigger
        histS.Draw("same")
        legend = makeLegend(histS,histB,title=method+" seperation",entries=["signal","background"])
        legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        c.SaveAs("MVA/"+method+"_"+config.name+".png")
        c.Close()
        gDirectory.Delete("histS")
        gDirectory.Delete("histB")



# HISTOGRAMS: compare all methods and variable configurations
def compare(configs):
    
    hists_effs = [ ]
    for config in configs:
        hist_effs.extend(config.hist_effs)
    
    if not hists_effs:
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

    reader = TMVA.Reader()
    f = TFile("HH_MVA_"+config.name+".root")
    TestTree = gDirectory.Get("TestTree")

    c = makeCanvas(square=True)
    histS = f.Get("CorrelationMatrixS.png")
    histS.Draw("colz")
    makeAxes2D(histS)
    CMS_lumi.CMS_lumi(c,14,33)
    c.SaveAs("MVA/CorrelationMatrixS.png")
    c.Close()

    c = makeCanvas(square=True)
    histB = f.Get("CorrelationMatrixB.png")
    histB.Draw("colz")
    makeAxes2D(histB)
    CMS_lumi.CMS_lumi(c,14,33)
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


