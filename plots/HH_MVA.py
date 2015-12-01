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

# Manual: http://tmva.sourceforge.net/docu/TMVAUsersGuide.pdf
# Method options: http://tmva.sourceforge.net/optionRef.html
# Example in python: https://aholzner.wordpress.com/2011/08/27/a-tmva-example-in-pyroot/
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
            ("BDT","BDTMaxDepth"),
#            ("BDT","BDTCuts"),
            ("BDT","BDTBoost"),
            ("BDT","BDTNodeSize"),
            ("MLP","MLPTanh"),
            ("MLP","MLPLearningRate"),
#            ("MLP","MLPNodes"),
            ("MLP","MLPSigmoid") ]
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

h0_S = file_HH.Get("stage_0/selection/category") # ~ 166483
h0_B = file_tt.Get("stage_0/selection/category") # ~ 164661
print h0_S.GetBinContent(1)
print h0_B.GetBinContent(1)
S_tot = 166483 #h0_S.GetBinContent(1)
B_tot = 164661 #h0_B.GetBinContent(1)
S1 = h0_S.GetBinContent(2)
B1 = h0_B.GetBinContent(2)
S2 = h0_S.GetBinContent(3)
B2 = h0_B.GetBinContent(3)
S3 = h0_S.GetBinContent(4)
B3 = h0_B.GetBinContent(4)
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

    def __init__(self, name, varNames, stage):
        self.name = name
        self.varNames = varNames
        self.treeS = None
        self.treeB = None
        self.hist_effs = [ ]
#        self.significances
        if stage==1:
            self.treeS = treeS1
            self.treeB = treeB1
        elif stage==2:
            self.treeS = treeS2
            self.treeB = treeB2
        elif stage==3:
            self.treeS = treeS3
            self.treeB = treeB3



def train(config):
    print "\n>>> train with configuration "+config.name

    TMVA.Tools.Instance()
    f_out = TFile("MVA/trees/HH_MVA_"+config.name+".root","RECREATE")

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

#    # LD: Linear Classifier
#    factory.BookMethod(TMVA.Types.kLD, "LD", "H:!V")

    # BDT: Boosted Decision Tree
    factory.BookMethod(TMVA.Types.kBDT, "BDT", "!H:!V" )
    # BDTTuned
    factory.BookMethod(TMVA.Types.kBDT, "BDTTuned",
                       ":".join([ "!H","!V",
                                  "NTrees=2000",
                                  "MinNodeSize=10.%", # 2 ->
#                                  "nEventsMin=200",
                                  "MaxDepth=3",
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.1", # 0.3 -> 0.1
                                  "SeparationType=GiniIndex",
                                  "nCuts=70" # 20 -> 70
                                 ]) )
    # BDTMaxDepth
    factory.BookMethod(TMVA.Types.kBDT, "BDTMaxDepth",
                       ":".join([ "!H","!V",
                                  "NTrees=2000",
#                                  "MinNodeSize=1.%",
#                                  "nEventsMin=200",
                                  "MaxDepth=5", # 3 -> 5
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.3",
                                  "SeparationType=GiniIndex",
                                  "nCuts=20"
                                 ]) )
    # BDTBoost
    factory.BookMethod(TMVA.Types.kBDT, "BDTMaxDepth",
                       ":".join([ "!H","!V",
                                  "NTrees=2000",
#                                  "MinNodeSize=1.%",
#                                  "nEventsMin=200",
                                  "MaxDepth=5",
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.05", # 0.1 -> 0.05
                                  "SeparationType=GiniIndex",
                                  "nCuts=20"
                                 ]) )
    # BDTNodeSize
    factory.BookMethod(TMVA.Types.kBDT, "BDTNodeSize",
                       ":".join([ "!H","!V",
                                  "NTrees=2000",
                                  "MinNodeSize=20.%", # 10.% -> 20.%
#                                  "nEventsMin=200",
                                  "MaxDepth=3",
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.1",
                                  "SeparationType=GiniIndex",
                                  "nCuts=20"
                                 ]) )
    # MLPTanh
    factory.BookMethod( TMVA.Types.kMLP, "MLPTanh",
                        ":".join([ "!H","!V",
                                   "LearningRate=0.01",
#                                   "NCycles=200",
                                   "NeuronType=tanh",
                                   "VarTransform=N",
                                   "HiddenLayers=N+9,N",
                                   "UseRegulator"
                                  ]) )
    # MLPLearningRate
    factory.BookMethod( TMVA.Types.kMLP, "MLPLearningRate",
                        ":".join([ "!H","!V",
                                   "LearningRate=0.1",
#                                   "NCycles=200",
                                   "NeuronType=tanh",
                                   "VarTransform=N",
                                   "HiddenLayers=N+9,N",
                                   "UseRegulator"
                                  ]) )
