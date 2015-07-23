from ROOT import *
from math import sqrt

# intgrated luminosity
L = 3000 # / fb

# cross section
sigma_S = 40 * 0.027 # fb = sigma_HH * BR_bbWW
sigma_B = 984500 # fb

# expected number of events
N_S = sigma_S * L
N_B = sigma_B * L
print "\nN_S = %s" % N_S
print "N_B = %s" % N_B

# total number of MC events run on
S_tot = 96084
B_tot = 496200
print "\nS_tot = %s" % S_tot
print "B_tot = %s" % B_tot

file = TFile("/home/uzh/ineute/phase2/Delphes_CMS/controlPlots_HH_all.root")
file_tt = TFile("/home/uzh/ineute/phase2/Delphes_CMS/controlPlots_tt_all.root")



    ######################
    # Punzi significance #
    ######################

def punzi(stage):
    print "\n  %s: Punzi significance" % stage[:-1]
    print "  -------------------------------------------------"
    print "   sigma \tS \tB \tS/B \treco"
    print "  -------------------------------------------------"

    hist_S = file.Get(stage+"selection/category") # signal: HH -> bbWW
    hist_B = file_tt.Get(stage+"selection/category") # BG: tt -> bbWW
    
    S = hist_S.GetBinContent(1) # MC after reco and cuts
    B = hist_B.GetBinContent(1)
    
    sigma = round( N_S * (S/S_tot) / (1+sqrt( N_B * (B/B_tot) ))*10000 )/10000

    print "   %s\t%i\t%i\t%s\tno reco" % (sigma,S,B,round(S/B*10)/10)
    print "  -------------------------------------------------"

    names = [ ]
    for process in ["Hbb"]:
        for alg in ["_b2","_b3"]:
            names.append( "reco/"+process+alg+"M" )
            names.append( "reco/"+process+alg+"M_window" )
        names.append( "reco2/"+process+"_d1M" )
        names.append( "reco2/"+process+"_d1M_window" )

    for name in names:

        hist_S = file.Get(stage+name) # MC signal: HH -> bbWW
        hist_B = file_tt.Get(stage+name) # MC BG: tt -> bbWW
        
        S = hist_S.GetEntries()
        B = hist_B.GetEntries()
        
        sigma = round( N_S * (S/S_tot) / (1+sqrt( N_B * (B/B_tot) ))*10000 )/10000

        title = name[name.index("_")+1:]
        print "   %s\t%i\t%i\t%s\t" % (sigma,S,B,round(S/B*10)/10) + title
#        print "   "+name+" sigma = %s, (S,B) = ( %i, %i )" % (sigma,S,B)



    ########
    # main #
    ########

def main():

    for stage in ["stage_1/","stage_2/","stage_3/","stage_4/"]:
        punzi(stage)

    print "\nDone!\n"



if __name__ == '__main__':
    main()


