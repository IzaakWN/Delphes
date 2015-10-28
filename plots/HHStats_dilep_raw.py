from __future__ import division
from math import sqrt
import time

# intgrated luminosity
L = 3000.0 # / fb
S_tot = 0.0
B_tot = 0.0
N_S = 0.0
N_B = 0.0


    ######################
    # Punzi significance #
    ######################

def punzi(S,B):
    P = round( N_S * (S/S_tot) / (1+sqrt( N_B * (B/B_tot) )),5)
    print "   %s\t%i\t%i\t" % (P,N_S*(S/S_tot),N_B*(B/B_tot))
    return P


    ########
    # main #
    ########

def main():

    global S_tot, B_tot, N_S, N_B, L
    
    header = " Punzi significance" + \
         "\n  ---------------------------------------" + \
         "\n   P     \tS \tB" + \
         "\n  ---------------------------------------"

    S_di = [ 51464, 51464, 3181, 2499 ]
    B_di = [ 50789, 18899, 2023, 331 ]
    S_semi = [ 214888, 214888, 26511, 20634 ]
    B_semi = [ 211952, 182709, 35223, 15335 ]
    
    sigma_S = 40 * 0.0113
    sigma_B = 984500 * 0.0453
#    sigma_S = 0.163*2.3
#    sigma_B = 9030*1.85/0.372
    sigma_S = 0.163
    sigma_B = 9030/0.372
    N_S = sigma_S * L
    N_B = sigma_B * L
    S_tot = S_di[0]
    B_tot = B_di[0]
    
    print "\n#Dileptonic channel\n" + header
    for i in range(4):
        P = punzi(S_di[i],B_di[i])


    sigma_S = 40 * 0.0715
    sigma_B = 984500 * 0.2873
#    sigma_S = 0.163*2.3/0.0113*0.0715
#    sigma_B = 9030*1.85/0.372/0.0453*0.2873
    N_S = sigma_S * L
    N_B = sigma_B * L
    S_tot = S_semi[0]
    B_tot = B_semi[0]

    k = sqrt(0.0453/0.2873)
    print "\n\n#Semileptonic channel\n" + header
    for i in range(4):
        P = punzi(S_semi[i],B_semi[i])
        print "   %s" % round(k*P,5)
    


    print "\nDone!\n"



if __name__ == '__main__':
    main()