#    # MLPNodes
#    # Warning: use ROOT 34 or newer for larger buffer for the xml reader
#    factory.BookMethod( TMVA.Types.kMLP, "MLPNodes",
#                        ":".join([ "!H","!V",
##                                   "LearningRate=0.02",
##                                   "NCycles=200",
#                                   "NeuronType=tanh",
#                                   "VarTransform=N",
#                                   "HiddenLayers=N,N",
#                                   "UseRegulator"
#                                  ]) )
    # MLPSigmoid
    factory.BookMethod( TMVA.Types.kMLP, "MLPSigmoid",
                        ":".join([ "!H","!V",
                                   "LearningRate=0.01",
#                                   "NCycles=200",
                                   "NeuronType=sigmoid",
                                   "VarTransform=N",
                                   "HiddenLayers=N+9,N",
                                   "UseRegulator"
                                  ]) )

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
    f_out.Close()

    # move files from weights/ to MVA/weights/configname
    weightsdir = "MVA/weights/"+config.name
    if not os.path.exists(weightsdir):
        os.makedirs(weightsdir)
    for method in methods:
        os.rename("weights/TMVAClassification_"+method+".weights.xml",
                  weightsdir+"/TMVAClassification_"+method+".weights.xml")
        os.rename("weights/TMVAClassification_"+method+".class.C",
                  weightsdir+"/TMVAClassification_"+method+".class.C")



# SIGNIFICANCE
def significance(histS,histB):
    
    Pmax = 0
    Smax = 0
    Bmax = 0
    imax = 0

    # scan cut over all bins, find cut with highest significance
    N = histS.GetNbinsX()
    for i in range(1,N):
        S = N_S * histS.Integral(i,N) / S_tot # yield
        B = N_B * histB.Integral(i,N) / B_tot
        P = S / sqrt(1+B)
        if Pmax<P and S > 10 and B > 10:
            Pmax = P
            Smax = S
            Bmax = B
            imax = i

    return [Pmax,Smax,Bmax,histS.GetXaxis().GetBinCenter(imax)]



# SIGNIFICANCE
def significanceBins(histS,histB):
    
    P2 = 0

    # calculate significance per bin and add
    # using variance addition law: sigma^2 = sum(sigma_i^2)
    N = histS.GetNbinsX()
    for i in range(1,N):
        S = N_S * histS.GetBinContent(i) / S_tot # yield for bin i
        B = N_B * histB.GetBinContent(i) / B_tot
        P2 += S*S/(1+B) # P^2 += P_i^2

    return sqrt(P2)



