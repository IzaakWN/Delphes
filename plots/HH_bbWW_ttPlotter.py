from ROOT import *
import CMS_lumi, tdrstyle
from HH_bbWWPlotterTools import *

# CMS style
# CMS_lumi.CMS_lumi( c, 4, 33) # TPad, iPeriod, iPosX
CMS_lumi.cmsText = "CMS"
CMS_lumi.extraText = "Simulation preliminary"
CMS_lumi.cmsTextSize = 0.65
#CMS_lumi.drawLogo = True
CMS_lumi.outOfFrame = True
tdrstyle.setTDRStyle()

file = TFile("/home/uzh/ineute/phase2/Delphes_CMS/controlPlots_HH_all.root")
file_tt = TFile("/home/uzh/ineute/phase2/Delphes_CMS/controlPlots_tt_all.root")

stage = "stage_2/"


def main():



    ###############
    # basic plots #
    ###############
    print "\nBasic plots"

    names = [ ]

    for particle in ["b1","b2","q","nu","l","e","mu"]:
        for var in ["Pt","Eta","M"]:
            names.append("gen/"+particle+var)

    for particle in ["NVirtualWs","NLeptons","NElectrons","NMuons","NTaus",
                     "NWlnu","WDPID","tDPID"]: #NWjj
        names.append("gen/"+particle)

    for jet in ["jet","bjet"]:
        for var in ["Pt","Eta","M"]:
            for i in ["1","2","3","4"]:
                names.append("jets/"+jet+i+var)

    for jet in ["Njets","Nbjets"]:
        names.append("jets/"+jet)

    for particle in ["NMuons20","NElectrons20"]:
        names.append("leptons/"+particle)

    for process in ["Hbb", "HWW", "HHbbWW"]:
        for alg in ["_b2"]: #["_b1","_b2","_c1","_c2"]:
            for var in ["Pt","Eta","M"]:
                names.append("reco/"+process+alg+var)

    for name in names:

        c = makeCanvas()
        hist_S = file.Get(stage+name) # signal: HH -> bbWW
        hist_tt = file_tt.Get(stage+name) # BG: tt -> bbWW
        
#        if "N" == name[4] or "PID" in name:
        I = hist_S.Integral()
        if I == 0: I=1
        hist_S.Scale(1./I)
        hist_tt.Scale(1./hist_tt.Integral())
        
        hist_S.Draw()
        hist_tt.Draw("same")
        makeAxes(hist_S,hist_tt)
        
        legend = makeLegend(hist_S,hist_tt,tt=True)
        legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(hist_S,hist_tt)
        
        name = name.replace("gen/","basic_tt/")
        name = name.replace("leptons/","basic_tt/")
        name = name.replace("jets/","basic_tt/")
        name = name.replace("reco/","reco_tt/")
        c.SaveAs(name+".png")
        c.Close()



    ############################
    # overlay "reco" and "gen" #
    ############################
    print "\nOverlay plots: reco and gen"
    
    names2 = [ ]

