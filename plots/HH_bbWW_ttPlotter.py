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



    ###############
    # basic plots #
    ###############

def plotBasic(stage):
    print "\n  %s: Basic plots" % stage[:-1]

    names = [ ]

#    for particle in ["b1","b2","q","nu","l","e","mu"]:
#        for var in ["Pt","Eta","M"]:
#            names.append("gen/"+particle+var)
#
#    for particle in ["NVirtualWs","NLeptons","NElectrons","NMuons","NTaus",
#                     "NWlnu","WDPID","tDPID"]: #NWjj
#        names.append("gen/"+particle)
#
#    for jet in ["jet","bjet"]:
#        for var in ["Pt","Eta","M"]:
#            for i in ["1","2","3","4"]:
#                names.append("jets/"+jet+i+var)
#
#    for jet in ["Njets","Nbjets"]:
#        names.append("jets/"+jet)

    names.append("res/NJetiWMatch")
    names.append("res/jetWMatchEta")
    names.append("res/jetWUnMatchEta")
    names.append("jets/NjetsEta3")
    names.append("jets/NjetsEta25")
    names.append("jets/NjetsEta2")

#    for particle in ["NMuons20","NElectrons20","NLeptons20"]:
#        names.append("leptons/"+particle)

    for process in ["Hbb", "HWW"]:
#        for alg in ["_b2","_d1"]: #["_b1","_b2","_c1","_c2"]:
        for var in ["Pt","Eta","M"]:
            names.append("reco/"+process+"_b2"+var)
            names.append("reco2/"+process+"_d1"+var)

    for name in names:

        c = makeCanvas()
        hist_S = file.Get(stage+name) # signal: HH -> bbWW
        hist_tt = file_tt.Get(stage+name) # BG: tt -> bbWW
        
        if "H" not in name:
            norm(hist_S,hist_tt)
        
        hist_S.Draw()
        hist_tt.Draw("same")
        makeAxes(hist_S,hist_tt)
        
        legend = makeLegend(hist_S,hist_tt,tt=True)
        legend.Draw()

        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(hist_S,hist_tt)
        
        name = name.replace("gen/","basic_tt/"+stage)
        name = name.replace("leptons/","basic_tt/"+stage)
        name = name.replace("jets/","basic_tt/"+stage)
        name = name.replace("res/","basic_tt/"+stage)
        name = name.replace("reco/","reco_tt/"+stage)
        name = name.replace("reco2/","reco_tt/"+stage)
        c.SaveAs(name+".png")
        c.Close()



    ############################
    # overlay "reco" and "gen" #
    ############################

def plotOverlay(stage):
    print "\n  %s: Overlay plots: reco and gen" % stage[:-1]
    
    names2 = [ ]

    names2.extend([("gen/WlnuPt", "reco/Wlnu1Pt"),
                   ("gen/WlnuEta", "reco/Wlnu1Eta"),
                   ("gen/WlnuM", "reco/Wlnu1M"),
                   ("gen/nuPt", "jets/MET")]) # beware of normalization above!

#    names2.extend([("gen/lPt", "leptons/lPt")])

    for process in ["Wjj","HHbbWW"]:
        for alg in ["_b2"]: #["_b1","_b2","_c1","_c2"]:
            for var in ["Pt","Eta","M"]:
                names2.append( ("gen/"+process+var,\
                                "reco/"+process+alg+var))
                                
    for process in ["Wlnu","Wjj","HHbbWW"]:
        for alg in ["_d1"]: #["_b1","_b2","_c1","_c2"]:
            for var in ["Pt","Eta","M"]:
                names2.append( ("gen/"+process+var,\
                                "reco2/"+process+alg+var))

    for gen, reco in names2:

        c = makeCanvas()
        hist_gen = file.Get(stage+gen) # "data"
        hist_reco = file.Get(stage+reco) # "MC"
        hist_reco_tt = file_tt.Get(stage+reco) ## "MC" from tt
        
#        if "MET" in reco:
#            norm(hist_gen,hist_reco,hist_reco_tt)

        hist_reco.Draw("histsame")
        hist_reco_tt.Draw("histsame")
        hist_gen.Draw("P0same")
        makeAxes(hist_reco,hist_reco_tt,hist_gen)
        
        legend = makeLegend(hist_gen,hist_reco,hist_reco_tt,tt=True)
        legend.Draw()
        
        CMS_lumi.CMS_lumi(c,14,33)
        setLineStyle(hist_reco,hist_reco_tt)
        setMarkerStyle(hist_gen)
        
        reco = reco.replace("reco/","reco_tt/"+stage)
        reco = reco.replace("reco2/","reco_tt/"+stage)
        reco = reco.replace("jets/","basic_tt/"+stage)
        c.SaveAs(reco+".png")
        c.Close()



    ############
    # 2D plots #
    ############