# HISTOGRAMS: TMVA output
def plot(config):
    print "\n>>> examine training with configuration "+config.name

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
            histS = TH1F("histS", "", 100, -0.4, 1.4)
            histB = TH1F("histB", "", 100, -0.4, 1.4)
        else:
            histS = TH1F("histS", "", 100, -1.4, 1.4)
            histB = TH1F("histB", "", 100, -1.4, 1.4)
        config.hist_effs.append(deepcopy(gDirectory.Get("Method_"+Method+"/"+method+"/MVA_"+method+"_rejBvsS")) )
        TestTree.Draw(method+">>histS","classID == 0","goff")
        TestTree.Draw(method+">>histB","classID == 1", "goff")

        [Pmax,Smax,Bmax,cut] = significance(histS,histB)
        Pbins = significanceBins(histS, histB)
        significances.append( ">>> "+config.name+" - "+method + \
                              ":\n>>>\t\t%.4f significance, yields S = %.1f, B = %.1f with a cut at %.4f" % \
                              (Pmax,Smax,Bmax,cut) + \
                              "\n>>>\t\t%.4f significance with bins" % Pbins  )

        histS.SetLineColor(ROOT.kRed)
        histS.SetLineWidth(2)
        histB.SetLineColor(ROOT.kBlue)
        histB.SetLineWidth(2)
        histB.SetStats(0)

        histB.Draw() # draw first: mostly bigger
        histS.Draw("same")
        makeAxes(histB,histS,xlabel=(method+" response"),ylabel="")
        legend = makeLegend(histS,histB,title=method+" response",entries=["signal","background"],position="RightTopTop")
        legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        c.SaveAs("MVA/"+method+"_"+config.name+".png")
        c.Close()
        gDirectory.Delete("histS")
        gDirectory.Delete("histB")

    for s in significances:
        print s



# HISTOGRAMS: compare all methods and variable configurations
def compare(configs,stage="",methods0=methods):
    print "\n>>> compare methods with "+", ".join([c.name for c in configs])
    
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
    hist_effs[0].SetLineWidth(2)
    hist_effs[0].SetStats(0)
    makeAxes(hist_effs[0],xlabel="signal efficiency",ylabel="background rejection")
    if len(hist_effs)>1:
        for hist in hist_effs[1:]:
            hist.Draw("same")
            hist.SetLineWidth(2)
    labels = [ ]
    for config in configs:
        labels.extend([config.name+", "+method for method in methods])
    legend = makeLegend(*hist_effs,title="#splitline{background rejection}{vs. signal efficiency}",
                                   entries=labels, position="RightTop")
    legend.Draw()
    setLineColor(*hist_effs)
    CMS_lumi.CMS_lumi(c,14,33)
    c.SaveAs("MVA/BrejvsSeffs_"+stage+".png")
    c.Close()



# 2D COLOR HISTOGRAM: Correlation matrices
def correlation(config):
    print "\n>>> make correlation matrix plots"

    reader = TMVA.Reader()
    f = TFile("MVA/trees/HH_MVA_"+config.name+".root")
    TestTree = gDirectory.Get("TestTree")

    c = makeCanvas(square=True, scaleleftmargin=1.5)
    histS = f.Get("CorrelationMatrixS")
    histS.Draw("colz")
    makeLabels2D(histS,xaxis=True,yaxis=True)
    histS.SetLabelSize(0.048,"x")
    histS.SetLabelSize(0.062,"y")
#    CMS_lumi.CMS_lumi(c,14,33)
    c.SaveAs("MVA/CorrelationMatrixS_"+config.name+".png")
    c.Close()

    c = makeCanvas(square=True, scaleleftmargin=1.5)
    histB = f.Get("CorrelationMatrixB")
    histB.Draw("colz")
    makeLabels2D(histB,xaxis=True,yaxis=True)
    histB.SetLabelSize(0.048,"x")
    histB.SetLabelSize(0.062,"y")
#    CMS_lumi.CMS_lumi(c,14,33)
    c.SaveAs("MVA/CorrelationMatrixB_"+config.name+".png")
    c.Close()



