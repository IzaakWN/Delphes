# DecayTree by IWN



def main():

    import time
    start = time.time()

    from ROOT import TFile, gDirectory
    from ROOT import TH1D, TH2D, TVirtualPad, TCanvas, TMath, gStyle


    ###  ___ SET-UP ___ ###

    myfile = TFile('HH_bbWW_1_TP.root')
    mychain = gDirectory.Get( 'Delphes' )
    mychain.SetBranchStatus("*",0)
    mychain.SetBranchStatus("Particle",1)
    mychain.SetBranchStatus("Particle.PID",1)
    mychain.SetBranchStatus("Particle.M1",1)
    mychain.SetBranchStatus("Particle.M2",1)
    mychain.SetBranchStatus("Particle.D1",1)
    mychain.SetBranchStatus("Particle.D2",1)
    nentries = mychain.GetEntriesFast()

    # electron PT histogram
    hist_PID = TH1D("hist_PID","Histogram of PID",10,-1,40)
    hist_PID.GetYaxis().SetTitle("number of particles")
    hist_PID.GetXaxis().SetTitle("PID")
    
#    nSucces = 0
#    nFails = 0


    ###  ___ LOOP ___ ###
    for jentry in xrange( nentries ):
        
        # Get the next tree in the chain and verify.
        nentry = mychain.LoadTree( jentry )
        if nentry < 0:
            break
        
        # Copy next entry into memory and verify.
        nb = mychain.GetEntry( jentry )
        if nb <= 0:
            continue

#        nP = mychain.Particle.GetEntries()
        for i in xrange(6):
            #print "Particle i=%d" %i
            if mychain.GetLeaf("Particle","Particle.PID").GetValue(i)==0:
                print "Fail"
            else:
                hist_PID.Fill(mychain.GetLeaf("Particle","Particle.PID").GetValue(i))


    ###  ___ WRAP UP ___ ###

    lol = TCanvas("lol","Histograms")
#    lol.Divide(2,1,0.01,0.01)
#
#    lol.cd(1)
    hist_PID.Draw()


    lol.Update()

    end = time.time()
    print "\nThe program lasted",end-start,"seconds."
    raw_input("Press enter to close off.\n")



if __name__ == '__main__':
    main()


