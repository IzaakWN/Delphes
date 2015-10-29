from __future__ import division
from ROOT import *
from math import sqrt
import time

file = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_all.root")
file_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_all.root")

# intgrated luminosity
L = 3000.0 # / fb

sigma_S = 40 * 0.0715
sigma_B = 984500 * 0.2873

N_S = sigma_S * L
N_B = sigma_B * L

hist_S = file.Get("stage_0/selection/category") # signal: HH -> bbWW
hist_B = file_tt.Get("stage_0/selection/category") # BG: tt -> bbWW

S_tot = hist_S.GetBinContent(1)
B_tot = hist_B.GetBinContent(1)


    ######################
    # Punzi significance #
    ######################

def punzi(stage):

    print "\n   " + stage[:-1] + \
          " Punzi significance" + \
          "\n  ---------------------------------------" + \
          "\n   P     \tS \tB\t Mass reco" + \
          "\n  ---------------------------------------"
    
    for obj in [ "jj","jj_cut","jj_leading","jj_leading_cut","jj_b2b","jj_b2b_cut","jjl",
                 "bb","bb_cut","bb_leading","bb_leading_cut","bb_closest","bb_closest_cut","b1l" ]:
        
        hist_S = file.Get("stage_"+stageN+"/cleanup/M_"+obj) # signal: HH -> bbWW
        hist_B = file_tt.Get("stage_"+stageN+"/cleanup/M_"+obj) # BG: tt -> bbWW
        
        S = hist_S.Integral(1,hist_S.GetMaximumBin())
        B = hist_B.Integral(1,hist_S.GetMaximumBin())
        
        P = round( N_S * (S/S_tot) / (1+sqrt( N_B * (B/B_tot) )), 5 )
        print "   %s\t%.2f\t%.2f\t" % ( P, N_S*(S/S_tot), N_B*(B/B_tot) ) + "M_" + obj

    print "\n\n"


    ########
    # main #
    ########

def main():

    for stageN in ["0","1","2","3","4","5","6","7"]:
        punzi("stage_"+stageN)

    print "\nDone!\n"



if __name__ == '__main__':
    main()