def main():
    
    allVars = [ "Njets20","Nbjets30",
                "jet1Pt","jet2Pt",
                "bjet1Pt","bjet2Pt",
                "leptonPt","MET",
                "DeltaR_j1l","DeltaR_j2l",
                "DeltaR_b1l","DeltaR_b2l",
                "DeltaR_bb1","DeltaR_jj",
                "DeltaR_jjl","DeltaR_jjb",
                "DeltaPhi_lMET",
                "M_bb_closest", "M_jjlnu", # Higgs reconstruction
                "M_jjb", "M_blnu",         # top reconstruction
                "MT_lnu","MT_jjlnu" ]

    betterVars = [  "Nbjets30",
                    "jet1Pt","jet2Pt",
                    "bjet1Pt","bjet2Pt",
                    "leptonPt","MET",
                    "DeltaR_j1l","DeltaR_j2l",
                    "DeltaR_b1l","DeltaR_b2l",
                    "DeltaR_bb1",
                    "DeltaR_jjl","DeltaR_jjb",
                    "M_bb_closest", "M_jjlnu",
                    "M_jjb", "M_blnu" ]

#    bestVars = [    "Nbjets30",
#                    "bjet1Pt","bjet2Pt",
#                    "leptonPt",
#                    "DeltaR_j1l","DeltaR_j2l",
#                    "DeltaR_b1l","DeltaR_b2l",
#                    "DeltaR_bb1",
#                    "DeltaR_jjl","DeltaR_jjb",
#                    "M_bb_closest", "M_jjlnu",
#                    "M_jjb", "M_blnu" ]

#    MLPTop10Vars = [ "Nbjets30",
#                     "jet1Pt","jet2Pt",
#                     "bjet1Pt","bjet2Pt",
#                     "leptonPt",
##                     "DeltaR_bb1",
#                     "M_bb_closest", "M_jjlnu",
#                     "M_jjb", "M_blnu" ]

#    favVars = [ "DeltaR_b1l", "DeltaR_b2l", "DeltaR_bb1",
#                "DeltaR_j1l", "DeltaR_j2l",
#                "M_bb_closest", "M_jjlnu",
#                "M_jjb", "M_blnu" ]

    if opts.test:
        print ">>> test mode"
        configs = [configuration("test", ["M_bb_closest", "DeltaR_bb1"], 1)]
    else:
        configs = [
#                    configuration("everything20", allVars, 1),
#                    configuration("better20", betterVars, 1),
#                    configuration("best20",   bestVars, 1),
#                    configuration("MLPTop20", MLPTop10Vars, 1),
#                    configuration("favs20",   favVars, 1),
#                    configuration("everythingCleanUp", allVars, 2),
                    configuration("betterCleanUp", betterVars, 2),
#                    configuration("bestCleanUp",   bestVars, 2),
#                    configuration("MLPTopCleanUp", MLPTop10Vars, 2),
#                    configuration("favsCleanUp",   favVars, 2)
                   ]

    if opts.onlyPlot:
        print ">>> plots only"
    else:
        for config in reversed(configs):
            train(config)
    for config in configs:
        plot(config)
    compare(configs[:len(configs)/2],stage="stage_1")
    compare(configs[len(configs)/2:],stage="stage_2")
    compare(configs[:len(configs)/2],stage="stage_1_DBT",methods0=[m for m in methods if "BDT" in m])
    compare(configs[:len(configs)/2],stage="stage_1_MLP",methods0=[m for m in methods if "MLP" in m])

    for config in configs:
        if "everything" in config.name:
            correlation(config)



if __name__ == '__main__':
    main()


# strong correlations between:
#    M_bb vs. DeltaR_bb
#    M_bb vs. bjet1, bjet2 for background
#



