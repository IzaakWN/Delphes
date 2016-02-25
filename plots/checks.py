from ROOT import TFile, TH1F

file = TFile("/Users/IWN/Code/ROOT/phase2/Delphes/controlPlots_HH_all.root")
file_tt = TFile("/Users/IWN/Code/ROOT/phase2/Delphes/controlPlots_tt_all.root")



def forwardJet(stage):
    print "\n>>> " + stage

    cuts = [ "", "20", "30", "50" ]
    etaRegions = [ [0,2.5], [2.5,3.0], [3.0,3.5], [3.5,4.0], [4.0,4.5], [4.5,5.0], [5.0,100.0] ]

    header = "  cut  |   eta<2.5  2.5<eta<3  3<eta<3.5  3.5<eta<4 " + \
                                " 4<eta<4.5  4.5<eta<5     5<eta"
    tableS = header
    tableB = header

    for cut in cuts:
        
        if cut:
            tableS += "\n   "+cut+"  |"
            tableB += "\n   "+cut+"  |"
        else:
            tableS += "\n    0  |"
            tableB += "\n    0  |"

        hist_S = file.Get(stage+"jets/EtaMostForwardJet"+cut)
        hist_B = file_tt.Get(stage+"jets/EtaMostForwardJet"+cut)

        S_tot = hist_S.Integral()
        B_tot = hist_B.Integral()

        for min, max in etaRegions:
#            print hist_S.GetXaxis().FindBin(min)
#            print hist_S.GetXaxis().FindBin(max)
            S = hist_S.Integral(hist_S.FindBin(min),hist_S.FindBin(max)-1)
            B = hist_B.Integral(hist_B.GetXaxis().FindBin(min),hist_B.GetXaxis().FindBin(max))

            tableS += "    %4.1f   " % (S/S_tot*100.0)
            tableB += "    %4.1f   " % (B/B_tot*100.0)

    print "\nSignal: eta of most forward jet\n" + tableS
    print "\nBackground: eta of most forward jet\n" + tableB



    cuts = [ 0.0, 20.0, 30.0, 50.0 ]
    header = "  cut  |  most forward jet fails cut  "
    tableS = header
    tableB = header
    hist_S = file.Get(stage+"jets/PTMostForwardJet")
    hist_B = file_tt.Get(stage+"jets/PTMostForwardJet")
    S_tot = hist_S.Integral()
    B_tot = hist_B.Integral()
    
    for cut in cuts:
        tableS += "\n   %2.f  |" % cut
        tableB += "\n   %2.f  |" % cut
        
        if cut:
            S = hist_S.Integral(hist_S.FindBin(0),hist_S.FindBin(cut)-1)
            B = hist_B.Integral(hist_B.FindBin(0),hist_B.FindBin(cut)-1)
            tableS += "         %4.1f          " % (S/S_tot*100.0)
            tableB += "         %4.1f          " % (B/B_tot*100.0)
        else:
            tableS += "         %4.1f          " % 0
            tableB += "         %4.1f          " % 0

    print "\n\nSignal: cutflow\n" + tableS
    print "\nBackground: cutflow\n" + tableB



    cuts = [ "", "20", "30", "50" ]
    header = "  cut  |    0      1      2      3      4      5      6      7"
    tableS = header
    tableB = header

    for cut in cuts[1:]:
        
        if cut:
            tableS += "\n   "+cut+"  |"
            tableB += "\n   "+cut+"  |"
        else:
            tableS += "\n    0  |"
            tableB += "\n    0  |"

        hist_S = file.Get(stage+"jets/NForwardJets"+cut)
        hist_B = file_tt.Get(stage+"jets/NForwardJets"+cut)

        S_tot = hist_S.Integral()
        B_tot = hist_B.Integral()

        for i in [ 0, 1, 2, 3, 4, 5, 6, 7 ]:
            S = hist_S.GetBinContent(i+1) # bin 0 is underflow
            B = hist_B.GetBinContent(i+1)

            tableS += " %5.1f " % (S/S_tot*100.0)
            tableB += " %5.1f " % (B/B_tot*100.0)

    print "\n\nSignal: number of jet with |eta|>2.5\n" + tableS
    print "\nBackground: number of jet with |eta|>2.5\n" + tableB
    print " "



def main():

    forwardJet("stage_0/")
    forwardJet("stage_1/")



if __name__ == '__main__':
    main()
    print "\n>>> done"


