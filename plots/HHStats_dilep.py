from __future__ import division
from ROOT import *
from math import sqrt
import time

preamble = time.strftime("\n\n%D - %H:%M:%S",time.gmtime()) + \
           "\n\n# Comments:\n" + raw_input("\n# Comments: ")

print preamble
f = open("HHStats_dilep.txt","a")
f.write( preamble )
file = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_dilep_all.root")
file_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_dilep_all.root")

# intgrated luminosity
L = 3000 # / fb

# cross section
# ttbar: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
#sigma_S = 40 * 0.0113 # fb = sigma_HH * BR_bbWW_bblnulnu
#sigma_B = 984500 * 0.0453 # fb
sigma_S = 0.163*2.3 # fb
sigma_B = 9030*1.85/0.372 # fb

# expected number of events
N_S = sigma_S * L
N_B = sigma_B * L

# total number of MC events run on
hist_S = file.Get("stage_0/selection/category") # signal: HH -> bbWW
hist_B = file_tt.Get("stage_0/selection/category") # BG: tt -> bbWW
S_tot = hist_S.GetBinContent(1) #51464 #214888
B_tot = hist_B.GetBinContent(1) #50789 #8899 #211952 #170692



    ######################
    # Punzi significance #
    ######################

def punzi(stage):

    hist_S = file.Get(stage+"selection/category") # signal: HH -> bbWW
    hist_B = file_tt.Get(stage+"selection/category") # BG: tt -> bbWW

    if int(stage[-2]) < 4:
        S = hist_S.GetBinContent(1) # MC after reco and cuts
        B = hist_B.GetBinContent(2)
        if int(stage[-2]) == 0:
            B2 = hist_B.GetBinContent(2)
            print "\nGenlevel with cuts on BG = %s GenLevel without cuts on BG \n" % \
                  (round(B2/B*1000)/1000)
    else:
        S = hist_S.GetBinContent(5) # MC after reco and cuts
        B = hist_B.GetBinContent(5)
    
    P = round( N_S * (S/S_tot) / (1+sqrt( N_B * (B/B_tot) ))*100000 )/100000
    table = "   %s\t%i\t%i\t" % (P,N_S*(S/S_tot),N_B*(B/B_tot)) + stage[:-1]

    print table
    f.write( "\n"+table)



    ########
    # main #
    ########

def main():

    global S_tot, B_tot, N_S, N_B, L

    header = "\n\n Punzi significance" + \
             "\n  -------------------------------------------------" + \
             "\n   P     \tS \tB \t\tstage" + \
             "\n  -------------------------------------------------"


    preamble = "\n\n# Dileptonic channel" + \
               "\n\n# expected number of events\nN_S = %i\nN_B = %i" % (N_S,N_B) + \
               "\n\n# total number of MC events run on\nS_tot = %i\nB_tot = %i" % (S_tot,B_tot) + \
               header
    print preamble
    f.write( preamble)

    for stageN in ["1","2","3"]:
        punzi("stage_"+stageN+"/")


#    sigma_S = 40 * 0.0715 # fb
#    sigma_B = 984500 * 0.2873 # fb
    sigma_S = 0.163*2.3/0.0113*0.0715 # fb
    sigma_B = 9030*1.85/0.372/0.0453*0.2873 # fb
    N_S = sigma_S * L
    N_B = sigma_B * L
    hist_S = file.Get("stage_4/selection/category") # signal: HH -> bbWW
    hist_B = file_tt.Get("stage_4/selection/category") # BG: tt -> bbWW
    S_tot = hist_S.GetBinContent(5) #214888
    B_tot = hist_B.GetBinContent(5) #211952 #170692
    preamble = "\n\n\n# Semileptonic channel" + \
               "\n\n# expected number of events\nN_S = %i\nN_B = %i" % (N_S,N_B) + \
               "\n\n# total number of MC events run on\nS_tot = %i\nB_tot = %i" % (S_tot,B_tot) + \
               header
    print preamble
    f.write( preamble)

    for stageN in ["5","6","7"]:
        punzi("stage_"+stageN+"/")


    f.write("\n\n\n")
    f.close()

    print "\n"
    for stageN in ["0","1","2","3","4","5","6","7"]:
        hist_S = file.Get("stage_"+stageN+"/selection/category") # signal: HH -> bbWW
        hist_B = file_tt.Get("stage_"+stageN+"/selection/category") # BG: tt -> bbWW
        S = hist_S.GetBinContent(int(stageN)+1)
        B = hist_B.GetBinContent(int(stageN)+1)
        print "stage_"+stageN+ ":  S = %s,\t B = %s" % (S,B)
        


    print "\nDone!\n"



if __name__ == '__main__':
    main()