def plot2D(stage):
    print "\n  %s: 2D plots" % stage[:-1]


    # WWM signal
    c = makeCanvas(square=True)
    hist = file.Get(stage+"gen/WWM")
    
    hist.Draw()
    makeAxes(hist)
    legend = makeLegend(hist)
    legend.Draw()
    hist.SetMarkerColor(kRed+3)

    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic_tt/"+stage+"WWM.png")
    c.Close()


    # WWM BG
    c = makeCanvas(square=True)
    hist_tt = file_tt.Get(stage+"gen/WWM")
    
    hist_tt.Draw()
    makeAxes(hist_tt)
    legend = makeLegend(hist)
    legend.Draw()
    hist.SetMarkerColor(kRed+3)

    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic_tt/"+stage+"WWM_tt.png")
    c.Close()


    # WWM signal vs BG
    c = makeCanvas(square=True)
    hist = file.Get(stage+"gen/WWM")
    hist_tt = file_tt.Get(stage+"gen/WWM")

    hist_tt.Draw()
    hist.Draw("same")
    makeAxes(hist_tt,hist)
    legend = makeLegend(hist,hist_tt,tt=True)
    legend.Draw()
    hist.SetMarkerColor(kRed+3)
    hist_tt.SetMarkerColor(kAzure+4)

    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic_tt/"+stage+"WWM_both.png")
    c.Close()
    

    # bbWWM signal vs BG
    c = makeCanvas(square=True)
    hist = file.Get(stage+"gen/bbWWM")
    hist_tt = file_tt.Get(stage+"gen/bbWWM")

    hist_tt.Draw()
    hist.Draw("same")
    makeAxes(hist)
    hist.SetMarkerColor(kRed+3)
    hist_tt.SetMarkerColor(kAzure+4)

    CMS_lumi.CMS_lumi(c,14,33)

    c.SaveAs("basic_tt/"+stage+"bbWWM_both.png")
    c.Close()



    ###############
    # extra plots #
    ###############

def plotExtra(stage):
    print "\n  %s: Extra plots" % stage[:-1]
    
    
    # __HH_vs._tt__
    
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


    # __NJetiWMatch__
    c = makeCanvas()
    hist = file.Get(stage+"res/NJetiWMatch")
    norm(hist)
    hist.Draw()
    makeAxes(hist)
    setLineStyle(hist)
    legend = makeLegend(hist,entries="#splitline{jet i matches}{q from W}")
    legend.Draw()

    CMS_lumi.CMS_lumi(c,14,33)
    
    c.SaveAs("basic_tt/"+stage+"NJetiWMatch.png")
    c.Close()


    # __jetWMatchEta_vs._jetWUnMatchEta___
    c = makeCanvas()
    hist = file.Get(stage+"res/jetWMatchEta")
    hist_un = file.Get(stage+"res/jetWUnMatchEta")
    hist.Draw()
    hist_un.Draw("same")
    makeAxes(hist,hist_un)
    setLineStyle(hist,hist_un)
    legend = makeLegend(hist,hist_un,title="jet and q from W",entries=["matched","unmatched"])
    legend.Draw()

    CMS_lumi.CMS_lumi(c,14,33)
    
    c.SaveAs("basic_tt/"+stage+"jetWMatchEta_unscaled.png")
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

    c.SaveAs("basic_tt/"+stage+"WWM_1D.png")
    c.Close()



    ###############
    # Pies, mmmmm #
    ###############

def plotPie(stage):
    print "\n  %s: Pie charts" % stage[:-1]
    
    W = 1200
    H = 1200
    
    c = makeCanvas(square=True)
    hist = file_tt.Get(stage+"gen/NWlnu")
    hist.GetXaxis().SetRangeUser(0, 3)
    pie = TPie(hist)
    pie.SetCircle(.53,.5,.2)
#    pie.SetAngularOffset(200)
    pie.SetEntryRadiusOffset(2,.03)

    labels = [" hadronic"," monoleptonic"," dileptonic"]
    colors = [kAzure-4,kGreen-3,kRed] #kOrange-3
    linecolors = [kAzure-6,kGreen+4,kRed+4] #Orange+4
    pie.SetLabelFormat("#splitline{#scale[1.4]{#font[2]{%txt}}}{#scale[1.2]{  %perc}}")
    pie.SetLabelsOffset(0.026)
    for i in range(3):
        pie.SetEntryFillColor(i,colors[i])
        pie.SetEntryLineColor(i,linecolors[i])
        pie.SetEntryLineWidth(i,1)
        pie.SetEntryLabel(i,labels[i])
    
    if "0" in stage:
        pie.SetEntryRadiusOffset(0,.02)
    else:
        pie.SetEntryRadiusOffset(1,.02)

    pie.Draw("SC>")

    c.SaveAs("basic_tt/"+stage+"branchfraction"+stage[-2]+".png")
    c.Close()



    ########
    # main #
    ########

def main():

    for stage in ["stage_0/","stage_1/","stage_2/","stage_3/","stage_4/"]:
        plotOverlay(stage)
        plotExtra(stage)
        plotBasic(stage)
        plot2D(stage)
        plotPie(stage)

    print "\nDone with this, son.\n"



if __name__ == '__main__':
    main()


