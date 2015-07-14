from ROOT import *
import CMS_lumi, tdrstyle
from HH_bbWWPlotterTools import *

# CMS style
# CMS_lumi.CMS_lumi( c, 4, 33) # TPad, iPeriod, iPosX
CMS_lumi.extraText = "Simulation preliminary"
CMS_lumi.cmsTextSize = 0.65
CMS_lumi.outOfFrame = True
tdrstyle.setTDRStyle()

file = TFile("/home/uzh/ineute/phase2/Delphes_CMS/controlPlots_HH_all.root")



def main():



    ###############
    # basic plots #
    ###############
    print "\nBasic plots"

    names = [ ]

    for particle in ["b1","b2","q","nu","l","e","mu"]:
        for var in ["Pt","Eta","M"]:
            names.append("gen/"+particle+var)

    for particle in ["NVirtualWs","NLeptons","NElectrons","NMuons","NTaus","WDPID"]:
        names.append("gen/"+particle)

    for jet in ["jet","bjet"]:
        for var in ["Pt","Eta","M"]:
            for i in ["1","2","3","4"]:
                names.append("jets/"+jet+i+var)

    for jet in ["Njets","Nbjets"]:
        names.append("jets/"+jet)

    for name in names:

        c = makeCanvas()
        hist = file.Get("stage_1/"+name)
        
        if "N" in name or "PID" in name:
            hist.Scale(1./hist.Integral())
        
        hist.Draw()
        makeAxes(hist)
        
        legend = makeLegend(hist)
        legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        setFillStyle(hist)
        
        name = name.replace("gen/","basic/")
        name = name.replace("jets/","basic/")
        c.SaveAs(name+".png")
        c.Close()



    ############################
    # overlay "reco" and "gen" #
    ############################
    print "\nOverlay plots: reco and gen"
    
    names2 = []

    names2.extend([("gen/WlnuPt", "reco/Wlnu1Pt"),
                   ("gen/WlnuEta", "reco/Wlnu1Eta"),
                   ("gen/WlnuM", "reco/Wlnu1M"),
                   ("gen/nuPt", "jets/MET")])

    for process in ["Hbb", "Wjj", "HWW", "HHbbWW"]:
        for alg in ["_b1","_b2","_c1","_c2"]:
            for var in ["Pt","Eta","M"]:
                names2.append( ("gen/"+process+var,\
                                "reco/"+process+alg+var))

    for gen, reco in names2:

        c = makeCanvas()
        hist_gen = file.Get("stage_1/"+gen) # "data"
        hist_reco = file.Get("stage_1/"+reco) # "MC"
        hist_reco.Draw("histsame")
        hist_gen.Draw("ex0same")
        makeAxes(hist_reco,hist_gen)
        
        legend = makeLegend(hist_reco,hist_gen)
        legend.Draw()
        
        CMS_lumi.CMS_lumi(c,14,33)
        setFillStyle(hist_reco)
        setMarkerStyle(hist_gen)
        
        reco = reco.replace("jets/","basic/")
        c.SaveAs(reco+".png")
        c.Close()



    ############
    # 2D plots #
    ############
    print "\n2D plots"


    c = makeCanvas(square=True)
    hist = file.Get("stage_1/gen/WWM")
    hist.Draw()
    makeAxes(hist)
    CMS_lumi.CMS_lumi(c,14,33)
    hist.GetXaxis().SetRangeUser(0,110)
    hist.GetYaxis().SetRangeUser(0,110)
    legend = makeLegend(hist)
    legend.Draw()
    c.SaveAs("basic/WWM.png")

    hist_Wlnu = file.Get("stage_1/gen/WlnuM")
    hist_Wjj = file.Get("stage_1/gen/WjjM")

    scaleWlnu = 70/hist_Wlnu.GetMaximum()
    scaleWj = 70/hist_Wjj.GetMaximum()
    hist_Wlnu.Scale(scaleWlnu)
    hist_Wjj.Scale(scaleWj)
    hist_Wlnu.GetXaxis().SetRangeUser(0,110)
    hist_Wjj.GetXaxis().SetRangeUser(0,110)
    
    hist_Wlnu.SetFillColor(0)
    hist_Wlnu.SetLineColor(kRed)
    hist_Wjj.SetFillColor(kCyan-10)
#    hist_Wjj.SetLineColor(kAzure)
    hist_Wlnu.Draw("same")
    hist_Wjj.Draw("hbarsame")
    hist.Draw("same")

    legend = makeLegend(hist)
    legend.Draw()

    c.SaveAs("basic/WWM2.png")
    c.Close()



    ###############
    # extra plots #
    ###############
    print "\nExtra plots"


    # __WlnuM vs Wjj__
    c = makeCanvas()
    hist_Wlnu = file.Get("stage_1/gen/WlnuM")
    hist_Wjj = file.Get("stage_1/gen/WjjM")
    hist_Wlnu.Scale(1/hist_Wlnu.Integral())
    hist_Wjj.Scale(1/hist_Wjj.Integral())
    
    hist_Wlnu.Draw()
    hist_Wjj.Draw("same")
    setLineStyle(hist_Wlnu,hist_Wjj)
    hist_Wjj.SetFillColor(0)

    makeAxes(hist_Wlnu,hist_Wjj)
    hist_Wlnu.GetXaxis().SetRangeUser(0,120)
#    hist_Wjj.GetXaxis().SetRangeUser(0,120)
#    hist_Wlnu.GetYaxis().SetTitleOffset(1.88)

    y1 = y2 - height[1]
    legend = TLegend(x1,y1,x2,y2)
    legend.SetBorderSize(0)
    legend.SetTextSize(legendTextSize)
    legend.SetHeader("W at gen level")
    legend.AddEntry(hist_Wlnu,"W #rightarrow l#nu")
    legend.AddEntry(hist_Wjj,"W #rightarrow qq")
    legend.Draw()


    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic/WWM_1D.png")
    c.Close()



    print "\nDone with this, son.\n"



if __name__ == '__main__':
    main()