#--- Factory                  : Ranking input variables (method specific)...
#--- BDT                      : Ranking result (top variable is best ranked)
#--- BDT                      : ----------------------------------------------
#--- BDT                      : Rank : Variable     : Variable Importance
#--- BDT                      : ----------------------------------------------
#--- BDT                      :    1 : DeltaR_b1l   : 8.348e-02
#--- BDT                      :    2 : DeltaR_bb1   : 7.458e-02
#--- BDT                      :    3 : DeltaR_b2l   : 7.071e-02
#--- BDT                      :    4 : bjet1Pt      : 6.810e-02
#--- BDT                      :    5 : leptonPt     : 6.797e-02
#--- BDT                      :    6 : M_bb_closest : 6.744e-02
#--- BDT                      :    7 : DeltaR_jjb   : 6.633e-02
#--- BDT                      :    8 : M_jjlnu      : 5.746e-02
#--- BDT                      :    9 : DeltaR_j1l   : 5.320e-02
#--- BDT                      :   10 : MET          : 5.112e-02
#--- BDT                      :   11 : DeltaR_jjl   : 4.788e-02
#--- BDT                      :   12 : M_jjb        : 4.712e-02
#--- BDT                      :   13 : M_blnu       : 4.658e-02
#--- BDT                      :   14 : DeltaR_j2l   : 4.607e-02
#--- BDT                      :   15 : jet1Pt       : 4.550e-02
#--- BDT                      :   16 : bjet2Pt      : 4.542e-02
#--- BDT                      :   17 : jet2Pt       : 3.192e-02
#--- BDT                      :   18 : Nbjets30     : 2.912e-02
#--- BDT                      : ----------------------------------------------
#--- BDTTuned                 : Ranking result (top variable is best ranked)
#--- BDTTuned                 : ----------------------------------------------
#--- BDTTuned                 : Rank : Variable     : Variable Importance
#--- BDTTuned                 : ----------------------------------------------
#--- BDTTuned                 :    1 : M_bb_closest : 1.470e-01
#--- BDTTuned                 :    2 : DeltaR_bb1   : 1.133e-01
#--- BDTTuned                 :    3 : DeltaR_b1l   : 9.707e-02
#--- BDTTuned                 :    4 : DeltaR_b2l   : 8.975e-02
#--- BDTTuned                 :    5 : jet1Pt       : 6.760e-02
#--- BDTTuned                 :    6 : leptonPt     : 6.432e-02
#--- BDTTuned                 :    7 : DeltaR_jjb   : 4.899e-02
#--- BDTTuned                 :    8 : DeltaR_j1l   : 4.463e-02
#--- BDTTuned                 :    9 : M_blnu       : 4.200e-02
#--- BDTTuned                 :   10 : M_jjlnu      : 4.021e-02
#--- BDTTuned                 :   11 : M_jjb        : 3.975e-02
#--- BDTTuned                 :   12 : DeltaR_j2l   : 3.680e-02
#--- BDTTuned                 :   13 : MET          : 3.579e-02
#--- BDTTuned                 :   14 : bjet1Pt      : 3.079e-02
#--- BDTTuned                 :   15 : jet2Pt       : 2.867e-02
#--- BDTTuned                 :   16 : bjet2Pt      : 2.790e-02
#--- BDTTuned                 :   17 : DeltaR_jjl   : 2.686e-02
#--- BDTTuned                 :   18 : Nbjets30     : 1.852e-02
#--- BDTTuned                 : ----------------------------------------------
#--- BDTCuts                  : Ranking result (top variable is best ranked)
#--- BDTCuts                  : ----------------------------------------------
#--- BDTCuts                  : Rank : Variable     : Variable Importance
#--- BDTCuts                  : ----------------------------------------------
#--- BDTCuts                  :    1 : leptonPt     : 8.336e-02
#--- BDTCuts                  :    2 : DeltaR_bb1   : 7.889e-02
#--- BDTCuts                  :    3 : M_bb_closest : 7.424e-02
#--- BDTCuts                  :    4 : DeltaR_j1l   : 7.165e-02
#--- BDTCuts                  :    5 : DeltaR_jjb   : 6.601e-02
#--- BDTCuts                  :    6 : DeltaR_b1l   : 6.522e-02
#--- BDTCuts                  :    7 : DeltaR_b2l   : 6.112e-02
#--- BDTCuts                  :    8 : jet1Pt       : 6.075e-02
#--- BDTCuts                  :    9 : bjet2Pt      : 5.597e-02
#--- BDTCuts                  :   10 : DeltaR_jjl   : 5.518e-02
#--- BDTCuts                  :   11 : M_jjb        : 5.444e-02
#--- BDTCuts                  :   12 : MET          : 5.390e-02
#--- BDTCuts                  :   13 : M_blnu       : 5.380e-02
#--- BDTCuts                  :   14 : bjet1Pt      : 4.969e-02
#--- BDTCuts                  :   15 : M_jjlnu      : 4.412e-02
#--- BDTCuts                  :   16 : DeltaR_j2l   : 3.612e-02
#--- BDTCuts                  :   17 : jet2Pt       : 2.002e-02
#--- BDTCuts                  :   18 : Nbjets30     : 1.552e-02
#--- BDTCuts                  : ----------------------------------------------
#--- BDTBoost                 : Ranking result (top variable is best ranked)
#--- BDTBoost                 : ----------------------------------------------
#--- BDTBoost                 : Rank : Variable     : Variable Importance
#--- BDTBoost                 : ----------------------------------------------
#--- BDTBoost                 :    1 : M_bb_closest : 9.722e-02
#--- BDTBoost                 :    2 : DeltaR_b2l   : 9.047e-02
#--- BDTBoost                 :    3 : DeltaR_bb1   : 8.576e-02
#--- BDTBoost                 :    4 : DeltaR_b1l   : 8.127e-02
#--- BDTBoost                 :    5 : DeltaR_j1l   : 6.761e-02
#--- BDTBoost                 :    6 : leptonPt     : 6.263e-02
#--- BDTBoost                 :    7 : M_blnu       : 5.581e-02
#--- BDTBoost                 :    8 : jet2Pt       : 5.502e-02
#--- BDTBoost                 :    9 : jet1Pt       : 5.457e-02
#--- BDTBoost                 :   10 : bjet1Pt      : 5.412e-02
#--- BDTBoost                 :   11 : M_jjlnu      : 4.542e-02
#--- BDTBoost                 :   12 : M_jjb        : 4.262e-02
#--- BDTBoost                 :   13 : DeltaR_jjl   : 4.063e-02
#--- BDTBoost                 :   14 : DeltaR_jjb   : 3.980e-02
#--- BDTBoost                 :   15 : bjet2Pt      : 3.843e-02
#--- BDTBoost                 :   16 : DeltaR_j2l   : 3.694e-02
#--- BDTBoost                 :   17 : MET          : 3.220e-02
#--- BDTBoost                 :   18 : Nbjets30     : 1.947e-02
#--- BDTBoost                 : ----------------------------------------------
#--- MLPTanh                  : Ranking result (top variable is best ranked)
#--- MLPTanh                  : -------------------------------------
#--- MLPTanh                  : Rank : Variable     : Importance
#--- MLPTanh                  : -------------------------------------
#--- MLPTanh                  :    1 : M_bb_closest : 7.899e+01
#--- MLPTanh                  :    2 : bjet2Pt      : 4.600e+01
#--- MLPTanh                  :    3 : bjet1Pt      : 3.932e+01
#--- MLPTanh                  :    4 : jet2Pt       : 3.747e+01
#--- MLPTanh                  :    5 : Nbjets30     : 3.361e+01
#--- MLPTanh                  :    6 : M_blnu       : 2.890e+01
#--- MLPTanh                  :    7 : jet1Pt       : 2.731e+01
#--- MLPTanh                  :    8 : leptonPt     : 2.426e+01
#--- MLPTanh                  :    9 : M_jjb        : 2.326e+01
#--- MLPTanh                  :   10 : M_jjlnu      : 1.995e+01
#--- MLPTanh                  :   11 : MET          : 1.668e+01
#--- MLPTanh                  :   12 : DeltaR_j1l   : 1.330e+01
#--- MLPTanh                  :   13 : DeltaR_bb1   : 6.548e+00
#--- MLPTanh                  :   14 : DeltaR_jjl   : 5.670e+00
#--- MLPTanh                  :   15 : DeltaR_jjb   : 4.631e+00
#--- MLPTanh                  :   16 : DeltaR_j2l   : 3.463e+00
#--- MLPTanh                  :   17 : DeltaR_b2l   : 3.431e+00
#--- MLPTanh                  :   18 : DeltaR_b1l   : 1.537e-01
#--- MLPTanh                  : -------------------------------------
#--- MLPNodes                 : Ranking result (top variable is best ranked)
#--- MLPNodes                 : -------------------------------------
#--- MLPNodes                 : Rank : Variable     : Importance
#--- MLPNodes                 : -------------------------------------
#--- MLPNodes                 :    1 : Nbjets30     : 7.304e+01
#--- MLPNodes                 :    2 : M_bb_closest : 6.960e+01
#--- MLPNodes                 :    3 : bjet1Pt      : 6.776e+01
#--- MLPNodes                 :    4 : bjet2Pt      : 5.731e+01
#--- MLPNodes                 :    5 : jet1Pt       : 4.345e+01
#--- MLPNodes                 :    6 : jet2Pt       : 3.984e+01
#--- MLPNodes                 :    7 : M_blnu       : 3.776e+01
#--- MLPNodes                 :    8 : M_jjlnu      : 3.193e+01
#--- MLPNodes                 :    9 : M_jjb        : 3.100e+01
#--- MLPNodes                 :   10 : leptonPt     : 2.399e+01
#--- MLPNodes                 :   11 : MET          : 2.355e+01
#--- MLPNodes                 :   12 : DeltaR_j1l   : 2.125e+01
#--- MLPNodes                 :   13 : DeltaR_bb1   : 1.367e+01
#--- MLPNodes                 :   14 : DeltaR_j2l   : 5.576e+00
#--- MLPNodes                 :   15 : DeltaR_jjl   : 4.332e+00
#--- MLPNodes                 :   16 : DeltaR_b2l   : 4.040e+00
#--- MLPNodes                 :   17 : DeltaR_jjb   : 3.624e+00
#--- MLPNodes                 :   18 : DeltaR_b1l   : 1.328e-01
#--- MLPNodes                 : -------------------------------------
#--- MLPSigmoid               : Ranking result (top variable is best ranked)
#--- MLPSigmoid               : -------------------------------------
#--- MLPSigmoid               : Rank : Variable     : Importance
#--- MLPSigmoid               : -------------------------------------
#--- MLPSigmoid               :    1 : M_bb_closest : 7.583e+01
#--- MLPSigmoid               :    2 : bjet1Pt      : 6.390e+01
#--- MLPSigmoid               :    3 : M_blnu       : 4.270e+01
#--- MLPSigmoid               :    4 : Nbjets30     : 4.238e+01
#--- MLPSigmoid               :    5 : bjet2Pt      : 3.666e+01
#--- MLPSigmoid               :    6 : jet1Pt       : 3.395e+01
#--- MLPSigmoid               :    7 : jet2Pt       : 2.994e+01
#--- MLPSigmoid               :    8 : M_jjb        : 2.390e+01
#--- MLPSigmoid               :    9 : leptonPt     : 2.274e+01
#--- MLPSigmoid               :   10 : M_jjlnu      : 2.191e+01
#--- MLPSigmoid               :   11 : MET          : 1.830e+01
#--- MLPSigmoid               :   12 : DeltaR_j1l   : 1.641e+01
#--- MLPSigmoid               :   13 : DeltaR_bb1   : 1.254e+01
#--- MLPSigmoid               :   14 : DeltaR_b2l   : 5.473e+00
#--- MLPSigmoid               :   15 : DeltaR_jjl   : 4.492e+00
#--- MLPSigmoid               :   16 : DeltaR_jjb   : 3.828e+00
#--- MLPSigmoid               :   17 : DeltaR_j2l   : 2.635e+00
#--- MLPSigmoid               :   18 : DeltaR_b1l   : 1.671e-01
#--- MLPSigmoid               : -------------------------------------
