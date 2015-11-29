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
# MLP parameters to tune: number of neurons on each hidden layer, learning rate, activation function
# BDT parameters to tune: number of cycles, tree depth, ...
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
methods = [ ("BDT","BDT"), ("BDT","BDTTuned"), ("MLP","MLPTuned"), ("MLP","MLPTunedSigmoid") ] #("LD","LD"), , ("MLP","MLP")

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

#    # LD: Linear Classifier
#    factory.BookMethod(TMVA.Types.kLD, "LD", "H:!V")

    # BDT: Boosted Decision Tree
    factory.BookMethod(TMVA.Types.kBDT, "BDT", "!H:!V" )

    # BDTTuned
    factory.BookMethod(TMVA.Types.kBDT, "BDTTuned",
                       ":".join([ "!H","!V",
                                  "NTrees=1500", # ~ number of boost steps, too large mainly costs time
#                                  "nEventsMin=200",
                                  "MaxDepth=3", #  ~ 2-5 maximum tree depth (depends on the interaction of variables
                                  "BoostType=AdaBoost",
                                  "AdaBoostBeta=0.2", # ~ 0.01-0.5
                                  "SeparationType=GiniIndex",
                                  "nCuts=20" ]) )

#    # MLP: Neutal Network
#    factory.BookMethod( TMVA.Types.kMLP, "MLP", "H:!V:" )

    # MLPTuned
    factory.BookMethod( TMVA.Types.kMLP, "MLPTuned",
                        ":".join([ "!H","!V",
#                                   "N:TestRate=5",
#                                   "NCycles=200",
                                   "NeuronType=tanh",
                                   "VarTransform=N", # normalise variables
                                   "HiddenLayers=N+5", # number of nodes in NN layers
                                   "UseRegulator" ]) ) # L2 norm regulator to avoid overtraining
    # MLPTuned
    factory.BookMethod( TMVA.Types.kMLP, "MLPTunedSigmoid",
                        ":".join([ "!H","!V",
#                                   "N:TestRate=5",
#                                   "NCycles=200",
                                   "NeuronType=sigmoid",
                                   "VarTransform=N", # normalise variables
                                   "HiddenLayers=N+5", # number of nodes in NN layers
                                   "UseRegulator" ]) ) # L2 norm regulator to avoid overtraining

 
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
    f_out.Close()

    weightsdir = "weights/"+config.name
    if not os.path.exists(weightsdir):
        os.makedirs(weightsdir)
    for Method, method in methods:
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
        S = N_S * histS.Integral(i,N)/ S_tot
        B = N_B * histB.Integral(i,N) /B_tot
        P = S / sqrt(1+B)
        if Pmax<P:
            Pmax = P
            Smax = S
            Bmax = B
            imax = i

    return [Pmax,Smax,Bmax,histS.GetXaxis().GetBinCenter(imax)]



# SIGNIFICANCE
def significanceBins(histS,histB):
    
    P2 = 0

    # calculate significance per bin and add using: sigma^2 = sum(sigma_i^2)
    N = histS.GetNbinsX()
    for i in range(1,N):
        S = N_S * histS.GetBinContent(i) / S_tot
        B = N_B * histB.GetBinContent(i) / B_tot
        P2 += S*S/(1+B)

    return sqrt(P2)



# HISTOGRAMS: TMVA output
def plot(config):
    print "\n>>> examine training with configuration "+config.name

    reader = TMVA.Reader()
    f = TFile("HH_MVA_"+config.name+".root")
    TestTree = gDirectory.Get("TestTree")

    vars = [ ]
    for name in config.varNames:
        vars.append(array('f',[0]))
        reader.AddVariable(name,vars[-1])

    significances = [ ]
    for Method, method in methods:
        reader.BookMVA(method,"weights/"+config.name+"/TMVAClassification_"+method+".weights.xml")

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
                              ": %.4f significance, yields S = %.1f, B = %.1f with a cut at %.4f" % \
                              (Pmax,Smax,Bmax,cut) + \
                              "\n: %.4f significance with bins" % Pbins  )

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

    for s in significances:
        print s