#    names2.extend([("gen/WlnuPt", "reco/Wlnu1Pt"),
#                   ("gen/WlnuEta", "reco/Wlnu1Eta"),
#                   ("gen/WlnuM", "reco/Wlnu1M"),
#                   ("gen/nuPt", "jets/MET")]) # beware of normalization above!
#
##    names2.extend([("gen/lPt", "leptons/lPt")])
#
#    for process in ["Wjj"]:
#        for alg in ["_b2"]: #["_b1","_b2","_c1","_c2"]:
#            for var in ["Pt","Eta","M"]:
#                names2.append( ("gen/"+process+var,\
#                                "reco/"+process+alg+var))

    for gen, reco in names2:

        c = makeCanvas()
        hist_gen = file.Get(stage+gen) # "data"
        hist_reco = file.Get(stage+reco) # "MC"
        hist_reco_tt = file_tt.Get(stage+reco) ## "MC" from tt
        
        if "nu" in gen:
            hist_gen.Scale(1./hist_gen.Integral())
            hist_reco.Scale(1./hist_reco.Integral())
            hist_reco_tt.Scale(1./hist_reco_tt.Integral())

        hist_reco.Draw("histsame")
        hist_reco_tt.Draw("histsame")
        hist_gen.Draw("ex0same")
        makeAxes(hist_reco,hist_reco_tt,hist_gen)
        
        legend = makeLegend(hist_gen,hist_reco,hist_reco_tt,tt=True)
        legend.Draw()
        
        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(hist_reco,hist_reco_tt)
        setMarkerStyle(hist_gen)
        
        reco = reco.replace("reco/","reco_tt/")
        reco = reco.replace("jets/","basic_tt/")
        c.SaveAs(reco+".png")
        c.Close()



    ############
    # 2D plots #
    ############

    # WWM BG
    c = makeCanvas(square=True)
    hist = file.Get(stage+"gen/WWM")
    hist_tt = file_tt.Get(stage+"gen/WWM")
    
    hist_tt.Draw()
    makeAxes(hist_tt)

    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic_tt/WWM.png")
    c.Close()

    # WWM singal vs BG
    c = makeCanvas(square=True)
    hist_tt = file_tt.Get(stage+"gen/WWM")

    hist_tt.Draw()
    hist.Draw("same")
    makeAxes(hist)
    legend = makeLegend(hist,hist_tt,tt=True)
    legend.Draw()
    hist.SetMarkerColor(kRed+3)
    hist_tt.SetMarkerColor(kAzure+4)

    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic_tt/WWM_both.png")
    c.Close()

    # bbWWM singal vs BG
    c = makeCanvas(square=True)
    hist = file.Get(stage+"gen/bbWWM")
    hist_tt = file_tt.Get(stage+"gen/bbWWM")

    hist_tt.Draw()
    hist.Draw("same")
    makeAxes(hist)
    hist.SetMarkerColor(kRed+3)
    hist_tt.SetMarkerColor(kAzure+4)

    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic_tt/bbWWM_both.png")
    c.Close()



    ###############
    # extra plots #
    ###############
    print "\nExtra plots"
    
    for var in ["M","Pt","Eta"]:

        c = makeCanvas()
        hist_S = file.Get(stage+"gen/HHbbWW"+var) # signal: HH -> bbWW
        hist_tt = file_tt.Get(stage+"gen/ttbbWW"+var) # BG: tt -> bbWW
        hist_S.Scale(1./hist_S.Integral())
        hist_tt.Scale(1./hist_tt.Integral())
        
        hist_S.Draw()
        hist_tt.Draw("same")
        makeAxes(hist_S,hist_tt)

        y1 = y2 - height[1]
        legend = TLegend(x1,y1,x2,y2)
        legend.SetBorderSize(0)
        legend.SetTextSize(legendTextSize)
        legend.SetHeader("gen level")
        legend.AddEntry(hist_S,"HH #rightarrow bbWW")
        legend.AddEntry(hist_tt,"t#bar{t} #rightarrow bbWW")
        legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(hist_S,hist_tt)
        
        c.SaveAs("basic/HHtt"+var+".png")
        c.Close()



    # __WlnuM vs Wjj__
    c = makeCanvas()
    hist_Wlnu = file_tt.Get(stage+"gen/WlnuM")
    hist_Wjj = file_tt.Get(stage+"gen/WjjM")
    hist_Wlnu.Draw()
    hist_Wjj.Draw("same")
    setLineStyle(hist_Wlnu,hist_Wjj)

    makeAxes(hist_Wlnu,hist_Wjj)
    hist_Wlnu.GetXaxis().SetRangeUser(0, 120)
#    hist_Wjj.GetXaxis().SetRangeUser(0, 120)
    hist_Wlnu.GetYaxis().SetTitleOffset(1.88)

    y1 = y2 - height[1]
    legend = TLegend(x1,y1,x2,y2)
    legend.SetBorderSize(0)
    legend.SetTextSize(legendTextSize)
    legend.SetHeader("W at gen level")
    legend.AddEntry(hist_Wlnu,"W #rightarrow l#nu")
    legend.AddEntry(hist_Wjj,"W #rightarrow qq")
    legend.Draw()


    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic_tt/WWM_1D.png")
    c.Close()

    
    # __Pie chart__
    W = 1200
    H = 1200

    for stageN in ["0"]:
        c = makeCanvas(square=True)
        hist = file_tt.Get("stage_"+stageN+"/gen/NWlnu")
        hist.GetXaxis().SetRangeUser(0, 3)
        pie = TPie(hist)
        pie.SetCircle(.486,.5,.2)
        pie.SetAngularOffset(200)
        pie.SetEntryRadiusOffset(2,.03)

        labels = ["hadronic","monoleptonic","dileptonic"]
        colors = [kAzure-4,kGreen-3,kRed] #kOrange-3
        linecolors = [kAzure-6,kGreen+4,kRed+4] #Orange+4
        pie.SetLabelFormat("#splitline{#scale[1.4]{#font[2]{%txt}}}{#scale[1.2]{ %perc}}")
        pie.SetLabelsOffset(0.019)
        for i in range(3):
            pie.SetEntryFillColor(i,colors[i])
            pie.SetEntryLineColor(i,linecolors[i])
            pie.SetEntryLineWidth(i,1)
            pie.SetEntryLabel(i,labels[i])
        
        if stageN == "0":
            pie.SetEntryRadiusOffset(0,.02)
        else:
            pie.SetEntryRadiusOffset(1,.02)

        pie.Draw("SC>")

        c.SaveAs("basic_tt/branchfraction_stage"+stageN+".png")
        c.Close()



    print "\nDone with this, son.\n"



if __name__ == '__main__':
    main()


