from optparse import OptionParser
import sys
import ConfigParser
import ROOT
from ROOT import TFile, TChain, TMVA, TCut, TCanvas, THStack, TH1F
from array import array
import CMS_lumi, tdrstyle
from HHPlotterTools import *

# W

# http://tmva.sourceforge.net/docu/TMVAUsersGuide.pdf
# https://aholzner.wordpress.com/2011/08/27/a-tmva-example-in-pyroot/
# https://indico.cern.ch/event/395374/other-view?view=standard#20151109.detailed
#
# AdaBoost
# https://en.wikipedia.org/wiki/AdaBoost
#
#
# Gini-coefficient
# https://en.wikipedia.org/wiki/Gini_coefficient
# used to select the best variable to be used in each tree node
#
#

argv = sys.argv
parser = OptionParser()
parser.add_option("-o", "--onlyHist", dest="onlyHist", default=False, action="store_true",
                  help="Only make hist, don't go through training.")
(opts, args) = parser.parse_args(argv)



def train(treeS, treeB, var_names):

    TMVA.Tools.Instance()
    f_out = TFile("HH_MVA.root","RECREATE")

    factory = TMVA.Factory( "TMVAClassification", f_out,
                            ":".join([ "!V",
                            "!Silent",
                            "Color",
                            "DrawProgressBar",
                            "Transformations=I;D;P;G,D",
                            "AnalysisType=Classification" ]) )

    for name in var_names:
        factory.AddVariable(name,"F")

    factory.AddSignalTree(treeS)
    factory.AddBackgroundTree(treeB)

    cut_S = TCut("")
    cut_B = TCut("")

    factory.PrepareTrainingAndTestTree( cut_S, cut_B,
                                        ":".join([ "nTrain_Signal=0",
                                                   "nTrain_Background=0",
                                                   "SplitMode=Random",
                                                   "NormMode=NumEvents",
                                                   "!V" ]) )

    method = factory.BookMethod(TMVA.Types.kBDT, "BDT",
                                ":".join([ "!H",    # help text
                                           "!V",
                                           "NTrees=850",
                                           "nEventsMin=150",
                                           "MaxDepth=3",
                                           "BoostType=AdaBoost",
                                           "AdaBoostBeta=0.5",
                                           "SeparationType=GiniIndex",
                                           "nCuts=20",
                                           "PruneMethod=NoPruning" ]) )
 
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()



def examine(var_names):

    reader = TMVA.Reader()
    f = TFile("HH_MVA.root")
    TestTree = f.Get("TestTree")
    
    vars = [ ]
    for name in var_names:
        vars.append(array('f',[0]))
        reader.AddVariable(name,vars[-1])

    reader.BookMVA("BDT","weights/TMVAClassification_BDT.weights.xml")

    # fill histograms for signal and background from the test sample tree
    c = makeCanvas()
    hSig = TH1F("hSig", "hSig", 22, -1.1, 1.1)
    hBg = TH1F("hBg", "hBg", 22, -1.1, 1.1)
    TestTree.Draw("BDT>>hSig(22,-1.1,1.1)","classID == 0","goff")  # signal
    TestTree.Draw("BDT>>hBg(22,-1.1,1.1)","classID == 1", "goff")  # background

    norm(hSig,hBg)
    hSig.SetLineColor(ROOT.kRed); # signal histogram
    hSig.SetLineWidth(2)
    hBg.SetLineColor(ROOT.kBlue); # background histogram
    hBg.SetLineWidth(2)

    # draw histograms
    ROOT.hSig.Draw()
    ROOT.hBg.Draw("same")

#    # use a THStack to show both histograms
#    stack = THStack("hist","MVA output, vars: "+", ".join(var_names))
#    hist.Add(ROOT.hSig)
#    hist.Add(ROOT.hBg)

    # show the histograms
#    hist.Draw()
    CMS_lumi.CMS_lumi(c,14,33)
    c.SaveAs("MVA/HH_MVA_"+"_".join(var_names)+".png")
    c.Close()



def main():
    print "Hello, world!"
    
    f_in_HH = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_all.root")
    f_in_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_all.root")
    
    treeS = f_in_HH.Get("stage_2/cleanup/cleanup")
    treeB = f_in_tt.Get("stage_2/cleanup/cleanup")
    
    var_names = [ "DeltaR_b1l", "DeltaR_bb1" ]
    
    if not opts.onlyHist:
        train(treeS, treeB, var_names)
    examine(var_names)


if __name__ == '__main__':
    main()


