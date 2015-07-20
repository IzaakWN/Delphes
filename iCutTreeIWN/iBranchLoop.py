# Branch looper by IWN



def main():

    import time
    start = time.time()

    from ROOT import TFile, gDirectory
    from ROOT import TH1D, TH2D, TVirtualPad, TCanvas, TMath, gStyle


    ###  ___ SET-UP ___ ###

    myfile = TFile('HH_bbWW_1_TP.root') # get file
    mychain = gDirectory.Get( 'Delphes' ) # get chain (collection of tree)
    mychain.SetBranchStatus("*",0)
    #mychain.SetBranchStatus("Electron.*",1)
    mychain.SetBranchStatus("Electron.PT",1)
    mychain.SetBranchStatus("Electron.Phi",1)
    #mychain.SetBranchStatus("Muon.*",1)
    mychain.SetBranchStatus("Muon.PT",1)
    mychain.SetBranchStatus("Muon.Phi",1)
    #mychain.SetBranchStatus("MissingET.*",1)
    mychain.SetBranchStatus("MissingET.MET",1)
    mychain.SetBranchStatus("MissingET.Phi",1)
    nentries = mychain.GetEntriesFast() # get number of entries

    # electron PT histogram
    hist_ePT = TH1D("hist_ePT","Histogram of electron",100,0,250)
    hist_ePT.GetYaxis().SetTitle("number of events")
    hist_ePT.GetXaxis().SetTitle("P_T [GeV]")

    # MET histogram
    hist_MET = TH1D("hist_MET","Histogram of MET",100,0,250)
    hist_MET.GetYaxis().SetTitle("number of events")
    hist_MET.GetXaxis().SetTitle("MET")

    # sum histogram
    hist_sum = TH1D("hist_sum","Sum of electron's P_T and MET",100,0,250)
    hist_sum.GetYaxis().SetTitle("number of events")
    hist_sum.GetXaxis().SetTitle("P_T + MET [GeV]")

    # transverse mass histogram
    hist_MT = TH1D("hist_MT","Transverse mass",100,0,250)
    hist_MT.GetYaxis().SetTitle("number of events")
    hist_MT.GetXaxis().SetTitle("MT [GeV]")

    ## 2D histogram
    #hist_2D = TH2D("hist_2D","Scatterplot of ... vs. ...",100,0,250,100,0,250)
    #hist_2D.GetYaxis().SetTitle("... []")
    #hist_2D.GetXaxis().SetTitle("... []")


    ###  ___ LOOP ___ ###
    for jentry in xrange( nentries ): # for-loop from 0 to entries
        
        # Get the next tree in the chain and verify.
        nentry = mychain.LoadTree( jentry )
        if nentry < 0:
            break
        
        # Copy next entry into memory and verify.
        nb = mychain.GetEntry( jentry )
        if nb <= 0:
            continue
        
        # Select events that have both electrons and MET
        nE = mychain.Electron.GetEntries()
        nM = mychain.MissingET.GetEntries()
        if (nE==1 and nM==1):
            ePT = mychain.GetLeaf("Electron","Electron.PT").GetValue()
            MET = mychain.GetLeaf("MissingET","MissingET.MET").GetValue()
            Phi = mychain.GetLeaf("MissingET","MissingET.Phi").GetValue()-mychain.GetLeaf("Electron","Electron.Phi").GetValue()
            hist_ePT.Fill(ePT)
            hist_MET.Fill(MET)
            hist_sum.Fill(ePT + MET)
            hist_MT.Fill( TMath.Sqrt(ePT*MET*(1-TMath.cos(Phi))) )


    ###  ___ WRAP UP ___ ###

    lol = TCanvas("lol","Test histograms!")
    lol.Divide(2,2,0.01,0.01)
    
    lol.cd(1)
    hist_ePT.Draw()
    #ebeamHist.Fit("gaus")
    #gStyle.SetOptFit()

    lol.cd(2)
    hist_MET.Draw()
    #chi2Hist.Fit("gaus")
    #gStyle.SetOptFit()

    lol.cd(3)
    hist_sum.Draw()

    lol.cd(4)
    hist_MT.Draw()

    lol.Update()

    end = time.time()
    print "\nThe program lasted",end-start,"wseconds."

    raw_input("Press enter to close off.\n")



if __name__ == '__main__':
    main()