# HISTOGRAMS: compare all methods and variable configurations
def compare(configs,stage=""):
    print "\n>>> compare all methods with all variable configurations"
    
    hist_effs = [ ]
    for config in configs:
        hist_effs.extend(config.hist_effs)
    
    if not hist_effs:
        return
    
    c = makeCanvas()
    hist_effs[0].Draw()
    hist_effs[0].SetLineWidth(1.2)
    hist_effs[0].SetStats(0)
    makeAxes(hist_effs[0],xlabel="signal efficiency",ylabel="background rejection")
    if len(hist_effs)>1:
        for hist in hist_effs[1:]:
            hist.Draw("same")
            hist.SetLineWidth(1.2)
    labels = [ ]
    for config in configs:
        labels.extend([config.name+", "+method[1] for method in methods])
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
    f = TFile("HH_MVA_"+config.name+".root")
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
    
    varNames = [ "Njets20","Nbjets30",
                 "jet1Pt","jet2Pt",
                 "bjet1Pt","bjet2Pt",
                 "leptonPt","MET",
                 "DeltaR_j1l","DeltaR_j2l",
                 "DeltaR_b1l","DeltaR_b2l",
                 "DeltaR_bb1","DeltaR_jj",
                 "DeltaR_jjl","DeltaR_jjb",
                 "DeltaPhi_lMET",
                 "M_bb_closest", "M_jjlnu",
                 "M_jjb", "M_blnu",
                 "MT_lnu","MT_jjlnu" ]
                 
    varNamesBest = [ "jet1Pt","jet2Pt",
                     "bjet1Pt","bjet2Pt",
                     "leptonPt","MET",
                     "DeltaR_b1l", "DeltaR_b2l", "DeltaR_bb1",
                     "DeltaR_j1l", "DeltaR_j2l",
                     "M_bb_closest", "M_jjlnu",
                     "M_jjb", "M_blnu" ]
                 
#    varNamesMLPTop5 = [ "bjet1Pt", "bjet2Pt",
#                        "DeltaR_j2l", "DeltaR_b2l",
#                        "M_bb_closest" ]

    varNamesFavs = [ "DeltaR_b1l", "DeltaR_b2l", "DeltaR_bb1",
                     "DeltaR_j1l", "DeltaR_j2l",
                     "M_bb_closest", "M_jjlnu",
                     "M_jjb", "M_blnu" ]

    if opts.test:
        configs = [configuration("test", ["bjet1Pt","jet1Pt"], 1)]
    else:
        configs = [
#                    configuration("everything20", varNames, 1),
#                    configuration("best20",    varNamesBest, 1),
#                    configuration("MLPTop520", varNamesMLPTop5, 1),
#                    configuration("favs20",    varNamesFavs, 1),
                    configuration("everythingCleanUp", varNames, 2),
                    configuration("favsCleanUp",    varNamesFavs, 2),]
