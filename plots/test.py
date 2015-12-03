import sys
import os
import ROOT
from ROOT import TFile, gDirectory, TChain, TMVA, TCut, TCanvas, THStack, TH1F

# file with trees
file_HH = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_all.root")
file_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_all.root")
treeS1 = file_HH.Get("stage_1/cleanup/cleanup")
treeB1 = file_tt.Get("stage_1/cleanup/cleanup")


class configuration(object):

    def __init__(self, name, varNames, stage):
        self.name = name
        self.varNames = [ ]
        self.treeS = None
        self.treeB = None
        self.hist_effs = [ ]
        self.stage = stage
#        self.significances
        if stage==1:
            self.treeS = treeS1
            self.treeB = treeB1
#        elif stage==2:
#            self.treeS = treeS2
#            self.treeB = treeB2
#        elif stage==3:
#            self.treeS = treeS3
#            self.treeB = treeB3
        # check existence of variables
        if self.treeS and self.treeB:
            listS = self.treeS.GetListOfBranches()
            listB = self.treeB.GetListOfBranches()
            for var in varNames:
                if var in listS and var in listB:
                    print ">>> "+self.name+": variable "+var+" added"
                    self.varNames.append(varNames)
                else:
                    sys.exit(">>> ERROR: "+self.name+": variables \""+var+"\" not in the tree!")


def main():
    
    allVars = [ "Njets20","Nbjets30",
                "jet1Pt","jet2Pt",
                "bjet1Pt","bjet2Pt",
                "Pt_bb","Pt_bl","Pt_j1l",
                "leptonPt","MET",
                "DeltaR_j1l","DeltaR_j2l",
                "DeltaR_b1l","DeltaR_b2l",
                "DeltaR_bb1","DeltaR_jj",
                "DeltaR_jjl","DeltaR_jjb",
                "DeltaPhi_lMET","DeltaPhi_jjlbb",
                "M_bb_closest", "M_jjlnu", # Higgs reconstruction
                "M_jjb", "M_blnu",         # top reconstruction
                "M_bl", "M_j1l",
                "MT_lnu","MT_jjlnu" ]

    betterVars = [  "Nbjets30",
                    "jet1Pt","jet2Pt",
                    "bjet1Pt","bjet2Pt",
                    "Pt_bb","Pt_bl","Pt_j1l",
                    "leptonPt","MET",
                    "DeltaR_j1l","DeltaR_j2l",
                    "DeltaR_b1l","DeltaR_b2l",
                    "DeltaR_bb1",
                    "DeltaPhi_jjlbb",
                    "DeltaR_jjl","DeltaR_jjb",
                    "M_bb_closest", "M_jjlnu",
                    "M_jjb", "M_bl",
                    "M_j1l" ]


    MLPTopVars = [  "Njets20",
                    "jet1Pt","jet2Pt",
                    "bjet1Pt","bjet2Pt",
                    "Pt_bb","Pt_bl","Pt_j1l",
                    "leptonPt","MET",
                    "DeltaR_j1l",
                    "M_jjlnu", "M_jjb",
                    "M_bl", "M_j1l" ]

    ANVars = [  "Njets20",
                "Pt_bb","Pt_bl","Pt_j1l",
                "leptonPt","MET",
                "DeltaR_j1l","DeltaR_b1l",
                "DeltaR_bb1","DeltaPhi_jjlbb",
                "M_bb_closest", "M_jjlnu", # Higgs reconstruction
                "M_jjb", "M_blnu",         # top reconstruction
                "M_bl", "M_j1l" ]

    favVars = [ "DeltaR_b1l", "DeltaR_b2l", "DeltaR_bb1",
                "DeltaR_j1l", "DeltaR_j2l", "DeltaR_jjl",
                "Pt_bb", "Pt_bl",
                "M_bb_closest", "M_jjlnu",
                "M_jjb", "M_bl", "M_j1l" ]

    badVars = [ "badvariable" ]

    configs = [ configuration("everything20", allVars, 1),
                configuration("better20",     betterVars, 1),
                configuration("MLPTop20", MLPTopVars, 1),
                configuration("AN20",     ANVars, 1),
                configuration("favs20",   favVars, 1),
                configuration("bad20",    badVars, 1)
               ]
    
    print "Done"


if __name__ == '__main__':
    main()


# strong correlations between:
#    M_bb vs. DeltaR_bb
#    M_bb vs. bjet1, bjet2 for background
#


