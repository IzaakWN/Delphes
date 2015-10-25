from __future__ import division
from ROOT import *
from math import sqrt
import time

# intgrated luminosity
L = 3000 # / fb

# cross section
# ttbar: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
sigma_S = 40 * 0.01 # fb = sigma_HH * BR_bbWW_bblnulnu
sigma_B = 984500 * 0.06 # fb
#sigma_S = 0.163 # fb
#sigma_B = 9.03 # fb

# expected number of events
N_S = sigma_S * L
N_B = sigma_B * L

# total number of MC events run on
S_tot = 51464 #214888
B_tot = 50789 #8899 #211952 #170692

preamble = time.strftime("\n\n%D - %H:%M:%S",time.gmtime()) + \
           "\n\n# Comments:\n" + raw_input("\n# Comments: ")

print preamble
f = open("HHStats_dilep.txt","a")
f.write( preamble )
file = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_dilep_all.root")
file_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_dilep_all.root")



    ######################
    # Punzi significance #
    ######################

def punzi(stage):
    table = "\n\n  %s: Punzi significance" % stage[:-1] + \
              "\n  -------------------------------------------------" + \
              "\n   P     \tS \tB \t\treco" + \
              "\n  -------------------------------------------------"

    hist_S = file.Get(stage+"selection/category") # signal: HH -> bbWW
    hist_B = file_tt.Get(stage+"selection/category") # BG: tt -> bbWW

    if int(stage[-2]) < 4:
        S = hist_S.GetBinContent(1) # MC after reco and cuts
        B = hist_B.GetBinContent(1)
    else:
        S = hist_S.GetBinContent(5) # MC after reco and cuts
        B = hist_B.GetBinContent(5)
    
    P = round( N_S * (S/S_tot) / (1+sqrt( N_B * (B/B_tot) ))*10000 )/10000

    table += "\n   %s\t%i\t%i\tnone" % (P,N_S*(S/S_tot),N_B*(B/B_tot)) + \
             "\n  -------------------------------------------------"

    print table
    f.write( "\n"+table )



    ########
    # main #
    ########

def main():

    global S_tot, B_tot, N_S, N_B, L


    preamble = "\n\n# Dileptonic channel" + \
               "\n\n# expected number of events\nN_S = %i\nN_B = %i" % (N_S,N_B) + \
               "\n\n# total number of MC events run on\nS_tot = %i\nB_tot = %i" % (S_tot,B_tot)
    print preamble
    f.write( preamble )

    for stageN in ["0","1","2","3"]:
        punzi("stage_"+stageN+"/")


    sigma_S = 40 * 0.07 # fb
    sigma_B = 984500 * 0.30 # fb
    N_S = sigma_S * L
    N_B = sigma_B * L
    S_tot = 214888
    B_tot = 211952 # 170692
    preamble = "\n\n\n\n# Semileptonic channel" + \
               "\n\n# expected number of events\nN_S = %i\nN_B = %i" % (N_S,N_B) + \
               "\n\n# total number of MC events run on\nS_tot = %i\nB_tot = %i" % (S_tot,B_tot)
    print preamble
    f.write( preamble )

    for stageN in ["4","5","6","7"]:
        punzi("stage_"+stageN+"/")


    f.write("\n\n\n")
    f.close()
    print "\nDone!\n"



if __name__ == '__main__':
    main()