#                    configuration("everything30", varNames, 3),
#                    configuration("favs30", varNamesFavs, 3),]

    if opts.onlyPlot:
        for config in configs:
            plot(config)
    else:
        for config in configs:
            train(config)
            plot(config)
    compare(configs,"stage_12")
    compare(configs[:len(configs)/2],"stage_1")
    compare(configs[len(configs)/2:],"stage_2")

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
#--- BDT                      : -----------------------------------------------
#--- BDT                      : Rank : Variable      : Variable Importance
#--- BDT                      : -----------------------------------------------
#--- BDT                      :    1 : jet1Pt        : 9.931e-02
#--- BDT                      :    2 : DeltaPhi_lMET : 9.459e-02
#--- BDT                      :    3 : DeltaR_b1l    : 9.376e-02
#--- BDT                      :    4 : MT_lnu        : 9.331e-02
#--- BDT                      :    5 : leptonPt      : 8.634e-02
#--- BDT                      :    6 : DeltaR_b2l    : 7.308e-02
#--- BDT                      :    7 : DeltaR_j1l    : 7.037e-02
#--- BDT                      :    8 : DeltaR_j2l    : 6.931e-02
#--- BDT                      :    9 : M_bb_closest  : 6.519e-02
#--- BDT                      :   10 : DeltaR_bb1    : 6.223e-02
#--- BDT                      :   11 : bjet2Pt       : 5.419e-02
#--- BDT                      :   12 : bjet1Pt       : 5.396e-02
#--- BDT                      :   13 : MET           : 4.431e-02
#--- BDT                      :   14 : jet2Pt        : 4.006e-02
#--- BDT                      : -----------------------------------------------
#--- BDTTuned                 : Ranking result (top variable is best ranked)
#--- BDTTuned                 : -----------------------------------------------
#--- BDTTuned                 : Rank : Variable      : Variable Importance
#--- BDTTuned                 : -----------------------------------------------
#--- BDTTuned                 :    1 : DeltaR_b1l    : 8.847e-02
#--- BDTTuned                 :    2 : DeltaR_j1l    : 7.976e-02
#--- BDTTuned                 :    3 : DeltaR_bb1    : 7.546e-02
#--- BDTTuned                 :    4 : DeltaR_j2l    : 7.392e-02
#--- BDTTuned                 :    5 : DeltaPhi_lMET : 7.371e-02
#--- BDTTuned                 :    6 : leptonPt      : 7.350e-02
#--- BDTTuned                 :    7 : MT_lnu        : 7.105e-02
#--- BDTTuned                 :    8 : bjet1Pt       : 7.099e-02
#--- BDTTuned                 :    9 : bjet2Pt       : 6.887e-02
#--- BDTTuned                 :   10 : MET           : 6.884e-02
#--- BDTTuned                 :   11 : jet1Pt        : 6.694e-02
#--- BDTTuned                 :   12 : M_bb_closest  : 6.601e-02
#--- BDTTuned                 :   13 : jet2Pt        : 6.420e-02
#--- BDTTuned                 :   14 : DeltaR_b2l    : 5.829e-02
#--- BDTTuned                 : -----------------------------------------------
#--- MLPTuned                 : Ranking result (top variable is best ranked)
#--- MLPTuned                 : --------------------------------------
#--- MLPTuned                 : Rank : Variable      : Importance
#--- MLPTuned                 : --------------------------------------
#--- MLPTuned                 :    1 : M_bb_closest  : 6.879e+01
#--- MLPTuned                 :    2 : DeltaR_j2l    : 6.287e+01
#--- MLPTuned                 :    3 : bjet1Pt       : 6.040e+01
#--- MLPTuned                 :    4 : DeltaR_b2l    : 4.892e+01
#--- MLPTuned                 :    5 : bjet2Pt       : 3.951e+01
#--- MLPTuned                 :    6 : jet2Pt        : 2.673e+01
#--- MLPTuned                 :    7 : jet1Pt        : 2.546e+01
#--- MLPTuned                 :    8 : DeltaR_j1l    : 1.711e+01
#--- MLPTuned                 :    9 : leptonPt      : 1.664e+01
#--- MLPTuned                 :   10 : MET           : 1.515e+01
#--- MLPTuned                 :   11 : MT_lnu        : 1.217e+01
#--- MLPTuned                 :   12 : DeltaR_bb1    : 5.648e+00
#--- MLPTuned                 :   13 : DeltaR_b1l    : 2.099e+00
#--- MLPTuned                 :   14 : DeltaPhi_lMET : 5.774e-01
#--- MLPTuned                 : --------------------------------------