#--- BDT                      : -----------------------------------------------
#--- BDT                      : Rank : Variable      : Variable Importance
#--- BDT                      : -----------------------------------------------
#--- BDT                      :    1 : M_bb_closest  : 6.179e-02
#--- BDT                      :    2 : DeltaR_j1l    : 6.056e-02
#--- BDT                      :    3 : jet1Pt        : 5.183e-02
#--- BDT                      :    4 : DeltaR_jjl    : 5.172e-02
#--- BDT                      :    5 : bjet1Pt       : 5.170e-02
#--- BDT                      :    6 : leptonPt      : 5.118e-02
#--- BDT                      :    7 : DeltaR_bb1    : 5.087e-02
#--- BDT                      :    8 : DeltaR_j2l    : 4.737e-02
#--- BDT                      :    9 : DeltaR_b2l    : 4.551e-02
#--- BDT                      :   10 : DeltaR_jjb    : 4.344e-02
#--- BDT                      :   11 : DeltaR_b1l    : 4.309e-02
#--- BDT                      :   12 : M_blnu        : 4.248e-02
#--- BDT                      :   13 : M_jjb         : 4.137e-02
#--- BDT                      :   14 : DeltaR_jj     : 4.097e-02
#--- BDT                      :   15 : MT_lnu        : 3.884e-02
#--- BDT                      :   16 : MT_jjlnu      : 3.857e-02
#--- BDT                      :   17 : M_jjlnu       : 3.852e-02
#--- BDT                      :   18 : DeltaPhi_lMET : 3.710e-02
#--- BDT                      :   19 : MET           : 3.566e-02
#--- BDT                      :   20 : bjet2Pt       : 3.477e-02
#--- BDT                      :   21 : jet2Pt        : 3.458e-02
#--- BDT                      :   22 : Njets20       : 3.006e-02
#--- BDT                      :   23 : Nbjets30      : 2.803e-02
#--- BDT                      : -----------------------------------------------
#--- BDTTuned                 : Ranking result (top variable is best ranked)
#--- BDTTuned                 : -----------------------------------------------
#--- BDTTuned                 : Rank : Variable      : Variable Importance
#--- BDTTuned                 : -----------------------------------------------
#--- BDTTuned                 :    1 : DeltaR_j1l    : 5.944e-02
#--- BDTTuned                 :    2 : M_bb_closest  : 5.577e-02
#--- BDTTuned                 :    3 : DeltaR_jjl    : 5.213e-02
#--- BDTTuned                 :    4 : bjet1Pt       : 5.113e-02
#--- BDTTuned                 :    5 : jet1Pt        : 4.970e-02
#--- BDTTuned                 :    6 : DeltaR_bb1    : 4.853e-02
#--- BDTTuned                 :    7 : leptonPt      : 4.721e-02
#--- BDTTuned                 :    8 : M_blnu        : 4.487e-02
#--- BDTTuned                 :    9 : DeltaR_b2l    : 4.477e-02
#--- BDTTuned                 :   10 : DeltaR_jj     : 4.475e-02
#--- BDTTuned                 :   11 : DeltaR_j2l    : 4.425e-02
#--- BDTTuned                 :   12 : DeltaR_jjb    : 4.407e-02
#--- BDTTuned                 :   13 : DeltaR_b1l    : 4.325e-02
#--- BDTTuned                 :   14 : M_jjb         : 4.267e-02
#--- BDTTuned                 :   15 : MT_lnu        : 4.251e-02
#--- BDTTuned                 :   16 : MT_jjlnu      : 3.944e-02
#--- BDTTuned                 :   17 : DeltaPhi_lMET : 3.872e-02
#--- BDTTuned                 :   18 : MET           : 3.827e-02
#--- BDTTuned                 :   19 : bjet2Pt       : 3.771e-02
#--- BDTTuned                 :   20 : M_jjlnu       : 3.715e-02
#--- BDTTuned                 :   21 : jet2Pt        : 3.681e-02
#--- BDTTuned                 :   22 : Njets20       : 2.971e-02
#--- BDTTuned                 :   23 : Nbjets30      : 2.714e-02
#--- BDTTuned                 : -----------------------------------------------
#--- BDTMaxDepth              : Ranking result (top variable is best ranked)
#--- BDTMaxDepth              : -----------------------------------------------
#--- BDTMaxDepth              : Rank : Variable      : Variable Importance
#--- BDTMaxDepth              : -----------------------------------------------
#--- BDTMaxDepth              :    1 : DeltaR_j1l    : 5.344e-02
#--- BDTMaxDepth              :    2 : M_bb_closest  : 5.219e-02
#--- BDTMaxDepth              :    3 : DeltaR_jjl    : 5.100e-02
#--- BDTMaxDepth              :    4 : DeltaR_bb1    : 5.070e-02
#--- BDTMaxDepth              :    5 : DeltaR_jj     : 4.885e-02
#--- BDTMaxDepth              :    6 : bjet1Pt       : 4.859e-02
#--- BDTMaxDepth              :    7 : DeltaR_b2l    : 4.832e-02
#--- BDTMaxDepth              :    8 : leptonPt      : 4.683e-02
#--- BDTMaxDepth              :    9 : DeltaR_jjb    : 4.578e-02
#--- BDTMaxDepth              :   10 : DeltaR_b1l    : 4.503e-02
#--- BDTMaxDepth              :   11 : DeltaPhi_lMET : 4.499e-02
#--- BDTMaxDepth              :   12 : DeltaR_j2l    : 4.463e-02
#--- BDTMaxDepth              :   13 : jet1Pt        : 4.392e-02
#--- BDTMaxDepth              :   14 : MET           : 4.288e-02
#--- BDTMaxDepth              :   15 : MT_lnu        : 4.200e-02
#--- BDTMaxDepth              :   16 : bjet2Pt       : 4.189e-02
#--- BDTMaxDepth              :   17 : MT_jjlnu      : 4.140e-02
#--- BDTMaxDepth              :   18 : M_jjb         : 4.052e-02
#--- BDTMaxDepth              :   19 : M_blnu        : 4.001e-02
#--- BDTMaxDepth              :   20 : M_jjlnu       : 3.855e-02
#--- BDTMaxDepth              :   21 : jet2Pt        : 3.738e-02
#--- BDTMaxDepth              :   22 : Njets20       : 3.063e-02
#--- BDTMaxDepth              :   23 : Nbjets30      : 2.050e-02
#--- BDTMaxDepth              : -----------------------------------------------
#--- BDTCuts                  : Ranking result (top variable is best ranked)
#--- BDTCuts                  : -----------------------------------------------
#--- BDTCuts                  : Rank : Variable      : Variable Importance
#--- BDTCuts                  : -----------------------------------------------
#--- BDTCuts                  :    1 : bjet1Pt       : 5.828e-02
#--- BDTCuts                  :    2 : M_bb_closest  : 5.681e-02
#--- BDTCuts                  :    3 : leptonPt      : 5.414e-02
#--- BDTCuts                  :    4 : DeltaR_j1l    : 5.131e-02
#--- BDTCuts                  :    5 : DeltaR_b1l    : 4.944e-02
#--- BDTCuts                  :    6 : DeltaR_jjl    : 4.917e-02
#--- BDTCuts                  :    7 : jet1Pt        : 4.853e-02
#--- BDTCuts                  :    8 : DeltaR_bb1    : 4.770e-02
#--- BDTCuts                  :    9 : DeltaR_b2l    : 4.598e-02
#--- BDTCuts                  :   10 : DeltaR_j2l    : 4.521e-02
#--- BDTCuts                  :   11 : MT_jjlnu      : 4.320e-02
#--- BDTCuts                  :   12 : DeltaR_jjb    : 4.208e-02
#--- BDTCuts                  :   13 : M_jjb         : 4.160e-02
#--- BDTCuts                  :   14 : jet2Pt        : 4.160e-02
#--- BDTCuts                  :   15 : M_blnu        : 4.119e-02
#--- BDTCuts                  :   16 : M_jjlnu       : 4.050e-02
#--- BDTCuts                  :   17 : DeltaR_jj     : 4.023e-02
#--- BDTCuts                  :   18 : MET           : 3.976e-02
#--- BDTCuts                  :   19 : MT_lnu        : 3.808e-02
#--- BDTCuts                  :   20 : bjet2Pt       : 3.742e-02
#--- BDTCuts                  :   21 : DeltaPhi_lMET : 3.720e-02
#--- BDTCuts                  :   22 : Nbjets30      : 2.549e-02
#--- BDTCuts                  :   23 : Njets20       : 2.507e-02
#--- BDTCuts                  : -----------------------------------------------
#--- BDTBoost                 : Ranking result (top variable is best ranked)
#--- BDTBoost                 : -----------------------------------------------
#--- BDTBoost                 : Rank : Variable      : Variable Importance
#--- BDTBoost                 : -----------------------------------------------
#--- BDTBoost                 :    1 : DeltaR_j1l    : 7.212e-02
#--- BDTBoost                 :    2 : bjet1Pt       : 6.457e-02
#--- BDTBoost                 :    3 : M_bb_closest  : 6.368e-02
#--- BDTBoost                 :    4 : leptonPt      : 5.486e-02
#--- BDTBoost                 :    5 : DeltaR_jjl    : 5.285e-02
#--- BDTBoost                 :    6 : DeltaR_b2l    : 4.906e-02
#--- BDTBoost                 :    7 : DeltaR_bb1    : 4.892e-02
#--- BDTBoost                 :    8 : jet1Pt        : 4.864e-02
#--- BDTBoost                 :    9 : DeltaR_j2l    : 4.514e-02
#--- BDTBoost                 :   10 : M_blnu        : 4.470e-02
#--- BDTBoost                 :   11 : DeltaR_b1l    : 4.396e-02
#--- BDTBoost                 :   12 : DeltaR_jjb    : 3.903e-02
#--- BDTBoost                 :   13 : M_jjb         : 3.784e-02
#--- BDTBoost                 :   14 : DeltaR_jj     : 3.783e-02
#--- BDTBoost                 :   15 : MT_lnu        : 3.738e-02
#--- BDTBoost                 :   16 : jet2Pt        : 3.482e-02
#--- BDTBoost                 :   17 : M_jjlnu       : 3.438e-02
#--- BDTBoost                 :   18 : bjet2Pt       : 3.433e-02
#--- BDTBoost                 :   19 : Nbjets30      : 3.291e-02
#--- BDTBoost                 :   20 : MT_jjlnu      : 3.196e-02
#--- BDTBoost                 :   21 : Njets20       : 3.131e-02
#--- BDTBoost                 :   22 : DeltaPhi_lMET : 3.006e-02
#--- BDTBoost                 :   23 : MET           : 2.964e-02
#--- BDTBoost                 : -----------------------------------------------
#--- BDTNodeSize              : Ranking result (top variable is best ranked)
#--- BDTNodeSize              : -----------------------------------------------
#--- BDTNodeSize              : Rank : Variable      : Variable Importance
#--- BDTNodeSize              : -----------------------------------------------
#--- BDTNodeSize              :    1 : DeltaR_j1l    : 7.197e-02
#--- BDTNodeSize              :    2 : bjet1Pt       : 6.799e-02
#--- BDTNodeSize              :    3 : DeltaR_jjl    : 6.078e-02
#--- BDTNodeSize              :    4 : M_bb_closest  : 5.858e-02
#--- BDTNodeSize              :    5 : DeltaR_bb1    : 5.723e-02
#--- BDTNodeSize              :    6 : leptonPt      : 5.440e-02
#--- BDTNodeSize              :    7 : M_jjb         : 4.899e-02
#--- BDTNodeSize              :    8 : jet1Pt        : 4.833e-02
#--- BDTNodeSize              :    9 : DeltaR_b2l    : 4.760e-02
#--- BDTNodeSize              :   10 : DeltaR_b1l    : 4.270e-02
#--- BDTNodeSize              :   11 : M_blnu        : 4.084e-02
#--- BDTNodeSize              :   12 : DeltaR_j2l    : 3.904e-02
#--- BDTNodeSize              :   13 : bjet2Pt       : 3.778e-02
#--- BDTNodeSize              :   14 : DeltaR_jjb    : 3.746e-02
#--- BDTNodeSize              :   15 : Nbjets30      : 3.515e-02
#--- BDTNodeSize              :   16 : MT_lnu        : 3.432e-02
#--- BDTNodeSize              :   17 : MET           : 3.267e-02
#--- BDTNodeSize              :   18 : DeltaR_jj     : 3.228e-02
#--- BDTNodeSize              :   19 : MT_jjlnu      : 3.225e-02
#--- BDTNodeSize              :   20 : jet2Pt        : 3.173e-02
#--- BDTNodeSize              :   21 : M_jjlnu       : 3.124e-02
#--- BDTNodeSize              :   22 : DeltaPhi_lMET : 3.081e-02
#--- BDTNodeSize              :   23 : Njets20       : 2.586e-02
#--- BDTNodeSize              : -----------------------------------------------
#--- MLPTanh                  : Ranking result (top variable is best ranked)
#--- MLPTanh                  : --------------------------------------
#--- MLPTanh                  : Rank : Variable      : Importance
#--- MLPTanh                  : --------------------------------------
#--- MLPTanh                  :    1 : M_blnu        : 4.103e+01
#--- MLPTanh                  :    2 : bjet1Pt       : 4.070e+01
#--- MLPTanh                  :    3 : jet2Pt        : 3.806e+01
#--- MLPTanh                  :    4 : leptonPt      : 3.381e+01
#--- MLPTanh                  :    5 : jet1Pt        : 3.366e+01
#--- MLPTanh                  :    6 : Nbjets30      : 3.289e+01
#--- MLPTanh                  :    7 : M_jjlnu       : 3.052e+01
#--- MLPTanh                  :    8 : M_jjb         : 2.736e+01
#--- MLPTanh                  :    9 : DeltaR_j1l    : 2.292e+01
#--- MLPTanh                  :   10 : MT_jjlnu      : 2.213e+01
#--- MLPTanh                  :   11 : MT_lnu        : 2.158e+01
#--- MLPTanh                  :   12 : MET           : 2.139e+01
#--- MLPTanh                  :   13 : bjet2Pt       : 1.750e+01
#--- MLPTanh                  :   14 : Njets20       : 1.180e+01
#--- MLPTanh                  :   15 : M_bb_closest  : 1.043e+01
#--- MLPTanh                  :   16 : DeltaR_jjl    : 6.199e+00
#--- MLPTanh                  :   17 : DeltaR_bb1    : 6.108e+00
#--- MLPTanh                  :   18 : DeltaPhi_lMET : 5.939e+00
#--- MLPTanh                  :   19 : DeltaR_j2l    : 4.815e+00
#--- MLPTanh                  :   20 : DeltaR_jj     : 4.761e+00
#--- MLPTanh                  :   21 : DeltaR_b2l    : 4.093e+00
#--- MLPTanh                  :   22 : DeltaR_jjb    : 3.134e+00
#--- MLPTanh                  :   23 : DeltaR_b1l    : 2.048e+00
#--- MLPTanh                  : --------------------------------------
#--- MLPLearningRate          : Ranking result (top variable is best ranked)
#--- MLPLearningRate          : --------------------------------------
#--- MLPLearningRate          : Rank : Variable      : Importance
#--- MLPLearningRate          : --------------------------------------
#--- MLPLearningRate          :    1 : Njets20       : -nan
#--- MLPLearningRate          :    2 : Nbjets30      : -nan
#--- MLPLearningRate          :    3 : jet1Pt        : -nan
#--- MLPLearningRate          :    4 : jet2Pt        : -nan
#--- MLPLearningRate          :    5 : bjet1Pt       : -nan
#--- MLPLearningRate          :    6 : bjet2Pt       : -nan
#--- MLPLearningRate          :    7 : leptonPt      : -nan
#--- MLPLearningRate          :    8 : MET           : -nan
#--- MLPLearningRate          :    9 : DeltaR_j1l    : -nan
#--- MLPLearningRate          :   10 : DeltaR_j2l    : -nan
#--- MLPLearningRate          :   11 : DeltaR_b1l    : -nan
#--- MLPLearningRate          :   12 : DeltaR_b2l    : -nan
#--- MLPLearningRate          :   13 : DeltaR_bb1    : -nan
#--- MLPLearningRate          :   14 : DeltaR_jj     : -nan
#--- MLPLearningRate          :   15 : DeltaR_jjl    : -nan
#--- MLPLearningRate          :   16 : DeltaR_jjb    : -nan
#--- MLPLearningRate          :   17 : DeltaPhi_lMET : -nan
#--- MLPLearningRate          :   18 : M_bb_closest  : -nan
#--- MLPLearningRate          :   19 : M_jjlnu       : -nan
#--- MLPLearningRate          :   20 : M_jjb         : -nan
#--- MLPLearningRate          :   21 : M_blnu        : -nan
#--- MLPLearningRate          :   22 : MT_lnu        : -nan
#--- MLPLearningRate          :   23 : MT_jjlnu      : -nan
#--- MLPLearningRate          : --------------------------------------
#--- MLPNodes                 : Ranking result (top variable is best ranked)
#--- MLPNodes                 : --------------------------------------
#--- MLPNodes                 : Rank : Variable      : Importance
#--- MLPNodes                 : --------------------------------------
#--- MLPNodes                 :    1 : M_jjb         : 4.189e+01
#--- MLPNodes                 :    2 : Nbjets30      : 4.154e+01
#--- MLPNodes                 :    3 : M_jjlnu       : 4.052e+01
#--- MLPNodes                 :    4 : jet2Pt        : 3.888e+01
#--- MLPNodes                 :    5 : leptonPt      : 3.493e+01
#--- MLPNodes                 :    6 : M_blnu        : 3.431e+01
#--- MLPNodes                 :    7 : bjet1Pt       : 3.308e+01
#--- MLPNodes                 :    8 : jet1Pt        : 2.927e+01
#--- MLPNodes                 :    9 : MET           : 2.549e+01
#--- MLPNodes                 :   10 : MT_jjlnu      : 2.529e+01
#--- MLPNodes                 :   11 : bjet2Pt       : 2.402e+01
#--- MLPNodes                 :   12 : MT_lnu        : 2.299e+01
#--- MLPNodes                 :   13 : DeltaR_j1l    : 1.564e+01
#--- MLPNodes                 :   14 : Njets20       : 1.526e+01
#--- MLPNodes                 :   15 : M_bb_closest  : 1.187e+01
#--- MLPNodes                 :   16 : DeltaPhi_lMET : 7.993e+00
#--- MLPNodes                 :   17 : DeltaR_bb1    : 7.825e+00
#--- MLPNodes                 :   18 : DeltaR_j2l    : 7.751e+00
#--- MLPNodes                 :   19 : DeltaR_jjl    : 7.709e+00
#--- MLPNodes                 :   20 : DeltaR_jj     : 5.440e+00
#--- MLPNodes                 :   21 : DeltaR_b2l    : 3.462e+00
#--- MLPNodes                 :   22 : DeltaR_jjb    : 3.427e+00
#--- MLPNodes                 :   23 : DeltaR_b1l    : 1.783e+00
#--- MLPNodes                 : --------------------------------------
#--- MLPSigmoid               : Ranking result (top variable is best ranked)
#--- MLPSigmoid               : --------------------------------------
#--- MLPSigmoid               : Rank : Variable      : Importance
#--- MLPSigmoid               : --------------------------------------
#--- MLPSigmoid               :    1 : Nbjets30      : 4.929e+01
#--- MLPSigmoid               :    2 : leptonPt      : 4.123e+01
#--- MLPSigmoid               :    3 : jet2Pt        : 3.833e+01
#--- MLPSigmoid               :    4 : bjet1Pt       : 3.743e+01
#--- MLPSigmoid               :    5 : M_blnu        : 3.633e+01
#--- MLPSigmoid               :    6 : jet1Pt        : 3.188e+01
#--- MLPSigmoid               :    7 : M_jjlnu       : 2.955e+01
#--- MLPSigmoid               :    8 : M_jjb         : 2.893e+01
#--- MLPSigmoid               :    9 : DeltaR_j1l    : 2.398e+01
#--- MLPSigmoid               :   10 : MT_jjlnu      : 2.240e+01
#--- MLPSigmoid               :   11 : MT_lnu        : 2.088e+01
#--- MLPSigmoid               :   12 : MET           : 1.834e+01
#--- MLPSigmoid               :   13 : bjet2Pt       : 1.609e+01
#--- MLPSigmoid               :   14 : M_bb_closest  : 1.548e+01
#--- MLPSigmoid               :   15 : Njets20       : 1.134e+01
#--- MLPSigmoid               :   16 : DeltaR_bb1    : 9.760e+00
#--- MLPSigmoid               :   17 : DeltaR_j2l    : 7.457e+00
#--- MLPSigmoid               :   18 : DeltaR_jjl    : 6.064e+00
#--- MLPSigmoid               :   19 : DeltaPhi_lMET : 4.941e+00
#--- MLPSigmoid               :   20 : DeltaR_b2l    : 4.293e+00
#--- MLPSigmoid               :   21 : DeltaR_jj     : 3.791e+00
#--- MLPSigmoid               :   22 : DeltaR_jjb    : 3.175e+00
#--- MLPSigmoid               :   23 : DeltaR_b1l    : 1.933e+00
#--- MLPSigmoid               : --------------------------------------


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
