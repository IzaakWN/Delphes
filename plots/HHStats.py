from __future__ import division
from ROOT import *
from math import sqrt
import time

# intgrated luminosity
L = 3000 # / fb

# cross section
sigma_S = 40 * 0.07 # fb = sigma_HH * BR_bbWW_bbqqlnu
sigma_B = 984500 # fb

# expected number of events
N_S = sigma_S * L
N_B = sigma_B * L

# total number of MC events run on
S_tot = 96084
B_tot = 496200

preamble = time.strftime("\n\n%D - %H:%M:%S",time.gmtime()) + \
           "\n\n# expected number of events\nN_S = %i\nN_B = %i" % (N_S,N_B) + \
           "\n\n# total number of MC events run on\nS_tot = %i\nB_tot = %i" % (S_tot,B_tot) + \
           "\n\n# Comments:\n" + raw_input("\n# Comments: ")

print preamble
f = open("HHStats.txt","a")
f.write( preamble )
file = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_HH_all.root")
file_tt = TFile("/shome/ineuteli/phase2/CMSSW_5_3_24/src/Delphes/controlPlots_tt_all.root")



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
    
    S = hist_S.GetBinContent(1) # MC after reco and cuts
    B = hist_B.GetBinContent(1)
    
    P = round( N_S * (S/S_tot) / (1+sqrt( N_B * (B/B_tot) ))*10000 )/10000

    table += "\n   %s\t%i\t%i\tnone" % (P,N_S*(S/S_tot),N_B*(B/B_tot)) + \
             "\n  -------------------------------------------------"

    names = [ ]
    #for alg in ["_b1","_b2","_b3","_b4","_a1"]:
        #names.append( "reco/Hbb"+alg+"M" )
        #names.append( "reco/Hbb"+alg+"M_window1" )
        #names.append( "reco/Hbb"+alg+"M_window2" )
    #names.append( "reco/Hbb_a1M_window3" )
    #names.append( "reco2/Hbb_d1M" )
    #names.append( "reco2/Hbb_d1M_window1" )
    #names.append( "reco2/Hbb_d1M_window2" )
    for alg in ["jj","jj_cut","jj_b2b","jj_b2b_cut","bb","bb_cut"]
        names.append( "cleanup/M_"+alg )

    for name in names:

        hist_S = file.Get(stage+name) # MC signal: HH -> bbWW
        hist_B = file_tt.Get(stage+name) # MC BG: tt -> bbWW
        
        S = hist_S.GetEntries()
        B = hist_B.GetEntries()
        
        P = round( N_S * (S/S_tot) / (1+sqrt( N_B * (B/B_tot) ))*10000 )/10000

        title = name[name.index("_")+1:]
        table += "\n   %s\t%i\t%i\t" % (P,N_S*(S/S_tot),N_B*(B/B_tot)) + title

    print table
    f.write( "\n"+table )



    ########
    # main #
    ########

def main():

    for stage in ["stage_0/","stage_1/","stage_2/","stage_3/","stage_4/","stage_5/"]:
        punzi(stage)

    f.write("\n\n\n")
    f.close()
    print "\nDone!\n"



if __name__ == '__main__':
    main()

