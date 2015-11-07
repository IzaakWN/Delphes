import ROOT
from ROOT import TFile, TChain, TMVA, TCut
from array import array

# http://tmva.sourceforge.net/docu/TMVAUsersGuide.pdf
# https://aholzner.wordpress.com/2011/08/27/a-tmva-example-in-pyroot/
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



def train(treeS, treeB, var_names):

    TMVA.Tools.Instance()
    f_out = TFile("testNN.root","RECREATE")

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
    
    vars = [ ]
    for name in var_names:
        vars.append(array('f',[0]))
        reader.AddVariable(name,vars[-1])

    reader.BookMVA("BDT","weights/TMVAClassification_BDT.weights.xml")

    # fill histograms for signal and background from the test sample tree
    ROOT.TestTree.Draw("BDT>>hSig(22,-1.1,1.1)","classID == 0","goff")  # signal
    ROOT.TestTree.Draw("BDT>>hBg(22,-1.1,1.1)","classID == 1", "goff")  # background
     
    ROOT.hSig.SetLineColor(ROOT.kRed); # signal histogram
    ROOT.hBg.SetLineColor(ROOT.kBlue); # background histogram
    ROOT.hSig.SetLineWidth(2)
    ROOT.hBg.SetLineWidth(2)
     
    # use a THStack to show both histograms
    hist = ROOT.THStack("hs","")
    hist.Add(ROOT.hSig)
    hist.Add(ROOT.hBg)
     
    # show the histograms
    ROOT.gcSaver.append(ROOT.TCanvas())
    hist.Draw()



def main():
    print "Hello, world!"
    
    f_in_HH = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_all.root")
    f_in_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_all.root")
    
    treeS = f_in_HH.Get("stage_2/cleanup/cleanup")
    treeB = f_in_tt.Get("stage_2/cleanup/cleanup")
    
    var_names = [ "DeltaR_b1l", "DeltaR_bb1" ]

    train(treeS, treeB, var_names)
    examine(var_names)



if __name__ == '__main__':
    main()