#--- Factory                  : Ranking input variables (method specific)...
#--- BDT                      : Ranking result (top variable is best ranked)
#--- BDT                      : -----------------------------------------------
#--- BDT                      : Rank : Variable      : Variable Importance
#--- BDT                      : -----------------------------------------------
#--- BDT                      :    1 : DeltaR_b2l    : 1.058e-01
#--- BDT                      :    2 : jet1Pt        : 9.148e-02
#--- BDT                      :    3 : DeltaR_b1l    : 8.879e-02
#--- BDT                      :    4 : DeltaR_j1l    : 7.546e-02
#--- BDT                      :    5 : DeltaR_bb1    : 7.469e-02
#--- BDT                      :    6 : bjet2Pt       : 7.450e-02
#--- BDT                      :    7 : MET           : 7.430e-02
#--- BDT                      :    8 : leptonPt      : 7.217e-02
#--- BDT                      :    9 : MT_lnu        : 6.578e-02
#--- BDT                      :   10 : bjet1Pt       : 6.328e-02
#--- BDT                      :   11 : DeltaR_j2l    : 5.946e-02
#--- BDT                      :   12 : M_bb_closest  : 5.882e-02
#--- BDT                      :   13 : jet2Pt        : 4.845e-02
#--- BDT                      :   14 : DeltaPhi_lMET : 4.703e-02
#--- BDT                      : -----------------------------------------------
#--- BDTTuned                 : Ranking result (top variable is best ranked)
#--- BDTTuned                 : -----------------------------------------------
#--- BDTTuned                 : Rank : Variable      : Variable Importance
#--- BDTTuned                 : -----------------------------------------------
#--- BDTTuned                 :    1 : DeltaR_b1l    : 8.571e-02
#--- BDTTuned                 :    2 : DeltaR_j1l    : 8.140e-02
#--- BDTTuned                 :    3 : DeltaR_j2l    : 7.829e-02
#--- BDTTuned                 :    4 : DeltaR_bb1    : 7.710e-02
#--- BDTTuned                 :    5 : bjet2Pt       : 7.440e-02
#--- BDTTuned                 :    6 : DeltaPhi_lMET : 7.394e-02
#--- BDTTuned                 :    7 : leptonPt      : 7.200e-02
#--- BDTTuned                 :    8 : jet1Pt        : 7.158e-02
#--- BDTTuned                 :    9 : MT_lnu        : 7.104e-02
#--- BDTTuned                 :   10 : MET           : 7.063e-02
#--- BDTTuned                 :   11 : bjet1Pt       : 6.799e-02
#--- BDTTuned                 :   12 : jet2Pt        : 6.282e-02
#--- BDTTuned                 :   13 : M_bb_closest  : 6.163e-02
#--- BDTTuned                 :   14 : DeltaR_b2l    : 5.145e-02
#--- BDTTuned                 : -----------------------------------------------
#--- MLPTuned                 : Ranking result (top variable is best ranked)
#--- MLPTuned                 : --------------------------------------
#--- MLPTuned                 : Rank : Variable      : Importance
#--- MLPTuned                 : --------------------------------------
#--- MLPTuned                 :    1 : bjet1Pt       : 5.738e+01
#--- MLPTuned                 :    2 : DeltaR_j2l    : 5.223e+01
#--- MLPTuned                 :    3 : M_bb_closest  : 4.327e+01
#--- MLPTuned                 :    4 : DeltaR_b2l    : 4.132e+01
#--- MLPTuned                 :    5 : bjet2Pt       : 3.307e+01
#--- MLPTuned                 :    6 : jet2Pt        : 2.016e+01
#--- MLPTuned                 :    7 : leptonPt      : 1.932e+01
#--- MLPTuned                 :    8 : jet1Pt        : 1.851e+01
#--- MLPTuned                 :    9 : DeltaR_j1l    : 1.681e+01
#--- MLPTuned                 :   10 : MET           : 1.385e+01
#--- MLPTuned                 :   11 : MT_lnu        : 1.102e+01
#--- MLPTuned                 :   12 : DeltaR_bb1    : 4.222e+00
#--- MLPTuned                 :   13 : DeltaR_b1l    : 2.222e+00
#--- MLPTuned                 :   14 : DeltaPhi_lMET : 7.937e-01
#--- MLPTuned                 : --------------------------------------
