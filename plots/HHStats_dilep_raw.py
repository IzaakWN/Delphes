from __future__ import division
from math import sqrt
import time

# intgrated luminosity
L = 3000.0 # / fb


    ######################
    # Punzi significance #
    ######################

def punzi(S,B,S_tot,B_tot,sigma_S,sigma_B):

    N_S = sigma_S * L
    N_B = sigma_B * L
    P = round( N_S * (S/S_tot) / (1+sqrt( N_B * (B/B_tot) )),5)
    print "   %.4f\t%.1f\t%.1f\t" % (P,N_S*(S/S_tot),N_B*(B/B_tot))
    return P


    ########
    # main #
    ########

def main():

#    global S_tot, B_tot, N_S, N_B, L

    header = " Punzi significance" + \
         "\n  ---------------------------------------" + \
         "\n   P     \tS \tB" + \
         "\n  ---------------------------------------"

#    # with taus
#    S_di = [ 51464, 51464, 3181, 2499 ]
#    B_di = [ 50789, 18899, 2023, 331 ]
#    S_semi = [ 214888, 214888, 26511, 20634 ]
#    B_semi = [ 211952, 182709, 35223, 15335 ]

#    # with taus
#    # with oppositely charged + DeltaR_ql
#    S_di = [ 51464, 51464, 3181, 2500  ]
#    B_di = [ 50789, 18899, 2023, 331 ]
#    S_semi = [ 214888, 214888, 26511, 20634 ]
#    B_semi = [ 211952, 101940, 20848, 9428 ]

    # without taus
    # with oppositely charged + DeltaR_ql
    S_di = [ 22812, 22812, 2748, 2149 ]
    B_di = [ 22546, 8339, 1755, 296 ]
    S_semi = [ 166483, 166483, 28203, 22189 ]
    B_semi = [ 164661, 68011, 19401, 8748 ]

    # without taus in BR
    sigma_S = 40 * 0.011
    sigma_B = 984500 * 0.045
#    # with taus in BR
#    sigma_S = 40 * 0.0263
#    sigma_B = 984500 * 0.1057
    k = B_di[1]/B_di[0]
    sigma_S_AN = 0.163*2.3
    sigma_B_AN = 9030*1.85/k
    
    print "\n#Dileptonic channel\n" + header
    for i in range(4):
        P = punzi(S_di[i],B_di[i],S_di[0],B_di[0],sigma_S,sigma_B)
        P = punzi(S_di[i],B_di[i],S_di[0],B_di[0],sigma_S_AN,sigma_B_AN)
        print "\n"

    # without taus in BR
    sigma_S = 40 * 0.072
    sigma_B = 984500 * 0.287
#    # with taus in BR
#    sigma_S = 40 * 0.1093
#    sigma_B = 984500 * 0.4389
    k = B_semi[1]/B_semi[0]
    sigma_S_AN = sigma_S_AN/0.011*0.072
    sigma_B_AN = sigma_B_AN/0.045*0.287

    k_BR = sqrt(0.0453/0.2873) # scale back to dileptonic cross section
    print "\n\n#Semileptonic channel\n" + header
    for i in range(4):
        P = punzi(S_semi[i],B_semi[i],S_semi[0],B_semi[0],sigma_S,sigma_B)
        print "   %.4f" % (k_BR*P)
        P = punzi(S_semi[i],B_semi[i],S_semi[0],B_semi[0],sigma_S_AN,sigma_B_AN)
        print "   %.4f" % (k_BR*P)
        print "\n"



    print "\nDone!\n"



if __name__ == '__main__':
    main()

