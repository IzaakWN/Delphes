import sys
import os
import ROOT
from ROOT import TFile, gDirectory, TChain, TMVA, TCut, TCanvas, THStack, TH1F

# file with trees
#file_HH = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_all.root")
#file_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_all.root")
file_HH = TFile("../controlPlots_HH_all.root")
file_tt = TFile("../controlPlots_tt_all.root")

treeS1 = file_HH.Get("stage_1/cleanup/cleanup")
treeB1 = file_tt.Get("stage_1/cleanup/cleanup")

h0_S = file_HH.Get("stage_0/selection/category") # ~ 166483
h0_B = file_tt.Get("stage_0/selection/category") # ~ 164661
S1 = h0_S.GetBinContent(2)
B1 = h0_B.GetBinContent(2)
print "treeS1.GetEntries()=%i" % treeS1.GetEntries()
print "S1=%i" % S1
print "treeB1.GetEntries()=%i" % treeB1.GetEntries()
print "B1=%i" % B1


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
